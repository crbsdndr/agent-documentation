"""Merge managed MCP server fragments into CLI config files (TOML & JSON)."""

from __future__ import annotations

import json
import os
import re
import shutil
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import DeployConfig, Target
from .dotenv import load_dotenv
from . import jsonc


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
    if target.mcp_format == "jsonc":
        return _sync_jsonc_target(cfg, target, names)
    if target.mcp_format == "json":
        return _sync_json_target(cfg, target, names)
    return _sync_toml_target(cfg, target, managed_block, names)


def _sync_toml_target(
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


def _sync_json_target(
    cfg: DeployConfig,
    target: Target,
    names: list[str],
) -> SyncLine:
    if not target.installed:
        return SyncLine(target.name, False, f"skip (home not found: {target.home})")

    backup_str = ""
    if target.mcp_config.is_file():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = Path(str(target.mcp_config) + f".bak-pre-mcp-sync-{stamp}")
        shutil.copy2(target.mcp_config, backup)
        backup_str = f" (backup: {backup.name})"
        try:
            current_data = json.loads(target.mcp_config.read_text(encoding="utf-8"))
        except Exception:
            current_data = {}
    else:
        target.mcp_config.parent.mkdir(parents=True, exist_ok=True)
        current_data = {}

    if not isinstance(current_data, dict):
        current_data = {}

    mcp_servers = current_data.get("mcpServers")
    if not isinstance(mcp_servers, dict):
        mcp_servers = {}

    for name in names:
        path = cfg.mcp_servers / f"{name}.toml"
        raw = path.read_text(encoding="utf-8")
        parsed = tomllib.loads(raw)
        server_info = parsed.get("mcp_servers", {}).get(name, {})

        srv_dict = {}
        for k, v in server_info.items():
            if k in ("command", "args", "env", "serverUrl", "disabled", "autoApprove"):
                srv_dict[k] = v

        for key in cfg.env_inject.get(name, []):
            val = os.environ.get(key)
            if val:
                env_dict = srv_dict.setdefault("env", {})
                env_dict[key] = val

        mcp_servers[name] = srv_dict

    current_data["mcpServers"] = mcp_servers
    target.mcp_config.write_text(json.dumps(current_data, indent=2) + "\n", encoding="utf-8")
    return SyncLine(target.name, True, f"-> {target.mcp_config}{backup_str}")


def _sync_jsonc_target(
    cfg: DeployConfig,
    target: Target,
    names: list[str],
) -> SyncLine:
    if not target.installed:
        return SyncLine(target.name, False, f"skip (home not found: {target.home})")
    if not target.mcp_config.is_file():
        return SyncLine(target.name, False, f"skip (config not found: {target.mcp_config})")

    current = target.mcp_config.read_text(encoding="utf-8")
    if not jsonc.is_valid(current):
        return SyncLine(
            target.name,
            False,
            f"abort (existing config is not valid JSONC: {target.mcp_config})",
        )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = Path(str(target.mcp_config) + f".bak-pre-mcp-sync-{stamp}")
    shutil.copy2(target.mcp_config, backup)

    try:
        next_text = _apply_jsonc_sync(cfg, current, names)
    except ValueError as e:
        return SyncLine(
            target.name,
            False,
            f"abort ({e}; config unchanged, backup: {backup.name})",
        )

    target.mcp_config.write_text(next_text, encoding="utf-8", newline="\n")
    return SyncLine(target.name, True, f"-> {target.mcp_config} (backup: {backup.name})")


def _apply_jsonc_sync(cfg: DeployConfig, text: str, names: list[str]) -> str:
    text = jsonc.remove_block(text, cfg.jsonc_mcp_start, cfg.jsonc_mcp_end)
    entries = [_opencode_entry(cfg, name) for name in names]

    span = jsonc.object_span(text, "mcp")
    if span is None:
        close = jsonc.top_level_close(text)
        if close < 0:
            raise ValueError("no top-level object found in config")
        block = jsonc.build_block(cfg.jsonc_mcp_start, cfg.jsonc_mcp_end, entries, False)
        text = jsonc.insert_key_before_close(text, close, "mcp", block)
    else:
        text = jsonc.remove_named_entries(text, span, names)
        text = jsonc.fix_trailing_commas(text)
        span = jsonc.object_span(text, "mcp")
        if span is None:
            raise ValueError("mcp object lost during merge")
        open_i, _ = span
        rest = text[open_i + 1 :].lstrip(" \t\r\n")
        needs_comma = not rest.startswith("}")
        block = jsonc.build_block(
            cfg.jsonc_mcp_start, cfg.jsonc_mcp_end, entries, needs_comma
        )
        text = jsonc.insert_after_brace(text, open_i, block)

    if not jsonc.is_valid(text):
        raise ValueError("merge produced invalid JSONC")
    return text


def _opencode_entry(cfg: DeployConfig, name: str) -> str:
    path = cfg.mcp_servers / f"{name}.toml"
    raw = path.read_text(encoding="utf-8")
    parsed = tomllib.loads(raw)
    info = parsed.get("mcp_servers", {}).get(name, {})

    command = [str(info["command"])]
    args = info.get("args") or []
    if isinstance(args, str):
        args = [args]
    command.extend(str(a) for a in args)

    entry: dict = {"type": "local"}
    if command:
        entry["command"] = command
    if "enabled" in info:
        entry["enabled"] = bool(info["enabled"])
    if info.get("startup_timeout_sec"):
        entry["timeout"] = int(info["startup_timeout_sec"]) * 1000
    for key in cfg.env_inject.get(name, []):
        val = os.environ.get(key)
        if val:
            entry.setdefault("environment", {})[key] = val
    return f'"{name}": ' + json.dumps(entry, indent=2)

