"""Sync agents/global/AGENTS.md to installed CLI homes."""

from __future__ import annotations

import shutil
from dataclasses import dataclass

from .config import DeployConfig, Target


@dataclass
class SyncLine:
    target: str
    ok: bool
    message: str


def sync_agents(cfg: DeployConfig) -> list[SyncLine]:
    if not cfg.agents_global.is_file():
        raise FileNotFoundError(f"source not found: {cfg.agents_global}")

    results: list[SyncLine] = []
    for t in cfg.targets:
        results.append(_copy_one(t, cfg.agents_global))
    return results


def _copy_one(target: Target, source) -> SyncLine:
    if not target.installed:
        return SyncLine(target.name, False, f"skip (home not found: {target.home})")

    shutil.copy2(source, target.agents)
    return SyncLine(target.name, True, f"-> {target.agents}")
