---
name: gsd-testing
description: Generate and manage tests for project code. Creates unit tests, integration tests, and end-to-end tests based on implementation and requirements. Also manages todo items for tracking work items. Use when tests need to be written, updated, or when managing project todos.
---

# GSD Testing

**Prerequisite:** Read `gsd-core` skill first: `read /home/ubuntu/skills/gsd-core/SKILL.md`

Generate tests for project code and manage todo items for tracking work.

## Quick Start

When the user says "write tests", "add tests for", "generate tests", or "test phase N":

1. Identify the code to test
2. Follow the test generation workflow

## Test Generation Workflow

### Step 1: Identify Test Targets

Determine what needs testing:

**From a phase:** Read SUMMARY.md files to find all modified files:
```bash
# Glob for summaries
.gsd/phases/XX-name/XX-*-SUMMARY.md
```

**From a specific file:** User specifies the file directly.

**From requirements:** Map REQ-XX acceptance criteria to test cases.

### Step 2: Analyze Code

For each file to test:

1. Read the source file
2. Identify public functions/methods/classes
3. Identify edge cases, error paths, boundary conditions
4. Check for existing tests

### Step 3: Generate Tests

Create test files following project conventions. Auto-detect the test framework:

| Language | Framework Detection | Default |
|---|---|---|
| Python | `pytest` in deps, `unittest` imports | pytest |
| JavaScript/TypeScript | `jest`, `vitest`, `mocha` in package.json | vitest |
| Go | Built-in `testing` package | testing |
| Rust | Built-in `#[test]` | built-in |

Test structure per function:

```
1. Happy path — normal inputs, expected output
2. Edge cases — empty input, null, boundary values
3. Error cases — invalid input, expected failures
4. Integration — interaction with dependencies
```

### Step 4: Write Test Files

Follow naming conventions:

| Language | Convention | Example |
|---|---|---|
| Python | `test_<module>.py` in `tests/` | `tests/test_auth.py` |
| JS/TS | `<module>.test.ts` or `__tests__/` | `src/auth.test.ts` |
| Go | `<module>_test.go` same package | `auth_test.go` |

Test file structure (Python/pytest example):

```python
"""Tests for [module] — [what it does]."""

import pytest
from module import function_under_test


class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self):
        """Should [expected behavior] when [condition]."""
        result = function_under_test(valid_input)
        assert result == expected_output

    def test_edge_case_empty(self):
        """Should handle empty input gracefully."""
        result = function_under_test("")
        assert result == default_value

    def test_error_invalid_input(self):
        """Should raise ValueError for invalid input."""
        with pytest.raises(ValueError):
            function_under_test(invalid_input)
```

### Step 5: Run and Verify Tests

```bash
# Python
python -m pytest tests/ -v
# JavaScript/TypeScript
npx vitest run  # or npx jest
# Go
go test ./...
```

Fix any test failures. Ensure all tests pass before committing.

### Step 6: Commit

```bash
git add tests/
git commit -m "test: add tests for [module/feature]"
```

## Todo Management

### Create Todo

Create a todo file in `.gsd/todos/pending/`:

```markdown
# [Todo Title]

**Created:** [date]
**Priority:** High / Medium / Low
**Phase:** [phase number, if related]
**Requirement:** [REQ-XX, if related]

## Description
[What needs to be done]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

File naming: `<slug>.md` (e.g., `fix-auth-timeout.md`)

### List Todos

```bash
# Use match tool
.gsd/todos/pending/*.md
```

### Complete Todo

Move from pending to done:
```bash
mv .gsd/todos/pending/<todo>.md .gsd/todos/done/<todo>.md
```

Update the todo file with completion date and notes.

### Todo from Code Comments

Scan for TODO/FIXME comments and create todo files:

```bash
grep -rn "TODO\|FIXME" --include="*.py" --include="*.js" --include="*.ts" --include="*.go"
```

For each found comment, create a corresponding todo file in `.gsd/todos/pending/`.

## Test Coverage Analysis

When the user asks "what's our test coverage" or "what needs tests":

1. Identify all source files in the project
2. Check which have corresponding test files
3. Report coverage gaps:

```
Test Coverage Report:
  src/auth.py ............ TESTED (tests/test_auth.py)
  src/database.py ........ TESTED (tests/test_database.py)
  src/api/routes.py ...... NO TESTS
  src/api/middleware.py ... NO TESTS
  src/utils.py ........... TESTED (tests/test_utils.py)

Coverage: 3/5 modules (60%)
Priority gaps: api/routes.py, api/middleware.py
```

## Related Skills

- `gsd-phase-executor` — Tests should be written during or after execution
- `gsd-code-reviewer` — Reviews check for test coverage
- `gsd-debugger` — Write regression tests after fixing bugs
