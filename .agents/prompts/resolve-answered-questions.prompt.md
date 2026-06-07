# Resolve Answered Questions Prompt

Review `QUESTIONS.md` and `SUGGESTIONS.md` and resolve any items that already have explicit answers or accepted decisions recorded.

Workflow reference:

- `.agents/skills/resolve-questions/SKILL.md`

Requirements:

- Apply the answered or accepted decisions to the relevant repository files.
- Remove or rewrite resolved entries so `QUESTIONS.md` and `SUGGESTIONS.md` keep only open items.
- If the answers imply a repeated workflow, add or update an agent, skill, or prompt so the task can be triggered with a short request later.
- Keep changes grounded in files that actually exist.
- Keep unresolved ideas in `SUGGESTIONS.md` and record only truly new out-of-scope ideas there.

Output format:

1. Answered or accepted items applied
1. Files updated
1. Remaining open questions or suggestions
1. New reusable workflow assets added
