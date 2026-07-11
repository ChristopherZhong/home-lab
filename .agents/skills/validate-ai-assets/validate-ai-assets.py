#!/usr/bin/env python3
"""Validate the repository's AI asset layout conventions."""
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[3]
agents_dir = repo_root / ".agents" / "agents"
prompts_dir = repo_root / ".agents" / "prompts"
skills_dir = repo_root / ".agents" / "skills"
rules_dir = repo_root / ".agents" / "rules"

errors = []

for expected_path, suffix, description in [
    (agents_dir, ".agent.md", "agent"),
    (prompts_dir, ".prompt.md", "prompt"),
    (rules_dir, ".rule.md", "rule"),
]:
    if not expected_path.exists():
        errors.append(f"Missing directory: {expected_path.relative_to(repo_root)}")
        continue

    matching_files = sorted([path.name for path in expected_path.glob(f"*{suffix}") if path.is_file()])
    if not matching_files:
        errors.append(f"No {description} assets found in {expected_path.relative_to(repo_root)}")

    for path in sorted(expected_path.iterdir()):
        if not path.is_file():
            continue
        if path.suffixes[-2:] != [".agent", ".md"] and description == "agent":
            if path.name != "README.md" and not path.name.endswith(".agent.md"):
                errors.append(f"Unexpected file name: {path.relative_to(repo_root)}")
        elif path.suffixes[-2:] != [".prompt", ".md"] and description == "prompt":
            if path.name != "README.md" and not path.name.endswith(".prompt.md"):
                errors.append(f"Unexpected file name: {path.relative_to(repo_root)}")
        elif path.suffixes[-2:] != [".rule", ".md"] and description == "rule":
            if path.name != "README.md" and not path.name.endswith(".rule.md"):
                errors.append(f"Unexpected file name: {path.relative_to(repo_root)}")

if not skills_dir.exists():
    errors.append(f"Missing directory: {skills_dir.relative_to(repo_root)}")
else:
    skill_dirs = sorted([path for path in skills_dir.iterdir() if path.is_dir()])
    if not skill_dirs:
        errors.append(f"No skill directories found under {skills_dir.relative_to(repo_root)}")
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"Missing skill file: {skill_file.relative_to(repo_root)}")

if not (repo_root / "AGENTS.md").exists():
    errors.append("Missing repository guide: AGENTS.md")

if errors:
    print("AI asset validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)

print(
    "AI asset validation passed: "
    f"{len(list(agents_dir.glob('*.agent.md')))} agent files, "
    f"{len(list(prompts_dir.glob('*.prompt.md')))} prompt files, "
    f"{len(list(skills_dir.iterdir()))} skill directories, "
    f"{len(list(rules_dir.glob('*.rule.md')))} rule files."
)
