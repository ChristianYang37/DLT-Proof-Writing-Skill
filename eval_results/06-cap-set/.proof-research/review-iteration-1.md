# Review loop — iteration 1

Proof under review: Ellenberg–Gijswijt cap-set bound,
`/Users/christian/DLT-Proof-Writing-Skill/eval_results/06-cap-set`
(`\Cref{thm:cap-set}`: every cap set $A\subseteq\F_3^n$ has $|A|\le 3M_n$;
`\Cref{cor:numerical}`: $|A|\le C(2.7558)^n$, $\limsup|A|^{1/n}\le 3\gamma<2.7558$).

## Reviewer scores

| Reviewer | Lens | Score | Blocking? |
|---|---|---|---|
| R1 | Correctness: line-by-line rigor | 8 | no |
| R2 | Correctness: assumptions / generality / tightness | 9 | no |
| R3 | Correctness: ML-significance | 9 | no |
| R4 | Math taste | 9 | no |
| R5 | Derivation integrity | 9 | no |
| **mean** | | **8.80** | |

## Accept decision

**ACCEPT.** Mean = 8.80 > 8 (strict) AND no unresolved REAL-blocking critical
weakness (the only REAL weaknesses are minor/style and non-load-bearing). Per
`review-loop.md` Component 4 gate 1, the proof is accepted as-is. **No edits
applied to the proof** (record-only).

## Merged + verified weaknesses

Eight distinct weaknesses after merge/dedupe (12 raw weaknesses across 5 reviews).

