---
name: agent-design
description: Design new reusable AI agents for this repository.
---

# Agent Design

Use this skill when creating new reusable agents that coordinate repository workflows.

User-facing prompt reference:

- `.agents/prompts/agent-design.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Use Cases

- **New workflow agent:** Design an agent to coordinate a frequently-triggered workflow that spans multiple skills or prompts.
- **Tool-agnostic definition:** Define the agent in a tool-agnostic way, storing the canonical version in `.agents/agents/`.
- **Thin wrappers:** When needed later, create thin tool-specific wrappers that reference the canonical source.

## Inputs to inspect

- `.agents/agents/` (existing agent definitions)
- `.agents/prompts/` (existing prompts to reuse)
- `.agents/skills/` (existing skills to reuse)
- `AGENTS.md` (repository guidance on agents and workflows)
- `README.md` (to verify the workflow is grounded in actual repository needs)

## Workflow

1. **Validate the workflow scope:** Confirm the agent represents a real, frequently-invoked repository workflow—not a hypothetical or one-off task.

2. **Review existing coverage:** Check if an existing skill or prompt already covers this workflow. Reuse rather than duplicate.

3. **Define clear boundaries:** Document:
   - When to use this agent (what triggers it?)
   - What inputs it should inspect (files, directories, prior context)
   - What outputs it should produce
   - How it differs from related agents or workflows

4. **Create the canonical definition:** Write the agent in Markdown with YAML frontmatter, tool-agnostic and stored in `.agents/agents/`.

5. **Link related assets:** Reference linked skills, prompts, and agents from the canonical definition so the workflow is discoverable.

6. **Consider tool-specific wrappers:** If the agent will be used in multiple tools, keep the canonical definition tool-neutral and create thin derivatives for each tool.

## Output Expectations

- **Canonical agent definition** in `.agents/agents/` following existing naming conventions
- **Clear YAML frontmatter** with name, description, and purpose
- **Markdown body** with:
  - When to use it
  - Inputs to inspect
  - Outputs to produce
  - Related skills, prompts, and agents (with links)
- **Tool-agnostic language** (no VS Code–specific or GitHub-specific wording unless intentional)
- **Linked to supporting assets:** The agent should reference its backing skill and prompt, not duplicate their content

## Naming Conventions

- Agent file: `<workflow>-<actor>.md` (e.g., `gitops-change-reviewer.md`, `docs-auditor.md`)
- Descriptor in filename:
  - Use `-reviewer` for auditing/validation workflows
  - Use `-maintainer` for maintenance or management workflows
  - Use `-designer` or `-creator` for design workflows
- Keep names concise and action-oriented

## Examples from Repository

- `gitops-change-reviewer.md` → Reviews proposed infrastructure changes
- `docs-auditor.md` → Audits documentation consistency
- `question-resolution-maintainer.md` → Resolves open questions and suggestions

