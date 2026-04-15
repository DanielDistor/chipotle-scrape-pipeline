# Design: Save Firecrawl Results to knowledge/raw/

**Date:** 2026-04-15
**File:** `scrape_pipeline.py`

## What We're Building

Extend the existing Step 01 parse block in `scrape_pipeline.py` to loop over Firecrawl results and write one markdown file per result into `knowledge/raw/`.

## Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Filename format | `NN-slug.md` (zero-padded index + title slug) | Prevents collisions when multiple results share a title; sorts in order |
| File header | Source URL on line 1 | Provenance — lets Claude Code cite the origin when reading knowledge/raw/ later |
| Empty markdown | Skip the result entirely | A zero-byte file is worse than no file |
| Code placement | Inline after parse block in same file | Tutorial expects a single scrape_pipeline.py; ~10 lines doesn't warrant extraction |

## Implementation

Add directly after the existing `for r in results` print loop:

1. `Path("knowledge/raw").mkdir(parents=True, exist_ok=True)` — create output dir if missing
2. Loop over `results` with `enumerate(results, start=1)`
3. Skip any result where `r.get("markdown")` is falsy
4. Slugify title: lowercase, `re.sub` non-alphanumeric to hyphens, strip/collapse hyphens
5. Filename: `f"{i:02d}-{slug}.md"`
6. Write: source URL on line 1, then markdown content

Uses existing imports (`re`, `Path`) already in the file.
