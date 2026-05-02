import os
import re
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("FIRECRAWL_API_KEY")

# --- Step 01: Search + scrape with Firecrawl ---

api_url = "https://api.firecrawl.dev/v2/search"

headers = {
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "query": "Chipotle investor relations press releases",
    "limit": 5,
    "scrapeOptions": {"formats": ["markdown"]}
}

response = requests.post(api_url, headers=headers, json=payload)

print(response)
print(response.text)

data = response.json()
results = data["data"]["web"]
print(f"Firecrawl returned {len(results)} results")

for r in results:
    print(f"  - {r.get('title', '(no title)')}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")

# --- Step 02: Loop and save to knowledge/raw/ ---

def find_existing_file(url, output_dir):
    """Return (filepath, existing_markdown_length) if URL already has a file, else (None, 0)."""
    for filepath in sorted(output_dir.glob("*.md")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line == f"Source: {url}":
                    return filepath, len(f.read())
        except Exception:
            continue
    return None, 0

def next_index(output_dir):
    """Return next available numeric index based on existing NN-slug.md files."""
    indices = []
    for filepath in output_dir.glob("*.md"):
        m = re.match(r"^(\d+)-", filepath.name)
        if m:
            indices.append(int(m.group(1)))
    return (max(indices) + 1) if indices else 1

output_dir = Path("knowledge/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for r in results:
    markdown = r.get("markdown")
    if not markdown:
        print(f"  skipping (no markdown): {r.get('url', '?')}")
        continue

    url = r["url"]
    title = r.get("title") or url

    existing_path, existing_len = find_existing_file(url, output_dir)

    if existing_path and len(markdown) <= existing_len:
        print(f"  keeping existing (not longer): {existing_path.name}")
        continue

    if existing_path:
        filepath = existing_path
        print(f"  overwriting (new is longer): {filepath.name}")
    else:
        idx = next_index(output_dir)
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        filepath = output_dir / f"{idx:02d}-{slug}.md"
        print(f"  saving new: {filepath.name}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Source: {url}\n\n")
        f.write(markdown)
