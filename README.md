# agent-documentation

Source of truth for AGENTS.md rules, agent skills, and managed MCP servers used by **Grok Build CLI**, **Codex**, **Antigravity**, **Devin**, and **OpenCode**.

## Structure

```text
agent-documentation/
├── deploy.toml                   # Central deploy config (targets, paths, MCP env inject)
├── agents/
│   ├── global/AGENTS.md          # CLI-wide rules
│   └── stacks/<stack>/AGENTS.md  # Framework / platform rules
├── mcp/
│   └── servers/*.toml            # Managed MCP server definitions
├── skills/
│   ├── global/<skill>/           # CLI-wide skills (synced)
│   ├── domain/<skill>/           # Shared domain skills (not auto-synced)
│   └── apps/<app>/<skill>/       # App-specific skills (not auto-synced)
├── scripts/
│   ├── sync.py                   # Deploy entrypoint (TUI + CLI)
│   └── lib/                      # Python modules
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

## Requirements

- **Python 3.11+** (stdlib only: `tomllib`, no pip packages)
- Grok Build, Codex, Antigravity, Devin, and/or OpenCode installed (home folder exists)

## Deploy (Python only)

Central config: [`deploy.toml`](deploy.toml) — targets, paths, MCP markers, and env-key injection.

Supported harnesses:

| Platform | Home | Agents | Skills | MCP config |
|----------|------|--------|--------|------------|
| Grok Build CLI | `~/.grok` | `~/.grok/AGENTS.md` | `~/.grok/skills/` | `~/.grok/config.toml` |
| Codex | `~/.codex` | `~/.codex/AGENTS.md` | `~/.codex/skills/` | `~/.codex/config.toml` |
| Antigravity | `~/.gemini` | `~/.gemini/AGENTS.md` | `~/.gemini/config/plugins/global-skills/skills/` | `~/.gemini/config/mcp_config.json` |
| Devin (Linux/macOS) | `~/.config/devin` | `~/.config/devin/AGENTS.md` | `~/.config/devin/skills/` | `~/.config/devin/config.json` |
| Devin (Windows) | `%APPDATA%\devin` | `%APPDATA%\devin\AGENTS.md` | `%APPDATA%\devin\skills\` | `%APPDATA%\devin\config.json` |
| OpenCode | `~/.config/opencode` | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills/` | `~/.config/opencode/opencode.jsonc` |

Scripts **skip** targets whose home (or MCP config file) does not exist. They never create tool homes.

### Interactive TUI

```bash
python scripts/sync.py
```

Menu: sync agents / skills / MCP / everything / status / quit.

### CLI

```bash
python scripts/sync.py status
python scripts/sync.py agents
python scripts/sync.py skills              # all global skills
python scripts/sync.py skills git-commit
python scripts/sync.py mcp
python scripts/sync.py all
```

Windows (PowerShell):

```powershell
python scripts\sync.py
python scripts\sync.py all
```

After sync, open a new session so tools reload agents / skills / MCP.

## Global MCP

Source: [`mcp/servers/*.toml`](mcp/servers/)

Each file is a TOML fragment for one managed server. Sync merges them into TOML configs (`config.toml`), JSON configs (`mcp_config.json`), or JSONC configs (`opencode.jsonc`) inside managed markers / structures.

### MCP merge rules (by server name)

1. Load secrets from repo-root `.env` (gitignored).
2. Remove the previous managed marker block (for TOML and JSONC) or update `mcpServers` object (for JSON).
3. Remove any existing `[mcp_servers.<name>]` / nested sections (TOML), `mcpServers.<name>` entries (JSON), or `mcp.<name>` entries (JSONC) for **managed** names only.
4. Append/insert fresh managed configuration for every `mcp/servers/*.toml`.
5. Inject env keys declared in `deploy.toml` → `[mcp.env_inject]` when present in `.env`.

For OpenCode (`opencode.jsonc`), the managed servers live in a `// --- agent-documentation:mcp:start ---` / `...:end ---` marker block inside the `mcp` object; `command`/`args` are transformed into the opencode `command` array and `startup_timeout_sec` into `timeout` (ms). Unmanaged keys (for example `$schema`, `plugin`, or other MCP names like `ast-grep`) are preserved.

Same name = **overwrite** (flags/args always replaced). Unmanaged servers (for example Codex `node_repl`) are left alone. Re-runs are safe (no duplicates). Every write is validated before it lands (JSONC must still parse after stripping comments); existing configs and AGENTS.md files are backed up (`*.bak-pre-*-sync-<ts>`) before overwriting.

Notes:

- **Must** keep secrets out of git. Put keys in `.env` (see `.env.example`).
- Injected keys are written only into local CLI `config.toml` / `mcp_config.json`, never into `mcp/servers/*.toml`.
- Restart Codex / Grok / Antigravity / Devin / OpenCode after MCP sync. Verify OpenCode with `opencode mcp list`.

Current managed servers:

| Server | Purpose |
|--------|---------|
| `chrome-devtools` | Browser debug/automation (`chrome-devtools-mcp@1.6.0`) |
| `codegraph` | Local project code graph (`codegraph serve --mcp`) |
| `context7` | Up-to-date library docs (`@upstash/context7-mcp`) |

## Conventions

- **Must** keep global CLI deploy limited to `agents/global`, `skills/global`, and `mcp/servers`.
- **Must** keep deploy targets configured in `deploy.toml`.
- **Must** use `AGENTS.md` / `SKILL.md` names only (no platform prefixes).
- **Must** add new managed MCP servers as `mcp/servers/<name>.toml`, then run `python scripts/sync.py mcp`.
- **Must** declare secret inject keys in `deploy.toml` `[mcp.env_inject]` when a server needs them.
- **Should** add new stacks under `agents/stacks/<stack>/`.
- **Should** put shared non-CLI skills under `skills/domain/`.
- **Should** put product-specific skills under `skills/apps/<app>/`.
- **Should** use `*_windows` path overrides in `deploy.toml` when a target uses different paths on Windows (e.g. `home_windows`, `mcp_config_windows`).

