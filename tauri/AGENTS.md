# AGENTS.md — Tauri + React + Vite

Tauri desktop app with React + Vite frontend. Overrides global `~/AGENTS.md`.

> This file contains only project-specific conventions. Do not repeat generic global rules here unless they need a stricter or more concrete interpretation.

---

## PHILOSOPHY

Code is written once but read many times. The goal is not to produce output that satisfies the immediate request — it is to produce a codebase that the next person (or future self) can understand, extend, and trust without fear. Working code that nobody can maintain is a liability, not an asset. Every change is an opportunity to leave the codebase slightly better than it was found.

---

## TYPESCRIPT

- MUST avoid `any`; use `unknown` and narrow it properly.
- MUST document unavoidable `any` usage with a short reason.
- MUST type function parameters and return values explicitly when the type is not obvious from local inference.
- MUST handle `null` and `undefined` intentionally.
- MUST prefer `type` for object shapes; use `interface` only when extension or declaration merging is needed.
- MUST type all `invoke()` calls explicitly using a generic or a typed wrapper — never leave them untyped.
- MUST type all React component props explicitly.
- SHOULD avoid non-null assertions (`!`).
- SHOULD avoid `as` casting unless there is no safer alternative.
- SHOULD keep types close to the feature that owns them.
- SHOULD extract shared types only after reuse is proven.

---

## RUST (BACKEND / CORE)

- MUST write idiomatic Rust; avoid unnecessary `clone()`, `unwrap()`, or `expect()` in production paths.
- MUST handle `Result` and `Option` explicitly; propagate errors with `?` instead of panicking.
- MUST use a consistent error type strategy for command errors returned to the frontend; document the choice.
- MUST keep Tauri commands thin: delegate business logic to separate modules, not inline in the command handler.
- MUST avoid blocking the async runtime; use `tokio::task::spawn_blocking` for CPU-heavy or blocking I/O work.
- MUST define explicit structs for command arguments and return values; avoid passing raw JSON blobs.
- MUST derive `serde::Deserialize` on command argument structs and `serde::Serialize` on response structs.
- SHOULD keep the Tauri entry point minimal — register commands and bootstrap only.
- SHOULD group related commands into feature modules rather than putting everything in one file.
- SHOULD avoid `unsafe` unless interfacing with FFI; document every `unsafe` block with a safety comment.
- SHOULD run `cargo clippy` and resolve all warnings before finalizing changes.

---

## QUALITY

- MUST prioritize quality code over merely working code: keep changes maintainable, reusable, typed, and verified.
- MUST keep source files at or below 300 lines unless the file is generated, declarative config, or a clearly justified exception.
- MUST read the entire file before splitting it — never split only the code being added without first understanding the full responsibility landscape of the existing file; the best extraction point may already exist elsewhere in the file.
- MUST when a file approaches or exceeds 300 lines, evaluate all existing responsibilities in the file and split along the most coherent boundary — not just isolate the new addition into a separate file.
- MUST remove obvious duplication during related edits by extracting shared components or utilities when reuse is already proven.
- MUST consider the surrounding feature/module before patching; modularize when a file accumulates too many responsibilities.
- MUST keep changes scoped to the requested behavior unless a small related refactor clearly improves correctness.
- SHOULD prefer small, behavior-preserving refactors over broad rewrites.
- SHOULD avoid clever abstractions before a real reuse pattern exists.

---

## TOOLCHAIN

- MUST use the Tauri CLI (`tauri dev`, `tauri build`) as the canonical development and build interface.
- MUST use Vite as the frontend bundler; do not replace or bypass it.
- MUST keep `tauri.conf.json` as the single source of truth for app identity, window config, and capabilities.
- SHOULD pin the Rust toolchain version when long-term build stability is required.
- SHOULD prefer Tauri plugins over custom native Rust code for common OS integrations (fs, shell, dialog, notification).
- SHOULD document clearly when a Tauri plugin is insufficient and custom Rust code is required.
- SHOULD avoid ejecting or bypassing Tauri's build pipeline without a documented reason.

---

## PROJECT STRUCTURE

- MUST follow the existing folder and file structure conventions already present in the codebase.
- MUST name files after what they export.
- MUST separate frontend code from Tauri backend code as established by the project.
- MUST keep IPC wrappers in a dedicated layer — never call `invoke` directly from components.
- SHOULD keep one component per file.
- SHOULD group code by feature rather than by technical type when the codebase has no established convention yet.
- SHOULD keep feature-specific logic inside the feature until reuse is proven.
- SHOULD move shared business logic into hooks or utilities instead of UI components.

