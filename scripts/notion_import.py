#!/usr/bin/env python3
"""
Notion Markdown export -> Hugo post helper (stdlib only).

What it does:
- Moves Notion-style front matter (often placed after a leading "# Title") to the top so Hugo can parse it.
- Also supports Notion exports with top properties lines like "Date: February 6, 2026" / "slug: ..." / "Category: ...".
- Copies referenced local images into static/notion/<slug>/ (renaming to URL-safe filenames).
- Rewrites Markdown image links to /notion/<slug>/<filename> (consistent with existing posts in this repo).

Typical usage:
  python3 scripts/notion_import.py \
    --md "notion_export/part1/Some Post abc123.md" \
    --lang zh \
    --category tech

If the source Markdown has no YAML front matter, provide --title/--date/--slug (or at least --date).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import unquote


LANG_TO_CONTENT_DIR: Dict[str, str] = {
    "zh": "content/Chinese",
    "en": "content/English",
}


def _today_iso() -> str:
    return date.today().isoformat()


def slugify(value: str, fallback: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", (value or "").lower()).strip("-")
    return base[:80] if base else fallback


def parse_human_date(value: str) -> Optional[str]:
    value = (value or "").strip()
    if not value:
        return None

    # ISO
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value

    # e.g. "February 6, 2026"
    m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", value)
    if m:
        month_name = m.group(1).lower()
        day = int(m.group(2))
        year = int(m.group(3))
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        month = months.get(month_name)
        if month:
            return f"{year:04d}-{month:02d}-{day:02d}"

    return None


def normalize_filename(name: str) -> str:
    name = name.strip().replace("\\", "/")
    name = name.rsplit("/", 1)[-1]
    stem, dot, ext = name.partition(".")
    ext = ext.lower() if dot else ""

    stem = stem.strip().lower()
    stem = re.sub(r"\s+", "-", stem)
    stem = re.sub(r"[^a-z0-9._-]+", "-", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("-")

    if not stem:
        stem = "file"
    if ext:
        return f"{stem}.{ext}"
    return stem


def parse_front_matter_value(front_matter: str, key: str) -> Optional[str]:
    # Very small YAML "parser": extracts simple "key: value" scalars.
    # Good enough for this repo's front matter (slug/title/date).
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", re.MULTILINE)
    m = pattern.search(front_matter)
    if not m:
        return None
    raw = m.group(1).strip()
    if raw.startswith(("'", '"')) and raw.endswith(("'", '"')) and len(raw) >= 2:
        return raw[1:-1].strip()
    return raw


@dataclass
class FrontMatterSplit:
    front_matter: str
    body: str
    found: bool


def split_front_matter(text: str) -> FrontMatterSplit:
    lines = text.splitlines(keepends=True)
    if not lines:
        return FrontMatterSplit(front_matter="", body="", found=False)

    def first_nonempty_index(start: int = 0) -> Optional[int]:
        for i in range(start, len(lines)):
            if lines[i].strip():
                return i
        return None

    first_idx = first_nonempty_index(0)
    if first_idx is None:
        return FrontMatterSplit(front_matter="", body=text, found=False)

    # Case 1: front matter already at the top
    if lines[first_idx].strip() == "---":
        end = _find_front_matter_end(lines, first_idx + 1)
        if end is None:
            return FrontMatterSplit(front_matter="", body=text, found=False)
        fm = "".join(lines[first_idx : end + 1]).rstrip() + "\n"
        body = "".join(lines[end + 1 :]).lstrip("\n")
        return FrontMatterSplit(front_matter=fm, body=body, found=True)

    # Case 2: Notion export: a leading "# Title" then YAML block
    if lines[first_idx].lstrip().startswith("#"):
        after_heading = first_nonempty_index(first_idx + 1)
        if after_heading is not None and lines[after_heading].strip() == "---":
            end = _find_front_matter_end(lines, after_heading + 1)
            if end is None:
                return FrontMatterSplit(front_matter="", body=text, found=False)
            fm = "".join(lines[after_heading : end + 1]).rstrip() + "\n"
            body = "".join(lines[end + 1 :]).lstrip("\n")
            return FrontMatterSplit(front_matter=fm, body=body, found=True)

    return FrontMatterSplit(front_matter="", body=text, found=False)


def split_notion_properties(text: str) -> Tuple[Dict[str, str], str]:
    """
    Handles Notion exports that start like:

      # Title

      Date: February 6, 2026
      slug: howmuch.tax
      Category: observation

      ...content...
    """
    lines = text.splitlines(keepends=True)
    if not lines:
        return {}, text

    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Skip leading H1 if present
    if i < len(lines) and re.match(r"^\s*#\s+.+", lines[i]):
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1

    props: Dict[str, str] = {}
    start = i
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            break
        m = re.match(r"^([A-Za-z][A-Za-z0-9 _-]{0,30})\s*:\s*(.*?)\s*$", stripped)
        if not m:
            props = {}
            i = start
            break
        key = m.group(1).strip().lower().replace(" ", "_")
        props[key] = m.group(2).strip()
        i += 1

    if not props:
        return {}, text

    # Skip the blank line after properties
    while i < len(lines) and not lines[i].strip():
        i += 1

    body = "".join(lines[i:])
    return props, body


def _find_front_matter_end(lines: List[str], start: int) -> Optional[int]:
    for i in range(start, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def build_front_matter(
    title: str,
    dt: str,
    slug: str,
    author: str,
    category: str,
    draft: bool,
) -> str:
    draft_str = "true" if draft else "false"
    safe_title = title.replace('"', '\\"')
    safe_author = author.replace('"', '\\"')
    safe_slug = slug.replace('"', '\\"')
    safe_category = category.replace('"', '\\"')
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        f"date: {dt}\n"
        f"lastmod: {dt}\n"
        f"draft: {draft_str}\n"
        f'author: "{safe_author}"\n'
        "categories:\n"
        f"  - {safe_category}\n"
        "tags: []\n"
        f"slug: {safe_slug}\n"
        "comments: true\n"
        "ShowToc: true\n"
        "ShowReadingTime: true\n"
        "ShowWordCounts: true\n"
        "ShowPageViews: true\n"
        "ShowLastMod: true\n"
        "---\n"
    )


def is_remote_link(url: str) -> bool:
    u = (url or "").strip().lower()
    return (
        u.startswith("http://")
        or u.startswith("https://")
        or u.startswith("data:")
        or u.startswith("mailto:")
        or u.startswith("#")
        or u.startswith("/")
    )


def split_md_dest_and_title(raw: str) -> Tuple[str, str]:
    s = (raw or "").strip()
    if s.startswith("<") and s.endswith(">") and len(s) >= 2:
        return s[1:-1].strip(), ""

    # Try parse `(dest "title")` / `(dest 'title')`
    m = re.match(r'^(?P<dest>\S+)\s+(?P<title>"[^"]*"|\'[^\']*\')\s*$', s)
    if m:
        return m.group("dest"), " " + m.group("title")

    return s, ""


def rewrite_and_copy_images(
    markdown: str,
    src_md_path: Path,
    slug: str,
    static_root: Path,
    asset_dir: str,
    dry_run: bool,
) -> Tuple[str, int]:
    md_dir = src_md_path.parent
    dest_dir = static_root / asset_dir / slug
    replaced = 0

    img_pattern = re.compile(r"!\[(?P<alt>[^\]]*)]\((?P<target>[^)]+)\)")

    def repl(match: re.Match[str]) -> str:
        nonlocal replaced
        alt = match.group("alt")
        raw_target = match.group("target")
        dest_raw, title_part = split_md_dest_and_title(raw_target)
        if is_remote_link(dest_raw):
            return match.group(0)

        decoded = unquote(dest_raw)
        candidate = (md_dir / decoded).resolve()
        if not candidate.exists():
            # Try without leading "./"
            decoded2 = decoded.lstrip("./")
            candidate = (md_dir / decoded2).resolve()
        if not candidate.exists() or not candidate.is_file():
            return match.group(0)

        new_name = normalize_filename(candidate.name)
        dest_path = dest_dir / new_name

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if dest_path.exists():
                # If already exists but content differs, disambiguate deterministically.
                if dest_path.read_bytes() != candidate.read_bytes():
                    digest = hashlib.sha1(candidate.read_bytes()).hexdigest()[:8]
                    dest_path = dest_dir / f"{dest_path.stem}-{digest}{dest_path.suffix}"
            if not dest_path.exists():
                dest_path.write_bytes(candidate.read_bytes())

        replaced += 1
        new_url = f"/{asset_dir}/{slug}/{dest_path.name}"
        return f"![{alt}]({new_url}{title_part})"

    new_md = img_pattern.sub(repl, markdown)
    return new_md, replaced


def resolve_output_path(repo_root: Path, lang: str, category: str, slug: str) -> Path:
    content_dir = LANG_TO_CONTENT_DIR.get(lang)
    if not content_dir:
        raise ValueError(f"Unsupported --lang {lang!r}. Use one of: {', '.join(sorted(LANG_TO_CONTENT_DIR))}")
    return repo_root / content_dir / "posts" / category / f"{slug}.md"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True, help="Path to Notion-exported Markdown file")
    parser.add_argument("--lang", default="zh", choices=sorted(LANG_TO_CONTENT_DIR.keys()))
    parser.add_argument("--category", required=True, help="Hugo posts/<category> directory (e.g. tech/life)")
    parser.add_argument("--asset-dir", default="notion", help="Folder under static/ to store images (default: notion)")
    parser.add_argument("--slug", default="", help="Override slug (defaults to front matter slug)")
    parser.add_argument("--title", default="", help="Only used if source has no YAML front matter")
    parser.add_argument("--date", dest="dt", default="", help="Only used if source has no YAML front matter (YYYY-MM-DD)")
    parser.add_argument("--author", default="Danny Yuan", help="Only used if source has no YAML front matter")
    parser.add_argument("--draft", default="false", choices=["true", "false"], help="Only used if source has no YAML front matter")
    parser.add_argument("--out", default="", help="Write to this exact output path (overrides lang/category/slug)")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes but do not write files")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    src_md_path = (Path.cwd() / args.md).resolve() if not Path(args.md).is_absolute() else Path(args.md).resolve()
    if not src_md_path.exists():
        print(f"ERROR: source markdown not found: {src_md_path}", file=sys.stderr)
        return 2

    src_text = src_md_path.read_text(encoding="utf-8", errors="replace")
    split = split_front_matter(src_text)

    front_matter = split.front_matter
    body = split.body

    if not split.found:
        props, body2 = split_notion_properties(src_text)
        title = (args.title or _first_h1(src_text) or src_md_path.stem).strip()
        dt = (args.dt or parse_human_date(props.get("date", "")) or _today_iso()).strip()
        draft = args.draft == "true"
        prop_slug = props.get("slug", "").strip()
        slug = (
            args.slug
            or prop_slug
            or slugify(title, fallback=f"notion-{dt.replace('-', '')}-{_short_hash(src_md_path)}")
        ).strip()
        front_matter = build_front_matter(
            title=title,
            dt=dt,
            slug=slug,
            author=args.author,
            category=args.category,
            draft=draft,
        )
        body = body2 if props else _strip_leading_h1(src_text)
    else:
        slug = (args.slug or parse_front_matter_value(front_matter, "slug") or "").strip()
        if not slug:
            title = parse_front_matter_value(front_matter, "title") or src_md_path.stem
            dt = parse_front_matter_value(front_matter, "date") or _today_iso()
            slug = slugify(title, fallback=f"notion-{dt.replace('-', '')}-{_short_hash(src_md_path)}")
            # Insert slug near the end of the front matter (before closing ---)
            front_matter = _insert_slug(front_matter, slug)

    out_path = Path(args.out).resolve() if args.out else resolve_output_path(repo_root, args.lang, args.category, slug)

    rewritten_body, replaced = rewrite_and_copy_images(
        markdown=body,
        src_md_path=src_md_path,
        slug=slug,
        static_root=repo_root / "static",
        asset_dir=args.asset_dir.strip().strip("/"),
        dry_run=args.dry_run,
    )

    final_text = front_matter.rstrip() + "\n\n" + rewritten_body.lstrip("\n")

    if args.dry_run:
        print(f"[dry-run] would write: {out_path}")
        print(f"[dry-run] would copy images to: {repo_root / 'static' / args.asset_dir / slug}")
        print(f"[dry-run] rewrote {replaced} image link(s)")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_text, encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Copied/relinked {replaced} image(s) -> /{args.asset_dir}/{slug}/")
    return 0


def _first_h1(text: str) -> str:
    for line in text.splitlines():
        m = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return ""


def _strip_leading_h1(text: str) -> str:
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and re.match(r"^\s*#\s+.+", lines[i]):
        i += 1
        # also remove following blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        return "".join(lines[i:])
    return text


def _short_hash(path: Path) -> str:
    return hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:6]


def _insert_slug(front_matter: str, slug: str) -> str:
    if re.search(r"^\s*slug\s*:", front_matter, re.MULTILINE):
        return front_matter
    lines = front_matter.splitlines(keepends=True)
    # Insert before the closing --- (last line with ---)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "---":
            lines.insert(i, f"slug: {slug}\n")
            return "".join(lines)
    return front_matter.rstrip() + f"\nslug: {slug}\n---\n"


if __name__ == "__main__":
    raise SystemExit(main())
