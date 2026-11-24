# AI Asset Naming Conventions

This document standardizes naming patterns for agents, skills, and prompts in this repository.

## Skills

Skills use the `<verb>-<noun>` pattern:

```
<verb>-<noun>
```

**Examples:**

- ✅ `design-agent` — Design new agents
- ✅ `review-prompts` — Review prompts
- ✅ `onboard-contributor` — Onboard contributors
- ✅ `create-issue` — Create issues
- ✅ `validate-ai-assets` — Validate AI asset layout conventions
- ❌ `agent-design` — Wrong: noun-verb order
- ❌ `prompt-review` — Wrong: noun-verb order

**Verb guidelines:**

- Use action verbs: `create`, `review`, `design`, `audit`, `onboard`, `align`, `resolve`, `harden`, `sync`
- Keep it concise and unambiguous

**Noun guidelines:**

- Use singular nouns where possible: `agent`, `prompt`, `skill`, `contributor`
- Use compound nouns when necessary: `pull-request`, `github-issue`
- Keep it descriptive of the artifact or role

**Directory structure:**

```
.agents/skills/<verb>-<noun>/SKILL.md
```

## Agents

Agents use the `<workflow>-<actor>` pattern:

```
<workflow>-<actor>.agent.md
```

**Examples:**

- ✅ `docs-auditor.agent.md` — Audits documentation
- ✅ `ai-assets-maintainer.agent.md` — Maintains AI assets
- ✅ `question-resolution-maintainer.agent.md` — Maintains question resolutions

**Actor guidelines:**

- Use role descriptors: `-reviewer`, `-auditor`, `-maintainer`, `-designer`, `-creator`
- `-reviewer` for validation and quality assessment workflows
- `-maintainer` for ongoing management or maintenance workflows
- `-auditor` for inspection or compliance workflows
- `-designer` or `-creator` for design workflows

**Directory structure:**

```
.agents/agents/<workflow>-<actor>.agent.md
```

## Prompts

Prompts follow the same pattern as their linked skill or agent:

**Examples:**

- `review-prompts.prompt.md` → Links to skill `review-prompts`
- `agent-design.prompt.md` → Links to skill `design-agent`
- `align-related-ai-assets.prompt.md` → Links to skill `align-assets`

**Pattern:**

```
.agents/prompts/<descriptive-name>.prompt.md

---
# Prompt Title

Workflow reference:
- `.agents/skills/<verb>-<noun>/SKILL.md`
```

## When to Apply These Rules

- **New skills:** Always use `<verb>-<noun>` format and create a corresponding `.agents/rules/` entry if patterns differ
- **New agents:** Always use `<workflow>-<actor>` format
- **New prompts:** Name after the skill or use a descriptive action phrase; always include workflow reference
- **Existing assets:** Migrate to these conventions during refactoring or when renamed for clarity

## Examples

| Asset Type | Name                             | Pattern              |
| ---------- | -------------------------------- | -------------------- |
| Skill      | `align-assets`                   | `<verb>-<noun>`      |
| Skill      | `design-agent`                   | `<verb>-<noun>`      |
| Skill      | `sync-agents`                    | `<verb>-<noun>`      |
| Agent      | `docs-auditor.agent.md`          | `<workflow>-<actor>` |
| Agent      | `ai-assets-maintainer.agent.md`  | `<workflow>-<actor>` |
| Prompt     | `documentation-review.prompt.md` | Descriptive phrase   |
| Rule       | `markdown.rule.md`               | `<topic>.rule.md`    |

The directory itself is the authoritative list. Do not enumerate every asset
in this rule.
