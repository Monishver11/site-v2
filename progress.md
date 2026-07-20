# Site v2 progress

> 2026-07-20: Session handoff. Current state + next steps live in HANDOFF.md (read that first in a new session). This file remains the decision log, newest entries near the top of their date section.

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

## 2026-07-20: Zettel, step 3 (93 stubs published, retro-link report ready)

DECISION: **stubs, published** (option 1 of 3). This resolves a real conflict between the docs: progress.md decision 3 (07-19) said blog posts ARE the zettelkasten corpus "converted into the vault", while design.md's content flow said each post keeps a "stub in the graph linking to it". `vault/posts/` is NOT quartz-ignored, so full copies would have put all 93 posts at both `/blog/<slug>/` and `/notes/posts/<slug>/`: duplicate content, split giscus discussions, and search engines picking a canonical for us. Stubs give the full graph and backlinks with none of that.

- New `tooling/make_stubs.py` generates `vault/posts/<slug>.md` from the Astro collection's frontmatter: title, date, tags (+ a `post` tag), the description as the summary, and a link out to the real post.
### Linking: superseded the report approach, graph now fully built
First pass left 88 of 93 stubs isolated with a 43-item candidate report for the user to apply. User then asked for the links to be made properly from the whole corpus. Done, and the report approach was the wrong shape for this job: term-frequency matching cannot see that big-data-1..11 is a numbered series or that AdaBoost is an instance of forward stagewise additive modelling. Structure beats term overlap here.

`tooling/post-links.json` holds the curated graph, built by reading the corpus inventory (title, date, category per post) rather than by matching words:
- **threads** (21 ordered reading sequences): each member gets prev/next only. Deliberate: a fully-connected 11-post cluster is 55 edges and a useless hairball, while prev/next is 10 edges and actually navigable.
- **bridges** (39 conceptual pairs, bidirectional): the edges worth having, e.g. `adaboost <-> fsam` ("AdaBoost is forward stagewise additive modelling"), `regularization <-> max-margin-classifier` ("max margin is L2 regularisation in disguise"), `transformer-block-accounting <-> fa3-worklog`. Each carries its reason, which is rendered in the stub.
- **zettels**: expanded from the original 5 pairs to 9, bidirectional.
- Cross-links already present in post bodies are merged in automatically as hard facts.

Result: **216 links across 92 of 93 posts.** Only `nyu-grad` is isolated, correctly, it is a personal milestone post.

`make_stubs.py` also now:
- Rewrites only the `## Related posts` section of each zettel, leaving hand-written prose above untouched.
- Validates every link target and reports unknown slugs rather than emitting dead wikilinks.
- Preserves user edits: anything below the `<!-- links below this line are kept when regenerating -->` marker in a stub is read back and re-emitted, so regenerating never destroys editorial work. Verified by round-trip test.

`tooling/link-candidates.md` is kept but is now largely redundant; it stays as a way to spot connections the curated graph missed.
- While wiring, fixed a dead link in the cute-layouts zettel: it pointed at `https://monishver11.github.io/blog/fa3-cute/`, which does not exist on the old site (old permalinks are year-based). Now a `[[fa3-cute]]` wikilink.

### Two publishing bugs caught by building rather than assuming
1. **`vault/goals.md` was publishing to /notes.** It sits at the vault root so Obsidian and the rollover can read it, and it was not in `ignorePatterns`. Personal planning, should not be public. Adding `"goals"` was NOT enough: these patterns are globs against the path, so a bare `goals` only matches a DIRECTORY. It still published. The working pattern is `"goals.md"`. Verified by checking for `public/goals.html` after the build.
2. **Root-relative outbound links do not survive Quartz.** Stubs first linked to `/blog/<slug>/`. Quartz treats a root-relative href as a VAULT-internal path and rewrote it to `../blog/<slug>/`, i.e. `/notes/blog/<slug>/`, which does not exist. Stubs now use an ABSOLUTE URL via `BLOG_BASE` in make_stubs.py (defaults to the staging origin). An earlier attempt to solve this by extending `tooling/fix-base.mjs` with a /notes pass was WRONG and has been reverted; a comment there records why, so nobody re-adds it.

**AT PROD FLIP:** re-run `BLOG_BASE=https://monishver11.github.io python3 tooling/make_stubs.py`. That is the only change needed for the stubs.

