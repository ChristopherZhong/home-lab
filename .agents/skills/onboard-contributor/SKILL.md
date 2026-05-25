---
name: repo-onboarding
description: Guide new contributors through this repository with accurate, current information.
---

# Repository Onboarding

Use this skill to onboard new contributors by explaining the repository structure, current state, and key workflows with high accuracy.

User-facing prompt reference:

- `.agents/prompts/repo-onboarding.md`

Use that prompt when you want a short reusable invocation for this workflow. Treat this skill as the procedural source of truth and keep the prompt concise.

## Use Cases

- **New contributor onboarding:** A developer joining the project needs an accurate overview of what exists today.
- **Architecture briefing:** Someone needs to understand the repository's structure, tooling, and workflows before making changes.
- **Roadmap vs. implementation clarity:** Distinguish between what is currently deployed and what is planned for later.

## Inputs to inspect

- `README.md` (primary onboarding document)
- `AGENTS.md` (AI assistant guidance and repository conventions)
- `.agents/` directory structure (skills, prompts, agents)
- `scripts/` (available administration tooling)
- `argocd/` and `kube-system/` (deployed manifests and their state)
- `QUESTIONS.md` (open questions a contributor should be aware of)
- `SUGGESTIONS.md` (planned ideas and roadmap items)

## Workflow

1. **Inventory current state:** List what is actually in the repository today—files, scripts, manifests, configurations that are deployed or active.

2. **Explain structure:** Describe:
   - The purpose of each major directory
   - What technologies are in use (Kubernetes, K3s, Argo CD, Traefik)
   - How the GitOps workflow operates
   - Where AI assets are stored (agents, skills, prompts)

3. **Document key scripts:** For each script in `scripts/`, explain what it does and when to use it.

4. **Identify roadmap items:** Clearly separate "implemented and deployed today" from "planned for later" so contributors don't assume something exists.

5. **Surface gaps:** Note any assumptions or gaps a new contributor should verify before making changes (e.g., "Argo CD is assumed to be already installed").

6. **Keep it grounded:** Reference only files and directories that actually exist. Do not invent missing infrastructure.

## Output Expectations

- **High-level overview** of repository purpose and scope
- **Clear inventory** of what exists today (implementations)
- **Roadmap clarity** (what is planned or in progress)
- **Script documentation** with use cases and safety notes
- **AI asset explanation** (how agents, skills, and prompts work together)
- **Gap identification** (assumptions, missing pieces, or areas needing verification)
- **Grounded in reality** (no references to non-existent files or future systems unless explicitly marked as "planned")

## Assumptions to Call Out

- Kubernetes and K3s knowledge (explain briefly if contributor is new to these)
- Git familiarity (assume they know Git basics, but explain GitOps if new)
- GitHub Actions or CI/CD (mention if present; this repo uses Argo CD)
- Administrative access (note what scripts require sudo or special permissions)

## Validation Checklist

When producing onboarding material, verify:

- [ ] All files and directories mentioned actually exist
- [ ] All commands and scripts are current and safe
- [ ] Planned items are clearly marked as such, not presented as current
- [ ] No outdated examples or commands are referenced
- [ ] The explanation is concise enough for a quick read but complete enough to prevent mistakes
- [ ] Key safety notes (e.g., permission requirements, destructive operations) are surfaced
- [ ] Related documentation (README, AGENTS.md) is consistent with this explanation

