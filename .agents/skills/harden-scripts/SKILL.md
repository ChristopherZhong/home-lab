---
name: harden-scripts
description: Use when reviewing or editing the repository shell scripts so bootstrap, install, and upgrade flows stay clear, safe, and aligned with the documented home lab workflow.
---

# K3s Shell Safety

Use this skill when working on `scripts/init`, `scripts/install-argocd`, `scripts/upgrade`, or related documentation.

User-facing prompt reference:

- `.agents/prompts/script-hardening-review.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Inputs to inspect

- `scripts/`
- `README.md`
- `AGENTS.md`

## Workflow

1. Review assumptions about the current working directory, privileges, and required binaries.
1. Check whether paths are robust when scripts are launched from different directories.
1. Prefer explicit, readable command forms in documentation and examples.
1. Preserve simple operator flows suitable for a home lab setup.
1. If script behavior changes, update the matching docs in the same task when requested.

## Output expectations

- Call out brittle relative paths, missing checks, and idempotency risks.
- Keep changes minimal and aligned with the repository's current scope.
- Note any operator-facing behavior changes that should be documented.
