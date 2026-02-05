---
title: "One Book, Four AIs: Different Work Attitudes on the Same Task"
date: 2026-01-28
lastmod: 2026-01-28
draft: false
author: "Danny Yuan"
categories:
  - tech
tags: []
slug: ai
comments: true
showToc: true
ShowReadingTime: true
ShowWordCounts: true
ShowPageViews: true
ShowLastMod: true
cover:
  image: "/wechat/ai/cover.jpg"
  caption: ""
  alt: ""
  relative: false
description: "NotebookLM is boundary‑aware and will stop; GPT looks polished even when it lacks material; Kimi is steady; Manus feels like a real agent you can work with."
---

*(Looks like I picked the wrong book—the previous post got taken down.)*

Recently I downloaded a batch of books—mostly heavy volumes, hundreds of pages each. Many were only available as scans. For humans, that’s fine; for AI, it’s a hostile input format.

This time I tested **Mankiw’s *Principles of Economics***, which covers key macro indicators and mechanisms. It’s well‑structured, but my copy was a scanned PDF with no readable text layer.

My goal was simple: understand what the book is saying and its logic framework. I wasn’t writing a paper or research report, so I chose **PPT** as the output. For me, slides are lighter than a report—they’re for understanding, not presentation. Flipping through slides lets me quickly see what problems the author is solving, which analytical paths are used, and where the causal chains sit. That’s why I didn’t ask for a long essay and explicitly said: **make a PPT**.

I gave the same task to NotebookLM, GPT 5.2, Kimi 2.5 agent, and later Manus:

> Read the book and build a PPT.

## NotebookLM

NotebookLM reacted the most directly. It detected a scan with no usable text layer, said it couldn’t do the task, and stopped. It was disappointing in the moment, but looking back, it was the cleanest choice. It doesn’t pretend to understand just to deliver. You don’t get a PPT, but you also don’t get misled. Because it stays strictly inside the data I provided, hallucinations are almost nonexistent.

![](/wechat/ai/img-01.jpg)

## GPT

GPT was the most uncomfortable experience. It recognized the cover, title, and some preface, then produced a PPT. Formally, it “completed” the task, but the content was obviously shallow: title, author, year, plus a few vague summaries. For a report, low density might be tolerable; for a PPT—where each slide must carry signal—it’s a waste. If it had said upfront that scanned books were impossible, I would respect it more. Poor output is worse than no output.

![](/wechat/ai/img-02.jpg)
![](/wechat/ai/img-03.jpg)

## Kimi

Kimi’s agent was more stable. It ran into the same problem (large file, failed extraction, poor OCR), tried to read the file, confirmed the text layer was unusable, attempted chunking, decided OCR cost was too high, and gave up “full text extraction.” That’s where most models stop. But the agent stepped back and treated the book as a set of pages to be understood. It used the cover, preface, chapter start pages, and author background to infer the core question, the author’s main judgments, and what gets repeated. It supplemented with search, but stayed constrained by the book’s title, author, and topic.

![](/wechat/ai/img-04.jpg)

Still, Kimi solved the “book’s problem,” not **my** problem. When the task shifted from content整理 to building an understanding framework, it felt conservative.

## Manus

The real shift happened when I brought in Manus.

Same task, same output format, but it clearly stood on the other side. Its first step wasn’t processing materials, but understanding the task itself. It aligned on what I actually wanted: summarization vs. framework, completeness vs. judgment. That alignment wasn’t a single confirmation line; it showed up directly in later trade‑offs.

When building slides, Manus focused on what was essential to understand the system, what could be compressed, which models were tools rather than conclusions, and where causal relationships deserved emphasis instead of jargon stacking. It wasn’t answering “what does this page say,” but **why this page should exist**.

![](/wechat/ai/img-05.jpg)

The difference was obvious: Kimi’s PPT felt like a re‑typeset textbook; Manus’s felt like a pair of glasses for understanding.

![](/wechat/ai/img-06.jpg)

Manus also made the process transparent: which information came from the book’s structure, which from external sources, and which was inference. That mattered to me because my goal wasn’t to reproduce the book, but to build a reliable framework quickly under constraints. The result wasn’t perfect, but I always knew **how** the PPT was made and **where its boundaries were**.

If I had to sum them up in one line:

- NotebookLM is a boundary‑aware research assistant. If it can’t, it says so.
- GPT is a polished analyst who will hand in something even when the material is weak.
- Kimi is a steady book‑splitting executor.
- Manus is the agent that feels like you’re actually working together.

**People pay not for token consumption, but for whether results are reliable and the process is transparent.**

One more practical line: every worker can learn from agents. Don’t fake understanding; know your boundaries; switch paths; push the work forward step by step. That’s a rare professional ability.

*Below are the PPTs generated by Kimi and Manus for reference.*

**by Kimi k2.5**

![](/wechat/ai/img-07.jpg)
![](/wechat/ai/img-08.jpg)
![](/wechat/ai/img-09.jpg)
![](/wechat/ai/img-10.jpg)
![](/wechat/ai/img-11.jpg)
![](/wechat/ai/img-12.jpg)
![](/wechat/ai/img-13.jpg)
![](/wechat/ai/img-14.jpg)
![](/wechat/ai/img-15.jpg)
![](/wechat/ai/img-16.jpg)
![](/wechat/ai/img-17.jpg)
![](/wechat/ai/img-18.jpg)
![](/wechat/ai/img-19.jpg)
![](/wechat/ai/img-20.jpg)
![](/wechat/ai/img-21.jpg)
![](/wechat/ai/img-22.jpg)
![](/wechat/ai/img-23.jpg)

**by Manus**

![](/wechat/ai/img-24.jpg)
![](/wechat/ai/img-25.jpg)
![](/wechat/ai/img-26.jpg)
![](/wechat/ai/img-27.jpg)
![](/wechat/ai/img-28.jpg)
![](/wechat/ai/img-29.jpg)
![](/wechat/ai/img-30.jpg)
![](/wechat/ai/img-31.jpg)
![](/wechat/ai/img-32.jpg)
![](/wechat/ai/img-33.jpg)
![](/wechat/ai/img-34.jpg)
