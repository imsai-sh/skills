---
name: discard-worktree
description: Use when the user wants to discard ALL changes in the current worktree (committed or not), delete the worktree, and delete its branch — without merging back. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and discards them too with strict reverse-order cleanup. Triggers in Chinese: "丢弃这个 worktree", "废掉这个 worktree", "扔了这个 branch", "不要这个分支了". In English: "discard this worktree", "throw away this branch", "abandon the worktree", "trash this work".
---

# Discard Worktree

丢弃这个 worktree 的任何更改（含已 commit 但未合并的），删除 worktree 和分支，**不**合并回主仓库。

## 确认策略

是否需要事先确认，取决于是否真的会丢东西：

- **没东西可丢** —— 没有 uncommitted 改动 **且** 相对 base 也没有领先 commit。这种情况就只是清理 worktree 元数据 + 同名空分支，**直接执行，不必询问**。
- **有东西要丢** —— 存在任何 uncommitted 改动 **或** 任何领先 commit。先列出将被丢的内容（uncommitted 文件数、unmerged commit 数 / 列表），等用户明确说 "确认丢弃" / "yes, discard" 后再执行。**一旦执行不可逆。**

嵌套模式下两侧必须**一起评估、一起决策**。原因：清理是先子后父的硬顺序，子拆掉就没法撤回——如果"先静默清干净的子，再去问父"，结果用户在父那边犹豫，子已经回不来了。规则：

- **两侧都干净** → 全部静默清理。
- **任一侧有内容** → 把两侧状态都列出来，等一次明确的 "确认丢弃" 后再启动清理。

## 1. 检测是否嵌套 worktree

扫当前 worktree 根下的子目录，凡同时满足：

- 被当前 worktree 的 `.gitignore` 排除
- 自身含 `.git`（目录或文件）

→ 是**嵌套子仓库**，走 §2b。
否则走 §2a。

## 2a. 单仓库模式

```
1. 检查当前 worktree 状态：
   - `git status --porcelain`（uncommitted 改动）
   - `git log <main>..HEAD`（领先 commit）
   两个都空 → 跳过确认，直接静默清理。任一非空 → 列给用户，等明确 "确认丢弃"。
2. 切到主仓库
3. git -C <主仓库> worktree remove --force <worktree path>
4. git -C <主仓库> branch -D <branch>
5. git -C <主仓库> worktree prune
```

## 2b. 嵌套模式 —— **清理反序：先子后父**

理由：子 worktree 嵌在父里，父 `worktree remove` 时会撞到子级 `.git` 报错。必须先拆子。

```
1. 一开始就把两侧状态都摸清楚（清理是先子后父，子拆完没法回头）：
   - 子级： git -C <父wt>/<子> status --porcelain; git -C <父wt>/<子> log <子main>..HEAD
   - 父级：git -C <父wt> status --porcelain;       git -C <父wt> log <父main>..HEAD
   两侧都干净 → 跳过确认，全部静默清理。任一侧非空 → 列出两侧状态，等一次明确 "确认丢弃" 再启动。

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
- **不可逆（仅在有内容时才有意义）**：执行后 uncommitted 改动 / unmerged commit 全部丢失；用户在有内容那侧犹豫 → 停下问清楚再继续

## 跟 finish-worktree 的区别

| | finish-worktree | discard-worktree |
|---|---|---|
| 目标 | 合并回 main 后清理 | 直接丢弃 + 清理 |
| commit | 未 staged 改动也 commit | 改动直接丢 |
| merge | 子先父后 merge 回 main | 不 merge |
| push | 父级可 push；子级问用户 | 不 push 任何东西 |
| 清理 | 反序（先子后父） | 反序（先子后父） |
| 确认 | 总是要确认 | 只在会丢东西时确认 |
