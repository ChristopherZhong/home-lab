# Argo CD Configuration Guide

Welcome! This guide walks you through configuring Argo CD for GitOps in the home lab. After Argo CD is installed, these steps will help you set up automated deployments from this Git repository to your Kubernetes cluster.

## What is Argo CD?

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It simplifies deployments by:

- **Declaring desired state in Git**: You define what should run on your cluster in YAML files committed to this repository
- **Automatically syncing**: Argo CD continuously watches this repository and applies any changes to your Kubernetes cluster
- **Providing a dashboard**: A web UI lets you monitor deployments, check status, and manually sync if needed

## Getting Started

https://argo-cd.readthedocs.io/en/stable/getting_started/

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

### 3. Connect Your Git Repository

Argo CD needs to know where to pull your cluster configuration from. Set up the connection to this repository:

1. In the Argo CD dashboard, click **Settings** (gear icon) in the left sidebar
2. Select **Repositories** → **Connect Repo**
3. Choose **VIA HTTPS** or **VIA SSH** based on your setup
4. Fill in these fields:
   - **Repository URL**: `https://github.com/ChristopherZhong/home-lab.git` (or your fork)
   - **Username**: Your GitHub username (HTTPS only)
   - **Password**: Your GitHub personal access token (HTTPS only)
   - **TLS client cert data** / **TLS client cert key**: (Leave blank unless using client certificates)
5. Click **Connect**

Once connected, you should see a status message confirming the connection succeeded.

### 4. Create Your First Application

An Argo CD Application tells Argo CD which manifests to deploy and where to deploy them. Here's how to create one:

1. Click the **+ New App** button in the top-left of the Argo CD dashboard
2. Fill in the **Application Details**:
   - **Application Name**: `home-lab` (or your preferred name)
   - **Project**: Leave as `default`
   - **Sync Policy**: Select **Automatic** (Argo CD will automatically sync changes)
3. Configure the **Source** (where your manifests are):
   - **Repository URL**: Select the repository you just connected
   - **Revision**: `main` (the branch to track)
   - **Path**: `./` (the root folder to watch for manifests)
4. Configure the **Destination** (where to deploy):
   - **Cluster**: `https://kubernetes.default.svc` (your local cluster)
   - **Namespace**: `default` (can change for different namespaces)
5. Click **Create** at the top

Your application is now created and Argo CD will begin synchronizing manifests from the repository.

### 5. Understanding the Application Status

After creating an application, you'll see it listed on the dashboard. Here's what the status indicators mean:

| Status | Meaning |
|--------|---------|
| 🟢 **Synced** | Cluster state matches Git repository (everything is up-to-date) |
| 🟡 **OutOfSync** | Cluster state differs from Git repository (changes are pending) |
| 🔴 **Error** | Argo CD encountered an error deploying the application |
| ⏳ **Syncing** | Argo CD is currently applying changes to the cluster |

### 6. Manually Sync Application Changes

If you have **Automatic** sync enabled, Argo CD checks for changes every few minutes. To manually trigger a sync:

1. Click on your application in the dashboard
2. Click the **Sync** button in the top-right
3. Review the changes that will be applied
4. Click **Synchronize** to apply them immediately

### 7. Monitor Deployment Progress

While your application syncs:

1. The dashboard shows real-time status updates
2. Click on your application to see detailed information about each Kubernetes resource
3. You can view logs from the **Logs** tab
4. The **Tree** view shows the hierarchy of deployed resources (Deployments, Pods, Services, etc.)

## Understanding Manifest Organization

Argo CD deploys all YAML files in your specified path. Organize your manifests like this:

```
home-lab/
├── argocd/                          # Application manifests deployed by Argo CD
│   ├── README.md                    # This file
│   ├── argocd-server-ingress.yaml   # Example: Ingress for Argo CD UI
│   └── ...other-manifests.yaml      # Add your application manifests here
├── kube-system/                     # Reserved for kube-system namespace manifests
├── scripts/                         # Installation and admin scripts
└── ...other project files
```

Argo CD monitors the `./argocd/` directory by default. Place your application manifests there.

## GitOps Workflow

Now that Argo CD is configured, this is how deployments work:

1. **Make Changes**: Edit YAML manifest files in your local repository
2. **Commit**: `git commit -m "deploy: add new service"`
3. **Push**: `git push origin main`
4. **Sync**: Argo CD detects the change and automatically deploys it (or manually sync if you prefer)
5. **Monitor**: Use the Argo CD dashboard to watch the deployment progress

