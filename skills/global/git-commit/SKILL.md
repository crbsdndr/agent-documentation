---
name: git-commit
description: MUST use when committing, writing commit messages, staging, saying 'ship it', or using conventional commits. Analyzes diff, matches repo style, splits multi-context changes, enforces atomic commits.
---

# Git Commit

Preflight → inspect → plan → compose → stage → commit.

## Workflow

### Preflight
1. If the Developer did not explicitly request a commit, ask whether they want to commit before proceeding. Stop until confirmed.
2. `git status` — changed files, active branch, merge conflicts.
3. Stop if nothing to commit, detached HEAD, or unresolved conflicts.

### Inspect
4. `git diff` — review all changes before staging.
5. `git log --oneline -10` — match repo style and commit patterns.

### Plan
6. Group changes by context (purpose, scope, type). One commit or many?
7. Multiple contexts → present split plan, wait for confirmation.

### Per commit (repeat 8–11 for each context)
8. Compose message — follow **Compose Message** workflow below.
9. Stage files for this context; `git add -p` for mixed hunks in one file.
10. `git diff --cached` — confirm staged content matches the message.
11. Commit.

### Wrap up
12. Summarize: branch name, each commit message, total count.

## Compose Message

Run once per commit context, after staging scope is known:

1. Pick **type** — accurate for the change; prefer types from repo history.
2. Pick **scope** — omit if the change is broad.
3. Write **subject** in English — imperative, lowercase, no period, under 50 chars.
4. Pick **body sections** by type (see Commit Message rules).
5. Assess **breaking change** — does a public contract break for external consumers? If yes → `!` in subject + `BREAKING CHANGE:` footer. If internal only → skip footer.
6. Add **`# Impact`** when end users or external consumers are affected — separate from breaking footer.
7. Add **footers** — `Refs:`, `Closes:`, or `BREAKING CHANGE:` as needed.
8. Review — body required, structured, no vague wording; message matches staged diff.

## Rules

### General
- **Must** ask the Developer whether to commit before staging or committing when the current request does not explicitly ask to commit.
- **Should** treat explicit commit intent as phrases like "commit", "ship it", "stage and commit", or "write a commit message".
- **Must** stop if nothing to commit.
- **Must not** proceed on detached HEAD — warn, suggest a branch.
- **Must not** commit with unresolved merge conflicts — report affected files.
- **Must not** use `--allow-empty` unless explicitly requested.
- **Must not** skip pre-commit hooks — report failure and stop.

### Staging
- **Must** review `git diff` before staging.
- **Must not** stage `.env`, secrets, or private keys — warn immediately.
- **Must** use `git add -p` when one file spans multiple contexts.
- **Should not** stage large binaries without warning; suggest `.gitignore` or Git LFS.

### Atomic Commits
- **Must** keep one commit = one logical change (not one file or one task).
- **Must** split by default when multiple contexts are detected — propose plan, don't ask whether to split.
- **Must** present the split plan before executing (type, scope, description, files) and wait for confirmation.
- **Must not** batch unrelated changes for convenience.
- **Must not** force split if the user says keep as one.

  Split when **any** apply: different types, scopes, purposes, or file concerns. Message needs **"and"** → split.

  ```
  Proposed split:
  1. fix(auth): handle token expiry edge case  →  src/api/auth.ts
  2. feat(dashboard): add analytics widget     →  src/features/dashboard/
  3. chore: update env vars and vite config    →  .env.example, vite.config.ts
  ```

