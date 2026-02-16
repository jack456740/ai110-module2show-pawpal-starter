#!/usr/bin/env python3
"""
Generate a concise commit message summary from staged git changes.

Usage:
  python scripts/generate_commit_message.py

The script reads staged changes (`git diff --staged --name-status`) and
prints a suggested commit message with a short header and bullet list.
"""
import subprocess
import sys


def get_staged_changes():
    try:
        out = subprocess.check_output(["git", "diff", "--staged", "--name-status"], text=True)
    except subprocess.CalledProcessError:
        return []
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    changes = []
    for line in lines:
        parts = line.split('\t')
        if len(parts) == 2:
            status, path = parts
        else:
            # fallback split by whitespace
            parts = line.split(None, 1)
            if len(parts) == 2:
                status, path = parts
            else:
                continue
        changes.append((status, path))
    return changes


def summarize(changes):
    added = [p for s, p in changes if s == 'A']
    modified = [p for s, p in changes if s == 'M']
    deleted = [p for s, p in changes if s == 'D']

    header_parts = []
    if added:
        header_parts.append('add')
    if modified:
        header_parts.append('update')
    if deleted:
        header_parts.append('remove')

    header = 'chore: ' + ', '.join(header_parts) + ' files' if header_parts else 'chore: changes'

    body_lines = []
    if added:
        body_lines.append(f"Added: {len(added)} files")
        for p in added[:10]:
            body_lines.append(f"  - {p}")
    if modified:
        body_lines.append(f"Modified: {len(modified)} files")
        for p in modified[:10]:
            body_lines.append(f"  - {p}")
    if deleted:
        body_lines.append(f"Deleted: {len(deleted)} files")
        for p in deleted[:10]:
            body_lines.append(f"  - {p}")

    if not body_lines:
        body_lines = ["No staged changes found."]

    message = header + '\n\n' + '\n'.join(body_lines)
    return message


def main():
    changes = get_staged_changes()
    msg = summarize(changes)
    print(msg)


if __name__ == '__main__':
    main()
