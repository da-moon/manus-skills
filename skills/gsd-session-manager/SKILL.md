---
name: gsd-session-manager
description: Manage work sessions including pause/resume, session reports, context handoff between sessions, and accumulated context tracking. Use when pausing work, resuming after a break, or generating session summaries for continuity.
---

# GSD Session Manager

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Manage work sessions for continuity across Manus task boundaries. Handles pause, resume, session reports, and context preservation.

## Quick Start

When the user says "pause", "save progress", "resume", "where was I", or "session report":

1. Determine the operation
2. Follow the appropriate workflow

## Pause Session

When the user needs to stop work and resume later:

### Step 1: Capture Current State

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py snapshot
```

### Step 2: Write Session Report

Create `.gsd/sessions/session-[date].md`:

```markdown
# Session Report — [date]

**Duration:** [start time] to [end time]
**Phase:** [current phase number and name]
**Status:** Paused

## What Was Done
- [Completed task 1]
- [Completed task 2]

## In Progress
- [Task being worked on when paused]
- [Current state of that task]

## Next Steps
1. [Immediate next action to take on resume]
2. [Following action]
3. [Following action]

## Open Questions
- [Question that needs answering before proceeding]

## Files Modified This Session
- `path/to/file1.ext` — [what changed]
- `path/to/file2.ext` — [what changed]

## Accumulated Context
[Important decisions, discoveries, or context that future sessions need]
```

### Step 3: Update State

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py patch \
  --status "Paused" \
  --last-activity "$(date -u +%Y-%m-%d)"
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "docs: session pause report"
```

## Resume Session

When the user returns to continue work:

### Step 1: Load Latest Session Report

Find the most recent session report:
```bash
ls -t .gsd/sessions/session-*.md | head -1
```

Read it to understand where work left off.

### Step 2: Load Current State

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py snapshot
```

### Step 3: Present Context

Show the user:
- What was being worked on
- What the next steps are
- Any open questions
- Current phase and plan progress

### Step 4: Update State and Continue

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py patch \
  --status "In Progress" \
  --last-activity "$(date -u +%Y-%m-%d)"
```

Suggest the next action (usually resuming phase execution or planning).

## Session Report (Status Check)

When the user asks "where are we", "status", or "what's the progress":

### Step 1: Gather All Context

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py snapshot
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py analyze
```

### Step 2: Present Comprehensive Status

```
Project: [name]
Milestone: [version — name]
Phase: [N] — [name] ([status])
Plan Progress: [M of T plans complete]
Last Activity: [date]

Phase Summary:
  Phase 1: [name] ......... COMPLETE
  Phase 2: [name] ......... COMPLETE
  Phase 3: [name] ......... IN PROGRESS (3/5 plans)
  Phase 4: [name] ......... NOT STARTED

Recent Activity:
  [date] — Completed Phase 2 Plan 5
  [date] — Started Phase 3
  [date] — Completed Phase 3 Plans 1-3
```

## Accumulated Context

Track important context that persists across sessions. When significant decisions or discoveries happen during work:

Append to `.gsd/STATE.md` under an "Accumulated Context" section:

```markdown
## Accumulated Context

### Decisions
- [date] [decision and rationale]

### Discoveries
- [date] [unexpected finding and implications]

### Roadmap Evolution
- [date] [phase added/removed/modified and why]
```

This section grows throughout the project and ensures no important context is lost between sessions.

## Related Skills

- `gsd-phase-executor` — Execution state is tracked for resume
- `gsd-milestone-manager` — Session reports feed milestone audits
- `gsd-workspace-manager` — Multi-workspace session management
