#!/usr/bin/env python3
"""GSD Roadmap — Parse and manipulate ROADMAP.md.

Usage:
    python3 gsd_roadmap.py get-phase <N>
    python3 gsd_roadmap.py analyze
    python3 gsd_roadmap.py update-progress <N>
"""

import json;
import os;
import re;
import sys;
from datetime import date;


def find_gsd_dir():
    """Walk up from cwd to find the project root containing .gsd/."""
    d = os.getcwd();
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".gsd")):
            return os.path.join(d, ".gsd");
        d = os.path.dirname(d);
    return os.path.join(os.getcwd(), ".gsd");


def get_roadmap_path():
    """Return path to ROADMAP.md."""
    return os.path.join(find_gsd_dir(), "ROADMAP.md");


def normalize_phase_name(phase_num):
    """Zero-pad phase number for directory matching (e.g., '1' -> '01')."""
    parts = str(phase_num).split(".");
    parts[0] = parts[0].zfill(2);
    return ".".join(parts);


def cmd_get_phase(phase_num):
    """Extract phase section, goal, success criteria from ROADMAP.md."""
    roadmap_path = get_roadmap_path();
    if not os.path.isfile(roadmap_path):
        print(json.dumps({"found": False, "error": "ROADMAP.md not found"}));
        return;

    with open(roadmap_path) as f:
        content = f.read();

    escaped = re.escape(str(phase_num));
    # Match ## Phase N:, ### Phase N:, or #### Phase N:
    pattern = re.compile(rf"(#{{{2,4}}}\s*Phase\s+{escaped}:\s*([^\n]+))", re.IGNORECASE);
    header_match = pattern.search(content);

    if not header_match:
        print(json.dumps({"found": False, "phase_number": str(phase_num)}));
        return;

    phase_name = header_match.group(2).strip();
    header_index = header_match.start();

    # Find end of section (next phase header or end of file)
    rest = content[header_index:];
    next_header = re.search(r"\n#{2,4}\s+Phase\s+\d", rest, re.IGNORECASE);
    section_end = header_index + next_header.start() if next_header else len(content);
    section = content[header_index:section_end].strip();

    # Extract goal
    goal_match = re.search(r"\*\*Goal(?::\*\*|\*\*:)\s*([^\n]+)", section, re.IGNORECASE);
    goal = goal_match.group(1).strip() if goal_match else None;

    # Extract success criteria
    criteria_match = re.search(
        r"\*\*Success Criteria\*\*[^\n]*:\s*\n((?:\s*\d+\.\s*[^\n]+\n?)+)",
        section, re.IGNORECASE,
    );
    success_criteria = [];
    if criteria_match:
        for line in criteria_match.group(1).strip().splitlines():
            item = re.sub(r"^\s*\d+\.\s*", "", line).strip();
            if item:
                success_criteria.append(item);

    print(json.dumps({
        "found": True,
        "phase_number": str(phase_num),
        "phase_name": phase_name,
        "goal": goal,
        "success_criteria": success_criteria,
        "section": section,
    }, indent=2));


def cmd_analyze():
    """Full roadmap parse with disk status per phase."""
    roadmap_path = get_roadmap_path();
    gsd_dir = find_gsd_dir();

    if not os.path.isfile(roadmap_path):
        print(json.dumps({"error": "ROADMAP.md not found", "phases": []}));
        return;

    with open(roadmap_path) as f:
        content = f.read();

    phases_dir = os.path.join(gsd_dir, "phases");
    phase_pattern = re.compile(r"#{2,4}\s*Phase\s+(\d+[A-Z]?(?:\.\d+)*)\s*:\s*([^\n]+)", re.IGNORECASE);
    phases = [];

    for match in phase_pattern.finditer(content):
        phase_num = match.group(1);
        phase_name = re.sub(r"\(INSERTED\)", "", match.group(2), flags=re.IGNORECASE).strip();

        # Extract section
        start = match.start();
        rest = content[start:];
        next_h = re.search(r"\n#{2,4}\s+Phase\s+\d", rest, re.IGNORECASE);
        end = start + next_h.start() if next_h else len(content);
        section = content[start:end];

        goal_m = re.search(r"\*\*Goal(?::\*\*|\*\*:)\s*([^\n]+)", section, re.IGNORECASE);
        goal = goal_m.group(1).strip() if goal_m else None;

        depends_m = re.search(r"\*\*Depends on(?::\*\*|\*\*:)\s*([^\n]+)", section, re.IGNORECASE);
        depends_on = depends_m.group(1).strip() if depends_m else None;

        # Check disk status
        normalized = normalize_phase_name(phase_num);
        disk_status = "no_directory";
        plan_count = 0;
        summary_count = 0;

        if os.path.isdir(phases_dir):
            for d in os.listdir(phases_dir):
                dp = os.path.join(phases_dir, d);
                if os.path.isdir(dp) and (d.startswith(normalized + "-") or d == normalized):
                    files = os.listdir(dp);
                    plan_count = len([f for f in files if f.endswith("-PLAN.md") or f == "PLAN.md"]);
                    summary_count = len([f for f in files if f.endswith("-SUMMARY.md") or f == "SUMMARY.md"]);
                    has_context = any(f.endswith("-CONTEXT.md") or f == "CONTEXT.md" for f in files);
                    has_research = any(f.endswith("-RESEARCH.md") or f == "RESEARCH.md" for f in files);

                    if summary_count >= plan_count and plan_count > 0:
                        disk_status = "complete";
                    elif summary_count > 0:
                        disk_status = "partial";
                    elif plan_count > 0:
                        disk_status = "planned";
                    elif has_research:
                        disk_status = "researched";
                    elif has_context:
                        disk_status = "discussed";
                    else:
                        disk_status = "empty";
                    break;

        # Check roadmap checkbox
        cb_pattern = re.compile(rf"-\s*\[(x| )\]\s*.*Phase\s+{re.escape(phase_num)}[:\s]", re.IGNORECASE);
        cb_match = cb_pattern.search(content);
        roadmap_complete = cb_match and cb_match.group(1) == "x" if cb_match else False;

        if roadmap_complete and disk_status != "complete":
            disk_status = "complete";

        phases.append({
            "number": phase_num,
            "name": phase_name,
            "goal": goal,
            "depends_on": depends_on,
            "plan_count": plan_count,
            "summary_count": summary_count,
            "disk_status": disk_status,
            "roadmap_complete": roadmap_complete,
        });

    completed = len([p for p in phases if p["disk_status"] == "complete"]);
    total_plans = sum(p["plan_count"] for p in phases);
    total_summaries = sum(p["summary_count"] for p in phases);
    current = next((p["number"] for p in phases if p["disk_status"] in ("planned", "partial")), None);
    next_phase = next((p["number"] for p in phases if p["disk_status"] in ("empty", "no_directory", "discussed", "researched")), None);

    print(json.dumps({
        "phases": phases,
        "phase_count": len(phases),
        "completed_phases": completed,
        "total_plans": total_plans,
        "total_summaries": total_summaries,
        "progress_percent": min(100, round((total_summaries / total_plans) * 100)) if total_plans > 0 else 0,
        "current_phase": current,
        "next_phase": next_phase,
    }, indent=2));


