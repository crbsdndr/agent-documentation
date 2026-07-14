#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills/global"

# name|home_dir|skills_dir  — only sync when home_dir already exists
TARGETS=(
  "Grok|$HOME/.grok|$HOME/.grok/skills"
  "Cursor|$HOME/.cursor|$HOME/.cursor/skills"
  "Codex|$HOME/.codex|$HOME/.codex/skills"
  "OpenClaw|$HOME/.openclaw|$HOME/.openclaw/skills"
  "Kimi|$HOME/.kimi-code|$HOME/.kimi-code/skills"
)

usage() {
  cat <<EOF
Usage: $(basename "$0") [skill-name|all]

Copy global skills from skills/global/ to installed CLI skill directories only.
Skips tools whose home directory does not exist (does not create them).

Examples:
  $(basename "$0") git-commit
  $(basename "$0") all
EOF
}

copy_skill() {
  local name="$1"
  local source="$SKILLS_ROOT/$name"

  if [[ ! -d "$source" ]]; then
    echo "error: skill not found: $source" >&2
    return 1
  fi

  echo "Syncing: $name"
  echo "  source: $source"

  local synced=0
  local entry tool_name home_dir skills_dir dest

  for entry in "${TARGETS[@]}"; do
    IFS='|' read -r tool_name home_dir skills_dir <<< "$entry"
    if [[ ! -d "$home_dir" ]]; then
      echo "  skip $tool_name ($home_dir not found)"
      continue
    fi

    dest="$skills_dir/$name"
    mkdir -p "$dest"
    cp -a "$source/." "$dest/"
    echo "  -> $dest"
    synced=$((synced + 1))
  done

  if [[ "$synced" -eq 0 ]]; then
    echo "error: no installed CLI tool homes found to sync" >&2
    return 1
  fi

  echo
}

main() {
  local arg="${1:-git-commit}"

  if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
    usage
    exit 0
  fi

  if [[ ! -d "$SKILLS_ROOT" ]]; then
    echo "error: skills directory not found: $SKILLS_ROOT" >&2
    exit 1
  fi

  if [[ "$arg" == "all" ]]; then
    local found=0
    for dir in "$SKILLS_ROOT"/*; do
      [[ -d "$dir" ]] || continue
      found=1
      copy_skill "$(basename "$dir")"
    done
    if [[ "$found" -eq 0 ]]; then
      echo "error: no skills found in $SKILLS_ROOT" >&2
      exit 1
    fi
  else
    copy_skill "$arg"
  fi

  echo "Done."
}

main "$@"
