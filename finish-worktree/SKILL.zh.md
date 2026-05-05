---
name: finish-worktree
description: Use when the user wants to merge their current worktree's work back into the main repo and clean up the worktree + branch. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and handles them with strict ordering (child first → parent next → cleanup reversed). Triggers in Chinese: "合并 worktree", "收尾 worktree", "清理 worktree", "ship 这个 worktree", "结束这个 branch". In English: "merge feature back", "wrap up the worktree", "ready to ship", "finish this branch", "land this branch", "merge and cleanup".
---

# Finish Worktree

把当前 worktree 的改动（含尚未提交的代码）合并回主仓库，并清理这个临时 worktree 和分支。

## 0. Push 政策（最高优先级，先读）

**默认绝不 push**——不论哪个仓库。本 skill 完成的是"本地 commit + merge 到主仓库 main + 清理 worktree"，**不**包含 push。

只有当用户在调用本 skill 时**明确**说要 push（例如"finish 完顺便 push 到远端"、"merge 后推上去"），才执行 push。否则：

- **不要问"要不要 push？"** —— 一旦默认要问 OSS push，就违背了"不擅自 push"的本意
- **不要在结尾提示"我可以再 push"** —— 也是变相诱导
- 完成后直接报告 commit / merge / cleanup 结果，留 main 在本地等用户自己决定何时 push

OSS / 公共仓库 push 是**永远不主动做**的写操作，本 skill 不破例。

## 1. 先同步 settings.local.json

`.claude/settings.local.json` 在 gitignore 里跟随不了合并 —— 把它合并到 `.claude/settings.json`，再同步到主工作树的 `.claude/settings.json`。
（嵌套场景下，父子两侧 worktree 都要做这一步。）

## 2. 检测是否嵌套 worktree

扫当前 worktree 根下的子目录，凡同时满足：

- 被当前 worktree 的 `.gitignore` 排除
- 自身含 `.git`（目录或文件）

→ 是**嵌套子仓库**，走 §3b。
否则走 §3a。

**特殊拓扑**：父 workspace 仓库 + 子仓库被 init 脚本"折叠"到同一 worktree 路径下（父 worktree 的 `.git` 文件实际指向子仓库的 worktree gitdir，而父级在该路径其实没有真实文件，全是子仓库内容）。这种情况下 `git rev-parse --git-dir` 会反映出真实归属，按子仓库走 §3b 流程，父侧仅做 worktree 元数据清理（无 commit / merge）。

## 3a. 单仓库模式

```
1. 当前 worktree commit 未 staged 改动（如有）—— commit message 先给用户确认
2. 切到主仓库 → git checkout main → git merge <feature-branch>
3. （不 push —— 见 §0）
4. 清理：worktree remove --force + branch -D + worktree prune
```

## 3b. 嵌套模式 —— **子级先 → 父级后 → 清理反序**

对每个嵌套子仓库：

```
1. cd <父worktree>/<子>  → commit 未 staged 改动（如有）—— commit message 先给用户确认
2. cd <子级主仓库>        → git checkout main && git merge <feature-branch>
3. （不 push —— 见 §0）
```

然后父级：

```
4. cd <父worktree>        → commit 未 staged 改动（如有）—— commit message 先给用户确认
5. cd <父级主仓库>         → git checkout main && git merge <feature-branch>
6. （不 push —— 见 §0）
```

清理（**严格反序**：先子后父，否则父 worktree remove 会撞到嵌套子级 `.git`）：

```
7. git -C <子级主> worktree remove --force <父worktree>/<子>
   git -C <子级主> branch -D <feature-branch>
8. git -C <父级主> worktree remove --force <父worktree>
   git -C <父级主> branch -D <feature-branch>
9. 两侧各 worktree prune
```

## 通用约束

- **commit message 写完先给用户确认**（每次 commit 都要问 message）。push 默认就不做（见 §0），所以不需要"问 push" —— 因为答案永远是不做。
- merge conflict → 暂停流程，让用户手动解决，解决完再 resume。
- `worktree remove` 默认带 `--force`：worktree 内常含 symlinks，会被 git 判 unclean。
- 某侧零改动 / branch 不存在 → 跳过对应 commit + merge + branch -D 步骤。
- 用户明确说"merge 完 push 到 main 远端"：可以执行 push，但 push 前先 `git pull --ff-only origin main` 防 fast-forward 失败。
