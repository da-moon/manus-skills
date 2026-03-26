#!/usr/bin/env python3
"""Check upstream GSD repo for updates against tracked version.

Usage:
    python3 check_upstream.py <manus_skills_dir> <upstream_dir>

Outputs JSON with:
    - current_version: tracked version
    - upstream_version: latest upstream version
    - current_commit: tracked commit
    - upstream_commit: latest upstream commit
    - needs_update: boolean
    - changed_files: list of changed files (if needs_update)
    - affected_skills: list of skills that need updating
"""

import json
import os
import subprocess
import sys


SKILL_FILE_MAP = {
    "commands/gsd/new-project": "gsd-project-setup",
    "commands/gsd/plan-phase": "gsd-phase-planner",
    "commands/gsd/add-phase": "gsd-phase-planner",
    "commands/gsd/insert-phase": "gsd-phase-planner",
    "commands/gsd/remove-phase": "gsd-phase-planner",
    "commands/gsd/discuss-phase": "gsd-phase-planner",
    "commands/gsd/do": "gsd-phase-executor",
    "commands/gsd/next": "gsd-phase-executor",
    "commands/gsd/fast": "gsd-phase-executor",
    "commands/gsd/quick": "gsd-phase-executor",
    "commands/gsd/autonomous": "gsd-phase-executor",
    "commands/gsd/milestone": "gsd-milestone-manager",
    "commands/gsd/complete-milestone": "gsd-milestone-manager",
    "commands/gsd/audit": "gsd-milestone-manager",
    "commands/gsd/review": "gsd-code-reviewer",
    "commands/gsd/verify": "gsd-code-reviewer",
    "commands/gsd/uat": "gsd-code-reviewer",
    "commands/gsd/debug": "gsd-debugger",
    "commands/gsd/forensics": "gsd-debugger",
    "commands/gsd/health": "gsd-debugger",
    "commands/gsd/test": "gsd-testing",
    "commands/gsd/todo": "gsd-testing",
    "commands/gsd/research": "gsd-research",
    "commands/gsd/map-codebase": "gsd-research",
    "commands/gsd/pause": "gsd-session-manager",
    "commands/gsd/resume": "gsd-session-manager",
    "commands/gsd/report": "gsd-session-manager",
    "commands/gsd/workspace": "gsd-workspace-manager",
    "commands/gsd/settings": "gsd-workspace-manager",
    "commands/gsd/cleanup": "gsd-workspace-manager",
    "commands/gsd/ui": "gsd-ui-developer",
    "commands/gsd/ship": "gsd-git-shipper",
    "commands/gsd/pr": "gsd-git-shipper",
    "commands/gsd/backlog": "gsd-git-shipper",
    "commands/gsd/manage": "gsd-manager-mode",
    "get-shit-done/bin/lib/": "gsd-core",
    "get-shit-done/workflows/": "multiple",
    "agents/": "review",
    "templates/": "gsd-core",
}

WORKFLOW_SKILL_MAP = {
    "new-project": "gsd-project-setup",
    "plan-phase": "gsd-phase-planner",
    "execute-phase": "gsd-phase-executor",
    "quick": "gsd-phase-executor",
    "transition": "gsd-phase-executor",
    "complete-milestone": "gsd-milestone-manager",
    "review": "gsd-code-reviewer",
    "verify": "gsd-code-reviewer",
    "debug": "gsd-debugger",
    "research": "gsd-research",
    "pause": "gsd-session-manager",
    "resume": "gsd-session-manager",
    "ship": "gsd-git-shipper",
    "manage": "gsd-manager-mode",
}


def run_cmd(cmd, cwd=None):
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    return result.stdout.strip()


def map_file_to_skill(filepath):
    """Map a changed file path to the affected skill(s)."""
    skills = set()

    for pattern, skill in SKILL_FILE_MAP.items():
        if filepath.startswith(pattern):
            if skill == "multiple":
                # Map workflow files to specific skills
                basename = os.path.basename(filepath).replace(".md", "")
                for wf_pattern, wf_skill in WORKFLOW_SKILL_MAP.items():
                    if wf_pattern in basename:
                        skills.add(wf_skill)
                        break
                else:
                    skills.add("review")
            elif skill == "review":
                skills.add("review")
            else:
                skills.add(skill)
            break

    return skills


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <manus_skills_dir> <upstream_dir>")
        sys.exit(1)

    manus_dir = sys.argv[1]
    upstream_dir = sys.argv[2]

    # Read tracked version
    tracking_file = os.path.join(manus_dir, ".gsd-upstream.json")
    if not os.path.exists(tracking_file):
        print(json.dumps({"error": "No .gsd-upstream.json found"}, indent=2))
        sys.exit(1)

    with open(tracking_file) as f:
        tracked = json.load(f)

    current_version = tracked.get("version", "unknown")
    current_commit = tracked.get("commit", "unknown")

    # Get upstream version
    upstream_version = run_cmd(
        "node -p \"require('./package.json').version\"", cwd=upstream_dir
    )
    upstream_commit = run_cmd("git rev-parse HEAD", cwd=upstream_dir)

    needs_update = current_commit != upstream_commit

    result = {
        "current_version": current_version,
        "upstream_version": upstream_version,
        "current_commit": current_commit,
        "upstream_commit": upstream_commit,
        "needs_update": needs_update,
        "changed_files": [],
        "affected_skills": [],
    }

    if needs_update:
        # Get changed files
        changed = run_cmd(
            f"git diff --name-only {current_commit}..HEAD 2>/dev/null || "
            f"git diff --name-only HEAD~10..HEAD",
            cwd=upstream_dir,
        )
        changed_files = [f for f in changed.split("\n") if f]
        result["changed_files"] = changed_files

        # Map to affected skills
        all_skills = set()
        for f in changed_files:
            skills = map_file_to_skill(f)
            all_skills.update(skills)

        result["affected_skills"] = sorted(list(all_skills))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
