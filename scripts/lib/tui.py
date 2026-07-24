"""Interactive terminal menu for deploy actions."""

from __future__ import annotations

from .config import DeployConfig
from .skills import list_global_skills
from .status import collect_status


def print_header(cfg: DeployConfig) -> None:
    print()
    print("agent-documentation deploy")
    print("=" * 32)
    for t in cfg.targets:
        mark = "OK" if t.installed else "--"
        print(f"  [{mark}] {t.name}  ({t.home})")
    print()


def run_tui(cfg: DeployConfig, handlers: dict) -> int:
    """
    handlers keys:
      agents, skills, mcp, all, status
    Each is callable(cfg, **kwargs) -> int exit code
    """
    while True:
        print_header(cfg)
        print("  1) Sync AGENTS.md")
        print("  2) Sync skills")
        print("  3) Sync MCP servers")
        print("  4) Sync everything")
        print("  5) Status")
        print("  0) Quit")
        print()
        choice = input("Select> ").strip().lower()

        if choice in ("0", "q", "quit", "exit"):
            print("Bye.")
            return 0
        if choice == "1":
            code = handlers["agents"](cfg)
            if code != 0:
                return code
            continue
        if choice == "2":
            skill = _pick_skill(cfg)
            if skill is None:
                continue
            names = None if skill == "all" else [skill]
            code = handlers["skills"](cfg, skill_names=names)
            if code != 0:
                return code
            continue
        if choice == "3":
            code = handlers["mcp"](cfg)
            if code != 0:
                return code
            continue
        if choice == "4":
            code = handlers["all"](cfg)
            if code != 0:
                return code
            continue
        if choice == "5":
            for line in collect_status(cfg):
                print(line)
            print()
            input("Press Enter to continue...")
            continue

        print("Unknown choice. Try again.")


def _pick_skill(cfg: DeployConfig) -> str | None:
    skills = list_global_skills(cfg)
    print()
    print("  Skills:")
    print("    0) all")
    for i, name in enumerate(skills, start=1):
        print(f"    {i}) {name}")
    print("    c) cancel")
    raw = input("Skill> ").strip().lower()
    if raw in ("c", "cancel", ""):
        return None
    if raw in ("0", "all"):
        return "all"
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(skills):
            return skills[idx - 1]
    if raw in skills:
        return raw
    print(f"Unknown skill: {raw}")
    return None
