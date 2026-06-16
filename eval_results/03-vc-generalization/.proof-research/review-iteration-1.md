# Review loop — iteration 1 (VC generalization bound)

Proof under review: `eval_results/03-vc-generalization` — Theorem `thm:vc-bound`
(uniform distribution-free VC generalization bound) via McDiarmid →
symmetrization → Sauer–Shelah → Massart → Cauchy–Schwarz assembly.

## Reviewer scores

| Reviewer | Lens | Score | Blocking? |
|---|---|---|---|
| R1 | correctness: line-by-line | 5 | no |
| R2 | correctness: assumptions/generality | 8 | no |
| R3 | correctness: ML-significance | 9 | no |
| R4 | math taste | 8 | no |
| R5 | derivation integrity | 7 | no |
| **mean** | | **7.40** | |

Accept gate (`mean > 8` AND no unresolved REAL-blocking critical): mean 7.40 ≤ 8
→ **ITERATE**.

## Merged + verified weaknesses

### Weakness #1 (severity: major, raised by 4/5)
**Claim:** Symmetrization step (d) (`03-symmetrization.tex:39-40`) produces the
absolute-value Rademacher average `2 E_σ sup_ℓ |1/n Σ σ_i ℓ(z_i)|` and equates it
to `2 Rad_n(L)`, but Definition 1.3 (`def:rademacher`) defines `Rad` WITHOUT an
absolute value, and Massart's core (`04:90`) bounds only the signed max. Since
`E sup|X| ≥ E sup X`, the no-abs definition does not upper-bound the abs object;
the equality as written is unlicensed (R1/R5 major; R2/R3 minor).
**Verdict:** REAL-blocking.
**Fix-plan / fix applied:** Routed the absolute value through the symmetrized
class `L̄ := L ∪ (−L)` via the exact identity `sup_{ℓ∈L}|X_ℓ| = sup_{ℓ∈L̄} X_ℓ`
(`|t| = max(t,−t)`). Lemma 3 now concludes `≤ 2 Rad_n(L̄)`; the abs is removed
legitimately into the signless definition. Headline ("universal constant `C>0`")
unchanged. New macro `\Lbar` added.

### Weakness #2 (severity: major, raised by 2/5)
**Claim:** Massart (`04:90-96`) bounds the no-abs `Rad_n(L)`; plugging in the
abs object needs a doubling argument `|A| → |A ∪ (−A)|` (cost `log 2`) never
shown (R1 major / R5 minor). Same defect as #1, viewed from the Massart side.
**Verdict:** REAL-blocking (jointly with #1).
**Fix applied:** Massart Lemma 7 now bounds `Rad_n(L̄)` over the projection
`Ā = A ∪ (−A)` with `|Ā| ≤ 2|A| ≤ 2 Π_H(n)`, giving
`√(2(d log(en/d)+log 2)/n)`. The `log 2` is absorbed into the universal constant
downstream (`C` changed from `3` to `√17` inside the proof; the theorem headline
fixes no numeric value).

### Weakness #3 (severity: minor, raised by 1/5)
**Claim:** Symmetrization step (b) (`03:46`) attributes the sup/expectation swap
to "Jensen (convexity of the supremum)", but `sup E ≤ E sup` is monotonicity,
not Jensen; the `|·|` half is genuinely Jensen.
**Verdict:** REAL-nonblocking (both inequalities valid; naming imprecise).
**Fix applied:** Split the justification — `|·|` via Jensen (convexity of `|·|`),
the sup via the monotonicity relation `sup E ≤ E sup`.

### Weakness #4 (severity: minor, raised by 1/5)
**Claim:** McDiarmid (`02:14`) needs `Φ(S) = sup_{h∈H} |...|` measurable, but `H`
is an arbitrary (possibly uncountable) subset of `{0,1}^X` with no measurability
hypothesis stated.
**Verdict:** REAL-nonblocking (genuine omitted technical hypothesis).
**Fix applied:** Added a standing image-admissible-Suslin / pointwise-separable
measurability convention to the Preliminaries notation paragraph.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** Main-theorem step (d) (`05:53`) writes `√(log(1/δ)/(2n))` as
`√(log(1/δ))/√n`, dropping `1/√2`, and is "presented as equality" — an
undisplayed `√2` inflation.
**Verdict:** PHANTOM / INTENTIONAL.
**Rebuttal:** Line 53 is already marked `\overset{(d)}{\le}`, not `=`; the
dropped `1/√2` is a direction-preserving conservative bound, and `C` is
explicitly non-optimized (Remark `rem:rate`). No fix. (The `(d)` step was
rewritten anyway as part of #1/#2, and remains a documented inequality.)

### Weakness #6 (severity: minor, raised by 1/5)
**Claim:** Remark 1 (`01:74`) justifies excluding `n<d` by asserting the RHS of
`thm:vc-bound` "exceeds 1", which is not literally true at the boundary / for `δ`
near 1.
**Verdict:** REAL-nonblocking (conclusion fine, stated reason imprecise).
**Fix applied:** Rewrote the remark to invoke the deterministic trivial bound
`sup|R−R̂| ≤ 1` (always valid since risks lie in `[0,1]`) directly in the `n<d`
regime, making no claim about the theorem's RHS there.

### Weakness #7 (severity: style, raised by 1/5)
**Claim:** Macros `\poly`, `\esssup`, `\inner` defined but never used
(`macros:61-68`).
**Verdict:** REAL-nonblocking (style).
**Fix applied:** Deleted the three dead macros.

### Weakness #8 (severity: minor/style, raised by 1/5)
**Claim:** `\Ecal` declared (`macros:77`) but unused; section 05 hand-writes raw
`\mathcal{E}` nine times.
**Verdict:** REAL-nonblocking (style).
**Fix applied:** Deleted the dead `\Ecal` macro (minimum-change vs. 9 inline
edits; raw `\mathcal{E}` is consistent within section 05).

### Weakness #9 (severity: style, raised by 1/5)
**Claim:** Theorem statement (`05:14-19`) is over-decorated: restates the bound
in two algebraic forms plus an inline explanatory clause.
**Verdict:** INTENTIONAL / would touch the headline.
**Rebuttal:** Editing this lives inside `\begin{theorem}` and modifies the
headline statement block; per the statement-change rule it is NOT auto-applied.
The dual form and the `log e = 1 ⟹ +d` clause are a deliberate
prompt-rate-matching choice. Flagged to the user, no fix.

## Fixes applied this iteration
#1, #2 (joint, REAL-blocking major — abs/no-abs seam closed via `L̄`),
#3, #4, #6 (REAL-nonblocking minor), #7, #8 (style). Rebutted: #5 (phantom),
#9 (intentional, headline). Constant changed `3 → √17` (in-proof only; headline
unchanged).

## Post-fix gates
- `lint.py` (incl. R19): **0 errors, 0 warnings**.
- `latexmk-wrapper.py`: **compile_ok = true**; 0 undef refs/cites/macros, 0
  overfull violations above threshold.
- `pdf/main.pdf` refreshed.

## Decision
Iterate (fixes applied). Next panel re-runs on the patched proof.
