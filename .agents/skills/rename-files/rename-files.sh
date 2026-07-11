#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: rename-files.sh <old-path> <new-path> [<old-path> <new-path> ...]
Renames one or more files or directories and updates textual references across the repo.
Each old/new pair is processed in order. The script stages changes but does not commit.
EOF
  exit 2
}

args=("$@")
if [ "${#args[@]}" -lt 2 ] || [ $(( ${#args[@]} % 2 )) -ne 0 ]; then
  usage
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository. Run this from the repository root." >&2
  exit 1
fi

if ! git diff --quiet --ignore-submodules --; then
  echo "Git working tree is dirty. Commit or stash changes before running this script." >&2
  exit 1
fi

for ((index = 0; index < ${#args[@]}; index += 2)); do
  old="${args[$index]}"
  new="${args[$index + 1]}"
  if [ ! -e "$old" ]; then
    echo "Path not found: $old" >&2
    exit 1
  fi
  if [ "$old" = "$new" ]; then
    echo "Old and new paths are identical: $old" >&2
    exit 1
  fi
  if [ -e "$new" ]; then
    echo "Destination already exists: $new" >&2
    exit 1
  fi
done

for ((index = 0; index < ${#args[@]}; index += 2)); do
  old="${args[$index]}"
  new="${args[$index + 1]}"
  echo "Renaming: $old -> $new"
  if git ls-files --error-unmatch "$old" >/dev/null 2>&1; then
    git mv -- "$old" "$new"
  else
    mkdir -p "$(dirname -- "$new")"
    mv -- "$old" "$new"
  fi
  old_basename=$(basename -- "$old")
  new_basename=$(basename -- "$new")
  echo "Updating textual references to '$old' and '$old_basename'..."
  git grep -Il -e "$old" -e "$old_basename" -- . ':(exclude).git' || true | while IFS= read -r file; do
    [ -z "$file" ] && continue
    python3 .agents/skills/rename-files/replace-references.py "$file" "$old" "$new" "$old_basename" "$new_basename"
  done
done

git add -A

echo "Done. Changes staged. Review with 'git status --porcelain' or 'git diff --staged'."
echo "This script does NOT commit changes. Commit manually with an appropriate Conventional Commit message."
