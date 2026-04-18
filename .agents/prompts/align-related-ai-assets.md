# Align Related AI Assets Prompt

Review the existing agents, skills, and prompts in this repository and look for workflows that are represented in more than one place.

Workflow reference:

- `.agents/skills/ai-asset-alignment/SKILL.md`

Requirements:

- Detect related assets that describe the same workflow.
- Make the skill the procedural source of truth.
- Make the prompt the concise user-facing invocation.
- Make the agent a thin coordinator that references the skill and prompt instead of duplicating them.
- Keep only intentional variants when there is a meaningful difference in scope.

Output format:

1. Related workflow sets found
1. Assets aligned
1. Variants kept intentionally
1. Remaining duplication risks
