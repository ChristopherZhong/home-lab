# 🏡 Kubernetes Home Lab

A comprehensive guide to building a production-ready Kubernetes home lab, starting with a single Raspberry Pi 5 and growing incrementally. This project documents the journey of learning Kubernetes while building a well-structured cluster for home use.

## 📁 Current Repository State

The repository currently tracks:

- `argocd/argocd-server-ingress.yaml`: Ingress manifest for exposing `argocd-server` through Traefik
- `.agents/agents/`: Shared custom agent definitions for this repository
- `.agents/prompts/`: Reusable prompt templates for repository workflows, general reusable tasks, and human or agent use
- `.agents/skills/`: Shared reusable skills in an open-standard style location
- `scripts/init`: K3s bootstrap script for server or agent mode
- `scripts/install-argocd`: Argo CD installation script
- `scripts/upgrade`: K3s upgrade script
- `kube-system/`: Reserved for future `kube-system` namespace manifests and currently empty

## 🤖 AI Assets

This repository stores canonical AI assets under `.agents/`. See
`AGENTS.md` for repository-wide guidance and the canonical locations for
agents, prompts, and skills.

## 🎯 Project Goals

- ✅ **Document Home Lab Build**: Step-by-step instructions for building a Kubernetes home lab from scratch
- ✅ **Learn Kubernetes**: Hands-on experience with Kubernetes concepts, tools, and best practices
- 🟡 **Incremental Growth**: Start simple with one node and expand the cluster over time
- 🟡 **Production Practices**: Implement monitoring, security, and operational best practices

## 🏗️ Architecture Overview

The home lab starts with a single Raspberry Pi 5 and can be expanded to a multi-node cluster:

- **Hardware**: Raspberry Pi 5 with M.2 NVMe SSD for improved I/O performance
- **OS**: Raspberry Pi OS (headless configuration)
- **Kubernetes Distribution**: K3s (lightweight, perfect for edge/IoT scenarios)
- **Storage**: Local storage with expansion to distributed storage solutions
- **Networking**: Traefik for ingress and load balancing

---

## 🗺️ Road Map

Here is the plan for building the home lab.

