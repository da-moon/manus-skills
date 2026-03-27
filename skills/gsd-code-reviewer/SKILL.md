---
name: gsd-code-reviewer
description: Perform structured code reviews, verification against requirements, and user acceptance testing (UAT). Reviews code changes from phase execution against plans, requirements, and best practices. Use after phase execution or before shipping.
---

# GSD Code Reviewer

Structured code review and verification for phase deliverables. Reviews implementation against plans, requirements, and engineering best practices.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "review phase N", "review code", "verify phase N", or "UAT":

1. Load phase context and plans
2. Follow the appropriate review workflow

## Code Review Workflow

### Step 1: Load Context

Read the phase plans and summaries:
```bash
# Glob for all plans and summaries in the phase directory
.gsd/phases/XX-name/XX-*-PLAN.md
.gsd/phases/XX-name/XX-*-SUMMARY.md
```

Read requirements linked to this phase from ROADMAP.md and REQUIREMENTS.md.

### Step 2: Identify Changed Files

From SUMMARY.md files, collect all modified files. Also check git:
```bash
git diff --name-only main..HEAD  # or appropriate base branch
```

### Step 3: Review Each File

For each modified file, review against these dimensions:

**Correctness**
- Does the code do what the plan specified?
- Are edge cases handled?
- Are error paths covered?

**Requirements Compliance**
- Does the implementation satisfy linked requirements (REQ-XX)?
- Are acceptance criteria from REQUIREMENTS.md met?

**Code Quality**
- Is the code readable and well-structured?
- Are naming conventions consistent?
- Is there unnecessary duplication?
- Are functions/methods appropriately sized?

**Security**
- Input validation present?
- No hardcoded secrets or credentials?
- SQL injection / XSS / CSRF protections?
- Authentication/authorization checks?

**Performance**
- No obvious N+1 queries or unbounded loops?
- Appropriate caching where needed?
- Resource cleanup (connections, file handles)?

**Testing**
- Are critical paths tested?
- Are edge cases covered in tests?
- Do tests actually assert meaningful behavior?

### Step 4: Write Review

Create `XX-REVIEWS.md` in the phase directory:

```markdown
# Phase [X]: [Name] — Code Review

**Reviewed:** [date]
**Reviewer:** Manus (automated)
**Scope:** [N files across M plans]

## Summary
[Overall assessment: APPROVED / APPROVED WITH COMMENTS / CHANGES REQUESTED]

## Findings

### Critical (Must Fix)
- [ ] **[File:Line]** — [Issue description and suggested fix]

### Important (Should Fix)
- [ ] **[File:Line]** — [Issue description]

### Minor (Nice to Have)
- [ ] **[File:Line]** — [Suggestion]

## Requirements Verification

| Requirement | Status | Evidence |
|---|---|---|
| REQ-01 | PASS | [file/test that proves it] |
| REQ-02 | PASS | [file/test that proves it] |
| REQ-03 | FAIL | [what's missing] |

## Positive Observations
- [Good pattern or practice noticed]
```

### Step 5: Present and Iterate

Present findings to user. If changes requested:
1. User or Manus fixes the issues
2. Re-review the specific files
3. Update REVIEWS.md with resolution status

Commit:
```bash
python3 /home/ubuntu/skills/gsd-code-reviewer/scripts/gsd_commit.py "docs: code review for phase N"
```

## User Acceptance Testing (UAT)

When the user says "UAT phase N" or "acceptance test":

### Step 1: Extract Acceptance Criteria

From REQUIREMENTS.md, extract all acceptance criteria for requirements linked to this phase.

### Step 2: Create UAT Checklist

Write `XX-UAT.md` in the phase directory:

```markdown
# Phase [X]: [Name] — User Acceptance Testing

**Date:** [date]
**Tester:** [user]

## Test Scenarios

### REQ-01: [Name]
- [ ] **Scenario 1:** [Description of what to test]
  - Steps: [1, 2, 3]
  - Expected: [outcome]
  - Actual: ___
  - Status: PASS / FAIL

### REQ-02: [Name]
- [ ] **Scenario 1:** [Description]
  ...

## Overall Result
- [ ] All critical scenarios pass
- [ ] No blocking issues found
- [ ] Ready to ship
```

### Step 3: Guide User Through Testing

Walk the user through each test scenario. Record results in the UAT document.

## Verification Mode

Quick verification that phase deliverables match success criteria:

```bash
python3 /home/ubuntu/skills/gsd-code-reviewer/scripts/gsd_roadmap.py get-phase <N>
```

Check each success criterion from the phase definition. Write `XX-VERIFICATION.md`:

```markdown
# Phase [X]: [Name] — Verification

**Date:** [date]

## Success Criteria Check
- [x] [Criterion 1] — VERIFIED: [evidence]
- [x] [Criterion 2] — VERIFIED: [evidence]
- [ ] [Criterion 3] — FAILED: [what's missing]

## Result: PASS / FAIL
```

## Related Skills

- `gsd-phase-executor` — Produces the code this skill reviews
- `gsd-testing` — Generate tests for reviewed code
- `gsd-debugger` — Debug issues found during review
- `gsd-milestone-manager` — Reviews feed into milestone completion
