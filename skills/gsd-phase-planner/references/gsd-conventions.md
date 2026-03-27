# GSD Conventions Reference

This file documents the `.gsd/` directory conventions used by this skill.

## ROADMAP.md Format

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

## STATE.md Format

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

## config.json Schema

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
