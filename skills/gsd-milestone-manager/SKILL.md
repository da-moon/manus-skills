---
name: gsd-milestone-manager
description: Manage milestone lifecycle including completion, archiving, gap analysis, auditing, and transitioning to the next milestone. Use when all phases in a milestone are complete, when auditing progress, or when starting a new milestone.
---

# GSD Milestone Manager

Manage the full milestone lifecycle: completion, archiving, retrospective, gap analysis, and next milestone setup.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "complete milestone", "milestone done", "audit milestone", or "start next milestone":

1. Analyze current roadmap progress
2. Follow the appropriate workflow below

## Complete Milestone Workflow

### Step 1: Verify All Phases Complete

```bash
python3 /home/ubuntu/skills/gsd-milestone-manager/scripts/gsd_roadmap.py analyze
```

Check that all phases have `disk_status: "complete"` and `progress_percent: 100`.

If incomplete phases exist, report them and ask the user:
- **Complete remaining phases** — use `gsd-phase-executor`
- **Ship anyway** — mark incomplete phases as deferred
- **Cancel** — don't complete milestone yet

### Step 2: Run Gap Analysis

Review each requirement in `.gsd/REQUIREMENTS.md`:

| Requirement | Status | Evidence |
|---|---|---|
| REQ-01 | Delivered | Phase 2, Plan 1 |
| REQ-02 | Delivered | Phase 3, Plan 2 |
| REQ-03 | Partial | Missing edge case handling |
| REQ-04 | Deferred | Moved to next milestone |

Present gap analysis to user for review.

### Step 3: Write Retrospective

Create or update `.gsd/RETROSPECTIVE.md`:

```markdown
# Retrospective — [Milestone Version]

**Completed:** [date]
**Duration:** [start date] to [end date]

## What Went Well
- [Positive outcome 1]
- [Positive outcome 2]

## What Could Improve
- [Issue 1] — [suggested improvement]
- [Issue 2] — [suggested improvement]

## Key Learnings
- [Learning 1]
- [Learning 2]

## Metrics
- Phases: [completed]/[total]
- Plans: [executed]/[total]
- Requirements: [delivered]/[total]
```

Ask the user for their input on what went well and what could improve.

### Step 4: Archive Milestone

Move current milestone artifacts to archive:

```bash
mkdir -p .gsd/milestones
cp .gsd/ROADMAP.md .gsd/milestones/[version]-ROADMAP.md
cp .gsd/REQUIREMENTS.md .gsd/milestones/[version]-REQUIREMENTS.md
cp -r .gsd/phases .gsd/milestones/[version]-phases
```

### Step 5: Update MILESTONES.md

Append to `.gsd/MILESTONES.md`:

```markdown
## [version] [name] (Shipped: [date])

**Phases:** [count] completed
**Requirements:** [delivered]/[total] delivered
**Duration:** [start] to [end]

### Delivered
- [Key deliverable 1]
- [Key deliverable 2]

### Deferred
- [Deferred item] — moved to [next milestone]
```

### Step 6: Update PROJECT.md

Review and update `.gsd/PROJECT.md`:
1. Move delivered requirements from Active to Validated
2. Move deferred items to Out of Scope (with "deferred to vN.x" reason)
3. Update "What This Is" if the product has evolved
4. Check Core Value — still accurate?
5. Add milestone completion to Key Decisions table

### Step 7: Commit Everything

```bash
python3 /home/ubuntu/skills/gsd-milestone-manager/scripts/gsd_commit.py "docs: complete milestone [version]"
```

## Audit Milestone

When the user says "audit", "check progress", or "where are we":

```bash
python3 /home/ubuntu/skills/gsd-milestone-manager/scripts/gsd_roadmap.py analyze
python3 /home/ubuntu/skills/gsd-milestone-manager/scripts/gsd_state.py snapshot
```

Present a comprehensive status report:

```
Milestone: v1.0 — Initial Release
Progress: 65% (13/20 plans complete)

Phase Status:
  Phase 1: Setup .............. COMPLETE (3/3 plans)
  Phase 2: Core ............... COMPLETE (5/5 plans)
  Phase 3: Auth ............... IN PROGRESS (3/5 plans)
  Phase 4: UI ................. NOT STARTED
  Phase 5: Deploy ............. NOT STARTED

Requirements Coverage:
  Delivered: 4/8
  In Progress: 2/8
  Not Started: 2/8
```

## Start Next Milestone

After completing a milestone:

1. Clear phase directories for new work
2. Reset STATE.md for new milestone
3. Ask user about next milestone goals
4. Create new ROADMAP.md with fresh phases
5. Carry over any deferred requirements

```bash
python3 /home/ubuntu/skills/gsd-milestone-manager/scripts/gsd_state.py patch \
  --milestone "v[next] — [Name]" \
  --current-phase "1" \
  --status "Not Started" \
  --plan "0 of 0"
```

## Related Skills

- `gsd-phase-executor` — Must complete all phases before milestone completion
- `gsd-project-setup` — Initial milestone is created during project setup
- `gsd-code-reviewer` — Review code quality before shipping milestone
- `gsd-git-shipper` — Ship the milestone (tags, PRs, releases)