### Verified
- Quartz build: 97 input files, 218 emitted, 0 broken internal links, no `goals.html`.
- Browser: online-softmax zettel shows the populated graph, backlinks including the new "K2 in CuTe [FA3]" stub, and its Related section; the fa3-k2 stub shows a correct absolute outbound link and a backlink to the zettel.

### Quartz footer fixed
Footer links were hardcoded to the bare domain, so a reader on staging /notes clicking "Blog" was sent to the OLD site. They now read `SITE_BASE_URL` (set in deploy.yml, defaults to the staging origin in quartz.layout.ts). One more thing to flip at prod flip.

## 2026-07-20: Projects section

Ported the 5 al-folio `_projects` portfolio pieces into a dedicated `/projects` gallery. User chose a dedicated gallery (option a) over folding them into the blog; the 3 small "Projects"-category blog posts (mlp-derivatives, mlp-fw-bwd, nyu-grad) stay as blog posts, unchanged.

### Shared converter refactor
The al-folio body pipeline (figures, captions, math delimiter normalisation, heading promotion, link rewriting, image copying) was extracted from `convert_post.convert()` into `convert_post.transform_body()`. Verified behaviour-preserving by diffing two re-converted posts against their prior output (identical). `tooling/convert_project.py` imports it, so projects get every math/figure fix for free.

### Two things _projects had that _posts did not (correcting my earlier "no video in the corpus")
That claim was true for _posts, NOT _projects. Both surfaced only because the converter reports missing images and dropped liquid:
1. **A space in an image filename** (`project_1/Lasso Regression_plot.png`). A markdown image URL cannot hold a raw space, so the link broke. Fix in transform_body: `fig_sub` percent-encodes spaces to `%20`; `copy_image` decodes before locating the file on disk. The public file keeps its real spaced name, the browser requests `%20`, served fine. Verified live (200).
2. **A `video.liquid` embed** (project 2, episode-success.mp4, 830 KB). The generic liquid-drop would have discarded it. Added a `video_sub` in transform_body -> HTML5 `<video controls muted loop playsinline>` (no autoplay, to avoid surprise motion). The mp4 is copied by the same image pass. Verified: readyState 4, controls present.

### Astro side
- New `projects` content collection (content.config.ts): title, description, thumb, importance.
- `convert_project.py`: SLUGS maps 1_project..5_project to real slugs (mta-transit-prediction, gaze-guided-rl, swap-regret, smallgraph-gcn, single-gpu-moe). Keeps `importance` for ordering, `thumb` for the card.
- `/projects/` gallery (src/pages/projects/index.astro): 2-col card grid, thumbnail + title + description, ordered by importance (MoE=1 first). `/projects/<slug>/` detail pages with giscus, no Subscribe/book chrome.
- "Projects" added to the nav between Book and Notes.
- `.post-video` style added to post.css.

### Images: earlier "leave the 47 uncopied" is now partly reversed
The project image folders (project_1..5 + proj2-1.jpg, 30 files) are now copied because the projects reference them. public/img went 135 -> 171 files. The genuinely-unused leftovers (old Projects-page duplicates that no ported content references, publication_preview, theme junk) remain uncopied. Copying is driven by references, so nothing orphaned.

### Verified
- Build 114 pages, 0 KaTeX errors across all 5 projects (swap-regret has 58 display-math blocks, all clean).
- 30 project images referenced, 0 missing, including the `%20` space one. Video loads with controls.
- Gallery ordered MoE, GCN, Gaze, Swap-regret, MTA (importance 1-5). Nav shows Projects.

## 2026-07-20: Book section (step 4)

The ML Theory posts assembled into an ordered book. User approved the structure with 5 decisions: exclude rl-intro and ds1, move subgradient into the SVM part before svm, keep ml-history as ch2 of Foundations, keep loss-functions closing "The learning problem", keep dual-problem after svm.

### Category change: new "Misc"
New "Misc" category added to `src/lib/categories.ts`, `src/content.config.ts` enum, and the converter's CATEGORY_MAP.

