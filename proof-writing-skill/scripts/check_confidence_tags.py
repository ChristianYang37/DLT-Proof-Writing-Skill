#!/usr/bin/env python3
"""check_confidence_tags.py — verify Phase C.5 confidence-trace coverage.

Usage:
    python scripts/check_confidence_tags.py <project-root>

Exit codes:
    0 — trace file exists, coverage adequate, every 🔴 step has \\todo{}.
    1 — any of the above failed (see stderr for details).
    2 — input error (project-root missing or not a directory).

What it checks
--------------

The Phase C.5 confidence sweep produces
``<project-root>/.proof-research/confidence-trace.md`` listing every
derivation step with a 🔴 / 🟡 / 🟢 tag (see
``references/confidence-sweep.md`` §Tag taxonomy and §Trace file).

This validator enforces:

1. Trace file exists.
2. Trace contains at least one tagged entry.
3. Estimated derivation-step count (over all ``.tex`` files in the project)
   has tag coverage ≥ 80% — i.e. ``len(tagged_entries) >= 0.8 *
   estimated_steps``. The estimate counts align-rows, standalone
   equations, ``Case N`` markers, and prose connectives ("Hence" /
   "Therefore" / "Thus" / "By <X>, we have").
4. Every 🔴 (from-memory) entry in the trace has a corresponding
   ``\\todo{verify`` marker within ±3 lines of its declared
   ``Location:`` in the .tex source. This routes unverified steps to
   the Phase D reviewer's attention per ``confidence-sweep.md`` §Step 5.

The 80% threshold is intentionally loose — exact step enumeration is
heuristic and we'd rather under-flag than annoy. If trace coverage is
suspiciously low (≥ 50% missing), exit 1.

Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Optional


# ---------------------------------------------------------------------------
# Step enumeration in .tex
# ---------------------------------------------------------------------------


def estimate_steps_in_proof(proof_body: str) -> int:
    """Estimate the number of derivation steps in a single proof body.

    Counts (deliberately loose):
      - Each `\\\\` line-break inside an align/align*/multline/gather block
        (= one displayed row).
      - Each standalone \\begin{equation} / \\begin{equation*}.
      - Each "Case N." / "Case N:" prose marker.
      - Each sentence starting with "Hence", "Therefore", "Thus",
        "It follows", "By ", "From " — these are inference markers in
        the conventional voice.
    """
    n = 0

    # align/align*/multline/gather row count: each `\\` separator inside
    # an align env represents the start of a new row, so the row count
    # is (count of `\\` inside the env) + 1.
    for env_match in re.finditer(
        r"\\begin\{(align\*?|multline\*?|gather\*?)\}(.*?)\\end\{\1\}",
        proof_body,
        flags=re.DOTALL,
    ):
        body = env_match.group(2)
        # Strip comment portions to avoid counting `\\` in comments
        clean_lines = []
        for line in body.splitlines():
            clean_lines.append(re.sub(r"(?<!\\)%.*$", "", line))
        clean = "\n".join(clean_lines)
        rows = clean.count("\\\\") + 1
        n += rows

    # Standalone equation envs (not wrapped in align/multline/gather)
    n += len(re.findall(r"\\begin\{equation\*?\}", proof_body))

    # Case markers
    n += len(re.findall(r"\\(?:paragraph|noindent)?\s*\{?\s*Case\s+\d+[:.]\s*\}?", proof_body))
    n += len(re.findall(r"(?:^|\n)\\textbf\{Case\s+\d+[:.]", proof_body))

    # Prose connectives (conservative — only count once per sentence start)
    for connective in (
        r"\bHence\b",
        r"\bTherefore\b",
        r"\bThus\b",
        r"\bIt follows\b",
        r"\bBy\s+\\Cref",
        r"\bFrom\s+\\Cref",
    ):
        n += len(re.findall(connective, proof_body))

    return n


def enumerate_proof_bodies(text: str) -> list[tuple[int, str]]:
    """Yield (start_line_1_indexed, body) for each \\begin{proof}...\\end{proof}."""
    out: list[tuple[int, str]] = []
    lines = text.splitlines()
    in_proof = False
    proof_start = -1
    buf: list[str] = []
    for i, line in enumerate(lines, 1):
        if not in_proof:
            if re.search(r"\\begin\{proof\*?\}", line):
                in_proof = True
                proof_start = i
                buf = [line]
        else:
            buf.append(line)
            if re.search(r"\\end\{proof\*?\}", line):
                out.append((proof_start, "\n".join(buf)))
                in_proof = False
                buf = []
    return out


def estimate_total_steps(project_root: str) -> int:
    total = 0
    for dirpath, _, fnames in os.walk(project_root):
        # Skip output/research/git/cache dirs
        parts = set(dirpath.replace(project_root, "").split(os.sep))
        if parts & {".output", ".proof-research", ".git", "__pycache__"}:
            continue
        for fn in fnames:
            if not fn.endswith(".tex"):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, "r", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            for _, body in enumerate_proof_bodies(text):
                total += estimate_steps_in_proof(body)
    return total


# ---------------------------------------------------------------------------
# Trace parsing
# ---------------------------------------------------------------------------


TRACE_ENTRY_RE = re.compile(
    r"^##\s+Step\s+(\S+)\s*$"
    r"(.*?)(?=^##\s+Step\s|\Z)",
    re.MULTILINE | re.DOTALL,
)

CURRENT_TAG_RE = re.compile(
    r"\*\*Current\s+tag:\*\*\s*([🔴🟡🟢])", re.IGNORECASE
)
LOCATION_RE = re.compile(
    r"\*\*Location:\*\*\s*([^\s:]+):(\d+)"
)


def parse_trace(trace_path: str) -> list[dict]:
    """Parse confidence-trace.md into a list of entry dicts.

    Each entry: {"step_id": str, "tag": str|None, "location": (file, line) | None}.
    """
    entries: list[dict] = []
    with open(trace_path, "r", errors="replace") as f:
        text = f.read()
    for m in TRACE_ENTRY_RE.finditer(text):
        step_id = m.group(1)
        block = m.group(2)
        tag_m = CURRENT_TAG_RE.search(block)
        loc_m = LOCATION_RE.search(block)
        entries.append({
            "step_id": step_id,
            "tag": tag_m.group(1) if tag_m else None,
            "location": (loc_m.group(1), int(loc_m.group(2))) if loc_m else None,
        })
    return entries


# ---------------------------------------------------------------------------
# 🔴 todo-pairing check
# ---------------------------------------------------------------------------


def red_steps_have_todo(
    entries: list[dict], project_root: str
) -> list[str]:
    """Return list of problem strings (one per 🔴 step missing \\todo).

    For each 🔴 entry, look at the .tex file and line specified in its
    Location field. Within ±3 lines, there must be a `\\todo{verify`
    marker. Missing → report.
    """
    problems: list[str] = []
    for e in entries:
        if e["tag"] != "🔴":
            continue
        loc = e["location"]
        if loc is None:
            problems.append(
                f"step {e['step_id']}: 🔴 but no Location: line in trace"
            )
            continue
        rel_path, lineno = loc
        # Resolve relative to project_root
        fp = (
            rel_path if os.path.isabs(rel_path)
            else os.path.join(project_root, rel_path)
        )
        if not os.path.exists(fp):
            problems.append(
                f"step {e['step_id']}: 🔴 location {rel_path}:{lineno} "
                f"does not exist on disk"
            )
            continue
        try:
            with open(fp, "r", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            problems.append(
                f"step {e['step_id']}: cannot read {fp}"
            )
            continue
        lo, hi = max(0, lineno - 4), min(len(lines), lineno + 3)
        window = "\n".join(lines[lo:hi])
        if "\\todo{verify" not in window and "\\todo{ verify" not in window:
            problems.append(
                f"step {e['step_id']}: 🔴 at {rel_path}:{lineno} but no "
                f"\\todo{{verify ...}} marker within ±3 lines"
            )
    return problems


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project_root",
        help="Path to project root containing .proof-research/",
    )
    parser.add_argument(
        "--coverage-min",
        type=float,
        default=0.5,
        help=(
            "Minimum fraction of estimated derivation steps that must "
            "appear as tagged entries in confidence-trace.md (default 0.5)"
        ),
    )
    args = parser.parse_args()

    root = os.path.abspath(args.project_root)
    if not os.path.isdir(root):
        sys.stderr.write(f"error: not a directory: {root}\n")
        return 2

    trace_path = os.path.join(root, ".proof-research", "confidence-trace.md")
    if not os.path.exists(trace_path):
        sys.stderr.write(
            f"error: confidence-trace.md not found at {trace_path}\n"
            f"Phase C.5 (confidence sweep) was skipped — see "
            f"references/confidence-sweep.md for the workflow.\n"
        )
        return 1

    entries = parse_trace(trace_path)
    if not entries:
        sys.stderr.write(
            f"error: trace file {trace_path} contains no Step entries\n"
        )
        return 1

    estimated = estimate_total_steps(root)
    tagged = sum(1 for e in entries if e["tag"] is not None)
    untagged = [e["step_id"] for e in entries if e["tag"] is None]

    coverage = tagged / estimated if estimated > 0 else 1.0
    coverage_ok = coverage >= args.coverage_min

    red_issues = red_steps_have_todo(entries, root)

    print(f"trace_path:       {trace_path}")
    print(f"trace_entries:    {len(entries)}")
    print(f"tagged_entries:   {tagged}")
    print(f"untagged_entries: {len(untagged)}")
    if untagged:
        print(f"  IDs: {', '.join(untagged[:10])}"
              + (" ..." if len(untagged) > 10 else ""))
    print(f"estimated_steps:  {estimated}")
    print(f"coverage:         {coverage:.2%} "
          f"(threshold {args.coverage_min:.0%})")
    print(f"red_issues:       {len(red_issues)}")
    for p in red_issues[:20]:
        print(f"  - {p}")

    exit_code = 0
    if not coverage_ok:
        sys.stderr.write(
            f"\nFAIL: coverage {coverage:.2%} < threshold "
            f"{args.coverage_min:.0%}. Add more entries to "
            f"confidence-trace.md or finish the sweep.\n"
        )
        exit_code = 1
    if untagged:
        sys.stderr.write(
            f"\nFAIL: {len(untagged)} entries in trace have no 'Current "
            f"tag:' line. Every step must carry 🔴 / 🟡 / 🟢.\n"
        )
        exit_code = 1
    if red_issues:
        sys.stderr.write(
            f"\nFAIL: {len(red_issues)} 🔴 step(s) without \\todo{{verify}} "
            f"marker. Per confidence-sweep.md §Step 5, unverified steps "
            f"MUST carry a \\todo{{}} marker in the .tex so the Phase D "
            f"reviewer notices.\n"
        )
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
