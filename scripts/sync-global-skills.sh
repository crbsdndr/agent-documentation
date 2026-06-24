#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills/global"

TARGETS=(
  "$HOME/.grok/skills"
  "$HOME/.cursor/skills"
  "$HOME/.codex/skills"
  "$HOME/.openclaw/skills"
  "$HOME/.kimi-code/skills"
)

usage() {
  cat <<EOF
Usage: $(basename "$0") [skill-name|all]

Copy global skills from skills/global/ to all CLI skill directories.

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

  for base in "${TARGETS[@]}"; do
    local dest="$base/$name"
    mkdir -p "$dest"
    cp -a "$source/." "$dest/"
    echo "  -> $dest"
  done

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