# skills

> 中文版：[README.zh.md](README.zh.md)

A collection of [Agent Skills](https://agentskills.io/specification) for Claude Code, Codex, Cursor, Gemini CLI, and other Agent Skills-compatible tools.

## Skills

| Skill | What it does |
|---|---|
| [ios-icp-filing](./ios-icp-filing/SKILL.md) | Extract Bundle ID, distribution-cert SHA-1, and RSA public-key modulus from a signed IPA, formatted for Tencent Cloud / Aliyun / Huawei Cloud ICP filing forms |
| [finish-worktree](./finish-worktree/SKILL.md) | Merge the current worktree's changes back to main and clean up the worktree + branch. Auto-detects nested child repos and handles them child-first, parent-second. Never pushes by default |
| [discard-worktree](./discard-worktree/SKILL.md) | Destructively discard all changes in the current worktree (committed or not), delete the worktree and branch. Same nested-repo handling, reverse-order cleanup |
| [git-worktree-setup](./git-worktree-setup/SKILL.md) | Generate a tailored `setup-worktree.sh` + agent hook for your repo so new worktrees boot ready to run (`node_modules` symlinked / `.env` copied / dev port hashed / DB state shared or isolated) |
| [claude-code-cli-reference](./claude-code-cli-reference/SKILL.md) | Local mirror of the official Claude Code CLI reference — subcommands, flags, common one-line recipes, print-mode-only flags, gotchas. Look up `claude ...` syntax without loading the upstream doc |
| [claude-code-docs](./claude-code-docs/SKILL.md) | Local mirror of the **full** Claude Code documentation set (140+ pages from code.claude.com/docs), one reference file per page, mirroring the upstream `llms.txt` index. Covers CLI, IDE integrations, plugins, skills, hooks, MCP, the Agent SDK, deployment, configuration, and the weekly changelog. Includes the methodology + re-scrape scripts in `references/_meta/` so the skill is self-refreshing |
| [volcengine-rtc-docs](./volcengine-rtc-docs/SKILL.md) | VolcEngine RTC (火山引擎实时音视频) documentation, split into 248 TOC-indexed PDFs. Covers core RTC SDK, AI voice agents, hardware-side agents, RTS signaling, whiteboard, legacy IM. PDFs are git-LFS-tracked (~128MB) |
| [hackernews-show-hn](./hackernews-show-hn/SKILL.md) | Prepare or troubleshoot a Hacker News Show HN submission. Covers the silent new-account throttle (the `/showlim` redirect), karma thresholds, 1–2 week account-warming plan, post-template, and backup channels (Reddit / Twitter / awesome-* / etc.) while the HN cooldown clears. Includes verbatim local copies of pg's Show HN guidelines, HN community guidelines, and the throttle page |

## Install


```bash
npx skills add imsai-sh/skills

npx skills add imsai-sh/skills --skill git-worktree-setup
```

## License

[MIT](./LICENSE) — use, modify, redistribute, even commercially. Keep the original copyright notice.
