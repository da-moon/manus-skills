---
name: gsd-debugger
description: Systematic debugging and forensic analysis for project issues. Provides structured workflows for diagnosing bugs, analyzing error patterns, performing health checks, and resolving issues with full documentation. Use when something is broken, tests fail, or behavior is unexpected.
---

# GSD Debugger

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Systematic debugging with structured diagnosis, root cause analysis, and documented resolution.

## Quick Start

When the user says "debug", "fix this", "something is broken", "tests failing", or describes unexpected behavior:

1. Gather symptoms
2. Follow the diagnostic workflow

## Debugging Workflow

### Step 1: Symptom Collection

Gather information about the issue:

1. **What's happening?** — Error messages, unexpected behavior, test failures
2. **What's expected?** — Correct behavior
3. **When did it start?** — Recent changes, last known working state
4. **Reproducibility** — Always, sometimes, specific conditions

Check recent git history for potential causes:
```bash
git log --oneline -10
git diff HEAD~3 --stat
```

### Step 2: Hypothesis Formation

Based on symptoms, form ranked hypotheses:

```
Hypothesis 1 (HIGH): [Most likely cause] — because [evidence]
Hypothesis 2 (MED): [Alternative cause] — because [evidence]
Hypothesis 3 (LOW): [Less likely cause] — because [evidence]
```

### Step 3: Systematic Investigation

For each hypothesis (highest probability first):

1. **Identify test** — What would confirm or eliminate this hypothesis?
2. **Execute test** — Run the diagnostic command/check
3. **Analyze result** — Does evidence support or refute?
4. **Update hypotheses** — Re-rank based on new evidence

Common diagnostic techniques:

| Technique | When to Use | How |
|---|---|---|
| Log analysis | Runtime errors | `grep -r "ERROR\|WARN" logs/` |
| Stack trace | Exceptions | Read error output, trace call chain |
| Binary search | Regression | `git bisect start`, test at midpoints |
| Isolation | Complex systems | Test components independently |
| Diff analysis | Recent breakage | `git diff` against last working commit |
| Dependency check | Import/build errors | Verify versions, lock files |

### Step 4: Root Cause Identification

Document the root cause:

```markdown
## Root Cause
**Category:** [Logic error / Configuration / Dependency / Race condition / etc.]
**Location:** [file:line]
**Mechanism:** [How the bug manifests]
**Trigger:** [What conditions cause it]
```

### Step 5: Fix Implementation

1. Implement the fix
2. Verify the fix resolves the original symptom
3. Check for regressions (run existing tests)
4. Commit with descriptive message:

```bash
git add -A
git commit -m "fix: [description of what was fixed and why]"
```

### Step 6: Document Resolution

If within a GSD project, update the phase summary or create a debug log:

```markdown
## Debug Session: [Issue Title]

**Date:** [date]
**Duration:** [time spent]
**Severity:** Critical / High / Medium / Low

### Symptoms
[What was observed]

### Root Cause
[What caused it]

### Fix Applied
[What was changed and why]

### Prevention
[How to prevent similar issues]
```

## Forensic Analysis

For complex or recurring issues, perform deeper analysis:

### Codebase Health Check

Scan the project for common issues:

```bash
# Find TODO/FIXME/HACK comments
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.js" --include="*.ts"

# Find large files
find . -name "*.py" -o -name "*.js" -o -name "*.ts" | xargs wc -l | sort -rn | head -20

# Check for common anti-patterns
grep -rn "except:" --include="*.py"  # bare except
grep -rn "eval(" --include="*.py" --include="*.js"  # eval usage
```

### Dependency Audit

```bash
# Python
pip list --outdated 2>/dev/null
# Node
npm audit 2>/dev/null || pnpm audit 2>/dev/null
```

### Git Forensics

```bash
# Find when a specific line was introduced
git log -p -S "problematic_string" -- path/to/file
# Find who last modified a file section
git blame path/to/file
# Find commits that touched a specific function
git log --all -p -- path/to/file | grep -B5 "function_name"
```

## Integration with GSD Workflow

When debugging during phase execution:

1. Pause the current plan execution
2. Run the debug workflow
3. Document the issue in the plan's SUMMARY.md
4. Resume execution after fix

Update state if debugging causes delays:
```bash
python3 /home/ubuntu/skills/gsd-core/scripts/gsd_state.py update "Status" "Debugging"
```

## Related Skills

- `gsd-phase-executor` — May need debugging during execution
- `gsd-testing` — Generate tests to prevent regressions
- `gsd-code-reviewer` — Review fixes before committing
