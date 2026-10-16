# Argo CD Configuration Guide

Welcome! This guide walks you through configuring Argo CD for GitOps in the home lab. After Argo CD is installed, these steps will help you set up automated deployments from this Git repository to your Kubernetes cluster.

## What is Argo CD?

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It simplifies deployments by:

- **Declaring desired state in Git**: You define what should run on your cluster in YAML files committed to this repository
- **Automatically syncing**: Argo CD continuously watches this repository and applies any changes to your Kubernetes cluster
- **Providing a dashboard**: A web UI lets you monitor deployments, check status, and manually sync if needed

## Getting Started

This repository bootstraps Argo CD with `scripts/install-argocd` and uses the
tracked ApplicationSet to manage `argocd/` and each directory under `apps/`.
See the root [README](../README.md) for the full home-lab setup sequence.

### 1. Access the Argo CD Dashboard

Since Argo CD is running on your Raspberry Pi and you're connecting from another device, use `kubectl` port-forwarding to access the Argo CD server securely:

1. On your local machine, open a terminal and run:

   ```bash
   kubectl port-forward svc/argocd-server --namespace argocd 8080:443
   ```

   This forwards port 8080 on your local machine to port 443 (HTTPS) on the Argo CD server.

2. Open your browser and go to: `https://localhost:8080`

3. You'll see a login page requesting credentials
   - The default username is `admin`
   - The password was saved to `argocd-initial-admin-password` file on the Raspberry Pi

4. You may see a certificate warning because you're accessing via `localhost`. Click **Advanced** or **Proceed Anyway** to continue (this is normal for local development).

**Tip**: If you lose the password, reset it by running on the Raspberry Pi:

```bash
kubectl --namespace argocd account update-password admin <new-password>
```

**Keep the port-forward running**: Leave the terminal with `kubectl port-forward` open while you use the Argo CD dashboard. When you're done, press `Ctrl+C` to close the port-forward.

### 2. Change Your Password (Recommended)

On first login, it's strongly recommended to change the default password:

1. Log in with the default credentials
2. Click your username in the top-right corner
3. Select **User Info**
4. Click **Update Password**
5. Enter your current password and the new password
6. Click **Update**

### 3. Bootstrap and Verify Repository Applications

Before bootstrapping, create the Tailscale `operator-oauth` Secret if you plan
to deploy the operator. The ApplicationSet automatically syncs `apps/tailscale`
when applied, so the Secret must exist first. See
[`apps/tailscale/README.md`](../apps/tailscale/README.md) for the supported
secret setup methods.

For a new installation, run the repository bootstrap script from the repository
root:

```bash
./scripts/install-argocd
```

For an existing Argo CD installation that does not yet have the tracked
ApplicationSet, run:

```bash
./scripts/bootstrap-argocd
```

The ApplicationSet watches `apps/*` and `argocd`, enables automatic sync, and
creates each destination namespace. Verify the generated Applications with:

```bash
kubectl get applications --namespace argocd
```

### 4. Understanding the Application Status

After the ApplicationSet creates an application, you'll see it listed on the dashboard. Here's what the status indicators mean:

| Status           | Meaning                                                         |
| ---------------- | --------------------------------------------------------------- |
| 🟢 **Synced**    | Cluster state matches Git repository (everything is up-to-date) |
| 🟡 **OutOfSync** | Cluster state differs from Git repository (changes are pending) |
| 🔴 **Error**     | Argo CD encountered an error deploying the application          |
| ⏳ **Syncing**   | Argo CD is currently applying changes to the cluster            |

### 5. Manually Sync Application Changes

If you have **Automatic** sync enabled, Argo CD checks for changes every few minutes. To manually trigger a sync:

1. Click on your application in the dashboard
2. Click the **Sync** button in the top-right
3. Review the changes that will be applied
4. Click **Synchronize** to apply them immediately

### 6. Monitor Deployment Progress

While your application syncs:

1. The dashboard shows real-time status updates
2. Click on your application to see detailed information about each Kubernetes resource
3. You can view logs from the **Logs** tab
4. The **Tree** view shows the hierarchy of deployed resources (Deployments, Pods, Services, etc.)

## Understanding Manifest Organization

The tracked ApplicationSet discovers application directories and the Argo CD
configuration. The repository layout is:

```
home-lab/
├── argocd/                          # Argo CD installation and supporting resources
│   ├── core/
│   │   └── kustomization.yaml       # Pinned upstream Argo CD release
│   ├── application-set.yaml         # Discovers apps and manages this directory
│   ├── proxy-group.yaml             # Tailscale ingress proxy group
│   ├── argocd-server-ingress.yaml   # Private ingress for Argo CD UI
│   └── kustomization.yaml           # Composes Argo CD supporting resources
├── apps/
│   └── tailscale/                   # Tailscale Kubernetes Operator
├── kube-system/                     # Reserved for kube-system namespace manifests
├── scripts/                         # Installation and admin scripts
└── ...other project files
```

The checked-in ApplicationSet watches both the `apps/` directory and the
`argocd/` directory. The latter is a Kustomize source containing the pinned
upstream Argo CD installation, the ApplicationSet, and the UI ingress, so Argo
CD reconciles its own installation as well as its supporting resources.

