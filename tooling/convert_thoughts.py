#!/usr/bin/env python3
"""Convert the al-folio thoughts page into structured JSON for the new site.

Rules (agreed 2026-07-19):
- Quote credited to a person (incl. Anonymous, books, films) -> "others" tab.
- No attribution, or attribution that is only a date stamp -> "mine" tab.
- Grouped by year. Month headers in the source give the year; the undated
  block at the top is the current year; the legacy block after the last
  month header is 2025.
"""

import json
import re
from pathlib import Path

SRC = Path("/Users/monishver/monishver11.github.io/_pages/thoughts.md")
OUT = Path(__file__).resolve().parent.parent / "astro/src/data/thoughts.json"

DATE_RE = re.compile(r"^[-–—\s]*\d{1,2}/\d{1,2}/\d{2,4}\.?$")

text = SRC.read_text()

# Walk the document in order, tracking the year from month headers.
tokens = re.split(r'(#{2,6}\s+\*\*[^*]+\*\*)', text)
entries = []
year = 2026  # undated leading block is the newest

def parse_quotes(chunk, year):
    out = []
    for m in re.finditer(r'<div class="small-quote">(.*?)</div>', chunk, re.S):
        inner = m.group(1)
        paras = [
            " ".join(p.split())
            for p in re.findall(r"<p>(.*?)</p>", inner, re.S)
        ]
        authors = [
            " ".join(a.split()).lstrip("-–— ").rstrip(".")
            for a in re.findall(r'<span class="author">(.*?)</span>', inner, re.S)
        ]
        if not paras:
            continue
        # strip inner html tags except strong
        paras = [re.sub(r"</?(?!strong)[a-z]+[^>]*>", "", p) for p in paras]
        date_authors = [a for a in authors if DATE_RE.match(a)]
        real_authors = [a for a in authors if not DATE_RE.match(a)]
        out.append(
            {
                "text": "\n\n".join(paras),
                "author": " / ".join(real_authors) if real_authors else None,
                "mine": not real_authors,
                "year": year,
            }
        )
    return out

for tok in tokens:
    header = re.match(r"#{2,6}\s+\*\*([^*]+)\*\*", tok)
    if header:
        ym = re.search(r"(\d{4})", header.group(1))
        if ym:
            year = int(ym.group(1))
        continue
    # The legacy block after the July 2025 section is separated by a --- rule;
    # items there carry 2025 dates. The year variable already holds 2025 by
    # the time we reach it, so nothing special needed.
    entries.extend(parse_quotes(tok, year))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(entries, indent=1, ensure_ascii=False))
mine = sum(1 for e in entries if e["mine"])
print(f"{len(entries)} quotes -> {OUT.name} ({mine} mine, {len(entries)-mine} others)")
