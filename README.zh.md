# skills

> English: [README.md](README.md)

[Agent Skills](https://agentskills.io/specification) 集合，可用于 Claude Code、Codex、Cursor、Gemini CLI 等支持 Agent Skills 格式的工具。

## 已收录

| Skill | 用途 |
|---|---|
| [ios-icp-filing](./ios-icp-filing/SKILL.zh.md) | 从已签名 IPA 反查 Bundle ID / SHA-1 / 公钥 modulus，按腾讯云 / 阿里云 / 华为云 ICP 备案表单格式输出 |
| [finish-worktree](./finish-worktree/SKILL.zh.md) | 把当前 worktree 的改动合并回主仓库并清理 worktree + 分支；自动识别嵌套子仓库，按子先父后顺序处理；默认绝不 push |
| [discard-worktree](./discard-worktree/SKILL.zh.md) | 销毁性丢弃当前 worktree 的所有改动（含已 commit 未合并），删除 worktree 和分支；同样支持嵌套子仓库的反序清理 |
| [git-worktree-setup](./git-worktree-setup/SKILL.zh.md) | 为目标仓库生成定制 `setup-worktree.sh` + 配套 hook，让新 worktree 一开就能跑（`node_modules` 软链 / `.env` 拷贝 / dev port 哈希分配 / DB state 共享或隔离） |
| [claude-code-cli-reference](./claude-code-cli-reference/SKILL.zh.md) | Claude Code CLI 官方文档本地镜像 —— 子命令、flag、常用组合、print 模式专用 flag、坑点速查；离线查阅且不用拉远端文档 |
| [claude-code-docs](./claude-code-docs/SKILL.zh.md) | Claude Code **全量** 官方文档本地镜像（140+ 页，来自 code.claude.com/docs），按 `llms.txt` 索引一页一个 reference 文件。覆盖 CLI、IDE 集成、plugins、skills、hooks、MCP、Agent SDK、企业部署、配置、weekly changelog。内置 `references/_meta/` 抓取方法 + 重跑脚本，skill 自带刷新能力 |
| [volcengine-rtc-docs](./volcengine-rtc-docs/SKILL.zh.md) | 火山引擎实时音视频（VolcEngine RTC）官方文档本地副本，按目录切成 248 个 PDF。覆盖核心 RTC SDK、AI 语音 agent、硬件对话智能体、RTS 实时信令、互动白板、旧版 IM；PDF 通过 git LFS 管理（~128MB） |
| [submit-show-hn](./submit-show-hn/SKILL.zh.md) | 准备或 troubleshoot 一个 Hacker News Show HN 帖子。覆盖新账号的静默限流（`/showlim` 重定向）、karma 门槛、1–2 周账号 warming 计划、帖子模板、HN 冷却期可同步推的备用渠道（Reddit / Twitter / awesome-* 等）。内置 pg 的 Show HN 官方规则、HN 社区通用规则、throttle 页面的本地副本 |

## 安装


```bash
npx skills add imsai-sh/skills

npx skills add imsai-sh/skills --skill git-worktree-setup
```

## License

[MIT](./LICENSE) — 用、改、商用、二次分发都行，保留原作者声明即可。
