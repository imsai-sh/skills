#!/usr/bin/env python3
"""Fetch Claude Code doc pages via Mintlify .md endpoint. Minimal header to avoid duplicating upstream."""
import re, subprocess, sys, time
from pathlib import Path

LLMS_TXT = Path(sys.argv[1]); REFS = Path(sys.argv[2])
entries = []
for line in LLMS_TXT.read_text().splitlines():
    m = re.match(r'- \[(.+?)\]\((https://code\.claude\.com/docs/en/(.+?)\.md)\):?\s*(.*)', line)
    if m: entries.append((m.group(1), m.group(2), m.group(3), m.group(4).strip()))
print(f"{len(entries)} entries")

REFS.mkdir(parents=True, exist_ok=True)
ok = fail = 0
for i, (title, url, slug, desc) in enumerate(entries, 1):
    out = REFS / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", "30", "-w", "%{http_code}",
                            "-o", "/tmp/_page.md", url], capture_output=True, text=True)
        if r.stdout.strip()[-3:] != "200":
            print(f"  [{i}/{len(entries)}] ❌ {slug}"); fail += 1; continue
        body = Path("/tmp/_page.md").read_text()
        # Strip Mintlify's repeating "> ## Documentation Index" block (3-4 leading blockquote lines)
        body = re.sub(
            r'^> ## Documentation Index\s*\n(?:> [^\n]*\n)+\n*',
            '', body, count=1, flags=re.MULTILINE
        )
        # Minimal header — just provenance metadata, then upstream content (which has its own # Title + > Desc)
        header = f"<!-- source: {url} | scraped: 2026-05-25 -->\n\n"
        out.write_text(header + body.lstrip())
        ok += 1
        if i % 20 == 0: print(f"  [{i}/{len(entries)}] ok={ok}")
        time.sleep(0.3)
    except Exception as e:
        print(f"  [{i}/{len(entries)}] ❌ {slug}: {e}"); fail += 1
print(f"Done: {ok}/{len(entries)} ok")
