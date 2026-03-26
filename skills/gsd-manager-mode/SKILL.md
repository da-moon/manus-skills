---
name: gsd-manager-mode
description: High-level project orchestration mode that coordinates across all GSD skills. Manages the full project lifecycle from setup through shipping, delegates to appropriate skills, tracks overall progress, and makes strategic decisions. Use when you want Manus to autonomously drive a project end-to-end or when coordinating complex multi-phase work.
---

# GSD Manager Mode

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Orchestration mode that coordinates across all GSD skills to drive projects end-to-end. Acts as the project manager, deciding what to do next and delegating to the right skill.

## Quick Start

When the user says "manage this project", "autonomous mode", "drive this end to end", or "take over":

1. Assess current project state
2. Determine next action
3. Execute using the appropriate skill
4. Loop until milestone complete or user intervenes

## Orchestration Loop

### Step 1: Assess State

```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py snapshot
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py analyze
```

### Step 2: Decision Tree

Based on project state, determine the next action:

```
Is .gsd/ initialized?
├── No → Use gsd-project-setup
└── Yes
    ├── Is ROADMAP.md present?
    │   ├── No → Use gsd-project-setup (Step 8: Roadmap)
    │   └── Yes
    │       ├── Are all phases complete?
    │       │   ├── Yes → Use gsd-milestone-manager (Complete Milestone)
    │       │   └── No
    │       │       ├── Is current phase planned?
    │       │       │   ├── No → Use gsd-phase-planner
    │       │       │   └── Yes
    │       │       │       ├── Is current phase in progress?
    │       │       │       │   ├── No → Use gsd-phase-executor
    │       │       │       │   └── Yes
    │       │       │       │       ├── Are there incomplete plans?
    │       │       │       │       │   ├── Yes → Use gsd-phase-executor (resume)
    │       │       │       │       │   └── No
    │       │       │       │       │       ├── Is verification enabled?
    │       │       │       │       │       │   ├── Yes → Use gsd-code-reviewer
    │       │       │       │       │       │   └── No → Advance to next phase
    │       │       │       │       │       └── ...
    │       │       │       └── ...
    │       └── ...
    └── ...
```

### Step 3: Execute

Read the appropriate skill's SKILL.md and follow its workflow. After completion, return to Step 1.

### Step 4: Report Progress

After each major action, provide a brief status update:

```
[Phase 3/5] Completed Plan 2/4 — Auth middleware implemented
Next: Plan 3 — API route protection
```

## Autonomous Execution

In autonomous mode, Manus drives the entire project lifecycle:

1. **Setup** → `gsd-project-setup` (if needed)
2. **For each phase:**
   a. **Research** → `gsd-research` (if enabled)
   b. **Plan** → `gsd-phase-planner`
   c. **Execute** → `gsd-phase-executor`
   d. **Review** → `gsd-code-reviewer` (if enabled)
   e. **Test** → `gsd-testing` (if needed)
   f. **Advance** → update state, move to next phase
3. **Ship** → `gsd-git-shipper`
4. **Complete** → `gsd-milestone-manager`

### Intervention Points

Even in autonomous mode, pause and ask the user when:
- A critical decision needs human judgment
- Tests are failing and the fix isn't obvious
- Requirements seem contradictory
- The phase is taking significantly longer than expected
- A security-sensitive operation is needed

### Progress Tracking

Use the Manus `plan` tool to maintain a high-level task plan that maps to GSD phases. Update the plan as phases complete.

## Strategic Decisions

The manager makes these decisions automatically:

| Situation | Decision |
|---|---|
| Phase has UI work | Delegate to `gsd-ui-developer` instead of `gsd-phase-executor` |
| Debug needed during execution | Pause, delegate to `gsd-debugger`, resume |
| Research reveals better approach | Update plans before executing |
| Phase fails verification | Re-execute failed plans or create fix plans |
| User goes idle | Use `gsd-session-manager` to save state |

## Multi-Phase Coordination

When managing multiple phases:

1. Respect dependency order from ROADMAP.md
2. Track cross-phase dependencies (e.g., Phase 3 needs Phase 2's API)
3. Carry forward accumulated context between phases
4. Update PROJECT.md at phase transitions (requirements evolution)

## Delegation Pattern

When delegating to a skill:

1. Read the skill's SKILL.md
2. Provide the skill with current context (phase number, state, relevant files)
3. Follow the skill's workflow
4. Capture the skill's output (commits, artifacts, state changes)
5. Return to the orchestration loop

## Related Skills

All GSD skills are coordinated by this manager:
- `gsd-project-setup` — Project initialization
- `gsd-phase-planner` — Phase planning
- `gsd-phase-executor` — Phase execution
- `gsd-milestone-manager` — Milestone lifecycle
- `gsd-code-reviewer` — Code review
- `gsd-debugger` — Debugging
- `gsd-testing` — Test generation
- `gsd-research` — Research
- `gsd-session-manager` — Session management
- `gsd-workspace-manager` — Workspace management
- `gsd-ui-developer` — UI-specific execution
- `gsd-git-shipper` — Git shipping
- `gsd-update` — Skill updates
