---
name: sync-docs
description: Use when updating or reviewing documentation in this repository so README, AGENTS, prompts, suggestions, and questions stay consistent with the actual files and workflows.
---

# Home Lab Documentation Sync

Use this skill when a task touches repository documentation, onboarding guidance, or reusable prompts.

User-facing prompt reference:

- `.agents/prompts/documentation-review.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Inputs to inspect

- `README.md`
- `AGENTS.md`
- `QUESTIONS.md`
- `SUGGESTIONS.md`
- `.agents/prompts/`
- The files or directories being documented

## Workflow

1. Check the real repository state before changing documentation.
1. Separate implemented assets from roadmap ideas.
1. Update the nearest relevant documentation instead of scattering the same note across many files.
1. If a better approach exists but was not requested, record it in `SUGGESTIONS.md`.
1. If intent is unclear or repository evidence is missing, add the unresolved question to `QUESTIONS.md`.
1. Keep command examples in long-form option style when practical.

## Output expectations

- Documentation should reference files that actually exist.
- New prompts should match real maintenance tasks in this repository.
- Repository-wide guidance should stay in `AGENTS.md`, while task-specific reusable text belongs in `.agents/prompts/`.
