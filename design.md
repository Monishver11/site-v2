# Site v2 rough outline

Status: draft for discussion, 2026-07-19. Nothing built yet.

## Architecture

Two builds, one domain (monishver11.github.io), deployed together by one GitHub Action:

```
repo: site-v2
├── astro/            main site (Astro)
│   ├── /             about (leaf touch)
│   ├── /blog         tabs: written | excalidraw
│   ├── /book         ML fundamentals book (52 posts as ordered chapters)
│   ├── /thoughts     tabs: mine | others
│   ├── /reads        tabs: technical | non-technical
│   └── /reviews      weekly/monthly reflections (public, distilled from private daily logs)
├── vault/            Obsidian vault (zettelkasten source of truth)
│   ├── zettels/      atomic notes, wikilinked
│   ├── posts/        converted blog posts (part of the graph)
│   ├── daily/        PRIVATE, excluded from publish
│   └── templates/
└── .github/workflows/
    ├── deploy.yml    build Astro + Quartz, publish to Pages
    └── nightly.yml   12am: archive daily note, reset for new day (private housekeeping)
```

- Quartz builds `vault/` (minus private folders) to `/notes`: wikilinks, backlinks, graph, search, LaTeX.
- Astro handles everything else: off-white theme (whiter than siboehm), sidenotes, Buttondown embed per post, Google Analytics, giscus.
- Obsidian is the writing environment; git is the sync + publish pipeline.

## Content flow

1. Write in Obsidian (zettels, drafts, daily logs).
2. Long-form drafts graduate to Astro blog posts; each post keeps a zettel stub in the graph linking to it.
3. Retro-linking pass on converted posts with Note Linker / Semantic Auto-Linker plugins.
4. Daily logs private; weekly/monthly review is written from them and published to /reviews.

## Book (/book)

The ~52 ML posts, reorganized into parts/chapters (intro ML, optimization, kernels/SVMs, Bayesian, boosting/trees, online learning, structured prediction, wrap-up). GitBook-style: fixed sidebar with chapter tree, prev/next footer nav, same math rendering. Built as an Astro collection with an ordered manifest, so no third tool.

## Settled (2026-07-19, round 2)

- Thoughts: mine/others tabs kept; credited-to-a-person = others, date-only/uncredited = mine; grouped by year inside each tab.
- Book: built as Astro /book section (no GitBook/mdBook).
- Reviews: automation drafts from daily logs, user edits, then publish. Cadence: weekly proposed, TBC.
- 12am job: vault housekeeping only (archive + reset daily note), publishes nothing.

## Open items

- Review cadence: weekly vs monthly (weekly proposed).
- Blog topic taxonomy replacing course categories (proposal: ML Theory, GPU/Performance, Big Data Systems, Projects) - not yet confirmed.
- Visual system: palette, typography, dark mode (discussion in progress).
- Excalidraw pipeline: draw in Obsidian excalidraw plugin, export SVG/PNG into gallery tab + embed in posts.
