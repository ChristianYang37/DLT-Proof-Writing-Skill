#!/usr/bin/env python3
"""
Symbol extraction script for the v3 paper (Round-5 notation).

Parses sections/*.tex and macros.tex to enumerate every distinct
mathematical symbol used in the paper, with its first occurrence
(file:line) and a heuristic category (variable / set / operator /
constant / function).

The output is a markdown-formatted table that can be pasted into
section 01 (Preliminaries) as the symbol table.

Round-5 update: \\Cset replaced by \\Afirst (first-token projection of
\\Aset); standalone V (vocab size) replaced by |\\Vocab|; vocab
iterator v/c replaced by \\nu.

Usage:
    python3 .proof-research/scripts-extract_symbols.py > /tmp/symbols.md
"""
import re
import glob
import sys
from collections import OrderedDict
from pathlib import Path

PROJECT = Path(__file__).parent.parent  # eval_results/08-reasoning-as-optimization/

# Patterns that match common math-symbol forms.
# We use the LaTeX macro name (e.g., \loss) as the canonical key,
# and the first inline-math context as a description.
SYMBOL_PATTERNS = [
    # ----- Custom macros from macros.tex -----
    (r'\\loss\b',     'Constrained-softmax loss L(x;Q) = -log pi(x;Q)'),
    (r'\\cmass\b',    'Correct-mass functional pi(x;Q)'),
    (r'\\qcond\b',    'A_1-conditional posterior q_C'),
    (r'\\Aset\b',     'Answer set A(Q) subset V^n (verifier-accepted sequences)'),
    (r'\\Afirst\b',   'First-token projection A_1(Q) subset V'),
    (r'\\Vocab\b',    'Vocabulary set V (token alphabet)'),
    (r'\\Snowball\b', 'Snowball event S (verifier success in window)'),
    (r'\\Extinction\b','Extinction event X'),
    (r'\\rateinit\b', 'Initial / snowball-region effective rate lambda_0(Q)'),
    (r'\\critrate\b', 'Critical effective-token rate lambda_c'),
    (r'\\Lstar\b',    'Snowball-region cutoff L^*(Q)'),
    (r'\\Ldecode\b',  'Decode-threshold loss L_dec(|V|, |A_1|)'),
    (r'\\Margin\b',   'Logit margin M(x;Q)'),
    (r'\\incoh\b',    'Row-incoherence mu(W_U)'),
    (r'\\Difficulty\b','Problem-difficulty functional D(Q)'),

    # ----- Standard objects (not in macros.tex) -----
    (r'\\Fcal_t\b|\\mathcal\s*F_t\b',        'Filtration F_t at step t'),
    (r'\bx_t\b',                              'Residual-stream state at step t'),
    (r'\bV_t\b|\bV_j\b|\bV_k\b',              'Attention value vector at step t/j/k'),
    (r'\bw_\{T,t\}|\bw_\{T,k\}|\bw_\{j,k\}', 'Softmax attention weight at step t (sum to 1)'),
    (r'\bE_t\b',                              'Effective-token indicator (Bernoulli)'),
    (r'\bW_U\b',                              'Unembedding matrix W_U in R^{|V| x d}'),
    (r'W_U\^\\nu\b',                          'Row nu of W_U: token nu\'s unembedding vector'),
    (r'\bd\b(?![a-zA-Z_])',                   'Residual-stream dimension d in N'),
    (r'\bT_\{\\max\}',                        'Trajectory horizon T_max'),
    (r'\bT_\{\\mathrm\{dec\}\}',              'Decode hitting time T_dec'),
    (r'\bR_U\b',                              'Row-norm upper bound R_U (Ass. 2.3)'),
    (r'\\incoh_0\b|\\mu_0\b',                 'Incoherence parameter mu_0 (Ass. 2.3)'),
    (r'\bM\b(?![a-zA-Z_]|\\)',                'Value-norm upper bound M (Ass. 2.4)'),
    (r'\bc_1\b',                              'Critical-rate prefactor c_1 (Theorem T1)'),
    (r'\bc_2\b',                              'T2 rate prefactor'),
    (r'\\sigma\b',                            'Per-step noise scale sigma'),
    (r'\\kappa\b',                            'Lemma A constant kappa(mu_0) = 1 + mu_0'),
    (r'\\cos\\theta_0|\\cos\s+\\theta_0',     'Alignment cosine cos theta_0'),
    (r'\\delta_\+|\\delta_-',                 'Probability bounds delta_+, delta_-'),
    (r'\|\\Vocab\|',                          'Vocabulary size |V|'),
    (r'\\nu\b',                               'Vocabulary token iterator nu'),
    (r'\\nu\^\\star',                         'Specific correct-first-token nu^star (arg-max-row-norm)'),
    (r'\\Aset\(Q\)',                          'Answer set for question Q (sequences)'),
    (r'\\Afirst\(Q\)',                        'First-token answer set for question Q'),
    (r'\\loss\(x_0;\s*Q\)',                   'Initial loss L(x_0; Q)'),
    (r'\bL_0\b',                              'Generic initial-loss value (conditioning)'),
    (r'\bL_\{\\mathrm\{sm\}\}\b',             'Smoothness constant L_sm of loss'),
    (r'\bn\b(?![a-zA-Z_])',                   'Maximum answer length n'),
    (r'\br_t\b',                              'Radial coordinate r_t = ||x_t||'),
    (r'\bg_t\b',                              'Per-step increment g_t = x_t - x_{t-1}'),
    (r'\bs_j\b',                              'Cumulative softmax denominator s_j'),
    (r'\bm\b(?![a-zA-Z_])',                   'GW offspring mean m = lambda_0 / lambda_c'),
    (r'\bZ_n\b',                              'Galton-Watson generation size'),
    (r'\\mathsf\s*Z',                         'GW total progeny'),
    (r'\bp\b(?![a-zA-Z_])',                   'Softmax probability vector p = softmax(W_U x)'),
    (r'\\tau\b',                              'Average per-step softmax weight tau = 1/T'),
]


def scan_files():
    """Scan section files; return dict[symbol] -> (file, lineno, snippet)."""
    results = OrderedDict()
    tex_files = sorted(glob.glob(str(PROJECT / 'sections' / '*.tex'))) + \
                [str(PROJECT / 'macros.tex')]

    for fp in tex_files:
        rel = Path(fp).name
        with open(fp) as f:
            for lineno, line in enumerate(f, 1):
                for canonical_pat, desc in SYMBOL_PATTERNS:
                    m = re.search(canonical_pat, line)
                    if m and canonical_pat not in results:
                        results[canonical_pat] = (rel, lineno,
                                                   line.strip()[:80],
                                                   desc, m.group(0))
    return results


def main():
    results = scan_files()
    print('# Symbol Extraction Report (Round-5 notation)')
    print()
    print(f'Total distinct symbols matched: {len(results)}')
    print()
    print('| Symbol | First seen | Description |')
    print('|---|---|---|')
    for pat, (fp, ln, snippet, desc, sample) in results.items():
        sample_show = sample.replace('\\', '\\textbackslash{}')
        print(f'| `{sample}` | {fp}:{ln} | {desc} |')


if __name__ == '__main__':
    main()
