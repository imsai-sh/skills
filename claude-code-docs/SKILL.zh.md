---
name: claude-code-docs
description: |
  Local mirror of the full Claude Code documentation set (code.claude.com/docs), one
  reference file per page, mirroring the upstream `llms.txt` index. Load on demand
  instead of fetching live docs. Covers CLI, IDE integrations (VS Code, JetBrains,
  Desktop, Chrome, Slack, Web), CI/CD (GitHub Actions, GitLab), building blocks
  (skills, subagents, plugins, hooks, commands, output styles, headless, sandboxes,
  channels, agent orchestration, advanced workflows like ultraplan/ultrareview/goal/
  fast-mode), MCP, the Agent SDK (Python + TypeScript), enterprise deployment
  (Bedrock/Vertex/Foundry/AWS), configuration (settings, permissions, memory,
  checkpointing), reference material (cli-reference, slash-commands, tools-reference,
  errors, glossary), and the weekly changelog.
  Triggers in Chinese: "claude code 的", "claude code 文档", "claude code skills",
  "claude code plugins", "claude code hooks", "claude code mcp", "agent sdk",
  "subagents", "claude code ide", "claude code 配置", "claude code 怎么用".
  In English: "claude code docs", "claude code feature", "how does claude code",
  "claude code skill", "claude code plugin", "claude code hook", "agent sdk",
  "subagent", "claude code ide integration", "claude code config".
  Methodology and re-scrape scripts live in `references/_meta/`.
---

# Claude Code 全量文档（本地镜像）

[code.claude.com/docs](https://code.claude.com/docs/en/) 整站本地镜像，**一页一个文件**，结构对齐官方 `llms.txt` 索引。当 agent（或你自己）想查 Claude Code 的任何特性、配置、SDK 用法时翻这里，不用现拉文档。

## 什么时候用

- 用户问到 Claude Code 的具体特性、配置、SDK 用法（CLI、Desktop、VS Code、JetBrains、Chrome、Slack、Web）
- 要写 / 调试 hooks、subagents、plugins、skills、output styles、headless mode、MCP server
- 要在企业环境部署（Bedrock、Vertex、Foundry、AWS、network、llm-gateway）
- 排查 `claude` 跑不通、配置不生效 → `references/troubleshooting.md`、`references/debug-your-config.md`、`references/errors.md`
- 想看 Agent SDK（Python / TypeScript）的 API、自定义 tools、streaming、structured outputs、permissions
- 查 Claude Code 最近几周更新了什么 → `references/whats-new/`
- 想刷新这个 skill 自己 → `references/_meta/scraping-method.md`

## 资料在哪里

| 你想查的东西 | 看哪个文件 |
|---|---|
| 主索引（143 页清单 + 描述） | 本文件（SKILL.md） |
| 单个文档页 | `references/<slug>.md` 或 `references/agent-sdk/<page>.md` |
| 周更新 changelog | `references/whats-new/2026-w13.md` ~ `2026-w20.md` |
| **怎么造的 / 怎么刷新这个 skill** | `references/_meta/scraping-method.md` |
| 重抓脚本（curl Mintlify `.md` endpoint） | `references/_meta/scripts/refetch-md.py` |
| SKILL.md 索引生成器 | `references/_meta/scripts/generate-skill-md.py` |

## 命名规则

文件路径 = URL 路径 - `/docs/en/`，例如：
- `https://code.claude.com/docs/en/skills` → `references/skills.md`
- `https://code.claude.com/docs/en/agent-sdk/custom-tools` → `references/agent-sdk/custom-tools.md`
- `https://code.claude.com/docs/en/whats-new/2026-w20` → `references/whats-new/2026-w20.md`

按需 load 单文件，不要 dump 整个 skill。

## 抓取方法（一句话）

不用 scraper。Mintlify 在每个 doc URL 的 `.md` 后缀返回**原始 markdown**（不走 React），llms.txt 列出的就是这些 `.md` URL。`refetch-md.py` 就是 curl 一遍这 140 个 URL 落盘，~45 秒搞定。完整流程 + 走过的弯路（之前用 HTML scraper 漏掉了表格 → 重做）看 `_meta/scraping-method.md`。

## 已知坑（节选自 `_meta/scraping-method.md`）

- 上游 `llms.txt` 偶尔有改名 / 删除（如 `microsoft-foundry` → `azure-ai-foundry`），刷新时 diff 一下 slug 列表能看到
- 3 个文件 >100 KB（`hooks.md`、`settings.md`、`commands.md`）是上游单页就那么长，没拆 —— 按需 load 不浪费
- Mintlify `.md` endpoint 这招只适用于 Mintlify 托管的 docs 站；其他站点要 fallback 到真 scraper

## 来源 & 工具

- 文档源：Anthropic，[code.claude.com/docs](https://code.claude.com/docs/en/)（snapshot: 2026-05-25）
- 抓取方法：Mintlify `.md` endpoint + `curl`（无第三方依赖）
- 索引基准：[`llms.txt` 标准](https://llmstxt.org/)
