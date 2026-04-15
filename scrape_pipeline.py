import os
import re
import time
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
    print(f"  - {r['title']}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")

# --- Step 02: Loop and save to knowledge/raw/ ---

output_dir = Path("knowledge/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for i, r in enumerate(results, start=1):
    markdown = r.get("markdown")
    if not markdown:
        print(f"  skipping result {i} (no markdown)")
        continue

    title = r.get("title") or f"result-{i}"
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    filename = f"{i:02d}-{slug}.md"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Source: {r['url']}\n\n")
        f.write(markdown)

    print(f"  saved → {filepath}")
