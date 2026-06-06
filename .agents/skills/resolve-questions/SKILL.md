---
name: resolve-questions
description: Use when QUESTIONS.md or SUGGESTIONS.md contains explicit answers or accepted decisions that should be applied to repository files and removed from the open backlog.
---

# Question Resolution

Use this skill when the repository has recorded answers inside `QUESTIONS.md` or accepted decisions inside `SUGGESTIONS.md` and those decisions should now be turned into concrete updates.

User-facing prompt reference:

- `.agents/prompts/resolve-answered-questions.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Inputs to inspect

- `QUESTIONS.md`
- `README.md`
- `SUGGESTIONS.md`
- `.agents/agents/`
- `.agents/prompts/`
- `.agents/skills/`

See `AGENTS.md` for repository-wide guidance.

## Workflow

1. Read `QUESTIONS.md` and identify which questions have explicit answers attached.
1. Read `SUGGESTIONS.md` and identify which suggestions have been explicitly accepted or converted into clear decisions.
1. Apply those answers or accepted decisions to the relevant files instead of leaving them as comments only.
1. Remove or rewrite the resolved question entries so `QUESTIONS.md` remains an open backlog.
1. Remove or rewrite the resolved suggestion entries so `SUGGESTIONS.md` remains a backlog of still-open ideas.
1. If the decision reveals a repeated maintenance pattern, add or update an agent, prompt, or skill for that workflow.
1. Keep unresolved or ambiguous items in `QUESTIONS.md` and `SUGGESTIONS.md`.

## Output expectations

- Answered questions and accepted suggestions should result in concrete repository updates.
- `QUESTIONS.md` and `SUGGESTIONS.md` should contain only unresolved items after the task.
- Repeated workflows should gain reusable AI assets when that will reduce future prompting overhead.
