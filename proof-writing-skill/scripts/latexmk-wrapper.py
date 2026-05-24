#!/usr/bin/env python3
"""latexmk-wrapper.py — compile LaTeX and emit structured JSON of compile state.

Usage:
    python scripts/latexmk-wrapper.py <main.tex> [--outdir .output] [--quiet]
                                      [--overfull-threshold 50.0]

Output: JSON on stdout describing compile result.

Exit codes:
    0 — compile_ok is true (no errors, no overfull boxes > threshold).
    1 — compile_ok is false (errors, undefined macros, or overfull boxes
        exceeding --overfull-threshold).
    2 — input file missing.

Downstream tooling MUST check the exit code. A non-zero exit means a
blocking defect was found. Phase D gate (a) requires exit 0.

Schema:
    {
      "compile_ok": bool,
      "pdf_path": "<path to .pdf, may not exist>",
      "log_path": "<path to .log, may not exist>",
      "undef_refs": ["lem:foo", ...],
      "undef_cites": ["smith2023", ...],
      "mult_labels": ["lem:foo", ...],
      "undef_macros": ["\\foo", ...],
      "overfull_hbox_pts": [12.3, 50.1, ...],
      "overfull_violations": [{"pts": 73.2, "location": "lines 145--147"}, ...],
      "overfull_threshold": 50.0,
      "errors": [{"file": "a.tex", "line": 42, "message": "..."}],
      "warnings_count": 17
    }

`overfull_violations` lists ONLY boxes exceeding --overfull-threshold
(default 50.0pt); these are the boxes that flip `compile_ok` to false.
`overfull_hbox_pts` retains every overfull value (incl. small) for
backward compat.

Dependencies: stdlib only. Requires `latexmk` (preferred) or `pdflatex` on PATH.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any


def run_compile(main_tex: str, outdir: str, quiet: bool) -> None:
    """Run latexmk (preferred) or pdflatex twice. Suppress stdout/stderr."""
    os.makedirs(outdir, exist_ok=True)

    # latexmk and pdflatex run in cwd by default, which means \input{macros}
    # would not find macros.tex sitting next to main.tex. Use `-cd` (latexmk)
    # or chdir manually (pdflatex) so the project root is the source dir.
    src_dir = os.path.dirname(os.path.abspath(main_tex)) or "."
    src_base = os.path.basename(main_tex)
    # If outdir is relative, anchor it to src_dir so -cd doesn't move it
    if not os.path.isabs(outdir):
        outdir_for_cmd = os.path.relpath(
            os.path.abspath(outdir), start=src_dir
        )
    else:
        outdir_for_cmd = outdir

    if shutil.which("latexmk"):
        # Note: do NOT pass `-halt-on-error=false`. Newer latexmk versions
        # (v4.88+ in TeX Live 2026) reject it as unknown. The absence of
        # `-halt-on-error` plus `-interaction=nonstopmode` is the correct
        # way to keep going past errors. `-cd` runs in the source's dir
        # so `\input{macros}` resolves relative to main.tex.
        cmd = [
            "latexmk",
            "-pdf",
            "-cd",
            f"-outdir={outdir_for_cmd}",
            "-interaction=nonstopmode",
            src_base,
        ]
        subprocess.run(cmd, capture_output=True, text=True, cwd=src_dir)
    elif shutil.which("pdflatex"):
        for _ in range(2):
            subprocess.run(
                [
                    "pdflatex",
                    f"-output-directory={outdir_for_cmd}",
                    "-interaction=nonstopmode",
                    src_base,
                ],
                capture_output=True,
                text=True,
                cwd=src_dir,
            )
    else:
        if not quiet:
            sys.stderr.write(
                "warning: neither latexmk nor pdflatex found on PATH\n"
            )


def parse_log(log_path: str) -> dict[str, Any]:
    """Parse a LaTeX .log file into structured findings."""
    if not os.path.exists(log_path):
        return {"log_missing": True}

    with open(log_path, "r", errors="replace") as f:
        log = f.read()

    # Undefined references: lines like
    #   LaTeX Warning: Reference `lem:foo' on page 3 undefined ...
    undef_refs = sorted(
        set(re.findall(r"Reference [`'](.+?)['`] on page", log))
    )

    # Undefined citations
    undef_cites = sorted(
        set(re.findall(r"Citation [`'](.+?)['`] on page", log))
    )

    # Multiply defined labels
    mult_labels = sorted(
        set(re.findall(r"Label [`'](.+?)['`] multiply defined", log))
    )

    # Overfull hbox/vbox warnings:
    #   "Overfull \hbox (12.34pt too wide) in paragraph at lines 145--147"
    #   "Overfull \vbox (15.0pt too high) detected at line 1234"
    overfull: list[float] = []
    overfull_detail: list[dict[str, Any]] = []
    for match in re.finditer(
        r"Overfull \\[hv]box \(([\d.]+)pt[^)]*\)\s*(.*?)(?=\n\n|\Z)",
        log,
        flags=re.DOTALL,
    ):
        pts = float(match.group(1))
        ctx = match.group(2).strip().replace("\n", " ")[:120]
        # Extract "at lines X--Y" or "at line X" if present
        loc_match = re.search(r"at lines? ([\d\-]+)", ctx)
        location = (
            f"lines {loc_match.group(1)}" if loc_match else "unknown"
        )
        overfull.append(pts)
        overfull_detail.append({"pts": pts, "location": location})

    # Undefined control sequence errors
    undef_macros: list[str] = []
    for match in re.finditer(
        r"! Undefined control sequence\..*?(\\[A-Za-z@]+)",
        log,
        flags=re.DOTALL,
    ):
        undef_macros.append(match.group(1))
    undef_macros = sorted(set(undef_macros))

    # Generic errors (lines starting with "!" that aren't "! Undefined control...")
    errors: list[dict[str, Any]] = []
    for match in re.finditer(
        r"^! (.+?)$\s*l\.(\d+)",
        log,
        flags=re.MULTILINE | re.DOTALL,
    ):
        msg = match.group(1).strip().replace("\n", " ")[:200]
        line = int(match.group(2))
        # Don't double-report undefined-control-sequence errors
        if "Undefined control sequence" not in msg:
            errors.append({"line": line, "message": msg})

    warnings_count = len(re.findall(r"LaTeX Warning:", log)) + len(
        re.findall(r"Package .* Warning:", log)
    )

    return {
        "undef_refs": undef_refs,
        "undef_cites": undef_cites,
        "mult_labels": mult_labels,
        "undef_macros": undef_macros,
        "overfull_hbox_pts": overfull,
        "overfull_detail": overfull_detail,
        "errors": errors,
        "warnings_count": warnings_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main_tex", help="Path to main .tex file")
    parser.add_argument(
        "--outdir",
        default=".output",
        help="Output directory for build artifacts (default: .output)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress diagnostic messages on stderr",
    )
    parser.add_argument(
        "--overfull-threshold",
        type=float,
        default=50.0,
        help=(
            "Maximum allowed Overfull \\hbox/vbox size in points. Any box "
            "exceeding this flips compile_ok to false and exits 1 (default: 50.0)"
        ),
    )
    args = parser.parse_args()

    if not os.path.exists(args.main_tex):
        print(
            json.dumps(
                {"error": f"file not found: {args.main_tex}", "compile_ok": False}
            )
        )
        return 2

    main_base = os.path.basename(args.main_tex)
    if main_base.endswith(".tex"):
        main_base = main_base[:-4]
    log_path = os.path.join(args.outdir, main_base + ".log")
    pdf_path = os.path.join(args.outdir, main_base + ".pdf")

    run_compile(args.main_tex, args.outdir, args.quiet)

    log_info = parse_log(log_path)

    # Pull overfull violations exceeding the threshold (these block compile_ok)
    threshold = args.overfull_threshold
    overfull_detail = log_info.pop("overfull_detail", [])
    overfull_violations = [
        d for d in overfull_detail if d["pts"] > threshold
    ]

    compile_ok = (
        os.path.exists(pdf_path)
        and not log_info.get("log_missing", False)
        and not log_info.get("errors")
        and not log_info.get("undef_macros")
        and not overfull_violations
    )

    result: dict[str, Any] = {
        "compile_ok": compile_ok,
        "pdf_path": pdf_path,
        "log_path": log_path,
        "overfull_violations": overfull_violations,
        "overfull_threshold": threshold,
        **log_info,
    }
    print(json.dumps(result, indent=2))

    # Emit verbose stderr diagnostics on failure so Claude can act without
    # parsing the JSON when reading scrollback.
    if not compile_ok and not args.quiet:
        sys.stderr.write("\n=== latexmk-wrapper: compile_ok=false ===\n")
        if log_info.get("log_missing"):
            sys.stderr.write(
                "  log file not produced — toolchain (latexmk/pdflatex) "
                "may not be installed\n"
            )
        for v in overfull_violations:
            sys.stderr.write(
                f"  Overfull box {v['pts']:.1f}pt > {threshold}pt "
                f"at {v['location']} — fix display sizing\n"
            )
        for m in log_info.get("undef_macros", []):
            sys.stderr.write(f"  Undefined control sequence: {m}\n")
        for e in log_info.get("errors", []):
            sys.stderr.write(
                f"  Error at line {e.get('line')}: {e.get('message')}\n"
            )
        sys.stderr.write("===\n")

    return 0 if compile_ok else 1


if __name__ == "__main__":
    sys.exit(main())
