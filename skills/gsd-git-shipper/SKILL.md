---
name: gsd-git-shipper
description: Handle git shipping operations including creating pull requests, managing branches, tagging releases, and maintaining a backlog. Manages the full git workflow from feature branches to merged PRs and release tags. Use when ready to ship code, create PRs, or manage release workflow.
---

# GSD Git Shipper

Handle git shipping: PRs, branch management, release tags, and backlog tracking.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "ship it", "create PR", "merge", "release", or "tag":

1. Determine the shipping operation
2. Follow the appropriate workflow

## Create Pull Request

### Step 1: Verify Ready to Ship

Check that the current phase/milestone is complete:
```bash
python3 /home/ubuntu/skills/gsd-git-shipper/scripts/gsd_state.py snapshot
python3 /home/ubuntu/skills/gsd-git-shipper/scripts/gsd_roadmap.py analyze
```

Verify:
- All plans have SUMMARY.md files
- No failing tests
- Code review completed (if enabled)

### Step 2: Prepare PR

Determine the base branch:
```bash
git remote show origin | grep "HEAD branch"
```

Generate PR description from phase summaries:

```markdown
## Summary
[What this PR delivers — synthesized from plan summaries]

## Changes
- [Key change 1]
- [Key change 2]

## Phase: [N] — [Name]
**Plans completed:** [M/M]

## Testing
- [x] [Test 1 description]
- [x] [Test 2 description]

## Requirements Addressed
- REQ-XX: [name] — [status]
```

### Step 3: Create PR via GitHub CLI

```bash
gh pr create \
  --title "[Phase N] [Phase Name]" \
  --body-file /tmp/pr-body.md \
  --base main \
  --head $(git branch --show-current)
```

### Step 4: Update State

```bash
python3 /home/ubuntu/skills/gsd-git-shipper/scripts/gsd_state.py update "Status" "PR Created"
python3 /home/ubuntu/skills/gsd-git-shipper/scripts/gsd_commit.py "docs: update state after PR creation"
```

## Branch Management

### Branch Strategy

Based on `.gsd/config.json` branching strategy:

| Strategy | Branch Pattern | When to Create |
|---|---|---|
| `none` | Work on current branch | Never |
| `phase` | `gsd/phase-{N}-{slug}` | Before each phase |
| `milestone` | `gsd/{version}-{slug}` | Before each milestone |

### Create Phase Branch

```bash
PHASE_NUM=$(printf "%02d" $N)
SLUG=$(echo "$PHASE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
git checkout -b "gsd/phase-${PHASE_NUM}-${SLUG}"
```

### Merge Phase Branch

After PR is approved:
```bash
gh pr merge --squash --delete-branch
git checkout main
git pull
```

### Clean Up Stale Branches

```bash
# List merged branches
git branch --merged main | grep "gsd/"

# Delete merged branches
git branch --merged main | grep "gsd/" | xargs -r git branch -d

# Clean remote tracking
git remote prune origin
```

## Release Tagging

When the user says "release", "tag", or "create release":

### Step 1: Determine Version

Check `.gsd/MILESTONES.md` for the current milestone version. Or ask the user.

### Step 2: Create Tag

```bash
git tag -a "v${VERSION}" -m "Release v${VERSION} — ${MILESTONE_NAME}"
git push origin "v${VERSION}"
```

### Step 3: Create GitHub Release

```bash
gh release create "v${VERSION}" \
  --title "v${VERSION} — ${MILESTONE_NAME}" \
  --notes-file /tmp/release-notes.md
```

Generate release notes from milestone completion data:

```markdown
# v${VERSION} — ${MILESTONE_NAME}

## What's New
- [Feature 1 from delivered requirements]
- [Feature 2 from delivered requirements]

## Phases Completed
- Phase 1: [name] — [summary]
- Phase 2: [name] — [summary]

## Requirements Delivered
- REQ-01: [name]
- REQ-02: [name]

## Contributors
- Manus (AI-assisted development)
- [User name]
```

## Backlog Management

Track items deferred from current milestone:

### Add to Backlog

When a requirement is deferred during milestone completion:

Append to `.gsd/BACKLOG.md`:

```markdown
## [Item Title]
**Source:** REQ-XX (deferred from v1.0)
**Priority:** [High/Medium/Low]
**Reason:** [Why it was deferred]
**Description:** [What needs to be done]
```

### Review Backlog

When starting a new milestone, review backlog items for inclusion:
```bash
cat .gsd/BACKLOG.md
```

Present items to user for prioritization into the new milestone.

## Related Skills

- `gsd-phase-executor` — Produces the code to ship
- `gsd-milestone-manager` — Milestone completion triggers shipping
- `gsd-code-reviewer` — Reviews must pass before shipping
