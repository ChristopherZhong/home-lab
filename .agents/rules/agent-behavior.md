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
- **Scripts:** make runnable scripts executable and note this in commit messages.
- **Language:** keep messaging neutral and professional; avoid emotional phrasing.
