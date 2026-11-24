---
name: sync-agents
description: Use when creating or updating this repository's agent assets from the upstream agents harness, including the first run into a repository that has none.
---

# Sync Agents

Bring this repository's `.agents/` tree into line with the upstream harness
without discarding any deliberate local decision.

## Safety contract

- Never execute anything fetched from upstream. Read and write files only.
- Never write outside the repository root. Reject absolute paths and `..`.
- Never overwrite a file without an explicit decision.
- Write via a temporary file and rename. Never leave a partial file.
- If any step is ambiguous, stop before writing and ask.

## Inputs

- `.agents/config.yaml` — may be absent.
- The upstream URL. Use `agents.upstream` when `config.yaml` exists. On a first
  run there is no config, so the URL must come from the user or from the
  instructions that asked for the sync.
- The payload directory `agents/` in that repository.

## Step 1 — Load state

Read `.agents/config.yaml`:

```
agents:
  upstream: <url>
  commit: <full 40-character sha>
  exclude: [<path>, ...]
```

If the file is missing, or `commit` cannot be read, this is a **first run**.
A first run has no base: treat **B** as false for every path, so every payload
file is either new or a collision. Skip Step 5 entirely on a first run.

## Step 2 — Fetch upstream

Clone into a temporary directory outside this repository. Do not pass
`--depth`; the recorded commit must be reachable.

```
git clone --quiet <upstream> <tmpdir>
```

Resolve the target:

```
git -C <tmpdir> rev-parse HEAD
```

On a first run there is no base, so skip the base check. Otherwise confirm the
recorded commit exists:

```
git -C <tmpdir> rev-parse --verify --quiet <commit>^{commit}
```

If the base is missing, fetch it explicitly:

```
git -C <tmpdir> fetch --quiet origin <commit>
```

## Step 3 — Map the payload

```
agents/AGENTS.md  -> AGENTS.md
agents/<path>     -> .agents/<path>
```

## Step 4 — Classify

Skip every path in `exclude`. Never create, modify, or report an excluded
path, even if it changes or disappears upstream.

For each remaining target path, establish:

- **B** — present in the payload at `commit`
- **H** — present in the payload at HEAD
- **L** — present on disk

The candidate paths are the union of three sets: every path in the payload at
`commit`, every path in the payload at HEAD, and every path already present on
disk at its mapped location. Enumerating only the payload would miss files the
consumer owns, and a file the consumer owns must never be touched.

| B   | H   | L   | Local vs base  | Payload   | Action                       |
| --- | --- | --- | -------------- | --------- | ---------------------------- |
| –   | –   | ✓   | —              | —         | ignore — repository-owned    |
| –   | ✓   | –   | —              | —         | create                       |
| –   | ✓   | ✓   | equals payload | —         | record only                  |
| –   | ✓   | ✓   | differs        | —         | **ask — collision**          |
| ✓   | –   | –   | —              | —         | nothing to do                |
| ✓   | –   | ✓   | —              | removed   | **ask — delete or exclude**  |
| ✓   | ✓   | –   | —              | present   | **ask — restore or exclude** |
| ✓   | ✓   | ✓   | equals base    | unchanged | nothing to do                |
| ✓   | ✓   | ✓   | equals base    | changed   | write payload                |
| ✓   | ✓   | ✓   | differs        | unchanged | keep local                   |
| ✓   | ✓   | ✓   | differs        | changed   | three-way merge              |

## Step 5 — Detect renames

Ask git; do not guess:

```
git -C <tmpdir> diff --name-status -M <commit> HEAD -- agents/
```

- `A` — added upstream
- `D` — removed upstream
- `M` — changed upstream
- `R<score> <old> <new>` — renamed upstream

For a rename, move the local file from the old target to the new target, then
merge with base = payload at `<old>` and theirs = payload at `<new>`. Report it
as **one** decision. Remove the old parent directory when the move leaves it
empty.

If the new target already exists locally, treat it as a collision.

If git does not detect the rename, the result is a delete plus an add. Say so
plainly; do not claim the history was preserved.

## Step 6 — Resolve ambiguous cases

An ambiguous case is a collision, a delete, a local deletion, or a merge
conflict. For each, present:

1. What is identical between the local file and the payload.
1. What differs, with each difference marked as either
   **intentional local divergence** — keep it, or
   **should follow the harness** — take the payload text.
1. A proposed result.

Then offer exactly one action:

- **take** — overwrite with the payload version.
- **merge** — payload version plus the retained local differences.
- **exclude** — keep the local file and add the path to `exclude`.

If you cannot classify a difference with confidence, ask. Do not guess and do
not default to either side.

## Step 7 — Merge

Merge into a scratch copy. `git merge-file` rewrites its first argument, so
merging in place would leave conflict markers in the consumer's file.

```
cp <local> <scratch>
git merge-file --diff3 <scratch> <base> <theirs>
```

Exit status 0 means clean: move `<scratch>` over `<local>`.

Non-zero means conflict: show the conflicting hunks from `<scratch>`, propose a
resolution, and stop without writing. Delete `<scratch>`. The local file must be
byte-identical to how it started.

## Step 8 — Write

Apply approved changes atomically. Create parent directories as needed.
Preserve the executable bit reported by git.

## Step 9 — Update state

Write `.agents/config.yaml` with any newly excluded paths, sorted.

Advance `commit` only when the payload changed. Compare the recorded commit to
the new one:

```
git -C <tmpdir> diff --quiet <old> <new> -- agents/
```

Exit status 0 means the payload is identical, so keep the recorded commit
unchanged. Otherwise record the new commit as the full 40-character SHA, exactly
as reported by `git -C <tmpdir> rev-parse HEAD`. An abbreviated SHA fails
validation.

A sync commit changes only `.agents/`, so it advances HEAD without changing the
payload. Recording it unconditionally would make every sync invalidate the
commit it just recorded and produce an endless series of config-only commits.

On a first run there is no recorded commit. Record the new one.

## Step 10 — Validate

Run `.agents/scripts/validate.py` and report its output verbatim.

## Output

Report per path: created, updated, merged, renamed, excluded, kept, or awaiting
a decision. State the previous and new commit, or state that the recorded commit
is unchanged because the payload did not change.
