# Phase D — Review iteration 3 (final, ACCEPTED)

Proof under review: **Linear convergence of gradient descent for over-parameterized two-layer
ReLU networks** (NTK analysis), `eval_results/02-ntk-convergence/`, headline
`\Cref{thm:main}` in `sections/06-main-theorem.tex`.

Five INDEPENDENT reviewers (R1 line-by-line rigor, R2 assumptions/generality, R3 ML-significance,
R4 math-taste, R5 derivation-integrity). Inputs: `sections/*.tex`, `.output/main.pdf`,
`.output/main.log`, `.proof-research/confidence-trace.md`.

## Scores

| Reviewer | Score | Blocking? |
|---|---|---|
| R1 line-by-line | 8 | no |
| R2 assumptions/generality | 8 | no |
| R3 ML-significance | 8 | no |
| R4 math-taste | 8 | no |
| R5 derivation-integrity | 9 | no |
| **mean** | **8.20** | — |

Orchestrator decision: mean **8.20 > 8** (strict bar) AND no unresolved REAL-blocking critical
→ **ACCEPT**.

Score history across iterations: 4.20 → 7.40 → 8.20.

---

## Merged + deduped weaknesses

Dedupe rule: same `file:line ± 3` OR paraphrase of the Claim = one merged weakness; keep max
severity; record how many of 5 raised it. Verified once against the cited `file:line`.

