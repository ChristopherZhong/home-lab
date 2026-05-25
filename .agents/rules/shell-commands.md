# Shell and CLI Command Standards

All shell and CLI commands in code, scripts, and documentation must use long-form options to ensure clarity and readability for all users, including beginners.

## Rule

- **Use long-form options only, never short forms**
- Applies to: kubectl, git, bash, sh, and all CLI tools
- Purpose: Improve readability and reduce ambiguity

## Examples

### kubectl

✅ **Good:**
```bash
kubectl port-forward svc/argocd-server --namespace argocd 8080:443
kubectl logs --namespace argocd deployment/argocd-server
kubectl get application --namespace argocd
```

❌ **Bad:**
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl logs -n argocd deployment/argocd-server
kubectl get application -n argocd
```

### git

✅ **Good:**
```bash
git commit --message "feat: add new feature"
git branch --list
git checkout --branch main
```

❌ **Bad:**
```bash
git commit -m "feat: add new feature"
git branch -l
git checkout -b main
```

### Other Tools

✅ **Good:**
```bash
grep --recursive --include="*.md" "search term"
find . --type f --name "*.yaml"
```

❌ **Bad:**
```bash
grep -r -i "*.md" "search term"
find . -t f -n "*.yaml"
```

## Notes

- This standard applies to documentation, scripts, code comments, and all examples
- Users who check out this repository should be able to understand and run commands without prior knowledge
