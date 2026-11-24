---
name: harden-scripts
description: Use when reviewing or editing the repository shell scripts so bootstrap, install, upgrade, and teardown flows stay clear, safe, and idempotent.
---

# Shell Script Hardening

Use this skill when working on `scripts/init`, `scripts/install-argocd`,
`scripts/upgrade`, or the documentation that describes them.

User-facing prompt reference:

- `.agents/prompts/script-hardening-review.prompt.md`

Use that prompt when you want a short reusable invocation for this workflow.
Treat this skill as the procedural source of truth and keep the prompt concise.

## Inputs to inspect

- `scripts/`
- `README.md`
- The documentation for each script
- See `AGENTS.md` for repository-wide guidance

## Workflow

1. Review assumptions about the current working directory, privileges, and
   required binaries.
1. Check whether paths stay correct when a script is launched from a different
   directory.
1. Check that repeated runs are safe: creating what is missing, skipping what
   already exists, and failing loudly on a partial state.
1. Prefer explicit, readable command forms in documentation and examples.
1. Preserve simple operator flows; do not add abstraction without a reason.
1. If script behavior changes, update the matching documentation in the same
   task.

## Output expectations

- Call out brittle relative paths, missing checks, and idempotency risks.
- Keep changes minimal and aligned with the repository's current scope.
- Note any operator-facing behavior change that should be documented.

## Validation checklist

- [ ] The script works when run from a directory other than the repository
      root, or states the assumption plainly.
- [ ] Required binaries and privileges are checked before use.
- [ ] A second run does not corrupt or duplicate state.
- [ ] Failure messages say what failed and what to do next.
- [ ] The documentation still matches the script.