---

## NAMING

- MUST use PascalCase for React components and TypeScript types.
- MUST use camelCase for variables, functions, and hooks.
- MUST use snake_case for Rust functions, variables, struct fields, and module names.
- MUST use PascalCase for Rust structs, enums, and traits.
- MUST use UPPER_SNAKE_CASE for constants in both Rust and TypeScript.
- MUST prefix boolean variables with `is`, `has`, or `can`.
- MUST prefix custom hooks with `use`.
- MUST name Tauri commands in snake_case on the Rust side; the frontend `invoke` string must match exactly.
- SHOULD name IPC wrapper functions by intent (e.g., `fetchUserProfile`, `saveSettings`), not by the raw command name.
- SHOULD name event handlers by intent: `handleSubmit`, `handleClose`, `handleRetry`.

---

## PLATFORM

- MUST assume Windows, macOS, and Linux can behave differently.
- MUST isolate platform-specific Rust behavior using `#[cfg(target_os = "...")]`.
- MUST isolate platform-specific frontend behavior using Tauri's `platform()` or OS detection utilities.
- MUST keep platform-sensitive behavior explicit and localized.
- SHOULD extract repeated platform branching into shared utilities.
- SHOULD verify behavior on all supported platforms when touching window management, tray, dialogs, or native modules.

---

## STYLING

- MUST use a shared design token system for colors, spacing, typography, and radius values.
- MUST NOT hardcode color values in components; use semantic CSS custom properties or the project's token system.
- MUST name tokens by use case, not by incidental color value (e.g., `--color-surface-primary`, not `--color-gray-100`).
- MUST deduplicate tokens when multiple variables share the same use case and value.
- SHOULD keep design tokens centralized in one place; do not scatter them across component files.
- SHOULD use the project's adopted styling system consistently; do not mix strategies.
- SHOULD avoid deeply nested component trees when a flatter layout is clearer.
- SHOULD avoid magic numbers unless documented or tied to a platform constraint.

---

## ACCESSIBILITY

- MUST provide accessible labels for interactive elements without visible text.
- MUST use appropriate ARIA roles for buttons, links, inputs, tabs, and toggles.
- MUST ensure interactive elements meet minimum click target size.
- MUST preserve readable text contrast through design tokens.
- MUST keep focus order logical and predictable.
- SHOULD provide ARIA hints when the action is not obvious from the label.
- SHOULD expose selected, disabled, expanded, and loading states to assistive technologies where relevant.

---

## COMPONENTS

- MUST keep components focused on presentation and interaction.
- MUST keep side effects out of render logic; use `useEffect` or event handlers.
- MUST prefer composition over prop-heavy mega components.
- MUST reuse existing components completely: match both visual styling and interaction behavior unless a deliberate variant is required.
- MUST wrap critical UI trees with React error boundaries to prevent full-app crashes.
- MUST show a fallback UI instead of a blank screen when a render error occurs.
- SHOULD extract reusable UI only after a clear reuse pattern exists.
- SHOULD split components when they start handling too many responsibilities.
- SHOULD keep loading, empty, error, and success states explicit.

---

## IPC AND COMMANDS

- MUST wrap all `invoke()` calls in typed frontend service functions; never call `invoke` directly from components.
- MUST type every `invoke` call with an explicit return type generic: `invoke<ResponseType>('command_name', args)`.
- MUST handle command errors on the frontend explicitly; never silently swallow rejected `invoke` promises.
- MUST keep command names unique and clearly scoped to their feature.
- MUST validate and sanitize all data from the frontend in Rust before acting on it.
- SHOULD keep Rust command handlers thin — validate input, call a service function, return a typed result.
- SHOULD not use `invoke` for high-frequency updates; use Tauri events for streaming or push data instead.
- SHOULD document non-obvious command contracts (side effects, required state, platform constraints).

---

## EVENTS

- MUST use Tauri's event system (`emit`, `listen`, `once`) for backend-to-frontend push communication.
- MUST call `unlisten()` when a component unmounts or the listener is no longer needed to prevent memory leaks.
- MUST type event payloads explicitly on both the Rust (`#[derive(Serialize)]`) and TypeScript sides.
- SHOULD prefer events over polling for real-time updates from the backend.
- SHOULD scope event names to their feature to avoid collisions (e.g., `download:progress`, `auth:logout`).

---

## WINDOW MANAGEMENT

