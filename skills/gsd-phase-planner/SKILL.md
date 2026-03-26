---
name: gsd-phase-planner
description: Create, modify, and organize execution plans for roadmap phases. Handles research, context gathering, plan creation, plan verification, and phase CRUD operations (add, insert, remove, reorder). Use when planning what to build in a specific phase.
---

# GSD Phase Planner

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Create executable PLAN.md files for roadmap phases. Default flow: Research (if enabled) then Plan then Verify.

## Quick Start

When the user says "plan phase N", "create plans for phase N", or "what should we build next":

1. Identify the target phase from ROADMAP.md
2. Follow the planning workflow below

## Phase Planning Workflow

### Step 1: Initialize

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py get-phase <N>
```

Parse JSON for: `phase_number`, `phase_name`, `goal`, `success_criteria`, `section`.

If phase not found, show available phases:
```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py analyze
```

Check if phase directory exists. If not, create it:
```bash
mkdir -p .gsd/phases/$(printf "%02d" N)-<slug>
```

### Step 2: Load Context

Check for existing artifacts in the phase directory:
- `XX-CONTEXT.md` — Previous discussion context
- `XX-RESEARCH.md` — Previous research
- Existing `XX-NN-PLAN.md` files

If no CONTEXT.md exists, gather context by asking the user about implementation decisions for this phase. Write findings to `XX-CONTEXT.md`:

```markdown
# Phase [X]: [Name] - Context

**Gathered:** [date]
**Status:** Ready for planning

## Phase Boundary
[What this phase delivers and what it does not]

## Implementation Decisions
### [Category]
- [Decision as locked choice]

### Open Questions
[Areas where Manus should use best judgment]

## Canonical References
- `.gsd/REQUIREMENTS.md` — Requirements [REQ-XX] linked to this phase
- `.gsd/PROJECT.md` — Project context and constraints
```

### Step 3: Research (If Enabled)

Check `.gsd/config.json` for `workflow.research`. If enabled and no `XX-RESEARCH.md` exists:

Use the `search` tool to research technical approaches for this phase:
- Best practices for the specific implementation
- Common patterns and anti-patterns
- Library/tool recommendations
- Performance considerations

Write findings to `XX-RESEARCH.md` in the phase directory.

### Step 4: Create Plans

Based on context, research, and phase goal, create PLAN.md files. Each plan is a self-contained unit of work.

Plan file naming: `XX-NN-PLAN.md` (e.g., `03-01-PLAN.md` for phase 3, plan 1).

Plan structure:

```markdown
# Phase [X] Plan [N]: [Title]

**Objective:** [What this plan achieves]
**Wave:** [dependency group — plans in same wave can run in parallel]

## Context
[What the executor needs to know]

## Tasks
1. [Task with specific file paths and expected changes]
2. [Task with clear acceptance criteria]
3. [Task with verification steps]

## Files to Modify
- `path/to/file.ext` — [what changes]

## Verification
- [ ] [How to verify task 1 is complete]
- [ ] [How to verify task 2 is complete]

## Dependencies
- Requires: [other plans that must complete first, if any]
```

Guidelines for plan creation:
- Each plan should be completable in one focused session
- Plans within the same wave have no dependencies on each other
- Include specific file paths, not vague descriptions
- Verification steps should be concrete and testable

### Step 5: Verify Plans (If Enabled)

Check `.gsd/config.json` for `workflow.plan_check`. If enabled:

Review each plan against:
1. Does it achieve the phase goal?
2. Are tasks specific enough to execute without ambiguity?
3. Are file paths correct and complete?
4. Do verification steps actually prove completion?
5. Are dependencies correctly identified?

If issues found, revise the plan (max 3 revision iterations).

### Step 6: Commit and Update State

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "docs: plan phase N" --files .gsd/phases/XX-name/
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py patch --current-phase "N" --phase-name "[Name]" --plan "0 of M" --status "Planned"
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "docs: update state for phase N"
```

## Phase CRUD Operations

### Add Phase

Append a new phase at the end of the roadmap:

1. Get current phase count from `python3 gsd_roadmap.py analyze`
2. Create new phase section in ROADMAP.md with next number
3. Add to phase summary checklist
4. Create phase directory

### Insert Phase

Insert an urgent phase between existing phases (uses decimal numbering):

1. Identify the phase to insert after (e.g., after phase 2 creates phase 2.1)
2. Add phase section to ROADMAP.md with decimal number
3. Create phase directory with decimal naming (e.g., `02.1-hotfix/`)

### Remove Phase

Remove an unstarted future phase:

1. Verify phase has no executed plans
2. Remove phase section from ROADMAP.md
3. Remove phase directory
4. Renumber subsequent phases if needed

### Discuss Phase

Have a focused discussion about a phase before planning:

1. Load phase context from ROADMAP.md
2. Ask the user targeted questions about implementation
3. Write discussion results to `XX-CONTEXT.md`

## Related Skills

- `gsd-project-setup` — Must be done before planning
- `gsd-phase-executor` — Execute the plans created here
- `gsd-research` — Deep research for complex phases
- `gsd-code-reviewer` — Review plans against requirements
