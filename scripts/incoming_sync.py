#!/usr/bin/env python3
"""
incoming/ -> Hugo importer (Chinese source) + English stub creator.

Workflow:
- Drop a folder (or a zip) under incoming/ containing:
  - one or more .md files
  - images referenced by relative links in the markdown
- Run this script to import Chinese posts and create English draft stubs.

Notes:
- This script does NOT machine-translate content (no network/LLM dependency).
  It creates English stubs marked as draft=true, so you can translate later.
- Images are copied to static/incoming/<slug>/ and linked as /incoming/<slug>/...

Usage:
  python3 scripts/incoming_sync.py --apply
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import notion_import


REPO_ROOT = Path(__file__).resolve().parents[1]
INCOMING_DIR = REPO_ROOT / "incoming"
INBOX_DIR = INCOMING_DIR / ".inbox"

KNOWN_CATEGORIES = {"life", "tech", "travel", "observation"}


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


def unpack_incoming_zips(apply: bool) -> List[Path]:
    extracted_dirs: List[Path] = []
    if not INCOMING_DIR.exists():
        return extracted_dirs

    for zip_path in sorted(INCOMING_DIR.glob("*.zip")):
        data = zip_path.read_bytes()
        tag = f"{_safe_dir_name(zip_path.stem)}-{_short_hash_bytes(data)}"
        dest_root = (INBOX_DIR / tag).resolve()
        extracted_dirs.append(dest_root)
        if dest_root.exists():
            continue
        if not apply:
            continue
        dest_root.mkdir(parents=True, exist_ok=True)
        _unpack_zip_bytes(data, dest_root)
        print(f"Unpacked {zip_path.relative_to(REPO_ROOT)} -> {dest_root.relative_to(REPO_ROOT)}")
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


def iter_zip_markdowns(data: bytes) -> List[Tuple[str, str]]:
    """
    Returns list of (name, text) for markdown files found in a zip.
    Supports nested zip entries.
    """
    found: List[Tuple[str, str]] = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if not name or name.endswith("/"):
                continue
            content = z.read(info)
            if name.lower().endswith(".zip"):
                found.extend(iter_zip_markdowns(content))
                continue
            if name.lower().endswith(".md"):
                text = content.decode("utf-8", errors="replace")
                found.append((name, text))
    return found


def summarize_md_text(name: str, text: str, default_category: str) -> str:
    split = notion_import.split_front_matter(text)
    if split.found:
        fm = split.front_matter
        title = (notion_import.parse_front_matter_value(fm, "title") or "").strip().strip("'\"") or notion_import._first_h1(text) or Path(name).stem
        slug = (notion_import.parse_front_matter_value(fm, "slug") or "").strip()
        dt = (notion_import.parse_front_matter_value(fm, "date") or "").strip() or _today_iso()
        category = infer_category(Path(name), fm, default_category)
    else:
        props, _ = notion_import.split_notion_properties(text)
        title = notion_import._first_h1(text) or Path(name).stem
        slug = (props.get("slug") or "").strip()
        dt = notion_import.parse_human_date(props.get("date", "")) or _today_iso()
        category = normalize_category_folder(props.get("category", "") or default_category)

    if not slug:
        slug = notion_import.slugify(title, fallback=f"incoming-{dt.replace('-', '')}-{hashlib.sha1(name.encode('utf-8')).hexdigest()[:6]}")
    return f"{title}  ({dt})  category={category}  slug={slug}"


def parse_yaml_first_list_item(front_matter: str, key: str) -> Optional[str]:
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
            if not re.match(r"^\s+", line):
                break
    return None


def normalize_category_folder(value: str) -> str:
    s = (value or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "life"


def infer_category(md_path: Path, front_matter: str, default_category: str) -> str:
    cat = parse_yaml_first_list_item(front_matter, "categories")
    if cat:
        return normalize_category_folder(cat)

    props, _ = notion_import.split_notion_properties(md_path.read_text(encoding="utf-8", errors="replace"))
    cat2 = (props.get("category") or props.get("categories") or "").strip()
    if cat2:
        return normalize_category_folder(cat2)

    for part in (p.lower() for p in md_path.parts):
        if part in KNOWN_CATEGORIES:
            return part
    return normalize_category_folder(default_category)


@dataclass
class Candidate:
    src: Path
    slug: str
    title: str
    dt: str
    category: str


def build_candidates(md_paths: Iterable[Path], default_category: str) -> List[Candidate]:
    items: List[Candidate] = []
    for md_path in md_paths:
        text = md_path.read_text(encoding="utf-8", errors="replace")
        split = notion_import.split_front_matter(text)
        if split.found:
            fm = split.front_matter
            slug = (notion_import.parse_front_matter_value(fm, "slug") or "").strip()
            title = (notion_import.parse_front_matter_value(fm, "title") or "").strip().strip("'\"") or notion_import._first_h1(text) or md_path.stem
            dt = (notion_import.parse_front_matter_value(fm, "date") or "").strip() or _today_iso()
            category = infer_category(md_path, fm, default_category)
        else:
            props, _ = notion_import.split_notion_properties(text)
            title = notion_import._first_h1(text) or md_path.stem
            slug = (props.get("slug") or "").strip()
            dt = notion_import.parse_human_date(props.get("date", "")) or _today_iso()
            category = normalize_category_folder(props.get("category", "") or default_category)

        if not slug:
            slug = notion_import.slugify(title, fallback=f"incoming-{dt.replace('-', '')}-{notion_import._short_hash(md_path)}")

        items.append(Candidate(src=md_path, slug=slug, title=title, dt=dt, category=category))
    return items


def find_incoming_markdowns() -> List[Path]:
    if not INCOMING_DIR.exists():
        return []
    md_paths = [p for p in INCOMING_DIR.rglob("*.md") if p.is_file()]
    # avoid scanning inbox when it doesn't exist; when it does, include it.
    return sorted(md_paths)


def ensure_en_stub(c: Candidate, apply: bool) -> Optional[Path]:
    dest = notion_import.resolve_output_path(REPO_ROOT, "en", c.category, c.slug)
    if dest.exists():
        return None
    if not apply:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    fm = notion_import.build_front_matter(
        title=c.title,
        dt=c.dt,
        slug=c.slug,
        author="Danny Yuan",
        category=c.category,
        draft=True,
    )
    body = (
        "TODO: Translate this post into English.\n\n"
        f"Chinese version: `/zh/posts/{c.category}/{c.slug}/`\n"
    )
    dest.write_text(fm.rstrip() + "\n\n" + body, encoding="utf-8")
    return dest


def import_zh(c: Candidate, apply: bool, force: bool) -> Tuple[Optional[Path], str]:
    dest = notion_import.resolve_output_path(REPO_ROOT, "zh", c.category, c.slug)
    existed = dest.exists()
    if existed and not force:
        return None, "exists"
    if not apply:
        return dest, "new" if not existed else "overwrite"
    argv = [
        "--md",
        str(c.src),
        "--lang",
        "zh",
        "--category",
        c.category,
        "--asset-dir",
        "incoming",
        "--slug",
        c.slug,
    ]
    rc = notion_import.main(argv)
    if rc != 0:
        raise RuntimeError(f"notion_import failed for {c.src} (rc={rc})")
    return dest, "new" if not existed else "overwrite"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write files (default is report-only)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing destination posts")
    parser.add_argument("--default-category", default="life", help="Used when category is missing")
    args = parser.parse_args(argv)

    if not INCOMING_DIR.exists():
        print("No incoming/ directory found.")
        return 0

    zip_paths = sorted(INCOMING_DIR.glob("*.zip"))
    if args.apply:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
    unpack_incoming_zips(apply=args.apply)

    md_paths = find_incoming_markdowns()
    if not md_paths:
        if zip_paths and not args.apply:
            print(f"Found {len(zip_paths)} zip file(s) under incoming/ (not unpacked in report-only mode).")
            for zp in zip_paths:
                try:
                    md_items = iter_zip_markdowns(zp.read_bytes())
                except Exception as e:
                    print(f"- {zp.name}: failed to read zip ({e})")
                    continue
                if not md_items:
                    print(f"- {zp.name}: no markdown found")
                    continue
                print(f"- {zp.name}:")
                for name, text in md_items[:5]:
                    print(f"  - {summarize_md_text(name, text, args.default_category)}")
            print("\nRe-run with --apply to unpack and import.")
            return 0
        print("No markdown files found under incoming/")
        return 0

    candidates = build_candidates(md_paths, default_category=args.default_category)
    new_items: List[Candidate] = []
    for c in candidates:
        zh_dest = notion_import.resolve_output_path(REPO_ROOT, "zh", c.category, c.slug)
        if zh_dest.exists() and not args.force:
            continue
        new_items.append(c)

    if not new_items:
        print("No new posts to import (all destinations already exist).")
        return 0

    print("New posts:")
    for c in new_items:
        dest = notion_import.resolve_output_path(REPO_ROOT, "zh", c.category, c.slug)
        print(f"- [zh] {dest.relative_to(REPO_ROOT)}  ({c.dt})  {c.title}")

    if not args.apply:
        print("\n(report-only) Re-run with --apply to import and copy images.")
        return 0

    for c in new_items:
        out, status = import_zh(c, apply=True, force=args.force)
        if out:
            print(f"Imported [zh] {out.relative_to(REPO_ROOT)} ({status})")
        stub = ensure_en_stub(c, apply=True)
        if stub:
            print(f"Created stub [en] {stub.relative_to(REPO_ROOT)} (draft)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
