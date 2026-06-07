# AI Asset Naming Conventions

This document standardizes naming patterns for agents, skills, and prompts in this repository.

## Skills

Skills use the `<verb>-<noun>` pattern:

```
<verb>-<noun>
```

**Examples:**
- ✅ `design-agent` — Design new agents
- ✅ `review-prompt` — Review prompts
- ✅ `onboard-contributor` — Onboard contributors
- ✅ `create-issue` — Create issues
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
<workflow>-<actor>.md
```

**Examples:**
- ✅ `gitops-change-reviewer.md` — Reviews GitOps changes
- ✅ `docs-auditor.md` — Audits documentation
- ✅ `resolve-questions-maintainer.md` → Maintains question resolutions

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
- `review-prompt.md` → Links to skill `review-prompt`
- `agent-design.md` → Links to skill `design-agent`
- `align-related-ai-assets.md` → Links to skill `align-assets`

**Pattern:**
```
.agents/prompts/<descriptive-name>.md

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

## Examples from This Repository

| Asset Type | Name | Pattern | Purpose |
|-----------|------|---------|---------|
| **Skill** | `align-assets` | `<verb>-<noun>` | Align related AI assets |
| **Skill** | `conduct-interview` | `<verb>-<noun>` | Conduct structured interviews |
| **Skill** | `design-agent` | `<verb>-<noun>` | Design new agents |
| **Skill** | `harden-scripts` | `<verb>-<noun>` | Review and harden shell scripts |
| **Skill** | `onboard-contributor` | `<verb>-<noun>` | Onboard contributors |
| **Skill** | `resolve-questions` | `<verb>-<noun>` | Resolve open questions |
| **Skill** | `review-manifests` | `<verb>-<noun>` | Review Kubernetes manifests |
| **Skill** | `review-prompt` | `<verb>-<noun>` | Review reusable prompts |
| **Skill** | `sync-docs` | `<verb>-<noun>` | Synchronize documentation |
| **Agent** | `ai-asset-alignment-maintainer.agent.md` | `<workflow>-<actor>` | Maintain AI asset alignment |
| **Agent** | `docs-auditor.agent.md` | `<workflow>-<actor>` | Audit documentation |
| **Agent** | `gitops-change-reviewer.agent.md` | `<workflow>-<actor>` | Review infrastructure changes |
| **Agent** | `k3s-script-reviewer.agent.md` | `<workflow>-<actor>` | Review K3s scripts |
| **Agent** | `question-resolution-maintainer.agent.md` | `<workflow>-<actor>` | Maintain question resolutions |
| **Prompt** | `align-related-ai-assets.md` | Descriptive phrase | Align related AI assets |
| **Prompt** | `design-agent.md` | Mirrors skill name | Design new agents |
| **Prompt** | `documentation-review.md` | Descriptive phrase | Review documentation |
| **Prompt** | `kubernetes-change-review.md` | Descriptive phrase | Review Kubernetes changes |
| **Prompt** | `relentless-interview.md` | Mirrors skill name (user-facing) | Conduct persistent interviews |
| **Prompt** | `review-prompt.md` | Mirrors skill name | Review reusable prompts |
| **Prompt** | `script-hardening-review.md` | Descriptive phrase | Review script safety |
