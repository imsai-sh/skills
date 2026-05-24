#!/usr/bin/env python3
"""Generate SKILL.md as a llms.txt-style index over the references/ tree.

Usage:
    python3 generate-skill-md.py <skill_root_dir> <llms_txt_path>
"""
import re, sys
from pathlib import Path

if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)

ROOT    = Path(sys.argv[1])
LLMSTXT = Path(sys.argv[2])
REFS    = ROOT / "references"

# Title + description map from llms.txt
meta = {}  # slug -> (title, desc)
for line in LLMSTXT.read_text().splitlines():
    m = re.match(r'- \[(.+?)\]\(https://code\.claude\.com/docs/en/(.+?)\.md\):?\s*(.*)', line)
    if m:
        meta[m.group(2)] = (m.group(1), m.group(3).strip())

# Walk references/, get slugs (relative path without .md, excluding _meta/)
slugs = []
for f in REFS.rglob("*.md"):
    rel = f.relative_to(REFS)
    if rel.parts[0] == "_meta": continue
    slugs.append(str(rel.with_suffix("")).replace("\\","/"))
slugs.sort()

def group(s):
    if s.startswith("agent-sdk/"): return "Agent SDK"
    if s.startswith("whats-new/"): return "What's new (weekly changelog)"
    return "Core docs"

groups = {}
for s in slugs:
    groups.setdefault(group(s), []).append(s)

out = [
    "---",
    "name: claude-code-docs",
    'description: Local mirror of the full Claude Code documentation set (code.claude.com/docs), one reference file per page. Use for any question about Claude Code CLI, IDE integrations, plugins, skills, hooks, MCP, the Agent SDK, deployment, configuration, or reference material. Load only the reference files relevant to the user question. Methodology and re-scrape scripts live in references/_meta/.',
    "---",
    "",
    "# Claude Code Documentation",
    "",
    "> Official documentation for Claude Code, Anthropic's agentic coding tool available in the terminal, IDE, desktop app, and browser. Covers installation, configuration, skills, subagents, hooks, MCP, the Agent SDK, and reference material.",
    "",
    "## Build provenance",
    "",
    "This skill mirrors code.claude.com/docs as one reference file per page. Each `references/<slug>.md` is the verbatim markdown source returned by Mintlify's `.md` URL endpoint (e.g. `cli-reference.md` is `https://code.claude.com/docs/en/cli-reference.md`). No reformatting, summarization, or re-scraping — refresh by re-running `references/_meta/scripts/refetch-md.py`. Full methodology and gotchas in `references/_meta/scraping-method.md`.",
    "",
    "## When to Use This Skill",
    "",
    "Whenever the user asks about Claude Code features, configuration, plugins, skills, hooks, MCP, the Agent SDK, deployment options, or reference material. Each documentation page is preserved as its own file under `references/` — load only what you need rather than dumping the whole skill into context.",
    "",
    f"## References ({len(slugs)} files, one per documentation page)",
    "",
]
for header in ["Core docs", "Agent SDK", "What's new (weekly changelog)"]:
    if header not in groups: continue
    out += [f"### {header}", ""]
    for s in groups[header]:
        title, desc = meta.get(s, (s, ""))
        line = f"- [{title}](references/{s}.md)" + (f": {desc}" if desc else "")
        out.append(line)
    out.append("")

out += [
    "## Meta",
    "",
    "- [How this skill was built](references/_meta/scraping-method.md): Source, tools, exact recipe, refresh procedure, and known gotchas.",
    "- [Fetcher script](references/_meta/scripts/refetch-md.py): Curls the Mintlify `.md` endpoint for every page in llms.txt; run any time to refresh the snapshot.",
    "- [SKILL.md generator](references/_meta/scripts/generate-skill-md.py): Regenerates this file from the references/ tree.",
    ""
]
(ROOT / "SKILL.md").write_text("\n".join(out))
print(f"Wrote {ROOT / 'SKILL.md'}")
