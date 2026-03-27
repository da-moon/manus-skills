#!/usr/bin/env python3
"""GSD Init — Initialize or validate the .gsd/ directory structure.

Usage:
    python3 gsd_init.py [--validate] [--repair]

Creates .gsd/ with config.json, STATE.md, ROADMAP.md if missing.
--validate checks structural integrity without modifying.
--repair fixes common issues (missing dirs, broken frontmatter).
Returns JSON with project state summary.
"""

import argparse;
import json;
import os;
import sys;

DEFAULT_CONFIG = {
    "model_profile": "balanced",
    "commit_docs": True,
    "parallelization": True,
    "search_gitignored": False,
    "git": {
        "branching_strategy": "none",
        "phase_branch_template": "gsd/phase-{phase}-{slug}",
        "milestone_branch_template": "gsd/{milestone}-{slug}",
    },
    "workflow": {
        "research": True,
        "plan_check": True,
        "verifier": True,
        "ui_phase": True,
        "skip_discuss": False,
    },
};

STATE_TEMPLATE = """**Project:** {project_name}
**Milestone:** v1.0 — Initial Release
**Current Phase:** 1
**Phase Name:** Planning
**Plan:** 0 of 0
**Status:** Not Started
**Last Activity:** {date}

## Current Position
Status: Not started
Last activity: Project initialized
Plan: 0 of 0
""";

ROADMAP_TEMPLATE = """# Roadmap

## Phase Summary
<!-- Checklist of all phases -->

## Phases
<!-- Phase details will be added by gsd-phase-planner -->
""";


def find_project_root():
    """Walk up from cwd to find existing .gsd/ or return cwd."""
    d = os.getcwd();
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".gsd")):
            return d;
        d = os.path.dirname(d);
    return os.getcwd();


def ensure_dir(path):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True);


def validate_structure(gsd_dir):
    """Check .gsd/ structural integrity. Returns list of issues."""
    issues = [];
    required_files = ["config.json", "STATE.md", "ROADMAP.md"];
    required_dirs = ["phases", "todos", "todos/pending", "todos/done"];

    for f in required_files:
        fp = os.path.join(gsd_dir, f);
        if not os.path.isfile(fp):
            issues.append(f"missing file: {f}");
        elif f == "config.json":
            try:
                with open(fp) as fh:
                    json.load(fh);
            except (json.JSONDecodeError, ValueError):
                issues.append(f"invalid JSON: {f}");

    for d in required_dirs:
        dp = os.path.join(gsd_dir, d);
        if not os.path.isdir(dp):
            issues.append(f"missing directory: {d}");

    return issues;


def repair_structure(gsd_dir, project_name, date):
    """Repair common structural issues."""
    repaired = [];

    # Ensure directories
    for d in ["phases", "todos", "todos/pending", "todos/done", "milestones"]:
        dp = os.path.join(gsd_dir, d);
        if not os.path.isdir(dp):
            ensure_dir(dp);
            repaired.append(f"created directory: {d}");

    # Ensure config.json
    config_path = os.path.join(gsd_dir, "config.json");
    if not os.path.isfile(config_path):
        with open(config_path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2);
        repaired.append("created config.json");
    else:
        try:
            with open(config_path) as f:
                json.load(f);
        except (json.JSONDecodeError, ValueError):
            with open(config_path, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2);
            repaired.append("repaired config.json (was invalid JSON)");

    # Ensure STATE.md
    state_path = os.path.join(gsd_dir, "STATE.md");
    if not os.path.isfile(state_path):
        with open(state_path, "w") as f:
            f.write(STATE_TEMPLATE.format(project_name=project_name, date=date));
        repaired.append("created STATE.md");

    # Ensure ROADMAP.md
    roadmap_path = os.path.join(gsd_dir, "ROADMAP.md");
    if not os.path.isfile(roadmap_path):
        with open(roadmap_path, "w") as f:
            f.write(ROADMAP_TEMPLATE);
        repaired.append("created ROADMAP.md");

    return repaired;


def get_project_summary(project_root):
    """Build a summary of the project state."""
    gsd_dir = os.path.join(project_root, ".gsd");
    summary = {
        "project_root": project_root,
        "gsd_exists": os.path.isdir(gsd_dir),
        "config_exists": os.path.isfile(os.path.join(gsd_dir, "config.json")),
        "state_exists": os.path.isfile(os.path.join(gsd_dir, "STATE.md")),
        "roadmap_exists": os.path.isfile(os.path.join(gsd_dir, "ROADMAP.md")),
        "project_exists": os.path.isfile(os.path.join(gsd_dir, "PROJECT.md")),
        "requirements_exists": os.path.isfile(os.path.join(gsd_dir, "REQUIREMENTS.md")),
        "has_git": os.path.isdir(os.path.join(project_root, ".git")),
    };

    # Count phases
    phases_dir = os.path.join(gsd_dir, "phases");
    if os.path.isdir(phases_dir):
        phase_dirs = [d for d in os.listdir(phases_dir) if os.path.isdir(os.path.join(phases_dir, d))];
        summary["phase_count"] = len(phase_dirs);
    else:
        summary["phase_count"] = 0;

    # Load config if exists
    config_path = os.path.join(gsd_dir, "config.json");
    if os.path.isfile(config_path):
        try:
            with open(config_path) as f:
                summary["config"] = json.load(f);
        except (json.JSONDecodeError, ValueError):
            summary["config"] = None;

    return summary;


def main():
    parser = argparse.ArgumentParser(description="GSD directory initialization");
    parser.add_argument("--validate", action="store_true", help="Check integrity only");
    parser.add_argument("--repair", action="store_true", help="Fix common issues");
    args = parser.parse_args();

    project_root = find_project_root();
    gsd_dir = os.path.join(project_root, ".gsd");

    from datetime import date;
    today = date.today().isoformat();
    project_name = os.path.basename(project_root);

    if args.validate:
        if not os.path.isdir(gsd_dir):
            print(json.dumps({"valid": False, "issues": [".gsd/ directory not found"]}));
            sys.exit(1);
        issues = validate_structure(gsd_dir);
        result = {"valid": len(issues) == 0, "issues": issues};
        print(json.dumps(result, indent=2));
        sys.exit(0 if result["valid"] else 1);

    if args.repair:
        if not os.path.isdir(gsd_dir):
            ensure_dir(gsd_dir);
        repaired = repair_structure(gsd_dir, project_name, today);
        remaining = validate_structure(gsd_dir);
        result = {"repaired": repaired, "remaining_issues": remaining, "valid": len(remaining) == 0};
        print(json.dumps(result, indent=2));
        sys.exit(0);

    # Default: initialize if needed, then return summary
    if not os.path.isdir(gsd_dir):
        ensure_dir(gsd_dir);
        repair_structure(gsd_dir, project_name, today);
        summary = get_project_summary(project_root);
        summary["initialized"] = True;
        print(json.dumps(summary, indent=2));
    else:
        summary = get_project_summary(project_root);
        summary["initialized"] = False;
        print(json.dumps(summary, indent=2));


if __name__ == "__main__":
    main();
