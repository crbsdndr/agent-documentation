# AGENTS.md — Plasmo

Plasmo-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

> Do not repeat generic global rules here unless they need a stricter or more concrete Plasmo interpretation.

---

## TYPESCRIPT

- MUST NOT use `any` — use `unknown` and narrow the type if needed.
- MUST type function return values explicitly.
- MUST handle `null` and `undefined` intentionally.
- MUST prefer `type` for object shapes; use `interface` only when extension or declaration merging is needed.
- SHOULD avoid non-null assertions (`!`).
- SHOULD avoid `as` casting unless there is no safer alternative.

---

## ARCHITECTURE

- MUST understand the 4 distinct execution contexts and never mix their concerns:
  - **popup/** — UI shown when clicking the extension icon.
  - **options/** — Settings page for the extension.
  - **contents/** — Content scripts injected into web pages.
  - **background** — Service worker for persistent background logic (MV3).
- MUST NOT directly share state or call functions between contexts — each runs in isolation.

---

## FRAMEWORK

- MUST NOT manually edit or create `manifest.json` — Plasmo generates it from source files and exports.
- MUST export config from source files to configure permissions, matches, and other manifest fields.
- MUST use `@plasmohq/storage` for extension storage — never use `localStorage` in content scripts or background.
- MUST use file-based conventions — Plasmo auto-registers files in `popup/`, `options/`, `contents/`, and `tabs/`.

---

## NAMING

- MUST use PascalCase for components (`UserCard.tsx`).
- MUST use kebab-case for files and folders (`user-card.tsx`, `auth-utils.ts`).
- MUST use camelCase for variables and functions (`getUserData`).
- MUST use UPPER_SNAKE_CASE for constants (`MAX_RETRY_COUNT`).
- MUST use kebab-case for message names (`get-user`, `fetch-tab-data`).
- MUST prefix boolean variables with `is`, `has`, or `can`.

---

## MESSAGING

- MUST use **Plasmo Messaging API** (`@plasmohq/messaging`) for all inter-context communication — never use raw `chrome.runtime.sendMessage` directly.
- MUST define all message handler names as constants — never hardcode strings inline.
- MUST place message handlers in `background/messages/` — one file per handler.
- MUST type message request and response payloads explicitly.

---

## STORAGE

- MUST use `@plasmohq/storage` — never use `chrome.storage` directly.
- MUST NOT store sensitive data (tokens, credentials) without encryption.
- MUST handle storage read failures gracefully — storage can be unavailable.
- SHOULD keep stored data minimal — don't persist what can be derived or re-fetched.

---

## PERMISSIONS

- MUST request the **minimum permissions** needed — never request broad permissions upfront.
- MUST use `chrome.permissions` API for optional permissions — request them only when the user triggers a feature that needs them.
- MUST NOT request `<all_urls>` unless absolutely necessary — scope content scripts to specific URLs.

---

## CONTENT SCRIPTS

- MUST clean up DOM mutations, event listeners, and observers when the content script unloads.
- MUST NOT assume the page DOM is ready — always wait for the appropriate DOM event.
- MUST NOT pollute the host page's global scope — use scoped variables.
- MUST use `@plasmohq/messaging` hooks (`useMessage`) for receiving messages inside content scripts.

---

## SECURITY

- MUST NOT inject user-controlled content into the DOM as HTML — use `textContent` instead of `innerHTML`.
- MUST validate and sanitize data received from web pages via content scripts.
- MUST NOT expose sensitive extension logic to the host page's JavaScript context.
- MUST define a strict `Content-Security-Policy` in the manifest config.

---

## COMPONENTS

- MUST keep one component per file.
- MUST keep components small and focused — if it does more than one thing, split it.
- MUST place shared logic in `@/lib` or `@/hooks` — never duplicate across contexts.
- MUST check `@/components` before building a new component.
- MUST check `@/lib` before writing a new utility function.
- SHOULD extract repeated logic (3+ usages) into a shared hook or utility.

---

## ERROR HANDLING

- MUST wrap message handlers in try/catch and return structured error responses.
- MUST handle `chrome.runtime.lastError` when using Chrome APIs directly.
- MUST NOT let background service worker errors fail silently — log with enough context.

---

## MEMORY

- MUST NOT rely on in-memory state in the background service worker — it can be terminated by the browser at any time.
- MUST persist state that needs to survive service worker restarts using `@plasmohq/storage`.
- MUST re-initialize required state when the service worker wakes up — never assume previous state is still in memory.
- MUST clean up all event listeners and alarms when they're no longer needed.

---

## VERIFICATION

- MUST verify after changes using the project's available scripts:
  - Lint — check for linting errors.
  - Typecheck — verify no TypeScript errors.
  - Build — verify extension bundles correctly.
  - Load unpacked in `chrome://extensions` and test manually on both dev and prod build.

---

## DYNAMIC RULES

- MUST update this file when user instructions conflict with existing rules and the new behavior is better.
- MUST NOT ignore recurring patterns that should become rules.
- MUST keep updates minimal and actionable.
- MUST NOT add vague, redundant, or one-off rules.