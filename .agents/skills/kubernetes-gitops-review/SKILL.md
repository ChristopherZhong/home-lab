---
name: kubernetes-gitops-review
description: Use when reviewing or preparing Kubernetes and Argo CD changes in this repository, especially when manifests, namespaces, ingress, or GitOps workflow documentation may need to change together.
---

# Kubernetes GitOps Review

Use this skill for manifest reviews, Argo CD workflow updates, and changes that could affect how the repository maps to the cluster.

User-facing prompt references:

- `.agents/prompts/kubernetes-change-review.md`
- `.agents/prompts/gitops-rollout-review.md`

Use the Kubernetes change review prompt as the default invocation for this workflow. Use the GitOps rollout review prompt when the emphasis is merge-readiness, rollout risk, or recovery planning.

## Inputs to inspect

- `argocd/`
- `kube-system/`
- `scripts/install-argocd`
- `README.md`
- `AGENTS.md`

## Workflow

1. Confirm the manifest path, namespace, and resource names match the current repository layout.
1. Check whether the change assumes components that are not yet tracked in Git.
1. Verify whether the change affects bootstrap or operator instructions in `README.md`.
1. Call out rollout risks, path coupling, or mismatches between scripts and manifests.
1. If a suggestion is useful but outside the requested change, record it in `SUGGESTIONS.md`.

## Output expectations

- Findings should be concrete and path-specific.
- Documentation follow-ups should be listed when manifests or scripts change operator behavior.
- Recommendations should preserve the GitOps workflow already described in the repository.
