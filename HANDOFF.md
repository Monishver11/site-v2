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

## Daily notes (step 1, DONE 2026-07-20)

The writing loop: one running file `vault/daily/today.md`, archived to `vault/daily/<date>.md` by `tooling/daily-rollover.sh`, which also reseeds today.md from `vault/templates/daily.md` and regenerates its Goals section from `vault/goals.md`.

**THE ROLLOVER IS MANUAL. There is no scheduled job, and this is deliberate.** A launchd agent cannot read file contents under `~/Downloads` (macOS TCC), so a scheduled run fails with "Operation not permitted"; an interactive terminal can, so running it by hand works. This was tested, not assumed: the job was installed, it failed, it was removed, and `~/Library/LaunchAgents` is clean. Do not re-attempt scheduling while the project lives in `~/Downloads`. `tooling/com.monishver.daily-rollover.plist` is kept unused for the day the project moves.

The script is idempotent with catch-up, so running it repeatedly is a no-op and forgetting for a week still archives correctly. Full operational detail in `vault/daily/README.md`; full decision trail in progress.md under 2026-07-20.

## Next steps, in order (user-approved sequence)

1. ~~Obsidian setup~~ DONE, see above. Remaining nits: user should replace the placeholder goal in `vault/goals.md` with real goals.
2. ~~Port the remaining posts~~ DONE 2026-07-20. All 93 posts are in `astro/src/content/blog/`. Build is 107 pages with 0 KaTeX errors, 0 dead links, 0 missing images, 0 leftover liquid. The converter gained 8 fixes in the process (post_url resolution, YAML-safe frontmatter, old-permalink rewriting, display-delimiter normalization, multi-line figure.liquid, \text underscore escaping, empty-link -> /404). See progress.md 2026-07-20 for the full list and the traps.
   NOTE: the old warning here about "video/audio/jupyter liquid needing hand attention" was WRONG. There is none of that in the corpus. Removed.
3. ~~Zettel~~ DONE 2026-07-20. 93 stubs in `vault/posts/` with **216 curated links across 92 of them** (only nyu-grad isolated, correctly). Graph, backlinks, search verified.
   The link graph lives in `tooling/post-links.json` (threads = ordered reading sequences giving prev/next; bridges = conceptual pairs with reasons; zettels). Edit that file and re-run `python3 tooling/make_stubs.py`.
   **Regenerating is safe**: anything below the `<!-- links below this line are kept when regenerating -->` marker in a stub is preserved, so add your own links there freely.
4. Build the Book section: ordered manifest of the ML Theory posts (parts/chapters, sidebar tree, prev/next). User wants involvement in the ordering.
5. Reads content: user will supply their list (reads.json holds it: title/href/by/note fields).
6. Weekly review automation: draft from daily logs for user to edit, publish to /reviews.
7. Prod flip when port is complete: set BASE_PATH and NOTES_BASE_URL to root values, remove fix-base step, move Pages to the main repo. Old permalink format was /blog/:year/:title/ so add redirects or match slugs when flipping (current new format is /blog/<slug>/, NOT year-based; decide redirect strategy with user).

## Gotchas

- Quartz v5 (master) breaks on this machine's node 23.4 (plugin loader chokes on .scss). We vendor Quartz v4 branch, .git removed. Upgrade only by re-clone + re-apply config (quartz.config.ts, quartz.layout.ts footer, package.json "notes" script).
- The in-app browser pane renders blank screenshots on long pages when the viewport is resized to 1440x900; use the native size.
- Re-running convert_post.py on a post overwrites hand edits (e.g. the demo sidenote in kernel-trick). This is why math/link corrections live in the converter as general rules rather than as edits to the generated markdown. The batch excludes sgd, fa3-cute, and kernel-trick for this reason.
- Converter URL rewriting must never match on domain alone: the corpus cites external blogs (gregorygundersen.com) whose URLs have the same `/blog/YYYY/slug/` shape as the old permalinks. Anchor such rules to link-target position instead.
- Quartz `ignorePatterns` are globs against the path, so a bare name only matches a DIRECTORY. To exclude a single file you must write the extension (`"goals.md"`, not `"goals"`). A bare name fails SILENTLY and the file publishes; check the built output, do not assume.
- Vault notes must link OUT to the Astro site with ABSOLUTE urls. Quartz rewrites root-relative hrefs as vault-internal paths (`/blog/x/` becomes `/notes/blog/x/`). Do not try to fix this in fix-base.mjs; that was tried and reverted.
- Images: 141 of the old site's 188 are copied, which is correct. The other 47 belong to the old Projects page and al-folio scaffolding and are deliberately left behind (progress.md 2026-07-20).
- astro build output must not be committed (gitignored); CI builds fresh.
- The kernel-trick post has one demo sidenote in its intro; user may want it removed eventually.