### Tailscale ingress

The tracked ingress uses `ingressClassName: tailscale`, references the
`argocd-ingress-proxies` `ProxyGroup`, and requests TLS for the `argocd` host.
Tailscale terminates TLS at the ingress; the Argo CD server is configured for
insecure HTTP behind it to avoid HTTPS redirect loops.

## GitOps Workflow

Now that Argo CD is configured, this is how deployments work:

1. **Make Changes**: Edit YAML manifest files in your local repository
2. **Commit**: `git commit --message "deploy: add new service"`
3. **Push**: `git push origin main`
4. **Sync**: Argo CD detects the change and automatically deploys it (or manually sync if you prefer)
5. **Monitor**: Use the Argo CD dashboard to watch the deployment progress

This declarative approach ensures your cluster state always matches your Git repository.

### Argo CD Self-Management and Upgrades

The Argo CD release is pinned in `argocd/core/kustomization.yaml`, which
references the official versioned install manifest. Renovate checks for newer
Argo CD tags and opens a pull request for that pin. After the pull request is
reviewed and merged, the ApplicationSet-managed `argocd` Application
automatically syncs the new release. The core resources use server-side apply
to avoid client-side annotation-size failures, matching the bootstrap script.

The `scripts/install-argocd` script uses the same Kustomize source and applies
the ApplicationSet. Use it for initial bootstrap or recovery; routine upgrades
are applied by Argo CD after the version update is merged.

## Common Tasks

### Update an Existing Deployment

1. Edit the relevant application under `apps/<name>/` or shared Argo CD configuration under `argocd/`
2. Commit and push your changes to Git
3. Argo CD automatically detects the change and updates the deployment
4. Monitor the sync progress in the dashboard

### Disable Automatic Sync

Generated Applications follow the sync policy in `argocd/application-set.yaml`.
To disable automatic sync for generated Applications, remove the `automated`
entry from the ApplicationSet template and commit that change. Editing a
generated Application in the UI is not the source of truth and may be reverted
by the ApplicationSet controller.

### Rollback a Failed Deployment

Revert the Git commit that introduced the failed deployment. Argo CD will sync
the restored manifests and bring the cluster back to the desired state. For a
temporary manual recovery, first change the ApplicationSet sync policy in Git.

## Adding an Application

Create an application directory under `apps/` and include a `kustomization.yaml`
or manifests that Argo CD can render. The ApplicationSet creates an Application
named after the directory, targets a namespace with the same name, and enables
automatic sync and namespace creation.

```bash
mkdir --parents apps/my-new-app
```

After adding the manifests and committing the changes, Argo CD discovers the
directory and syncs it automatically. See the
[ApplicationSet manifest](application-set.yaml) for the generator and sync
policy.

## Troubleshooting

### Application Status Shows "OutOfSync"

**Cause**: Your Git repository has changes that haven't been applied to the cluster yet.

**Solution**:

- Check that your manifests are valid YAML
- Ensure the manifests are in a discovered path: `apps/<name>/` or `argocd/`
- Click **Sync** to manually apply the changes
- Check application logs for error messages

### Getting "No resources found" Error

**Cause**: The specified path in your Application configuration doesn't contain any YAML files.

**Solution**:

- Verify the application source path matches a discovered directory under
  `apps/` or the tracked `argocd/` path
- Ensure YAML files have `.yaml` or `.yml` extensions
- Check that files aren't hidden files or in ignored directories

### Cannot Connect to Repository

**Cause**: Git credentials are incorrect or the repository URL is invalid.

**Solution**:

- Verify the repository URL is correct
- For HTTPS: Ensure your GitHub personal access token has the required permissions
- For SSH: Verify your SSH key has access to the repository
- Run `git clone <repo-url>` locally to test connectivity

### Deployment Stuck in "Syncing" State

**Cause**: Usually a resource is waiting on an external dependency or condition.

**Solution**:

- Check the application logs for error messages
- Verify all image registries are accessible
- Ensure sufficient cluster resources (CPU, memory, disk space)
- Check Kubernetes events: `kubectl describe pod <pod-name>`

### Need to See More Details

To troubleshoot further, use kubectl commands:

```bash
# Check Argo CD application status
kubectl get application --namespace argocd

# Describe an application for details
kubectl describe application <app-name> --namespace argocd

# Check Argo CD server logs
kubectl logs --namespace argocd deployment/argocd-server

# Check Argo CD repo server logs
kubectl logs --namespace argocd deployment/argocd-repo-server
```

## Next Steps

Once you're comfortable with Argo CD basics:

1. **Organize Manifests**: Create separate manifests for each application
2. **Use Kustomize or Helm**: For more complex deployments, consider using Kustomize overlays or Helm charts
3. **Set Up Notifications**: Configure webhooks to be notified of sync events
4. **Implement RBAC**: Restrict Argo CD access to specific users or teams
5. **Monitor Health**: Set up alerts for deployment failures

## Resources

- [Argo CD Official Documentation](https://argo-cd.readthedocs.io/)
- [Argo CD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [Kubernetes Declarative Management](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)

---

**Happy GitOps!** 🚀
