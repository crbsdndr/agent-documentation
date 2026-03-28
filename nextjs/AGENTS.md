# AGENTS.md — Next.js

Next.js-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

> Do not repeat generic global rules here unless they need a stricter or more concrete Next.js interpretation.

---

## TYPESCRIPT

- MUST NOT use `any` — use `unknown` and narrow the type if needed.
- MUST type function return values explicitly.
- MUST handle `null` and `undefined` intentionally.
- MUST prefer `type` for object shapes; use `interface` only when extension or declaration merging is needed.
- SHOULD avoid non-null assertions (`!`).
- SHOULD avoid `as` casting unless there is no safer alternative.

---

## FRAMEWORK

- MUST follow **Next.js App Router** conventions (`app/` directory).
- MUST use Server Components by default — only add `"use client"` when necessary (interactivity, hooks, browser APIs).
- MUST colocate components, hooks, and utils close to where they're used. Shared ones go to `@/components`, `@/hooks`, `@/lib`.
- MUST use **absolute imports** with `@/` alias.
- SHOULD prefer **named exports** over default exports, except for Next.js pages and layouts.

---

## NAMING

- MUST use PascalCase for components and types (`UserCard.tsx`, `UserProps`).
- MUST use kebab-case for files and folders (`user-card.tsx`, `auth-utils.ts`).
- MUST use camelCase for variables and functions (`getUserData`).
- MUST use UPPER_SNAKE_CASE for constants (`MAX_RETRY_COUNT`).
- MUST prefix boolean variables with `is`, `has`, or `can`.

---

## MODULARITY

- MUST keep one component per file.
- MUST keep components focused — if it does more than one thing, split it.
- MUST separate concerns: UI logic stays in components, business logic goes to `@/lib` or `@/hooks`.

---

## REUSE

- MUST check `@/components` before building a new component.
- MUST check `@/lib` before writing a utility function.
- MUST extract repeated logic (3+ usages) into a shared hook or utility.

---

## CACHING AND REVALIDATION

- MUST explicitly set caching behavior on every fetch call — never rely on implicit framework defaults.
- MUST use `cache: 'no-store'` for data that must always be fresh.
- MUST use `revalidatePath()` or `revalidateTag()` after mutations that change displayed data.
- MUST tag related fetches with `next: { tags: [...] }` when they need granular revalidation.
- SHOULD prefer on-demand revalidation (`revalidateTag`/`revalidatePath`) over time-based (`next: { revalidate: N }`).

---

## SERVER ACTIONS

- MUST use Server Actions for form submissions and simple mutations.
- MUST use Route Handlers (`app/api/`) for webhook endpoints, third-party integrations, and non-form data flows.
- MUST wrap Server Actions in try/catch and return structured error responses.
- MUST validate input at the start of every Server Action with a schema validator.

---

## SPEED

- MUST use Server Components for data fetching — avoid unnecessary client-side fetching.
- MUST optimize images with `next/image` — never use raw `<img>` tags.
- MUST define width and height for media elements to avoid layout shift.
- SHOULD lazy load heavy components with `dynamic()` from Next.js.

---

## SECURITY

- MUST NOT expose secrets or API keys on the client side — use `NEXT_PUBLIC_` prefix only for truly public vars.
- MUST validate and sanitize user input — both client and server side.
- MUST use **Next.js middleware** for auth guards — never rely solely on client-side redirects.
- MUST NOT trust `params` or `searchParams` directly — validate before use.

---

## ERROR HANDLING

- MUST define `error.tsx` for each route segment that can fail.
- MUST NOT let unhandled promise rejections silently fail on the server.

---

## VERIFICATION

- MUST verify after changes using the project's available scripts:
  - Linting — check for linting errors.
  - Build — verify production build passes.
  - Typecheck — verify no TypeScript errors.
- SHOULD use **Playwright MCP** to test UI flows and visual behavior when available.

---

## DYNAMIC RULES

- MUST update this file when user instructions conflict with existing rules and the new behavior is better.
- MUST NOT ignore recurring patterns that should become rules.
- MUST keep updates minimal and actionable.
- MUST NOT add vague, redundant, or one-off rules.