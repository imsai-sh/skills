# How this skill was built

This file documents exactly how the knowledge in this skill was produced, so you (or anyone) can refresh it when the upstream docs change, or apply the same recipe to a different docs site.

## TL;DR

The Claude Code docs are hosted on Mintlify. Mintlify exposes a **raw markdown endpoint** at the `.md` suffix of every doc URL — `<page>.md` returns the page's source markdown directly, bypassing the React-rendered HTML entirely. We just `curl` each `.md` URL listed in [`llms.txt`](https://code.claude.com/docs/llms.txt) and save the result.

That's it. No scraper, no Playwright, no selector hacks. ~45 seconds end-to-end for the full 140-page snapshot.

## Why not use a generic scraper (e.g. skill-seekers)?

We tried that first and it produced badly broken output. **Skip this section unless you're curious or porting the recipe to a docs site that doesn't expose `.md` endpoints.**

skill-seekers (or any `requests`-based HTML scraper) hits the HTML URL (no `.md` suffix), parses the DOM, and extracts content via CSS selectors. On Mintlify sites:

- Initial server-side HTML is a React shell — page chrome + code blocks (kept inline for SEO), but **reference tables, flag tables, structured prose are hydrated client-side**.
- A `requests` scraper sees the SSR shell only. Result: every reference-heavy page (`cli-reference`, `commands`, `settings`, `hooks`, `errors`, `tools-reference`, `slash-commands`, …) ends up with intro + footer + naked code blocks, no tables, no descriptive prose.

Empirically: `cli-reference` HTML scrape = 4 KB (essentially empty). Same page via `.md` endpoint = 57 KB with all 68 flag rows intact.

A browser-mode scraper (Playwright) would fix this but is overkill — heavier install, slower, and entirely unnecessary when the raw markdown is one URL away.

## The recipe (5 minutes)

### Step 1: Get the page inventory from `llms.txt`

Mintlify-hosted sites publish a machine-readable doc index at `/llms.txt`. Each entry is a link to a `.md` URL.

```bash
curl -s https://code.claude.com/docs/llms.txt > /tmp/llms.txt
wc -l /tmp/llms.txt   # 146 lines, 140 entries on this snapshot
```

Format:

```markdown
- [Page title](https://code.claude.com/docs/en/<slug>.md): Description.
```

### Step 2: Fetch every `.md` URL

```bash
python3 ./scripts/refetch-md.py /tmp/llms.txt ../   # writes refs/<slug>.md for all 140
```

The script (see `scripts/refetch-md.py`):

