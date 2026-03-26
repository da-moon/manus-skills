---
name: gsd-research
description: Conduct deep research for project phases using Manus search and browser tools. Handles codebase mapping, technology research, domain analysis, and competitive analysis. Uses wide-research parallel processing for comprehensive coverage. Use when a phase needs research before planning or when the user needs domain knowledge.
---

# GSD Research

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Deep research for project phases using Manus native `search` and `browser` tools. Replaces GSD's subagent-based research with Manus's wide-research capabilities.

## Quick Start

When the user says "research phase N", "research [topic]", "map codebase", or "investigate [domain]":

1. Determine the research scope
2. Follow the appropriate workflow

## Phase Research Workflow

Use when planning a phase that needs technical investigation before creating plans.

### Step 1: Determine Research Scope

Read the phase from ROADMAP.md:
```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_roadmap.py get-phase <N>
```

Identify what needs researching based on the phase goal and requirements.

### Step 2: Conduct Research Using Wide-Research

Use the Manus `search` tool with multiple query variants for each research dimension. For comprehensive coverage, use the `map` tool to parallelize research across multiple topics.

Research dimensions for a typical phase:

**Technical Approach**
- Best practices for the specific implementation
- Library/framework recommendations with versions
- Common patterns and anti-patterns

**Architecture Implications**
- How this phase's work fits into the overall system
- Component boundaries and interfaces
- Data flow considerations

**Risk Assessment**
- Known pitfalls for this type of work
- Performance considerations
- Security implications

**Prior Art**
- How similar projects solved this problem
- Open-source implementations to reference
- Industry standards or specifications

### Step 3: Validate Findings

For critical findings, use the `browser` tool to visit source URLs and verify:
- Library versions are current (not training data)
- APIs haven't changed
- Recommendations are still valid

### Step 4: Write Research Document

Create `XX-RESEARCH.md` in the phase directory:

```markdown
# Phase [X]: [Name] — Research

**Conducted:** [date]
**Scope:** [what was researched]

## Executive Summary
[2-3 sentences: key findings and recommendation]

## Technical Approach
### Recommended
[Specific approach with rationale]

### Alternatives Considered
| Approach | Pros | Cons | Verdict |
|---|---|---|---|
| [Option A] | [pros] | [cons] | Recommended |
| [Option B] | [pros] | [cons] | Rejected — [why] |

## Libraries and Tools
| Library | Version | Purpose | Confidence |
|---|---|---|---|
| [lib] | [ver] | [what for] | High/Medium/Low |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| [risk] | [impact] | [how to prevent] |

## References
1. [Source title](url) — [what it covers]
2. [Source title](url) — [what it covers]
```

Commit:
```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_commit.py "docs: research for phase N"
```

## Codebase Mapping

When the user says "map codebase", "analyze codebase", or during brownfield project setup:

### Step 1: Scan Project Structure

```bash
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" -o -name "*.java" | head -100
```

### Step 2: Analyze Architecture

Read key files to understand:
- Entry points (main files, index files, app files)
- Directory structure and organization pattern
- Configuration files (package.json, pyproject.toml, Cargo.toml, go.mod)
- Database schemas or migrations
- API routes or endpoints
- Test structure

### Step 3: Write Architecture Map

Create `.gsd/research/ARCHITECTURE.md`:

```markdown
# Codebase Architecture Map

**Mapped:** [date]
**Project:** [name]

## Tech Stack
| Layer | Technology | Version |
|---|---|---|
| Language | [lang] | [ver] |
| Framework | [fw] | [ver] |
| Database | [db] | [ver] |
| Testing | [test fw] | [ver] |

## Directory Structure
[Annotated tree showing what each directory contains]

## Key Components
### [Component 1]
- **Location:** `src/component1/`
- **Purpose:** [what it does]
- **Dependencies:** [what it depends on]
- **Dependents:** [what depends on it]

## Data Flow
[How data moves through the system]

## Entry Points
- `src/main.py` — Application entry point
- `src/api/routes.py` — HTTP API endpoints

## Patterns in Use
- [Pattern 1] — used in [where]
- [Pattern 2] — used in [where]
```

## Project-Level Research

For new project research (used by `gsd-project-setup`), research 4 dimensions using the `search` tool:

1. **Stack Research** — Standard tech stack for the domain
2. **Features Research** — Table stakes vs. differentiators
3. **Architecture Research** — Typical system structure
4. **Pitfalls Research** — Common mistakes and prevention

Write each to `.gsd/research/STACK.md`, `FEATURES.md`, `ARCHITECTURE.md`, `PITFALLS.md`, then synthesize into `SUMMARY.md`.

## Related Skills

- `gsd-project-setup` — Uses project-level research during setup
- `gsd-phase-planner` — Uses phase research before planning
- `gsd-code-reviewer` — Research informs review standards
