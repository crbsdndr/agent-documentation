Projek ini adalah projek untuk menyimpan berbagai dokumentasi AGENTS.md dan Agents skill untuk keperluan aplikasi saya nantinya.

## Global AGENTS Deploy

Source of truth: [`AGENTS - GLOBAL.md`](AGENTS%20-%20GLOBAL.md)

```bash
./scripts/sync-global-agents.sh
```

| Platform | Path |
|----------|------|
| Grok Build CLI | `~/.grok/AGENTS.md` |
| Cursor | `~/.cursor/AGENTS.md` |
| Codex | `~/.codex/AGENTS.md` |
| Kimi Code | `~/.kimi-code/AGENTS.md` |
| OpenClaw | `~/.openclaw/workspace/AGENTS.md` (merged, bootstrap tetap) |

## Global Skills Deploy

Source of truth untuk skill global ada di `skills/global/<skill-name>/`.

Sync ke semua CLI (user-global):

| Platform | Path |
|----------|------|
| Grok Build CLI | `~/.grok/skills/<skill>/` |
| Cursor | `~/.cursor/skills/<skill>/` |
| Codex | `~/.codex/skills/<skill>/` |
| OpenClaw | `~/.openclaw/skills/<skill>/` |
| Kimi Code | `~/.kimi-code/skills/<skill>/` |

```bash
./scripts/sync-global-skills.sh git-commit
./scripts/sync-global-skills.sh all
```

Setelah sync, buka session baru agar skill terdeteksi:
- **Codex** — restart CLI/session
- **Kimi Code** — `/new` atau restart
- **Grok / Cursor / OpenClaw** — session baru biasanya cukup