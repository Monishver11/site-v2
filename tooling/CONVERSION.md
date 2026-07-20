# Porting a Jekyll (al-folio) post to site-v2

One command per post (repeatable, idempotent):

```
cd /Users/monishver/Downloads/site-v2
python3 tooling/convert_post.py /Users/monishver/monishver11.github.io/_posts/<file>.md
```

Output lands in `astro/src/content/blog/<slug>.md` (slug = filename minus date
prefix; Astro lowercases it for the URL). Referenced images are copied to
`astro/public/img/` automatically.

## What the script does

1. Frontmatter: keeps title/date/description/tags; maps course categories to
   the new taxonomy (ML-NYU, ADV-ML-NYU, RL-NYU, DS-NYU -> ML Theory; GPU-NYU,
   LLMR-NYU -> GPU & Performance; RBDA-NYU -> Big Data Systems; anything else
   -> Projects). Drops Jekyll-only keys (layout, giscus_comments, toc, ...).
2. Math: Kramdown treats `$$...$$` inside a sentence as inline; remark-math
   treats every `$$` as display. Inline occurrences become `$...$`; `$$`
   blocks on their own lines stay. A closing `$$` with trailing prose on the
   same line is split onto its own line (remark-math chokes otherwise).
3. Headings: the post's shallowest heading level is promoted to h2, keeping
   relative hierarchy (the corpus uses ####/#####/###### which render tiny).
   Code fences are skipped during the shift.
4. Figures: `{% include figure.liquid %}` becomes a markdown image;
   `<div class="caption">` becomes `<p class="caption">` (styled centered
   italic); Bootstrap row/col wrapper divs are unwrapped (markdown inside raw
   HTML blocks is otherwise not parsed); deep-indented image lines are
   dedented (4+ spaces = code block in markdown).
5. `{% post_url X %}` resolves to `/blog/<slug>/`, by SLUG not filename (so a
   wrong date in the reference still resolves). Old `/blog/:year/:title/`
   permalinks, including the absolute and localhost forms, are rewritten too.
6. Display-math delimiters are normalised: every unpaired `$$` is put on its
   own line. remark-math opens/closes a flow block ONLY on a line that is
   exactly `$$`, and the corpus constantly shares that line (`...text:  $$`,
   `$$\hat{y} =`, `- $$`, `t$$`). Left alone, the pairing slips and following
   PROSE gets parsed as math.
7. Bare `_` inside `\text{}` is escaped (KaTeX rejects it, MathJax allowed it).
8. `[label]()` becomes `[label](/404)`.
9. Remaining liquid tags AND `{{ }}` expressions are dropped and printed to the
   console - check that output and handle anything unusual by hand.

## Manual checks after converting

Mechanical checks, all of which should be zero. Run against `dist/` after a build:

- `.katex-error` count.
- Leftover liquid: `grep -rl '{%' src/content/blog/`. IMPORTANT - this is the
  only check that catches a dropped `figure.liquid`. A missing-image check
  looks for "referenced but absent" and is blind to "dropped entirely".
- Dead internal `/blog/` links, and `/img/` references with no file on disk.
- Frontmatter that fails to parse (use the js-yaml in astro/node_modules).
- Swallowed prose: scan each rendered node's `<annotation encoding="application/x-tex">`
  for markdown emphasis or paragraph breaks inside math. Catches math that
  silently ate prose while still parsing, which raises no error.

Then eyeball a few posts in the browser for images and captions.

- Multi-column figure rows (3-up images) stack vertically after conversion;
  acceptable, revisit per post if a grid matters.
- Sidenotes are new-site-only: add `:sidenote[text]` inline where wanted.
  Re-running the converter overwrites the file, so re-add any sidenotes (or
  convert once, then edit). Prefer fixing recurring problems as general rules
  in the converter over editing generated markdown, which gets overwritten.

## Styling contract the converter relies on

- `astro/src/styles/post.css`: `.prose` typography; headings weight 500 with
  0.3px text-stroke (Charter/Georgia have no medium weight); `.caption`
  centered italic; sidenote CSS (margin notes >=1360px, tap-to-expand below).
- Math: remark-math + rehype-katex, KaTeX CSS imported in the post layout.
- Code: Shiki `vitesse-light`.
