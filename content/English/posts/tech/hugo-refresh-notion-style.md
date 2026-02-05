---
title: "Upgrading My Personal Site with Codex: Notion‑Style Layout, SEO, Cloudflare Cache, and WeChat Sync"
date: 2026-02-04
lastmod: 2026-02-04
draft: false
author: "Danny Yuan"
categories:
  - tech
tags:
  - hugo
  - cloudflare
  - wechat
  - seo
keywords:
  - Hugo
  - Cloudflare Pages
  - WeChat Official Account
  - Static Blog
description: "A full pipeline refresh of my Hugo blog: Notion/Substack‑style typography, TOC sidebar, SEO, CSS cache busting, and WeChat article import."
slug: hugo-refresh-notion-style
comments: true
ShowToc: true
ShowReadingTime: true
ShowWordCounts: true
ShowPageViews: true
ShowLastMod: true
---

My personal website hadn’t been updated for a long time. I spent half a day polishing it from “barely usable” to “something I’m willing to write on long‑term”: Notion/Substack‑like typography, a much better TOC sidebar, stronger SEO and structure, fewer deployment/cache nightmares, and a batch sync from WeChat to my site.

Below is a reusable record of the key actions, for my future self and for anyone who’s also tinkering.

## Goals

1. **Writing & reading experience**: better fonts, sizes, line height, spacing—close to Notion/Substack.
2. **Usable TOC**: doesn’t steal content width, fixed on the right on desktop; hidden on mobile; no empty TOC when there are no headings.
3. **Stable deployment**: local preview OK, online release predictable; style updates no longer “luck‑based.”
4. **Efficient content sync**: batch import WeChat posts by time range, localize images, avoid broken external links.

## Phase 1: Make Local Build Work

First, eliminate the “`hugo server` throws errors immediately” problem so local preview is stable.

Key idea: **local Hugo version may differ from Cloudflare’s build environment**. Newer template functions can fail on older versions in the cloud.

Two fixes:

1. Make templates compatible across Hugo versions (avoid too‑new functions).
2. Pin `HUGO_VERSION` in Cloudflare Pages to match local, reducing environment drift.

![image.png](/notion/hugo-refresh-notion-style/image.png)

## Phase 2: UI & Reading Experience (Notion/Substack)

This was mostly CSS and layout tweaks. The goal was simple: **make it read like an article, not like a web page**.

Notable changes:

- **Unified Chinese/English typography**: adjust base font size, line height, heading spacing so both languages feel relaxed.
- **Image experience**: more vertical breathing room, consistent subtle rounding; cover images handled separately because many themes don’t style them through `.post-content`.
- **Mobile nav button fix**: replace the odd horizontal bar with a standard hamburger (stacked), consistent size and alignment.

![image.png](/notion/hugo-refresh-notion-style/image-1.png)

![image.png](/notion/hugo-refresh-notion-style/image-2.png)

![image.png](/notion/hugo-refresh-notion-style/image-3.png)

## Phase 3: TOC Sidebar

Switching the TOC from a “big block eating content width” to a “floating right‑side component” improved reading flow.

Approach:

1. **Desktop**: fixed on the right, doesn’t squeeze content, default expanded.
2. **Mobile**: hidden (too dense for small screens).
3. **No empty TOC**: if there are no valid headings (or TableOfContents is empty), don’t render the TOC container.

![image.png](/notion/hugo-refresh-notion-style/image-4.png)

![image.png](/notion/hugo-refresh-notion-style/image-5.png)

## Phase 4: SEO & Structure

Static‑site SEO isn’t magic—it’s about completing structured data.

I added the common basics:

1. `title / description / canonical`
2. OpenGraph and Twitter Cards
3. JSON‑LD Schema (Article, Breadcrumb, etc.)
4. robots strategy (allow index in prod; noindex in non‑prod)

## Phase 5: Deployment & Cache (Cloudflare Pages + Custom Domain)

The most “mystical” part was cache: **pages.dev updated, but the custom domain stayed old**.

Two‑step fix:

- **Confirm origin updated**: check `*.pages.dev`; if that’s new, build is fine.
- **Handle custom domain cache**: Purge Cache in Cloudflare; more importantly, make CSS auto‑refresh.

I ended up using **CSS fingerprinting**: each build generates a hashed CSS filename; HTML references change, so the CDN can’t reuse old caches.

One‑line summary: **don’t argue with cache—change the URL and it must refresh.**

![image.png](/notion/hugo-refresh-notion-style/image-6.png)

![image.png](/notion/hugo-refresh-notion-style/image-7.png)

## Phase 6: Cleaner URLs (slug + aliases)

Chinese URLs get encoded (e.g. `%E9%9D%A2%E8%AF%95`). It works but isn’t pretty.

My approach:

1. New posts always set `slug` (short English links).
2. Old links preserved via `aliases` redirects.

Example:

```yaml
slug: gyg-interview-1
aliases:
  - /zh/posts/tech/gyg%E9%9D%A2%E8%AF%951/
```

New links look clean; old ones won’t 404.

![image.png](/notion/hugo-refresh-notion-style/image-8.png)

## Phase 7: Batch Import WeChat Articles

This was the main problem: WeChat had content, but the personal site was stale.

My flow:

1. Collect a list of WeChat article links within a time range.
2. Local script fetches content into `content/Chinese/posts/...`.
3. Auto‑set WeChat cover as Hugo `cover`.
4. Download images to `static/wechat/<slug>/` and replace external links with local paths (avoid the “image from WeChat platform” watermark).
5. Deduplicate: remove the first import without images, keep the localized version.

Now future WeChat updates are one‑click sync: drop links into the list and run the script.

![image.png](/notion/hugo-refresh-notion-style/image-9.png)

## Today’s Output Checklist

1. Local preview and build stable
2. UI typography closer to Notion/Substack
3. TOC floating sidebar + mobile hidden + empty TOC suppressed
4. Fixed Cloudflare custom‑domain cache showing old styles
5. CSS auto‑refresh (fingerprint)
6. `slug` + `aliases` for clean URLs with backward compatibility
7. WeChat batch import + image localization + dedupe + category clean‑up

All of this was done by talking to Codex in natural language—no code written by hand.

Visit the site: [https://yfreetime.com/](https://yfreetime.com/)

![image.png](/notion/hugo-refresh-notion-style/image-10.png)
