# Changelog

All notable changes to the GSD Manus Skills will be documented in this file.

## [1.0.0] — 2025-03-25

### Initial Release

Converted from upstream GSD v1.29.0 (`604a78b30b44463be583d6a36647af7fdd1f525f`).

**Skills created:**

- `gsd-core` — Shared foundation with 5 Python scripts, templates, and references
- `gsd-project-setup` — Project initialization with deep questioning workflow
- `gsd-phase-planner` — Phase planning with research, context, and plan creation
- `gsd-phase-executor` — Phase execution with wave grouping and resume support
- `gsd-milestone-manager` — Milestone lifecycle management
- `gsd-code-reviewer` — Structured code review and UAT
- `gsd-debugger` — Systematic debugging with forensic analysis
- `gsd-testing` — Test generation and todo management
- `gsd-research` — Deep research using Manus native tools
- `gsd-session-manager` — Session pause/resume and context preservation
- `gsd-workspace-manager` — Workspace and multi-repo management
- `gsd-ui-developer` — UI/frontend specialized execution
- `gsd-git-shipper` — Git shipping, PRs, and release management
- `gsd-manager-mode` — Autonomous end-to-end orchestration
- `gsd-update` — Upstream synchronization

**Key architectural decisions:**

- Eliminated subagent spawning (Manus handles all work in context)
- Ported 17 CJS scripts to 5 shared Python scripts
- Renamed `.planning/` to `.gsd/` directory convention
- Replaced subagent research with Manus `search` and `map` tools
- Replaced `AskUserQuestion` TUI with Manus `message` tool interactions
