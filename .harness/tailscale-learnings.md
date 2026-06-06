# Tailscale operator learnings

Notes and long-term recommendations for adding the Tailscale operator and
related manifests to this repository.

- Use a static upstream manifest for the Tailscale operator and reference the
  raw `operator.yaml` from the upstream repository in
  `apps/tailscale/kustomization.yaml`. Pin the URL to a tag or commit SHA for
  reproducible installs.
- Use a Kustomize strategic-merge patch (for example,
  `apps/tailscale/remove-operator-oauth-secret.yaml`) to remove any upstream
  placeholder `operator-oauth` Secret so that secret material is not applied
  from Git.
- Do not commit plaintext secrets. Preferred approaches:
  - Inject secrets via CI/CD at deploy time.
  - Use an ExternalSecrets controller or SealedSecrets to manage secrets from
    external secret stores.
  - Apply secrets out-of-band via a local script (for example,
    `scripts/create-tailscale-secret`) when manual provisioning is required.
- CRD ordering can cause sync failures if CRDs are not established before CRs
  are created. Options to mitigate this include pre-applying CRDs via a
  bootstrap Application, adding a pre-sync hook that waits for CRDs to be
  `Established`, or sequencing Argo CD Applications so CRDs are applied first.

Relevant files
- `apps/tailscale/kustomization.yaml`
- `apps/tailscale/remove-operator-oauth-secret.yaml`
- `apps/tailscale/README.md`
- `scripts/create-tailscale-secret` (executable)
