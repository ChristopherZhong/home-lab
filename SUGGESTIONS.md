# Suggestions

- Consider moving the ingress class from the `metadata.annotations` block to `spec.ingressClassName` in `argocd/argocd-server-ingress.yaml`. That matches the native field in `networking.k8s.io/v1` Ingress resources more closely.
