# Review iteration 2 — LSVI-UCB regret (thm:regret)

## Reviewer scores
| Reviewer | Lens | Score | Blocking |
|---|---|---|---|
| R1 | correctness: line-by-line | 8 | no |
| R2 | correctness: assumptions/generality | 8 | no |
| R3 | correctness: ML-significance | 9 | no |
| R4 | math-taste | 8 | no |
| R5 | derivation-integrity | 9 | no |
| **mean** | | **8.40** | |

**Accept gate:** mean = 8.40 > 8 (strict) ✅ AND no unresolved REAL-blocking critical ✅ ⇒ **ACCEPT**.
Score history: iteration 1 = 8.00, iteration 2 = 8.40. The iteration-1 fixes (CS-factor naming, two-term relabel, discretization display, predictability clause, dead-macro removal) lifted four lenses; the only new substantive finding is a precision defect *inside* the lower-order discretization term that was made visible by iteration 1's own display addition.

## Merged + verified weaknesses

### Weakness #1 (severity: minor, raised by 3/5: R1, R2, R6-style-via-R1; the discretization-correction chain) — dropped √(k−1) Cauchy–Schwarz factor + silent k≥d
**Claim (merged):** At 02-concentration.tex:113–115 the chain
`‖∑_τ φ^τ[ε^τ(V)−ε^τ(V̄)]‖_{Λ⁻¹} ≤ 2ε(∑_τ φ^τᵀΛ⁻¹φ^τ)^{1/2} ≤ 2ε√d ≤ 2ε√k`
is not licensed as displayed: (a) the first `≤` drops a √(k−1) Cauchy–Schwarz factor — the correct deterministic bound is `2ε·∑_τ‖φ^τ‖_{Λ⁻¹} ≤ 2ε√((k−1)d)`, not `2ε(∑ quad)^{1/2}=2ε‖∑‖`-style; and (b) `2ε√d ≤ 2ε√k` silently assumes k≥d (false in the early-episode d>k regime, e.g. k=1 gives an empty sum so the true correction is 0). Raised by R1 (minor, with numerical violations up to ~1.75×), R2/R5 (the squared correction `2(2dH)²` should be `2·(2ε√((k−1)d))² = O(d³H²/K)`), and R6 (minor, k=1 empty-sum counterexample).
**Verdict:** REAL-nonblocking.
**Verification:** I reproduced the violation numerically — with adversarial signs `lhs/claimed_rhs` reaches ~2.45 (>1 ⇒ displayed bound false), and `√d ≤ √k` fails whenever d>k. The *correct* bound is `2ε√((k−1)d)`. With ε=dH/K this is `2(dH/K)√((k−1)d) ≤ 2dH√(d/K)`; squared = `4d³H²/K ≤ 4d²H²` for K≥d, which absorbs into the `C²d²H²ι` radius exactly as the body intends. **The conclusion (radius `C·dH√ι`, β floor, final rate) is unaffected** — only the written chain is imprecise. Choosing ε a √d-factor smaller (ε=dH/(K√d)) removes even the K≥d assumption, since the cover depends only on log(1/ε). 
**Rebuttal / fix-plan (NOT applied — accepted):** The defect lives entirely inside a provably lower-order term that does not feed the rate, the β constant, or any load-bearing inequality; the panel itself rates it minor/non-blocking with the conclusion intact. Minimum fix (≤3 lines), deferred to the next author pass: replace the chain at :113–115 with `≤ 2ε∑_τ‖φ^τ‖_{Λ⁻¹} ≤ 2ε√((k−1)d) ≤ 2dH√(d/K)` and update the squared term at :120 from `2(2dH)²` to `2(2dH)²d/K`, which is still ≤ `8d²H²` for K≥d and absorbs identically. No statement change; no other site touched.

