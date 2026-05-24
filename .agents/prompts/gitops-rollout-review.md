# GitOps Rollout Review Prompt

Review a proposed infrastructure change for this home lab repository before it is merged.

Workflow reference:

- `.agents/skills/kubernetes-gitops-review/SKILL.md`

Focus on:

- Whether the manifest paths and namespaces match the repository
- Whether scripts and manifests still agree with each other
- Whether `README.md` or `AGENTS.md` must change with the code
- Whether the change assumes services that are not yet tracked in Git
- Whether there are rollout or recovery risks for a small K3s home lab

Output format:

1. Findings
1. Required documentation updates
1. Suggestions that are out of scope
