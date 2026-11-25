#!/usr/bin/env python3
"""One Line, One Laugh — make.fun entry.

Writes a single funny line of text to /output/entry.txt.

The bounty gate requires UTF-8 text of 1 to 200 characters, not only
whitespace. This program writes the line, reads it back, and verifies
the gate itself before exiting, so a bad write can never pass silently.

The line: a robot vacuum maps the flat, then rats out its owner to the
landlord. Familiar gadget, absurd escalation, punchline lands in the
subject line.
"""

import os
import sys

# The entry: one line, well under the 200-character cap.
ENTRY = (
    "My Roomba mapped my apartment and emailed the floor plan to my "
    "landlord with the subject line: 'He lives like this.'"
)

MAX_CHARS = 200

# Local-testing escape hatch: set ENTRY_TEXT to write a different line
# (for example when checking a variant against the gate). The sealed
# grader run never sets this, so the submitted line is always ENTRY.
ENTRY_OVERRIDE_ENV = "ENTRY_TEXT"


def pick_entry() -> str:
    """Return the line to submit: ENTRY, or the env override if set."""
    override = os.environ.get(ENTRY_OVERRIDE_ENV)
    if override is not None:
        return override.strip()
    return ENTRY.strip()


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    # Never delete the output directory: the grader mounts it and runs
    # this program as an unprivileged user, so removing it fails the run.
    os.makedirs(out_dir, exist_ok=True)

    line = pick_entry()
    if not line:
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: entry is {len(line)} chars, over the {MAX_CHARS} cap",
            file=sys.stderr,
        )
        return 1
    if "\n" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")

    # Read it back and verify the gate exactly as the scorer checks it:
    # 1-200 characters of UTF-8, not only whitespace, a single line.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()

    body = written.rstrip("\n")
    chars = len(body)
    if not (1 <= chars <= MAX_CHARS) or not body.strip():
        print(
            f"error: gate check failed, entry.txt is {chars} chars",
            file=sys.stderr,
        )
        return 1
    if "\n" in body:
        print("error: gate check failed, entry.txt is not a single line",
              file=sys.stderr)
        return 1

    print(f"wrote {out_path} ({chars} chars): {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
