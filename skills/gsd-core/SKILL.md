---
name: gsd-core
description: Core infrastructure for the GSD (Get Shit Done) project management framework. Provides shared Python scripts for git commits, state management, roadmap parsing, and frontmatter CRUD used by all other gsd-* skills. Must be installed before using any gsd-* skill.
---

# GSD Core

Shared infrastructure for all GSD skills. Install this skill first before using any `gsd-*` skill.

## The `.gsd/` Directory Convention

All GSD skills operate on a `.gsd/` directory in the project root. This directory contains all project management state.

### Directory Structure

```
project-root/
└── .gsd/
    ├── config.json          # Project configuration
    ├── STATE.md             # Current project state (frontmatter + body)
    ├── ROADMAP.md           # Phased execution roadmap
    ├── PROJECT.md           # Project description and goals
    ├── REQUIREMENTS.md      # Requirements with IDs (REQ-01, REQ-02...)
    ├── MILESTONES.md        # Completed milestone history
    ├── RETROSPECTIVE.md     # Lessons learned
    ├── phases/              # Phase directories (01-setup/, 02-core/...)
    │   └── XX-name/
    │       ├── XX-01-PLAN.md
    │       ├── XX-01-SUMMARY.md
    │       ├── XX-CONTEXT.md
    │       ├── XX-RESEARCH.md
    │       └── XX-UAT.md
    ├── todos/
    │   ├── pending/         # Active todo files
    │   └── done/            # Completed todo files
    └── milestones/          # Archived milestone data
```

### STATE.md Format

STATE.md uses bold markdown fields as structured frontmatter:

```markdown
**Project:** My Project
**Milestone:** v1.0 — Initial Release
**Current Phase:** 3
**Phase Name:** Core Implementation
**Plan:** 2 of 4
**Status:** In Progress
**Last Activity:** 2025-03-25

## Current Position
Status: Executing plan 2 of 4
Last activity: Implementing auth module
Plan: 2 of 4
```

Fields are read/written using `**Field:** value` bold format or plain `Field: value` format.

### config.json Schema

```json
{
  "model_profile": "balanced",
  "commit_docs": true,
  "parallelization": true,
  "git": {
    "branching_strategy": "none",
    "phase_branch_template": "gsd/phase-{phase}-{slug}",
    "milestone_branch_template": "gsd/{milestone}-{slug}"
  },
  "workflow": {
    "research": true,
    "plan_check": true,
    "verifier": true,
    "ui_phase": true,
    "skip_discuss": false
  }
}
```

### ROADMAP.md Format

Phases use heading format `### Phase N: Name` with structured metadata:

```markdown
### Phase 1: Project Setup
**Goal:** Initialize project structure and tooling
**Depends on:** None
**Requirements:** [REQ-01, REQ-02]
**Plans:** 0/2 plans complete

**Success Criteria:**
1. Project scaffolded with all dependencies
2. CI/CD pipeline configured
```

Phase summary checklist at top uses `- [x] **Phase N: Name**` format.

## Shared Scripts

Scripts in `scripts/` are used by multiple gsd-* skills. Run with `python3`.

### gsd_commit.py

Smart git commit for `.gsd/` documentation files.

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "message" [--files f1 f2] [--no-verify]
```

- Stages only `.gsd/` files by default unless `--files` specifies others
- Supports `--no-verify` to skip git hooks

### gsd_init.py

Initialize or validate `.gsd/` directory structure.

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_init.py [--validate] [--repair]
```

- Creates `.gsd/` with config.json, STATE.md, ROADMAP.md if missing
- `--validate` checks integrity; `--repair` fixes common issues
- Returns JSON with project state summary

### gsd_roadmap.py

Parse and manipulate ROADMAP.md.

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py <command> [args]
```

Commands: `get-phase <N>`, `analyze`, `update-progress <N>`

### gsd_state.py

Parse and update STATE.md frontmatter fields.

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py <command> [args]
```

Commands: `load`, `get [field]`, `update <field> <value>`, `patch --field1 val1 --field2 val2`, `snapshot`

### gsd_frontmatter.py

Generic YAML frontmatter CRUD for any markdown file.

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_frontmatter.py <file> <command> [args]
```

Commands: `extract <file>`, `update <file> <key> <value>`, `reconstruct <file>`

## Procedural Operations (No Script Needed)

These are simple enough to perform with Manus tools directly:

| Operation | How to Do It |
|---|---|
| Read config value | `file` tool: read `.gsd/config.json`, parse JSON, extract key |
| Set config value | `file` tool: read JSON, modify, write back |
| Check file exists | `shell` tool: `test -f path && echo yes` |
| Find phase directory | `match` tool: glob `.gsd/phases/XX-*` (XX = zero-padded phase) |
| Generate slug | Lowercase, replace `[^a-z0-9]+` with `-`, trim leading/trailing `-` |
| Get timestamp | `shell` tool: `date -u +%Y-%m-%d` |
| List todos | `match` tool: glob `.gsd/todos/pending/*.md` |

## Related Skills

All `gsd-*` skills depend on this skill. Key skills:
- `gsd-project-setup` — Initialize new projects
- `gsd-phase-planner` — Plan and organize phases
- `gsd-phase-executor` — Execute phase plans
- `gsd-milestone-manager` — Manage milestone lifecycle
