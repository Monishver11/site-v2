# Site v2 handoff

Read this first, then progress.md (decision log) and design.md (architecture). Follow the working rules in /Users/monishver/Downloads/me.md for the whole session: discuss first and get confirmation before implementing, minimal responses, numbered clarifying questions, no em-dashes in writeups, record decisions in these files as you go.

## What this project is

A ground-up rebuild of Monishver's personal site (currently monishver11.github.io, al-folio Jekyll) as:
- Astro 5 main site in `astro/` (about, blog, book, thoughts, reads, reviews)
- Quartz v4 zettelkasten in `quartz/` publishing `vault/` to /notes
- One GitHub Actions workflow deploying both to GitHub Pages

STAGING IS LIVE: https://monishver11.github.io/site-v2/ (repo github.com/Monishver11/site-v2, public). The old site is untouched and stays primary until the full port is done.

## Key locations

- Old site (content source): /Users/monishver/monishver11.github.io
- This project: /Users/monishver/Downloads/site-v2
- Design tokens (all colors/fonts): astro/src/styles/tokens.css
- Post pipeline + typography: astro/src/styles/post.css, astro/src/plugins/remark-sidenote.mjs
- Porting tools + recipe: tooling/convert_post.py, tooling/CONVERSION.md, tooling/convert_thoughts.py
- Deploy: .github/workflows/deploy.yml, tooling/fix-base.mjs (staging base-path rewrite)
- Dev servers (launch.json in experiments/.claude): "site-v2" (astro, port 4322), "site-v2-notes" (quartz, port 8081)

## Design decisions (locked, do not relitigate)

- Light mode only on the Astro site. Background #FCFCF9, clay accent #B5533C, serif everywhere (Charter/Georgia stack), classical feel, no decorative animations, content width 50rem.
- Headings: weight 500 + 0.3px -webkit-text-stroke (the stack has no medium weight). No borders under headings.
- Blog: Written | Excalidraw tabs; category row (ML Theory, GPU & Performance, Big Data Systems, Projects); category pages newest-first; sidenotes via :sidenote[...] directive.
- Thoughts: Mine | Others tabs (person-credited incl. Anonymous = others; uncredited or date-only = mine), grouped by year, data in astro/src/data/thoughts.json (280 quotes parsed from old site).
- Buttondown username: monishver (live). Giscus: same repo/category/title mapping as old site so old discussions carry over.
- Daily logs are private: vault/daily is gitignored AND quartz-ignored. Public artifact is a weekly review (automation drafts, user edits, then publishes).
- The ~52 ML Theory posts become an ordered "book" section built in Astro (no GitBook/mdBook).

## Current state (2026-07-20)

Done and verified live: about page, blog pipeline with 3 ported posts (kernel-trick, sgd, fa3-cute), math (KaTeX, 0 errors), sidenotes, giscus + Buttondown on posts, thoughts (real data, both tabs), reads/reviews/book placeholder pages, Quartz notes with 4 seed notes (graph/search/backlinks/wikilinks working), staging deploy green.

## Next steps, in order (user-approved sequence)

1. Obsidian setup: user points Obsidian at vault/ (their step). Then scaffold: daily-note template in vault/templates, sensible .obsidian defaults. Then the 12am housekeeping job (archive today's daily note, reset the running note) as a local launchd job. Write the script and SHOW THE USER before installing anything scheduled.
2. Port the remaining ~91 posts with tooling/convert_post.py (batch, then spot-check per CONVERSION.md; posts with video/audio/jupyter liquid need hand attention). Copy needed images automatically happens.
3. Build the Book section: ordered manifest of the ML Theory posts (parts/chapters, sidebar tree, prev/next). User wants involvement in the ordering.
4. Reads content: user will supply their list (reads.json holds it: title/href/by/note fields).
5. Weekly review automation: draft from daily logs for user to edit, publish to /reviews.
6. Prod flip when port is complete: set BASE_PATH and NOTES_BASE_URL to root values, remove fix-base step, move Pages to the main repo. Old permalink format was /blog/:year/:title/ so add redirects or match slugs when flipping (current new format is /blog/<slug>/, NOT year-based; decide redirect strategy with user).

## Gotchas

- Quartz v5 (master) breaks on this machine's node 23.4 (plugin loader chokes on .scss). We vendor Quartz v4 branch, .git removed. Upgrade only by re-clone + re-apply config (quartz.config.ts, quartz.layout.ts footer, package.json "notes" script).
- The in-app browser pane renders blank screenshots on long pages when the viewport is resized to 1440x900; use the native size.
- Re-running convert_post.py on a post overwrites hand edits (e.g. the demo sidenote in kernel-trick).
- astro build output must not be committed (gitignored); CI builds fresh.
- The kernel-trick post has one demo sidenote in its intro; user may want it removed eventually.
