---
name: git-commit
description: MUST use this skill when committing changes, writing commit messages, staging files, saying 'ship it', or using conventional commits. Auto-analyzes diff, matches repo style, generates messages, handles multi-context splitting, and enforces atomic commits.
---

# Git Commit Skill

Handles the commit lifecycle: inspect → analyze → stage → message → commit.

---

## Workflow

1. Run `git status` to see which files changed and which branch is active.
2. Run `git diff` to review the full content of changes before staging anything.
3. Check recent commit history with `git log --oneline -10` to match repo style and patterns.
4. Group changes by context — purpose, scope, and type. Determine if this is one commit or many.
5. If multiple contexts exist, present a split plan and wait for confirmation before executing.
6. Stage files per context — use `git add -p` for mixed changes within a single file.
7. Run `git diff --cached` to confirm what's staged looks correct.
8. Commit with the generated message. Repeat steps 6–8 for each remaining context.

After all commits, show a summary:
```
✅ Committed on branch: feat/login
📝 feat(auth): add JWT refresh token support
📝 chore: update env vars and vite config
📦 2 commits total
```

---

## Rules

### General
- **Must** stop and tell the user if there is nothing to commit — don't proceed.
- **Must not** proceed if the repo is in a detached HEAD state — warn and suggest creating a branch first.
- **Must not** commit when there are unresolved merge conflicts — report which files are affected.
- **Must not** use `--allow-empty` unless the user explicitly asks for it.
- **Must not** skip pre-commit hooks — if they fail, report the error and stop.

### Staging
- **Must** review `git diff` output before staging to understand what's actually changing.
- **Must not** stage `.env`, secrets, or private key files — warn the user immediately.
- **Must** use `git add -p` when a single file contains changes that belong to different contexts — do not skip partial staging because it feels tedious.
- **Should not** stage large binary files without warning the user and suggesting `.gitignore` or Git LFS.

### Atomic Commits
- **Must** treat one commit as one logical change — not one file, not one task.
- **Must** split by default when multiple contexts are detected — do not ask whether to split, just propose the plan.
- **Must** present the split plan before executing — list each commit with its type, scope, description, and relevant files, then wait for confirmation.
- **Must not** batch unrelated changes into one commit for convenience.
- **Must not** force split if the user explicitly says to keep it as one — respect their call.

  Split when **any** of these are true:
  - Different types in the same diff (e.g., a `fix` and a `refactor`)
  - Different scopes (e.g., changes to `auth` and to `dashboard`)
  - Different purposes (e.g., adding a feature while also fixing a typo)
  - Different files serving different concerns

  If a commit message needs the word **"and"** — split it into two commits.

  **Example split plan + execution:**
  ```
  Proposed split:
  1. fix(auth): handle token expiry edge case  →  src/api/auth.ts
  2. feat(dashboard): add analytics widget     →  src/features/dashboard/
  3. chore: update env vars and vite config    →  .env.example, vite.config.ts

  Executing...

  git add src/api/auth.ts
  git commit -m "fix(auth): handle token expiry edge case"

  git add src/features/dashboard/
  git commit -m "feat(dashboard): add analytics widget"

  git add .env.example vite.config.ts
  git commit -m "chore: update env vars and vite config"
  ```

### Commit Message
- **Must** follow the [Conventional Commits](https://www.conventionalcommits.org/) format: `<type>(<scope>): <subject>`
- **Must** pick the correct type:

  | Type | When to use |
  |------|-------------|
  | `feat` | New feature |
  | `fix` | Bug fix |
  | `refactor` | Code change, no feature/fix |
  | `chore` | Tooling, deps, configs |
  | `docs` | Documentation only |
  | `style` | Formatting, whitespace |
  | `test` | Adding/updating tests |
  | `perf` | Performance improvement |
  | `ci` | CI/CD pipeline changes |
  | `build` | Build system changes |
  | `revert` | Reverting a previous commit |

- **Must** write the subject in imperative mood, lowercase, no period — "add" not "added", not "Add."
- **Must** keep the subject under 50 characters. Wrap body lines at 72 characters.
- **Must** add a `BREAKING CHANGE:` footer if the change breaks an existing API or contract.
- **Must** match the repo's existing commit style — check history first and adapt to gitmoji or commitlint config if present.
- **Must not** write vague messages like `fix stuff`, `update`, or `wip`.
- **Should** omit scope if the change is broad and doesn't belong to one area.
- **Should** reference issue or ticket numbers in the footer when applicable — `Refs: #123` or `Closes: #456`.
- **Should** add a body only when the subject can't capture the *why* or *impact* — explain what was wrong, then what improved.
- **Should not** add a body just to fill space — if the subject is self-explanatory, leave it.

  ```
  feat(auth): add JWT refresh token support

  Previous tokens expired mid-session with no recovery path.
  Now silently refreshes 60s before expiry to keep users logged in.

  Closes: #87
  BREAKING CHANGE: /auth/login now returns refresh_token field
  ```

### WIP / Squash Pattern
- **Should** use WIP commits freely on feature branches — messy history is fine during active work.
- **Should** use `fixup!` commits to amend previous ones, then `git rebase -i --autosquash` before merging to main.
- **Must not** squash on shared or main branches.

---

## Quick Reference

```bash
git diff                          # review full changes before staging
git add -p                        # stage hunks interactively
git diff --cached                 # confirm what's staged
git log --oneline -10             # check repo commit style
git reset --soft HEAD~1           # undo last commit, keep changes staged
git commit --amend -m "message"   # fix last commit message
git restore --staged <file>       # unstage a file
git rebase -i --autosquash HEAD~N # squash WIP commits before merging
```
