---
name: gsd-phase-executor
description: Execute phase plans created by gsd-phase-planner. Handles sequential and wave-based plan execution, state tracking, branch management, verification, and auto-advance to next phases. Use when ready to implement the work defined in PLAN.md files.
---

# GSD Phase Executor

Execute PLAN.md files for a roadmap phase. Reads plans, implements the work, writes SUMMARY.md files, and tracks progress.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "execute phase N", "do phase N", "start working on phase N", or "next":

1. Load phase context and plans
2. Execute each plan sequentially or by wave
3. Write summaries and update state

## Execution Workflow

### Step 1: Initialize

```bash
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_roadmap.py get-phase <N>
```

Load phase info: `phase_number`, `phase_name`, `goal`, `success_criteria`.

Find all plans in the phase directory:
```bash
# Use match tool to glob for plans
.gsd/phases/XX-name/XX-*-PLAN.md
```

Check for existing summaries (partially completed phases):
```bash
# Glob for summaries
.gsd/phases/XX-name/XX-*-SUMMARY.md
```

### Step 2: Branch Management

Check `.gsd/config.json` for `git.branching_strategy`:

| Strategy | Action |
|---|---|
| `none` | Stay on current branch |
| `phase` | Create/checkout `gsd/phase-{N}-{slug}` |
| `milestone` | Create/checkout `gsd/{milestone}-{slug}` |

```bash
git checkout -b <branch-name> 2>/dev/null || git checkout <branch-name>
```

### Step 3: Update State

```bash
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_state.py patch \
  --current-phase "N" \
  --phase-name "[Name]" \
  --status "In Progress" \
  --last-activity "$(date -u +%Y-%m-%d)"
```

### Step 4: Plan Discovery and Wave Grouping

Read all PLAN.md files and group by wave:
- **Wave 1**: Plans with no dependencies (can conceptually run in parallel)
- **Wave 2**: Plans depending on wave 1 completion
- **Wave N**: Plans depending on wave N-1

Skip plans that already have matching SUMMARY.md files (resume support).

### Step 5: Execute Plans

For each plan in wave order:

1. **Read the PLAN.md** — understand objective, tasks, files to modify, verification steps
2. **Execute the tasks** — implement the actual code/config changes described in the plan
3. **Run verification** — execute the verification steps from the plan
4. **Write SUMMARY.md** — document what was done

SUMMARY.md structure:

```markdown
# Phase [X] Plan [N] Summary: [Title]

**Status:** Complete
**Started:** [timestamp]
**Completed:** [timestamp]

## What Was Done
[Description of actual implementation]

## Files Modified
- `path/to/file.ext` — [what changed]

## Verification Results
- [x] [Verification step 1] — PASS
- [x] [Verification step 2] — PASS

## Notes
[Any deviations from plan, issues encountered, decisions made]
```

5. **Commit work:**
```bash
git add -A
git commit -m "feat: phase N plan M - [title]"
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_commit.py "docs: summary for phase N plan M"
```

6. **Update state:**
```bash
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_state.py update "Plan" "M of T"
```

### Step 6: Post-Phase Completion

After all plans are executed:

1. **Update roadmap progress:**
```bash
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_roadmap.py update-progress <N>
```

2. **Update state:**
```bash
python3 /home/ubuntu/skills/gsd-phase-executor/scripts/gsd_state.py patch \
  --status "Phase N Complete" \
  --last-activity "$(date -u +%Y-%m-%d)"
```

3. **Run verification** (if `workflow.verifier` enabled in config):
   - Check all success criteria from ROADMAP.md
   - Write `XX-VERIFICATION.md` in phase directory
   - Report any failures to user

4. **Display completion summary:**
   - Plans executed: M/M
   - Files modified: [count]
   - Verification: PASS/FAIL
   - Next step: suggest next phase or milestone completion

## Execution Modes

### Standard Mode
Execute plans one at a time with user visibility into progress.

### Fast Mode
Execute all plans without pausing between them. Use when user says "fast", "quick", or "just do it".

### Interactive Mode
Pause after each plan for user review. Use when user says "interactive" or "step by step".

### Gaps Only Mode
Only execute plans that don't have SUMMARY.md files yet. Use when resuming a partially completed phase.

### Auto-Advance Mode
After completing a phase, automatically start planning/executing the next phase. Use when user says "autonomous" or "keep going".

## Handling Failures

If a plan execution fails:

1. Write a partial SUMMARY.md documenting what was done and what failed
2. Update state to reflect the failure
3. Ask the user how to proceed:
   - **Retry** — attempt the failed tasks again
   - **Skip** — mark plan as skipped, continue to next
   - **Stop** — halt execution, user will fix manually

## Related Skills

- `gsd-phase-planner` — Creates the plans this skill executes
- `gsd-code-reviewer` — Review code after execution
- `gsd-debugger` — Debug issues during execution
- `gsd-testing` — Generate tests for implemented code
- `gsd-milestone-manager` — Complete milestone after all phases done