### Weakness #1 (severity: minor, raised by 3/5)
**Claim:** The per-flipping-pair coordinate perturbation magnitude `(1/√m)R_step` (`05:134-135`)
is asserted in prose, not displayed; the rigorous 1-Lipschitz-ReLU bound on
`|σ(w(k+1)ᵀxᵢ)−linearization|` is twice that, `(2/√m)R_step` (ReLU is 1-Lipschitz, applied to
both the true increment and its linearization), so the asserted per-pair constant is short by a
factor 2. (R1 minor `05:134-135`; R5 minor `05:134`; carried over from iter-2 #9.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed at `05:134-135`: the magnitude is prose-asserted and the true
1-Lipschitz figure is `(2/√m)R_step`. The factor 2 is harmlessly absorbed by the slack in
`8c·ηλ₀ ≤ ηλ₀/8` at `c ≤ 1/64` (line 148): doubling the per-pair contribution gives prefactor
`16c·ηλ₀ ≤ ηλ₀/8` still for `c ≤ 1/128`, a change in the universal constant only. The realized
`eq:remainder` bound is on the safe over-estimating side and R19 already passes. DECLINED per the
cost gate (a full Lipschitz derivation exceeds the 3-line budget for a minor non-blocking item;
identical decline to iter-2 #9). Not blocking; conclusion intact.

### Weakness #2 (severity: minor, raised by 3/5)
**Claim:** `eq:remainder`'s first inequality (`05:144-146`) names "triangle inequality within each
coordinate and Cauchy–Schwarz over the n coordinates", but the precise chain yields
`(η√n/m)‖y−u(k)‖·√(Σᵢ|S_{k,i}|²)`; the displayed `(ηn/m)|S_k|‖·‖` follows only via the unstated
extra step `√(Σᵢ|S_{k,i}|²) ≤ √n·|S_k|`. The named rule alone does not produce the displayed
factor — but the result is a valid over-estimate. (R1 minor `05:144-146`; R5 minor `05:144`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed at `05:144-146`: the transition bundles two inequalities plus a
`√n` slack into one named step, eliding the intermediate
`√(Σᵢ|S_{k,i}|²) ≤ √n·|S_k|`. The displayed bound is a correct over-estimate (it can only enlarge
the RHS), so `eq:remainder` and every downstream step hold. The elision is an exposition gap, not a
correctness gap. DECLINED on cost: inserting the intermediate display is a >3-line patch on a minor
non-blocking item with no rigor gain (the realized bound is already a safe upper bound). Surfaced,
not auto-fixed.

### Weakness #3 (severity: minor, raised by 1/5)
**Claim:** The gram-stability lemma (`03:8`) is stated for a single (possibly data-dependent) `W`
with prob `1−δ`; for a fixed data-dependent `W` correlated with `W(0)` that event is allegedly not
what the proof delivers — the statement should be the uniform sup-over-the-ball form to preclude a
fixed-`W` misreading. (R2 minor `03:8`.)
**Verdict:** PHANTOM.
**Rebuttal / fix-plan:** Misread. The object the proof actually consumes, `E_2` at `06:39-41`, is
*already* the uniform sup form: `E_2 := {‖H(W)−H(0)‖₂ ≤ λ₀/4 whenever ‖w_r−w_r(0)‖≤R ∀r}` — a
single `W(0)`-only event quantified over the whole ball, exactly precluding the fixed-`W`
misreading the reviewer fears. The lemma's "any weights (possibly depending on the data)" phrasing
at `03:8-9` is the standard universally-quantified statement whose proof is `W(0)`-only; the
downstream use is the uniform event. No defect; no change. (Two other reviewers, R1 and R3,
independently confirmed this quantifier handling is correct.)

### Weakness #4 (severity: minor, raised by 2/5)
**Claim:** Two load-bearing arithmetic chains silently assume `λ₀ ≤ n` (true since
`λ₀ = λ_min(H^∞) ≤ tr(H^∞) = n/2`), which is never stated or derived. At `05:169` the chain
`ηλ₀ ≤ κλ₀²/n² ≤ ½` writes an inequality whose first relation is actually an equality
(`η = κλ₀/n²`) and whose final `≤ ½` needs the unstated `λ₀ ≤ n`; at `04:82` the nonnegativity
`ηλ_max(H(k)) ≤ ηn ≤ λ₀/(2n) ≤ 1` likewise needs `λ₀ ≤ 2n`. (R2 minor `05:169`; R3 minor `04:82`,
`05:169`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed at both `04:82` and `05:169`: the displayed chains are correct
but rest on `λ₀ ≤ n/2`, which is nowhere recorded in `01-preliminaries.tex` (lines 44–67 define
`H^∞` and `λ₀ := λ_min(H^∞)` but never note `tr(H^∞) = n/2` ⇒ `λ₀ ≤ n/2`). The fact is true and
the proof is sound; only the supporting one-liner is missing. The minimum patch — one sentence in
the preliminaries ("`H^∞` has `H^∞_ii = 1/2`, so `tr(H^∞) = n/2` and `λ₀ ≤ n/2`") plus two cite-
markers — is ≤ 5 lines but spans three files and edits no headline. Per Component 3 it is a legal
minor non-blocking fix; since the gate is already ACCEPTED and the conclusion is intact, it is
surfaced here as a recommended (not blocking) cleanup rather than applied, consistent with the
no-modify directive for an accepted proof.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** The flip-anchor inequality (`05:104`) is decomposed via the two-leg path
`‖w_r(k)−w_r(0)‖ + ‖w_r(k+1)−w_r(k)‖` whose first `≤` is labeled "Cauchy–Schwarz", but the clean
justification that a flipping pair satisfies `|w_r(0)ᵀx_i| ≤ 2R` runs through the sign-flip
mechanism (a flip forces one endpoint's pre-activation within one step of 0); the written first
`≤` is asserted rather than derived from that mechanism. (R2 minor `05:104`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed at `05:104-110`: the displayed two-leg bound reaches the correct
`2R` and the labels (Cauchy–Schwarz, then stay-in-ball + movement, then `R_step ≤ R`) are each
individually valid; what is elided is the one clause explaining *why* a flip makes `|w_r(0)ᵀx_i|`
small — namely that `‖x_i‖=1` and a sign flip between steps `k` and `k+1` puts the pre-activation
within `R_step` of 0 at one endpoint, so the triangle path back to `w_r(0)` is bounded by
`R + R_step`. The conclusion `S_k ⊆ N` and the anti-concentration count `eq:flip-count` are
unaffected. Exposition gap, not correctness gap; ≤3-line clause, surfaced not applied (accepted
proof, no-modify).

### Weakness #6 (severity: style, raised by 1/5)
**Claim:** The spectral norm is spelled two ways for the same object: the macro `\opnorm{·}`
(= `\|·\|₂`) in §02/§03/§06, but hand-written `\norm{·}_2` in §04 (`04:73`) and §05. One quantity,
two surface spellings. (R4 style `04:73`.)
**Verdict:** REAL-nonblocking (style).
**Rebuttal / fix-plan:** Confirmed: `\opnorm` is the defined spectral-norm macro
(`01-preliminaries.tex:5`), yet `04:73` and §05 write `\norm{I − ηH(k)}_2`. A purely cosmetic
single-token substitution (`\norm{·}_2 → \opnorm{·}`) at a handful of sites. Style-level, no
correctness impact; not applied for the accepted proof (recommended cosmetic sweep only). Does not
block.

### Weakness #7 (severity: style, raised by 1/5)
**Claim:** Notational asymmetry between siblings: the smallest eigenvalue uses the macro `\lmin`
(≈25 occurrences) while the largest uses raw `\lambda_{\max}` (3 occurrences, `04:83`). Both
well-defined; the two are spelled inconsistently. (R4 style `04:83`.)
**Verdict:** INTENTIONAL / REAL-nonblocking (style).
**Rebuttal / fix-plan:** Confirmed: `\lmin` is a defined macro; no `\lmax` macro exists, so
`\lambda_{\max}` is written raw at its 3 sites (`04:80,82,83`). Both notations are correct and
unambiguous. Introducing a `\lmax` macro is a project-wide convention change outside the
minimum-change scope and is not what acceptance requires. Style-level, non-blocking; no change.

### Weakness #8 (severity: style, raised by 1/5)
**Claim:** The δ-dependence is loose by design: the width carries `1/δ³` and the residual bound
`1/δ` (Markov route) rather than the `log(1/δ)` achievable by concentration; honestly disclosed but
weaker than the strongest known DZPS form. (R3 style `06:83`.)
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Deliberate, and disclosed. The width `m ≥ Cn⁶/(λ₀⁴δ³)` and the `1/δ` slack
are the explicit choices recorded in `rem:decisions` (`06:76-86`, Socratic Q4) and the runner-log
(tight rate + `\poly` width). The reviewer explicitly tags this `style` and "honestly disclosed".
The `\todo{user-decision}` markers preserve it for live-session confirmation. Not a defect under the
adopted scope; no change.

---

## Accept decision

Mean **8.20 > 8** (strict bar). No reviewer set `Blocking? = yes`; the merged set contains **no
critical** weakness and therefore **no unresolved REAL-blocking critical**. Per Component 4 gate 1,
the accept gate is **MET → ACCEPT**.

Verdict tally over the 8 merged weaknesses: **0 REAL-blocking**, **5 REAL-nonblocking** (#1, #2, #4,
#5, #6), **1 PHANTOM** (#3), **2 INTENTIONAL/style** (#7, #8). (#7 is style and effectively
intentional given the absent `\lmax` macro.)

**Fixes applied this iteration: NONE.** The proof is ACCEPTED and per the orchestrator directive is
not modified — this iteration only records. All five REAL-nonblocking residues are minor/style,
verified to leave the conclusion intact, and either declined on the cost gate (#1, #2: prose-
asserted micro-steps that already over-estimate safely) or surfaced as recommended non-blocking
cleanups (#4 the unstated `λ₀ ≤ n/2` supporting fact; #5 the flip-mechanism clause; #6 the
`\opnorm` spelling sweep). The lone PHANTOM (#3) is rebutted: `E_2` at `06:39-41` is already the
uniform sup-over-the-ball event. The two INTENTIONAL items (#7, #8) are project-scope decisions.

No headline `\begin{theorem}`/`\begin{lemma}` statement is implicated by any weakness — no
statement-change escalation.

Convergence note: iter-3's merged set vs iter-2's. iter-2 #9 (per-pair magnitude) recurs as iter-3
#1, and iter-2 #7's display family is now fully resolved (no recurrence). The new iter-3 entries
(#2 Cauchy–Schwarz intermediate, #3–#8) are a fresh lower-severity / style layer. Overlap well
below the 0.8 stall threshold; the loop terminates on the **accept gate**, not convergence failure
or the 3-iteration cap.