CORRECTION (same day): the book was first built with 60 chapters by keying off the merged "ML Theory" category. That was wrong. The book is the FOUNDATIONS course only, the 52 ML-NYU posts, which is exactly the "~52 ML posts" the original decision log called for. The old-site categories map cleanly:
- ML-NYU (52) -> ML Theory -> the Book.
- ADV-ML-NYU (8, the online-learning course) -> Misc. A distinct course, not foundations.
- RL-NYU (1, rl-intro), DS-NYU (1, ds1) -> Misc. ds1 is distributed systems, not ML.

So CATEGORY_MAP sends ADV-ML-NYU, RL-NYU, DS-NYU all to Misc; only ML-NYU and ADV-ML (the enum) stay ML Theory. Final: **ML Theory 52, Misc 10**. Converter is the source of truth, so re-porting preserves this.

### No duplicate URLs, same discipline as the vault
The book does NOT create `/book/<slug>/` pages. That would put all 60 posts at two URLs with two comment threads, the trap avoided in the vault. Instead:
- `/book/` is the table of contents (`src/pages/book/index.astro`).
- A post that appears in the manifest gets book chrome added to its existing `/blog/<slug>/` page: a part/chapter crumb above the title, and prev/next footer nav. One URL, full reading experience.

### Structure
- `src/data/book.json`: the manifest. 12 parts (Front matter, 10 numbered, Closing), **52 chapters** (online-learning part removed). Each part has a name and optional blurb.
- `src/lib/book.ts`: flattens the manifest into an ordered chapter list with running chapter numbers (front/back matter unnumbered, so numbers run 1-58), and gives `chapterFor(slug)` and `prevNext(slug)`. Single source of truth for both the TOC and the post chrome.
- The TOC page throws at build time if the manifest names a post that does not exist, so a typo fails the build instead of rendering a blank chapter.

Main reordering vs publication order: the online-learning and Bayesian threads were written in parallel (dates interleave them). The book separates them into Part 7 (Bayesian) and Part 8 (Online learning) so each reads start to finish.

### Verified in browser
- TOC: 60 chapters, 12 parts, numbers 1-58, all links 200.
- svm page: crumb "Book · Support vector machines and kernels · Chapter 19", prev = subgradient, next = dual-problem (the approved ordering).
- Edge cases: preface has next-only, wrapping-ml-basics has prev-only, fa3-k2 and rl-intro (non-book) have no chrome at all.
- Misc category page lists exactly ds1 and rl-intro; "Misc" shows in the nav row.
- Build 108 pages, 0 KaTeX errors, exactly 60 posts carry the book crumb.

### Known, inherent to reordering (not a bug)
A post's own prose may reference "the next post" by its publication neighbour, which the book reorders away from. E.g. svm's closing says subgradients come next, but the book places subgradient before svm. This is content for the user's own correction pass, not something the chrome can fix.

## 2026-07-20: 18 zettels written from the corpus

User chose option 3 (I draft them from post content) over extracting candidates for them to write. Noted the tradeoff at the time: these are my words describing their ideas. They are a starting point to be rewritten in the user's voice, not finished notes.

me.md rule 13 says to ask for `notes-style.md` on a notes task. Asked; it does not exist yet and the user said to proceed without it. Style followed is the three existing seed zettels: one idea, 2-4 short paragraphs, a concrete example rather than a bare definition (me.md rule 11), ending by linking outward.

Each was written from excerpts of the relevant posts so the framing is the user's, not generic. Where their language differs from the textbook default, theirs was kept: `bias-variance-tradeoff` leads with approximation error vs estimation error and hypothesis-space size, which is how the regularization post frames it, and mentions bias/variance as the classical synonym.

Written (21 zettels total now):
- Learning theory (11): empirical-risk-minimization, bias-variance-tradeoff, regularization-as-constraint, convex-duality, kernels-as-inner-products, margin-maximization, maximum-likelihood, bayesian-vs-frequentist, regret-minimization, boosting-as-additive-modeling, variance-reduction-by-averaging
- GPU (5 new): arithmetic-intensity, tiling, memory-coalescing, wgmma, warp-specialization
- Systems (2): mapreduce-model, exactly-once-semantics

Naming constraint worth remembering: **zettel filenames cannot collide with post slugs**, because Quartz resolves wikilinks by filename. `kernel-trick` is a post, so the concept note is `kernels-as-inner-products`. Same for tiling vs the GEMM posts.

