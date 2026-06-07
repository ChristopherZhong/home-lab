# Review Prompts

Audit the reusable prompts in `.agents/prompts/` for contradictions, inconsistencies, and coverage gaps.

Workflow reference:

- `.agents/skills/review-prompt/SKILL.md`

Analysis focus:

- **Technical correctness:** Verify skill linkage, file references, and frontmatter consistency.
- **Consistency & tone:** Check for conflicting guidance, verb consistency, and style alignment.
- **Coverage gaps:** Identify workflows that lack prompts or opportunities to consolidate variants.

Output format:

1. Technical issues (with specific prompts affected)
1. Consistency issues (with before/after examples)
1. Coverage gaps (with workflows named and action items)
1. Recommended rewrites (with specific wording suggestions)
1. Merge checkpoint (pass/fail + reasoning)
