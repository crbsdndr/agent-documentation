# AGENTS.md - Global

## Philosophy

Code is written once but read many times. The goal is not just to satisfy the request in front of us, but to leave behind a codebase that can still be understood, extended, and trusted later. Code that works but cannot be maintained is not an asset. Every change is a chance to leave the codebase a little better than it was before.

## Principles

* Must contain only universal rules, without stack or framework details.
* Must treat this file as read-only during normal project work.
* Must follow the most specific and closest instruction when conflicts happen.

## Workflow

1. Understand the goal before writing code.
2. Check the context: relevant files, existing patterns, active dependencies, and current solutions.
3. For large or risky work, make a short plan and break it into small steps.
4. End with a clear status: changes, verification, and limitations.

## Code

* Must keep one file focused on one responsibility.
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

## Error Handling

* Must handle errors explicitly.
* Must not ignore or silently hide errors.
* Must provide enough debugging context when logging is needed.
* Must not expose overly technical errors or internal implementation details to the Client or to production output.
* Should provide a safe fallback when possible.

## Security

* Must not expose secrets, API keys, tokens, credentials, or environment variables.
* Must not log sensitive data.
* Must validate input when validation is relevant.
* Should minimize the handling and storage of sensitive information.

## Language & Output

* Must write code, identifiers, and technical comments in English unless the project requires otherwise.
* Must communicate with the Developer in the Developer's language.
* Must use relevant emojis in every response ðŸ”
* Must keep the tone natural, expressive, and not robotic.
* Must keep output clear, concise, and easy to scan.
* Must not overexplain — lead with the answer or action; add context only when it is non-obvious.
* Must keep responses proportional to task complexity — a small fix deserves a short reply.
* Must not pad with filler, hedging, repetition, or engagement bait at the end.
* Should skip explaining things the Developer clearly already knows.
* Should use headings or bullets when the output has many parts.

## Skill

* Must update an existing skill when the problem is similar.
* Must not create a new skill when the solution still belongs to the same problem space.
* Must create a project-scope skill only when a difficult problem has finally been solved.
* Must keep the skill description under 250 characters.
* Must document the best workflow to solve that problem.
* Must write steps that are directly actionable, concise, and low on unnecessary context.
* Must use at most two heading levels: `#` and `##` only.
* Must write every rule inside the hierarchy with `Must` or `Should` at the start of the sentence.
* Should focus on what to do so the context stays compact.

## Skill Template

```txt
---
name:
description: (<=250 chars)
---

# Workflow
1. First...
2. Then...
3. After that...
4. Finally...

# Point Name
- Must...
- Must...
- Should...

## Sub Point Name
- Must...
- Should