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

import json
import re
import shutil
import sys
from pathlib import Path

JEKYLL_ROOT = Path("/Users/monishver/monishver11.github.io")
OUT_DIR = Path(__file__).resolve().parent.parent / "astro/src/content/blog"
IMG_OUT = Path(__file__).resolve().parent.parent / "astro/public/img"

CATEGORY_MAP = {
    # ML-NYU is the foundations course, the 52 posts that make up the Book.
    "ML-NYU": "ML Theory",
    # Everything below is NOT foundations material and goes to Misc, so it does
    # not land in the Book. ADV-ML-NYU is the Advanced ML course (8 online-
    # learning posts, a distinct course from foundations). RL-NYU and DS-NYU
    # hold one post each (rl-intro, ds1); ds1 is distributed systems, not ML.
    "ADV-ML-NYU": "Misc",
    "RL-NYU": "Misc",
    "DS-NYU": "Misc",
    "GPU-NYU": "GPU & Performance",
    "LLMR-NYU": "GPU & Performance",
    "RBDA-NYU": "Big Data Systems",
}


def yaml_str(s):
    """Emit a YAML-safe scalar. Several post titles contain double quotes (they
    quote a paper's name), which naive f-string quoting turned into invalid
    YAML. A JSON string is always valid YAML, and json handles the escaping."""
    return json.dumps(s, ensure_ascii=False)


def known_slugs():
    """Slugs of every post in the Jekyll corpus, date prefix stripped and
    lowercased, matching how Astro derives post ids."""
    return {
        re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.stem).lower()
        for p in (JEKYLL_ROOT / "_posts").glob("*.md")
    }


KNOWN_SLUGS = known_slugs()


def resolve_post_urls(body):
    """{% post_url 2025-09-23-GPU-Intro %} -> /blog/gpu-intro/

    These were previously swallowed by the generic liquid drop, which turned
    cross-post links into empty hrefs silently. Resolve them instead, and shout
    if the target does not exist.

    Resolution is by slug, not filename, so a wrong DATE in the reference still
    resolves (the corpus has one such typo). A wrong NAME cannot be guessed and
    is reported as an error.
    """

    def sub(m):
        name = m.group(1).strip()
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name).lower()
        if slug not in KNOWN_SLUGS:
            print(f"  [ERROR unresolved post_url] {name} -> /blog/{slug}/ (no such post)")
        elif not (JEKYLL_ROOT / "_posts" / f"{name}.md").exists():
            print(f"  [post_url date corrected] {name} -> /blog/{slug}/")
        return f"/blog/{slug}/"

    # The corpus always writes these as {{ site.baseurl }}{% post_url X %}.
    # Handle the bare form too, so a future post without the prefix still works.
    body = re.sub(
        r"{{\s*site\.baseurl\s*}}\s*{%\s*post_url\s+([^\s%]+)\s*%}", sub, body
    )
    body = re.sub(r"{%\s*post_url\s+([^\s%]+)\s*%}", sub, body)
    return body


def rewrite_old_permalinks(body):
    """Old Jekyll permalinks were /blog/:year/:title/; the new site uses
    /blog/:slug/. Posts cross-link each other in both the root-relative form
    and the absolute monishver11.github.io form, so rewrite both.

    CAREFUL: this must not touch other domains. The corpus cites
    gregorygundersen.com/blog/2020/02/09/log-sum-exp/, which matches the same
    shape. An earlier version of this used a negative lookbehind for the
    domain and silently mangled that citation into /blog/02/09/. So the
    root-relative rule now fires ONLY at the start of a link target -- right
    after "](" or 'href="' -- which a full URL can never satisfy.
    """

    def sub(m):
        slug = m.group(1).lower()
        if slug not in KNOWN_SLUGS:
            print(f"  [WARN old permalink to unknown post] -> /blog/{slug}/")
        return f"/blog/{slug}/"

    # Own domain, absolute. Safe to anchor on the domain itself.
    body = re.sub(
        r"https://monishver11\.github\.io/blog/\d{4}/([^/\s)\"']+)/?", sub, body
    )
    # Two posts link to http://localhost:8080/blog/... - dev-server URLs that
    # were committed by accident and are dead on the live site today. The
    # intent is plainly an internal link, so treat them as own-domain.
    body = re.sub(
        r"https?://localhost(?::\d+)?/blog/\d{4}/([^/\s)\"']+)/?", sub, body
    )
    # Root-relative, only as a link target.
    body = re.sub(
        r"(?<=\]\()/blog/\d{4}/([^/\s)\"']+)/?", sub, body
    )
    body = re.sub(
        r"(?<=href=\")/blog/\d{4}/([^/\s)\"']+)/?", sub, body
    )
    return body


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