def cmd_update_progress(phase_num):
    """Update plan/summary counts and checkboxes for a phase."""
    roadmap_path = get_roadmap_path();
    gsd_dir = find_gsd_dir();

    if not os.path.isfile(roadmap_path):
        print(json.dumps({"updated": False, "reason": "ROADMAP.md not found"}));
        return;

    # Find phase directory
    phases_dir = os.path.join(gsd_dir, "phases");
    normalized = normalize_phase_name(phase_num);
    phase_dir = None;
    plan_count = 0;
    summary_count = 0;
    summaries = [];

    if os.path.isdir(phases_dir):
        for d in os.listdir(phases_dir):
            dp = os.path.join(phases_dir, d);
            if os.path.isdir(dp) and (d.startswith(normalized + "-") or d == normalized):
                phase_dir = dp;
                files = os.listdir(dp);
                plan_count = len([f for f in files if f.endswith("-PLAN.md") or f == "PLAN.md"]);
                summary_count = len([f for f in files if f.endswith("-SUMMARY.md") or f == "SUMMARY.md"]);
                summaries = [f for f in files if f.endswith("-SUMMARY.md") or f == "SUMMARY.md"];
                break;

    if plan_count == 0:
        print(json.dumps({"updated": False, "reason": "No plans found"}));
        return;

    is_complete = summary_count >= plan_count;
    status = "Complete" if is_complete else ("In Progress" if summary_count > 0 else "Planned");
    today = date.today().isoformat();

    with open(roadmap_path) as f:
        content = f.read();

    escaped = re.escape(str(phase_num));

    # Update plan count in phase detail section
    plan_text = f"{summary_count}/{plan_count} plans complete" if is_complete else f"{summary_count}/{plan_count} plans executed";
    plan_pattern = re.compile(
        rf"(#{{2,4}}\s*Phase\s+{escaped}[\s\S]*?\*\*Plans:\*\*\s*)[^\n]+",
        re.IGNORECASE,
    );
    content = plan_pattern.sub(rf"\g<1>{plan_text}", content);

    # Check checkbox if complete
    if is_complete:
        cb_pattern = re.compile(rf"(-\s*\[) (\]\s*.*Phase\s+{escaped}[:\s][^\n]*)", re.IGNORECASE);
        content = cb_pattern.sub(rf"\g<1>x\g<2> (completed {today})", content);

    with open(roadmap_path, "w") as f:
        f.write(content);

    print(json.dumps({
        "updated": True,
        "phase": str(phase_num),
        "plan_count": plan_count,
        "summary_count": summary_count,
        "status": status,
        "complete": is_complete,
    }));


def main():
    if len(sys.argv) < 2:
        print("Usage: gsd_roadmap.py <command> [args]");
        print("Commands: get-phase, analyze, update-progress");
        sys.exit(1);

    cmd = sys.argv[1];

    if cmd == "get-phase":
        if len(sys.argv) < 3:
            print("Usage: gsd_roadmap.py get-phase <N>");
            sys.exit(1);
        cmd_get_phase(sys.argv[2]);
    elif cmd == "analyze":
        cmd_analyze();
    elif cmd == "update-progress":
        if len(sys.argv) < 3:
            print("Usage: gsd_roadmap.py update-progress <N>");
            sys.exit(1);
        cmd_update_progress(sys.argv[2]);
    else:
        print(f"Unknown command: {cmd}");
        sys.exit(1);


if __name__ == "__main__":
    main();
