# Contributing

## Before you start

- Read [AGENTS.md](AGENTS.md) and the rule files under [.agents/rules](.agents/rules) for repository conventions.
- Keep shell commands in long-form form, such as `--namespace` rather than `-n`.
- Follow Conventional Commits for commit messages.
- Review the repository-specific guidance in [README.md](README.md) when changing Kubernetes or GitOps-related content.

## Pull requests

- Open a pull request for changes to any repository content, including [.agents](.agents), [scripts](scripts), Kubernetes manifests under [argocd](argocd), and application configuration under [apps](apps).
- Include a brief summary of the change, the reason for it, and any validation performed.
- If your change touches Kubernetes manifests, scripts, or GitOps automation, mention the expected impact and any rollout considerations.

## Review expectations

- Changes across the repository should preserve naming conventions, reference integrity, and documented workflow expectations.
- Avoid introducing secrets or credentials into the repo.
- Keep documentation and automation changes aligned with the repository guidance in [AGENTS.md](AGENTS.md).
