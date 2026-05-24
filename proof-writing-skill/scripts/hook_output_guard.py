#!/usr/bin/env python3
"""hook_output_guard.py — Claude Code PreToolUse hook.

Blocks Write/Edit calls that would put LaTeX compile artifacts
(.pdf, .aux, .log, .bbl, .blg, .fls, .fdb_latexmk, .synctex.gz)
anywhere except under a directory named `.output/`.

Reads the tool input as JSON from stdin (Claude Code hook protocol).
Exit code 0 → allow; exit 2 → block (Claude Code interprets non-zero
PreToolUse exit codes as a block + surfaces stderr to the model).

Wire up via settings.json:

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "python3 ~/.claude/skills/dlt-proof-writing/scripts/hook_output_guard.py"
              }
            ]
          }
        ]
      }
    }

A copy of this snippet lives in `settings.recommended.json` at the
skill root.
"""

from __future__ import annotations

import json
import os
import sys

BLOCKED_EXT = {
    ".pdf",
    ".aux",
    ".log",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
    ".out",
    ".toc",
}


def is_under_output(path: str) -> bool:
    """True if the path has a `.output` directory component anywhere."""
    parts = os.path.normpath(path).split(os.sep)
    return ".output" in parts


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No usable input → don't block (fail-open keeps the hook
        # harmless when invoked manually).
        return 0

    # Claude Code hook payload shape:
    #   {"tool_name": "Write", "tool_input": {"file_path": "/abs/path", ...}}
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path")
    if not file_path:
        return 0

    # Determine extension; .synctex.gz needs special handling
    lower = file_path.lower()
    matched_ext: str | None = None
    for ext in sorted(BLOCKED_EXT, key=len, reverse=True):
        if lower.endswith(ext):
            matched_ext = ext
            break
    if matched_ext is None:
        return 0  # not a compile artifact

    if is_under_output(file_path):
        return 0  # under .output/ — allowed

    sys.stderr.write(
        f"[dlt-proof-writing hook] BLOCKED write of '{file_path}' — "
        f"compile artifacts ({matched_ext}) must live under a "
        f"`.output/` directory.\n"
        f"Fix: run `python <skill>/scripts/latexmk-wrapper.py main.tex "
        f"--outdir <project-root>/.output` instead of writing the PDF "
        f"directly. See SKILL.md §Non-negotiables.\n"
    )
    return 2  # Claude Code blocks the tool call on non-zero PreToolUse


if __name__ == "__main__":
    sys.exit(main())
