#!/usr/bin/env python3
"""Generate zettelkasten stubs in vault/posts/ from the Astro blog collection.

Design decision (progress.md 2026-07-20): STUBS, PUBLISHED. Each blog post gets
a short note in the vault carrying its title, description, tags and a link out
to the real post. The graph and backlinks work fully, and the 93 posts are not
duplicated at two URLs with two sets of giscus comments.

The stubs deliberately carry almost no links of their own. Retro-linking is the
user's editorial call, so this script also emits a CANDIDATE REPORT
(tooling/link-candidates.md) listing mechanical link suggestions with evidence,
for the user to apply in Obsidian. The only links written directly are the
handful of seed-zettel connections in SEED_LINKS, which the user approved.

Usage: python3 tooling/make_stubs.py [--report-only]
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "astro/src/content/blog"

# Stubs link OUT to the Astro site, so the URL must be ABSOLUTE. A
# root-relative /blog/<slug>/ does not work: Quartz treats root-relative hrefs
# as vault-internal paths and rewrites them, so the link came out as
# ../blog/<slug>/ = /notes/blog/<slug>/, inside the notes tree.
#
# AT PROD FLIP: set BLOG_BASE to https://monishver11.github.io and re-run this
# script. That is the only thing that needs changing here.
BLOG_BASE = os.environ.get("BLOG_BASE", "https://monishver11.github.io/site-v2")
POSTS_OUT = ROOT / "vault/posts"
ZETTELS = ROOT / "vault/zettels"
REPORT = ROOT / "tooling/link-candidates.md"

LINKS_FILE = ROOT / "tooling/post-links.json"

# Marker for hand-added links, so regenerating never destroys the user's own
# editorial work. Anything under this line in a stub is read back and re-emitted.
HAND_MARKER = "<!-- links below this line are kept when regenerating -->"

# Words too generic to be evidence of a real connection.
STOP = {
    "the", "and", "for", "with", "from", "this", "that", "notes", "intro",
    "using", "into", "part", "how", "why", "what", "a", "an", "of", "in", "on",
    "to", "is", "it", "as", "at", "by", "be", "are", "was", "we", "you",
}


def parse_frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def unquote(s):
    s = (s or "").strip()
    if s.startswith('"'):
        try:
            return json.loads(s)
        except Exception:
            return s.strip('"')
    return s


def parse_tags(raw):
    raw = (raw or "").strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [t.strip() for t in raw[1:-1].split(",") if t.strip()]
    return [t for t in raw.split() if t]


def load_posts():
    posts = {}
    for p in sorted(BLOG.glob("*.md")):
        fm, body = parse_frontmatter(p.read_text())
        slug = p.stem.lower()
        posts[slug] = {
            "slug": slug,
            "file": p,
            "title": unquote(fm.get("title", p.stem)),
            "date": (fm.get("date") or "").strip(),
            "desc": unquote(fm.get("description", "")),
            "tags": parse_tags(fm.get("tags", "")),
            "category": unquote(fm.get("category", "")),
            "body": body,
        }
    return posts


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def read_hand_links(slug):
    """Pull back any links the user added below HAND_MARKER in an existing stub."""
    path = POSTS_OUT / f"{slug}.md"
    if not path.exists():
        return []
    text = path.read_text()
    if HAND_MARKER not in text:
        return []
    tail = text.split(HAND_MARKER, 1)[1]
    return [l.rstrip() for l in tail.splitlines() if l.strip().startswith("- ")]


def write_stub(post, related, hand):
    """related: list of (target, reason) to write into the stub."""
    tags = list(dict.fromkeys(post["tags"] + ["post"]))
    lines = [
        "---",
        f"title: {yaml_str(post['title'])}",
        f"date: {post['date']}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
    ]
    if post["desc"]:
        lines += [post["desc"], ""]
    lines += [
        f"Full post: [{post['title']}]({BLOG_BASE}/blog/{post['slug']}/)"
        + (f" · {post['category']}" if post["category"] else ""),
        "",
    ]
    if related or hand:
        lines += ["## Related", ""]
        for target, reason in related:
            lines.append(f"- [[{target}]]" + (f" — {reason}" if reason else ""))
        lines += ["", HAND_MARKER, ""]
        lines += hand
        if not hand:
            lines.append("")
    POSTS_OUT.mkdir(parents=True, exist_ok=True)
    (POSTS_OUT / f"{post['slug']}.md").write_text("\n".join(lines).rstrip() + "\n")


def build_graph(posts, cfg):
    """Assemble each post's related list from threads, bridges, zettels and the
    cross-links already written in the post bodies. Returns slug -> [(target,
    reason)], and a list of validation problems."""
    rel = {s: [] for s in posts}
    problems = []

    def add(a, target, reason):
        if a not in rel:
            problems.append(f"unknown post in links config: {a}")
            return
        if target not in posts and target not in cfg.get("zettels", {}):
            problems.append(f"link target does not exist: {a} -> {target}")
            return
        if target == a:
            return
        if any(t == target for t, _ in rel[a]):
            return
        rel[a].append((target, reason))

    # Threads: prev/next only. N posts get N-1 edges, not N*(N-1)/2.
    for name, seq in cfg.get("threads", {}).items():
        for i, slug in enumerate(seq):
            if slug not in posts:
                problems.append(f"unknown post in thread {name}: {slug}")
                continue
            if i > 0:
                add(slug, seq[i - 1], f"previous in {name}")
            if i < len(seq) - 1:
                add(slug, seq[i + 1], f"next in {name}")

    # Bridges: conceptual, bidirectional.
    for entry in cfg.get("bridges", []):
        a, b = entry[0], entry[1]
        why = entry[2] if len(entry) > 2 else ""
        add(a, b, why)
        add(b, a, why)

    # Zettels, bidirectional.
    for z, slugs in cfg.get("zettels", {}).items():
        for s in slugs:
            add(s, z, "concept note")

    # Cross-links the posts already make in their own bodies: hard facts.
    for slug, post in posts.items():
        for target in sorted(set(re.findall(r"\]\(/blog/([a-z0-9\-]+)/\)", post["body"]))):
            if target in posts:
                add(slug, target, "referenced in this post")

    return rel, problems


def update_zettel_related(cfg, posts):
    """Rewrite ONLY the '## Related posts' section of each zettel, leaving the
    hand-written prose above it untouched."""
    changed = []
    for z, slugs in cfg.get("zettels", {}).items():
        path = ZETTELS / f"{z}.md"
        if not path.exists():
            continue
        text = path.read_text()
        block = ["## Related posts", ""]
        for s in slugs:
            title = posts[s]["title"] if s in posts else s
            block.append(f"- [[{s}]] — {title}")
        new_section = "\n".join(block) + "\n"
        if "## Related posts" in text:
            head = text.split("## Related posts", 1)[0].rstrip() + "\n\n"
            text = head + new_section
        else:
            text = text.rstrip() + "\n\n" + new_section
        path.write_text(text)
        changed.append(z)
    return changed


def zettel_slugs():
    return {p.stem: p for p in ZETTELS.glob("*.md")}


def candidates(posts, zettels):
    """Mechanical link suggestions with evidence. Editorial calls stay with the
    user, so nothing here is written into the vault automatically."""
    out = {}
    ztitles = {}
    for slug, path in zettels.items():
        fm, _ = parse_frontmatter(path.read_text())
        ztitles[slug] = unquote(fm.get("title", slug))

    for slug, post in posts.items():
        body_l = post["body"].lower()
        found = []

        # 1. Explicit cross-post links already in the body: a hard fact.
        for m in sorted(set(re.findall(r"\]\(/blog/([a-z0-9\-]+)/\)", post["body"]))):
            if m != slug and m in posts:
                found.append((m, "post links to it directly"))

        # 2. A zettel's title appears in the body.
        for z, zt in ztitles.items():
            terms = [w for w in re.split(r"[^a-z0-9]+", zt.lower()) if w and w not in STOP and len(w) > 3]
            if terms and all(t in body_l for t in terms):
                n = min(body_l.count(t) for t in terms)
                found.append((z, f'zettel title "{zt}" terms appear (min {n}x)'))

        # 3. Shared tags with another post, only for rare tags. A tag on 30
        #    posts says nothing; a tag on 3 says these belong together.
        for other_slug, other in posts.items():
            if other_slug == slug:
                continue
            shared = set(t.lower() for t in post["tags"]) & set(t.lower() for t in other["tags"])
            for t in shared:
                holders = sum(1 for q in posts.values() if t in [x.lower() for x in q["tags"]])
                if 2 <= holders <= 4:
                    found.append((other_slug, f'shares rare tag "{t}" ({holders} posts have it)'))

        # de-dupe, keep first reason per target
        seen = {}
        for target, why in found:
            seen.setdefault(target, why)
        if seen:
            out[slug] = seen
    return out


def main():
    report_only = "--report-only" in sys.argv
    posts = load_posts()
    zettels = zettel_slugs()
    cfg = json.loads(LINKS_FILE.read_text())

    rel, problems = build_graph(posts, cfg)
    for p in problems:
        print(f"  [PROBLEM] {p}")

    if not report_only:
        for slug, post in posts.items():
            write_stub(post, rel[slug], read_hand_links(slug))
        touched = update_zettel_related(cfg, posts)
        edges = sum(len(v) for v in rel.values())
        linked = sum(1 for v in rel.values() if v)
        print(f"wrote {len(posts)} stubs to vault/posts/")
        print(f"  {edges} links across {linked} posts; {len(posts) - linked} still isolated")
        print(f"  refreshed Related posts in zettels: {', '.join(touched)}")
        iso = [s for s, v in rel.items() if not v]
        if iso:
            print(f"  isolated: {', '.join(sorted(iso))}")

    cand = candidates(posts, zettels)
    total = sum(len(v) for v in cand.values())
    lines = [
        "# Retro-link candidates",
        "",
        "Generated by `tooling/make_stubs.py`. These are MECHANICAL suggestions,",
        "not decisions. Skim, delete what is wrong, and add the rest as `[[links]]`",
        "in Obsidian under each stub's `## Related` heading.",
        "",
        "Evidence types: a direct link already in the post body (hard fact), a",
        "zettel title whose terms appear in the post, or a rare shared tag.",
        "Generic tags are excluded: a tag on 30 posts is not evidence.",
        "",
        f"{total} suggestions across {len(cand)} posts.",
        "",
    ]
    for slug in sorted(cand):
        lines.append(f"## {slug}  ({posts[slug]['title']})")
        for target, why in sorted(cand[slug].items()):
            lines.append(f"- `[[{target}]]`  <- {why}")
        lines.append("")
    REPORT.write_text("\n".join(lines))
    print(f"wrote {REPORT.relative_to(ROOT)} ({total} suggestions across {len(cand)} posts)")


if __name__ == "__main__":
    main()