### Weakness #2 (severity: minor, raised by 3/5: R2, R3, R5; the symbolic constant C_β) — C_β unpinned / self-referential, sole 🔴 in trace
**Claim (merged):** The universal bonus constant C_β in β=C_β dH√ι is fixed by the self-referential floor `C_β ≥ C+4` (where C is an event-radius constant computed over a value class whose A-direction radius itself depends on β), is never pinned numerically, and is carried as the only 🔴 `\todo` in the confidence trace. R2 adds that the covering bound at :96 replaces Jin's explicit log β² term with HdK inside the log, creating a disclosed implicit dependence of C on C_β. (02-concentration.tex:96, 131, 136)
**Verdict:** INTENTIONAL.
**Verification:** Confirmed at :131–138. This is the A.1a Q2 user-decision: a symbolic, dependency-tagged universal constant with rate-exact exponents and a `\todo{verify: C_beta}` for a human to pin. β enters the cover only through `log(1+HdK/(ελ)) ≲ ι` — logarithmically — so the "fixed point" is benign: β never appears in an exponent and the self-reference does not feed back into the rate. Already rebutted in iteration 1 (weaknesses #5, #7).
**Rebuttal / fix-plan:** No fix. Pinning the numeric constant is out-of-scope false precision; the symbolic treatment is the declared author decision, rate exponents are exact, and no exponential-in-(H,d) constant hides. Surfaced to the user as a residual constant-accounting item.

### Weakness #3 (severity: style, raised by 2/5: R4 ×2 sites; stale three-term naming) — off-by-one eq labels + stale trace term names
**Claim (merged):** Equation labels `eq:T3-bound` (05-main-theorem.tex:88, on the now-`T_2` martingale bound) and `eq:T12-bound` (:113, on the now-`T_1` bonus bound) are off-by-one survivors of the iteration-1 three-term→two-term refactor; and the confidence trace (.proof-research/confidence-trace.md:348, 366) still names the decomposition `T_1+T_2`/`T_3` under the obsolete three-term scheme, contradicting the body's `T_1`(bonus)/`T_2`(martingale). Both are invisible in the compiled PDF.
**Verdict:** REAL-nonblocking (style residue).
**Verification:** Confirmed: :88 `\label{eq:T3-bound}` sits above `T_2 = ∑∑ζ ≤ 4H√(Tι)`; :113 `\label{eq:T12-bound}` sits above `T_1 = 2β∑…`. Cross-refs resolve cleanly (both labels are referenced consistently by name at :124, so the PDF is correct — only the label *string* is stale). Trace :348/:366 likewise carry old names. No undefined/multiply-defined labels; no verification impact.
**Rebuttal / fix-plan (NOT applied — accepted):** Cosmetic only and invisible in the PDF; renaming a `\label` would touch its `\eqref` consumers (the minimum-change rule forbids gratuitous label renames, and the cost exceeds the single-token style budget once consumers are counted). Deferred: optionally rename `eq:T3-bound`→`eq:T2-bound`, `eq:T12-bound`→`eq:T1-bound` with their `\eqref`s, and update trace :348/:366 to `T_1`/`T_2`. No correctness effect.

### Weakness #4 (severity: minor, raised by 1/5: R2; Azuma cross-conditioning) — increment bound uses optimism (δ≥0) which holds only on 𝓔
**Claim:** The Azuma increment bound `|ζ_{h+1}^k|≤2H` is justified via `0≤δ_{h+1}^k≤H`, whose lower bound δ≥0 uses optimism (which holds only on 𝓔), yet Azuma produces a separate event 𝓔′ combined with 𝓔 by a union bound — so the surely-bounded-increments hypothesis is not cleanly established off 𝓔. (05-main-theorem.tex:85)
**Verdict:** REAL-nonblocking (minor; bound holds with a worse-but-sufficient constant off 𝓔).
**Verification:** Confirmed the text at :84–87 conditions on 𝓔 ("On 𝓔, … with `|ζ|≤2H` since `0≤δ≤H`"). The clean reading: `δ_{h+1}^k = V^k−V^{π^k}`; even *off* 𝓔, `V^k∈[0,H]` (clipped by the min{·,H} in Q-def) and `V^{π^k}∈[0,H]`, so `|δ|≤H` and `|ζ|≤2H` hold *surely*, independent of optimism — optimism (δ≥0) is only needed for Step 1's regret reduction, not for the increment bound. Hence the Azuma hypothesis is in fact established off 𝓔; the prose merely over-attributes the bound to the `0≤δ` form. Trace Step 39 already 🟡 cross-checked this.
**Rebuttal / fix-plan (NOT applied — accepted):** The increment bound is surely true via the [0,H] range of both clipped value functions, so the union bound P[𝓔∩𝓔′]≥1−δ is valid as written; the only gap is presentational over-attribution. Optional ≤1-line fix: justify `|ζ|≤2H` from `V^k,V^{π^k}∈[0,H]` (surely) rather than from `0≤δ≤H` (on 𝓔). Non-blocking; conclusion intact.

### Weakness #5 (severity: minor, raised by 1/5: R4; base-symbol overload T) — T:=KH reused for term names T_1,T_2
**Claim:** The base letter T denotes both the scalar total-step count T:=KH (01-preliminaries.tex:8) and the regret-decomposition terms T_1,T_2; a mild base-symbol overload (distinct roles, never colliding in one expression).
**Verdict:** REAL-nonblocking (non-ambiguous, explicitly noted as such by the reviewer).
**Verification:** Confirmed at preliminaries:8 (`T:=KH`) vs main-theorem:75/77 (`T_1`,`T_2` underbraces). The scalar T and subscripted T_i never appear in the same expression and carry distinct typographic roles; no ambiguity arises.
**Rebuttal / fix-plan:** No fix. Renaming either symbol cascades across many call sites (well beyond the style budget) and the convention `T`=steps, `T_i`=decomposition terms is standard and reader-clear. Reviewer itself grades it non-ambiguous.

### Weakness #6 (severity: style, raised by 1/5: R5; P_h-monotonicity asserted in prose) — nonnegativity-preservation stated without a one-line display
**Claim:** Monotonicity/nonnegativity-preservation of P_h is asserted in prose at two load-bearing sites (optimism induction 03-optimism.tex:113 and the per-step recursion) without a one-line display, though it is immediate from P_h being a probability-kernel expectation.
**Verdict:** INTENTIONAL / REAL-nonblocking (immediate from the definition; display would be redundant).
**Verification:** Confirmed at 03-optimism.tex:112–113: "uses `P_h(V^k−V^⋆)≥0` (from the inductive hypothesis and `P_h` preserving nonnegativity)". P_h is `(P_h f)(x,a)=E[f(x′)|x,a]`, an expectation under a probability kernel, so `f≥0 ⇒ P_h f≥0` is the monotonicity of expectation — a one-liner the reader supplies. Both citations of the fact are correctly hypothesised (inductive hypothesis gives the nonnegativity of the integrand).
**Rebuttal / fix-plan:** No fix. The property is the monotonicity of a probability-kernel expectation, immediate and named in-line; adding a display for `E[f]≥0 when f≥0` would be over-decoration against the Occam lens. Non-blocking.

## Decision
**ACCEPT.** Mean 8.40 > 8 (strict) and no unresolved REAL-blocking critical (the sole 🔴, C_β, is an INTENTIONAL flagged symbolic constant with rate-exact exponents). Per review-loop.md Component 4 gate 1, the loop terminates in success at iteration 2. **No fixes applied** — an accepted proof is recorded, not modified.

Verdict counts (6 merged weaknesses): REAL-nonblocking ×4 (#1, #3, #4, #6-partial), INTENTIONAL ×2 (#2, #6 graded INTENTIONAL/nonblocking), PHANTOM ×0, REAL-blocking ×0, critical ×0.

The four REAL-nonblocking items are all precision/cosmetic and deferred (not auto-fixed, since acceptance forbids modifying the proof): (#1) the imprecise but lower-order discretization chain at :113–120, (#3) stale `eq:T3/T12` labels + trace term names, (#4) Azuma increment over-attributed to optimism, (#6) prose P_h-monotonicity. Each carries a ≤3-line minimum-change fix-plan above for a future author pass; none affects the headline statement or rate.