1. Parses `llms.txt` → list of `(title, url, slug, description)` tuples.
2. For each, `curl -sS <url>` → writes to `<refs-root>/<slug>.md`.
3. Prepends a single-line HTML comment with provenance: `<!-- source: <url> | scraped: YYYY-MM-DD -->`.
4. Strips the leading `> ## Documentation Index ...` blockquote that Mintlify injects (it's identical on every page, low signal).
5. Sleeps 300 ms between requests to be polite.

Nested URLs like `agent-sdk/quickstart` and `whats-new/2026-w13` automatically land in `refs/agent-sdk/` and `refs/whats-new/` because `mkdir -p` follows the slug's directory structure.

### Step 3: Regenerate `SKILL.md`

```bash
python3 ./scripts/generate-skill-md.py ../../ /tmp/llms.txt
```

The generator walks `references/` (skipping `_meta/`), groups slugs into "Core docs / Agent SDK / What's new", and writes a `SKILL.md` whose body mirrors the structure of `llms.txt` — one bullet per page with the upstream description, linked to the local mirror.

## Refreshing the skill (when upstream docs change)

```bash
# 1. Re-fetch the index
curl -s https://code.claude.com/docs/llms.txt > /tmp/llms.txt.new

# 2. Diff against the previous snapshot to see new/removed pages (optional but useful)
diff <(grep -oE 'docs/en/[a-z0-9/-]+\.md' /tmp/llms.txt     | sort -u) \
     <(grep -oE 'docs/en/[a-z0-9/-]+\.md' /tmp/llms.txt.new | sort -u)
mv /tmp/llms.txt.new /tmp/llms.txt

# 3. Re-fetch everything (overwrites in place)
python3 references/_meta/scripts/refetch-md.py /tmp/llms.txt references

# 4. Regenerate SKILL.md
python3 references/_meta/scripts/generate-skill-md.py . /tmp/llms.txt

# 5. (manual) review git diff to spot deleted slugs that should be removed
git diff --stat references/
```

## Known gotchas

1. **Stale slug in `llms.txt`** — `microsoft-foundry` was renamed to `azure-ai-foundry` upstream. The new `llms.txt` no longer lists `microsoft-foundry`, so nothing breaks for current snapshots; just be aware that older snapshots may have a renamed/empty page.

2. **404s and one-off content moves** — When pages are removed or renamed, the curl will get a 404 and the script counts it under `fail`. Inspect failures, prune leftover `<slug>.md` files manually.

3. **Three reference files >100 KB** — `hooks.md` (189 KB), `settings.md` (127 KB), `commands.md` (74 KB), `agent-sdk/python.md` (~70 KB). These are intrinsically long pages (full schemas / API references). Splitting them would break the single-page-per-file principle. Acceptable cost — Claude only loads them on demand.

4. **Don't strip the leading H1 / description** — earlier versions of the script added their own `# Title\n\n> Description` header, then suffered duplicates because the upstream `.md` starts with the same. Current `refetch-md.py` adds only the HTML-comment provenance line and lets the upstream content provide its own title.

## Why per-page (not by category)?

Per-page is the obvious choice once you decide to fetch from `llms.txt`. Each entry in `llms.txt` is one page → one file. No categorization disputes, predictable navigation, demand-driven context loading (Claude reads one ~5 KB file instead of a 100 KB category dump).

An earlier iteration tried category-grouping (11, 14, 28 categories). It worked but had two structural problems:

- Categorization is fragile (substring matching against URL slug). 75/142 pages fell into `other.md` (53 %) in the official skill-seekers config.
- Even with careful tuning (28-category config got it down to 1 page in `other.md`), every category file ended up 10–25 KB — Claude loads a lot of irrelevant material per query.

Per-page sidesteps both.

## Why the upstream content is good enough

The `.md` source is hand-authored markdown by the Mintlify-using docs team. Claude already speaks markdown natively. We add nothing beyond:

- HTML-comment provenance (`<!-- source: ... | scraped: ... -->`) so Claude knows where it came from.
- Directory layout matching the URL path so file lookups are predictable.
- A `SKILL.md` index with the upstream description for each page (so Claude can decide what to load without opening every file).

No reformatting, no extra summarization, no embeddings. Reproducible from the recipe above.

## Applying this recipe to other docs sites

This works for **any Mintlify-hosted docs site**. Check by adding `.md` to any doc URL — if it returns markdown, you're golden. Examples that work:

- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching.md`
- `https://docs.cursor.com/cmdk/overview.md`
- `https://docs.windsurfai.com/<...>.md`

Sites that publish `llms.txt` make it trivial (the URL list is given). Sites without `llms.txt` need a sitemap or manual enumeration.

For **non-Mintlify sites**: fall back to a real scraper. skill-seekers with the right CSS selectors, or Playwright for SPA-heavy sites.

## Files in this directory

- `scraping-method.md` — this file.
- `scripts/refetch-md.py` — fetcher. Run any time to refresh.
- `scripts/generate-skill-md.py` — index generator. Run after `refetch-md.py`.

## Credits

- Documentation source: Anthropic, [code.claude.com/docs](https://code.claude.com/docs/en/).
- `llms.txt` standard: [llmstxt.org](https://llmstxt.org/) by Jeremy Howard / Answer.AI.
- Mintlify's `.md` endpoint design — providing raw markdown to LLM consumers without needing screen-scraping.
