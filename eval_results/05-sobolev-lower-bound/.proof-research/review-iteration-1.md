# Review iteration 1 — Sobolev minimax lower bound

Proof under review: `\Cref{thm:main}` (Sobolev minimax lower bound) and supporting
lemmas, `eval_results/05-sobolev-lower-bound/`.

## Reviewer scores

| Reviewer | Lens | Score | Blocking? |
|---|---|---|---|
| R1 | Correctness: line-by-line rigor | 9 | no |
| R2 | Correctness: assumptions / generality | 7 | no |
| R3 | Correctness: ML-significance | 7 | no |
| R4 | Math taste | 8 | no |
| R5 | Derivation integrity | 9 | no |
| **mean** | | **8.00** | |

**Accept decision:** mean = 8.00 is NOT strictly `> 8`, so the accept gate is
not cleared → **ITERATE**. No unresolved REAL-blocking critical exists.

## Merged + verified weaknesses

### Weakness #1 (severity: major, raised by 5/5)
**Claim:** Headline says "for all $n$ large enough" but the construction only
holds along the subsequence where $m\mid n^{1/d}$; $m:=\lceil B n^{1/(2s+d)}\rceil$
is defined by $n$ yet simultaneously constrained to divide $n^{1/d}$ — circular,
non-emptiness never argued; closure only asserted in a `\todo`.
(`sections/06-main-theorem.tex:38`, headline `:11`.)
**Verdict:** REAL-nonblocking — STATEMENT-CHANGE / already disclosed.
**Rebuttal / fix-plan:** The defect is real but the only honest fix (restrict the
headline to the regular-grid subsequence, or add a nearest-grid interpolation
paragraph) changes the **theorem headline** "for all $n$ large enough". Per
review-loop Component 3 statement-changing escalation, headline changes are NOT
applied automatically. The author already flagged this explicitly as a
user-decision (`\todo` Q3, lines 40–42) — it is disclosed, not hidden, and the
bound is non-vacuous along an infinite subsequence. Surfaced to user; no
auto-fix.

### Weakness #2 (severity: minor, raised by 3/5)
**Claim:** The parenthetical "$M\ge M_0\ge 8$" is literally false: VG only gives
$M\ge 2^{M_0/8}$, which is $< M_0$ for $M_0\in\{8,\dots,63\}$. Non-load-bearing
(only $M\ge 2$ and $\log M\ge\tfrac{m^d}{8}\log2$ are used).
(`sections/06-main-theorem.tex:89`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Correct and cheap. Replaced with the true, sufficient
fact `$M\ge 2^{M_0/8}\ge 2$` (which is exactly what Step 3's Fano application
needs). FIXED.

### Weakness #3 (severity: style, raised by 1/5)
**Claim:** Reference digest `local-fano.md` derives the sufficient condition with
$\alpha\le 1/16$, but the theorem's Step 2 uses $\alpha=1/4$; a cross-checking
reader could be briefly misled. (`sections/06-main-theorem.tex:66`.)
**Verdict:** INTENTIONAL / PHANTOM (re proof source).
**Rebuttal / fix-plan:** The proof's $\alpha=1/4$ path is independently sound
(R1 verified $1-\tfrac14-\tfrac{\log2}{\log M}\ge\tfrac12$ given $\log M\ge4\log2$).
The digest's $1/16$ is one valid slack choice, not a constraint on the proof; the
$.md$ is internal scaffolding, not part of the deliverable. No source defect → no
fix.

### Weakness #4 (severity: minor, raised by 1/5)
**Claim:** `lem:kl` is stated with the exact-count hypothesis "each cell contains
exactly $n/M_0$ design points", but the proof only uses an upper bound; mildly
inconsistent with `rem:setup`'s "comparable number of points would serve equally
well". (`sections/04-kl-bound.tex:8`.)
**Verdict:** REAL-nonblocking — entangled with Weakness #1.
**Rebuttal / fix-plan:** The "exactly $n/M_0$" count is precisely what the
$m\mid n^{1/d}$ hypothesis (the subject of user-decision Q3, Weakness #1)
delivers, so the stated hypothesis is the honest consequence of the current
construction, not an overclaim. `rem:setup` already states a comparable-count
design would serve equally — the generality relaxation belongs to the same Q3
user-decision. Folding it in now would pre-empt that decision; deferred to
Weakness #1's escalation. No standalone fix.

### Weakness #5 (severity: minor/style, raised by 2/5)
**Claim:** Symbol `g` does double duty — generic second regression function in
`fac:gauss-kl` vs the fixed bump profile in `def:bumps` (and in the constant
`c(s,d,g,\sigma^2)`). (`sections/01-preliminaries.tex:48`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Real readability snag (the fixed bump `g` is the
load-bearing object everywhere else). Renamed the generic second argument in
`fac:gauss-kl` from `g` to `h` throughout the Fact and its proof; `g` is now
reserved for the bump. FIXED.

### Weakness #6 (severity: style, raised by 1/5)
**Claim:** Four declared macros never used (`\poly`, `\R`, `\abs`, `\inner`) —
dead notation in the preamble. (`macros.tex:49`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed unused via grep across all `.tex`. Removed the
four declarations. FIXED.

### Weakness #7 (severity: style, raised by 1/5)
**Claim:** `\argmin` is a single-use macro (Step 4 test definition), so the
declaration is marginal economy. (`sections/06-main-theorem.tex:106`.)
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** `\argmin` is a `\DeclareMathOperator*` providing correct
operator spacing and limit placement that raw `\arg\min` would not; a dedicated
declaration for a math operator is standard and not dead notation even at one
use. No fix.

### Weakness #8 (severity: minor, raised by 1/5)
**Claim:** `lem:fano` (eq:fano) folds `$I(V;Y)\le\max_{k\ne k'}\KL$` directly into
the quoted Tsybakov result, whereas Corollary 2.6 supplies the **averaged**
$\tfrac1{M^2}\sum\KL$ bound; the averaged→max convexity step is the author's, not
the citation's. (`sections/05-fano.tex:16`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Accurate attribution matters. Restated the cited
display `eq:fano` with the **averaged** form $\tfrac1{M^2}\sum_{k,k'}\KL$ (exactly
Cor 2.6), and moved the max-KL bound to an explicit "in particular ... by bounding
the average by the maximum" clause attributed to convexity, not to the citation.
`rem:fano` already carried this chain; Step 3's downstream use is unaffected.
FIXED.

## Fixes applied this iteration

- #2 `sections/06-main-theorem.tex:88–89` — `M\ge M_0\ge 8` → `M\ge 2^{M_0/8}\ge 2`.
- #5 `sections/01-preliminaries.tex:47–60` — generic regression fn `g`→`h` in `fac:gauss-kl`.
- #6 `macros.tex` — removed unused `\poly`, `\R`, `\abs`, `\inner`.
- #8 `sections/05-fano.tex:8–19` — cited display now averaged-KL; max-KL as a labeled "in particular" convexity consequence.

## Not fixed (surfaced to user)

- #1 (major, REAL-nonblocking, STATEMENT-CHANGE): subsequence vs "for all $n$"
  headline gap. Requires headline change → user decision (Q3 already flagged).
- #4 (minor): `lem:kl` exact-count — entangled with #1's Q3; deferred.
- #3 (style), #7 (style): INTENTIONAL — rebutted above.

## Post-fix gates

- `lint.py` (incl R19): **0 errors, 0 warnings.**
- `latexmk-wrapper.py`: **compile_ok = true**; no undef refs/cites/macros; no errors.
- `pdf/main.pdf` refreshed from `.output/main.pdf`.
