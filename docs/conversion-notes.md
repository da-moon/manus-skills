# GSD to Manus Skills — Conversion Notes

This document describes how the [get-shit-done](https://github.com/gsd-build/get-shit-done) framework was converted into Manus-compatible skills, including architectural decisions, trade-offs, and mapping details.

## Source Analysis

The upstream GSD repository (v1.29.0) contains 273 files organized in a 3-layer architecture. The table below summarizes the source material and how each layer was handled during conversion.

| Layer | File Count | Lines of Code | Conversion Strategy |
|---|---|---|---|
| Slash Commands | 57 | ~2,800 | Consolidated into skill trigger patterns |
| Workflows | 65 | ~12,000 | Converted to SKILL.md procedural knowledge |
| Agent Definitions | 18 | ~3,500 | Eliminated (Manus handles all work in context) |
| CJS Scripts | 17 | ~10,600 | 5 ported to Python, 12 became procedural knowledge |
| Templates | 35+ | ~2,000 | Preserved as Manus skill templates |
| References | 15 | ~1,500 | Selectively included in skill references |

## CJS Script Disposition

The 17 Node.js CJS scripts were categorized into three groups based on their function and how they map to Manus capabilities.

### Ported to Python (5 scripts in gsd-core)

These scripts contain complex logic that would be error-prone to express as prose instructions. They were rewritten in Python to run in the Manus sandbox.

| Original CJS | Python Port | Lines | Purpose |
|---|---|---|---|
| `state.cjs` | `gsd_state.py` | ~150 | STATE.md CRUD with YAML frontmatter |
| `roadmap.cjs` | `gsd_roadmap.py` | ~200 | ROADMAP.md parsing and progress tracking |
| `frontmatter.cjs` | `gsd_frontmatter.py` | ~100 | Generic YAML frontmatter operations |
| `init.cjs` | `gsd_init.py` | ~120 | .gsd/ directory initialization and validation |
| `commit.cjs` | `gsd_commit.py` | ~80 | Smart git commit with staging |

### Became Procedural Knowledge (7 scripts)

These scripts perform simple operations that Manus can do natively with its `file`, `match`, and `shell` tools. Their logic is described in SKILL.md files as step-by-step instructions.

| Original CJS | Manus Equivalent |
|---|---|
| `config.cjs` (get/set) | Read/write `.gsd/config.json` with `file` tool |
| `find-phase.cjs` | `match` tool glob for phase directories |
| `verify-path-exists.cjs` | `shell` tool `test -f` |
| `current-timestamp.cjs` | `shell` tool `date` |
| `generate-slug.cjs` | String transform described in SKILL.md |
| `phase-plan-index.cjs` | `match` tool glob + `file` tool read |
| `gsd-tools.cjs` (dispatcher) | Direct script calls replace the dispatcher |

### Dropped (5 scripts)

These scripts serve purposes that are either platform-specific or handled natively by Manus.

| Original CJS | Reason Dropped |
|---|---|
| `agent-skills.cjs` | Loads subagent prompts; Manus has no subagents |
| `resolve-model.cjs` | Selects AI model per agent; Manus handles model selection |
| `websearch.cjs` | Manus has native `search` and `browser` tools |
| `generate-claude-md.cjs` | Claude Code specific configuration |
| `profile.cjs` | Claude Code user profile management |

## Command-to-Skill Mapping

The 57 GSD slash commands were consolidated into 15 skills. The mapping below shows which commands feed into which skill.

| Skill | Source Commands |
|---|---|
| gsd-core | (shared infrastructure, no direct commands) |
| gsd-project-setup | `/gsd:new-project`, `/gsd:discover` |
| gsd-phase-planner | `/gsd:plan-phase`, `/gsd:add-phase`, `/gsd:insert-phase`, `/gsd:remove-phase`, `/gsd:discuss-phase` |
| gsd-phase-executor | `/gsd:do`, `/gsd:next`, `/gsd:fast`, `/gsd:quick`, `/gsd:autonomous`, `/gsd:transition` |
| gsd-milestone-manager | `/gsd:complete-milestone`, `/gsd:audit`, `/gsd:gap-analysis` |
| gsd-code-reviewer | `/gsd:review`, `/gsd:verify`, `/gsd:uat` |
| gsd-debugger | `/gsd:debug`, `/gsd:forensics`, `/gsd:health-check` |
| gsd-testing | `/gsd:test`, `/gsd:todo`, `/gsd:todo-done` |
| gsd-research | `/gsd:research`, `/gsd:map-codebase` |
| gsd-session-manager | `/gsd:pause`, `/gsd:resume`, `/gsd:report`, `/gsd:thread` |
| gsd-workspace-manager | `/gsd:workspace`, `/gsd:settings`, `/gsd:cleanup`, `/gsd:workstream` |
| gsd-ui-developer | `/gsd:ui`, `/gsd:ui-review` |
| gsd-git-shipper | `/gsd:ship`, `/gsd:pr`, `/gsd:backlog` |
| gsd-manager-mode | `/gsd:manage`, `/gsd:delegate` |
| gsd-update | (new skill, no upstream command) |

## Agent Elimination Strategy

GSD defines 18 subagent types. Since Manus operates in a single context without subagent spawning, each agent's behavior was absorbed into the relevant skill's workflow instructions.

| GSD Agent | Absorbed Into | How |
|---|---|---|
| gsd-project-researcher | gsd-research | Manus `search` + `map` tools |
| gsd-research-synthesizer | gsd-research | Inline synthesis in SKILL.md |
| gsd-phase-researcher | gsd-research | Phase-scoped search workflow |
| gsd-planner | gsd-phase-planner | Plan creation instructions |
| gsd-plan-checker | gsd-phase-planner | Verification step in workflow |
| gsd-executor | gsd-phase-executor | Execution instructions |
| gsd-verifier | gsd-code-reviewer | Verification workflow |
| gsd-reviewer | gsd-code-reviewer | Review workflow |
| gsd-debugger | gsd-debugger | Debug workflow |
| gsd-tester | gsd-testing | Test generation workflow |
| gsd-ui-executor | gsd-ui-developer | UI execution workflow |
| gsd-ui-reviewer | gsd-ui-developer | UI review workflow |
| gsd-manager | gsd-manager-mode | Orchestration decision tree |
| gsd-roadmapper | gsd-project-setup | Roadmap creation step |
| gsd-requirements | gsd-project-setup | Requirements step |
| gsd-quick-planner | gsd-phase-executor | Quick task workflow |
| gsd-quick-executor | gsd-phase-executor | Quick task execution |
| gsd-shipper | gsd-git-shipper | Shipping workflow |

## Directory Convention Change

The project state directory was renamed from `.planning/` (GSD convention) to `.gsd/` for clarity. The internal structure is preserved.

| GSD Path | Manus Path |
|---|---|
| `.planning/PROJECT.md` | `.gsd/PROJECT.md` |
| `.planning/STATE.md` | `.gsd/STATE.md` |
| `.planning/ROADMAP.md` | `.gsd/ROADMAP.md` |
| `.planning/config.json` | `.gsd/config.json` |
| `.planning/phases/` | `.gsd/phases/` |
| `.planning/research/` | `.gsd/research/` |
| `.planning/quick/` | `.gsd/quick/` |
