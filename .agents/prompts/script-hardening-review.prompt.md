# Script Hardening Review Prompt

Review a shell script in this repository with a focus on home lab safety and operator clarity.

Workflow reference:

- `.agents/skills/harden-scripts/SKILL.md`

Focus on:

- Working-directory assumptions
- Relative path safety
- Privilege assumptions such as `sudo`
- Clear failure messages
- Readability of commands and long-form option usage in documentation
- Whether the README still matches the script behavior

Output format:

1. Risks or brittle behavior
1. Safe improvements
1. Documentation changes needed
