#!/usr/bin/env python3
"""GSD State — Parse and update STATE.md frontmatter fields.

Usage:
    python3 gsd_state.py load
    python3 gsd_state.py get [field]
    python3 gsd_state.py update <field> <value>
    python3 gsd_state.py patch --field1 val1 --field2 val2
    python3 gsd_state.py snapshot
"""

import json;
import os;
import re;
import sys;


def find_gsd_dir():
    """Walk up from cwd to find the project root containing .gsd/."""
    d = os.getcwd();
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".gsd")):
            return os.path.join(d, ".gsd");
        d = os.path.dirname(d);
    return os.path.join(os.getcwd(), ".gsd");


def get_state_path():
    """Return path to STATE.md."""
    return os.path.join(find_gsd_dir(), "STATE.md");


def extract_field(content, field_name):
    """Extract a field value from STATE.md content.
    Supports both **Field:** bold and plain Field: format.
    """
    escaped = re.escape(field_name);
    # Bold format
    bold = re.search(rf"\*\*{escaped}:\*\*\s*(.+)", content, re.IGNORECASE);
    if bold:
        return bold.group(1).strip();
    # Plain format
    plain = re.search(rf"^{escaped}:\s*(.+)", content, re.IGNORECASE | re.MULTILINE);
    if plain:
        return plain.group(1).strip();
    return None;


def replace_field(content, field_name, new_value):
    """Replace a field value in STATE.md content.
    Returns modified content or None if field not found.
    """
    escaped = re.escape(field_name);
    # Bold format
    bold_pattern = re.compile(rf"(\*\*{escaped}:\*\*\s*)(.*)", re.IGNORECASE);
    if bold_pattern.search(content):
        return bold_pattern.sub(rf"\g<1>{new_value}", content, count=1);
    # Plain format
    plain_pattern = re.compile(rf"(^{escaped}:\s*)(.*)", re.IGNORECASE | re.MULTILINE);
    if plain_pattern.search(content):
        return plain_pattern.sub(rf"\g<1>{new_value}", content, count=1);
    return None;


def cmd_load():
    """Load full state as JSON."""
    state_path = get_state_path();
    gsd_dir = find_gsd_dir();
    config_path = os.path.join(gsd_dir, "config.json");

    result = {
        "state_exists": os.path.isfile(state_path),
        "config_exists": os.path.isfile(config_path),
        "roadmap_exists": os.path.isfile(os.path.join(gsd_dir, "ROADMAP.md")),
    };

    if os.path.isfile(config_path):
        try:
            with open(config_path) as f:
                result["config"] = json.load(f);
        except (json.JSONDecodeError, ValueError):
            result["config"] = None;

    if os.path.isfile(state_path):
        with open(state_path) as f:
            result["state_raw"] = f.read();

    print(json.dumps(result, indent=2));


def cmd_get(field=None):
    """Get specific field or full content."""
    state_path = get_state_path();
    if not os.path.isfile(state_path):
        print(json.dumps({"error": "STATE.md not found"}));
        sys.exit(1);

    with open(state_path) as f:
        content = f.read();

    if not field:
        print(json.dumps({"content": content}));
        return;

    value = extract_field(content, field);
    if value is not None:
        print(json.dumps({field: value}));
    else:
        # Try section match
        section_pattern = re.compile(rf"##\s*{re.escape(field)}\s*\n([\s\S]*?)(?=\n##|$)", re.IGNORECASE);
        section_match = section_pattern.search(content);
        if section_match:
            print(json.dumps({field: section_match.group(1).strip()}));
        else:
            print(json.dumps({"error": f'Field or section "{field}" not found'}));


def cmd_update(field, value):
    """Update a single field."""
    state_path = get_state_path();
    if not os.path.isfile(state_path):
        print(json.dumps({"updated": False, "reason": "STATE.md not found"}));
        sys.exit(1);

    with open(state_path) as f:
        content = f.read();

    new_content = replace_field(content, field, value);
    if new_content is not None:
        with open(state_path, "w") as f:
            f.write(new_content);
        print(json.dumps({"updated": True}));
    else:
        print(json.dumps({"updated": False, "reason": f'Field "{field}" not found'}));


def cmd_patch(patches):
    """Batch update multiple fields."""
    state_path = get_state_path();
    if not os.path.isfile(state_path):
        print(json.dumps({"error": "STATE.md not found"}));
        sys.exit(1);

    with open(state_path) as f:
        content = f.read();

    updated = [];
    failed = [];
    for field, value in patches.items():
        new_content = replace_field(content, field, value);
        if new_content is not None:
            content = new_content;
            updated.append(field);
        else:
            failed.append(field);

    if updated:
        with open(state_path, "w") as f:
            f.write(content);

    print(json.dumps({"updated": updated, "failed": failed}));


def cmd_snapshot():
    """Structured parse of all state data."""
    state_path = get_state_path();
    if not os.path.isfile(state_path):
        print(json.dumps({"error": "STATE.md not found"}));
        sys.exit(1);

    with open(state_path) as f:
        content = f.read();

    fields = [
        "Project", "Milestone", "Current Phase", "Phase Name",
        "Plan", "Status", "Last Activity",
    ];
    snapshot = {};
    for field in fields:
        val = extract_field(content, field);
        if val is not None:
            key = field.lower().replace(" ", "_");
            snapshot[key] = val;

    print(json.dumps(snapshot, indent=2));


def main():
    if len(sys.argv) < 2:
        print("Usage: gsd_state.py <command> [args]");
        print("Commands: load, get, update, patch, snapshot");
        sys.exit(1);

    cmd = sys.argv[1];

    if cmd == "load":
        cmd_load();
    elif cmd == "get":
        field = sys.argv[2] if len(sys.argv) > 2 else None;
        cmd_get(field);
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Usage: gsd_state.py update <field> <value>");
            sys.exit(1);
        cmd_update(sys.argv[2], " ".join(sys.argv[3:]));
    elif cmd == "patch":
        # Parse --field value pairs
        patches = {};
        i = 2;
        while i < len(sys.argv):
            if sys.argv[i].startswith("--"):
                key = sys.argv[i][2:].replace("-", " ").title();
                if i + 1 < len(sys.argv):
                    patches[key] = sys.argv[i + 1];
                    i += 2;
                else:
                    i += 1;
            else:
                i += 1;
        cmd_patch(patches);
    elif cmd == "snapshot":
        cmd_snapshot();
    else:
        print(f"Unknown command: {cmd}");
        sys.exit(1);


if __name__ == "__main__":
    main();