### Weakness #1 (severity: minor, raised by 1/5)
**Claim:** The parenthetical equivalence "$\gamma<0.9183$" is numerically false:
$\gamma\approx0.918368>0.9183$. (`sections/05-monomial-count.tex:68`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed by direct computation: $t_\ast=0.59307$,
$3\gamma=2.7551046$, so $\gamma=0.9183682>0.9183$. The parenthetical rounds the
wrong way. **Load-bearing bound $3\gamma<2.7558$ is correct (2.75510 < 2.7558)**;
the false clause is a non-load-bearing aside. Fix (deferred — accepted as-is):
delete the parenthetical or replace with the true "$\gamma<0.91837$". Same
phrasing recurs in `01-preliminaries`-era prose / runner-log; cosmetic only.

### Weakness #2 (severity: minor, raised by 1/5)
**Claim:** The pivot-column existence argument (a dimension-$w$ subspace contains
a vector of support $\ge w$) leans on "the sum of the basis rows is nonzero in
each pivot column", left implicit for the reader to reconstruct.
(`sections/02-slice-rank.tex:62`)
**Verdict:** PHANTOM.
**Rebuttal / fix-plan:** The argument is stated in-text (lines 62–65): in RREF the
$w$ pivot columns are distinct coordinates and each pivot row is the unique basis
row nonzero in its pivot column, so the sum of basis rows is nonzero in every
pivot column → support $\ge w$. This is a complete, field-agnostic one-liner, not
a gap; R5 independently rates the same passage "fully shown and correct over an
arbitrary field." No fix.

### Weakness #3 (severity: minor, raised by 3/5)
**Claim:** Uniqueness / interiority / attainment of the interior minimizer $t_\ast$
is asserted in prose, not proved. (`sections/05-monomial-count.tex:58`; merges R2,
R5 ×2.)
**Verdict:** INTENTIONAL (non-load-bearing).
**Rebuttal / fix-plan:** All three flagging reviewers explicitly note this is
non-load-bearing: Eq.~\eqref{eq:Mn-bound} holds for *every* $t\in(0,1]$, so any
single feasible $t$ already yields the bound; uniqueness of $t_\ast$ is exposition,
not a link in the inequality chain. Deliberate brevity, consistent with the
cited-optimum design (`\Cref{rem:cite-opt}`). No fix.

### Weakness #4 (severity: style, raised by 1/5)
**Claim:** Eq.~\eqref{eq:gamma-def} writes $\min_{0<t\le1}$ over a half-open
interval without arguing attainment vs. infimum. (`sections/05-monomial-count.tex:15`)
**Verdict:** INTENTIONAL (folds into #3).
**Rebuttal / fix-plan:** Harmless because the optimizer is interior
($t_\ast\approx0.593\in(0,1)$), so $\min$ is attained; the half-open domain is the
natural Chernoff-shift range $t\in(0,1]$. Non-load-bearing as in #3. No fix.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** The corollary's uniform-in-$n$ bound $|A|\le C(2.7558)^n$ "for all $n$"
is justified from a $\limsup$ with the small-$n$ cases glossed rather than the
finite exceptional set named. (`sections/06-main-theorem.tex:48`)
**Verdict:** INTENTIONAL (REAL-nonblocking, non-load-bearing).
**Rebuttal / fix-plan:** The proof explicitly states the standard absorb-into-$C$
mechanism (lines 48–51): finitely many $n$ with $|A|^{1/n}\ge2.7558$ are absorbed
into $C$, large $n$ immediate. R3 independently verified the exceptional set is
genuine and finite ($n\in\{1,2,3,6,9\}$). Naming that set is cosmetic; the
existence claim "$\exists C\,\forall n$" is correct. No fix.

### Weakness #6 (severity: minor, raised by 2/5)
**Claim:** The final decimal $3\gamma<2.7558$ is attributed to
`\cite{ellenberggijswijt2017}` rather than computed in-text, delegating a
load-bearing inequality to an external source. (`sections/05-monomial-count.tex:67`;
merges R3, R5.)
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Deliberate design, governed by `\Cref{rem:cite-opt}`: the
*reduction* to the one-variable minimization is proved in full in-text; only the
floating-point evaluation of the minimizer is cited. Both flaggers re-derived the
value independently (this trace confirms $3\gamma=2.75510<2.7558$ via direct
computation), so the inequality is verified even though the text cites it. The FOC
is also given symbolically in-text (lines 60–65). Reference-honesty-compliant. No fix.

### Weakness #7 (severity: style, raised by 1/5)
**Claim:** Seven macros declared in `macros.tex` are never used, plus one used
once. (`macros.tex:61–74`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed by grep over `sections/`: `\N, \Z, \norm,
\inner, \abs, \argmin` = 0 uses; `\rank` = 1 use. (`\R` = 2 uses, `\set` = 4,
`\deeg` = 11 — those are *not* dead, contra a loose reading.) Pure housekeeping in
a header file; does not touch the proof body, compilation, or any claim. Fix
(deferred — accepted as-is): delete the six unused notation macros + `\argmin`.
Style-tier, no correctness impact.

### Weakness #8 (severity: minor, raised by 1/5)
**Claim:** The boilerplate "$c,C,C_1,\dots$ universal constants" declaration is
vacuous for bare $c$ (never used that way) and mildly collides with the
parameter-dependent $c_a$ (diagonal coefficients) and slice index $c_i$.
(`sections/01-preliminaries.tex:10`; `sections/02-slice-rank.tex:57`; merges the
two R4 sub-flags.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** True but innocuous: subscripts ($c_a$, $c_i$) fully
disambiguate from the bare universal $c$, and the only genuinely consumed
universal constant is $C$ (in `\Cref{cor:numerical}`). No actual ambiguity in any
load-bearing step; R4 itself rates the proof "consistent and unambiguous
throughout" and scores 9. Style/minor housekeeping; non-blocking.

## Verdict counts

- REAL-blocking: 0
- REAL-nonblocking: 3 (#1, #7, #8)
- PHANTOM: 1 (#2)
- INTENTIONAL: 4 (#3, #4, #5, #6)
- **Unresolved critical: 0**

All REAL weaknesses are minor/style and non-load-bearing; under the accept gate
they do not block. Fixes are recorded for traceability but **not applied** (proof
accepted as-is per gate 1).
