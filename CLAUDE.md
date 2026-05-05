# CLAUDE.md

此仓库（`imsai-sh/skills`）是公开的开源 agent skill 集合，所有内容会被 publish 出去。

## 强制规则：开源项目隐私检查

**这是公开仓库。任何 commit / push 都可能在 git 历史里永久留下隐私痕迹，rebase 也擦不掉 fork 与 mirror。**

- **绝不擅自 commit、绝不擅自 push** —— 必须用户明确说才执行；即便用户一次说了 push，下次还是要再确认（授权不跨次有效）
- **每次 commit / push 之前强制扫一遍隐私**，至少覆盖：
  - **密钥 / token / 证书**：`sk-…`、`ghp_…`、`AIza…`、`xoxb-…`、AWS keys、`-----BEGIN …PRIVATE KEY-----`
  - **个人邮箱 / 真实姓名**（不是开源 handle）
  - **本机绝对路径**：`/Users/<name>/…`、`/home/<name>/…`、`C:\Users\…`
  - **内网 host / IP**：`*.local`、`*.internal`、`*.corp`、`10.x` / `192.168.x` / `172.16-31.x`
  - **私有仓库引用**：用户自己的非公开 repo 名（即使是 `imsai-sh/...` 也要核实是不是已 public）
  - **遗留 TODO/FIXME/HACK**：可能暴露未公开的内部计划或别处的 bug
- **扫到命中 → 停下找用户确认**，不要自己脑补"应该可以"
- **commit message 不要写公司名 / 内部项目代号 / 私有 repo 引用**

## 仓库约定

- 每个 skill 一个顶层目录，至少包含 `SKILL.md`（YAML frontmatter + 正文）；视情况再加 `SKILL.zh.md` / `scripts/` / `references/` / `assets/`
- **不要**在每个 skill 子目录里再放 LICENSE，根目录 `LICENSE` 已覆盖（参考现有 `ios-icp-filing/` 结构）
- 新增 skill 时同步更新根 `README.md` 的"已收录"表格
- 安装入口是 [`npx skills add imsai-sh/skills`](https://github.com/vercel-labs/skills)，不要破坏其期望的目录结构

## 搬运 / 合并外部 skill 时的流程

从其它仓库（包括用户自己的 `~/.claude/skills/`）搬运 skill 进来时：

1. 只复制核心内容：`SKILL.md` / `SKILL.zh.md` 及其引用的子目录（`scripts/` / `references/` / `assets/`）
2. **跳过**外部仓的 `README.md`、`LICENSE`、`.git`、`.claude`、`.idea`、`.DS_Store`
3. 跑上面的隐私扫描，重点检查 frontmatter 里的 `homepage` / `repository` 字段是否还指向独立仓 —— 决定保留还是改写
4. 更新根 `README.md` 表格
5. **不**在搬运动作里 commit / push，等用户明确指示
