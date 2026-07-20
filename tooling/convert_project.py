#!/usr/bin/env python3
"""Convert al-folio _projects entries to the site-v2 projects collection.

Projects are a portfolio gallery, separate from blog posts: each carries a
thumbnail and an `importance` used for ordering. The body pipeline is identical
to posts, so this reuses convert_post.transform_body and gets every math/figure
fix for free.

Output: astro/src/content/projects/<slug>.md (+ images copied to public/img).

The _projects filenames are 1_project.md ... 5_project.md, which make terrible
URLs, so SLUGS maps each to a real slug.

Usage: python3 tooling/convert_project.py /path/to/_projects/*.md
"""

import json
import re
import sys
from pathlib import Path

import convert_post as cp

OUT_DIR = Path(__file__).resolve().parent.parent / "astro/src/content/projects"

SLUGS = {
    "1_project": "mta-transit-prediction",
    "2_project": "gaze-guided-rl",
    "3_project": "swap-regret",
    "4_project": "smallgraph-gcn",
    "5_project": "single-gpu-moe",
}


def convert(path):
    fm, body = cp.parse_frontmatter(path.read_text())
    stem = path.stem
    slug = SLUGS.get(stem, re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-"))

    # al-folio project frontmatter is unquoted plain scalars.
    title = fm.get("title", slug).strip()
    desc = fm.get("description", "").strip()
    importance = fm.get("importance", "99").strip()
    thumb_rel = re.sub(r"^assets/img/", "", fm.get("img", "").strip())

    if thumb_rel:
        cp.copy_image(thumb_rel)

    body = cp.transform_body(body)

    thumb = "/img/" + thumb_rel if thumb_rel else ""
    fm_new = (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"description: {json.dumps(desc, ensure_ascii=False)}\n"
        f"thumb: {json.dumps(thumb)}\n"
        f"importance: {importance}\n"
        "---\n"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slug}.md"
    out.write_text(fm_new + body.lstrip("\n"))
    print(f"wrote {out.relative_to(OUT_DIR.parent.parent.parent.parent)} (importance {importance})")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p = Path(arg)
        print(f"converting {p.name}")
        convert(p)
