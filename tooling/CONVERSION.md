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
5. Remaining liquid tags are dropped and printed to the console - check that
   output and handle anything unusual by hand.

## Manual checks after converting

- Load the post, run in devtools: `document.querySelectorAll('.katex-error').length`
  (want 0) and eyeball images/captions.
- Multi-column figure rows (3-up images) stack vertically after conversion;
  acceptable, revisit per post if a grid matters.
- Posts with unusual liquid (video, audio, jupyter embeds) need hand-porting
  of those bits.
- Sidenotes are new-site-only: add `:sidenote[text]` inline where wanted.
  Re-running the converter overwrites the file, so re-add any sidenotes (or
  convert once, then edit).

## Styling contract the converter relies on

- `astro/src/styles/post.css`: `.prose` typography; headings weight 500 with
  0.3px text-stroke (Charter/Georgia have no medium weight); `.caption`
  centered italic; sidenote CSS (margin notes >=1360px, tap-to-expand below).
- Math: remark-math + rehype-katex, KaTeX CSS imported in the post layout.
- Code: Shiki `vitesse-light`.
