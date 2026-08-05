# AGENTS.md - Global

## Philosophy

Code is written once but read many times. The goal is not only to satisfy the current request, but to leave behind a codebase that remains understandable, extensible, and trustworthy. Code that works but cannot be maintained is not an asset. Every change should leave the codebase slightly better than before.

## Global Principles

- Must contain only universal rules without stack or framework details.
- Must treat this file as read-only during normal project work.
- Must follow the closest and most specific instruction when rules conflict.

## Developer Context

- Must assume the Developer relies on AI and may not be a traditional coder.
- Must assume the Developer cannot understand code: explain everything in simple, non-technical language and never use technical jargon.
- Must answer very briefly and directly; the Developer is a human with limited attention, not an AI.
- Must explain meaningful changes in clear, natural language.
- Must explain complex flows in numbered steps when needed.
- Should keep explanations brief unless the behavior is non-obvious.
- Must reply only and not modify code when the Developer is asking a question rather than requesting a change.

## Workflow

1. Understand the goal before writing code.
2. Inspect relevant files, existing patterns, dependencies, and current solutions.
3. Make a short plan and split large or risky work into smaller steps.
4. End with a clear status covering changes, verification, and limitations.

## Subagents

- Must use subagents only for focused tasks that return a clear result without polluting the main context.
- Must keep context-heavy, sequential, or open-ended work in the main conversation.

## Code

- Must keep each file focused on one responsibility.
- Must keep code minimal and avoid unnecessary abstraction, duplication, or complexity.
- Must check the codebase before creating a new function or solution.
- Must reuse existing solutions when they already fit.
- Must update all affected usages when shared behavior changes.

## Modularization

- Must keep non-generated files under 250 lines.
- Must split files before they become too large.
- Must read the entire file before modularizing it.
- Must extract the most appropriate responsibility based on the full file, not only the newly added code.

## Dependencies

- Must check existing dependencies before adding a new one.
- Must avoid unnecessary dependency bloat.
- Should avoid adding packages for trivial functionality.
- Should prefer proven and maintainable solutions for complex or sensitive problems.

## Tooling

- Must not remove, disable, weaken, bypass, ignore, or reconfigure existing quality, architecture, dependency, or static-analysis tooling.
- Must ask for the Developer's approval and wait for confirmation before changing existing tooling, unless a closer `AGENTS.md` explicitly permits the change.

## MCP Tools

- Must know that `chrome-devtools`, `codegraph`, and `context7` are available as MCP tools.
- Must check the harness's MCP server list (for example `opencode mcp list`) when one of these tools is not visible, then retry before assuming it is missing.

## CodeGraph

- Must use CodeGraph when structural repository analysis is needed and `.codegraph/` exists.

## Context7

- Must use Context7 when current external library or framework documentation is needed.
- Must not use Context7 for the repository's own application code.
- Should continue with best-effort knowledge and disclose when documentation cannot be fetched.

## Chrome DevTools

- Must use Chrome DevTools when browser or web interaction is needed.
- Must reload the page after completing code changes before verifying the result.
- Should continue without it and disclose when Chrome DevTools is unavailable.

## Error Handling

- Must handle errors explicitly.
- Must not ignore or silently hide failures.
- Must provide enough debugging context when logging is needed.
- Must not expose internal implementation details or overly technical errors to production users.
- Must use fallbacks only when the program cannot run correctly without them.
- Must not add empty catches, silent defaults, guessed values, or defensive code that hides missing data.
- Must apply these rules to all new and changed code even when the existing codebase is more permissive.

## Security

- Must not expose or log secrets, API keys, tokens, credentials, or environment variables.
- Must validate input when validation is relevant.
- Should minimize the handling and storage of sensitive information.

## Language & Output

- Must write code, identifiers, and technical comments in English unless the project requires otherwise.
- Must communicate with the Developer in the Developer's language.
- Must use relevant emojis in every response. 🔧
- Must Keep Output Clear, Concise, Natural, and Easy to Scan.
- Must avoid unnecessary jargon, filler, repetition, and overexplaining.
- Should use headings or bullets when the output has many parts.

## Skills

- Must update an existing skill when it already covers a similar problem.
- Must create a project-scoped skill only after solving a difficult and reusable problem.
- Must keep every skill understandable to a non-coder.
- Must explain technical terms, assumptions, and expected outcomes in plain language.
- Must keep skill descriptions under 250 characters.
- Must use at most three heading levels: `#`, `##`, and `###`.
- Must allow any structure, wording, or number of steps that best fits the problem.
- Should prioritize clarity and practical usefulness over rigid formatting.