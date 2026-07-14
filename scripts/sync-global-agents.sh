#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/agents/global/AGENTS.md"

MARKER_START="<!-- agent-documentation:global-agents:start -->"
MARKER_END="<!-- agent-documentation:global-agents:end -->"

TARGETS=(
  "$HOME/.grok/AGENTS.md"
  "$HOME/.cursor/AGENTS.md"
  "$HOME/.codex/AGENTS.md"
  "$HOME/.kimi-code/AGENTS.md"
)

usage() {
  cat <<EOF
Usage: $(basename "$0")

Copy agents/global/AGENTS.md to global AGENTS.md paths for Grok, Cursor, Codex, and Kimi.
For OpenClaw, merge into ~/.openclaw/workspace/AGENTS.md without removing workspace bootstrap content.
EOF
}

copy_agents() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  cp "$SOURCE" "$dest"
  echo "  -> $dest"
}

merge_openclaw_agents() {
  local dest="$HOME/.openclaw/workspace/AGENTS.md"
  mkdir -p "$(dirname "$dest")"

  if [[ ! -f "$dest" ]]; then
    cp "$SOURCE" "$dest"
    echo "  -> $dest (created)"
    return
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

  for dest in "${TARGETS[@]}"; do
    copy_agents "$dest"
  done

  merge_openclaw_agents
  echo "Done."
}

main "$@"