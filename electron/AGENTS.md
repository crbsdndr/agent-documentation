# AGENTS.md — Electron

Electron-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

---

## TYPESCRIPT RULES

- Never use `any` — use `unknown` and narrow the type if needed.
- Avoid non-null assertions (`!`) — handle nullability explicitly.
- Always type function return values explicitly.
- Use `type` for object shapes, `interface` only when extending.
- Never cast with `as` unless absolutely necessary.

## ARCHITECTURE RULES

- Always maintain strict separation between **main process** and **renderer process** — they run in different environments.
- Main process handles: OS integration, file system, native APIs, app lifecycle.
- Renderer process handles: UI only — treat it like a sandboxed browser.
- Never share mutable state directly between processes — always communicate via IPC.

## SECURITY RULES

- Always set `contextIsolation: true` and `nodeIntegration: false` in `BrowserWindow` — no exceptions.
- Never expose Node.js APIs directly to the renderer — use `contextBridge` to expose only what's needed.
- Always validate and sanitize data received via IPC — never trust renderer input blindly.
- Never load remote URLs in `BrowserWindow` without explicit `Content-Security-Policy`.
- Always use `shell.openExternal()` for opening external URLs — never load them in the app window.

## IPC RULES

- Always use `ipcMain.handle` and `ipcRenderer.invoke` for request/response patterns — avoid `send`/`on` for two-way communication.
- Define all IPC channel names as constants in a shared `@/constants/ipc-channels.ts` file.
- Always type IPC payloads — never pass untyped objects between processes.
- Keep IPC handlers lean — delegate business logic to separate modules, not inside handlers.

## NAMING CONVENTION

- **Components** → PascalCase (`UserCard.tsx`)
- **Files & folders** → kebab-case (`user-card.ts`, `ipc-handlers.ts`)
- **Variables & functions** → camelCase (`getUserData`)
- **Constants** → UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **IPC channels** → `domain:action` pattern (`window:minimize`, `file:open`, `app:quit`)
- **Boolean variables** → prefix with `is`, `has`, or `can` (`isLoading`, `hasError`)

## MODULARITY RULES

- Keep main process code modular — split by domain (`window-manager.ts`, `tray.ts`, `updater.ts`).
- Never put all main process logic in `main.ts` — it should only be the entry point.
- Separate concerns: IPC handlers, business logic, and OS integrations in their own modules.

## PERFORMANCE RULES

- Lazy load `BrowserWindow` — never create windows before the `app.ready` event.
- Always destroy windows explicitly when they're no longer needed to free memory.
- Avoid blocking the main process — offload heavy tasks to worker threads or child processes.
- Use `webContents.setBackgroundThrottling(false)` only when strictly necessary.

## ERROR HANDLING RULES

- Always handle `uncaughtException` and `unhandledRejection` in the main process.
- Never let IPC handlers throw unhandled errors — always wrap in try/catch and return structured error responses.
- Log errors with enough context for debugging — include process name (main/renderer).

## NATIVE & OS RULES

- Always check `process.platform` before using platform-specific APIs (`darwin`, `win32`, `linux`).
- Use `app.getPath()` for user data, temp, and app directories — never hardcode paths.
- Always request OS permissions (notifications, file access) gracefully — handle denial without crashing.

## VERIFICATION RULES

- After changes, always verify using the project's available scripts:
  - Lint — check for linting errors
  - Typecheck — verify no TypeScript errors
  - Build — verify the app packages correctly for the target platform

## MEMORY RULES

- Always remove IPC listeners when a window is closed — use `ipcMain.removeHandler()` and `ipcMain.removeAllListeners()`.
- Always clean up `app`, `webContents`, and `BrowserWindow` event listeners on destroy.
- Never register the same IPC handler more than once — check before registering or remove first.