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

### Import via Manus Web UI

Manus supports importing skills directly from public GitHub repositories through the **Import from GitHub** feature in Settings > Skills > + Add > Import from GitHub.

Because this repository is a monorepo containing multiple skills, you cannot import the repo root URL directly. Instead, import each skill individually using its subdirectory URL. **You must import `gsd-core` first** because all other skills (except `gsd-update`) depend on its shared scripts at runtime.

#### Step 1: Import gsd-core (required)

```
https://github.com/da-moon/manus-skills/tree/master/skills/gsd-core
```

#### Step 2: Import additional skills

Import any combination of the skills below. All of them require `gsd-core` to be installed first.

| Skill | Import URL |
|---|---|
| gsd-project-setup | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-project-setup` |
| gsd-phase-planner | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-phase-planner` |
| gsd-phase-executor | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-phase-executor` |
| gsd-milestone-manager | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-milestone-manager` |
| gsd-code-reviewer | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-code-reviewer` |
| gsd-debugger | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-debugger` |
| gsd-testing | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-testing` |
| gsd-research | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-research` |
| gsd-session-manager | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-session-manager` |
| gsd-workspace-manager | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-workspace-manager` |
| gsd-ui-developer | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-ui-developer` |
| gsd-git-shipper | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-git-shipper` |
| gsd-manager-mode | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-manager-mode` |
| gsd-update | `https://github.com/da-moon/manus-skills/tree/master/skills/gsd-update` |

#### Important Notes

**Dependency on gsd-core.** Thirteen of the fifteen skills call shared Python scripts located at `/home/ubuntu/skills/gsd-core/scripts/` via hardcoded paths. If `gsd-core` is not installed, those skills will fail at runtime with `FileNotFoundError`. The Agent Skills specification does not support a formal `requires` or `depends-on` field, so this dependency is enforced only by the prerequisite instruction in each skill's SKILL.md body.

**No live sync with Git.** After importing through the web UI, skills are copied into your Manus account. Changes pushed to this repository will not propagate automatically. To pick up updates, you must re-import each skill individually or use the `gsd-update` skill from within a Manus session.

**No bulk import.** The Manus web UI imports one skill at a time. There is no batch or monorepo import option. Each of the URLs above must be imported separately.

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
