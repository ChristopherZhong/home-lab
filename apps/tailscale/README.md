# Tailscale Kubernetes Operator (install assets)

This folder contains the Git-manifest layout to install the Tailscale Kubernetes
Operator via Argo CD using the static upstream manifest (recommended for this
repo). Do not commit any Tailscale auth keys or other secrets to Git — see
the `Secrets` section below.

See long-term learnings and guidance for this operator at
`.harness/tailscale-learnings.md`.

What is here
- `kustomization.yaml` — Kustomize overlay referencing the raw upstream operator manifest.
- `remove-operator-oauth-secret.yaml` — strategic-merge patch that deletes the
  placeholder `operator-oauth` Secret from the upstream manifest at build time.
- `scripts/create-tailscale-secret` — helper script to create the `operator-oauth` Secret
  out-of-band (keeps secrets out of Git).

How this is applied
- The repository contains an `ApplicationSet` (argocd/application-set.yaml) that
  auto-creates one `Application` per `apps/<name>` directory. The ApplicationSet
  is configured to `CreateNamespace=true`, so generated Applications create the
  `tailscale` namespace when they sync.

Install method
- This layout uses the static upstream manifest (`operator.yaml`) referenced from
  `kustomization.yaml`. For predictable installs, pin the raw manifest to a tag
  or commit SHA instead of `main`.

CRDs and RBAC ordering
- The upstream manifest includes CRDs and cluster-scoped RBAC. The manifest
  places CRDs at the top, but CRDs must reach the `Established` condition
  before CustomResources (CRs) are accepted by the API server. This repository
  does not include a bootstrap `crds/` Application — apply CRDs out-of-band
  (manually or via your provisioning pipeline) if you observe CR-related
  errors during sync.

Secrets
- The operator expects a Secret named `operator-oauth` containing `client_id`
  and `client_secret`. This repository intentionally removes the placeholder
  `operator-oauth` Secret from the upstream manifest (see
  `remove-operator-oauth-secret.yaml`) so that no secret material is ever
  applied from Git.

Before creating the `operator-oauth` Secret, follow the upstream guide to
configure tags and OAuth credentials (these steps must be completed prior to
applying the operator manifest):

https://tailscale.com/docs/kubernetes-operator/install-operator#configure-tags-and-oauth-credentials

Supply the real secret out-of-band using one of these options:
- Script (recommended for local workflows): run the included script before
  pushing or deploying:

```bash
# Non-interactive via environment variables
TS_CLIENT_ID=... TS_CLIENT_SECRET=... scripts/create-tailscale-secret

# Pass as flags
scripts/create-tailscale-secret --client-id your-id --client-secret your-secret
```

- CI-injected secret: have your CI create the Secret in the cluster before
  triggering Argo CD sync (suitable for automated pipelines).
- ExternalSecrets / SealedSecrets: use if you prefer controller-based secret
  injection or encrypted repo-backed secrets (not used here by default).

Notes and safety
- Test operator installation in a staging cluster before production.
- Do not commit plaintext secrets or sealed objects unless you accept that
  encrypted secrets are stored in Git.

References
- https://tailscale.com/docs/kubernetes-operator/
- https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/
