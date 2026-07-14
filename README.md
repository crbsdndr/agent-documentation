# agent-documentation

Source of truth for AGENTS.md rules and agent skills used across CLI tools and app stacks.

## Structure

```text
agent-documentation/
├── agents/
│   ├── global/AGENTS.md          # CLI-wide rules (synced to ~/.grok, etc.)
│   └── stacks/<stack>/AGENTS.md  # Framework / platform rules
├── skills/
│   ├── global/<skill>/           # CLI-wide skills (synced)
│   ├── domain/<skill>/           # Shared domain skills (not auto-synced)
│   └── apps/<app>/<skill>/       # App-specific skills (not auto-synced)
├── scripts/                      # Deploy helpers for global agents & skills
└── README.md
```

### Naming

| Kind | Path | Filename |
|------|------|----------|
| Global agents | `agents/global/` | `AGENTS.md` |
| Stack agents | `agents/stacks/<stack>/` | `AGENTS.md` |
| Global skill | `skills/global/<name>/` | `SKILL.md` |
| Domain skill | `skills/domain/<name>/` | `SKILL.md` |
| App skill | `skills/apps/<app>/<name>/` | `SKILL.md` |

### Stacks

| Stack | Path |
|-------|------|
| Electron | `agents/stacks/electron/AGENTS.md` |
| Laravel | `agents/stacks/laravel/AGENTS.md` |
| Next.js | `agents/stacks/nextjs/AGENTS.md` |
| Plasmo | `agents/stacks/plasmo/AGENTS.md` |
| React Native | `agents/stacks/react-native/AGENTS.md` |
| Tauri | `agents/stacks/tauri/AGENTS.md` |
| WXT | `agents/stacks/wxt/AGENTS.md` |

### Skills layout

| Scope | Path | Auto-sync |
|-------|------|-----------|
| Global | `skills/global/*` | Yes → CLI homes |
| Domain | `skills/domain/*` | No (copy when needed) |
| App | `skills/apps/<app>/*` | No (copy when needed) |

## Global AGENTS deploy

Source: [`agents/global/AGENTS.md`](agents/global/AGENTS.md)

```bash
# macOS / Linux
./scripts/sync-global-agents.sh

# Windows (PowerShell)
.\scripts\sync-global-agents.ps1
```

| Platform | Path |
|----------|------|
| Grok Build CLI | `~/.grok/AGENTS.md` |
| Cursor | `~/.cursor/AGENTS.md` |
| Codex | `~/.codex/AGENTS.md` |
| Kimi Code | `~/.kimi-code/AGENTS.md` |
| OpenClaw | `~/.openclaw/workspace/AGENTS.md` (merged, bootstrap kept) |

## Global skills deploy

Source: `skills/global/<skill-name>/`

| Platform | Path |
|----------|------|
| Grok Build CLI | `~/.grok/skills/<skill>/` |
| Cursor | `~/.cursor/skills/<skill>/` |
| Codex | `~/.codex/skills/<skill>/` |
| OpenClaw | `~/.openclaw/skills/<skill>/` |
| Kimi Code | `~/.kimi-code/skills/<skill>/` |

```bash
# macOS / Linux
./scripts/sync-global-skills.sh git-commit
./scripts/sync-global-skills.sh all

# Windows (PowerShell)
.\scripts\sync-global-skills.ps1 git-commit
.\scripts\sync-global-skills.ps1 all
```

After sync, open a new session so tools reload skills:

- **Codex** — restart CLI/session
- **Kimi Code** — `/new` or restart
- **Grok / Cursor / OpenClaw** — new session is usually enough

## Conventions

- **Must** keep global CLI deploy limited to `agents/global` and `skills/global`.
- **Must** use `AGENTS.md` / `SKILL.md` names only (no platform prefixes).
- **Should** add new stacks under `agents/stacks/<stack>/`.
- **Should** put shared non-CLI skills under `skills/domain/`.
- **Should** put product-specific skills under `skills/apps/<app>/`.