def escape_text_underscores(body):
    """Escape bare underscores inside \\text{...}.

    KaTeX rejects `\\text{training_loss}` ("Expected 'EOF', got '_'"); MathJax
    accepted it. The corpus is almost consistent already: 18 of 19 such spans
    write `\\_` correctly, so this only rescues the stragglers.
    """

    def sub(m):
        inner = re.sub(r"(?<!\\)_", r"\\_", m.group(1))
        return "\\text{" + inner + "}"

    return re.sub(r"\\text\{([^{}]*)\}", sub, body)


def rewrite_empty_links(body):
    """`[label]()` -> `[label](/404)`.

    fa3-k4 links to a K5 post that was never written, with an empty href in the
    original. An empty href silently reloads the current page, which is worse
    than an honest not-found page, so point it at /404 (which offers a way back
    to the About page).
    """
    n = len(re.findall(r"\]\(\s*\)", body))
    if n:
        print(f"  [empty link -> /404] {n} occurrence(s)")
    return re.sub(r"\]\(\s*\)", "](/404)", body)


def normalize_display_delimiters(body):
    """Put every unpaired `$$` on a line of its own.

    remark-math opens/closes a flow math block ONLY on a line that is exactly
    `$$`. The corpus routinely shares that line with other content, in both
    directions:

        Assume the data comes from a normal distribution:  $$   <- opens
           $$\\hat{y}_t =                                       <- opens
        - $$                                                    <- opens
        t$$                                                     <- closes

    Kramdown/MathJax tolerated all of these. remark-math instead reads them as
    INLINE math, so the delimiter pairing slips and the block runs on, parsing
    following prose as math. That surfaces downstream as "Can't use function
    '$' in math mode" on a paragraph that contains no display math at all.

    A `$$...$$` pair that is fully contained on one line is left alone: that is
    genuine inline math, and convert_inline_math rewrites it to `$...$`. Only
    an UNPAIRED delimiter is split out. Leading whitespace is preserved so that
    math nested inside a list item stays in its list item.
    """
    out = []
    in_block = False
    in_fence = False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or "$$" not in line:
            out.append(line)
            continue

        if line.strip() == "$$":
            in_block = not in_block
            out.append(line)
            continue

        indent = line[: len(line) - len(line.lstrip())]
        count = line.count("$$")

        if count % 2 == 0:
            # Fully paired on this line; inline math, leave it.
            out.append(line)
            continue

        if in_block:
            # The FIRST delimiter closes the open block.
            head, _, tail = line.partition("$$")
            if head.strip():
                out.append(head.rstrip())
            out.append(indent + "$$")
            if tail.strip():
                out.append(indent + tail.strip())
            in_block = False
        else:
            # The LAST delimiter opens a block; anything before it is content.
            head, _, tail = line.rpartition("$$")
            if head.strip():
                out.append(head.rstrip())
            out.append(indent + "$$")
            if tail.strip():
                out.append(indent + tail.strip())
            in_block = True
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

    # re.S matters: some includes wrap onto a second line, e.g.
    #   {% include figure.liquid path="assets/img/kafka-1.png" title="kafka-1"
    #      class="img-fluid rounded z-depth-1" %}
    # Without DOTALL those never matched, so 3 images in big-data-10-kafka were
    # dropped and the raw liquid was left visible in the rendered post.
    body = re.sub(r"{%\s*include figure\.liquid.*?%}", fig_sub, body, flags=re.S)

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

    # Cross-post links, before the generic drop below would eat them.
    body = resolve_post_urls(body)
    body = rewrite_old_permalinks(body)

    # Any remaining liquid: report and drop. {{ }} expressions are reported too;
    # dropping one silently would leave a plausible-looking but wrong sentence.
    liquid = re.findall(r"{%.*?%}", body, flags=re.S) + re.findall(r"{{.*?}}", body)
    for l in liquid:
        print(f"  [liquid dropped] {' '.join(l[:80].split())}")
    body = re.sub(r"{%.*?%}\n?", "", body, flags=re.S)
    body = re.sub(r"{{.*?}}", "", body)

    body = rewrite_empty_links(body)
    body = split_dangling_delimiters(body)
    body = normalize_display_delimiters(body)
    body = convert_inline_math(body)
    body = escape_text_underscores(body)
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
        f"title: {yaml_str(title)}\n"
        f"date: {date.split()[0] if date else ''}\n"
        f"description: {yaml_str(desc)}\n"
        f"tags: {tags_yaml}\n"
        f"category: {yaml_str(category)}\n"
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
