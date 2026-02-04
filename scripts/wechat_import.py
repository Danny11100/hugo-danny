#!/usr/bin/env python3
"""
WeChat -> Hugo importer (lightweight, standard-lib only).
- Reads a list of article URLs
- Fetches HTML, extracts title/date/cover/content
- Writes Hugo Markdown files into content/Chinese/posts/life
- Optionally downloads images to static/wechat/<slug>/

Usage:
  python3 scripts/wechat_import.py \
    --urls wechat_urls.txt \
    --from 2026-01-01 --to 2026-02-04 \
    --category life \
    --download-images
"""

from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import ssl

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


def fetch(url: str, insecure: bool = False) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    ctx = None
    if insecure:
        ctx = ssl._create_unverified_context()
    else:
        try:
            import certifi  # type: ignore
            ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            ctx = None
    with urlopen(req, context=ctx) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def extract_meta(html_text: str, prop: str) -> str:
    pattern = re.compile(
        rf'<meta[^>]+property=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    m = pattern.search(html_text)
    if not m:
        return ""
    return html.unescape(m.group(1)).strip()


def extract_title(html_text: str) -> str:
    title = extract_meta(html_text, "og:title")
    if title:
        return title
    m = re.search(r"<title>(.*?)</title>", html_text, re.S | re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def parse_date(value: str) -> Optional[datetime]:
    value = (value or "").strip()
    if not value:
        return None

    # ISO or date-like
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    # Unix timestamp (seconds or ms)
    if re.fullmatch(r"\d{10,13}", value):
        ts = int(value)
        if len(value) == 13:
            ts = ts // 1000
        return datetime.fromtimestamp(ts)

    return None


def extract_publish_date(html_text: str) -> Optional[datetime]:
    for prop in ("article:published_time", "og:published_time"):
        dt = parse_date(extract_meta(html_text, prop))
        if dt:
            return dt

    # Fallbacks from inline JS
    for pattern in (
        r"var\s+publish_time\s*=\s*\"(\d+)\"",
        r"var\s+ct\s*=\s*\"(\d+)\"",
        r"\"publish_time\"\s*:\s*\"(\d+)\"",
    ):
        m = re.search(pattern, html_text)
        if m:
            dt = parse_date(m.group(1))
            if dt:
                return dt

    return None


def extract_content(html_text: str) -> str:
    # Try js_content block
    m = re.search(r'<div[^>]+id=["\']js_content["\'][^>]*>(.*?)</div>', html_text, re.S | re.I)
    if not m:
        # Try rich_media_content
        m = re.search(r'<div[^>]+class=["\']rich_media_content["\'][^>]*>(.*?)</div>', html_text, re.S | re.I)
    if not m:
        return ""

    content = m.group(1)
    content = re.sub(r"<script.*?>.*?</script>", "", content, flags=re.S | re.I)
    content = re.sub(r"<style.*?>.*?</style>", "", content, flags=re.S | re.I)

    # Normalize image src
    content = re.sub(r"data-src=", "src=", content)
    return content.strip()


def slugify(title: str, dt: Optional[datetime], url: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    if base:
        return base[:80]
    date_part = dt.strftime("%Y%m%d") if dt else "nodate"
    short = hashlib.sha1(url.encode("utf-8")).hexdigest()[:6]
    return f"wx-{date_part}-{short}"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for i in range(1, 200):
        candidate = path.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
    return path


def download_image(url: str, dest: Path, insecure: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = html.unescape(url)
    req = Request(url, headers={
        "User-Agent": USER_AGENT,
        "Referer": "https://mp.weixin.qq.com/",
    })
    ctx = ssl._create_unverified_context() if insecure else None
    with urlopen(req, context=ctx) as resp:
        data = resp.read()
    dest.write_bytes(data)


def guess_ext(url: str) -> str:
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return ext
    return ".jpg"


def parse_input_urls(path: Path) -> List[Tuple[Optional[datetime], str]]:
    items: List[Tuple[Optional[datetime], str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Allow "YYYY-MM-DD <url>" or just "url"
        parts = line.split()
        if len(parts) >= 2 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]):
            dt = parse_date(parts[0])
            items.append((dt, parts[-1]))
        else:
            items.append((None, line))
    return items


def in_range(dt: Optional[datetime], start: Optional[date], end: Optional[date]) -> bool:
    if not dt:
        return True
    d = dt.date()
    if start and d < start:
        return False
    if end and d > end:
        return False
    return True


def esc_yaml(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\"", "\\\"")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", default="wechat_urls.txt", help="Path to URLs list")
    parser.add_argument("--from", dest="date_from", default=None, help="YYYY-MM-DD")
    parser.add_argument("--to", dest="date_to", default=None, help="YYYY-MM-DD")
    parser.add_argument("--out", default="content/Chinese/posts/life", help="Output directory")
    parser.add_argument("--category", default="life", help="Default category")
    parser.add_argument("--download-images", action="store_true", help="Download images locally")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL verification (not recommended)")
    parser.add_argument("--save-fail-html", action="store_true", help="Save raw html when parsing fails")
    args = parser.parse_args()

    urls_path = Path(args.urls)
    if not urls_path.exists():
        print(f"URLs file not found: {urls_path}", file=sys.stderr)
        return 1

    date_from = parse_date(args.date_from).date() if args.date_from else None
    date_to = parse_date(args.date_to).date() if args.date_to else None

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    items = parse_input_urls(urls_path)
    for hinted_dt, url in items:
        print(f"Processing: {url}")
        try:
            html_text = fetch(url, insecure=args.insecure)
        except Exception as exc:
            print(f"  Skip: fetch failed ({exc})", file=sys.stderr)
            continue

        title = extract_title(html_text)
        if not title:
            print(f"  Skip: cannot read title", file=sys.stderr)
            continue

        published_dt = hinted_dt or extract_publish_date(html_text)
        if not in_range(published_dt, date_from, date_to):
            print("  Skip: out of date range")
            continue

        cover_url = extract_meta(html_text, "og:image")
        description = extract_meta(html_text, "og:description")

        content = extract_content(html_text)
        if not content:
            if args.save_fail_html:
                debug_dir = Path("wechat_debug")
                debug_dir.mkdir(parents=True, exist_ok=True)
                debug_file = debug_dir / f"{hashlib.sha1(url.encode('utf-8')).hexdigest()}.html"
                debug_file.write_text(html_text, encoding="utf-8", errors="ignore")
                print(f"  Saved debug html: {debug_file}")
            if any(token in html_text for token in ("访问过于频繁", "此内容因违规无法查看", "暂无法查看", "已停止访问")):
                print("  Skip: blocked by WeChat (anti-crawl or restricted)", file=sys.stderr)
            else:
                print(f"  Skip: cannot parse content", file=sys.stderr)
            continue

        # image processing
        img_map: Dict[str, str] = {}
        if args.download_images:
            img_dir = Path("static/wechat") / slugify(title, published_dt, url)
            img_dir.mkdir(parents=True, exist_ok=True)

            img_urls = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.I)
            for idx, img_url in enumerate(dict.fromkeys(img_urls), start=1):
                ext = guess_ext(img_url)
                filename = f"img-{idx:02d}{ext}"
                dest = img_dir / filename
                try:
                    download_image(img_url, dest, insecure=args.insecure)
                    web_path = f"/wechat/{img_dir.name}/{filename}"
                    img_map[img_url] = web_path
                except Exception as exc:
                    print(f"  Warn: failed to download image: {img_url} ({exc})")

            # cover image
            if cover_url:
                ext = guess_ext(cover_url)
                cover_name = f"cover{ext}"
                cover_dest = img_dir / cover_name
                try:
                    download_image(cover_url, cover_dest, insecure=args.insecure)
                    img_map[cover_url] = f"/wechat/{img_dir.name}/{cover_name}"
                except Exception as exc:
                    print(f"  Warn: failed to download cover: {cover_url} ({exc})")

        # replace image urls in content
        for src, local in img_map.items():
            content = content.replace(src, local)

        slug = slugify(title, published_dt, url)
        filename = ensure_unique_path(out_dir / f"{slug}.md")

        date_str = published_dt.strftime("%Y-%m-%d") if published_dt else datetime.now().strftime("%Y-%m-%d")
        front_matter = [
            "---",
            f"title: \"{esc_yaml(title)}\"",
            f"date: {date_str}",
            f"lastmod: {date_str}",
            "draft: false",
            "author: \"Danny Yuan\"",
            f"categories:\n  - {args.category}",
            "tags: []",
            f"slug: {slug}",
            "comments: true",
            "showToc: true",
            "ShowReadingTime: true",
            "ShowWordCounts: true",
            "ShowPageViews: true",
            "ShowLastMod: true",
        ]

        if cover_url:
            cover_image = img_map.get(cover_url, cover_url)
            front_matter += [
                "cover:",
                f"  image: \"{cover_image}\"",
                "  caption: \"\"",
                "  alt: \"\"",
                "  relative: false",
            ]

        if description:
            front_matter.append(f"description: \"{esc_yaml(description)}\"")

        front_matter += ["---", "", content.strip(), ""]

        filename.write_text("\n".join(front_matter), encoding="utf-8")
        print(f"  Saved: {filename}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
