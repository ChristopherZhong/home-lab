# Tailscale Kubernetes Operator (install assets)

This folder contains the Git-manifest layout to install the Tailscale Kubernetes
Operator via Argo CD. Do not commit any Tailscale auth keys or other secrets to
Git — see the `Secrets` section below.

What is here
- `kustomization.yaml` — Kustomize overlay that references the upstream operator manifests.

How this is applied
- The repository contains an `ApplicationSet` (argocd/application-set.yaml) that
  auto-creates one `Application` per `apps/<name>` directory. The ApplicationSet
  is configured to `CreateNamespace=true`, so generated Applications will create
  the `tailscale` namespace when they sync.

CRDs and RBAC ordering
- The operator installs CRDs and may require cluster-scoped RBAC. If the
  operator's CustomResources (CRs) are applied before the CRDs exist, syncs
  will fail. Recommended approaches:
  - Create a separate `crds/` bootstrap app (or pre-apply CRDs) so CRDs exist
    before the operator's CRs are created.
  - Allow Argo CD to manage cluster-scoped resources by granting the Project
    appropriate permissions, but test this in staging first.

Secrets
- Do not store `TS_AUTHKEY` in Git. Create the secret out-of-band on the
  cluster (an example you can run locally):

```bash
kubectl create namespace tailscale
kubectl create secret generic tailscale-auth \
  --from-literal=TS_AUTHKEY=tskey-0123456789abcdef \
  --namespace=tailscale
```

- Recommended production approaches:
  - Use ExternalSecrets or SealedSecrets so values are injected at deploy time.
  - Store secrets in your CI/CD secret store and create cluster secrets during
    CI/CD runs (never commit plaintext secrets).

Notes and safety
- Test operator installation in a staging cluster before production.
- Ensure your Argo CD Project permits any required cluster-scoped resources or
  pre-apply them via a bootstrap `Application`.

References
- https://tailscale.com/docs/kubernetes-operator/
- https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/
