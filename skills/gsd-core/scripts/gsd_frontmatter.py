#!/usr/bin/env python3
"""GSD Frontmatter — Generic YAML frontmatter CRUD for any markdown file.

Usage:
    python3 gsd_frontmatter.py extract <file>
    python3 gsd_frontmatter.py update <file> <key> <value>
    python3 gsd_frontmatter.py reconstruct <file>  (reads JSON from stdin)
"""

import json;
import re;
import sys;


def extract_frontmatter(content):
    """Parse YAML-like frontmatter from markdown content.
    Supports --- delimited blocks and **Key:** value bold format.
    Returns dict of parsed fields.
    """
    frontmatter = {};

    # Try --- delimited YAML block first
    yaml_match = re.search(r"(?:^|\n)\s*---\r?\n([\s\S]+?)\r?\n---", content);
    if yaml_match:
        yaml_text = yaml_match.group(1);
        for line in yaml_text.splitlines():
            line = line.strip();
            if not line:
                continue;
            key_match = re.match(r"([a-zA-Z0-9_-]+):\s*(.*)", line);
            if key_match:
                key = key_match.group(1);
                value = key_match.group(2).strip().strip("\"'");
                # Handle inline arrays [a, b, c]
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()];
                frontmatter[key] = value;
        return frontmatter;

    # Fallback: parse **Key:** value bold format (STATE.md style)
    for match in re.finditer(r"\*\*([^*]+):\*\*\s*(.+)", content):
        key = match.group(1).strip();
        value = match.group(2).strip();
        frontmatter[key] = value;

    return frontmatter;


def reconstruct_frontmatter(data):
    """Rebuild YAML frontmatter string from dict."""
    lines = ["---"];
    for key, value in data.items():
        if value is None:
            continue;
        if isinstance(value, list):
            if len(value) == 0:
                lines.append(f"{key}: []");
            elif len(value) <= 3 and all(isinstance(v, str) for v in value):
                joined = ", ".join(value);
                if len(joined) < 60:
                    lines.append(f"{key}: [{joined}]");
                else:
                    lines.append(f"{key}:");
                    for item in value:
                        lines.append(f"  - {item}");
            else:
                lines.append(f"{key}:");
                for item in value:
                    lines.append(f"  - {item}");
        elif isinstance(value, dict):
            lines.append(f"{key}:");
            for k, v in value.items():
                lines.append(f"  {k}: {v}");
        else:
            lines.append(f"{key}: {value}");
    lines.append("---");
    return "\n".join(lines);


def cmd_extract(filepath):
    """Parse frontmatter from file and output as JSON."""
    try:
        with open(filepath) as f:
            content = f.read();
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {filepath}"}));
        sys.exit(1);

    fm = extract_frontmatter(content);
    print(json.dumps(fm, indent=2));


def cmd_update(filepath, key, value):
    """Update a frontmatter field in a file."""
    try:
        with open(filepath) as f:
            content = f.read();
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {filepath}"}));
        sys.exit(1);

    escaped_key = re.escape(key);

    # Try --- YAML block
    yaml_match = re.search(r"((?:^|\n)\s*---\r?\n)([\s\S]+?)(\r?\n---)", content);
    if yaml_match:
        yaml_text = yaml_match.group(2);
        key_pattern = re.compile(rf"^({re.escape(key)}:\s*)(.*)$", re.MULTILINE);
        if key_pattern.search(yaml_text):
            new_yaml = key_pattern.sub(rf"\g<1>{value}", yaml_text);
            content = content[:yaml_match.start(2)] + new_yaml + content[yaml_match.end(2):];
        else:
            # Add new key
            new_yaml = yaml_text.rstrip() + f"\n{key}: {value}";
            content = content[:yaml_match.start(2)] + new_yaml + content[yaml_match.end(2):];
        with open(filepath, "w") as f:
            f.write(content);
        print(json.dumps({"updated": True, "key": key}));
        return;

    # Try **Key:** bold format
    bold_pattern = re.compile(rf"(\*\*{escaped_key}:\*\*\s*)(.*)", re.IGNORECASE);
    if bold_pattern.search(content):
        content = bold_pattern.sub(rf"\g<1>{value}", content);
        with open(filepath, "w") as f:
            f.write(content);
        print(json.dumps({"updated": True, "key": key}));
        return;

    print(json.dumps({"updated": False, "reason": f'Key "{key}" not found'}));


def cmd_reconstruct(filepath):
    """Rebuild frontmatter from JSON input (stdin)."""
    try:
        data = json.load(sys.stdin);
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON on stdin"}));
        sys.exit(1);

    try:
        with open(filepath) as f:
            content = f.read();
    except FileNotFoundError:
        content = "";

    new_fm = reconstruct_frontmatter(data);

    # Replace existing frontmatter or prepend
    yaml_match = re.search(r"(?:^|\n)\s*---\r?\n[\s\S]+?\r?\n---\r?\n?", content);
    if yaml_match:
        content = content[:yaml_match.start()] + new_fm + "\n" + content[yaml_match.end():];
    else:
        content = new_fm + "\n\n" + content;

    with open(filepath, "w") as f:
        f.write(content);
    print(json.dumps({"reconstructed": True}));


def main():
    if len(sys.argv) < 3:
        print("Usage: gsd_frontmatter.py <command> <file> [key] [value]");
        print("Commands: extract, update, reconstruct");
        sys.exit(1);

    cmd = sys.argv[1];
    filepath = sys.argv[2];

    if cmd == "extract":
        cmd_extract(filepath);
    elif cmd == "update":
        if len(sys.argv) < 5:
            print("Usage: gsd_frontmatter.py update <file> <key> <value>");
            sys.exit(1);
        cmd_update(filepath, sys.argv[3], " ".join(sys.argv[4:]));
    elif cmd == "reconstruct":
        cmd_reconstruct(filepath);
    else:
        print(f"Unknown command: {cmd}");
        sys.exit(1);


if __name__ == "__main__":
    main();