This declarative approach ensures your cluster state always matches your Git repository.

## Common Tasks

### Update an Existing Deployment

1. Edit the relevant YAML file in the `argocd/` directory
2. Commit and push your changes to Git
3. Argo CD automatically detects the change and updates the deployment
4. Monitor the sync progress in the dashboard

### Disable Automatic Sync

If you want to review changes before applying them:

1. Click your application in the dashboard
2. Click **App Details** in the top-right
3. Find **Sync Policy** and toggle **Automatic Sync** to **Manual**
4. Now you must manually click **Sync** to deploy changes

### Rollback a Failed Deployment

If a deployment caused problems:

1. Click your application in the dashboard
2. Click the **History** tab
3. Find the previous stable revision
4. Click the revision and select **Rollback**

## Advanced: Auto-Discovering Applications with ApplicationSet

As your home lab grows and you manage multiple applications, manually creating each Application becomes tedious. Argo CD's **ApplicationSet** feature automatically discovers and deploys applications based on patterns in your Git repository.

### Why Use ApplicationSet?

- **Scalability**: Manage dozens or hundreds of applications without manual configuration
- **Consistency**: All auto-discovered applications follow the same template
- **Less manual work**: Add new applications by simply creating a new directory
- **True GitOps**: Everything is declared in Git, including application discovery rules

### Example: Auto-Discover Applications by Directory

Create an ApplicationSet that automatically discovers applications in subdirectories:

1. Create a file `argocd/application-set.yaml`:

   **Note**: The filename doesn't matter—Kubernetes only cares about the resource `kind` (ApplicationSet in this case). You could name it `app-discovery.yaml`, `auto-apps.yaml`, or anything else. We use `application-set.yaml` for clarity.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: home-lab-apps
  namespace: argocd
spec:
  generators:
    # Use Git generator to scan repository directories
    - git:
        repoURL: https://github.com/ChristopherZhong/home-lab.git
        revision: main
        directories:
          - path: 'apps/*'
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/ChristopherZhong/home-lab.git
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

2. Commit and push the file to your Git repository:
   ```bash
   git add argocd/application-set.yaml
   git commit --message "feat: add ApplicationSet for auto-discovery"
   git push origin main
   ```

3. Argo CD will automatically deploy this ApplicationSet, which will then scan the `apps/` directory and create an Application for each subdirectory

### Directory Structure for Auto-Discovery

For the example above, organize your applications like this:

```
home-lab/
├── argocd/
│   ├── README.md
│   ├── argocd-server-ingress.yaml
│   └── application-set.yaml         # ApplicationSet configuration
├── apps/                            # Auto-discovered applications
│   ├── my-service-1/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── my-service-2/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── my-service-3/
│       └── kustomization.yaml
└── scripts/
```

Now, when you create a new subdirectory under `apps/`, Argo CD automatically creates an Application for it!

### Adding a New Application

To add a new application when using ApplicationSet:

1. Create a new directory under `apps/` with your application manifests:
   ```bash
   mkdir -p apps/my-new-app
   # Add your Kubernetes manifests here
   ```

2. Commit and push:
   ```bash
   git add apps/my-new-app/
   git commit --message "feat: add my-new-app deployment"
   git push origin main
   ```

3. Argo CD automatically detects the new directory and deploys it within minutes (or manually sync to deploy immediately)

### Generator Types

ApplicationSet supports different generators for discovery:

| Generator | Use Case |
|-----------|----------|
| **Git** | Scan Git repository directories or branches |
| **List** | Create applications from a static list |
| **Cluster** | Generate applications across multiple clusters |
| **SCM** | Auto-discover repositories from GitHub, GitLab, Gitea |
| **Template** | Apply templates to complex scenarios |

For more information, see the [Argo CD ApplicationSet documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/).

## Troubleshooting

### Application Status Shows "OutOfSync"

**Cause**: Your Git repository has changes that haven't been applied to the cluster yet.

**Solution**: 
- Check that your manifests are valid YAML
- Ensure the manifests are in the correct path (`./` or your configured path)
- Click **Sync** to manually apply the changes
- Check application logs for error messages

### Getting "No resources found" Error

**Cause**: The specified path in your Application configuration doesn't contain any YAML files.

**Solution**:
- Verify the **Path** is correct (e.g., `./`, `./argocd/`)
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
