#!/usr/bin/env python3
"""Deploy agents, skills, and MCP configs to Grok Build + Codex.

Usage:
  python scripts/sync.py              # interactive TUI
  python scripts/sync.py status
  python scripts/sync.py agents
  python scripts/sync.py skills [name|all]
  python scripts/sync.py mcp
  python scripts/sync.py all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python scripts/sync.py` without installing a package.
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.agents import sync_agents  # noqa: E402
from lib.config import load_config  # noqa: E402
from lib.mcp import sync_mcp  # noqa: E402
from lib.skills import sync_skills  # noqa: E402
from lib.status import collect_status  # noqa: E402
from lib.tui import run_tui  # noqa: E402


_META = frozenset({"env", "servers", "inject"})


def _print_results(title: str, results) -> int:
    print(title)
    for r in results:
        mark = "ok" if r.ok else ".."
        print(f"  [{mark}] {r.target}: {r.message}")
    # Meta lines (env load, server list, inject status) are not target writes.
    target_rows = [r for r in results if r.target not in _META]
    target_ok = sum(1 for r in target_rows if r.ok)
    if target_rows and target_ok == 0:
        print("error: no installed CLI targets synced")
        return 1
    print(f"Done. ({target_ok} target write(s))")
    return 0


def cmd_agents(cfg) -> int:
    try:
        results = sync_agents(cfg)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return _print_results("Syncing global AGENTS.md", results)


def cmd_skills(cfg, skill_names=None) -> int:
    try:
        results = sync_skills(cfg, skill_names=skill_names)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    label = "all" if skill_names is None else ", ".join(skill_names)
    return _print_results(f"Syncing global skills ({label})", results)


def cmd_mcp(cfg) -> int:
    try:
        results = sync_mcp(cfg)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    code = _print_results("Syncing managed MCP servers", results)
    if code == 0:
        print("Restart Codex / Grok sessions so MCP reloads.")
    return code


def cmd_all(cfg) -> int:
    for fn in (cmd_agents, lambda c: cmd_skills(c, None), cmd_mcp):
        code = fn(cfg)
        if code != 0:
            return code
        print()
    return 0


def cmd_status(cfg) -> int:
    for line in collect_status(cfg):
        print(line)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Deploy agent-documentation to Grok Build + Codex only.",
    )
    p.add_argument(
        "command",
        nargs="?",
        choices=["agents", "skills", "mcp", "all", "status", "tui"],
        help="Action to run. Omit or use tui for interactive menu.",
    )
    p.add_argument(
        "skill",
        nargs="?",
        default="all",
        help="For skills: skill name or 'all' (default: all).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config()
    except (FileNotFoundError, SystemExit) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if not cfg.targets:
        print("error: no targets in deploy.toml", file=sys.stderr)
        return 1

    command = args.command
    if command is None or command == "tui":
        return run_tui(
            cfg,
            {
                "agents": cmd_agents,
                "skills": cmd_skills,
                "mcp": cmd_mcp,
                "all": cmd_all,
                "status": cmd_status,
            },
        )

    if command == "status":
        return cmd_status(cfg)
    if command == "agents":
        return cmd_agents(cfg)
    if command == "skills":
        names = None if args.skill == "all" else [args.skill]
        return cmd_skills(cfg, skill_names=names)
    if command == "mcp":
        return cmd_mcp(cfg)
    if command == "all":
        return cmd_all(cfg)

    print(f"error: unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
