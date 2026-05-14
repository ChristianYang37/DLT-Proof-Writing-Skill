#!/usr/bin/env python3
"""latexmk-wrapper.py — compile LaTeX and emit structured JSON of compile state.

Usage:
    python scripts/latexmk-wrapper.py <main.tex> [--outdir .output] [--quiet]

Output: JSON on stdout describing compile result. Always exits 0 unless the
input argument is missing or unreadable; downstream tooling reads
`compile_ok` from the JSON, not the process exit code.

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
      "errors": [{"file": "a.tex", "line": 42, "message": "..."}],
      "warnings_count": 17
    }

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

    # Overfull hbox warnings: "Overfull \hbox (12.34pt too wide)"
    overfull = [
        float(m) for m in re.findall(r"Overfull \\hbox \(([\d.]+)pt", log)
    ]

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
    args = parser.parse_args()

    if not os.path.exists(args.main_tex):
        print(
            json.dumps(
                {"error": f"file not found: {args.main_tex}", "compile_ok": False}
            )
        )
        return 1

    main_base = os.path.basename(args.main_tex)
    if main_base.endswith(".tex"):
        main_base = main_base[:-4]
    log_path = os.path.join(args.outdir, main_base + ".log")
    pdf_path = os.path.join(args.outdir, main_base + ".pdf")

    run_compile(args.main_tex, args.outdir, args.quiet)

    log_info = parse_log(log_path)
    compile_ok = (
        os.path.exists(pdf_path)
        and not log_info.get("log_missing", False)
        and not log_info.get("errors")
        and not log_info.get("undef_macros")
    )

    result: dict[str, Any] = {
        "compile_ok": compile_ok,
        "pdf_path": pdf_path,
        "log_path": log_path,
        **log_info,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
