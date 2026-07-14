#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/agents/global/AGENTS.md"

MARKER_START="<!-- agent-documentation:global-agents:start -->"
MARKER_END="<!-- agent-documentation:global-agents:end -->"

# name|home_dir|dest_file  — only sync when home_dir already exists
COPY_TARGETS=(
  "Grok|$HOME/.grok|$HOME/.grok/AGENTS.md"
  "Cursor|$HOME/.cursor|$HOME/.cursor/AGENTS.md"
  "Codex|$HOME/.codex|$HOME/.codex/AGENTS.md"
  "Kimi|$HOME/.kimi-code|$HOME/.kimi-code/AGENTS.md"
)

usage() {
  cat <<EOF
Usage: $(basename "$0")

Copy agents/global/AGENTS.md to installed CLI tool homes only.
Skips tools whose home directory does not exist (does not create them).

Targets (if present):
  ~/.grok/AGENTS.md
  ~/.cursor/AGENTS.md
  ~/.codex/AGENTS.md
  ~/.kimi-code/AGENTS.md
  ~/.openclaw/workspace/AGENTS.md  (merged)
EOF
}

copy_agents() {
  local name="$1"
  local home_dir="$2"
  local dest="$3"

  if [[ ! -d "$home_dir" ]]; then
    echo "  skip $name ($home_dir not found)"
    return 1
  fi

  cp "$SOURCE" "$dest"
  echo "  -> $dest"
  return 0
}

merge_openclaw_agents() {
  local home_dir="$HOME/.openclaw"
  local dest="$home_dir/workspace/AGENTS.md"

  if [[ ! -d "$home_dir" ]]; then
    echo "  skip OpenClaw ($home_dir not found)"
    return 1
  fi

  mkdir -p "$(dirname "$dest")"

  if [[ ! -f "$dest" ]]; then
    cp "$SOURCE" "$dest"
    echo "  -> $dest (created)"
    return 0
  fi

  local tmp
  tmp="$(mktemp)"

  if grep -qF "$MARKER_START" "$dest"; then
    awk -v start="$MARKER_START" -v end="$MARKER_END" '
      $0 == start { skip=1; print; while ((getline line < ARGV[2]) > 0) print line; next }
      $0 == end { skip=0 }
      !skip { print }
    ' "$dest" "$SOURCE" > "$tmp"
  else
    cp "$dest" "$tmp"
    {
      echo
      echo "$MARKER_START"
      cat "$SOURCE"
      echo "$MARKER_END"
    } >> "$tmp"
  fi

  mv "$tmp" "$dest"
  echo "  -> $dest (merged)"
  return 0
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  if [[ ! -f "$SOURCE" ]]; then
    echo "error: source not found: $SOURCE" >&2
    exit 1
  fi

  echo "Syncing global AGENTS.md"
  echo "  source: $SOURCE"

  local synced=0
  local entry name home_dir dest

  for entry in "${COPY_TARGETS[@]}"; do
    IFS='|' read -r name home_dir dest <<< "$entry"
    if copy_agents "$name" "$home_dir" "$dest"; then
      synced=$((synced + 1))
    fi
  done

  if merge_openclaw_agents; then
    synced=$((synced + 1))
  fi

  if [[ "$synced" -eq 0 ]]; then
    echo "error: no installed CLI tool homes found to sync" >&2
    exit 1
  fi

  echo "Done. ($synced target(s))"
}

main "$@"
