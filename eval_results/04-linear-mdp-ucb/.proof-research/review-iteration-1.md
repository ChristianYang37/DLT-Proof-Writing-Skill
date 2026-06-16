# Review iteration 1 — LSVI-UCB regret (thm:regret)

## Reviewer scores
| Reviewer | Lens | Score | Blocking |
|---|---|---|---|
| R1 | correctness: line-by-line | 8 | no |
| R2 | correctness: assumptions/generality | 9 | no |
| R3 | correctness: ML-significance | 8 | no |
| R4 | math-taste | 8 | no |
| R5 | derivation-integrity | 7 | no |
| **mean** | | **8.00** | |

**Accept gate:** mean > 8 is strict; 8.00 is NOT > 8 ⇒ **ITERATE**. No unresolved REAL-blocking critical (the only 🔴 is the symbolic C_β numeric constant, a flagged user decision — rate exponents exact). Decision: iterate, apply minimum-change fixes.

## Merged + verified weaknesses

### Weakness #1 (severity: minor, raised by 1/5: R1) — CS factor under-named in Lemma 2.1
**Claim:** The final Cauchy–Schwarz step omits the √(k−1) factor from summing vᵀΛ⁻¹v over τ; displayed (dk)^{1/2} is correct but under-licensed. (02-concentration.tex:28)
**Verdict:** REAL-nonblocking (conclusion correct; naming gap).
**Fix:** Added clause "(so the first factor is (∑‖v‖²)^{1/2}=√(k−1)≤√k)". 1 line.

### Weakness #2 (severity: minor, raised by 1/5: R1) — spurious √H in Step 6 decomposition
**Claim:** "√(H³)·√(HK)·√H = H^{5/2}√K ≠ H²√K"; middle √H spurious. Conclusion √(H³T) correct. (05-main-theorem.tex:127)
**Verdict:** REAL-nonblocking (typo; conclusion correct).
**Fix:** Replaced chain with H²√K=√(H⁴K)=√(H³·KH)=√(H³T). 1 line.

### Weakness #3 (severity: minor, raised by 2/5: R2,R3) — C / C_β cross-lemma binding left implicit
**Claim:** C in lem:recursion silently equals the event-radius C; C_β floors (≥C here, ≥C+4 in recursion) resolved only implicitly by MAX. (02-concentration.tex:110; 03-optimism.tex:79,84)
**Verdict:** REAL-nonblocking (constants licensed "change line to line"; binding correct but unstated).
**Fix:** At 02-concentration.tex:110 named C as the shared event-radius constant and switched to the stronger floor C_β≥C+4, explicitly noting it is the max of the two floors. ~3 lines.

### Weakness #4 (severity: MAJOR by R5; minor by R2, raised by 2/5: R2,R5) — discretization (cover-to-target) correction asserted not displayed
**Claim:** Fixed-V self-normalized bound applied to data-dependent V_{h+1}^k through prose; the additive discretization-correction term (the reason β=Θ(dH)) never appears as a display. (02-concentration.tex:94–104)
**Verdict:** REAL-nonblocking. The argument's validity does not hinge on the missing display — the bridge prose carries it and R1/R2/R3 line-verified the transition as correct; only R5 rated major. Still worth showing for derivation integrity.
**Fix:** Added an explicit display transferring V_{h+1}^k to its nearest cover element V̄ with additive correction 2ε√k (via 1-Lipschitzness + Cauchy–Schwarz + trace bound), evaluated ≤2dH at ε=dH/K, then carried it into the squared-norm bound via (a+b)²≤2a²+2b² with the new +2(2dH)² term absorbed into C²d²H²ι. ~14 lines. Lower-order term now load-bearing-visible.

### Weakness #5 (severity: minor, raised by 1/5: R3) — cover omits log-β dependence
**Claim:** Covering bound (eq:cover) carries no log β term though β controls the A-direction Lipschitz constant. (02-concentration.tex:91)
**Verdict:** INTENTIONAL / rate-immaterial. β enters only logarithmically and is absorbed into ι (the text states "log(1+HdK/(ελ))≲ι"); the JYWJ Lemma D.6 form quoted is the standard one. Headline rate unaffected. Rebut, no fix.

