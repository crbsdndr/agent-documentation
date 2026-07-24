"""Load central deploy.toml and resolve paths."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ is required (stdlib tomllib).")

import tomllib


@dataclass(frozen=True)
class Target:
    name: str
    id: str
    home: Path
    agents: Path
    skills: Path
    mcp_config: Path

    @property
    def installed(self) -> bool:
        return self.home.is_dir()


@dataclass(frozen=True)
class DeployConfig:
    repo_root: Path
    agents_global: Path
    skills_global: Path
    mcp_servers: Path
    env_file: Path
    mcp_start: str
    mcp_end: str
    env_inject: dict[str, list[str]] = field(default_factory=dict)
    targets: list[Target] = field(default_factory=list)


def _expand(path_str: str) -> Path:
    return Path(os.path.expanduser(path_str)).resolve()


def repo_root_from_here() -> Path:
    # scripts/lib/config.py -> scripts/lib -> scripts -> repo root
    return Path(__file__).resolve().parent.parent.parent


def load_config(repo_root: Path | None = None) -> DeployConfig:
    root = (repo_root or repo_root_from_here()).resolve()
    path = root / "deploy.toml"
    if not path.is_file():
        raise FileNotFoundError(f"deploy.toml not found: {path}")

    with path.open("rb") as f:
        raw = tomllib.load(f)

    paths = raw.get("paths") or {}
    markers = raw.get("markers") or {}
    mcp = raw.get("mcp") or {}
    env_inject = {
        str(k): [str(x) for x in v]
        for k, v in (mcp.get("env_inject") or {}).items()
    }

    targets: list[Target] = []
    for t in raw.get("targets") or []:
        targets.append(
            Target(
                name=str(t["name"]),
                id=str(t["id"]),
                home=_expand(str(t["home"])),
                agents=_expand(str(t["agents"])),
                skills=_expand(str(t["skills"])),
                mcp_config=_expand(str(t["mcp_config"])),
            )
        )

    return DeployConfig(
        repo_root=root,
        agents_global=(root / str(paths.get("agents_global", "agents/global/AGENTS.md"))).resolve(),
        skills_global=(root / str(paths.get("skills_global", "skills/global"))).resolve(),
        mcp_servers=(root / str(paths.get("mcp_servers", "mcp/servers"))).resolve(),
        env_file=(root / str(paths.get("env_file", ".env"))).resolve(),
        mcp_start=str(markers.get("mcp_start", "# --- agent-documentation:mcp:start ---")),
        mcp_end=str(markers.get("mcp_end", "# --- agent-documentation:mcp:end ---")),
        env_inject=env_inject,
        targets=targets,
    )
