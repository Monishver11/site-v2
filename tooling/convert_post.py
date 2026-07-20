#!/usr/bin/env python3
"""Convert an al-folio Jekyll post to the site-v2 Astro blog collection.

Usage: convert_post.py <jekyll_post.md> ...

- Maps frontmatter (title/date/description/tags/categories) to the new schema.
- Old course categories map to the new topic taxonomy.
- Kramdown renders $$...$$ as inline math when it appears inside a line of
  text; remark-math treats every $$ as display. So inline occurrences are
  rewritten to $...$, while $$ blocks standing on their own lines stay.
- Rewrites /assets/img/... references to /img/... and copies the images.
- Drops Jekyll-only frontmatter and liquid include lines (reported, not
  silently swallowed).
"""

import re
import shutil
import sys
from pathlib import Path

JEKYLL_ROOT = Path("/Users/monishver/monishver11.github.io")
OUT_DIR = Path(__file__).resolve().parent.parent / "astro/src/content/blog"
IMG_OUT = Path(__file__).resolve().parent.parent / "astro/public/img"

CATEGORY_MAP = {
    "ML-NYU": "ML Theory",
    "ADV-ML-NYU": "ML Theory",
    "RL-NYU": "ML Theory",
    "DS-NYU": "ML Theory",
    "GPU-NYU": "GPU & Performance",
    "LLMR-NYU": "GPU & Performance",
    "RBDA-NYU": "Big Data Systems",
}


def parse_frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        sys.exit("no frontmatter found")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end() :]


def promote_headings(body):
    """al-folio posts use ####/##### as their top heading levels, which render
    tiny. Shift every heading up so the shallowest level in the post is h2,
    preserving relative hierarchy. Skips fenced code blocks."""
    lines = body.split("\n")
    levels = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence:
            m = re.match(r"^(#{1,6})\s", line)
            if m:
                levels.append(len(m.group(1)))
    if not levels:
        return body
    shift = min(levels) - 2
    if shift <= 0:
        return body
    out = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        m = re.match(r"^(#{1,6})(\s.*)$", line)
        if m and not in_fence:
            out.append("#" * max(2, len(m.group(1)) - shift) + m.group(2))
        else:
            out.append(line)
    return "\n".join(out)


def split_dangling_delimiters(body):
    """A closing $$ with trailing prose on the same line breaks remark-math.
    Move the trailing text to its own line."""
    out = []
    for line in body.split("\n"):
        m = re.match(r"^(\s*)\$\$\s+(\S.*)$", line)
        if m and "$$" not in m.group(2):
            out.append(f"{m.group(1)}$$")
            out.append("")
            out.append(f"{m.group(1)}{m.group(2)}")
        else:
            out.append(line)
    return "\n".join(out)


def convert_inline_math(body):
    """$$...$$ on its own line(s) = display, keep. $$...$$ inside a text line = inline, convert to $...$."""
    out_lines = []
    for line in body.split("\n"):
        stripped = line.strip()
        # A pure display line: starts and ends the block delimiters alone,
        # or the line is exactly "$$".
        if stripped == "$$" or (
            stripped.startswith("$$")
            and stripped.endswith("$$")
            and len(stripped) > 2
            and stripped.count("$$") == 2
        ):
            out_lines.append(line)
            continue
        # Inline occurrences within a sentence line.
        line = re.sub(r"\$\$\s*(.+?)\s*\$\$", lambda m: f"${m.group(1)}$", line)
        out_lines.append(line)
    return "\n".join(out_lines)


def convert(post_path):
    text = post_path.read_text()
    fm, body = parse_frontmatter(text)

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post_path.stem)
    date = fm.get("date") or post_path.stem[:10]
    title = fm.get("title", slug)
    desc = fm.get("description", "")
    tags = [t for t in fm.get("tags", "").split() if t]
    old_cat = fm.get("categories", "").strip()
    category = CATEGORY_MAP.get(old_cat, "Projects")

    # figure.liquid includes become plain markdown images.
    def fig_sub(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
        path = attrs.get("path", "")
        rel = re.sub(r"^assets/img/", "", path)
        alt = attrs.get("title", rel)
        return f"![{alt}](/assets/img/{rel})"

    body = re.sub(r"{%\s*include figure\.liquid.*?%}", fig_sub, body)

    # al-folio wraps figures in Bootstrap grid divs; markdown inside raw HTML
    # blocks is not parsed, so unwrap them. Captions become italic lines.
    body = re.sub(
        r'<div class="caption[^"]*">\s*(.*?)\s*</div>',
        lambda m: '<p class="caption">' + " ".join(m.group(1).split()) + "</p>",
        body,
        flags=re.S,
    )
    body = re.sub(r"^\s*</?div[^>]*>\s*\n", "", body, flags=re.M)

    # Deep-indented image lines would parse as code blocks; dedent them.
    body = re.sub(r"^\s{4,}(!\[[^\]]*\]\([^)]*\))\s*$", r"\1", body, flags=re.M)

    # Any remaining liquid: report and drop.
    liquid = re.findall(r"{%.*?%}", body)
    for l in liquid:
        print(f"  [liquid dropped] {l[:80]}")
    body = re.sub(r"{%.*?%}\n?", "", body)

    body = split_dangling_delimiters(body)
    body = convert_inline_math(body)
    body = promote_headings(body)

    # Images: /assets/img/foo.png -> /img/foo.png, copy the file.
    def img_sub(m):
        rel = m.group(1)
        src = JEKYLL_ROOT / "assets/img" / rel
        dst = IMG_OUT / rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            print(f"  [missing image] {rel}")
        return f"/img/{rel}"

    body = re.sub(r"/assets/img/([^\s\)\"']+)", img_sub, body)

    tags_yaml = "[" + ", ".join(tags) + "]"
    fm_new = (
        "---\n"
        f"title: \"{title}\"\n"
        f"date: {date.split()[0] if date else ''}\n"
        f"description: \"{desc}\"\n"
        f"tags: {tags_yaml}\n"
        f"category: \"{category}\"\n"
        "---\n"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slug}.md"
    out.write_text(fm_new + body.lstrip("\n"))
    print(f"wrote {out.relative_to(OUT_DIR.parent.parent.parent)}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p = Path(arg)
        print(f"converting {p.name}")
        convert(p)