### Weakness #6 (severity: minor, raised by 1/5: R3) — prompt-vs-proven rate gap only in TODO comment
**Claim:** Proven d^{3/2}√(H³T) differs from prompt's d^{3/2}√(HT); justified only in commented-out TODO. (05-main-theorem.tex:19)
**Verdict:** INTENTIONAL (flagged user decision). The proven rate is the correct canonical JYWJ-2020 rate; the weaker prompt rate is not provable under β=Θ(dH√ι). Changing it would alter the theorem headline ⇒ out of scope per Component 3. Rebut, no fix; surfaced to user.

### Weakness #7 (severity: minor, raised by 1/5: R3) — C_β fixed point self-referential, asserted not shown
**Claim:** C_β fixed by self-referential choice (C_β≥C where C comes from a cover whose class uses β=C_β dH√ι); not exhibited as a self-consistent inequality. (02-concentration.tex:110)
**Verdict:** INTENTIONAL. The numeric C_β is a flagged symbolic constant (the sole 🔴 in the trace); rate exponents are exact, no exponential-in-H/d constant hides. The cover's log-β dependence is absorbed into ι and does NOT feed back into the exponent, so the "fixed point" is benign (β appears only inside a log). Rebut, no fix.

### Weakness #8 (severity: style, raised by 2/5: R4,R5) — phantom T₁+T₂+T₃ three-way split
**Claim:** Regret announced as T₁+T₂+T₃ but bonus sum is one underbrace T₁+T₂ never separately bounded; really a two-term split. (05-main-theorem.tex:75–82)
**Verdict:** REAL-nonblocking (decorative over-naming).
**Fix:** Relabelled to an honest two-term split: bonus sum = T₁, martingale = T₂. Updated intro prose, Step 3 heading ("two-term"), Steps 4–6 headings and the eq:T12-bound / eq:T3-bound term names. Mechanical rename, ~8 sites.

### Weakness #9 (severity: style, raised by 1/5: R4) — \Norm / \Inner cosmetic duplicate macros
**Claim:** \Norm is byte-identical to \norm; \Inner differs from \inner only by a thin space. (macros.tex:70)
**Verdict:** REAL-nonblocking style, but NOT fixed. Both macros are used (\Norm ×2, \Inner ×5) — not dead. Collapsing them touches 7 call sites (exceeds the 1-line/token style budget) and \Inner's thin space is a deliberate display-spacing choice; removing it risks an alignment regression. The comment already documents \Norm as an intentional display alias. Rebut, no fix.

### Weakness #10 (severity: style, raised by 1/5: R4) — dead macros \poly \Omegatil \Indic \argmin
**Claim:** Four declared macros never used. (macros.tex:54)
**Verdict:** REAL-nonblocking (confirmed unused by fixed-string search).
**Fix:** Removed all four. (\argmax was briefly removed too but is used at preliminaries:74 — compile caught it, rolled back and restored.) Net: 4 dead macros deleted.

### Weakness #11 (severity: minor, raised by 1/5: R5) — predictability hypothesis not asserted at cite-site
**Claim:** lem:self-normalized requires {φ_τ} to be {F_{τ−1}}-predictable; only the noise MDS property is checked at the application. (02-concentration.tex:62)
**Verdict:** REAL-nonblocking (true and easy to state).
**Fix:** Added clause "the regressors φ_h^τ are F_{τ,h−1}-measurable, hence {F_{τ,h−1}}-predictable, so the hypotheses of lem:self-normalized are met." ~2 lines.

## Fixes applied (summary)
Fixed: #1, #2, #3, #4, #8, #10, #11 (all minimum-change, within cost gates; #4's major flag addressed with an explicit display).
Rebutted (no fix): #5 (rate-immaterial), #6 (INTENTIONAL headline / user decision), #7 (INTENTIONAL symbolic constant), #9 (style, cost exceeds budget + spacing risk).

## Gates after fixes
- lint.py (incl R19): **0 errors, 0 warnings**.
- latexmk-wrapper: **compile_ok = True**, errors = [], undef_macros = [].
- pdf/main.pdf refreshed from .output/main.pdf.

## Decision
Iteration 1 complete; fixes applied and gates green. Mean was 8.00 (not > 8) ⇒ did not meet the strict accept gate this round; loop proceeds to iteration 2 (panel re-review) per review-loop.md. No unresolved REAL-blocking critical; the residual user-decision items (#6 prompt-vs-proven rate, #7 symbolic C_β) are headline/constant choices surfaced for the user, not auto-fixable.
