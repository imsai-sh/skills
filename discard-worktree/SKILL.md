---
name: discard-worktree
description: Use when the user wants to discard ALL changes in the current worktree (committed or not), delete the worktree, and delete its branch — without merging back. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and discards them too with strict reverse-order cleanup. Triggers in Chinese: "丢弃这个 worktree", "废掉这个 worktree", "扔了这个 branch", "不要这个分支了". In English: "discard this worktree", "throw away this branch", "abandon the worktree", "trash this work".
---

# Discard Worktree

Discard any changes (committed-but-unmerged included) in this worktree, delete the worktree, and delete its branch. **Do not** merge back to main.

## Confirmation policy

Whether to ask first depends on whether anything would actually be lost:

- **Nothing to lose** — no uncommitted changes AND no commits ahead of base. The discard is pure metadata + empty-branch cleanup. **Proceed without asking.**
- **Something to lose** — any uncommitted change OR any commit ahead of base. List what's about to go (uncommitted file count, unmerged commit count + list) and require explicit "confirm discard" / "yes, discard" before running. **Irreversible once executed.**

In nested mode, assess both sides **up-front** before touching anything. Cleanup is reverse-order (child first, parent next) and the child can't be un-removed if the user balks at the parent — so "silently clean the empty child first, then ask about the parent" is unsafe. Rule:

- **Both sides empty** → both clean silently.
- **Either side has content** → list both sides' state and require a single explicit "confirm discard" before any cleanup starts.

## 1. Detect whether this is a nested worktree

Scan subdirs under the current worktree root. Any subdir that **both**:

- is excluded by the current worktree's `.gitignore`
- contains its own `.git` (dir or file)

→ it's a **nested child repo**, go to §2b.
Otherwise go to §2a.

## 2a. Single-repo mode

```
1. Check state:
   - `git status --porcelain` (uncommitted changes)
   - `git log <main>..HEAD` (commits ahead)
   Both empty → silent cleanup, no prompt. Either non-empty → list to user and wait for explicit "yes".
2. cd to main repo
3. git -C <main-repo> worktree remove --force <worktree path>
4. git -C <main-repo> branch -D <branch>
5. git -C <main-repo> worktree prune
```

## 2b. Nested mode — **cleanup reverse order: child first, parent next**

Why: the child worktree is nested inside the parent. The parent's `worktree remove` will trip on the child's `.git`. The child must be dismantled first.

```
1. Assess both sides up-front (cleanup is reverse-order; child can't be rolled back if parent stalls):
   - child:  git -C <parent-wt>/<child> status --porcelain; git -C <parent-wt>/<child> log <child-main>..HEAD
   - parent: git -C <parent-wt> status --porcelain;          git -C <parent-wt> log <parent-main>..HEAD
   Both sides empty → skip confirmation, clean silently. Either side non-empty → list both sides and wait for one explicit "yes" before starting.

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
- **Irreversible (only matters when there's content)**: any uncommitted changes / unmerged commits are gone after execution. If the user hesitates on a side that has content, stop and ask before continuing.

## How this differs from finish-worktree

| | finish-worktree | discard-worktree |
|---|---|---|
| Goal | Merge into main, then clean up | Discard + clean up |
| Commit | Commits unstaged changes too | Throws the changes away |
| Merge | Child first, parent next, into main | No merge |
| Push | Parent may push if user opts in; child asks user | Push nothing |
| Cleanup | Reverse order (child first, parent next) | Reverse order (child first, parent next) |
| Confirmation | Always confirms | Only when something would be lost |
