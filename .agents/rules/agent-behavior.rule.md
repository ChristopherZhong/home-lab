# Agent behavior and process rules

These rules describe the expected behavior and process for automated agents
working in this repository. They are repository-wide and not specific to Git
operations.

- **Check-first:** search for and read existing files before creating new
  documentation or rules; propose edits or merges instead of creating duplicates.

- **Ask-before-act:** require explicit user approval for design or behavior
  decisions that change repository behavior or add automation.

- **Verify-after-edit:** after any file edit, open and read the edited files to
  confirm content and absence of duplicate headers or stray fragments.

- **Canonical-first:** prefer updating canonical documents (for example, files
  under `.agents/rules/`) rather than adding near-duplicate files elsewhere.

- **Rule-first:** before taking action or promising future compliance, read the
  canonical rules in `.agents/rules/` and follow them immediately in the
  current session; do not rely on vague promises such as "I will remember
  next time."

- **Correct-on-failure:** if an earlier step violated repository rules, stop
  and correct that mistake in the same session instead of deferring it to a
  future session.

- **Scripts:** make runnable scripts executable and note this in commit messages.

- **Language:** keep messaging neutral and professional; avoid emotional phrasing.

- **Self-evolution / Maintain canonical assets:** when an agent makes a
  repository change that affects `.agents/` assets (agents, prompts, skills,
  or rules), the agent SHOULD update the canonical files under
  `.agents/rules/`, `.agents/agents/`, `.agents/prompts/`, or
  `.agents/skills/` so the repository's source-of-truth remains consistent.

- **Rename safety:** when renaming an agent or other AI asset, update all
  textual references (both path and basename) across the repository. Use a
  helper script (for example `.agents/scripts/rename-agent-files.sh`) when
  available, stage the changes, and present them for human review before
  committing.

- **Preflight and approval:** automated agents must present a concise
  preflight summary before committing, including the proposed Conventional
  Commit message and list of files to be committed, and MUST wait for
  explicit user approval before performing the `git commit` operation.
