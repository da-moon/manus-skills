---
name: gsd-update
description: Update GSD Manus skills from the upstream get-shit-done repository. Compares local skill versions against upstream GSD, identifies changes in commands, workflows, agents, and templates, then refactors and updates skills accordingly. Use when the upstream GSD repo has been updated and skills need to be brought in sync.
---

# GSD Update

**Prerequisite:** The user must give Manus access to the `da-moon/manus-skills` GitHub repository for this skill to push updates.

Update all GSD Manus skills by pulling changes from the upstream [get-shit-done](https://github.com/gsd-build/get-shit-done) repository, analyzing what changed, and refactoring skills to match.

## Quick Start

When the user says "update GSD skills", "sync with upstream", or "check for GSD updates":

1. Clone both repos (upstream GSD and manus-skills)
2. Compare versions
3. Analyze changes
4. Update affected skills
5. Commit and push

## Update Workflow

### Step 1: Clone Repositories

```bash
cd /home/ubuntu
gh repo clone da-moon/manus-skills
git clone https://github.com/gsd-build/get-shit-done.git
```

### Step 2: Check Version Tracking

Read the version tracking file:

```bash
cat /home/ubuntu/manus-skills/.gsd-upstream.json
```

Expected format:
```json
{
  "upstream_repo": "gsd-build/get-shit-done",
  "version": "1.29.0",
  "commit": "abc123def456",
  "last_updated": "2025-03-25",
  "skills_version": "1.0.0"
}
```

### Step 3: Check Upstream Version

```bash
cd /home/ubuntu/get-shit-done
UPSTREAM_VERSION=$(node -p "require('./package.json').version")
UPSTREAM_COMMIT=$(git rev-parse HEAD)
echo "Upstream: v${UPSTREAM_VERSION} (${UPSTREAM_COMMIT})"
```

Compare with tracked version. If same, report "already up to date" and exit.

### Step 4: Analyze Changes

Get the diff between tracked commit and current upstream:

```bash
cd /home/ubuntu/get-shit-done
git log --oneline ${TRACKED_COMMIT}..HEAD
git diff --stat ${TRACKED_COMMIT}..HEAD
```

Categorize changes by impact area:

| Changed File Pattern | Affected Skill(s) |
|---|---|
| `commands/gsd/new-project*` | gsd-project-setup |
| `commands/gsd/plan-phase*` | gsd-phase-planner |
| `commands/gsd/do*`, `commands/gsd/next*` | gsd-phase-executor |
| `commands/gsd/milestone*` | gsd-milestone-manager |
| `commands/gsd/review*`, `commands/gsd/verify*` | gsd-code-reviewer |
| `commands/gsd/debug*` | gsd-debugger |
| `commands/gsd/test*`, `commands/gsd/todo*` | gsd-testing |
| `commands/gsd/research*`, `commands/gsd/map*` | gsd-research |
| `commands/gsd/pause*`, `commands/gsd/resume*` | gsd-session-manager |
| `commands/gsd/workspace*`, `commands/gsd/settings*` | gsd-workspace-manager |
| `commands/gsd/ui*` | gsd-ui-developer |
| `commands/gsd/ship*`, `commands/gsd/pr*` | gsd-git-shipper |
| `commands/gsd/manage*` | gsd-manager-mode |
| `get-shit-done/workflows/*` | Multiple (map by workflow name) |
| `get-shit-done/bin/lib/*.cjs` | All skills with shared scripts (see fan-out below) |
| `agents/*` | Review for behavioral changes |
| `templates/*` | All skills with shared scripts (see fan-out below) |

### Shared Script Fan-Out

Shared Python scripts (`gsd_commit.py`, `gsd_init.py`, `gsd_roadmap.py`, `gsd_state.py`) are distributed across multiple skills. When upstream changes affect `bin/lib/` or `templates/`, update the corresponding Python script in **every** skill that contains a copy:

| Script | Skills Containing Copy |
|---|---|
| `gsd_commit.py` | gsd-project-setup, gsd-phase-planner, gsd-phase-executor, gsd-milestone-manager, gsd-session-manager, gsd-workspace-manager, gsd-code-reviewer, gsd-git-shipper, gsd-research |
| `gsd_init.py` | gsd-project-setup |
| `gsd_roadmap.py` | gsd-phase-planner, gsd-phase-executor, gsd-milestone-manager, gsd-session-manager, gsd-code-reviewer, gsd-git-shipper, gsd-research, gsd-manager-mode |
| `gsd_state.py` | gsd-project-setup, gsd-phase-planner, gsd-phase-executor, gsd-milestone-manager, gsd-session-manager, gsd-workspace-manager, gsd-git-shipper, gsd-manager-mode, gsd-debugger |

When updating a shared script:
1. Update the script logic once
2. Copy the updated script to every skill listed above
3. Ensure all copies are identical

### Step 5: Read Changed Files

For each changed file, read the new version and understand:
- What behavior changed?
- Are there new features or commands?
- Were any workflows restructured?
- Did templates change format?

Use the `map` tool for parallel analysis if many files changed.

### Step 6: Update Affected Skills

For each affected skill:

1. Read the current SKILL.md from manus-skills
2. Read the changed upstream files
3. Identify what needs updating in the SKILL.md:
   - New workflow steps
   - Changed decision logic
   - New templates or formats
   - Removed features
4. Update the SKILL.md
5. Update any scripts, references, or templates

**For shared script updates:**
- If CJS logic changed, update the corresponding Python script
- Test the updated script
- Copy the updated script to all skills that contain it (see fan-out table above)
- Ensure backward compatibility with existing `.gsd/` directories

### Step 7: Update Version Tracking

Update `.gsd-upstream.json`:

```json
{
  "upstream_repo": "gsd-build/get-shit-done",
  "version": "[new version]",
  "commit": "[new commit hash]",
  "last_updated": "[today's date]",
  "skills_version": "[bumped version]"
}
```

### Step 8: Validate All Skills

```bash
cd /home/ubuntu
for skill in manus-skills/skills/gsd-*/; do
  skill_name=$(basename "$skill")
  python3 skills/skill-creator/scripts/quick_validate.py "$skill_name"
done
```

### Step 9: Commit and Push

```bash
cd /home/ubuntu/manus-skills
git add -A
git commit -m "feat: update GSD skills to upstream v${NEW_VERSION}

Upstream changes:
$(git -C /home/ubuntu/get-shit-done log --oneline ${TRACKED_COMMIT}..HEAD | head -20)

Skills updated:
$(echo "${AFFECTED_SKILLS}" | tr ' ' '\n' | sed 's/^/- /')"

git push
```

### Step 10: Generate Changelog

Append to `CHANGELOG.md`:

```markdown
## [skills_version] — [date]

### Updated from upstream v[version]

**Skills modified:**
- `gsd-[skill]` — [what changed]

**New features:**
- [feature description]

**Breaking changes:**
- [if any]
```

## Change Impact Assessment

Before applying changes, assess impact:

| Impact Level | Criteria | Action |
|---|---|---|
| **Low** | Template wording, comment changes | Auto-apply |
| **Medium** | New optional workflow steps, new flags | Apply with note |
| **High** | Workflow restructure, new required steps | Apply and highlight to user |
| **Breaking** | Format changes, removed features | Apply and warn user |

## Handling New Commands

If upstream adds entirely new commands:

1. Determine which existing skill it belongs to (or if a new skill is needed)
2. If existing skill: add the command's workflow as a new section
3. If new skill: create using the skill-creator workflow
4. Update `gsd-manager-mode` decision tree if needed
5. Update the repo README skill catalog

## Related Skills

- `gsd-manager-mode` — Decision tree may need updating
- All other GSD skills — may be affected by upstream changes
