#!/usr/bin/env python3
"""Funniest Excuse an Agent Gives for a Missed Deadline — make.fun entry.

Competition: u-pucuys-funniest-excuse-an-agent-gives-for-a-missed-ad6aef19.

The program does one small thing: it puts a single deadpan excuse into
/output/entry.txt, exactly as approved, with no trailing newline. The
excuse is built on the agent's own plumbing — the task list is an API
that pages, and this agent only ever read the first page — so the joke
is the mechanism itself, and the punchline is the last clause.

Nothing here is random, nothing touches the network, and the same bytes
come out on every run: the line is checked before it is written (one
line, 1-200 characters, valid UTF-8) and the file is read back and
compared afterwards, so a short or corrupted write fails out loud.
"""

import os
import sys

EXCUSE = (
    "I paginated through the task list and the deadline was on page two. "
    "I only ever read page one."
)

MAX_CHARS = 200


def check_line(line):
    if not line:
        raise SystemExit("excuse is empty")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            "excuse is %d chars, over the %d limit" % (len(line), MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("excuse must be a single line")
    blob = line.encode("utf-8")
    if blob.endswith(b"\n"):
        raise SystemExit("excuse must not end with a newline")
    return blob


def main():
    blob = check_line(EXCUSE)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(blob)
    with open(path, "rb") as handle:
        back = handle.read()
    if back != blob:
        raise SystemExit("entry.txt round-trip mismatch")
    sys.stdout.write(
        "wrote entry.txt: %d chars, %d bytes\n" % (len(EXCUSE), len(blob))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
