#!/usr/bin/env python3
"""Validate an agents tree.

Two modes, detected by the presence of agents/:

  payload    validate the distributable payload, including genericity
  installed  validate the installed .agents/ tree

Standard library only. No git dependency.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SEVERITY_ORDER = {"error": 0, "warning": 1}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

# Files exempt from the genericity scan. The validator must name the terms
# it forbids, so it cannot pass its own check.
GENERICITY_EXEMPT = {"scripts/validate.py"}

DENYLIST = [
    r"home[\s_-]?lab",
    r"\bk3s\b",
    r"\bkubernetes\b",
    r"\bkubectl\b",
    r"\bargo\s?cd\b",
    r"\bargocd\b",
    r"kube-system",
    r"\btailscale\b",
    r"\btraefik\b",
]

ABSOLUTE_PATHS = [
    r"/home/[A-Za-z0-9_.-]+",
    r"/Users/[A-Za-z0-9_.-]+",
    r"[A-Za-z]:\\\\Users\\\\",
]

SECRETS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key"),
    (r"\bghp_[A-Za-z0-9]{36}\b", "GitHub token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{22,}\b", "GitHub fine-grained token"),
    (r"\bsk-[A-Za-z0-9]{20,}\b", "API key"),
]

# Frontmatter keys that must never appear. A file's state is derived from
# presence at the recorded commit, at HEAD, and on disk. Nothing declares it.
FORBIDDEN_FRONTMATTER = {"mode"}

KEBAB = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
REFERENCE = re.compile(r"\.agents/[A-Za-z0-9_.\-/]+")
EXPLICIT_ORDER = re.compile(r"^\s*(?:[2-9]|[1-9][0-9]+)\.\s")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt"}

# References that are created by sync rather than shipped in the payload.
REFERENCE_EXEMPT = {".agents/config.yaml"}


# --- parsing ---------------------------------------------------------------


def _scalar(text: str):
    text = text.strip()
    if text in ("", "null", "~"):
        return None
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def parse_simple_yaml(text: str) -> dict:
    """Parse the YAML subset this project uses.

    Supports scalars, flat lists, and one level of nesting. Anything else is
    ignored rather than guessed at.
    """
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    pending: tuple[dict, str] | None = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1] if stack else root

        if stripped.startswith("- "):
            if pending is None:
                continue
            parent, key = pending
            if not isinstance(parent.get(key), list):
                parent[key] = []
            parent[key].append(_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key, value = key.strip(), value.strip()

        if value == "":
            child: dict = {}
            container[key] = child
            stack.append((indent, child))
            pending = (container, key)
        else:
            container[key] = _scalar(value)
            pending = None

    return root


def read_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return parse_simple_yaml(text[3:end])


def walk_dir(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return [
        child
        for child in sorted(path.rglob("*"))
        if child.is_file() and not any(part in SKIP_DIRS for part in child.parts)
    ]


def assets_base(root: Path, payload_mode: bool) -> Path:
    """The directory that holds rules/, skills/, prompts/, and agents/."""
    return root / "agents" if payload_mode else root / ".agents"


def resolve_reference(root: Path, reference: str, payload_mode: bool) -> Path:
    """Map a .agents/ reference to the file that should exist."""
    if not payload_mode:
        return root / reference
    if reference == ".agents/AGENTS.md":
        return root / "agents" / "AGENTS.md"
    if reference.startswith(".agents/"):
        return root / "agents" / reference[len(".agents/"):]
    return root / reference


def payload_target(relative: str) -> str:
    if relative == "AGENTS.md":
        return "AGENTS.md"
    return f".agents/{relative}"


# --- checks ----------------------------------------------------------------


def check_structure(root: Path, payload_mode: bool):
    findings = []
    if payload_mode:
        payload = root / "agents"
        if not payload.is_dir():
            findings.append((Path("agents"), "error", "missing payload directory"))
            return findings
        for name in ("rules", "skills", "prompts", "agents", "scripts"):
            if not (payload / name).is_dir():
                findings.append((Path(f"agents/{name}"), "warning", "missing directory"))
        return findings

    if not (root / "AGENTS.md").is_file():
        findings.append((Path("AGENTS.md"), "error", "missing"))
    if not (root / ".agents").is_dir():
        findings.append((Path(".agents"), "error", "missing directory"))
    if not (root / ".agents" / "config.yaml").is_file():
        findings.append((Path(".agents/config.yaml"), "error", "missing"))
    for name in ("rules", "skills", "prompts", "agents", "scripts"):
        if not (root / ".agents" / name).is_dir():
            findings.append((Path(f".agents/{name}"), "warning", "missing directory"))
    return findings


def check_naming(root: Path, payload_mode: bool):
    findings = []
    seen: dict[str, dict[str, list[Path]]] = {}
    base = assets_base(root, payload_mode)

    for path in walk_dir(base / "skills"):
        if path.name != "SKILL.md":
            continue
        directory = path.parent.name
        if not KEBAB.match(directory):
            findings.append(
                (path, "error", f"skill directory '{directory}' is not <verb>-<noun>")
            )
        declared = read_frontmatter(path).get("name")
        if declared and declared != directory:
            findings.append(
                (path, "error", f"name '{declared}' does not match directory '{directory}'")
            )
        if declared:
            seen.setdefault("skill", {}).setdefault(str(declared), []).append(path)

    for path in walk_dir(base / "agents"):
        if not path.name.endswith(".agent.md"):
            findings.append((path, "error", "agent file must end with .agent.md"))
            continue
        stem = path.name[: -len(".agent.md")]
        if not KEBAB.match(stem):
            findings.append(
                (path, "error", f"agent name '{stem}' is not <workflow>-<actor>")
            )
        declared = read_frontmatter(path).get("name")
        if declared and declared != stem:
            findings.append(
                (path, "error", f"name '{declared}' does not match filename '{stem}'")
            )
        if declared:
            seen.setdefault("agent", {}).setdefault(str(declared), []).append(path)

    for path in walk_dir(base / "prompts"):
        if not path.name.endswith(".prompt.md"):
            findings.append((path, "error", "prompt file must end with .prompt.md"))

    for path in walk_dir(base / "rules"):
        if not path.name.endswith(".rule.md"):
            findings.append((path, "error", "rule file must end with .rule.md"))

    for kind, mapping in seen.items():
        for name, paths in mapping.items():
            if len(paths) > 1:
                findings.append((paths[1], "error", f"duplicate {kind} name '{name}'"))

    return findings


def check_frontmatter(root: Path, payload_mode: bool):
    findings = []
    base = assets_base(root, payload_mode)

    for path in walk_dir(base / "skills"):
        if path.name != "SKILL.md":
            continue
        meta = read_frontmatter(path)
        for key in ("name", "description"):
            if not meta.get(key):
                findings.append((path, "error", f"missing frontmatter '{key}'"))
        for key in sorted(FORBIDDEN_FRONTMATTER):
            if key in meta:
                findings.append(
                    (path, "error", f"frontmatter must not declare '{key}'")
                )

    for path in walk_dir(base / "agents"):
        if not path.name.endswith(".agent.md"):
            continue
        meta = read_frontmatter(path)
        for key in ("name", "description"):
            if not meta.get(key):
                findings.append((path, "error", f"missing frontmatter '{key}'"))
        for key in ("scope", "inputs", "outputs"):
            if not meta.get(key):
                findings.append((path, "warning", f"missing frontmatter '{key}'"))
        for key in sorted(FORBIDDEN_FRONTMATTER):
            if key in meta:
                findings.append(
                    (path, "error", f"frontmatter must not declare '{key}'")
                )

    return findings


def check_markdown_lists(root: Path, payload_mode: bool):
    """Ordered lists use 1. for every item, per the markdown rule."""
    findings = []
    for path in walk_dir(assets_base(root, payload_mode)):
        if path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if EXPLICIT_ORDER.match(line):
                findings.append(
                    (path, "error", f"ordered list must use '1.' on line {number}")
                )
    return findings


def check_references(root: Path, payload_mode: bool):
    findings = []
    for path in walk_dir(assets_base(root, payload_mode)):
        if path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for match in REFERENCE.finditer(text):
            reference = match.group(0).rstrip(".,;:)`'\"")
            if reference in REFERENCE_EXEMPT:
                continue
            if not resolve_reference(root, reference, payload_mode).exists():
                findings.append(
                    (path, "warning", f"reference not found: {reference}")
                )
    return findings


def check_secrets(root: Path, payload_mode: bool):
    findings = []
    for path in walk_dir(assets_base(root, payload_mode)):
        if path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern, label in SECRETS:
            if re.search(pattern, text):
                findings.append((path, "error", f"possible secret: {label}"))
    return findings


def check_config(root: Path, payload_mode: bool):
    findings = []
    path = root / ".agents" / "config.yaml"
    if not path.is_file():
        return findings
    try:
        data = parse_simple_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        findings.append((path, "error", "cannot read config"))
        return findings

    agents = data.get("agents")
    if not isinstance(agents, dict):
        findings.append((path, "error", "missing 'agents' section"))
        return findings

    if not agents.get("upstream"):
        findings.append((path, "error", "missing agents.upstream"))

    commit = agents.get("commit")
    if not commit:
        findings.append((path, "error", "missing agents.commit"))
    elif not COMMIT.match(str(commit)):
        findings.append(
            (path, "error", "agents.commit must be 40 lowercase hex characters")
        )

    exclude = agents.get("exclude")
    if exclude is not None and not isinstance(exclude, list):
        findings.append((path, "warning", "agents.exclude must be a list"))
    elif isinstance(exclude, list):
        for entry in exclude:
            if not isinstance(entry, str):
                findings.append(
                    (path, "warning", "agents.exclude entries must be strings")
                )
            elif entry.startswith("/") or ".." in entry.split("/"):
                findings.append(
                    (path, "error", f"exclude entry escapes the repository: {entry}")
                )

    return findings


def check_self_sync(root: Path, payload_mode: bool):
    """In payload mode, every payload path must have an identical copy installed.

    The installed copy may contain extra repository-owned files; only the
    payload-to-installed direction is enforced.
    """
    findings = []
    if not payload_mode:
        return findings
    payload = root / "agents"
    if not (root / ".agents").is_dir():
        return findings
    for path in walk_dir(payload):
        target = payload_target(path.relative_to(payload).as_posix())
        candidate = root / target
        if not candidate.is_file():
            findings.append((path, "error", f"self-sync missing: {target}"))
        elif candidate.read_bytes() != path.read_bytes():
            findings.append((path, "error", f"self-sync stale: {target}"))
    return findings


def check_genericity(root: Path, payload_mode: bool):
    findings = []
    payload = root / "agents"
    if not payload.is_dir():
        return findings

    for path in walk_dir(payload):
        if path.suffix not in TEXT_SUFFIXES:
            continue
        if path.relative_to(payload).as_posix() in GENERICITY_EXEMPT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for pattern in DENYLIST:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(
                    (
                        path,
                        "error",
                        f"repository-specific term '{match.group(0)}' on line {line}",
                    )
                )

        for pattern in ABSOLUTE_PATHS:
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append((path, "error", f"absolute path on line {line}"))

    return findings


def check_payload(root: Path, payload_mode: bool):
    findings = []
    payload = root / "agents"
    if not payload.is_dir():
        return findings

    seen: dict[str, str] = {}
    for path in walk_dir(payload):
        target = payload_target(path.relative_to(payload).as_posix())
        key = target.lower()
        if key in seen:
            findings.append(
                (path, "error", f"target '{target}' collides with '{seen[key]}'")
            )
        seen[key] = target
        if path.stat().st_size == 0:
            findings.append((path, "warning", "empty file"))

    return findings


# --- entry point -----------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an agents tree.")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="report only failures")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    payload_mode = (root / "agents").is_dir()

    checks = [
        check_structure,
        check_naming,
        check_frontmatter,
        check_markdown_lists,
        check_references,
        check_secrets,
        check_config,
    ]
    if payload_mode:
        checks += [check_self_sync, check_genericity, check_payload]

    findings = []
    for check in checks:
        findings.extend(check(root, payload_mode))

    findings.sort(key=lambda item: (SEVERITY_ORDER.get(item[1], 9), str(item[0]), item[2]))

    errors = sum(1 for item in findings if item[1] == "error")
    warnings = sum(1 for item in findings if item[1] == "warning")

    for path, severity, message in findings:
        if args.quiet and severity != "error":
            continue
        print(f"{path}: {severity}: {message}")

    mode = "payload" if payload_mode else "installed"
    print(f"\n{mode} mode: {errors} error(s), {warnings} warning(s)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
