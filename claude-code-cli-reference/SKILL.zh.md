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

# Claude Code CLI 速查

官方 Claude Code CLI 参考的本地镜像（<https://code.claude.com/docs/en/cli-reference.md>）。当 agent（或你自己）想确认 `claude ...` 怎么用、不希望联网拉文档时翻这里。

## 什么时候用

- 用户或任务里出现 `claude ...` 子命令、`-p` / `-c` / `-r` / `-w` 等 flag，需要确认语法或行为。
- 要写脚本调用 Claude Code（CI、headless、batch）。
- 要配 MCP server、plugin、Remote Control、worktree、background agent。
- 选择合适的 permission mode 或 system-prompt 改写方式。
- 想了解某个 flag 是 print-mode-only 还是全模式可用。

## 资料在哪里

| 你想查的东西 | 看这里 |
| :-- | :-- |
| 完整子命令表（~30 条）+ 用法示例 | [references/commands.md](references/commands.md) |
| 完整 flag 表（~70 条） | [references/flags.md](references/flags.md) |
| 4 个 system-prompt flag 的对比 | [references/flags.md#system-prompt-flags](references/flags.md#system-prompt-flags) |
| 常用组合 | 本文件下方 |

## 常用组合

**干净的 headless 调用（CI / 脚本）**
```bash
claude --bare -p "summarize CHANGELOG" --max-budget-usd 0.5 --max-turns 3
```
`--bare` 跳过 hooks / skills / plugins / MCP / auto memory / CLAUDE.md 自动发现，冷启动飞快。

**继续 / 恢复会话**
```bash
claude -c                              # 继续当前目录最近一次 conversation
claude -r "auth-refactor" "Finish it"  # 按名字恢复
claude --resume <uuid> --fork-session  # 恢复但 fork 出新 session ID
claude --from-pr 123                   # 恢复关联到这个 PR 的 session
```

**Worktree 工作流**
```bash
claude -w feature-auth                 # 在 .claude/worktrees/feature-auth 起 session
claude -w "#123"                       # 从 GitHub PR #123 起 worktree
claude -w feature-auth --tmux          # 配合 tmux（或 iTerm2 原生 pane）
```

**后台 / 多 agent**
```bash
claude --bg "investigate flaky test"   # 后台起 session，返回 id
claude agents                          # 打开 agent view
claude attach <id>                     # 把后台 session 拉到前台
claude logs <id>                       # 看输出
claude respawn <id>                    # 重启停掉的 session
claude stop <id> / claude rm <id>      # 停 / 删
```

**Web ↔ Local**
```bash
claude --remote "Fix the login bug"    # 在 claude.ai 上开一个 web session
claude --teleport                      # 把 web session 拉回本地终端
claude --remote-control "My Project"   # 本地交互 + 允许 claude.ai 控制
```

**跨用户 / 跨机器 跑同任务时省 cache**
```bash
claude -p --exclude-dynamic-system-prompt-sections "query"
```
把"当前工作目录 / 机器环境 / memory 路径 / 是否 git repo"这些每机器不同的段落从 system prompt 移到首条 user message，让 prompt cache 跨用户复用。

**从 plan 模式起手，允许后续切到 bypass**
```bash
claude --permission-mode plan --allow-dangerously-skip-permissions
```

**临时挂一个 plugin（不入 registry）**
```bash
claude --plugin-dir ./my-plugin
claude --plugin-url https://example.com/plugin.zip
```

**严格 MCP 配置（忽略所有其他 MCP 源）**
```bash
claude --strict-mcp-config --mcp-config ./mcp.json
```

**动态定义 subagent（不写文件）**
```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'
```

**结构化输出（脚本里消费 JSON）**
```bash
claude -p --output-format json --json-schema '{"type":"object","properties":{...}}' "query"
```

**Auth（CI 用长期 token）**
```bash
claude setup-token                     # 打印长期 OAuth token（不落盘）；需 Claude 订阅
claude auth login --console            # 用 Anthropic Console API key 计费
claude auth status                     # JSON；退出码 0=已登录，1=未登录
```

## 隐藏宝藏

1. **`--bare`** — 脚本场景启动飞快，跳过所有自动发现（hooks / skills / plugins / MCP / auto memory / CLAUDE.md）。
2. **`-w "#123"`** — 直接从 PR 号或 PR URL 起 worktree。
3. **`--max-budget-usd` + `--max-turns`** — 无人值守任务的安全阀。
4. **`--exclude-dynamic-system-prompt-sections`** — 多用户 / 多机器跑同任务时大幅提升 prompt cache 命中。
5. **`claude --teleport`** — 在本地终端续 web session。
6. **`claude project purge <path> --dry-run`** — 清单个项目的所有本地状态（transcripts、task list、debug log、edit history、prompt 历史、`~/.claude.json` 项），先 `--dry-run` 看清单。
7. **`claude auto-mode defaults > rules.json`** — 拿到内置 auto-mode 分类器规则，便于自定义覆盖。

## Print 模式专用 flag

只在 `-p` / `--print` 模式生效，交互模式下传了会报错或被忽略：

`--fallback-model`, `--init`, `--maintenance`, `--include-hook-events`, `--include-partial-messages`, `--input-format`, `--json-schema`, `--max-budget-usd`, `--max-turns`, `--no-session-persistence`, `--output-format`, `--permission-prompt-tool`, `--replay-user-messages`, `--exclude-dynamic-system-prompt-sections`

## 约定与坑

- `claude --help` **不会列出所有 flag** —— 某个 flag 不在 `--help` 里 ≠ 不存在，以本参考为准。
- `--system-prompt` 和 `--system-prompt-file` 互斥；任意一个 `--append-*` flag 都可以跟任意一个 replace flag 组合。
- 子命令拼错时 CLI 会建议最接近的（`claude udpate` → 提示 `claude update`）。
- 写脚本时用 `claude auth status` 退出码判断（0 = 已登录），别 grep 输出。
- `claude install` 接受 `stable` / `latest` / 具体版本号（如 `2.1.118`）。

## 来源

- Upstream: <https://code.claude.com/docs/en/cli-reference.md>
- upstream 更新后，重新抓 `references/*.md` 两个文件即可，`SKILL.md` 本身改动很少。
