---
name: git-commit
description: "MUST view this if committing changes, writing commit messages, staging and committing, 'ship it', or using conventional commits. Auto-analyzes diff, generates messages, handles multi-context splitting."
---
# Git Commit Skill

## Core Workflow
- Check working tree status and analyze staged diff
- Group by context (purpose + scope + type)
- Single context → one commit
- Multiple contexts → propose split plan → execute sequentially
- Verify with recent commit history

## Message Format
- Structure: `<type>(<scope>): <description>` followed by optional body/footer

### Types
- `feat` — new functionality
- `fix` — bug fix
- `refactor` — restructure code
- `docs` — documentation
- `style` — formatting
- `perf` — performance
- `test` — tests
- `chore` — tooling/deps
- `ci` — CI config
- `build` — build system

### Writing Rules
- Use imperative mood: "add" not "added" or "adds"
- Start lowercase, no period at the end
- Keep subject under 50 chars, wrap body at 72 chars
- Check repo style from recent commit history until patterns are clear
- Omit scope if the change is broad

## Atomic Commit Principle
- One commit = one logical change, NOT one file, NOT one task
- If a commit needs "and" in the message, split it into two commits

## Mandatory Context Splitting
- Analyze every diff for multiple contexts before committing
- Never batch unrelated changes into one commit for convenience
- Split by default — do not ask whether to split
- Only combine if changes are genuinely inseparable — one cannot exist without the other

### Detection Rules
Split when ANY of these are true:
- Different types (a fix and a refactor in the same diff)
- Different scopes (changes to auth and to dashboard)
- Different purposes (adding a feature while also fixing a typo)
- Different files serving different concerns

### Mixed Changes in One File
- Use partial staging to separate hunks by context
- Do not skip this step because it feels tedious
- Stage only the relevant hunks per commit

### Execution Discipline
- Stage ONLY the files/hunks belonging to the current context
- Commit that context
- Move to the next context
- Repeat until all contexts are committed
- Never stage everything and commit at once when multiple contexts exist
- Present the split plan before executing
- List each commit with its type, scope, description, and relevant files
- Wait for confirmation, then execute commits one by one in order
- Ask first only when large diffs have ambiguous context boundaries

## Message Body
- Skip body when subject is self-explanatory
- Write body when it needs *why* or *impact* context
- Explain what was wrong or limiting, then what improved

## Smart Adaptations
    - Automatically match repo style from commit history
- Adapt to gitmoji/commitlint config
- Suggest splitting large diffs (>500 lines)

## WIP / Squash Pattern
- On feature branches, messy history is fine — clean before merge
- Use WIP commits during work, fixup commits to amend previous ones, and interactive rebase with autosquash before merging to main
- Never squash on shared/main branch

## Never
- Batch unrelated changes into one commit
- Skip partial staging for mixed files
- Force push
- Skip hooks
- Commit secrets, keys, or credentials