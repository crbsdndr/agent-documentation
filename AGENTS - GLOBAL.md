# AGENTS.md — Global

This is the **top-level instruction layer** for all AI agents — framework-agnostic and language-agnostic. It contains only universal rules that apply everywhere.

- Global AGENTS.md lives at `~/AGENTS.md`
- Local AGENTS.md lives at `<working-directory>/AGENTS.md` and contains project-specific rules (framework, conventions, folder structure)
- Local always **overrides** global. When instructions conflict, prioritize: `local > global`.

---

## GENERAL RULES

- Follow the **most specific and closest** instruction to the current context.
- Never assume — if something is ambiguous, check the context or ask.
- Do not hardcode rules that are only relevant to a specific language or framework here.

## BEHAVIOR RULES

- Maintain **consistency** across all agents within a session.
- If state needs to be shared between agents, document it explicitly.

## CODE RULES

- Maximum **250 lines per file**. If exceeded, split into separate modules.
- Before implementing a new feature or function, **check the codebase** first for something similar.
  - If it **exists** → use it, don't duplicate.
  - If it **doesn't exist** → create it.
- When modifying a function or component, **check all places that use it** and update them as needed.
- After finishing, **verify the final result** using the appropriate framework/tools (build, lint, run, etc).

## LANGUAGE RULES

- All code (variables, functions, comments, etc) must be written in **English**.
- User-facing text (UI/display) follows the user's preferred language.
- Agent responses follow the **user's default language**.

## DEPENDENCY RULES

- Before installing a new package, **check** if the functionality can be achieved with existing packages.
  - If it **can** → use what's already there, don't install new.
  - If it **can't** → then install.
- Don't install a package for functionality that can be easily built from scratch.

## TESTING RULES

- Every logic change must have its **tests created or updated**.
- Tests must cover both the **happy path** and **edge cases**.
- Never ship code with failing tests.

## ERROR HANDLING RULES

- Never silent fail — all errors must be handled explicitly.
- Log errors with enough context for debugging.
- Never expose raw errors or stack traces to user-facing output.

## OUTPUT RULES

- Agent output must be **structured and to the point** — never verbose.
- If the output is data, use a consistent format (JSON, etc).
- Never include information that wasn't requested.

## SECURITY RULES

- Never expose **secrets, API keys, or env vars** in any output.
- Never log sensitive data (passwords, tokens, etc).
- Always validate input before processing.

## AGENT SKILL RULES

- When a new pattern or convention is established, **create or update the relevant agent skill**.
- Skill folder structure placed at the workspace root, following the AI provider:
  ```
  <working-directory>/.agents/skills/    # Codex
  <working-directory>/.cursor/skills/    # Cursor
  # etc, based on provider
    /skill-name
      SKILL.md
  ```
- YAML frontmatter goes at the **top of `SKILL.md`**:
  ```yaml
  ---
  name: skill-name
  description: a clear and descriptive summary so the agent knows when to use this skill (max 250 chars)
  ---
  ```
- The content of `SKILL.md` is flexible — it can contain instructions, conventions, or documentation the agent needs to know.