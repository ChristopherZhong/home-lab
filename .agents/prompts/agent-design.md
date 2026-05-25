# Agent Design Prompt

Design a new reusable AI agent for this repository.

Workflow reference:

- `.agents/skills/design-agent/SKILL.md`

Requirements:

- Keep the definition tool-agnostic and store the canonical version in `.agents/agents/`.
- Use Markdown with YAML frontmatter.
- Scope the agent to a real repository workflow, not a hypothetical future system.
- Reuse existing prompts and skills if they already cover part of the workflow.
- If a tool-specific wrapper would help later, keep it thin and derive it from the canonical source.

Output format:

1. Agent name
1. When to use it
1. Inputs it should inspect
1. Outputs it should produce
1. Canonical Markdown definition
