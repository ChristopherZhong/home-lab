---
name: validate-ai-assets
description: Use when validating the repository's agent, prompt, skill, and rule asset layout.
---

# Validate AI assets

Use this skill when you need to verify that the repository's AI asset layout follows the documented conventions.

## Inputs to inspect

- [.agents/agents](.agents/agents)
- [.agents/prompts](.agents/prompts)
- [.agents/skills](.agents/skills)
- [.agents/rules](.agents/rules)
- [AGENTS.md](AGENTS.md)

## Workflow

1. Review the repository asset directories and confirm the expected naming conventions.
2. Run the validator script at `.agents/skills/validate-ai-assets/validate-ai-assets.py`.
3. If validation fails, fix the offending file names or layout issues before reporting completion.
4. Re-run the validator and confirm it passes.

## Output expectations

- The repository AI asset layout is verified.
- Any naming or placement issues are reported clearly and fixed.
