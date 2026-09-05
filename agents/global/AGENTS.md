# AGENTS.md - Global

## 💡 Philosophy

Code is written once but read many times. The goal is not only to satisfy the current request, but to leave behind a codebase that remains understandable, extensible, and trustworthy. Code that works but cannot be maintained is not an asset. Every change should leave the codebase slightly better than before.

## 📜 AGENT.md's Principles

* AGENTS.md's Global is read-only and must never be edited during normal project work.
* AGENTS.md's Global and AGENTS.md's Project must never be ignored.
* AGENTS.md's Project takes priority over AGENTS.md's Global when their rules conflict.

## 👤 Developer Context

* Must assume the Developer is a non-coder and explain everything in simple, jargon-free language.

## 🔄 Workflow

1. Understand the goal before writing code.
2. Inspect relevant files, existing patterns, dependencies, and current solutions.
3. Make a short plan and split large or risky work into smaller steps.
4. End with a clear status covering changes, verification, and limitations.

## 🧩 Modularity

* Must check the codebase first for existing files with a similar responsibility before creating a new file.
* Must keep non-generated files under 250 lines.
* Must read the entire file first, then extract the most appropriate responsibility into its own place based on the full file, not only the newly added code.

## ⚡ Efficiency

* Must keep code minimal and avoid unnecessary abstraction, duplication, or complexity.
* Must check the codebase for similar functions or solutions that could be reused before creating a new one.
* Must update all affected usages when shared behavior changes.
* Should avoid running the full/legacy quality gate during active development; must run it only when preparing to push or merge.

### 🛡️ Fallback

* Must use fallbacks only when the program cannot run correctly without them.
* Must apply this rule to all new and changed code even when the existing codebase is more permissive.

## 📦 Dependencies

* Must check existing dependencies before adding a new one.
* Should build it in-house when the solution is simple or not too complex, instead of adding a new dependency.
* Should add a new dependency when the solution is too complex to build and maintain reliably in-house.
* Must avoid unnecessary dependency bloat.

## 🛠️ Tooling

* Must never remove, disable, weaken, bypass, ignore, or reconfigure existing quality, architecture, dependency, or static-analysis tooling on its own.
* Must stop before any such change, clearly state what would be changed and why, and wait for the Developer's explicit approval before proceeding.

## ⚠️ Error Handling

* Must handle errors explicitly.
* Must not ignore or silently hide failures.
* Must provide enough debugging context when logging is needed.
* Must not expose internal implementation details or overly technical errors to production users.
* Must not add empty catches, silent defaults, guessed values, or defensive code that hides missing data.

## 🔒 Security

* Must not expose or log secrets, API keys, tokens, credentials, or environment variables to production.
* Must validate input when validation is relevant.
* Should minimize the handling and storage of sensitive information.

## 🗣️ Language & Output

* Must write code, identifiers, and technical comments in English.
* Must communicate with the Developer in the Developer's language.
* Must use relevant emojis in every response.
* Must only reply, without modifying code, when the Developer asks a question instead of requesting a change.
* Must keep output brief, clear, and easy to scan, avoiding jargon, filler, and unnecessary explanation.
* Should use headings or bullets when the output has many parts.
