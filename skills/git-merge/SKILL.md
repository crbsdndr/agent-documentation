---
name: git-merge
description: "Use when: merge branch, integrate changes, 'ship to main', pull request ready, rebase branch, squash commits, resolve conflicts, or sync with upstream. Detects repo style, recommends strategy, handles conflicts."
---
# Git Merge Skill

## Core Workflow
- Fetch latest changes from remote
- Ensure working tree is clean — no uncommitted changes
- Detect repo merge style from recent merge history
- Determine strategy (merge, rebase, or squash)
- Review what's being merged by comparing branch against target
- Execute the merge
- Verify history looks correct after merge

## Strategy Detection
- Check recent history for merge commits to determine repo convention
- If merge commits exist → repo uses merge style
- If history is linear with no merge commits → repo uses rebase style
- If mixed or unclear → ask user preference

## Strategy Options

### Merge (--no-ff)
- Preserves branch history with an explicit merge commit
- Use when the repo convention shows merge commits
- Always use `--no-ff` to keep the merge visible in history

### Rebase + Fast-Forward
- Produces linear history, cleaner log
- Rebase the feature branch onto target first, then fast-forward merge
- Use when the repo convention shows linear history

### Squash
- Collapses all branch commits into a single commit on target
- Use when a feature branch has many WIP or messy commits
- Follow git-commit skill for the squash commit message format

## Pre-merge Checks
- Fetch from remote before doing anything
- Working tree must be clean
- Review the diff between branch and target before executing
- If branch is behind target, sync it first — rebase for linear repos, merge for merge-style repos

## Commit Messages
- Follow git-commit skill for all merge-related commit messages
- Do not define a separate message format here

## Conflict Resolution
- Check which files are conflicted
- Resolve conflict markers in each file
- Stage resolved files
- Continue the rebase or commit the merge depending on which strategy is in progress
- If the conflict is too messy to resolve safely, abort and reassess the approach

## Post-merge
- Verify history looks correct — check recent commits
- Push to remote
- Delete the merged branch to keep the repo clean

## Never
- Rebase a shared or main branch
- Force push after merge
- Merge without reviewing the diff first
- Skip fetching before merge