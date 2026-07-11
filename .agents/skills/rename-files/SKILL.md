---
name: rename-files
description: Use when renaming repository files or directories and updating related references across the repo.
---

# Rename Files

Use this skill when a repository path needs to be renamed and related references should be updated consistently.

## Inputs to inspect

- The current file or directory path to rename.
- Any related documentation, prompt, skill, agent, or rule files that reference that path.
- Repository guidance in AGENTS.md.

## Workflow

1. Confirm the old path and the intended new path.
2. Use the helper script at `.agents/skills/rename-files/rename-files.sh`.
3. Rename the path and update textual references (path and basename) across the repository.
4. Stage the changes and present them for human review before committing.

## Output expectations

- The path is moved to its new location.
- Related references are updated consistently.
- The change is staged and ready for review.
