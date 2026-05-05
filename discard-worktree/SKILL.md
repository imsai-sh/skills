---
name: discard-worktree
description: Use when the user wants to discard ALL changes in the current worktree (committed or not), delete the worktree, and delete its branch — without merging back. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and discards them too with strict reverse-order cleanup. Triggers in Chinese: "丢弃这个 worktree", "废掉这个 worktree", "扔了这个 branch", "不要这个分支了". In English: "discard this worktree", "throw away this branch", "abandon the worktree", "trash this work".
---

# Discard Worktree

Discard any changes (committed-but-unmerged included) in this worktree, delete the worktree, and delete its branch. **Do not** merge back to main.

## ⚠️ Destructive operation

Before executing, **must** confirm with the user: list what's about to be discarded (number of uncommitted-changed files, count + list of unmerged commits). Only execute after explicit "confirm discard" / "yes, discard". **Once executed, irreversible.**

## 1. Detect whether this is a nested worktree

Scan subdirs under the current worktree root. Any subdir that **both**:

- is excluded by the current worktree's `.gitignore`
- contains its own `.git` (dir or file)

→ it's a **nested child repo**, go to §2b.
Otherwise go to §2a.

## 2a. Single-repo mode

```
1. Show changes for user confirmation (git status + git log <main>..HEAD)
2. cd to main repo
3. git -C <main-repo> worktree remove --force <worktree path>
4. git -C <main-repo> branch -D <branch>
5. git -C <main-repo> worktree prune
```

## 2b. Nested mode — **cleanup reverse order: child first, parent next**

Why: the child worktree is nested inside the parent. The parent's `worktree remove` will trip on the child's `.git`. The child must be dismantled first.

```
1. List both sides' changes for user confirmation:
   - child worktree: git -C <parent-wt>/<child> status; git -C <parent-wt>/<child> log <child-main>..HEAD
   - parent worktree: git -C <parent-wt> status; git -C <parent-wt> log <parent-main>..HEAD
   wait for explicit "yes"

2. Child cleanup (do first):
   git -C <child-main-repo> worktree remove --force <parent-wt>/<child>
   git -C <child-main-repo> branch -D <branch>
   git -C <child-main-repo> worktree prune

3. Parent cleanup:
   git -C <parent-main-repo> worktree remove --force <parent-wt>
   git -C <parent-main-repo> branch -D <branch>
   git -C <parent-main-repo> worktree prune
```

## General constraints

- **Push nothing.** Discard semantics: throw away, don't touch remotes. OSS / public-repo push is forbidden anyway (see project-level memory).
- `worktree remove --force` must include `--force`: worktrees contain symlinks + uncommitted changes that git judges unclean.
- `branch -D` (capital D) force-deletes the branch, bypassing the unmerged-check — exactly what discard wants.
- If one side's branch doesn't exist / the worktree was manually deleted → skip the corresponding step; `worktree prune` mops up the metadata.
- **Irreversible**: after execution all the user's changes are lost. If the user hesitates, stop and ask before continuing.

## How this differs from finish-worktree

| | finish-worktree | discard-worktree |
|---|---|---|
| Goal | Merge into main, then clean up | Discard + clean up |
| Commit | Commits unstaged changes too | Throws the changes away |
| Merge | Child first, parent next, into main | No merge |
| Push | Parent may push if user opts in; child asks user | Push nothing |
| Cleanup | Reverse order (child first, parent next) | Reverse order (child first, parent next) |
