# Manus Skills — GSD (Get Shit Done)

A collection of Manus-compatible skills converted from the [get-shit-done](https://github.com/gsd-build/get-shit-done) project management framework. These skills bring structured project planning, phased execution, code review, debugging, and shipping workflows to Manus.

## Upstream Tracking

These skills are derived from GSD v1.29.0 (`604a78b`). Use the `gsd-update` skill to sync with newer upstream versions.

## Skill Catalog

| Skill | Description | Depends On |
|---|---|---|
| **gsd-core** | Shared scripts, templates, references, and `.gsd/` directory conventions | None |
| **gsd-project-setup** | Initialize projects: questioning, research, requirements, roadmap | gsd-core |
| **gsd-phase-planner** | Create, modify, and organize execution plans for roadmap phases | gsd-core |
| **gsd-phase-executor** | Execute phase plans: implement code, track progress, write summaries | gsd-core |
| **gsd-milestone-manager** | Milestone lifecycle: completion, archiving, gap analysis, retrospective | gsd-core |
| **gsd-code-reviewer** | Structured code review, verification, and user acceptance testing | gsd-core |
| **gsd-debugger** | Systematic debugging: diagnosis, root cause analysis, resolution | gsd-core |
| **gsd-testing** | Test generation (unit, integration, e2e) and todo management | gsd-core |
| **gsd-research** | Deep research using Manus search/browser tools and codebase mapping | gsd-core |
| **gsd-session-manager** | Pause/resume sessions, context handoff, session reports | gsd-core |
| **gsd-workspace-manager** | Workspace CRUD, multi-repo setups, settings, cleanup | gsd-core |
| **gsd-ui-developer** | UI/frontend phase execution with browser-based visual verification | gsd-core |
| **gsd-git-shipper** | Git shipping: PRs, branch management, release tags, backlog | gsd-core |
| **gsd-manager-mode** | Autonomous orchestration across all skills for end-to-end delivery | gsd-core |
| **gsd-update** | Update skills from upstream GSD repository | None |

## Installation

### Import to Manus

Each skill is a self-contained directory under `skills/`. To use in Manus:

1. Import the `gsd-core` skill first (all other skills depend on it)
2. Import any additional skills you need
3. Reference skills in your Manus tasks with `/skill-name`

### Quick Start

The typical workflow is:

1. `gsd-project-setup` — Initialize a new project with structured questioning
2. `gsd-phase-planner` — Plan the first phase
3. `gsd-phase-executor` — Execute the plans
4. `gsd-code-reviewer` — Review the implementation
5. `gsd-git-shipper` — Ship it

Or use `gsd-manager-mode` to let Manus orchestrate the entire flow autonomously.

## Architecture

### Conversion from GSD

The original GSD framework uses a 3-layer architecture:

- **57 slash-commands** (thin dispatchers) — consolidated into skill trigger patterns
- **65 workflow files** (actual logic) — converted to SKILL.md procedural knowledge
- **18 agent definitions** (subagent personas) — eliminated; Manus handles everything in its own context
- **17 Node.js CJS scripts** (tooling) — ported to 5 shared Python scripts in `gsd-core`
- **35+ templates** — preserved as Manus skill templates

### Key Design Decisions

**No subagents.** GSD spawns subagents for research, planning, and verification. Manus handles all work in its own context, using native tools (`search`, `browser`, `map`, `plan`) instead.

**Python over Node.js.** GSD's CJS scripts are ported to Python for Manus sandbox compatibility. The 5 shared scripts in `gsd-core/scripts/` replace 17 CJS files.

**`.gsd/` over `.planning/`.** The project state directory is renamed from GSD's `.planning/` to `.gsd/` to avoid confusion with other tools.

**Wide-research over subagent research.** GSD spawns 4 parallel researcher subagents. Manus uses its native `search` tool with the `map` tool for parallel research.

### Directory Structure

```
skills/
├── gsd-core/                  # Shared foundation
│   ├── SKILL.md
│   ├── scripts/               # 5 shared Python scripts
│   ├── references/            # Directory structure spec
│   └── templates/             # STATE.md, ROADMAP.md, config.json
├── gsd-project-setup/         # Project initialization
│   ├── SKILL.md
│   ├── references/            # Questioning techniques
│   └── templates/             # PROJECT.md, REQUIREMENTS.md
├── gsd-phase-planner/         # Phase planning
│   └── SKILL.md
├── gsd-phase-executor/        # Phase execution
│   └── SKILL.md
├── gsd-milestone-manager/     # Milestone lifecycle
│   └── SKILL.md
├── gsd-code-reviewer/         # Code review and verification
│   └── SKILL.md
├── gsd-debugger/              # Debugging workflows
│   └── SKILL.md
├── gsd-testing/               # Test generation and todos
│   └── SKILL.md
├── gsd-research/              # Research workflows
│   └── SKILL.md
├── gsd-session-manager/       # Session management
│   └── SKILL.md
├── gsd-workspace-manager/     # Workspace management
│   └── SKILL.md
├── gsd-ui-developer/          # UI/frontend workflows
│   └── SKILL.md
├── gsd-git-shipper/           # Git shipping workflows
│   └── SKILL.md
├── gsd-manager-mode/          # Autonomous orchestration
│   └── SKILL.md
└── gsd-update/                # Upstream sync
    ├── SKILL.md
    └── scripts/check_upstream.py
```

## Updating from Upstream

When the GSD repo releases a new version:

1. Give Manus access to this repository
2. Say "update GSD skills" or use the `gsd-update` skill
3. Manus will clone upstream, diff against the tracked version, and update affected skills
4. Review the changes and merge

The `.gsd-upstream.json` file tracks the current upstream version and commit hash.

## License

Skills are derived from [get-shit-done](https://github.com/gsd-build/get-shit-done) and follow its licensing terms.
