"""Sync skills/global/* into installed CLI skill directories."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import DeployConfig, Target


@dataclass
class SyncLine:
    target: str
    ok: bool
    message: str


def list_global_skills(cfg: DeployConfig) -> list[str]:
    if not cfg.skills_global.is_dir():
        return []
    return sorted(
        p.name for p in cfg.skills_global.iterdir() if p.is_dir() and not p.name.startswith(".")
    )


def sync_skills(cfg: DeployConfig, skill_names: list[str] | None = None) -> list[SyncLine]:
    if not cfg.skills_global.is_dir():
        raise FileNotFoundError(f"skills directory not found: {cfg.skills_global}")

    names = skill_names if skill_names is not None else list_global_skills(cfg)
    if not names:
        raise FileNotFoundError(f"no skills found in {cfg.skills_global}")

    results: list[SyncLine] = []
    for name in names:
        source = cfg.skills_global / name
        if not source.is_dir():
            raise FileNotFoundError(f"skill not found: {source}")
        for t in cfg.targets:
            results.append(_copy_skill(t, name, source))
    return results


def _copy_skill(target: Target, name: str, source: Path) -> SyncLine:
    if not target.installed:
        return SyncLine(target.name, False, f"[{name}] skip (home not found: {target.home})")

    dest = target.skills / name
    dest.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        dst = dest / item.name
        if item.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)
    return SyncLine(target.name, True, f"[{name}] -> {dest}")
