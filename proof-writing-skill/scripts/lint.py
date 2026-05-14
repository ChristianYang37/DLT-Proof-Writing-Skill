#!/usr/bin/env python3
"""lint.py — LaTeX style/correctness linter for DLT-proof projects.

Usage:
    python scripts/lint.py <main.tex> [more.tex ...] [--bib refs.bib]
                           [--format text|json] [--quiet]

Implements the minimum rule set (10 rules):

    Tier 0 (already-in-conventions, must include):
        R0a  — \\[ ... \\] math display banned (use align*/align)
        R0b  — bare \\eqref{} missing 'Eq.~' prefix (allow inside \\tag{})
        R0c  — \\newtheorem{X}[theorem]{...} without \\newaliascnt{X}{theorem}

    Tier A (universal correctness):
        R1   — \\label{} inside a theorem-like env must use the right slug prefix
        R2   — theorem-like envs must have a \\label
        R3   — \\begin{proof} / \\end{proof} count mismatch
        R4   — duplicate \\label{} across files
        R6   — display block (align/align*/equation/multline/gather) last line
               does not end with '.' or ','
        R12  — \\cite{key} where key is not in the .bib

    Tier C (handwave flag, warning-only):
        R16  — "the other case is similar"

Exit code: 0 if no errors, 1 if any errors. Warnings do not change exit code.
Stdlib only; works on Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Violation:
    rule: str
    severity: str  # "error" or "warning"
    file: str
    line: int
    match: str
    message: str


@dataclass
class Env:
    name: str
    start_line: int
    end_line: int


# ---------------------------------------------------------------------------
# Conventions
# ---------------------------------------------------------------------------

# Map env name → expected \label{} slug prefix.
# Order matters for nested envs (innermost wins).
SLUG_MAP = {
    "theorem": "thm:",
    "lemma": "lem:",
    "proposition": "prop:",
    "corollary": "cor:",
    "definition": "def:",
    "assumption": "ass:",
    "fact": "fac:",
    "remark": "rem:",
    "hypothesis": "hyp:",
    "condition": "cond:",
    "claim": "claim:",
    "equation": "eq:",
    "equation*": "eq:",
    "align": "eq:",
    "align*": "eq:",
    "multline": "eq:",
    "gather": "eq:",
}

THEOREM_LIKE_ENVS = {
    "theorem", "lemma", "proposition", "corollary",
    "definition", "assumption", "fact", "claim",
}

DISPLAY_ENVS = {
    "align", "align*", "equation", "equation*",
    "multline", "multline*", "gather", "gather*",
}

CITE_COMMANDS = (
    r"cite|citet|citep|citealt|citealp|citeauthor|citeyear|citetalias|nocite"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def line_of(text: str, offset: int) -> int:
    """1-indexed line number containing the character at byte offset."""
    return text.count("\n", 0, offset) + 1


def strip_line_comment(line: str) -> str:
    """Remove the first unescaped %... to end of line."""
    return re.sub(r"(?<!\\)%.*$", "", line)


def is_in_comment(line: str, col: int) -> bool:
    """Is column `col` past an unescaped %?"""
    for i in range(min(col, len(line))):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            return True
    return False


def find_environments(text: str) -> list[Env]:
    """Find all \\begin{X}...\\end{X} pairs with start/end line numbers.

    Tolerates mild mismatches by popping the innermost matching name.
    """
    envs: list[Env] = []
    stack: list[tuple[str, int]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        # Skip commented-out portions
        clean = strip_line_comment(line)
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", clean):
            kind = m.group(1)
            name = m.group(2)
            if kind == "begin":
                stack.append((name, lineno))
            else:
                # Pop innermost matching
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == name:
                        n, start = stack.pop(i)
                        envs.append(Env(name=n, start_line=start, end_line=lineno))
                        break
    return envs


def innermost_env_containing(envs: list[Env], line: int) -> Optional[Env]:
    """Return the smallest-range env containing the given line (1-indexed)."""
    candidates = [e for e in envs if e.start_line <= line <= e.end_line]
    if not candidates:
        return None
    return min(candidates, key=lambda e: e.end_line - e.start_line)


def parse_bib(bib_path: str) -> set[str]:
    """Extract @type{key, ...} keys from a BibTeX file."""
    with open(bib_path, errors="replace") as f:
        content = f.read()
    keys = set()
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s}]+)", content):
        keys.add(m.group(1).strip())
    return keys


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------


def check_R0a_math_display(text: str, file: str) -> list[Violation]:
    """\\[ ... \\] display math is banned."""
    out: list[Violation] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\\\[", line):
            if is_in_comment(line, m.start()):
                continue
            out.append(Violation(
                rule="R0a", severity="error",
                file=file, line=lineno,
                match=line.strip()[:60],
                message=(
                    "display math uses \\[ ... \\]; use "
                    "\\begin{align*} ... \\end{align*} instead"
                ),
            ))
    return out


def check_R0b_eqref_prefix(text: str, file: str) -> list[Violation]:
    """Bare \\eqref{} without 'Eq.~' prefix (allow inside \\tag{...})."""
    out: list[Violation] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\\eqref\{([^}]+)\}", line):
            col = m.start()
            if is_in_comment(line, col):
                continue
            # Check if inside an open \tag{...} on the same line
            preceding = line[:col]
            last_tag = preceding.rfind("\\tag{")
            inside_tag = False
            if last_tag >= 0:
                # Count braces after \tag{
                depth = 1
                for ch in preceding[last_tag + 5:]:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            break
                if depth > 0:
                    inside_tag = True
            if inside_tag:
                continue
            # Check Eq.~ prefix
            prefix = line[max(0, col - 4): col]
            if prefix == "Eq.~":
                continue
            out.append(Violation(
                rule="R0b", severity="error",
                file=file, line=lineno,
                match=m.group(),
                message="bare \\eqref missing 'Eq.~' prefix",
            ))
    return out


def check_R0c_aliascnt(text: str, file: str) -> list[Violation]:
    """\\newtheorem{X}[Y]{...} where X != Y must have a matching \\newaliascnt{X}{Y}."""
    out: list[Violation] = []
    aliased: list[tuple[str, str, int, str]] = []
    for m in re.finditer(
        r"\\newtheorem\{([^}]+)\}\[([^}]+)\]\{[^}]*\}", text
    ):
        env_name, counter = m.group(1), m.group(2)
        if env_name != counter:
            aliased.append((env_name, counter, line_of(text, m.start()), m.group()))

    aliases: set[tuple[str, str]] = set()
    for m in re.finditer(r"\\newaliascnt\{([^}]+)\}\{([^}]+)\}", text):
        aliases.add((m.group(1), m.group(2)))

    for env_name, counter, lineno, match_str in aliased:
        if (env_name, counter) not in aliases:
            out.append(Violation(
                rule="R0c", severity="error",
                file=file, line=lineno,
                match=match_str,
                message=(
                    f"\\newtheorem{{{env_name}}}[{counter}]{{...}} shares "
                    f"the '{counter}' counter but no "
                    f"\\newaliascnt{{{env_name}}}{{{counter}}} found — "
                    f"\\Cref{{{env_name[:3]}:foo}} will render as "
                    f"'{counter.capitalize()}' in the PDF"
                ),
            ))
    return out


def check_R1_label_prefix(text: str, file: str) -> list[Violation]:
    """\\label{} inside a known env must use the slug prefix per SLUG_MAP."""
    out: list[Violation] = []
    envs = find_environments(text)
    for m in re.finditer(r"\\label\{([^}]+)\}", text):
        label = m.group(1)
        lineno = line_of(text, m.start())
        env = innermost_env_containing(envs, lineno)
        if env is None:
            continue
        if env.name not in SLUG_MAP:
            continue
        expected = SLUG_MAP[env.name]
        if not label.startswith(expected):
            out.append(Violation(
                rule="R1", severity="error",
                file=file, line=lineno,
                match=f"\\label{{{label}}}",
                message=(
                    f"label '{label}' inside {env.name} env should "
                    f"start with '{expected}'"
                ),
            ))
    return out


def check_R2_theorem_no_label(text: str, file: str) -> list[Violation]:
    """Theorem-like envs must contain a \\label."""
    out: list[Violation] = []
    envs = find_environments(text)
    lines = text.splitlines()
    for env in envs:
        if env.name not in THEOREM_LIKE_ENVS:
            continue
        block = "\n".join(lines[env.start_line - 1: env.end_line])
        if not re.search(r"\\label\{", block):
            out.append(Violation(
                rule="R2", severity="error",
                file=file, line=env.start_line,
                match=f"\\begin{{{env.name}}}",
                message=(
                    f"{env.name} environment has no \\label{{}} — "
                    f"cannot \\Cref to it"
                ),
            ))
    return out


def check_R3_proof_balance(text: str, file: str) -> list[Violation]:
    """\\begin{proof} count must equal \\end{proof} count.

    Strips comments line-by-line first so a literal '\\end{proof}' inside
    a `%`-comment is not counted.
    """
    out: list[Violation] = []
    clean = "\n".join(strip_line_comment(line) for line in text.splitlines())
    begins = list(re.finditer(r"\\begin\{proof\*?\}", clean))
    ends = list(re.finditer(r"\\end\{proof\*?\}", clean))
    if len(begins) != len(ends):
        # Find the orphan line in the cleaned text (line numbers match original
        # because strip_line_comment preserves newlines)
        if len(begins) > len(ends):
            orphan = begins[len(ends)] if ends else begins[0]
            kind = "\\begin{proof}"
        else:
            orphan = ends[len(begins)] if begins else ends[0]
            kind = "\\end{proof}"
        out.append(Violation(
            rule="R3", severity="error",
            file=file, line=line_of(clean, orphan.start()),
            match=orphan.group(),
            message=(
                f"unbalanced {kind}: {len(begins)} begins, "
                f"{len(ends)} ends"
            ),
        ))
    return out


def check_R4_duplicate_label(file_contents: dict[str, str]) -> list[Violation]:
    """Same \\label{} slug must not appear in multiple places across files."""
    out: list[Violation] = []
    locations: dict[str, list[tuple[str, int]]] = {}
    for fp, text in file_contents.items():
        for m in re.finditer(r"\\label\{([^}]+)\}", text):
            label = m.group(1)
            lineno = line_of(text, m.start())
            locations.setdefault(label, []).append((fp, lineno))
    for label, locs in locations.items():
        if len(locs) > 1:
            others = ", ".join(f"{f}:{l}" for f, l in locs)
            for fp, lineno in locs:
                out.append(Violation(
                    rule="R4", severity="error",
                    file=fp, line=lineno,
                    match=f"\\label{{{label}}}",
                    message=f"label '{label}' defined {len(locs)} times: {others}",
                ))
    return out


def check_R6_display_no_punct(text: str, file: str) -> list[Violation]:
    """Last content line of a display env must end with '.' or ','."""
    out: list[Violation] = []
    lines = text.splitlines()
    stack: list[tuple[str, int]] = []
    for lineno, line in enumerate(lines, 1):
        clean = strip_line_comment(line)
        for m in re.finditer(
            r"\\(begin|end)\{(align\*?|equation\*?|multline\*?|gather\*?)\}",
            clean,
        ):
            kind, name = m.group(1), m.group(2)
            if kind == "begin":
                stack.append((name, lineno))
            elif stack:
                # Pop innermost matching
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == name:
                        _, start_line = stack.pop(i)
                        # Walk back from lineno-1 to find last content line
                        for j in range(lineno - 2, start_line - 1, -1):
                            if not (0 <= j < len(lines)):
                                break
                            raw = lines[j]
                            content = strip_line_comment(raw).rstrip()
                            if not content.strip():
                                continue
                            # Strip trailing \\, \notag, \nonumber, \label{...}
                            prev = None
                            stripped = content
                            while prev != stripped:
                                prev = stripped
                                stripped = re.sub(
                                    r"(\\\\|\\notag|\\nonumber|"
                                    r"\\label\{[^}]*\}|\s)+$",
                                    "",
                                    stripped,
                                )
                            if stripped and stripped[-1] not in ".,":
                                out.append(Violation(
                                    rule="R6", severity="error",
                                    file=file, line=j + 1,
                                    match=raw.strip()[:80],
                                    message=(
                                        f"display block ({name}) last "
                                        f"line does not end with '.' or ','"
                                    ),
                                ))
                            break
                        break
    return out


def check_R12_cite_key(
    text: str, file: str, bib_keys: set[str]
) -> list[Violation]:
    """Every \\cite{key} must have key present in the .bib."""
    out: list[Violation] = []
    pattern = rf"\\(?:{CITE_COMMANDS})\*?(?:\[[^\]]*\])?\{{([^}}]+)\}}"
    for m in re.finditer(pattern, text):
        keys_str = m.group(1)
        lineno = line_of(text, m.start())
        for key in keys_str.split(","):
            key = key.strip()
            if not key:
                continue
            if key not in bib_keys:
                out.append(Violation(
                    rule="R12", severity="error",
                    file=file, line=lineno,
                    match=f"\\cite{{{key}}}",
                    message=f"cite key '{key}' not found in .bib",
                ))
    return out


def check_R16_other_case_similar(text: str, file: str) -> list[Violation]:
    """'the other case is similar' handwave (warning)."""
    out: list[Violation] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        clean = strip_line_comment(line)
        for m in re.finditer(
            r"(?i)the\s+other\s+case[s]?\s+(?:is|are)\s+similar", clean
        ):
            out.append(Violation(
                rule="R16", severity="warning",
                file=file, line=lineno,
                match=m.group(),
                message=(
                    "\"the other case is similar\" handwave — "
                    "expand the second case or prove symmetry explicitly"
                ),
            ))
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


PER_FILE_RULES = [
    ("R0a", check_R0a_math_display),
    ("R0b", check_R0b_eqref_prefix),
    ("R0c", check_R0c_aliascnt),
    ("R1",  check_R1_label_prefix),
    ("R2",  check_R2_theorem_no_label),
    ("R3",  check_R3_proof_balance),
    ("R6",  check_R6_display_no_punct),
    ("R16", check_R16_other_case_similar),
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("files", nargs="+", help=".tex files to lint")
    parser.add_argument(
        "--bib", help="Path to .bib for R12 cite-key checking (optional)"
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Output format (default: text)"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress excerpt lines and summary")
    args = parser.parse_args()

    bib_keys: set[str] = set()
    if args.bib:
        if os.path.exists(args.bib):
            bib_keys = parse_bib(args.bib)
        else:
            print(f"warning: .bib file not found: {args.bib}", file=sys.stderr)

    file_contents: dict[str, str] = {}
    for fp in args.files:
        if not os.path.exists(fp):
            print(f"error: file not found: {fp}", file=sys.stderr)
            return 2
        with open(fp, errors="replace") as f:
            file_contents[fp] = f.read()

    violations: list[Violation] = []

    # Per-file rules
    rules_run: list[str] = []
    for rule_name, fn in PER_FILE_RULES:
        rules_run.append(rule_name)
        for fp, text in file_contents.items():
            violations.extend(fn(text, fp))

    # Cross-file: R4
    rules_run.append("R4")
    violations.extend(check_R4_duplicate_label(file_contents))

    # R12 (only if --bib given)
    if args.bib:
        rules_run.append("R12")
        for fp, text in file_contents.items():
            violations.extend(check_R12_cite_key(text, fp, bib_keys))

    violations.sort(key=lambda v: (v.file, v.line, v.rule))

    n_errors = sum(1 for v in violations if v.severity == "error")
    n_warnings = sum(1 for v in violations if v.severity == "warning")

    if args.format == "json":
        print(json.dumps({
            "violations": [asdict(v) for v in violations],
            "n_errors": n_errors,
            "n_warnings": n_warnings,
            "rules_run": rules_run,
        }, indent=2))
    else:
        for v in violations:
            print(f"{v.file}:{v.line}: {v.severity}: [{v.rule}] {v.message}")
            if v.match and not args.quiet:
                print(f"    {v.match}")
        if not args.quiet:
            print(
                f"\n{n_errors} error{'s' if n_errors != 1 else ''}, "
                f"{n_warnings} warning{'s' if n_warnings != 1 else ''}.",
                file=sys.stderr,
            )

    return 1 if n_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
