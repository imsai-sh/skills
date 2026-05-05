---
name: discard-worktree
description: Use when the user wants to discard ALL changes in the current worktree (committed or not), delete the worktree, and delete its branch — without merging back. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and discards them too with strict reverse-order cleanup. Triggers in Chinese: "丢弃这个 worktree", "废掉这个 worktree", "扔了这个 branch", "不要这个分支了". In English: "discard this worktree", "throw away this branch", "abandon the worktree", "trash this work".
---

# Discard Worktree

丢弃这个 worktree 的任何更改（含已 commit 但未合并的），删除 worktree 和分支，**不**合并回主仓库。

## ⚠️ 销毁性操作

执行前**必须**跟用户确认：列出将被丢弃的内容（uncommitted 改动文件数、unmerged commit 数 / 列表），明确得到 "确认丢弃" / "yes, discard" 等明确同意后才执行。一旦执行**不可逆**。

## 1. 检测是否嵌套 worktree

扫当前 worktree 根下的子目录，凡同时满足：

- 被当前 worktree 的 `.gitignore` 排除
- 自身含 `.git`（目录或文件）

→ 是**嵌套子仓库**，走 §2b。
否则走 §2a。

## 2a. 单仓库模式

```
1. 当前 worktree 改动展示给用户确认（git status + git log <main>..HEAD）
2. 切到主仓库
3. git -C <主仓库> worktree remove --force <worktree path>
4. git -C <主仓库> branch -D <branch>
5. git -C <主仓库> worktree prune
```

## 2b. 嵌套模式 —— **清理反序：先子后父**

理由：子 worktree 嵌在父里，父 `worktree remove` 时会撞到子级 `.git` 报错。必须先拆子。

```
1. 列两侧改动给用户确认：
   - 子级 worktree： git -C <父wt>/<子> status; git -C <父wt>/<子> log <子main>..HEAD
   - 父级 worktree：git -C <父wt> status; git -C <父wt> log <父main>..HEAD
   等用户明确同意

2. 子级清理（先做）：
   git -C <子级主仓库> worktree remove --force <父wt>/<子>
   git -C <子级主仓库> branch -D <branch>
   git -C <子级主仓库> worktree prune

3. 父级清理：
   git -C <父级主仓库> worktree remove --force <父wt>
   git -C <父级主仓库> branch -D <branch>
   git -C <父级主仓库> worktree prune
```

## 通用约束

- **绝不 push 任何东西**（discard 的语义是丢弃，不涉及远端；尤其 OSS 公共仓库 push 默认禁止 —— 见项目级 memory 规则）
- `worktree remove --force` 必须带 `--force`（worktree 内含 symlinks + 未 commit 改动会被判 unclean）
- `branch -D`（大写 D）强删 branch，绕过 unmerged 检查 —— 这正是 discard 想要的
- 如果某侧 branch 不存在 / worktree 已被手动删 → 跳过对应步骤，prune 兜底清理 metadata
- **不可逆**：执行后用户的改动全部丢失；如果用户犹豫，停下问清楚再继续

## 跟 finish-worktree 的区别

| | finish-worktree | discard-worktree |
|---|---|---|
| 目标 | 合并回 main 后清理 | 直接丢弃 + 清理 |
| commit | 未 staged 改动也 commit | 改动直接丢 |
| merge | 子先父后 merge 回 main | 不 merge |
| push | 父级可 push；子级问用户 | 不 push 任何东西 |
| 清理 | 反序（先子后父） | 反序（先子后父） |
