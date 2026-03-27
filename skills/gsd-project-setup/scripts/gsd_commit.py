#!/usr/bin/env python3
"""GSD Commit — Smart git commit for .gsd/ documentation files.

Usage:
    python3 gsd_commit.py "message" [--files f1 f2 ...] [--no-verify]

Stages only .gsd/ files by default unless --files specifies others.
"""

import argparse;
import json;
import os;
import subprocess;
import sys;


def find_gsd_dir():
    """Walk up from cwd to find the project root containing .gsd/."""
    d = os.getcwd();
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".gsd")):
            return d;
        d = os.path.dirname(d);
    return os.getcwd();


def run_git(args, cwd=None, check=True):
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    );
    if check and result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr);
        sys.exit(1);
    return result.stdout.strip();


def main():
    parser = argparse.ArgumentParser(description="GSD smart git commit");
    parser.add_argument("message", help="Commit message");
    parser.add_argument("--files", nargs="*", default=None, help="Specific files to stage");
    parser.add_argument("--no-verify", action="store_true", help="Skip git hooks");
    args = parser.parse_args();

    project_root = find_gsd_dir();
    gsd_dir = os.path.join(project_root, ".gsd");

    if not os.path.isdir(gsd_dir):
        print(json.dumps({"error": ".gsd/ directory not found"}));
        sys.exit(1);

    # Determine files to stage
    if args.files:
        files_to_stage = args.files;
    else:
        # Stage all changed files under .gsd/
        status = run_git(["status", "--porcelain", "--", ".gsd/"], cwd=project_root, check=False);
        if not status:
            print(json.dumps({"committed": False, "reason": "No changes in .gsd/"}));
            return;
        files_to_stage = [];
        for line in status.splitlines():
            # Status format: XY filename
            if len(line) > 3:
                filepath = line[3:].strip();
                # Handle renamed files (old -> new)
                if " -> " in filepath:
                    filepath = filepath.split(" -> ")[1];
                files_to_stage.append(filepath);

    if not files_to_stage:
        print(json.dumps({"committed": False, "reason": "No files to stage"}));
        return;

    # Stage files
    run_git(["add", "--"] + files_to_stage, cwd=project_root);

    # Build commit command
    commit_cmd = ["commit", "-m", args.message];
    if args.no_verify:
        commit_cmd.append("--no-verify");

    # Commit
    result = subprocess.run(
        ["git"] + commit_cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    );

    if result.returncode != 0:
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print(json.dumps({"committed": False, "reason": "Nothing to commit"}));
        else:
            print(json.dumps({"committed": False, "error": result.stderr.strip()}));
            sys.exit(1);
    else:
        print(json.dumps({"committed": True, "message": args.message, "files": files_to_stage}));


if __name__ == "__main__":
    main();
