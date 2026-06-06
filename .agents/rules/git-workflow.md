# Git workflow preference

Team preferences and non-negotiable rules for contributors and automation:

- Use the local `git` CLI (in-repo terminal) for commits and pushes by default.
  - Rationale: uses the local worktree, respects local hooks and user identity,
    and does not require external helper toolchains as a prerequisite.
- Only use GitKraken, MCP, or other remote helpers when the user explicitly
  requests them.
- Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) format (for example, `chore(tailscale): ...`).

## Rules

- Do not automatically commit changes. Always stage and wait for user review before committing.
- When making automated edits, stage changes and commit them in the workspace, then verify resulting file contents before reporting completion.
- All commit messages must follow the Conventional Commits specification.