Links: 216 -> **262 across 92 posts**, plus 21 interlinked zettels. 0 broken wikilinks anywhere. `vault/index.md` now lists all 21 grouped by area.

## 2026-07-20: /notes entry point + graph depth

User reported "the zettels are just 3, and I don't see the full graph". Two different things, one of which was not a bug:

1. **Graph depth.** The sidebar panel is the LOCAL graph, and Quartz's default is `depth: 1`, so it only ever showed a note's immediate neighbours (about 8 nodes). The full graph was always there but hidden behind the small expand icon on the panel. Set `localGraph: { depth: 2, scale: 1.2 }` in quartz.layout.ts; the sidebar now shows a real neighbourhood.
2. **Only 3 zettels is accurate, not a display problem.** There are exactly 3 atomic notes; the 93 posts are stubs in a separate folder. The real issue was that `vault/index.md` listed only those 3 and never mentioned the posts, so /notes read as a 3-note site. It also still linked to the OLD site's blog (same bug the footer had).

`vault/index.md` rewritten as a real entry point: explains zettels vs post stubs, points at the expand icon for the full graph, and lists one entry per reading thread (preface-ml, gpu-intro, simons-gemm-notes, cute, fa3-worklog, big-data-1-intro, silu-mul-...-kernel-vllm). 0 broken links, all 10 wikilinks resolve.

NOTE: the blog URL in index.md is hardcoded to the staging origin. It is prose, so no generator owns it; added to the prod-flip checklist in HANDOFF.

## 2026-07-20: PUBLISHED to staging (commit 071010c)

Everything above is live at https://monishver11.github.io/site-v2/. Deploy run 29750414583, success.

### Privacy gap caught at the last moment
`goals.md` was quartz-ignored but NOT gitignored, and this repo is PUBLIC. Quartz-ignoring only stops a file publishing to /notes; it does nothing about the repo itself. Personal goals would have been readable on GitHub. Now gitignored, matching the daily notes it feeds. Tradeoff accepted: it is local-only, so a fresh clone has no goals.md and the rollover prints `_No goals.md yet._` until recreated.

**General lesson for this repo: quartz-ignored != private. The repo is public. Anything that should stay personal needs BOTH.**

Pre-push audit (worth repeating before any future publish): confirmed only `vault/daily/README.md` from the daily folder, no `goals.md`, no `astro/dist` or `quartz/public` build output, and checked `.obsidian/workspace.json` for leaked file paths (clean, its only "daily" mentions are command-palette entries).

### Verified live
- 93 blog posts and 93 vault stubs in the repo, 141 images. No daily notes, no goals.md.
- `/site-v2/`, `/blog/`, `/blog/svm/`, `/blog/big-data-10-kafka/`, `/notes/`, `/404.html` all 200. `/notes/goals` correctly 404.
- big-data-10-kafka renders all 17 images including the 3 recovered ones (750x296, 652x277, 699x342), no raw liquid, 0 KaTeX errors.
- notes/posts/svm shows 6 backlinks (dual-problem, feature-maps, kernel-trick, max-margin-classifier, multiclass-svm, subgradient), 0 broken internal links, and footer links now correctly pointing at /site-v2.

## 2026-07-20: Post port, step 2 (90 posts converted, 8 math errors outstanding)

Sequence note: user confirmed zettel work (importing the corpus into the vault + retro-linking) comes AFTER this port and BEFORE the Book section, so HANDOFF's step 3 (Book) slides to step 4.

### Corpus survey (correcting a stale HANDOFF claim)
93 posts in the Jekyll corpus, 3 already ported, 90 converted this round. HANDOFF warned that "posts with video/audio/jupyter liquid need hand attention" - that is WRONG. There is no video, audio, jupyter, or iframe content anywhere in the corpus. The only liquid is `figure.liquid` (142, already handled) and `post_url` (5). The only `{{ }}` usage is 5 `site.baseurl`, all paired with post_url.

