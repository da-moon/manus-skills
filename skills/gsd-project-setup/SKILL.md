---
name: gsd-project-setup
description: Initialize new GSD projects through a structured workflow of deep questioning, optional research, requirements definition, and roadmap creation. Converts ideas into actionable project plans with proper .gsd/ directory structure. Use when starting a new project or onboarding an existing codebase.
---

# GSD Project Setup

Initialize new projects through a structured flow: questioning, research (optional), requirements, roadmap.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "start a new project", "initialize GSD", or "set up project planning":

1. Run `python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_init.py` to create `.gsd/`
2. Follow the workflow below

## Workflow

### Step 1: Pre-Flight Checks

```bash
python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_init.py
```

Parse JSON output. If `.gsd/` already has PROJECT.md, project is initialized — suggest `gsd-phase-planner`. If no `.git`, run `git init`.

### Step 2: Brownfield Detection

Check for existing source code:

```bash
find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" -o -name "*.java" | head -5
```

If code found, ask: **Map codebase first** (use `gsd-research`) or **Skip mapping** (greenfield).

### Step 3: Deep Questioning

Ask: **"What do you want to build?"**

Then follow up with probing questions:
- **Challenge vagueness**: "When you say 'fast', what does that mean?"
- **Make abstract concrete**: "Walk me through what a user would actually do"
- **Surface assumptions**: "You mentioned X — are you assuming Y?"
- **Find edges**: "What happens when Z fails?"
- **Reveal motivation**: "What problem sparked this?"

When you have enough context, ask: "Ready to create PROJECT.md?"

### Step 4: Write PROJECT.md

Create `.gsd/PROJECT.md`:

```markdown
# [Project Name]

## What This Is
[2-3 sentences: what it does, who it's for]

## Core Value
[The ONE thing that matters most]

## Requirements

### Validated
(None yet — ship to validate)

### Active
- [ ] [Requirement 1]
- [ ] [Requirement 2]

### Out of Scope
- [Exclusion 1] — [why]

## Context
[Background: technical environment, prior work, known issues]

## Constraints
- **[Type]**: [What] — [Why]

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| [Choice] | [Why] | — Pending |

## Evolution
This document evolves at phase transitions and milestone boundaries.

---
*Last updated: [date] after initialization*
```

Commit: `python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_commit.py "docs: initialize project" --files .gsd/PROJECT.md`

### Step 5: Workflow Preferences

Ask the user to configure:

| Setting | Options | Default |
|---|---|---|
| Mode | YOLO / Interactive | YOLO |
| Granularity | Coarse / Standard / Fine | Standard |
| Git Tracking | Yes / No | Yes |
| Research | Yes / No | Yes |
| Verification | Yes / No | Yes |

Update `.gsd/config.json` and commit.

### Step 6: Research (Optional)

If research enabled, use the `search` tool to research 4 dimensions:

1. **Stack** — Standard tech stack (specific libraries, versions, rationale)
2. **Features** — Table stakes vs. differentiators
3. **Architecture** — Component boundaries, data flow, build order
4. **Pitfalls** — Common mistakes, prevention strategies

Write to `.gsd/research/`: `STACK.md`, `FEATURES.md`, `ARCHITECTURE.md`, `PITFALLS.md`, `SUMMARY.md`

Commit: `python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_commit.py "docs: project research"`

### Step 7: Requirements

Create `.gsd/REQUIREMENTS.md` with numbered requirements (REQ-01, REQ-02...) including priority, source, description, and acceptance criteria. Present to user for approval.

### Step 8: Roadmap

Create `.gsd/ROADMAP.md` with phased execution plan. Each phase has: goal, dependencies, linked requirements, success criteria. Present to user for approval.

Update state and commit:
```bash
python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_state.py update "Status" "Ready"
python3 /home/ubuntu/skills/gsd-project-setup/scripts/gsd_commit.py "docs: create roadmap"
```

### Step 9: Completion

Display summary: project name, core value, requirement count, phase count, next step.

## Auto Mode

If user provides a document (PRD, spec) with their request: skip questioning, default all config, auto-approve, complete without interruption.

## Related Skills

- `gsd-phase-planner` — Plan individual phases after setup
- `gsd-research` — Deep research on specific topics
- `gsd-milestone-manager` — Manage milestone lifecycle
