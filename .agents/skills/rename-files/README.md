# rename-files.sh

## Purpose

Small helper to rename repository files or directories and update textual
references across the repository. It is useful for agent files, prompts,
skills, documentation, or any other tracked asset. It stages changes but does
not commit.

## Usage

Use the helper through the rename skill rather than invoking it directly from the repository root.

The skill entry point is:

```text
.agents/skills/rename-files/SKILL.md
```

The helper is invoked by that skill as part of the rename workflow.

## Notes

- The script requires a clean git working tree before running.
- It will `git mv` the files and update textual references (both path and basename).
- It stages all changes (`git add -A`) but does not create a commit — you must
  review and commit with an appropriate Conventional Commit message.

## Validation

Run the validator locally before changing or renaming AI assets:

```bash
python3 .agents/skills/validate-ai-assets/validate-ai-assets.py
```

Example commit message:

```
chore(agents): rename agent files to '*.agent.md'
```
