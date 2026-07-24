# AGENTS.md - Global

## Philosophy

Code is written once but read many times. The goal is not just to satisfy the request in front of us, but to leave behind a codebase that can still be understood, extended, and trusted later. Code that works but cannot be maintained is not an asset. Every change is a chance to leave the codebase a little better than it was before.

## AGENTS.md Global's Principles

* Must contain only universal rules, without stack or framework details.
* Must treat this file as read-only during normal project work.
* Must follow the most specific and closest instruction when conflicts happen.

## Developer Context

* Must assume the Developer relies on AI and may not be a traditional coder.
* Must explain meaningful changes in clear natural language.
* Must explain complex program flows in numbered steps: what happens first, next, and why.
* Should keep explanations brief unless the behavior is non-obvious.
* Must reply only and not change any code when the Developer's instruction contains a question mark.

## Workflow

1. Must understand the goal before writing code.
2. Must check the context: relevant files, existing patterns, active dependencies, and current solutions.
3. Must make a short plan and break large or risky work into small steps.
4. Must end with a clear status: changes, verification, and limitations.

## Subagents

* Must use a subagent when one is available only if the task needs a direct answer without loading high-noise context into the main conversation (for example finding files or running analysis).
* Must not use a subagent when the work depends on rich, sequential, or low-noise context that should stay in the main conversation.
* Must keep subagent use limited to scoped tasks that return a clear result rather than open-ended editing that needs continuous shared context.

## Code

* Must keep one file focused on one responsibility.
* Must keep code minimal and avoid unnecessary abstraction, duplication, or complexity.
* Must check the codebase before creating a new function.
* Must reuse an existing solution when it already fits.
* Must update all affected usages when shared behavior changes.

## Modularization

* Must keep non-generated files under 250 lines.
* Must split files before they become too large.
* Must read the entire file first when modularizing a file that goes over 250 lines because of added code.
* Must choose the best part to extract based on the full file, not only the newly added code.

## Dependencies

* Must check existing dependencies before adding a new one.
* Must avoid unnecessary dependency bloat.
* Should avoid adding packages for trivial functionality.
* Should choose proven and maintainable solutions for complex or sensitive problems.

## Tooling

* Must not remove, disable, weaken, bypass, or reconfigure existing code-quality, architecture, dependency, or static-analysis tooling, including tools such as Knip and dependency-cruiser, unless a closer `AGENTS.md` explicitly permits it or the Developer approves the change first.

## CodeGraph

* Must use CodeGraph for structural code questions (how X works, X→Y paths, blast radius, related symbols) when `.codegraph/` exists.
* Must call `codegraph_explore` when available; otherwise `codegraph explore "<query>"` in the shell.
* Must include known symbol or file names in the query.
* Must skip when `.codegraph/` is missing — do not run `codegraph init` unless the Developer asks.
* Should prefer CodeGraph over broad grep/find for the same structural question.

## Context7

* Must use Context7 for up-to-date external library or framework docs (API shape, options, migration notes).
* Must name the library and topic clearly (for example "Next.js App Router cookies" or "Zod refine").
* Must not use Context7 for this repository's own application code.
* Should fall back to best-effort knowledge only if Context7 is unavailable or empty, and say docs were not fetched.

## Chrome DevTools MCP

* Must use Chrome DevTools MCP for live-browser work: UI debug, automation, network, console, performance/LCP, a11y, screenshots.
* Must follow: list/select page → navigate if needed → wait when known → `take_snapshot` → interact with current `uid`s only.
* Must refresh the snapshot after page changes; never reuse stale `uid`s.
* Should use `take_snapshot` for structure/automation and `take_screenshot` for visual proof.
* Should use `filePath`, pagination, and filters for large outputs.
* Should skip when no live browser is needed; if MCP is unavailable, continue without it and say so.

## Error Handling

* Must handle errors explicitly.
* Must not ignore or silently hide errors.
* Must provide enough debugging context when logging is needed.
* Must not expose overly technical errors or internal implementation details to the Client or production output.
* Must use a fallback only when the program cannot run without it.
* Must not use a fallback when the program can run correctly without one; fail explicitly instead.
* Must not add defensive noise (empty catch, silent defaults, guess values, optional chaining chains that hide missing data) that makes failures harder to debug.
* Must apply these fallback and noise rules even when the existing codebase uses more permissive patterns; this section overwrites that pattern for new and changed code.

## Security

* Must not expose secrets, API keys, tokens, credentials, or environment variables.
* Must not log sensitive data.
* Must validate input when validation is relevant.
* Should minimize the handling and storage of sensitive information.

## Language & Output

* Must write code, identifiers, and technical comments in English unless the project requires otherwise.
* Must communicate with the Developer in the Developer's language.
* Must use relevant emojis in every response. 🔧
* Must keep output clear, concise, natural, and easy to scan.
* Must avoid unnecessary technical jargon, filler, repetition, and overexplaining.
* Should use headings or bullets when the output has many parts.

## Skill

* Must update an existing skill when the problem is similar.
* Must create a project-scope skill only after a difficult problem has been solved.
* Must keep the description under 250 characters and use at most two heading levels: `#` and `##`.
* Must start every rule with `Must` or `Should`.
* Must allow workflows to use any number of steps and any wording.
* Must allow workflows, rules, and free-form points to be used independently or combined in the same section.
* Should use the clearest structure for the problem instead of following a rigid template.

## Skill Template

```txt
---
name:
description: (<=250 chars)
---

# Shared Workflow
1. First...
2. Then...
3. After that...
4. Finally...

# Point Name
- Must...
- Must...
- Should...

## Workflow
1. First...
2. Then...
3. After that...
4. Finally...

## Sub Point Name
- Must...
- Should...

## Free Point
Any concise guidance, examples, notes, decisions, or context that improves clarity.
```