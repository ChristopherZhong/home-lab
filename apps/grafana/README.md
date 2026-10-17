# Grafana

This Argo CD application deploys Grafana with a persistent data volume and
private HTTPS ingress through the Tailscale Kubernetes Operator. Prometheus
and metrics collection are not included yet, so the initial Grafana instance
will not have a metrics data source. No Kubernetes Secret is required to
bootstrap Grafana.

## First login

The ApplicationSet automatically discovers `apps/grafana`, creates its
namespace, and syncs the application. The Tailscale operator must already be
installed and connected to the tailnet.

After Argo CD syncs the application, open `https://grafana.<your-tailnet-domain>`
from a device connected to the tailnet. Sign in with the initial credentials
`admin` / `admin` and immediately set a unique password in Grafana. Anyone
allowed to reach the Tailscale hostname could otherwise try the default
credentials.

Grafana stores the changed password in its persistent database. Grafana data
is stored in a 2 GiB `local-path` volume on the node; it is not replicated and
will not survive loss of that node or its disk.
