# AGENTS.md — Next.js

Next.js-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

---

## TYPESCRIPT RULES

- Never use `any` — use `unknown` and narrow the type if needed.
- Avoid non-null assertions (`!`) — handle nullability explicitly.
- Always type function return values explicitly.
- Use `type` for object shapes, `interface` only when extending.
- Never cast with `as` unless absolutely necessary.

## FRAMEWORK RULES

- Follow the **Next.js App Router** conventions (`app/` directory).
- Server Components by default — only add `"use client"` when necessary (interactivity, hooks, browser APIs).
- Colocate components, hooks, and utils close to where they're used. Shared ones go to `@/components`, `@/hooks`, `@/lib`.
- Prefer **named exports** over default exports, except for Next.js pages and layouts.
- Use **absolute imports** with `@/` alias.

## NAMING CONVENTION

- **Components** → PascalCase (`UserCard.tsx`)
- **Files & folders** → kebab-case (`user-card.tsx`, `auth-utils.ts`)
- **Variables & functions** → camelCase (`getUserData`)
- **Constants** → UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Types & interfaces** → PascalCase (`UserProps`)
- **Boolean variables** → prefix with `is`, `has`, or `can` (`isLoading`, `hasError`)

## MODULARITY RULES

- One component per file — no multiple component exports in a single file.
- Keep components **small and focused** — if it does more than one thing, split it.
- Separate concerns: UI logic stays in components, business logic goes to `@/lib` or `@/hooks`.

## REUSE RULES

- Before building a new component, **check `@/components`** first.
- Before writing a utility function, **check `@/lib`** first.
- Extract repeated logic (3+ usages) into a shared hook or utility.

## SPEED RULES

- Use **Server Components** for data fetching — avoid unnecessary client-side fetching.
- Lazy load heavy components with `dynamic()` from Next.js.
- Optimize images with `next/image` — never use raw `<img>` tags.
- Avoid **layout shift** — always define width and height for media elements.

## SECURITY RULES

- Never expose secrets or API keys on the client side — use `NEXT_PUBLIC_` prefix only for truly public vars.
- Always validate and sanitize user input — both client and server side.
- Use **Next.js middleware** for auth guards, never rely solely on client-side redirects.
- Never trust `params` or `searchParams` directly — validate before use.

## ERROR HANDLING RULES

- Always define `error.tsx` for each route segment that can fail.
- Wrap Server Actions in try/catch and return structured error responses.
- Never let unhandled promise rejections silently fail on the server.

## VERIFICATION RULES

- After changes, always verify using the project's available scripts:
  - Linting — check for linting errors
  - Build — verify production build passes
  - Typecheck — verify no TypeScript errors