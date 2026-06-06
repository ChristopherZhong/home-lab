---
name: align-assets
description: Use when reviewing existing agents, skills, and prompts so related workflow assets can be linked together, deduplicated, and kept consistent.
---

# AI Asset Alignment

Use this skill when the repository has multiple agents, skills, and prompts that may describe the same workflow and should be aligned.

User-facing prompt reference:

- `.agents/prompts/align-related-ai-assets.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Inputs to inspect

- `.agents/agents/`
- `.agents/prompts/`
- `.agents/skills/`
- See `AGENTS.md` for repository-wide guidance.
- `README.md`

## Workflow

1. Review the existing agents, skills, and prompts and group any assets that describe the same workflow.
1. For each related set, make the skill the procedural source of truth.
1. Make the prompt the concise user-facing invocation and have it reference the skill.
1. Make the agent a thin coordinator that references the skill and prompt instead of restating the workflow.
1. Keep variants only when they differ meaningfully in scope or intent.
1. Update general AI asset guidance if a new convention needs to be made explicit.

## Output expectations

- Related workflow assets should be explicitly linked.
- Procedural duplication should move into the skill where possible.
- Prompts and agents should stay concise once the workflow is aligned.
