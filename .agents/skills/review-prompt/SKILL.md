---
name: review-prompt
description: Analyze reusable prompts in `.agents/prompts` for contradictions, inconsistencies, and gaps.
---

# Review Prompt

Use this skill to audit the repository's reusable prompts for quality, consistency, and coverage. This skill supports both general audits and pre-commit checkpoints.

User-facing prompt reference:

- `.agents/prompts/review-prompt.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Use Cases

- **General audit:** Review all prompts in `.agents/prompts/` to establish a baseline of quality and consistency.
- **Pre-commit checkpoint:** Validate new or modified prompts before merging changes to the repository.
- **Alignment check:** Ensure prompts are linked to their corresponding skills and reflect actual repository workflows.

## Inputs to inspect

- `.agents/prompts/` (all prompt files)
- `.agents/skills/` (to verify prompt-skill linkage and procedural accuracy)
- `.agents/agents/` (to check if agents duplicate prompt content instead of referencing it)
- `AGENTS.md` (to validate workflow descriptions against repository guidance)
- `README.md` (to catch documentation drift between prompts and reality)
- `QUESTIONS.md` and `SUGGESTIONS.md` (to identify unresolved decisions that should inform prompts)

## Workflow

### Phase 1: Technical Correctness & Consistency

1. **Verify skill linkage:** For each prompt, check that it references the correct skill file and that the skill file actually exists.
2. **Check frontmatter:** Ensure all prompts follow consistent YAML frontmatter structure (filename and location naming conventions).
3. **Validate repository references:** Confirm that any files, directories, or commands mentioned in prompts actually exist.
4. **Compare output formats:** Identify inconsistencies in how prompts structure their expected outputs (e.g., some use "Findings" vs "Risks").
5. **Detect duplication:** Identify prompts that describe overlapping workflows without clear differentiation or explicit variants.

### Phase 2: Tone, Voice & Style Alignment

1. **Check verb consistency:** Ensure prompts use consistent language for similar actions (e.g., "Review" vs "Analyze" vs "Audit").
2. **Assess requirement clarity:** Identify vague or subjective language that could lead to ambiguous interpretations.
3. **Validate focus areas:** Ensure "Focus on" or "Check" sections stay narrow and actionable (not diluted across too many concerns).
4. **Examine examples:** If prompts include examples, verify they reflect the repository's actual patterns and current state.

### Phase 3: Coverage & Gaps

1. **Map existing workflows:** Cross-reference `.agents/skills/` and `AGENTS.md` to identify key repository workflows.
2. **Find coverage gaps:** Identify workflows (especially in scripts, manifests, or maintenance tasks) that lack corresponding reusable prompts.
3. **Detect redundancy:** Note where multiple prompts could be consolidated or where clear variants are intentionally kept.
4. **Check agent coverage:** Verify that agents in `.agents/agents/` have corresponding prompts and are not replicating prompt content.

## Output Expectations

### Structured Report

1. **Technical issues found**
   - Missing or incorrect skill references
   - Non-existent files or directories mentioned
   - Inconsistent frontmatter or structure
   - Duplication (with specific prompts named)

2. **Consistency issues**
   - Tone or verb inconsistencies (with before/after examples)
   - Unclear or overly broad focus areas
   - Conflicting guidance between related prompts

3. **Coverage gaps**
   - Workflows that lack prompts
   - Opportunities to consolidate or differentiate variants
   - Agents that duplicate prompt content

4. **Recommended actions**
   - Specific prompt rewrites or clarifications (with suggested wording)
   - Consolidations or deduplication targets
   - New prompts to create (for uncovered workflows)
   - Links to establish between related assets

5. **Ready-to-merge checkpoint**
   - Passes technical correctness: Yes/No
   - Passes consistency audit: Yes/No
   - Gaps identified for later: Yes/No (with list)
   - Safe to merge: Yes/No (with reasoning)

## Validation Checklist

Use this checklist when reviewing prompts:

- [ ] All skill references point to files that exist
- [ ] All repository file/directory references match current structure
- [ ] Frontmatter is consistent with other prompts
- [ ] Output format is specific and actionable
- [ ] Terminology aligns with repository conventions (from `AGENTS.md`)
- [ ] No conflicting guidance with related prompts
- [ ] Does not duplicate content from linked skill
- [ ] Reflects current repository state (no outdated examples)
- [ ] Workflow is distinct or intentionally variant from other prompts
- [ ] Use cases and triggering conditions are clear

