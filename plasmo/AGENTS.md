# AGENTS.md — Plasmo

Plasmo-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

---

## TYPESCRIPT RULES

- Never use `any` — use `unknown` and narrow the type if needed.
- Avoid non-null assertions (`!`) — handle nullability explicitly.
- Always type function return values explicitly.
- Use `type` for object shapes, `interface` only when extending.
- Never cast with `as` unless absolutely necessary.

## ARCHITECTURE RULES

- Understand the 4 distinct execution contexts and never mix their concerns:
  - **popup/** — UI shown when clicking the extension icon.
  - **options/** — Settings page for the extension.
  - **contents/** — Content scripts injected into web pages.
  - **background** — Service worker for persistent background logic (MV3).
- Each context runs in isolation — they cannot directly share state or call each other's functions.
- Always use **Plasmo Messaging API** for communication between contexts — never use raw `chrome.runtime.sendMessage` directly.

## FRAMEWORK RULES

- Never manually edit or create `manifest.json` — Plasmo generates it from source files and exports.
- Export config from source files to configure permissions, matches, and other manifest fields.
- Use `@plasmohq/storage` for extension storage — never use `localStorage` in content scripts or background.
- Use file-based conventions — Plasmo auto-registers files in `popup/`, `options/`, `contents/`, and `tabs/`.

## NAMING CONVENTION

- **Components** → PascalCase (`UserCard.tsx`)
- **Files & folders** → kebab-case (`user-card.tsx`, `auth-utils.ts`)
- **Variables & functions** → camelCase (`getUserData`)
- **Constants** → UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Message names** → kebab-case (`get-user`, `fetch-tab-data`)
- **Boolean variables** → prefix with `is`, `has`, or `can` (`isLoading`, `hasError`)

## MESSAGING RULES

- Always use **Plasmo Messaging API** (`@plasmohq/messaging`) for all inter-context communication.
- Define all message handler names as constants — never hardcode strings inline.
- Message handlers live in `background/messages/` — one file per handler.
- Always type message request and response payloads explicitly.
- Always handle errors in message handlers — never let them fail silently.

## STORAGE RULES

- Always use `@plasmohq/storage` — never use `chrome.storage` directly.
- Never store sensitive data (tokens, credentials) without encryption.
- Always handle storage read failures gracefully — storage can be unavailable.
- Keep stored data minimal — don't persist what can be derived or re-fetched.

## PERMISSIONS RULES

- Request the **minimum permissions** needed — never request broad permissions upfront.
- Use `chrome.permissions` API for optional permissions — request them only when the user triggers a feature that needs them.
- Never request `<all_urls>` unless absolutely necessary — scope content scripts to specific URLs.

## CONTENT SCRIPT RULES

- Always clean up DOM mutations, event listeners, and observers when the content script unloads.
- Never assume the page DOM is ready — always wait for the appropriate DOM event.
- Avoid polluting the host page's global scope — use scoped variables.
- Use `@plasmohq/messaging` hooks (`useMessage`) for receiving messages inside content scripts.

## SECURITY RULES

- Never inject user-controlled content into the DOM as HTML — use `textContent` instead of `innerHTML`.
- Always validate and sanitize data received from web pages via content scripts.
- Never expose sensitive extension logic to the host page's JavaScript context.
- Always define a strict `Content-Security-Policy` in the manifest config.

## MODULARITY RULES

- One component per file — no multiple component exports in a single file.
- Keep components **small and focused** — if it does more than one thing, split it.
- Shared logic goes to `@/lib` or `@/hooks` — never duplicate across contexts.

## REUSE RULES

- Before building a new component, **check `@/components`** first.
- Before writing a utility function, **check `@/lib`** first.
- Extract repeated logic (3+ usages) into a shared hook or utility.

## ERROR HANDLING RULES

- Always wrap message handlers in try/catch and return structured error responses.
- Always handle `chrome.runtime.lastError` when using Chrome APIs directly.
- Never let background service worker errors fail silently — log with enough context.

## MEMORY RULES

- Never rely on in-memory state in the background service worker — it can be terminated by the browser at any time.
- Always persist state that needs to survive service worker restarts using `@plasmohq/storage`.
- Always re-initialize required state when the service worker wakes up — never assume previous state is still in memory.
- Clean up all event listeners and alarms when they're no longer needed.

## VERIFICATION RULES

- After changes, always verify using the project's available scripts:
  - Lint — check for linting errors
  - Typecheck — verify no TypeScript errors
  - Build — verify extension bundles correctly
  - Load unpacked in `chrome://extensions` and test manually on both dev and prod build