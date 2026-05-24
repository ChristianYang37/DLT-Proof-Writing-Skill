#!/usr/bin/env python3
"""check_scope.py — validate declared scope matches project characteristics.

Usage:
    python scripts/check_scope.py <project-root>

Exit codes:
    0 — `.proof-research/scope.md` exists and the declared scope (Quick /
        Standard / Appendix) is consistent with the project's actual size.
    1 — scope not declared OR declared scope mismatches project features
        (stderr describes the suggested scope).
    2 — input error.

Scope boundaries (codified from SKILL.md §Scope declaration):

  Quick     — single lemma, ≤ 5 derivation steps, no probability
              parameter δ in any theorem statement.
  Standard  — 1–3 lemmas + ≤ 1 theorem; OR a single theorem-like result
              with probabilistic component; 5 < estimated steps ≤ 30.
  Appendix  — ≥ 3 lemmas; OR a paper-level proof with theorem +
              multiple lemmas; OR estimated steps > 30.

This validator is intentionally strict on "Quick" — labeling something
Quick is the most-abused escape hatch (skips Phase C.5 and Phase D).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

VALID_SCOPES = ("Quick", "Standard", "Appendix")


def read_scope(project_root: str) -> tuple[str | None, str | None]:
    """Return (declared_scope, error_message)."""
    path = os.path.join(project_root, ".proof-research", "scope.md")
    if not os.path.exists(path):
        return None, (
            f"scope.md not found at {path} — declare scope at Phase A.0a"
        )
    with open(path, "r", errors="replace") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # Strip Markdown formatting (e.g. bold markers)
            stripped = re.sub(r"^\*+|\*+$", "", stripped).strip()
            for s in VALID_SCOPES:
                if stripped.lower() == s.lower():
                    return s, None
            return None, (
                f"first non-blank line of scope.md is '{stripped}'; "
                f"must be one of {VALID_SCOPES}"
            )
    return None, "scope.md has no non-blank lines"


# ---------------------------------------------------------------------------
# Project feature extraction
# ---------------------------------------------------------------------------


THEOREM_LIKE_BEGIN_RE = re.compile(
    r"\\begin\{(theorem|lemma|proposition|corollary|claim)\}"
)
DELTA_RE = re.compile(r"\\delta\b")


def project_features(project_root: str) -> dict:
    """Compute n_theorems, has_delta, estimated_steps over the project."""
    n_theorems = 0
    has_delta = False
    estimated_steps = 0
    for dirpath, _, fnames in os.walk(project_root):
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
            n_theorems += len(THEOREM_LIKE_BEGIN_RE.findall(text))
            if DELTA_RE.search(text):
                has_delta = True
            # Estimate steps: align-row count + equation envs across all
            # proofs in the file. Same heuristic as check_confidence_tags.py.
            for env_match in re.finditer(
                r"\\begin\{(align\*?|multline\*?|gather\*?)\}(.*?)"
                r"\\end\{\1\}",
                text,
                flags=re.DOTALL,
            ):
                body = env_match.group(2)
                estimated_steps += body.count("\\\\") + 1
            estimated_steps += len(
                re.findall(r"\\begin\{equation\*?\}", text)
            )
    return {
        "n_theorems": n_theorems,
        "has_delta": has_delta,
        "estimated_steps": estimated_steps,
    }


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(features: dict) -> str:
    """Return the suggested scope given features."""
    n = features["n_theorems"]
    has_d = features["has_delta"]
    steps = features["estimated_steps"]

    if n >= 3 or steps > 30:
        return "Appendix"
    if n >= 2 or has_d or steps > 5:
        return "Standard"
    return "Quick"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Path to project root")
    args = parser.parse_args()

    root = os.path.abspath(args.project_root)
    if not os.path.isdir(root):
        sys.stderr.write(f"error: not a directory: {root}\n")
        return 2

    declared, err = read_scope(root)
    if declared is None:
        sys.stderr.write(f"FAIL: {err}\n")
        sys.stderr.write(
            "\nFix: create .proof-research/scope.md with a single line\n"
            "containing Quick / Standard / Appendix. See SKILL.md §Phase A.0a.\n"
        )
        return 1

    features = project_features(root)
    suggested = classify(features)

    print(f"declared:        {declared}")
    print(f"suggested:       {suggested}")
    print(f"n_theorems:      {features['n_theorems']}")
    print(f"has_delta:       {features['has_delta']}")
    print(f"estimated_steps: {features['estimated_steps']}")

    if declared == suggested:
        return 0

    # Strictness asymmetry: declaring DOWN (Quick when project is Standard /
    # Appendix) is the abuse vector — always block. Declaring UP (Appendix
    # when project is Quick) is conservative — allow with note.
    rank = {"Quick": 0, "Standard": 1, "Appendix": 2}
    if rank[declared] < rank[suggested]:
        sys.stderr.write(
            f"\nFAIL: declared scope '{declared}' is below characteristics "
            f"(suggest '{suggested}'). Declaring Quick when the project is "
            f"Standard/Appendix is the most common abuse — it lets agents "
            f"skip Phase C.5 (confidence sweep) and Phase D (review loop).\n"
            f"Fix: update .proof-research/scope.md to '{suggested}' OR\n"
            f"justify the lower scope to the user before proceeding.\n"
        )
        return 1

    sys.stderr.write(
        f"\nnote: declared '{declared}' is more conservative than "
        f"suggested '{suggested}' — allowed.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
