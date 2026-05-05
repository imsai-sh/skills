---
name: finish-worktree
description: Use when the user wants to merge their current worktree's work back into the main repo and clean up the worktree + branch. Auto-detects nested child repositories (subdirs that are git-ignored AND contain a .git of their own — e.g. OSS sub-repo nested inside a private workspace) and handles them with strict ordering (child first → parent next → cleanup reversed). Triggers in Chinese: "合并 worktree", "收尾 worktree", "清理 worktree", "ship 这个 worktree", "结束这个 branch". In English: "merge feature back", "wrap up the worktree", "ready to ship", "finish this branch", "land this branch", "merge and cleanup".
---

# Finish Worktree

Merge the current worktree's changes (including uncommitted code) back into the main repo, and clean up the temporary worktree and branch.

## 0. Push policy (highest priority — read first)

**Default: never push** — regardless of which repo. This skill does "local commit + merge into main + cleanup worktree". It does **not** push.

Only push when the user **explicitly** says so during this invocation (e.g. "finish, then push to remote", "push after merge"). Otherwise:

- **Don't ask "should I push?"** — once you make pushing the OSS default question, you've already violated "don't push without being told"
- **Don't end with "I can also push"** — same trap, just phrased softer
- After completion, just report commit / merge / cleanup results. Leave main on local; let the user decide when to push.

OSS / public-repo push is a **never-do-it-on-your-own** write operation. This skill makes no exception.

## 1. Sync settings.local.json first

`.claude/settings.local.json` is in gitignore so it can't ride the merge. Merge it into `.claude/settings.json`, then sync to the main worktree's `.claude/settings.json`.
(In nested topology, do this on **both** parent and child worktree sides.)

## 2. Detect whether this is a nested worktree

Scan subdirs under the current worktree root. Any subdir that **both**:

- is excluded by the current worktree's `.gitignore`
- contains its own `.git` (dir or file)

→ it's a **nested child repo**, go to §3b.
Otherwise go to §3a.

**Special topology**: parent workspace repo + child repo "folded" by an init script into the same worktree path (the parent worktree's `.git` file actually points to the child repo's worktree gitdir, and the parent has no real files at that path — everything visible is child-repo content). In this case `git rev-parse --git-dir` reflects the true ownership; treat it as child-repo and follow §3b. The parent side only does worktree-metadata cleanup (no commit / merge).

## 3a. Single-repo mode

```
1. Commit unstaged changes in the current worktree (if any) — confirm commit message with user first
2. cd to main repo → git checkout main → git merge <feature-branch>
3. (no push — see §0)
4. Cleanup: worktree remove --force + branch -D + worktree prune
```

## 3b. Nested mode — **child first → parent next → cleanup reversed**

For each nested child repo:

```
1. cd <parent-worktree>/<child>  → commit unstaged changes (if any) — confirm message first
2. cd <child-main-repo>          → git checkout main && git merge <feature-branch>
3. (no push — see §0)
```

Then parent:

```
4. cd <parent-worktree>          → commit unstaged changes (if any) — confirm message first
5. cd <parent-main-repo>         → git checkout main && git merge <feature-branch>
6. (no push — see §0)
```

Cleanup (**strict reverse order**: child first, parent next — otherwise the parent's `worktree remove` will trip on the nested child's `.git`):

```
7. git -C <child-main> worktree remove --force <parent-worktree>/<child>
   git -C <child-main> branch -D <feature-branch>
8. git -C <parent-main> worktree remove --force <parent-worktree>
   git -C <parent-main> branch -D <feature-branch>
9. worktree prune on both sides
```

## General constraints

- **Confirm commit message with the user before every commit.** Don't ask about pushing — the answer is always no (see §0).
- Merge conflict → pause the flow; let the user resolve manually; resume after.
- `worktree remove` always uses `--force`: worktrees often hold symlinks that git judges unclean.
- Zero changes on one side / branch doesn't exist → skip the corresponding commit + merge + branch -D.
- User explicitly says "merge then push to main remote": OK to push, but `git pull --ff-only origin main` first to avoid fast-forward failure.
