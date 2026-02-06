#!/usr/bin/env python3
"""
Scan repo root for Notion exports (md + images, optionally inside zip),
import new posts into Hugo, and keep zh/en in sync.

Defaults are conservative:
- Only imports when the destination post does not exist (unless --force).
- If a post exists in one language but not the other, it creates a draft stub
  in the missing language (unless --no-stubs).

Usage:
  python3 scripts/notion_sync.py --apply

Common options:
  --apply             Actually write files (default is report-only)
  --force             Overwrite existing destination posts
  --no-unpack-zips     Skip unpacking root-level zip exports
  --no-stubs           Do not create missing-language draft stubs
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import notion_import


REPO_ROOT = Path(__file__).resolve().parents[1]


def _today_iso() -> str:
    return date.today().isoformat()


def _safe_dir_name(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "export"


def _short_hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()[:8]


def _safe_join(base: Path, rel: str) -> Path:
    rel = rel.replace("\\", "/")
    rel = rel.lstrip("/")
    rel = rel.replace("\x00", "")
    if ".." in Path(rel).parts:
        raise ValueError(f"Unsafe path traversal in zip entry: {rel!r}")
    return (base / rel).resolve()


def unpack_root_zips(inbox_dir: Path, apply: bool) -> List[Path]:
    """
    Unpacks top-level *.zip files into inbox_dir/<zip-stem>-<hash>/...
    Supports "zip containing ExportBlock-*.zip" (nested zip) patterns too.
    """
    extracted_dirs: List[Path] = []
    for zip_path in sorted(REPO_ROOT.glob("*.zip")):
        data = zip_path.read_bytes()
        tag = f"{_safe_dir_name(zip_path.stem)}-{_short_hash_bytes(data)}"
        dest_root = (inbox_dir / tag).resolve()

        if dest_root.exists():
            extracted_dirs.append(dest_root)
            continue

        if not apply:
            extracted_dirs.append(dest_root)
            continue

        dest_root.mkdir(parents=True, exist_ok=True)
        _unpack_zip_bytes(data, dest_root)
        extracted_dirs.append(dest_root)
        print(f"Unpacked {zip_path} -> {dest_root}")
    return extracted_dirs


def _unpack_zip_bytes(data: bytes, dest_root: Path) -> None:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if not name or name.endswith("/"):
                continue
            content = z.read(info)
            if name.lower().endswith(".zip"):
                _unpack_zip_bytes(content, dest_root)
                continue
            out_path = _safe_join(dest_root, name)
            if not str(out_path).startswith(str(dest_root)):
                raise ValueError(f"Zip entry escaped dest root: {name!r}")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path.exists() and out_path.read_bytes() == content:
                continue
            out_path.write_bytes(content)


def detect_lang(path: Path, front_matter: str) -> str:
    for key in ("lang", "language"):
        v = notion_import.parse_front_matter_value(front_matter, key)
        if v in {"zh", "en"}:
            return v

    p = path.as_posix().lower()
    if "/english/" in p or p.endswith((".en.md", "-en.md", "_en.md")):
        return "en"
    if "/chinese/" in p or p.endswith((".zh.md", "-zh.md", "_zh.md")):
        return "zh"
    return "zh"


def parse_yaml_first_list_item(front_matter: str, key: str) -> Optional[str]:
    # Finds:
    #   key:
    #     - value
    # or:
    #   key:
    #   - value
    in_block = False
    for line in front_matter.splitlines():
        if not in_block:
            if re.match(rf"^\s*{re.escape(key)}\s*:\s*$", line):
                in_block = True
            continue
        m = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip("'\"")
        if line.strip() and not line.lstrip().startswith("#"):
            # stop when leaving the list block
            if not re.match(r"^\s+", line):
                break
    return None


def normalize_category_folder(category: str) -> str:
    s = (category or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "tech"


def parse_property_style(text: str) -> Tuple[Dict[str, str], str]:
    props, body = notion_import.split_notion_properties(text)
    return props, body


@dataclass
class Candidate:
    src: Path
    lang: str
    slug: str
    title: str
    dt: str
    category_folder: str


def build_candidates(md_paths: Iterable[Path]) -> List[Candidate]:
    candidates: List[Candidate] = []
    for md_path in md_paths:
        text = md_path.read_text(encoding="utf-8", errors="replace")
        split = notion_import.split_front_matter(text)
        if split.found:
            fm = split.front_matter
            lang = detect_lang(md_path, fm)
            slug = (notion_import.parse_front_matter_value(fm, "slug") or "").strip()
            title = (notion_import.parse_front_matter_value(fm, "title") or "").strip().strip("'\"")
            dt = (notion_import.parse_front_matter_value(fm, "date") or "").strip()
            category = parse_yaml_first_list_item(fm, "categories") or "tech"
        else:
            props, _ = parse_property_style(text)
            fm = ""
            lang = detect_lang(md_path, fm)
            title = notion_import._first_h1(text) or md_path.stem
            slug = (props.get("slug", "") or "").strip()
            dt = notion_import.parse_human_date(props.get("date", "")) or _today_iso()
            category = props.get("category", "") or props.get("categories", "") or "tech"

        if not slug:
            slug = notion_import.slugify(title, fallback=f"notion-{dt.replace('-', '')}-{notion_import._short_hash(md_path)}")
        category_folder = normalize_category_folder(category)
        candidates.append(
            Candidate(
                src=md_path,
                lang=lang,
                slug=slug,
                title=title,
                dt=dt,
                category_folder=category_folder,
            )
        )
    return candidates


def find_export_markdowns() -> List[Path]:
    base = REPO_ROOT / "notion_export"
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*.md") if p.is_file())


def ensure_stub(
    lang: str,
    slug: str,
    title: str,
    dt: str,
    category_folder: str,
    apply: bool,
) -> Optional[Path]:
    dest = notion_import.resolve_output_path(REPO_ROOT, lang, category_folder, slug)
    if dest.exists():
        return None
    if not apply:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    body = (
        "TODO: Translate this post.\n\n"
        f"Chinese version: `/zh/posts/{category_folder}/{slug}/`\n"
        f"English version: `/en/posts/{category_folder}/{slug}/`\n"
    )
    fm = notion_import.build_front_matter(
        title=title,
        dt=dt,
        slug=slug,
        author="Danny Yuan",
        category=category_folder,
        draft=True,
    )
    dest.write_text(fm.rstrip() + "\n\n" + body, encoding="utf-8")
    return dest


def import_one(candidate: Candidate, apply: bool, force: bool) -> Tuple[Optional[Path], str]:
    dest = notion_import.resolve_output_path(REPO_ROOT, candidate.lang, candidate.category_folder, candidate.slug)
    existed = dest.exists()
    if existed and not force:
        return None, "exists"
    if not apply:
        return dest, "new" if not existed else "overwrite"

    argv = [
        "--md",
        str(candidate.src),
        "--lang",
        candidate.lang,
        "--category",
        candidate.category_folder,
        "--asset-dir",
        "notion",
    ]
    if force:
        argv.extend(["--out", str(dest)])
    rc = notion_import.main(argv)
    if rc != 0:
        raise RuntimeError(f"notion_import failed for {candidate.src} (rc={rc})")
    return dest, "new" if not existed else "overwrite"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write files (default is report-only)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing destination posts")
    parser.add_argument("--no-unpack-zips", action="store_true", help="Do not unpack repo-root *.zip exports")
    parser.add_argument("--no-stubs", action="store_true", help="Do not create missing-language draft stubs")
    args = parser.parse_args(argv)

    inbox_dir = (REPO_ROOT / "notion_export" / "inbox").resolve()
    if not args.no_unpack_zips:
        inbox_dir.mkdir(parents=True, exist_ok=True)
        unpack_root_zips(inbox_dir=inbox_dir, apply=args.apply)

    md_paths = find_export_markdowns()
    if not md_paths:
        print("No Notion export markdowns found under notion_export/")
        return 0

    candidates = build_candidates(md_paths)

    new_items: List[Tuple[str, Path, Candidate]] = []
    skipped = 0
    for c in candidates:
        dest = notion_import.resolve_output_path(REPO_ROOT, c.lang, c.category_folder, c.slug)
        if dest.exists() and not args.force:
            skipped += 1
            continue
        new_items.append((c.lang, dest, c))

    if not new_items:
        print("No new posts to import (all destinations already exist).")
    else:
        print("New posts:")
        for lang, dest, c in new_items:
            print(f"- [{lang}] {dest.relative_to(REPO_ROOT)}  ({c.dt})  {c.title}")

    if not args.apply:
        print("\n(report-only) Re-run with --apply to import and copy images.")
        return 0

    imported: List[Path] = []
    for _, _, c in new_items:
        dest = notion_import.resolve_output_path(REPO_ROOT, c.lang, c.category_folder, c.slug)
        if dest.exists() and not args.force:
            continue
        out, status = import_one(c, apply=True, force=args.force)
        if out:
            imported.append(out)
            print(f"Imported [{c.lang}] {out.relative_to(REPO_ROOT)} ({status})")

        if args.no_stubs:
            continue

        other_lang = "en" if c.lang == "zh" else "zh"
        stub = ensure_stub(
            lang=other_lang,
            slug=c.slug,
            title=c.title,
            dt=c.dt,
            category_folder=c.category_folder,
            apply=True,
        )
        if stub:
            print(f"Created stub [{other_lang}] {stub.relative_to(REPO_ROOT)} (draft)")

    if skipped:
        print(f"Skipped existing posts: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
