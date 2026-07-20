# Site v2 progress

## 2026-07-19: Context gathering (no code yet)

### Current site audit (monishver11.github.io, al-folio Jekyll)
- 94 posts in `_posts/`, math as `$$ ... $$` (MathJax), frontmatter: layout/title/date/description/tags/categories/giscus_comments/toc sidebar.
- Categories: ML-NYU (52), GPU-NYU (15), RBDA-NYU (11), ADV-ML-NYU (8), LLMR-NYU (2), RL-NYU (1), DS-NYU (1), 3 uncategorized.
- Pages: about (climate redesign planned), thoughts (quote divs, mine + others mixed, month headers), projects (5), cv, news; lifelog.md and worklog.md exist but frontmatter commented out (private drafts).
- Google Analytics wired (G-1HD0LJE1KY), giscus comments wired, search enabled.
- No excalidraw files anywhere in repo. No books/reads page yet.

### New site wishlist (from user brief)
- About: climate/weather-inspired (apple weather style, or floating leaf).
- Blogs: two tabs (written / excalidraw images).
- Thoughts: two tabs (mine / others).
- Notes: zettelkasten, Obsidian-connected, searchable, auto links + graph, daily log that publishes at 12am then resets.
- Books/Reads: two tabs (technical / non-technical).
- Mailing list per post (Aleksa Gordic style), sidenotes (siboehm style), off-white background but whiter than siboehm.
- GitHub Pages hosting, GitHub Actions, Google Analytics, modular build, reliable/durable.

### Research findings (zettelkasten/second brain publishing)
- Quartz v4: free, static, publishes an Obsidian vault to GitHub Pages; wikilinks, backlinks, local graph view, full-text search, LaTeX plugin (KaTeX or MathJax). De facto best free Obsidian Publish alternative.
- Obsidian Publish: $8/mo, less customizable, no self-host.
- Retro-linking existing notes (Obsidian plugins): Note Linker (scan and confirm links), Auto Linker (confidence-ranked inline suggestions, local), Semantic Auto-Linker (embedding-based, previews graph impact).
- Jekyll-to-vault conversion: no perfect off-the-shelf tool for our direction (existing tools go Obsidian to Jekyll); a small custom script over the 94 posts (strip liquid, keep $$ math, add aliases) is the realistic path.
- Daily-note automation: GitHub Action on cron at 12am ET; vault synced to a git repo; action publishes the day's note to the site and truncates/archives the running note.

