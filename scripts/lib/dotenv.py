"""Load a simple KEY=VALUE .env file into os.environ."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path) -> int:
    """Load key=value pairs from path. Returns number of keys set. Repo values win."""
    if not path.is_file():
        return 0

    loaded = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        if not key:
            continue
        os.environ[key] = value
        loaded += 1
    return loaded
