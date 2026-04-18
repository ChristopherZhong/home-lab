# Kubernetes Change Review Prompt

Review a proposed Kubernetes change for this home lab repository.

Workflow reference:

- `.agents/skills/kubernetes-gitops-review/SKILL.md`

Focus on:

- Whether the manifest path and namespace match the current repository layout
- Whether the change fits the GitOps workflow described in `AGENTS.md`
- Whether the README needs to be updated alongside the manifest or script change
- Whether the change introduces assumptions about components that are not yet present in the repo

Output format:

1. Risks or inconsistencies
1. Documentation updates required
1. Safe next steps