- MUST configure initial window properties (size, decorations, resizability, title) in `tauri.conf.json`.
- MUST handle window close and focus events explicitly when the app has custom window behavior.
- MUST avoid creating multiple windows without a clear UX reason and documented lifecycle management.
- SHOULD persist window state (position, size) across sessions when the UX requires it.
- SHOULD handle the system tray lifecycle explicitly when a tray icon is used.

---

## STATE MANAGEMENT

- MUST keep state minimal and derive values when possible.
- MUST keep backend state, local UI state, and persisted storage state conceptually separate.
- MUST manage Tauri `State<T>` in Rust with thread-safe wrappers (`Mutex`, `RwLock`, or `Arc`) when shared across commands.
- MUST clean up subscriptions, listeners, and timers in `useEffect` cleanup functions.
- SHOULD use a global state solution only for truly global state; prefer local state first.
- SHOULD avoid storing large derived objects in component or global state.
- SHOULD cancel or ignore outdated async work during cleanup.

---

## STORAGE AND PERSISTENCE

- MUST use OS-appropriate app data directories via Tauri path APIs — never hardcode file paths.
- MUST not store sensitive data in plain app storage; use OS keychain or secure storage APIs.
- SHOULD use a Tauri-compatible persistence solution for user preferences and app state.
- SHOULD separate ephemeral session state from persistent data.
- SHOULD version persisted data schemas and handle migrations explicitly when the schema can change.

---

## SECURITY

- MUST configure the Content Security Policy (CSP) in `tauri.conf.json`; never disable it without a documented reason.
- MUST use Tauri's capability system (v2) or allowlist (v1) to grant only the permissions the app actually needs.
- MUST never expose arbitrary shell or filesystem access through commands unless absolutely required and sandboxed.
- MUST avoid passing unsanitized user input to OS APIs, shell commands, or file paths in Rust.
- MUST not bundle secrets, API keys, or credentials in the Vite frontend bundle.
- SHOULD keep sensitive logic on the Rust side; treat the frontend webview as untrusted.
- SHOULD audit IPC surface regularly: every exposed command is a potential attack vector.
- SHOULD keep the app's attack surface minimal: fewer capabilities, fewer commands, fewer open resources.

---

## PERFORMANCE

- MUST avoid blocking the main thread on the frontend.
- MUST prefer async Tauri commands for all I/O-bound work.
- MUST use `spawn_blocking` for CPU-heavy or synchronous Rust work that cannot be made async.
- MUST avoid unnecessary re-renders in frequently updated components.
- SHOULD use `React.memo`, `useMemo`, and `useCallback` only when there is a measured or obvious performance reason.
- SHOULD defer non-critical work until after initial render when possible.
- SHOULD prefer native OS APIs via Tauri plugins over JavaScript polyfills for performance-critical operations.
- SHOULD use Vite's code splitting and lazy imports for large feature modules.

---

## FORMS AND INPUT

- MUST keep form state and validation predictable and explicit.
- MUST show validation errors in a consistent location close to the relevant input.
- MUST handle submit states (loading, error, success) explicitly.
- SHOULD use a form library for complex forms with multiple fields and validation rather than managing state manually.
- SHOULD debounce or throttle inputs that trigger expensive operations (search, filter, IPC calls).
- SHOULD keep submit actions disabled while a submission is in flight.

---

## TESTING

- MUST add or update tests for critical business logic when behavior changes.
- MUST keep Rust unit tests close to the module under test using `#[cfg(test)]` blocks.
- MUST keep frontend tests focused on observable behavior, not implementation details.
- MUST cover loading, error, empty, and success states for critical features.
- SHOULD test Rust command logic independently from the Tauri runtime when possible.
- SHOULD test IPC wrappers and hooks separately from UI components when they contain meaningful logic.
- SHOULD avoid brittle snapshot tests unless they provide clear regression value.

---

## VERIFICATION

- MUST verify platform-sensitive flows on all supported OSes before shipping.
- MUST verify window behavior, tray icon, native dialogs, and file system access after meaningful changes.
- MUST verify loading, error, and offline states for features that depend on backend commands.
- MUST run `cargo clippy`, `cargo test`, `tsc --noEmit`, and `vite build` before finalizing substantial changes.
- SHOULD treat Rust compiler warnings and TypeScript errors as blockers, not noise.
- SHOULD run `tauri build` in a clean environment periodically to catch configuration drift.

---

## DYNAMIC RULES

- MUST update this file when user instructions conflict with existing rules and the new behavior is better.
- MUST NOT ignore recurring patterns that should become rules.
- MUST keep updates minimal and actionable.
- MUST NOT add vague, redundant, or one-off rules.
- MUST remove or revise rules that become harmful, obsolete, or inconsistent with the project.