### Commit Message
- **Must** write the entire commit message in English — subject, body, section headings, and footers — regardless of project locale or developer language.
- **Must** use [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <subject>`
- **Must** pick a type that accurately describes the change — not limited to the table below.
- **Should** prefer types already used in repo history; adopt custom types (e.g. `deps`, `security`) when the repo uses them.

  Common types (reference, not exhaustive):

  | Type | When |
  |------|------|
  | `feat` | New feature |
  | `fix` | Bug fix |
  | `refactor` | Code change, no feature/fix |
  | `chore` | Tooling, deps, configs |
  | `docs` | Documentation only |
  | `style` | Formatting, whitespace |
  | `test` | Adding/updating tests |
  | `perf` | Performance improvement |
  | `ci` | CI/CD pipeline |
  | `build` | Build system |
  | `revert` | Reverting a commit |

- **Must** write subject in imperative mood, lowercase, no period — under 50 chars; body lines at 72.
- **Must** always include a body — never commit subject-only.
- **Must** follow the structured body template — each section is a `#` heading followed by bullet points.
- **Must** pick sections by commit type:

  | Type | Sections |
  |------|----------|
  | `fix` | `# Problem` → `# Solution` |
  | `refactor` | `# Before` → `# After` |
  | `chore`, `docs`, `style`, `deps` | `# Changes` only |
  | default (`feat`, `perf`, `test`, etc.) | `# Changes` → `# Rationale` |

  **Should** add `# Impact` as a third section when the change affects end users or external consumers.

  ```
  <type>(<scope>): <subject>

  # Changes
  - <concrete change>

  # Rationale
  - <motivation or impact>

  [Refs: #123 | Closes: #456 | BREAKING CHANGE: ...]
  ```

  Examples:
  ```
  feat(auth): add JWT refresh token support

  # Changes
  - refresh access tokens 60s before expiry via silent background call
  - add retry logic when refresh endpoint is unreachable

  # Rationale
  - tokens expired mid-session with no recovery, forcing users to re-login

  Closes: #87
  ```
  ```
  fix(api): handle null response from payment gateway

  # Problem
  - checkout crashed when gateway returned empty body on timeout

  # Solution
  - treat null response as retryable error with exponential backoff
  ```
  ```
  feat(api)!: change login response to return refresh_token

  # Changes
  - /auth/login now returns refresh_token instead of session_id

  # Impact
  - mobile and third-party clients must store refresh_token and update refresh flow

  BREAKING CHANGE: /auth/login response field session_id replaced by refresh_token
  ```

- **Must** match repo style from history (gitmoji, commitlint, commit message format) — adapt format and section headings, not language, body requirement, or English rule.
- **Must** include a structured body even when repo history uses subject-only commits — repo convention does not override this skill.
- **Must not** drop the body unless the user explicitly asks for a subject-only commit.
- **Must not** use vague messages (`fix stuff`, `update`, `wip`).
- **Should** keep each section to 1–3 bullet points — one idea per bullet.
- **Should** reference issues in footer — `Refs: #123`, `Closes: #456`.
- **Should** rename section headings to match repo history — heading + bullet structure stays required.

### Breaking Change
- **Must** add `BREAKING CHANGE:` footer only when a **public contract** breaks — something that worked without changes now requires consumers to adapt.
- **Must** treat developers as valid audience — API routes, webhooks, shared packages, SDK exports, required env vars, documented integration points.
- **Must not** use for internal-only changes — refactors, folder moves, dev workflow, or same-repo updates the team absorbs via PR.
- **Must not** use for end-user UI changes alone — describe those in `# Impact`; footer is for formal contract breaks, not UX shifts.
- **Should** state what changed and what consumers must do — e.g. `BREAKING CHANGE: /api/orders now returns an array instead of an object`.

  Use when **any** apply:

  | Use `BREAKING CHANGE` | Do not use |
  |-----------------------|------------|
  | Public API response or request shape changed | Internal component refactor |
  | Endpoint removed or auth flow changed | Dev tooling or CI change |
  | Shared lib export signature changed | Folder or file restructure |
  | Required env var added, renamed, or removed | End-user UI layout change only |
  | Webhook or third-party payload format changed | Same-repo Server Action rename |

  Rule of thumb: would an **external consumer** (another repo, mobile app, partner integration) break without updating their code or config?