### ✅ Phase 1: Initial Setup
1. [x] [Step 1: Prepare Raspberry Pi OS](#step-1-prepare-raspberry-pi-os)
    1. [x] Download Raspberry Pi Imager
    1. [x] Flash Raspberry Pi OS
    1. [x] Generate SSH Key Pair
    1. [x] Boot from NVMe SSD
    1. [x] Initial Boot and Setup (SSH, System Updates)
    1. [x] Install and Configure Git
1. [x] [Step 2: Install Kubernetes (K3s)](#step-2-install-kubernetes-k3s)
    - [x] Enable cgroups
    - [x] Install K3s
    - [ ] (Optional) Configure kubectl for non-root user
    - [ ] (Optional) Install kubectl on local machine
1. [x] [Step 3: Argo CD - Declarative GitOps](#step-3-argo-cd---declarative-gitops)
1. [ ] [(Optional) Step 4: Install Helm](#optional-step-4-install-helm)

### 🟡 Phase 2: Core Services
- [ ] **Networking**: Configure Traefik Ingress Controller
- [ ] **Monitoring and Observability**: Grafana Setup
- [ ] **Security and Secrets Management**: Kubernetes Dashboard, Infisical
- [ ] **Database Services**: PostgreSQL with CloudNativePG

### 📝 Phase 3: Expanding the Cluster

- [ ] **Add Worker Nodes**: Install additional Raspberry Pis and join them to the cluster
- [ ] **High Availability**: Configure multiple master nodes for production resilience
- [ ] **Storage Solutions**: Implement Longhorn or other distributed storage
- [ ] **Service Mesh**: Explore Istio or Linkerd for advanced networking

### 🚀 Phase 4: Advanced Topics

- [ ] **Advanced Monitoring**: Prometheus Stack, Log Aggregation, Distributed Tracing
- [ ] **Security Hardening**: Network Policies, Pod Security Standards, RBAC, Certificate Management

---

## 🚀 Getting Started

Details for the completed steps are below.

### Prerequisites

- Raspberry Pi 5 (8 GB or more RAM recommended)
- M.2 NVMe SSD (512 GB or larger recommended)
- MicroSD card (for initial boot)
- Network connection (Ethernet preferred)
- Another computer for SSH access

### **Step 1**: Prepare Raspberry Pi OS

The following instructions are for preparing the SSD. We assume that the SD card is already flashed. If not, the following instructions may still work.

1. **Download Raspberry Pi Imager** from https://www.raspberrypi.com/software/.

1. **Flash Raspberry Pi OS**
   - Use Raspberry Pi Imager to flash Raspberry Pi OS Lite (64-bit) to your SSD.
   - **Important**: Configure the following in Advanced Options:
     - **Hostname**: Set to `raspberrypi-1` (or your preferred hostname)
     - **Enable SSH**: Use public-key authentication only (recommended)
     - **Set username**: `pi` (or your preferred username)
     - **SSH Public Key**: Paste your Ed25519 public key (see SSH key generation below)
     - Configure WiFi if needed (Ethernet recommended)
     - Set locale settings

1. **Generate SSH Key Pair** (if you don't have one)
   ```shell
   # On your local machine, generate Ed25519 key (most secure and performant)
   $ ssh-keygen --type ed25519 --comment "you@example.com"
   
   # Display your public key to copy into Raspberry Pi Imager
   $ cat ~/.ssh/id_ed25519.pub
   ```

   **Note**: Copy the entire public key output and paste it into the SSH Public Key field in Raspberry Pi Imager.

1. **Booting from the M.2 NVMe SSD**. Follow the official instructions on how to boot from the SSD [here](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#nvme-ssd-boot).

1. **Initial Boot and Setup**
   ```shell
   # SSH into your Pi using the hostname or IP
   $ ssh pi@raspberrypi-1.local
   
   # Update the system
   $ sudo apt update
   $ sudo apt full-upgrade --yes
   ```

1. **Install Git**
   ```shell
   # Install Git to clone this repository
   $ sudo apt install --yes git
   ```

1. **Configure Git**. First configure the user name and email.
   ```shell
   $ git config --global user.name "John Doe"
   $ git config --global user.email johndoe@example.com
   ```
   For more details see the [docs](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).

### **Step 2**: Install Kubernetes (K3s)

[K3s](https://k3s.io/) is chosen for its lightweight nature and excellent ARM64 support.

This repository currently pins K3s to `v1.35.0+k3s1` in the helper scripts for reproducible installs and upgrades.

1. **Enable cgroups**
   K3s needs `cgroups` to be enabled (see https://docs.k3s.io/installation/requirements?os=pi).
   Append `cgroup_memory=1 cgroup_enable=memory` to `/boot/firmware/cmdline.txt` and reboot.

1. **Install K3s**. Follow the Quick-Start [guide](https://docs.k3s.io/quick-start).
   ```shell
   # Install K3s
   $ curl --silent --fail --location https://get.k3s.io | INSTALL_K3S_VERSION="v1.35.0+k3s1" sh -
   
   # Verify installation
   $ sudo systemctl status k3s
   
   # Check nodes
   $ sudo kubectl get nodes
   ```

   **Note**: An initialization script ([init](./scripts/init)) is provided that can initialize K3s in either server or agent mode.
   ```shell
   $ ./scripts/init
   ```

1. **Upgrade K3s**. Follow the instructions in this [guide](https://docs.k3s.io/upgrades) to upgrade K3s.

   **Note**: The provided script upgrades to the pinned repository version `v1.35.0+k3s1`:
   ```shell
   $ ./scripts/upgrade
   ```

1. **Optional: Configure kubectl for non-root user**
   ```shell
   # Copy kubeconfig to user directory
   $ mkdir --parents ~/.kube
   $ sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
   $ sudo chown $USER:$USER ~/.kube/config
   
   # Test access
   $ kubectl get all --all-namespaces
   ```

1. **Optional: Install kubectl on your local machine**
   ```shell
   # Copy the kubeconfig from Pi to your local machine
   $ scp pi@192.168.1.100:/etc/rancher/k3s/k3s.yaml ~/.kube/config-home-lab
   
   # Edit the server URL in the config file to point to your Pi's IP
   # Then use: export KUBECONFIG=~/.kube/config-home-lab
   ```

### **Step 3**: Argo CD - Declarative GitOps

Argo CD setup and operational guidance are maintained in a dedicated guide:
see `argocd/README.md` for full installation and configuration steps.

Use `./scripts/install-argocd` to install the pinned Argo CD version and see
`argocd/argocd-server-ingress.yaml` for the tracked ingress manifest.

**Bootstrapping Applications**

If you connected this Git repository to Argo CD, Argo CD can read the repo, but
it will not create `Application` or `ApplicationSet` Kubernetes resources in the
cluster by itself. To instruct Argo CD to manage the `apps/*` directories you
must apply an `ApplicationSet` (or an `Application`) resource into the cluster
so the Argo CD controllers can generate and sync Applications.

To apply the provided `ApplicationSet` manifest (recommended):

```bash
sudo kubectl --namespace argocd apply --filename argocd/application-set.yaml
```

After applying, Argo CD will create one `Application` per directory under
`apps/*`. You can verify generated Applications with:

```bash
sudo kubectl --namespace argocd get applications
sudo kubectl --namespace argocd get applicationsets
```

If you prefer an "app-of-apps" bootstrap approach, apply a single Argo CD
`Application` that points at the `argocd/` path. Argo CD will then sync the
`ApplicationSet` manifest from Git and create the per-app `Application` objects:

```bash
sudo kubectl --namespace argocd apply --filename - <<'EOF'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
   name: bootstrap-argocd
   namespace: argocd
spec:
   project: default
   source:
      repoURL: https://github.com/ChristopherZhong/home-lab.git
      targetRevision: main
      path: argocd
   destination:
      server: https://kubernetes.default.svc
      namespace: argocd
   syncPolicy:
      automated:
         prune: true
         selfHeal: true
EOF
```

Secrets: do NOT commit plaintext credentials. Use one of the options below:
- CI secret injection (recommended for CI/CD pipelines)
- ExternalSecrets controllers (e.g. ExternalSecrets, SealedSecrets)
- Local out-of-band script: run `./scripts/create-tailscale-secret` and provide
   `--client-id` and `--client-secret` via environment variables or flags. Example:

```bash
# interactive (prompts for values)
sudo ./scripts/create-tailscale-secret

# non-interactive (use environment variables)
sudo TS_CLIENT_ID="<id>" TS_CLIENT_SECRET="<secret>" \
   ./scripts/create-tailscale-secret --namespace tailscale
```

See `apps/tailscale/README.md` for operator-specific notes and `.harness/`
for long-term learnings.


### (*Optional*) **Step 4**: Install Helm

```shell
# Install Helm
$ curl --silent --fail --location https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Check that Helm is installed
$ helm version
```

## 📊 Monitoring and Observability

### Grafana Setup
Deploy Grafana for monitoring and visualization:

```shell
# Create grafana namespace
kubectl create namespace grafana

# Deploy Grafana
kubectl apply -f grafana/grafana.yaml

# Access Grafana at: http://<PI_IP>:3000
# Default credentials: admin/admin
```

## 🔐 Security and Secrets Management

### Kubernetes Dashboard
```shell
# Install Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Create admin user
kubectl apply -f kubernetes-dashboard/kubernetes-dashboard-admin-user.yml
kubectl apply -f kubernetes-dashboard/kubernetes-dashboard-admin-user-binding.yml

# Get access token
kubectl -n kubernetes-dashboard create token admin-user
```

### Infisical (Secrets Management)
```shell
# Add Infisical Helm repository
helm repo add infisical-helm-charts 'https://dl.cloudsmith.io/public/infisical/helm-charts/helm/charts/'
helm repo update

# Create namespace
kubectl create namespace infisical

# Apply secrets
kubectl apply -f infisical/infisical-secrets.yaml

# Install Infisical
helm install infisical infisical-helm-charts/infisical -f infisical/values.yaml -n infisical
```

## 💾 Database Services

### PostgreSQL with CloudNativePG
```shell
# Install CloudNativePG operator
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.20/releases/cnpg-1.20.0.yaml

# Create postgres namespace
kubectl create namespace postgres

# Deploy PostgreSQL cluster
kubectl apply -f postgres/k8s.yaml
```

## 🔧 Useful Commands

### Cluster Management
```shell
# View all resources across namespaces
$ kubectl get all --all-namespaces

# Describe a problematic pod
$ kubectl describe pod <pod-name> --namespace <namespace>

# View logs
$ kubectl logs <pod-name> --namespace <namespace> --follow

# Port forward for local access
$ kubectl port-forward svc/<service-name> 8080:80 --namespace <namespace>

# Scale deployment
$ kubectl scale deployment <deployment-name> --replicas=3 --namespace <namespace>
```

### Troubleshooting
```shell
# Check node resources
$ kubectl top nodes

# Check pod resources
$ kubectl top pods --all-namespaces

# View events
$ kubectl get events --sort-by=.metadata.creationTimestamp

# Check cluster info
$ kubectl cluster-info

# Verify K3s status
$ sudo systemctl status k3s
```

## 📚 Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [K3s Documentation](https://docs.k3s.io/)
- [Raspberry Pi Kubernetes Cluster](https://github.com/k8s-at-home/awesome-home-kubernetes)
- [CloudNative Landscape](https://landscape.cncf.io/)

## 🤝 Contributing

This is a learning project! Feel free to:
- Suggest improvements to the setup process
- Share your own home lab configurations
- Report issues or corrections
- Add new service configurations

## 📝 Notes

- **Performance**: Raspberry Pi 5 with NVMe SSD provides excellent performance for a home lab
- **Power**: Consider a UPS for production-like uptime
- **Networking**: Static IP configuration recommended for stability
- **Backups**: Regular etcd backups are crucial for cluster recovery

---

*Last updated: 2026-04-18*
*Cluster Status: Single Node (Raspberry Pi 5)*
