#!/usr/bin/env python3
"""lint.py — LaTeX style/correctness linter for DLT-proof projects.

Usage:
    python scripts/lint.py <main.tex> [more.tex ...] [--bib refs.bib]
                           [--project-root PATH]
                           [--format text|json] [--quiet]

Implements the rule set (16 rules):

    Tier 0 (already-in-conventions, must include):
        R0a  — \\[ ... \\] math display banned (use align*/align)
        R0b  — bare \\eqref{} missing 'Eq.~' prefix (allow inside \\tag{})
        R0c  — \\newtheorem{X}[theorem]{...} without \\newaliascnt{X}{theorem}

    Tier A (universal correctness):
        R1   — \\label{} inside a theorem-like env must use the right slug prefix
        R2   — theorem-like envs must have a \\label
        R3   — \\begin{proof} / \\end{proof} count mismatch
        R4   — duplicate \\label{} across files
        R5   — theorem-like env must be paired with \\begin{proof} or
               with a \\cite{} inside the optional [...] bracket
               (no "well-known" handwaves)
        R6   — display block (align/align*/equation/multline/gather) last line
               does not end with '.' or ','
        R12  — \\cite{key} where key is not in the .bib

    Tier B (AI-specific failure-mode defense — added 2026):
        R13  — \\cite{key} without `.proof-research/cite-<key>-*.md` digest
        R14  — non-trivial technique keyword without
               `.proof-research/<technique>.md` digest
        R15  — bare $C$ / $c$ / $C_n$ used without a universal-constant
               declaration somewhere in the project
        R17  — theorem with '1-\\delta' in its statement but no union-bound
               paragraph in the corresponding proof
        R18  — main-entry file (contains \\documentclass) holds a
               theorem-like / proof / abstract environment directly;
               those belong in sections/NN-*.tex via \\input{}

    Tier C (handwave flag, warning-only):
        R16  — "the other case is similar"

R13 / R14 require a project root (auto-detected from input file paths
unless --project-root given). They are skipped (silently) if no
`.proof-research/` directory exists — that's the "no digests at all"
case which would otherwise drown the user in noise during early drafting.

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


def _extract_optional_bracket(
    lines: list[str], env_start_line: int, env_name: str
) -> Optional[str]:
    """Extract the [...] content immediately after \\begin{env_name}.

    Scans up to 10 lines starting from `env_start_line` (1-indexed) and
    returns the content of the first balanced `[...]` after `\\begin{X}`,
    or None if no bracket is present.
    """
    end = min(len(lines), env_start_line - 1 + 10)
    block = "\n".join(lines[env_start_line - 1: end])
    m = re.search(rf"\\begin\{{{re.escape(env_name)}\}}", block)
    if not m:
        return None
    after = block[m.end():].lstrip(" \t")
    if not after.startswith("["):
        return None
    depth = 0
    for i, ch in enumerate(after):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return after[1:i]
    return None  # unbalanced — treat as no bracket


def check_R5_thm_needs_proof_or_cite(text: str, file: str) -> list[Violation]:
    """Every theorem-like env must be followed by \\begin{proof} OR have a
    \\cite{} inside its optional [...] bracket.

    Theorem-like = theorem, lemma, proposition, corollary, claim. The proof
    must be the FIRST environment after \\end{X}; intervening environments
    (e.g. \\begin{remark}) trigger the violation.

    Skipped: if \\end{X} is the last theorem-like environment in the file
    and no \\begin{...} follows it within the file (proof presumed to be in
    a later file that the linter doesn't see).
    """
    out: list[Violation] = []
    theorem_like = {"theorem", "lemma", "proposition", "corollary", "claim"}
    envs = find_environments(text)
    lines = text.splitlines()

    for env in envs:
        if env.name not in theorem_like:
            continue

        # (a) Check optional bracket for \cite — citation discharges the rule.
        bracket = _extract_optional_bracket(lines, env.start_line, env.name)
        if bracket and re.search(r"\\cite[a-z]*\*?(?:\[[^\]]*\])?\{", bracket):
            continue

        # (b) Check what follows \end{X}.
        # Build post-\end{X} text, strip comments line-by-line.
        post_lines = lines[env.end_line:]
        post_clean = "\n".join(strip_line_comment(l) for l in post_lines)

        first_begin = re.search(r"\\begin\{([^}]+)\}", post_clean)
        if first_begin is None:
            # No further environment in this file → proof likely in next file;
            # skip the check rather than false-flag.
            continue

        next_name = first_begin.group(1)
        if next_name in ("proof", "proof*"):
            continue  # proof immediately follows — OK

        # Otherwise: first env after \end{X} is not a proof env, and no
        # \cite in the optional bracket → violation.
        out.append(
            Violation(
                rule="R5", severity="error",
                file=file, line=env.start_line,
                match=f"\\begin{{{env.name}}}",
                message=(
                    f"{env.name} environment is not paired with a proof "
                    f"or a citation: next environment after \\end{{{env.name}}} "
                    f"is \\begin{{{next_name}}} (not \\begin{{proof}}) and "
                    f"no \\cite{{}} in its optional [...] bracket. "
                    "Either prove it locally (\\begin{proof} ... \\end{proof}) "
                    "or cite the source of the result via "
                    f"\\begin{{{env.name}}}[\\cite{{...}}]."
                ),
            )
        )

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
# Project-root + digest helpers (for R13, R14)
# ---------------------------------------------------------------------------


def find_project_root(file_paths: list[str]) -> Optional[str]:
    """Walk up from the first input file's parent looking for a marker.

    Markers (in order): `.proof-research/` directory, `.git/` directory.
    Returns the absolute path of the first matching ancestor, or None.
    """
    if not file_paths:
        return None
    start = os.path.dirname(os.path.abspath(file_paths[0])) or "."
    cur = start
    while True:
        for marker in (".proof-research", ".git"):
            if os.path.isdir(os.path.join(cur, marker)):
                return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def cite_digest_bodies(project_root: str) -> set[str]:
    """Return the set of filename "bodies" — the part between `cite-` and `.md`.

    Cite keys can contain hyphens (e.g. ``du-zhai-2018``), so we can't
    reliably tokenize the filename. Instead we keep the full body and let
    the matching function decide.

    File `cite-smith2023.md` → body `smith2023`.
    File `cite-smith2023-some-slug.md` → body `smith2023-some-slug`.
    """
    bodies: set[str] = set()
    digest_dir = os.path.join(project_root, ".proof-research")
    if not os.path.isdir(digest_dir):
        return bodies
    for fname in os.listdir(digest_dir):
        m = re.match(r"^cite-([^.]+)\.md$", fname)
        if m:
            bodies.add(m.group(1))
    return bodies


def cite_digest_matches(key: str, bodies: set[str]) -> bool:
    """A cite digest file matches `key` if its body equals `key` or starts
    with `key + "-"` (the slug-suffix form from technical-research.md)."""
    for body in bodies:
        if body == key:
            return True
        if body.startswith(key + "-"):
            return True
    return False


# Technique keyword → digest slug. Patterns are case-insensitive regex
# fragments matched against .tex content. The slug is what we expect to
# find as `.proof-research/<slug>.md`. Source: technical-research.md
# §"Examples of non-trivial techniques that benefit from a digest".
TECHNIQUE_KEYWORDS: list[tuple[str, str]] = [
    (r"matrix\s+bernstein", "matrix-bernstein"),
    (r"matrix\s+chernoff", "matrix-chernoff"),
    (r"hanson[\s\-]+wright", "hanson-wright"),
    (r"bernstein.*sub[\s\-]?exponential", "bernstein-sub-exponential"),
    (r"mcdiarmid", "mcdiarmid"),
    (r"azuma[\s\-]+hoeffding|azuma's", "azuma-hoeffding"),
    (r"self[\s\-]+normalized\s+concentration", "self-normalized"),
    (r"dudley'?s?\s+chaining", "dudley-chaining"),
    (r"talagrand'?s?\s+generic\s+chaining", "talagrand-chaining"),
    (r"local\s+rademacher", "local-rademacher"),
    (r"varshamov[\s\-]+gilbert", "varshamov-gilbert"),
    (r"semi[\s\-]?smoothness", "semi-smoothness"),
    (r"gronwall", "gronwall"),
    (r"lyapunov\s+decomposition", "lyapunov"),
    (r"polyak[\s\-]+(?:łojasiewicz|lojasiewicz)|\\mathsf\{PL\}|\bPL\s+inequality\b",
     "polyak-lojasiewicz"),
    (r"elliptical[\s\-]+potential", "elliptical-potential"),
    (r"weyl'?s?\s+perturbation", "weyl-perturbation"),
    (r"davis[\s\-]+kahan", "davis-kahan"),
    (r"sherman[\s\-]+morrison", "sherman-morrison"),
    (r"woodbury", "woodbury"),
    (r"hoffman[\s\-]+wielandt", "hoffman-wielandt"),
    (r"yarotsky", "yarotsky"),
    (r"\\mathsf\{SETH\}|\bSETH\b", "seth"),
    (r"orthogonal\s+vectors?\s+hypothesis|\\mathsf\{OVH\}|\bOVH\b", "ovh"),
    (r"3SUM[\s\-]+hardness|\b3SUM\b", "3sum-hardness"),
    (r"wasserstein\s+contraction", "wasserstein-contraction"),
    (r"talagrand'?s?\s+transportation", "talagrand-transport"),
    (r"sinkhorn", "sinkhorn"),
]


def technique_digest_slugs(project_root: str) -> set[str]:
    """List `.proof-research/<slug>.md` slugs (excluding cite-* digests)."""
    slugs: set[str] = set()
    digest_dir = os.path.join(project_root, ".proof-research")
    if not os.path.isdir(digest_dir):
        return slugs
    for fname in os.listdir(digest_dir):
        if not fname.endswith(".md"):
            continue
        if fname.startswith("cite-"):
            continue
        # Strip .md
        slugs.add(fname[:-3])
    return slugs


# ---------------------------------------------------------------------------
# R13 — \cite{key} must have .proof-research/cite-<key>-*.md
# ---------------------------------------------------------------------------


def check_R13_cite_digest(
    text: str, file: str, digest_bodies: set[str]
) -> list[Violation]:
    """Every \\cite{key} must have a matching digest under .proof-research/.

    A digest matches `key` if its filename body equals `key` or starts
    with `key + "-"`. Caller is responsible for skipping this rule if
    no .proof-research/ directory exists (early-drafting / unit-test mode).
    """
    out: list[Violation] = []
    pattern = rf"\\(?:{CITE_COMMANDS})\*?(?:\[[^\]]*\])?\{{([^}}]+)\}}"
    for m in re.finditer(pattern, text):
        keys_str = m.group(1)
        lineno = line_of(text, m.start())
        for key in keys_str.split(","):
            key = key.strip()
            if not key:
                continue
            if not cite_digest_matches(key, digest_bodies):
                out.append(Violation(
                    rule="R13", severity="error",
                    file=file, line=lineno,
                    match=f"\\cite{{{key}}}",
                    message=(
                        f"cite key '{key}' has no digest under "
                        f".proof-research/cite-{key}-*.md — "
                        f"fabricated-reference risk; run a citation digest "
                        f"per references/technical-research.md or write "
                        f"\\todo{{verify: <attribution>}} instead"
                    ),
                ))
    return out


# ---------------------------------------------------------------------------
# R14 — non-trivial technique must have a digest
# ---------------------------------------------------------------------------


def check_R14_technique_digest(
    text: str, file: str, digest_slugs: set[str]
) -> list[Violation]:
    """Every mention of a non-trivial technique keyword must have a digest.

    Caller is responsible for skipping if no .proof-research/ exists.
    """
    out: list[Violation] = []
    # Strip comments line-by-line so we don't false-flag examples in comments
    clean_lines = [strip_line_comment(line) for line in text.splitlines()]
    reported_pairs: set[tuple[str, int]] = set()  # (slug, line) — dedupe
    for pattern, slug in TECHNIQUE_KEYWORDS:
        rgx = re.compile(pattern, re.IGNORECASE)
        for lineno, line in enumerate(clean_lines, 1):
            m = rgx.search(line)
            if not m:
                continue
            if slug in digest_slugs:
                continue
            if (slug, lineno) in reported_pairs:
                continue
            reported_pairs.add((slug, lineno))
            out.append(Violation(
                rule="R14", severity="error",
                file=file, line=lineno,
                match=m.group()[:60],
                message=(
                    f"technique '{m.group()}' has no digest at "
                    f".proof-research/{slug}.md — AI memory of advanced "
                    f"techniques is unreliable on hypotheses and constants; "
                    f"spawn a research sub-agent per "
                    f"references/technical-research.md"
                ),
            ))
    return out


# ---------------------------------------------------------------------------
# R15 — bare $C$ / $c$ requires a universal-constant declaration somewhere
# ---------------------------------------------------------------------------


UC_DECLARATION_RE = re.compile(
    r"universal\s+(?:positive\s+)?constants?", re.IGNORECASE
)


def has_universal_constant_declaration(file_contents: dict[str, str]) -> bool:
    """True if any input file contains the universal-constant convention text."""
    for text in file_contents.values():
        if UC_DECLARATION_RE.search(text):
            return True
    return False


def check_R15_bare_constants(
    text: str, file: str, has_uc_declaration: bool
) -> list[Violation]:
    """Bare $C$ / $c$ / $C_<digit>$ requires a universal-constant declaration.

    If no declaration is present anywhere in the input file set, any bare
    $C$, $c$, $C_1$, ... triggers R15. The declaration relieves all bare
    usages (the convention permits them). Author can suppress per-line via
    `% lint: ignore R15` on the same line.

    Skips:
      - Lines inside a `\\newcommand` / `\\def` / `\\renewcommand`
        definition (these are macros, not derivation use).
      - Lines containing `% lint: ignore R15`.
      - Math-mode contexts where the C is followed by `_{...}` or `(...)`
        (problem-dependent constants are fine).
    """
    if has_uc_declaration:
        return []

    out: list[Violation] = []
    # Match a $...$ block that STARTS with one of {C, c, C_<digit>, c_<digit>}
    # immediately followed by either end-of-math, whitespace, or a
    # mathematical operator. This catches `$C$`, `$C > 0$`, `$C \le X$`,
    # `$C_1$`, `$c$` — but NOT `$C_{\lambda_0}$` (subscripted with a name)
    # or `$c(\lambda)$` (function-like, problem-dependent), which are the
    # canonical "OK" forms when no UC declaration exists.
    bare_c_pattern = re.compile(
        r"\$\s*([Cc](?:_\d+)?)(?=\s*(?:\$|\s|[><=+\-\\,]))"
    )
    for lineno, line in enumerate(text.splitlines(), 1):
        if "lint: ignore R15" in line:
            continue
        # Skip macro definitions
        if re.search(r"\\(?:re)?newcommand|\\def\b|\\providecommand", line):
            continue
        clean = strip_line_comment(line)
        for m in bare_c_pattern.finditer(clean):
            out.append(Violation(
                rule="R15", severity="error",
                file=file, line=lineno,
                match=m.group()[:60],
                message=(
                    "bare constant used without universal-constant "
                    "declaration — add the convention block "
                    "(\"Throughout, $c, C, C_1, ...$ denote universal "
                    "positive constants ...\") to your preliminaries, "
                    "or annotate the dependency (e.g. $C_{\\lambda_0,L}$). "
                    "Suppress with `% lint: ignore R15` after fixing intent."
                ),
            ))
    return out


# ---------------------------------------------------------------------------
# R17 — theorem with `1-\delta` must have union-bound paragraph in proof
# ---------------------------------------------------------------------------


_HP_DELTA_RE = re.compile(r"1\s*-\s*\\delta\b")
_UNION_BOUND_RE = re.compile(
    r"union[\s\-]+bound|"            # "union bound" / "union-bound"
    r"\\Pr\s*\[\s*\\mathcal\{E\}|"   # \Pr[\mathcal{E}
    r"\\Pr\s*\(\s*\\mathcal\{E\}|"   # \Pr(\mathcal{E}
    r"by\s+a\s+union",               # "by a union ..."
    re.IGNORECASE,
)


def check_R17_union_bound(text: str, file: str) -> list[Violation]:
    """Theorem-like env containing `1-\\delta` must be paired with a proof
    that contains a union-bound paragraph.

    Pairs theorems with proofs the same way R5 does: the FIRST environment
    after \\end{theorem-like} must be \\begin{proof}; we then scan that
    proof's body.
    """
    out: list[Violation] = []
    theorem_like = {"theorem", "lemma", "proposition", "corollary", "claim"}
    envs = find_environments(text)
    lines = text.splitlines()
    # Build a lookup: env_start_line → Env for theorem-like envs
    for env in envs:
        if env.name not in theorem_like:
            continue
        # Get the theorem body
        body = "\n".join(lines[env.start_line - 1: env.end_line])
        if not _HP_DELTA_RE.search(body):
            continue
        # Find the next environment after \end{X}
        post_lines = lines[env.end_line:]
        post_clean = "\n".join(strip_line_comment(l) for l in post_lines)
        first_begin = re.search(r"\\begin\{([^}]+)\}", post_clean)
        if first_begin is None:
            # No proof in this file; assume it lives in another file —
            # don't false-flag (R5 already handles missing-proof cases)
            continue
        next_name = first_begin.group(1)
        if next_name not in ("proof", "proof*"):
            # R5 already errors on this; don't double-report here
            continue
        # Find the proof env span
        proof_env = None
        for e in envs:
            if (
                e.name in ("proof", "proof*")
                and e.start_line > env.end_line
            ):
                if proof_env is None or e.start_line < proof_env.start_line:
                    proof_env = e
        if proof_env is None:
            continue
        proof_body = "\n".join(
            lines[proof_env.start_line - 1: proof_env.end_line]
        )
        if _UNION_BOUND_RE.search(proof_body):
            continue
        out.append(Violation(
            rule="R17", severity="error",
            file=file, line=env.start_line,
            match=f"\\begin{{{env.name}}}",
            message=(
                f"{env.name} statement contains '1-\\delta' but its proof "
                f"(at line {proof_env.start_line}) has no union-bound "
                f"paragraph — high-probability conclusions must explicitly "
                f"account for the failure budget (e.g. \"By a union bound "
                f"over \\Cref{{lem:A,lem:B}}, ...\"). "
                f"Suppress with `% lint: ignore R17` if the bound is "
                f"established elsewhere (cross-file)."
            ),
        ))
    # Honor per-theorem suppression: drop violation if the env body has
    # the ignore comment.
    filtered: list[Violation] = []
    for v in out:
        env = next(
            (e for e in envs if e.start_line == v.line), None
        )
        if env is None:
            filtered.append(v)
            continue
        body = "\n".join(lines[env.start_line - 1: env.end_line])
        if "lint: ignore R17" in body:
            continue
        filtered.append(v)
    return filtered


# ---------------------------------------------------------------------------
# R18 — main-entry file must not directly contain theorem/proof/abstract envs
# ---------------------------------------------------------------------------


# Envs forbidden in the main entry file (the one with \documentclass).
# Per conventions.md §Project file structure: "Proofs are written one section
# per .tex file, \input-ed into main.tex. Never write multiple proofs inline
# in main.tex; never inline a proof inside the file that imports it." Also
# the skill explicitly forbids abstracts (SKILL.md description, conventions.md).
_MAIN_FORBIDDEN_ENVS = {
    "theorem", "lemma", "proposition", "corollary", "claim",
    "definition", "assumption", "fact", "remark", "hypothesis", "condition",
    "proof", "proof*",
    "abstract",
}


def check_R18_main_no_inline_content(text: str, file: str) -> list[Violation]:
    """The main-entry file (containing \\documentclass) must NOT directly
    hold theorem-like / proof / abstract envs. Those belong in
    sections/NN-*.tex and are pulled in via \\input{}.

    Detection: presence of `\\documentclass` identifies the file as a main
    entry. Any forbidden env found at top level of that file is an error.
    """
    if not re.search(r"\\documentclass\b", text):
        return []
    out: list[Violation] = []
    envs = find_environments(text)
    for env in envs:
        if env.name in _MAIN_FORBIDDEN_ENVS:
            out.append(Violation(
                rule="R18", severity="error",
                file=file, line=env.start_line,
                match=f"\\begin{{{env.name}}}",
                message=(
                    f"main-entry file (contains \\documentclass) holds "
                    f"\\begin{{{env.name}}} inline — proofs, statements, "
                    f"and abstracts MUST live in sections/NN-*.tex and be "
                    f"pulled in via \\input{{}}. Move this environment "
                    f"to a section file. See conventions.md §Project "
                    f"file structure and SKILL.md §Non-negotiables."
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
    ("R5",  check_R5_thm_needs_proof_or_cite),
    ("R6",  check_R6_display_no_punct),
    ("R16", check_R16_other_case_similar),
    ("R17", check_R17_union_bound),
    ("R18", check_R18_main_no_inline_content),
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
        "--project-root",
        help=(
            "Path to project root for R13/R14 digest checks. Auto-detected "
            "by walking up from the first input file until `.proof-research/` "
            "or `.git/` is found. Pass explicitly to override."
        ),
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

    # Project-root + digest discovery for R13/R14
    project_root = args.project_root or find_project_root(args.files)
    digest_dir_present = bool(
        project_root and os.path.isdir(os.path.join(project_root, ".proof-research"))
    )
    cite_bodies: set[str] = set()
    technique_slugs: set[str] = set()
    if digest_dir_present and project_root is not None:
        cite_bodies = cite_digest_bodies(project_root)
        technique_slugs = technique_digest_slugs(project_root)

    # Cross-file: does any input file declare the universal-constant convention?
    has_uc = has_universal_constant_declaration(file_contents)

    violations: list[Violation] = []

    # Per-file rules
    rules_run: list[str] = []
    for rule_name, fn in PER_FILE_RULES:
        rules_run.append(rule_name)
        for fp, text in file_contents.items():
            violations.extend(fn(text, fp))

    # R15 — bare constants (per-file, but depends on cross-file declaration scan)
    rules_run.append("R15")
    for fp, text in file_contents.items():
        violations.extend(check_R15_bare_constants(text, fp, has_uc))

    # Cross-file: R4
    rules_run.append("R4")
    violations.extend(check_R4_duplicate_label(file_contents))

    # R12 (only if --bib given)
    if args.bib:
        rules_run.append("R12")
        for fp, text in file_contents.items():
            violations.extend(check_R12_cite_key(text, fp, bib_keys))

    # R13 / R14 — digest existence checks (only if .proof-research/ exists)
    if digest_dir_present:
        rules_run.append("R13")
        for fp, text in file_contents.items():
            violations.extend(check_R13_cite_digest(text, fp, cite_bodies))
        rules_run.append("R14")
        for fp, text in file_contents.items():
            violations.extend(check_R14_technique_digest(text, fp, technique_slugs))
    elif not args.quiet:
        # Drafting mode: no .proof-research/ yet. Surface this once on stderr
        # so the author knows R13/R14 are silently skipped.
        sys.stderr.write(
            "note: no .proof-research/ directory found "
            f"(searched from {project_root or args.files[0]}); "
            "R13/R14 skipped. Create the directory + digests once the proof "
            "matures (see references/technical-research.md).\n"
        )

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
