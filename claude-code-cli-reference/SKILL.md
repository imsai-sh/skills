---
name: claude-code-cli-reference
description: |
  Use when looking up the syntax, flags, or behavior of any `claude` CLI command —
  including session management, authentication, plugin/MCP config, background agents,
  worktree, print/headless mode, permission modes, system prompts, or model/budget controls.
  Triggers in Chinese: "claude 命令", "claude cli", "claude 参数", "claude flag",
  "claude -p", "claude -c", "claude -w", "claude 怎么用", "claude 用法",
  "headless 模式", "后台 agent", "claude worktree", "claude 怎么传 system prompt".
  In English: "claude CLI", "claude command", "claude flag", "claude option",
  "claude --bare", "claude headless", "claude background agent", "how to use claude CLI",
  "claude print mode", "claude resume session", "claude system prompt".
  Mirrors the official Anthropic cli-reference at code.claude.com/docs/en/cli-reference.
---

# Claude Code CLI Reference

Local mirror of the official Claude Code CLI reference (<https://code.claude.com/docs/en/cli-reference.md>). For when the agent (or you) wants to confirm a `claude ...` invocation without the upstream doc loaded.

## When to use this skill

- A task includes `claude ...` subcommands, or flags like `-p` / `-c` / `-r` / `-w`, and you need to confirm syntax or behavior.
- Scripting a Claude Code invocation (CI, headless, batch).
- Wiring up MCP servers, plugins, Remote Control, worktrees, or background agents.
- Picking the right permission mode or system-prompt override.
- Need to know if a flag is print-mode-only or works everywhere.

## Where to find things

| What you want | Where to look |
| :-- | :-- |
| Full subcommand table (~30 commands) + examples | [references/commands.md](references/commands.md) |
| Full flag table (~70 flags) | [references/flags.md](references/flags.md) |
| The four system-prompt flags compared | [references/flags.md#system-prompt-flags](references/flags.md#system-prompt-flags) |
| Common one-line recipes | this file (below) |

## Common patterns

**Clean headless invocation (CI / scripts)**
```bash
claude --bare -p "summarize CHANGELOG" --max-budget-usd 0.5 --max-turns 3
```
`--bare` skips auto-discovery of hooks / skills / plugins / MCP / auto memory / CLAUDE.md, so cold starts are fast.

**Continue or resume**
```bash
claude -c                              # continue the most recent conversation in this dir
claude -r "auth-refactor" "Finish it"  # resume by name
claude --resume <uuid> --fork-session  # resume but get a fresh session ID
claude --from-pr 123                   # resume the session linked to that PR
```

**Worktree workflows**
```bash
claude -w feature-auth                 # session inside .claude/worktrees/feature-auth
claude -w "#123"                       # branch a worktree off GitHub PR #123
claude -w feature-auth --tmux          # split-pane via iTerm2 or classic tmux
```

**Background / multi-agent**
```bash
claude --bg "investigate flaky test"   # spawn a background session, returns id
claude agents                          # open the agent view
claude attach <id>                     # pull background session into current terminal
claude logs <id>                       # tail recent output
claude respawn <id>                    # restart a stopped session, conversation intact
claude stop <id> / claude rm <id>      # stop / remove
```

**Web ↔ Local**
```bash
claude --remote "Fix the login bug"    # open a new web session on claude.ai
claude --teleport                      # pull a web session into your local terminal
claude --remote-control "My Project"   # local interactive + claude.ai can drive it
```

**Improve prompt-cache hits across users / machines**
```bash
claude -p --exclude-dynamic-system-prompt-sections "query"
```
Moves per-machine sections (cwd, env info, memory paths, git-repo flag) out of the system prompt and into the first user message, so the cached prompt prefix can be shared.

**Start in plan mode, allow bypass later**
```bash
claude --permission-mode plan --allow-dangerously-skip-permissions
```

**Side-load a plugin for this session only**
```bash
claude --plugin-dir ./my-plugin
claude --plugin-url https://example.com/plugin.zip
```

**Strict MCP (ignore all other MCP sources)**
```bash
claude --strict-mcp-config --mcp-config ./mcp.json
```

**Define a subagent without writing files**
```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'
```

**Structured JSON output (for scripts that consume it)**
```bash
claude -p --output-format json --json-schema '{"type":"object","properties":{...}}' "query"
```

**Long-lived auth for CI**
```bash
claude setup-token                     # prints a long-lived OAuth token (not stored). Requires a Claude subscription.
claude auth login --console            # use an Anthropic Console API key (billing) instead of a subscription
claude auth status                     # JSON; exit 0 = logged in, 1 = not
```

## Hidden gems

1. **`--bare`** — skips all auto-discovery (hooks / skills / plugins / MCP / auto memory / CLAUDE.md). Big win for scripted calls.
2. **`-w "#123"`** — branch a worktree directly off a PR number or PR URL.
3. **`--max-budget-usd` + `--max-turns`** — safety valves for unattended runs.
4. **`--exclude-dynamic-system-prompt-sections`** — big prompt-cache hit-rate boost when many users / machines run the same task.
5. **`claude --teleport`** — pull a web session back to your local terminal to keep going.
6. **`claude project purge <path> --dry-run`** — wipe one project's local state (transcripts, task lists, debug logs, edit history, prompt history, the `~/.claude.json` entry). Always `--dry-run` first.
7. **`claude auto-mode defaults > rules.json`** — dump the built-in auto-mode classifier rules so you can author overrides.

## Print-mode-only flags

These only take effect with `-p` / `--print` (rejected or ignored in interactive mode):

`--fallback-model`, `--init`, `--maintenance`, `--include-hook-events`, `--include-partial-messages`, `--input-format`, `--json-schema`, `--max-budget-usd`, `--max-turns`, `--no-session-persistence`, `--output-format`, `--permission-prompt-tool`, `--replay-user-messages`, `--exclude-dynamic-system-prompt-sections`

## Conventions and gotchas

- `claude --help` **does not list every flag** — a flag's absence from `--help` does not mean it is unavailable. Use this reference instead.
- `--system-prompt` and `--system-prompt-file` are mutually exclusive. Either `--append-*` flag can be combined with either replacement flag.
- Mistyped subcommands trigger a "Did you mean ...?" suggestion (`claude udpate` → `claude update`).
- In scripts, use `claude auth status` exit code (0 = logged in) rather than grepping output.
- `claude install` accepts `stable` / `latest` / explicit versions like `2.1.118`.

## Source

- Upstream: <https://code.claude.com/docs/en/cli-reference.md>
- If upstream changes, re-fetch and replace the two `references/*.md` files — `SKILL.md` itself rarely needs changes.