### Converter fixes made this round (tooling/convert_post.py)
1. **post_url resolution.** `{% post_url X %}` was falling into the generic "drop remaining liquid" path, silently turning 5 cross-post links into empty hrefs. Now resolved to `/blog/<slug>/`. Resolution is BY SLUG, not filename, so a wrong date in the reference still resolves; a wrong name is reported as an error. `{{ }}` expressions are now reported before being dropped too, instead of vanishing silently.
2. **YAML-safe frontmatter.** Titles containing double quotes (posts that quote a paper's name) were emitted as `title: "...\"...\""` = invalid YAML, and the build hard-failed on FPL-proof.md and gradient-boosting.md. Now emitted via `json.dumps` (a JSON string is always valid YAML).
3. **Old permalink rewriting.** Old format was `/blog/:year/:title/`; posts cross-link each other in that form, plus an absolute `https://monishver11.github.io/blog/YYYY/...` form, plus (in 2 posts) `http://localhost:8080/blog/YYYY/...` dev URLs committed by accident. All now rewritten to `/blog/<slug>/`.
4. **`split_trailing_close_delimiters`.** Root cause of a whole class of math breakage. remark-math closes a flow math block ONLY on a line that is exactly `$$`. The corpus closes some blocks with the delimiter glued to the last token (`t$$`). Kramdown/MathJax tolerated it; remark-math does not close there, so the block runs on and parses following PROSE as math. Fixed probability-1 entirely.

### Trap worth remembering
The permalink rewrite initially used a negative lookbehind for the domain, which matched inside `gregorygundersen.com/blog/2020/02/09/log-sum-exp/` and silently mangled that external citation to `/blog/02/09/`. The rule now fires only at the start of a link target (right after `](` or `href="`), which a full URL can never satisfy. Any future URL-rewriting rule in this converter needs the same care: the corpus cites external blogs whose URLs have the same shape as ours.

### Verified state after the port
- Build passes, 106 pages. All 93 frontmatter blocks parse (checked with js-yaml).
- 99 distinct internal `/blog/` links, **0 dead**. 131 referenced images, **0 missing**.
- External citations intact (gregorygundersen link verified byte-for-byte).
- **No silent math corruption.** Scanned every rendered KaTeX node's TeX annotation for swallowed prose (markdown emphasis or paragraph breaks inside math); the single hit is a legitimate `\begin{array}` pseudocode block. Every remaining problem announces itself as a visible error.

### Class A fixed: `normalize_display_delimiters` (5th converter fix)
Replaced the narrower `split_trailing_close_delimiters` with a general one. It puts EVERY unpaired `$$` on its own line, both directions, tracking block state and skipping code fences. A `$$...$$` pair fully contained on one line is left alone (that is genuine inline math, handled by convert_inline_math). Leading whitespace is preserved so math nested in a list item stays in its list item.

This is the single highest-value converter fix: the corpus shares the delimiter line constantly (`...distribution:  $$`, `   $$\hat{y}_t =`, `- $$`, `t$$`), and every instance silently slipped the pairing and swallowed following prose into math.

Side effect worth noting: it also fixed the 2 transformer-block-accounting `&` errors, which were NOT an authoring problem after all. The `\begin{aligned}` sat on the shared opener line and was being split off from its own block, so the alignment lost its environment. Class B was therefore 1 error, not 3.

KaTeX errors: 11 -> 8 -> **1**.

### Final round: 0 KaTeX errors (fixes 6-8)
6. **Multi-line `figure.liquid` (silent image loss).** The figure regex used `.` without `re.S`, so includes that wrap onto a second line never matched. In big-data-10-kafka that dropped 3 images AND left raw `{% include ... %}` text visible in the rendered post. 17 source includes had produced only 14 images. Now `flags=re.S` on both the figure substitution and the generic liquid drop. This is the bug behind "images not visible"; it was NOT a missing-copy problem.
   Note the shape of this failure: the missing-image check could not catch it, because the image was never referenced in the output at all. A check for "referenced but absent" is blind to "dropped entirely". Leftover-liquid count is the check that catches it.
7. **`escape_text_underscores`.** `\text{training_loss}` in regularization; KaTeX rejects a bare `_` inside `\text{}`, MathJax accepted it. 18 of 19 such spans in the corpus already wrote `\_`, so the rule only rescues stragglers. Done in the converter rather than by hand because re-running the converter overwrites hand edits.
8. **`rewrite_empty_links`.** `[label]()` -> `[label](/404)`. An empty href silently reloads the current page, which is worse than an honest not-found page.

New page `astro/src/pages/404.astro`: site-styled, explains that some posts link ahead to unwritten work, and redirects to the About page after 10 seconds with a visible countdown. The About link is a real anchor, so it works with JS disabled; the timer is progressive enhancement. Astro emits it as `dist/404.html`, which GitHub Pages serves for any unknown path.

### Verified state (final)
- Build 107 pages. **0 KaTeX errors across the whole corpus** (was 11).
- 0 leftover liquid tags. 135 images referenced, 0 missing. 99 internal links, 0 dead. 93/93 frontmatter parse.
- Browser: big-data-10-kafka renders all 17 images including the 3 recovered ones (real dimensions, no broken loads), no raw liquid on the page, 0 math errors. 404 page renders and the redirect to About was observed completing.

### Images: 141 of 188 copied, and that is the correct number
Every image any blog post references is copied and rendering. The 47 uncopied files (38 MB) are not blog assets: project_1 through project_5 (32 files, for the old Projects page, which the new site does not have), publication_preview (2, al-folio scaffolding), theme junk (1/2/3.jpg, logo, logo_old, template_error, prof_pic variants), and gemm/ (4 files that no post references, apparently drawn for a post never written).

DECISION: leave them uncopied. Copying would add 38 MB that CI builds and Pages serves for images nothing links to. If a Projects page is ever built on the new site, or the GEMM post gets written, copy the relevant subfolder from /Users/monishver/monishver11.github.io/assets/img at that point.

### Post-fix verification (all green)
- Build 106 pages. 93/93 frontmatter parse. 99 internal blog links, 0 dead. 132 images, 0 missing (131 -> 132: one image reference had been swallowed into math and now renders).
- All 15 rewritten cross-post links return 200 on the dev server; external gregorygundersen citation intact.
- Swallowed-prose scan clean (only hit is a legitimate `\begin{array}` pseudocode block in rwm).
- Browser: probability-1 0 errors / 112 math nodes with the previously-swallowed paragraph rendering as prose; transformer-block-accounting 0 errors with both aligned blocks rendering; blog index groups 2024/2025/2026 with the category row intact; no console errors.

Also: `fa3-k4.md` has `[K5: Warp specialization]()` with an empty href. That is authored-empty in the ORIGINAL post (K5 was never written), so it was ported faithfully. Left as-is pending user decision.

## 2026-07-20: Obsidian setup + daily rollover (step 1, script NOT yet scheduled)

- Obsidian pointed at `vault/` by user. Vault layout was already correct (`zettels/`, `posts/`, `daily/`, `templates/`, `index.md`); nothing moved.
- `.obsidian` config added: `daily-notes.json` (folder `daily`, format `YYYY-MM-DD`, template `templates/daily`) and `templates.json` (folder `templates`). Only the two core plugins needed; no third-party plugins. Note Linker / Semantic Auto-Linker deferred until the 91 posts are in the vault, since they have nothing to work on yet.
- Running-note model confirmed: ONE file, `vault/daily/today.md`, that the user writes in every day. Frontmatter `date:` stamps which day it belongs to.
- `vault/templates/daily.md`: frontmatter (date, tags) + sections Log / Learned / Goals / Open threads.
- Goals: new `vault/goals.md`, one `##` heading per active goal. The rollover copies those headings into each day's note as `###` with a blank bullet under each, so the daily note records what was done toward each goal. Deleting or demoting a heading in goals.md removes it from future daily notes.
- `tooling/daily-rollover.sh`: reads the stamped date in today.md; if it is not today, archives to `vault/daily/<stamped>.md` and reseeds today.md from the template. Idempotent with catch-up, so a Mac that was off for days still archives correctly and schedule time barely matters. Skips archiving if the note is unchanged from the template. Never clobbers an existing archive (falls back to `<date>-N.md`). Refuses to act if frontmatter has no `date:`. Logs to `vault/daily/.rollover.log`. Has `--dry-run`.
- Runs at 4am, NOT midnight: user decision that writing at 1am still counts as the previous day.
- DECISION: rollover stays a LOCAL launchd job, not GitHub Actions. Actions cannot do this job - the file it mutates is local, and `vault/daily/*` is gitignored by the locked privacy decision. Putting the vault in a repo to enable Actions would relitigate that, plus Actions cron drifts 10-60 min, the result would need pulling back to the Mac, and git rewriting a file Obsidian holds open invites conflicts. The "what if the Mac is off" worry is solved by the script's catch-up behavior instead.
- Tested against a throwaway copy of the vault, 6 scenarios: cold seed, same-day no-op, stale date with content (archives), stale date untouched (reseeds without an empty archive), archive collision (`-1` suffix), missing `date:` (refuses, exits non-zero). One bug found and fixed: command substitution stripped the trailing newline, so appended text ran onto the last heading.
- `tooling/com.monishver.daily-rollover.plist` written, installed, tested, and REMOVED. See below.

### BLOCKER FOUND: launchd cannot read files under ~/Downloads (macOS TCC)

Installed the launchd job and kickstarted it. It failed: `Operation not permitted`. Probed the actual permission boundary with a throwaway agent. A launchd agent under `~/Downloads` can:

| operation | result |
|---|---|
| stat / list files | allowed |
| **read file contents** | **DENIED** |
| write files | allowed |

Reading is precisely what the rollover does (today.md, daily.md, goals.md), so the job can never work while the project lives in `~/Downloads`. Moving only the script does NOT fix it (tried a wrapper in `~/Library/Scripts`; failed identically, because the unreadable thing is the vault, not the script). Note for future debugging: an `ls`-based probe reports success here and is misleading; only a probe that reads file CONTENTS exposes the restriction.

The script itself is correct and works when run from an interactive terminal, which has been granted disk access; launchd has not.

Options weighed: (1) move the project out of ~/Downloads, (2) grant Full Disk Access to /bin/bash, (3) drop the schedule and run on demand, relying on the script's catch-up behavior.

DECISION: option 3, no scheduled job. The launchd plist and the `~/Library/Scripts` wrapper were unloaded and deleted; nothing is scheduled and `~/Library/LaunchAgents` is clean. `tooling/com.monishver.daily-rollover.plist` is kept in the repo for reference only, unused, in case the project later moves out of ~/Downloads (at which point the move option becomes available and the plist works as written, after pointing ProgramArguments back at the repo script).

Option 2 was rejected on the merits: granting Full Disk Access to /bin/bash would give every script on the machine unrestricted disk access.

Trigger, decided separately: NONE. No shell profile hook, no alias. The user runs `tooling/daily-rollover.sh` by hand when sitting down to write. This is safe because the script is idempotent and catches up, so running it often is free and forgetting for a week costs nothing.

Documented in: the script's own header comment, HANDOFF.md, and here. Deliberately NOT in `vault/daily/README.md` - that file is read while writing, so it was trimmed to just how to run the script. The TCC reasoning is a maintenance concern, not a writing one.

First real goal set in `vault/goals.md`: "GPU/TPU kernel optimization and ML performance engineering" (work in the field and master it, kernel-level on both GPU and TPU plus the performance engineering around real ML systems). Placeholder removed. Today's note was regenerated to pick it up since it was still pristine.

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

## 2026-07-20: Staging deploy (done, LIVE)
- Repo: github.com/Monishver11/site-v2 (public). Live at https://monishver11.github.io/site-v2/ (user site untouched).
- Workflow .github/workflows/deploy.yml: Astro build + Quartz build into dist/notes + tooling/fix-base.mjs rewrites root-relative URLs for the /site-v2 prefix (skips /notes; Quartz emits relative links + NOTES_BASE_URL env). Deploys via actions/deploy-pages.
- Prod flip later: set BASE_PATH/NOTES_BASE_URL to root values, remove fix-base step, push to monishver11.github.io repo (or repoint Pages).
- gh needed `workflow` scope (user authorized device flow). Pages enabled via API with build_type=workflow.
- vault/daily/* gitignored (never reaches the public repo); quartz/ vendored (its .git removed), upgrades by re-clone.
- Verified live: about, kernel-trick (0 katex errors, sidenote, giscus, subscribe box), notes (graph/search/wikilinks).
- CI note: actions pin @v4 (node20 deprecation warnings, harmless for now).

## 2026-07-19: Blog feedback round 2 (done)
- Category pages flipped to newest-first; numbering + "in reading order" removed (ordering belongs to the Book).
- Headings lightened: weight 500 across h2-h6, strong inside headings inherits (no double-bold), h2 bottom border removed.
