"""Status / dry inspection of deploy targets."""

from __future__ import annotations

from .config import DeployConfig
from .mcp import managed_server_names
from .skills import list_global_skills


def collect_status(cfg: DeployConfig) -> list[str]:
    lines: list[str] = []
    lines.append(f"repo: {cfg.repo_root}")
    lines.append(f"agents source: {cfg.agents_global} ({'ok' if cfg.agents_global.is_file() else 'MISSING'})")
    skills = list_global_skills(cfg)
    lines.append(
        f"skills source: {cfg.skills_global} ({len(skills)}: {', '.join(skills) or 'none'})"
    )
    servers = managed_server_names(cfg)
    lines.append(
        f"mcp source: {cfg.mcp_servers} ({len(servers)}: {', '.join(servers) or 'none'})"
    )
    lines.append(f"env file: {cfg.env_file} ({'ok' if cfg.env_file.is_file() else 'missing'})")
    lines.append("")
    lines.append("targets (Codex + Grok Build only):")
    for t in cfg.targets:
        home = "installed" if t.installed else "NOT installed"
        agents = "present" if t.agents.is_file() else "absent"
        mcp = "present" if t.mcp_config.is_file() else "absent"
        lines.append(
            f"  - {t.name} [{t.id}]: home={home}; agents={agents}; mcp_config={mcp}"
        )
        lines.append(f"      home={t.home}")
    return lines