### Decisions (2026-07-19)
1. Stack: Astro (fresh build) + Quartz sub-build at /notes, GitHub Pages.
2. Obsidian: installed, vault starts fresh.
3. Blog posts ARE part of the zettelkasten corpus (converted into the vault, wikilinked), not a separate layer.
4. Daily logs stay private. 12am job = vault housekeeping only (archive today's note, reset running note; nothing published). Public artifact is a review: automation drafts it from the logs, user edits before publishing. Cadence TBD (weekly proposed).
5. Excalidraw tab: forward-looking, no existing files.
6. Mailing list: Buttondown.
7. Reorganize categories by topic (drop course names). The ~52 ML posts become a "book" (GitBook-style ordered chapters).
8. Thoughts: two tabs (mine / others). Credited to a person = others; date-only or uncredited = mine. Within each tab, group by year (drop month-level headers).
9. Books/Reads: build structure now, content list comes later.
10. About page: simple floating-leaf touch, not full weather system.

### Decisions (round 3)
11. Reviews: weekly cadence.
12. Blog taxonomy confirmed: ML Theory / GPU & Performance / Big Data Systems / Projects.
13. Typography: serif body, siboehm direction.
14. Palette: background #FCFCF9 (soft ivory), accent clay #B5533C. Dark mode kept: warm near-black bg, lightened clay accent.
15. Dark mode: keep (cheap if built with CSS variable tokens from day one; Quartz ships it built in).

## 2026-07-19: Implementation round 1 (done)
- Astro 5 initialized in `astro/`. Files: `src/styles/tokens.css` (all colors as CSS vars, light + dark), `src/layouts/Base.astro` (nav, footer, theme toggle with localStorage), `src/components/Leaf.astro` (clay leaf, gentle float over shadow, prefers-reduced-motion respected), `src/pages/index.astro` (about page).
- Verified in browser, both modes, no console errors. Dev server: `npm run dev` in astro/ (port 4322 in launch.json).
- Polish backlog: nav links other than About are dead until those pages exist.

## 2026-07-19: Feedback round (done)
- Classical restyle: serif for all chrome (nav, footer), nav active/hover = underline instead of color-only, italic tagline, centered hero with small flourish rule, italic centered footer. Sun/moon toggle icon now swaps with theme.
- Leaf redesigned per feedback: no longer fixed in the hero. It rests at the bottom-right of the viewport and every 75s takes a slow drifting flight up over the page (vw/vh keyframe path + constant gentle sway), then settles back. pointer-events none, aria-hidden, disabled under prefers-reduced-motion.
- Verified in browser: rest position clear of footer text, flight path confirmed (debug-accelerated), no console errors.

## 2026-07-19: Feedback round 2 (done)
- Light mode only: dark tokens, toggle, and theme script removed.
- Leaf removed entirely (component deleted). User decided against it.
- Footer: contact line "The best way to reach me is via email, followed by LinkedIn." + envelope icon (mailto:monishverchandrasekaran@gmail.com) + LinkedIn icon (linkedin.com/in/monishver); below it copyright + "Last updated <build date/time> ET" (render-time timestamp = deploy time on static build).
- About page: full content ported from current site (About Me / Beyond the technical stuff / sign-off), profile photo floated right (public/img/prof_pic_cmp.jpg).

## 2026-07-19: Feedback round 3 (done)
- "Best blogs to read" section removed from about page (user decision).
- Contact block moved out of the footer into the about page: after the "Best, Monishver" sign-off and before the footer's breaker line. Order: icons row (email, LinkedIn) first, sentence "The best way to reach me is via email, followed by LinkedIn." below it.
- Footer now holds only the copyright + last-updated line.

## 2026-07-19: Feedback round 4 (done)
- Margin decoration ideas (seasonal drift / engraved vines / scroll progress rule) prototyped, shown, and REJECTED - user prefers clean margins. MarginDemo component deleted.
- Instead: content column widened from 42rem to 50rem (--content-width in tokens.css) so side space is small. Verified at 1440px.

## 2026-07-19: Blog section, milestone 1 (done)
- Content collection `src/content/blog/` (schema: title, date, description, tags, category enum, draft). Post pages at /blog/<slug>/ (Astro lowercases ids).
- Math: remark-math + rehype-katex + KaTeX CSS. Jekyll inline `$$..$$` converted to `$..$` at port time; display blocks kept. Code: Shiki vitesse-light.
- Sidenotes: `:sidenote[...]` inline directive (remark-directive + custom plugin src/plugins/remark-sidenote.mjs). Numbered, right-gutter float >=1360px, checkbox tap-to-expand below. Demo note added to kernel-trick intro (remove/keep at will).
- Blog index: Written | Excalidraw tabs, posts grouped by year, date + title + category. Drawings tab is an empty state for now.
- Converter `tooling/convert_post.py`: frontmatter mapping (course categories -> new taxonomy), figure.liquid -> markdown images, Bootstrap row/col unwrap, caption divs -> italics, dangling $$ delimiter fix, image copy to public/img. Ported: kernel-trick, SGD, fa3-cute. All render clean (0 KaTeX errors, images load). Production build passes (6 pages).
- Dates are UTC-formatted everywhere to avoid off-by-one.
- Not yet: giscus, Buttondown embed, TOC, prev/next, remaining 91 posts.

## 2026-07-19: Blog feedback round (done)
- Category nav row on blog index right after the subtitle (ML Theory / GPU & Performance / Big Data Systems / Projects), each linking to /blog/category/<slug>/ pages that list that category's posts OLDEST-FIRST (numbered, "in reading order" - series semantics). Active category highlighted in clay.
- Heading hierarchy fixed at the converter: posts' shallowest heading level promoted to h2 (al-folio corpus uses ####/#####/###### which rendered tiny). CSS scale: h2 1.45rem + bottom border, h3 1.2rem, h4 1.1rem italic, h5/h6 0.95rem italic secondary.
- Captions emitted as <p class="caption">, centered italic muted under images.
- Note: enlarging the Browser pane viewport to 1440x900 causes blank screenshots on long pages (pane artifact, NOT a site bug - fine at native size).
- Build passes, 10 pages.

## 2026-07-19: Headings final touch (done)
- 0.3px -webkit-text-stroke on prose headings: the "in-between" weight Charter/Georgia don't ship (500 maps to regular, 600 to full bold). Bump to 0.4-0.5px if ever wanted.

## 2026-07-19: Comments + mailing list (done)
- Giscus on every post (same repo/category/title-mapping as old site, so existing discussions carry over). Component: astro/src/components/Giscus.astro.
- Buttondown subscribe box after post content (astro/src/components/Subscribe.astro). TODO: create the Buttondown account; username placeholder "monishver" must be updated to the real one.
- Conversion recipe documented in tooling/CONVERSION.md.

## 2026-07-19: Quartz notes (done, local)
- Quartz v4 (branch v4) cloned to quartz/; v5 (master) is broken on node 23.4 (plugin loader chokes on .scss import).
- quartz.config.ts customized: title "Monishver's Notes", GA tag, baseUrl monishver11.github.io/notes, ignorePatterns includes "daily" (private) + "private", palette matched to site tokens (light + dark), fonts Source Serif 4 / IBM Plex Mono. Footer links -> Home/Blog (quartz.layout.ts).
- Vault seeded: index.md + 3 wikilinked zettels (gpu-memory-hierarchy, cute-layouts, online-softmax). Graph, backlinks, search, tags, KaTeX all verified in browser.
- Serve locally: launch config "site-v2-notes" (npm run notes in quartz/, port 8081). Build: npx quartz build -d ../vault.
- Not yet: deploy workflow merging astro dist + quartz public into one GitHub Pages artifact (/notes prefix); Obsidian pointed at vault/; importing blog corpus into the vault; 12am housekeeping action; weekly review automation.

## 2026-07-19: Remaining tabs (done)
- Buttondown account created by user; username "monishver" confirmed (form was already pointing there).
- Thoughts: tooling/convert_thoughts.py parses the old thoughts page into astro/src/data/thoughts.json (280 quotes: 179 mine / 101 others; person-credited incl. Anonymous -> others, date-only/uncredited -> mine; year from month headers, undated top block = 2026, legacy tail = 2025). Two tabs (/thoughts/ mine, /thoughts/others/), grouped by year, quote + em-dash attribution styling.
- Reads: /reads/ (technical) + /reads/non-technical/ tabs reading from astro/src/data/reads.json (empty shelves with a stocked-soon note; user will supply the list; items support title/href/by/note).
- Reviews: /reviews/ intro + empty state (weekly cadence).
- Book: /book/ placeholder until the ML posts port.
- Build passes, 16 pages. Every nav link now resolves.

## 2026-07-19: Blog feedback round 2 (done)
- Category pages flipped to newest-first; numbering + "in reading order" removed (ordering belongs to the Book).
- Headings lightened: weight 500 across h2-h6, strong inside headings inherits (no double-bold), h2 bottom border removed.
