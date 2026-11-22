---
paths:
  - "*.md"
---

# Markdown Guidelines

- For numbered/ordered lists, always use `1.` for each item. Do not change `1.` to explicit numbers (e.g., `2.`, `3.`) to preserve Markdown auto-numbering. Explicit numbering breaks auto-numbering and requires manual renumbering when inserting items.
- For unordered lists, always use `-` (hyphen) instead of `*` (asterisk).
- For command-line examples, always use long-form options (e.g., `apt update --yes` instead of `apt update -y`).
- For script examples, always prefix commands with `$` to distinguish them from output.

## Documentation Writing Standards

### ASD-STE100 Simplified Technical English

- When writing documentation, apply ASD-STE100 Simplified Technical English principles:
  - Use controlled, approved vocabulary; avoid synonyms and jargon.
  - Keep sentences short and state one idea per sentence.
  - Use active voice and the present tense.
  - Avoid ambiguous words, idioms, and noun strings.
  - Write so the meaning is clear to non-native English speakers.

### EARS (Easy Approach to Requirements Syntax)

- When documenting requirements, use EARS syntax so each requirement is precise, testable, and consistent:
  - **Statement:** "The system shall <action> <object>."
  - **Trigger:** "The system shall <action> <object> when <condition>."
  - **State:** "The system shall <action> <object> while <condition>."
  - **Event-driven (after/before):** "The system shall <action> <object> after <event>." / "before <event>."
  - **Optional measure:** "The system shall <action> <object> <measure>."
  - Every requirement must contain exactly one testable obligation (`shall`).
