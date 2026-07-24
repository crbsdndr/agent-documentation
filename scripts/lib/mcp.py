"""Merge managed MCP server fragments into CLI config.toml files."""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import DeployConfig, Target
from .dotenv import load_dotenv


@dataclass
class SyncLine:
    target: str
    ok: bool
    message: str


def managed_server_names(cfg: DeployConfig) -> list[str]:
    if not cfg.mcp_servers.is_dir():
        return []
    return sorted(
        p.stem for p in cfg.mcp_servers.glob("*.toml") if p.is_file()
    )


def sync_mcp(cfg: DeployConfig) -> list[SyncLine]:
    if not cfg.mcp_servers.is_dir():
        raise FileNotFoundError(f"servers directory not found: {cfg.mcp_servers}")

    names = managed_server_names(cfg)
    if not names:
        raise FileNotFoundError(f"no server definitions in {cfg.mcp_servers}")

    loaded = load_dotenv(cfg.env_file)
    block = build_managed_block(cfg, names)

    results: list[SyncLine] = []
    results.append(
        SyncLine(
            "env",
            True,
            f"loaded .env ({loaded} key(s))" if loaded else ".env: not found (optional)",
        )
    )
    results.append(SyncLine("servers", True, ", ".join(names)))

    for server, keys in cfg.env_inject.items():
        if server not in names:
            continue
        present = [k for k in keys if os.environ.get(k)]
        missing = [k for k in keys if not os.environ.get(k)]
        if present:
            results.append(
                SyncLine("inject", True, f"{server}: {', '.join(present)} present")
            )
        if missing:
            results.append(
                SyncLine(
                    "inject",
                    True,
                    f"{server}: {', '.join(missing)} not set (optional)",
                )
            )


    for t in cfg.targets:
        results.append(_sync_target(cfg, t, block, names))
    return results


def build_managed_block(cfg: DeployConfig, names: list[str]) -> str:
    lines = [
        cfg.mcp_start,
        "# Managed by agent-documentation scripts/sync.py — do not edit by hand.",
        "# Source: mcp/servers/*.toml",
        "",
    ]
    for name in names:
        body = _server_body(cfg, name)
        lines.extend(body.splitlines())
        lines.append("")
    lines.append(cfg.mcp_end)
    return "\n".join(lines) + "\n"


def _server_body(cfg: DeployConfig, name: str) -> str:
    path = cfg.mcp_servers / f"{name}.toml"
    raw = path.read_text(encoding="utf-8")
    body_lines = []
    for line in raw.splitlines():
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        body_lines.append(line)
    body = "\n".join(body_lines).rstrip()

    for key in cfg.env_inject.get(name, []):
        value = os.environ.get(key)
        if not value:
            continue
        env_header = f"[mcp_servers.{name}.env]"
        if env_header in body:
            continue
        body = f'{body}\n\n{env_header}\n{key} = "{value}"'
    return body


def remove_managed_sections(content: str, cfg: DeployConfig, names: list[str]) -> str:
    start, end = cfg.mcp_start, cfg.mcp_end
    if start in content and end in content:
        pattern = re.escape(start) + r"[\s\S]*?" + re.escape(end) + r"\r?\n?"
        content = re.sub(pattern, "", content)

    for name in names:
        # Remove [mcp_servers.name] and nested [mcp_servers.name.*]
        pattern = (
            rf"(?m)^\[mcp_servers\.{re.escape(name)}(?:\.[^\]]+)?\][^\n]*\r?\n"
            rf"(?:(?!^\[).*\r?\n)*"
        )
        content = re.sub(pattern, "", content)

    return content.rstrip() + "\n"


def _sync_target(
    cfg: DeployConfig,
    target: Target,
    managed_block: str,
    names: list[str],
) -> SyncLine:
    if not target.installed:
        return SyncLine(target.name, False, f"skip (home not found: {target.home})")
    if not target.mcp_config.is_file():
        return SyncLine(target.name, False, f"skip (config not found: {target.mcp_config})")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = Path(str(target.mcp_config) + f".bak-pre-mcp-sync-{stamp}")
    shutil.copy2(target.mcp_config, backup)

    current = target.mcp_config.read_text(encoding="utf-8")
    cleaned = remove_managed_sections(current, cfg, names)
    next_text = cleaned.rstrip() + "\n\n" + managed_block
    target.mcp_config.write_text(next_text, encoding="utf-8", newline="\n")

    return SyncLine(target.name, True, f"-> {target.mcp_config} (backup: {backup.name})")
