# site-v2

Ground-up rebuild of monishver11.github.io.

- **`astro/`** — the main site (about, blog, book, thoughts, reads, reviews), Astro 5
- **`vault/`** — an Obsidian vault, published to `/notes` by Quartz v4
- **`quartz/`** — vendored Quartz v4, builds `vault/` into the notes site
- **`tooling/`** — the content pipelines (see below)

One GitHub Actions workflow builds both and deploys them as a single Pages artifact.

**Staging: https://monishver11.github.io/site-v2/** — the old al-folio site stays
primary until the port is finished.

Start with [HANDOFF.md](HANDOFF.md) for current state and next steps.
[progress.md](progress.md) is the decision log; [design.md](design.md) is the
architecture sketch.

## Commands

```sh
# main site
cd astro && npm run dev          # port 4322
cd astro && npm run build

# notes
cd quartz && npm run notes       # port 8081
cd quartz && npx quartz build -d ../vault

# port a Jekyll post into the Astro collection
python3 tooling/convert_post.py /path/to/_posts/<file>.md

# port an al-folio project into the projects gallery
python3 tooling/convert_project.py /path/to/_projects/<file>.md

# regenerate vault stubs + the link graph + the candidate report
python3 tooling/make_stubs.py

# archive yesterday's daily note and reseed today's (run by hand, see below)
./tooling/daily-rollover.sh
```

## How content flows

**Blog posts** live in `astro/src/content/blog/`. They are *generated* from the
old Jekyll corpus by `tooling/convert_post.py`. See
[tooling/CONVERSION.md](tooling/CONVERSION.md) for what the converter does and
the checks to run afterwards.

**Projects** in `astro/src/content/projects/` are the portfolio gallery at
`/projects`, generated from al-folio `_projects` by `tooling/convert_project.py`.
Both converters share `convert_post.transform_body()`, so a fix to the body
pipeline (math, figures, images, video) benefits both.

**Vault stubs** in `vault/posts/` are generated from those posts by
`tooling/make_stubs.py`. One short note per post, linking out to the real thing.
The blog posts themselves are deliberately *not* copied into the vault, which
would put the same content at two URLs with two sets of comments.

**Zettels** in `vault/zettels/` are hand-written atomic notes. Nothing generates
them except the `## Related posts` section at the bottom of each.

**The link graph** lives in `tooling/post-links.json`: `threads` are ordered
reading sequences giving prev/next, `bridges` are conceptual pairs with reasons,
`zettels` maps concept notes to posts. Edit it and re-run `make_stubs.py`.

## Things that will bite you

**Generated files are generated.** Re-running `convert_post.py` overwrites hand
edits to a post. Fix recurring problems as rules in the converter, not as edits
to the markdown it produces. (The batch skips `sgd`, `fa3-cute` and
`kernel-trick` because they carry hand edits.)

**Stub edits survive, in one place only.** Anything below the
`<!-- links below this line are kept when regenerating -->` marker in a stub is
preserved by `make_stubs.py`. Anything above it is not.

**Zettel filenames cannot collide with post slugs.** Quartz resolves wikilinks
by filename across the whole vault, so a zettel named `kernel-trick` would fight
with the post stub of the same name. That is why the concept note is
`kernels-as-inner-products`. Check `vault/posts/` before naming a new zettel.

**Quartz-ignored is not private.** `ignorePatterns` in `quartz.config.ts` only
stops a file publishing to `/notes`. **This repo is public.** Anything personal
needs a `.gitignore` entry too. `vault/daily/` and `vault/goals.md` have both.

**Quartz `ignorePatterns` are path globs.** A bare name matches a *directory*
only. To exclude a single file you must write the extension (`"goals.md"`, not
`"goals"`), and getting it wrong fails silently. Check the built output.

**Vault notes must link out with absolute URLs.** Quartz treats a root-relative
href as a vault-internal path, so `/blog/x/` becomes `/notes/blog/x/`. Stubs use
`BLOG_BASE` in `make_stubs.py`. Do not try to patch this in `fix-base.mjs`; that
was tried and reverted.

**URL rewriting must not match on domain alone.** The corpus cites external
blogs whose URLs have the same `/blog/YYYY/slug/` shape as the old permalinks. A
rule anchored on the domain silently mangled a `gregorygundersen.com` citation.
Anchor to link-target position instead.

**The daily rollover is manual, by design.** launchd cannot read file contents
under `~/Downloads` (macOS TCC), so a scheduled job fails with "Operation not
permitted". The script is idempotent and catches up instead, so running it late
or twice costs nothing. Details in [vault/daily/README.md](vault/daily/README.md).

**The graph panel is the *local* graph.** It shows a note's neighbourhood
(`depth: 2`). The full graph is behind the expand icon in the panel's corner.

**Build output is never committed.** `astro/dist/` and `quartz/public/` are
gitignored; CI builds fresh.

## At prod flip

1. Set `BASE_PATH` and `NOTES_BASE_URL` to root values in `.github/workflows/deploy.yml`
2. Set `SITE_BASE_URL` there too (drives the notes footer links)
3. Remove the `fix-base.mjs` step
4. Re-run `BLOG_BASE=https://monishver11.github.io python3 tooling/make_stubs.py`
5. Fix the one hardcoded blog URL in `vault/index.md` (prose, no generator owns it)
6. Decide the redirect strategy: old permalinks were `/blog/:year/:title/`, new are `/blog/<slug>/`
