# Documentation Review Prompt

Review this repository as a documentation auditor.

Workflow reference:

- `.agents/skills/sync-docs/SKILL.md`

Goals:

- Compare `README.md`, `AGENTS.md`, and any onboarding docs against the actual files and directories in the repository.
- Flag any commands, file paths, manifests, or scripts mentioned in documentation that do not exist.
- Distinguish clearly between "currently implemented" and "planned for later".
- Preserve the repository's current structure and do not invent missing files.

Output format:

1. Confirmed repository facts
1. Documentation inconsistencies
1. Exact wording changes to recommend
1. Open questions that need maintainer confirmation
