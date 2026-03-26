# GSD Directory Structure Reference

## Complete `.gsd/` Layout

```
.gsd/
├── config.json                    # Project configuration (branching, workflow flags)
├── STATE.md                       # Current state: phase, plan, status, milestone
├── ROADMAP.md                     # All phases with goals, criteria, dependencies
├── PROJECT.md                     # Project description, tech stack, architecture
├── REQUIREMENTS.md                # Numbered requirements (REQ-01, REQ-02...)
├── MILESTONES.md                  # Completed milestone history with dates
├── RETROSPECTIVE.md               # Lessons learned per milestone
├── phases/
│   ├── 01-project-setup/
│   │   ├── 01-CONTEXT.md          # Phase context from discussion
│   │   ├── 01-RESEARCH.md         # Research findings
│   │   ├── 01-01-PLAN.md          # Plan 1 of phase 1
│   │   ├── 01-01-SUMMARY.md       # Summary after plan 1 execution
│   │   ├── 01-02-PLAN.md          # Plan 2 of phase 1
│   │   ├── 01-02-SUMMARY.md       # Summary after plan 2 execution
│   │   ├── 01-UAT.md              # User acceptance testing
│   │   └── 01-VERIFICATION.md     # Verification checklist
│   ├── 02-core-implementation/
│   │   └── ...
│   └── 02.1-hotfix/               # Decimal phases (inserted between 2 and 3)
│       └── ...
├── todos/
│   ├── pending/
│   │   └── fix-auth-bug.md        # Active todo
│   └── done/
│       └── setup-ci.md            # Completed todo
└── milestones/
    ├── v1.0-ROADMAP.md            # Archived roadmap for v1.0
    ├── v1.0-REQUIREMENTS.md       # Archived requirements for v1.0
    └── v1.0-phases/               # Archived phase directories
```

## File Naming Conventions

- Phase directories: `XX-slug` where XX is zero-padded phase number
- Plans: `XX-NN-PLAN.md` where NN is plan number within phase
- Summaries: `XX-NN-SUMMARY.md` matching the plan number
- Context: `XX-CONTEXT.md` — one per phase
- Research: `XX-RESEARCH.md` — one per phase
- UAT: `XX-UAT.md` — user acceptance testing per phase
- Verification: `XX-VERIFICATION.md` — verification checklist per phase

## Phase Status Lifecycle

```
no_directory → empty → discussed → researched → planned → partial → complete
```

- **no_directory**: Phase in ROADMAP but no directory on disk
- **empty**: Directory exists but no content files
- **discussed**: Has CONTEXT.md
- **researched**: Has RESEARCH.md
- **planned**: Has PLAN.md files but no SUMMARY.md
- **partial**: Some SUMMARY.md files but not all plans complete
- **complete**: All plans have matching SUMMARY.md files
