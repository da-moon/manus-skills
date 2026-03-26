---
name: gsd-workspace-manager
description: Manage GSD workspaces including multi-repo setups, workspace cleanup, workstream organization, and project configuration. Handles sub-repo detection, workspace-level settings, and cleanup of stale artifacts. Use when managing project workspace structure or multi-repo environments.
---

# GSD Workspace Manager

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Manage GSD workspace structure, multi-repo setups, configuration, and cleanup.

## Quick Start

When the user says "clean up workspace", "manage workspace", "settings", or "configure project":

1. Determine the operation
2. Follow the appropriate workflow

## Workspace Operations

### List Workspaces

Show all GSD-initialized projects the user has:

```bash
find ~ -maxdepth 4 -name ".gsd" -type d 2>/dev/null | while read d; do
  project_dir=$(dirname "$d")
  echo "$project_dir"
done
```

### Workspace Status

For the current workspace, show:
- Project name and milestone
- Current phase and progress
- Config settings
- Sub-repos (if multi-repo)
- Disk usage of `.gsd/` directory

```bash
du -sh .gsd/
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py snapshot
```

## Settings Management

When the user says "settings", "configure", or "change settings":

### View Current Settings

```bash
cat .gsd/config.json
```

Present settings in a readable format:

| Setting | Current Value |
|---|---|
| Mode | YOLO |
| Granularity | Standard |
| Git Tracking | Yes |
| Research | Enabled |
| Verification | Enabled |
| Branching | phase |

### Update Settings

Allow the user to change any setting. Update `.gsd/config.json` using the `file` tool.

Commit:
```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "chore: update project settings"
```

## Multi-Repo Workspace

For workspaces containing multiple git repositories:

### Detection

```bash
find . -maxdepth 1 -type d -not -name ".*" -not -name "node_modules" -exec test -d "{}/.git" \; -print
```

### Configuration

If sub-repos detected, update config:

```json
{
  "planning": {
    "sub_repos": ["backend", "frontend"],
    "commit_docs": false
  }
}
```

When `sub_repos` is set:
- Planning docs stay local (not committed to any sub-repo)
- `.gsd/` is added to `.gitignore`
- Commits during phase execution target the appropriate sub-repo

### Cross-Repo Operations

When executing plans that span multiple repos:
1. Identify which repo each file belongs to
2. Stage and commit changes per-repo
3. Track which repos were modified in SUMMARY.md

## Workspace Cleanup

When the user says "clean up", "tidy", or "remove stale":

### Stale Artifact Detection

```bash
# Find empty phase directories
find .gsd/phases/ -maxdepth 1 -type d -empty

# Find orphaned summaries (summary without matching plan)
# Find stale session reports (older than 30 days)
find .gsd/sessions/ -name "*.md" -mtime +30

# Find large research files that could be archived
du -sh .gsd/research/ .gsd/phases/*/
```

### Cleanup Actions

Present findings and let user choose:
- **Remove empty directories** — delete empty phase dirs
- **Archive old sessions** — move to `.gsd/archive/sessions/`
- **Archive completed milestones** — move to `.gsd/milestones/`
- **Compact state** — remove resolved accumulated context entries

### Safe Cleanup

Always confirm before deleting. Never delete:
- Active phase directories with plans
- STATE.md or ROADMAP.md
- config.json
- Current session reports

## Workstream Management

For projects with parallel workstreams (e.g., frontend + backend + infrastructure):

### Define Workstreams

Add to `.gsd/config.json`:

```json
{
  "workstreams": [
    {"name": "backend", "path": "backend/", "phases": [1, 2, 5]},
    {"name": "frontend", "path": "frontend/", "phases": [3, 4, 6]},
    {"name": "infra", "path": "infra/", "phases": [7]}
  ]
}
```

### Workstream Status

Show progress per workstream:

```
Workstreams:
  backend .... 2/3 phases complete (67%)
  frontend ... 1/3 phases complete (33%)
  infra ...... 0/1 phases complete (0%)
```

## Related Skills

- `gsd-project-setup` — Initial workspace creation
- `gsd-session-manager` — Session management within workspace
- `gsd-git-shipper` — Git operations across workspace repos
