# Save Results to knowledge/raw/ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `scrape_pipeline.py` to loop over Firecrawl results and write one markdown file per result into `knowledge/raw/`.

**Architecture:** Inline save block appended after the existing parse loop in `scrape_pipeline.py`. Uses `Path` and `re` already imported. Skips results with no markdown. Filenames are zero-padded index + title slug.

**Tech Stack:** Python stdlib (`pathlib.Path`, `re`), no new dependencies.

---

### Task 1: Add save loop to scrape_pipeline.py

**Files:**
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Add the Step 02 save block**

Append the following after the existing `for r in results:` print loop in `scrape_pipeline.py`:

```python
# --- Step 02: Loop and save to knowledge/raw/ ---

output_dir = Path("knowledge/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for i, r in enumerate(results, start=1):
    markdown = r.get("markdown")
    if not markdown:
        print(f"  skipping result {i} (no markdown)")
        continue

    slug = re.sub(r"[^a-z0-9]+", "-", r["title"].lower()).strip("-")
    filename = f"{i:02d}-{slug}.md"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Source: {r['url']}\n\n")
        f.write(markdown)

    print(f"  saved → {filepath}")
```

- [ ] **Step 2: Run the script and verify output**

```bash
venv/bin/python scrape_pipeline.py
```

Expected output includes lines like:
```
  saved → knowledge/raw/01-news-releases-chipotle-mexican-grill.md
  saved → knowledge/raw/02-chipotle-news-releases.md
  ...
```

- [ ] **Step 3: Inspect the files**

```bash
ls knowledge/raw/
```

Expected: up to 5 `.md` files with zero-padded names.

```bash
head -3 knowledge/raw/01-*.md
```

Expected: first line is `Source: https://...`, followed by a blank line, then markdown content.

- [ ] **Step 4: Commit**

```bash
git add scrape_pipeline.py knowledge/raw/
git commit -m "feat: save Firecrawl results to knowledge/raw/ (Step 02)"
```
