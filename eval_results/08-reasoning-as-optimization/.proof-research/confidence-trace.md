# Confidence trace

Phase-C authoring scores the **approach** at proof-obligation granularity (see
`sketch.md`). Initial tag for every step is 🔴 from-memory; Phase-0 live Lean smoke tests
upgraded the algebraic obligations to 🟢. In **Phase E** each step that is rendered to LaTeX
and passes `drift_check.py` + a `faithful` verdict is upgraded to 🔵 `lean-verified` (the
locations are then re-pointed at `sections/02-theorem-decode-iff.tex`).

## Phase-E status (2026-06-03, 2nd layer — bridge + dynamics) — 🔵 GRANTED for the bridge; B2 cited (NOT 🔵)

This layer ADDS one Lean-verified theorem and one LaTeX section with a verified part (B1) and a
clearly-separated classical/cited part (B2).

**Part A / B1 — `Decode.loss_below_log2_decodes` (the loss-to-margin bridge) — 🔵 lean-verified.**
`lean-wrapper.py Proof.lean --mode build --axioms <five>` → `integrity_ok=true`, **5/5 PASS**,
axiom closure `{propext, Classical.choice, Quot.sound}` for ALL FIVE theorems, no sorry/admit, 0
warnings. `lean_lint.py --style --lock` on `Bridge.lean` → 0 errors / 0 warnings (SL1 holds: new
key `Decode.loss_below_log2_decodes` frozen, sig_hash `3eef8334…`; the 4 prior keys unchanged).
`drift_check.py` → **0 errors, 18 Lean ↔ 18 LaTeX** (14 advisory D4 warnings only — `\Cref`
cross-references that legitimately exceed the Lean tactic-citations, the documented non-blocking
class). `lint.py` → 0 errors / 0 warnings. `latexmk-wrapper.py` → `compile_ok=true`, no undef
refs/cites, no overfull > 50 pt (one 20.3 pt hbox < 50 pt threshold), no multiply-defined labels.
The 🔵 tier is GRANTED by the gates for the 5 rendered bridge steps (`lem:bridge`,
`lem:bridge.1`–`.4`); faithfulness verdict FAITHFUL (faithfulness-review.md, "NEW (5)"); vacuity
witnesses (5a boundary, 5b satisfiable) in `Proof/Vacuity.lean` confirm the hypothesis is
contingent and the theorem non-vacuous.

**Bridge steps (🔵 lean-verified, granted by the gates):**
- `lem:bridge` — statement: `L(x) < log 2 ⟹ Generated(a⋆, x)`. Lean `loss_below_log2_decodes`.
- `lem:bridge.1` — `Z = ∑_c exp(ℓ_c) > 0` (Real.exp_pos + Finset.sum_pos over nonempty univ).
- `lem:bridge.2` — `Z < 2 exp(ℓ_{a⋆})` (Real.log_exp, Real.log_mul, Real.log_lt_log_iff).
- `lem:bridge.3` — `exp(ℓ_{a⋆}) > ∑_{c≠a⋆} exp(ℓ_c)` (Finset.add_sum_erase + cancellation).
- `lem:bridge.4` — `∀ b≠a⋆, ⟪W_b,x⟫ < ⟪W_{a⋆},x⟫` (Finset.single_le_sum, Real.exp_lt_exp); = Generated.

**Part B2 — classical / cited, NOT machine-verified, NOT 🔵.** These items are tagged
**cited/classical** (one tier below 🟢; they are NOT in the Lean closure and carry NO `@lx-from`):
- `prop:gd_rate` — smooth-convex GD rate `L(x_t) − L⋆ ≤ 2β‖x₁−x⋆‖²/(t−1) = O(1/t)`. **CITED**
  `\cite[Theorem~3.3]{bubeck2015}` (digest `cite-bubeck2015-gd-smooth-convex-rate.md`). Status:
  **cited (R5 discharged by the `[\cite{}]` bracket; no local proof).**
- `cor:decode_time` — decode-correct for `t > t⋆ = 1 + 2β‖x₁−x⋆‖²/Δ = O(1/Δ)`, stays correct
  (monotone descent). Status: **cited-not-verified** — combines the cited rate with the verified
  bridge; carries a short proof for transparency but NO `@lx-from` and is explicitly labeled
  not-Lean-verified (Remark 4.6, `rem:cor-not-verified`).
- `rem:convex`, `rem:structural`, `rem:probability` — exposition (convexity of `L`; the iff is the
  exact success boundary; `pass@T → Pr_Q[solvable]`). Status: **classical/exposition, NOT 🔵.**

The verified/cited boundary is unmistakable in the prose (an explicit boxed disclaimer opens the
section; B2 opens with "every claim … is classical and cited … none is machine-verified") and in
the provenance channel (B1 has 5 `% @lx-from` markers, B2 has zero).

## Phase-E status (2026-06-03, THIS paper — 4 results) — 🔵 GRANTED (all gates green)

This deterministic paper EXTENDS the verified iff base with two new corollaries
(`decode_fails_iff_some_competitor`, `decode_iff_softmax_residual`). All FOUR theorems are
machine-verified: `lean-wrapper.py --mode build --axioms <four>` → `integrity_ok=true`, 4/4
PASS, axiom closure `{propext, Classical.choice, Quot.sound}`, no sorry/admit;
`lean_lint.py --style --lock` → 0 errors (SL1 holds for all 4 frozen signatures — 2 carried
byte-for-byte, 2 new); `drift_check.py` → 0 errors, **13 Lean ↔ 13 LaTeX** (9 advisory D4
warnings only); `lint.py` → 0 errors; `latexmk-wrapper.py` → `compile_ok=true` (1 overfull
hbox 20.3pt < 50pt). The 🔵 tier is GRANTED by the gates for all 13 rendered steps. The new
steps follow the same `@lx` conventions (closing `-/` on its own line + `show _ ↔ _`
flush-triggers for `cor:fail.1`/`cor:ce.2`); no signature/kernel-proof drift. The historical
note below pertains to the original two-theorem iff base.

## Phase-E status (2026-06-02, iff base) — 🔵 GRANTED (all gates green)

All rendered LaTeX steps received a **`faithful`** semantic verdict in the Phase-E drift
review (Lean as ground truth; per-step audit below), and **all gates now exit 0**:
`lean-wrapper.py --mode build` → `integrity_ok=true` (axiom closure
`{propext, Classical.choice, Quot.sound}`, no `sorry`/`admit`); `lean_lint.py --style --lock`
→ 0 errors, 0 warnings (statement-lock SL1 holds); `drift_check.py` → 0 errors, **8 Lean
steps ↔ 8 LaTeX steps** (4 advisory D4 warnings only — `\Cref` cross-references that
legitimately exceed the Lean tactic-citations, which the skill defines as non-blocking);
`lint.py` → 0 errors; `latexmk-wrapper.py` → `compile_ok=true`. The 🔵 tier (drift_check
D1–D3 green + a `faithful` verdict) is therefore **granted by the gates** (not self-marked).

Fix applied (for the record): the earlier D1 failure was a `drift_check.parse_lean`
join-key artifact, not a content over/under-claim. In
`.lean-proof/Proof/Proofs/DecodeIff.lean` the closing `-/` was glued to three `@lx step:`
ids (`lem:sign_equiv`, `thm:main`, `cor:neg`) and the `thm:main.3` / `cor:neg.2` blocks
lacked a `have|calc|theorem|…` flush-trigger. Resolution: move each `-/` to its own line,
complete the statement-level `@lx` blocks (`latex`/`why`/`cite`), add a no-op `show _ ↔ _`
flush-trigger before the assembly tactics of `thm:main.3`/`cor:neg.2`, and add matching
statement-level `% @lx-from:` markers in `sections/02-theorem-decode-iff.tex`. These touch
**no theorem signature** (SL1 unchanged) and **no kernel proof term** (`show _ ↔ _` is a
definitional no-op); the Lean re-built to `integrity_ok=true` after the edits.

## Step 1
**Location:** sections/02-theorem-decode-iff.tex (obligation O0; helper `sign_equiv`)
**Content (≤ 2 lines):** For $\mu \ne 0$ and $c \in \R$: $\mu^{-1} c > 0 \iff \mu c > 0$ (they differ by the factor $\mu^2 > 0$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Standalone Lean `example` proved green in Phase 0 (`positivity` for $\mu^2>0$; `field_simp` identity $\mu^{-1}c\,\mu^2=\mu c$; `nlinarith`/`linarith`). Promoted to 🔵 (drift_check D1–D3 green + faithful drift verdict).
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:00:00Z

## Step 2
**Location:** sections/02-theorem-decode-iff.tex (obligation O1)
**Content (≤ 2 lines):** From $\grad\loss(\xstar) = \mu\,\xstar$ and $\mu \ne 0$: $\xstar = \mu^{-1}\,\grad\loss(\xstar)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Phase-0 smoke test (`smul_smul`, `inv_mul_cancel₀`, `one_smul`) elaborated green.
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:00:00Z

## Step 3
**Location:** sections/02-theorem-decode-iff.tex (obligation O2)
**Content (≤ 2 lines):** For $v := W_{\astar} - W_b$: $\inner{v}{\xstar} = \mu^{-1}\inner{v}{\grad\loss(\xstar)}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Phase-0 smoke (`real_inner_smul_right` after substituting Step 2) elaborated green.
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:00:00Z

## Step 4
**Location:** sections/02-theorem-decode-iff.tex (obligation O3)
**Content (≤ 2 lines):** Per competitor: $\inner{v}{\xstar} > 0 \iff \mu\,\inner{v}{\grad\loss(\xstar)} > 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Composite O1→O2→O3 proved end-to-end as one Lean `example` in Phase 0 (rewrite Step 3, then Step 1).
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:00:00Z

## Step 5
**Location:** sections/02-theorem-decode-iff.tex (obligation O4)
**Content (≤ 2 lines):** Cone inequality: $\inner{W_{\astar}}{\xstar} > \inner{W_b}{\xstar} \iff \inner{W_{\astar}-W_b}{\xstar} > 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Phase-0 smoke (`inner_sub_left`, `sub_pos`) — both directions elaborated green.
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:00:00Z

## Step 6
**Location:** sections/02-theorem-decode-iff.tex (obligation O5; assembly)
**Content (≤ 2 lines):** Unfold $\Generated$ and push the per-competitor equivalence (Step 5 then Step 4) under $\forall b \ne \astar$ to obtain the biconditional.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (Phase D `integrity_ok`): `unfold Generated` + explicit `Iff.intro` pushing the per-competitor equivalence under `∀ b, b ≠ a⋆ →`. Promoted to 🔵 (drift_check D1–D3 green + faithful drift verdict).
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:30:00Z

## Step 7
**Location:** sections/02-theorem-decode-iff.tex (obligation O6; corollary)
**Content (≤ 2 lines):** Under $\mu < 0$: $\mu\,\inner{v}{g} > 0 \iff \inner{v}{-g} > 0$, via $\mu<0\Rightarrow(\mu c>0\iff c<0)$ and $\inner{v}{-g}=-\inner{v}{g}$ (`inner_neg_right`); chained under $\forall b$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (Phase D `integrity_ok`): `forall_congr'` + `imp_congr_right`, then `inner_neg_right` and two `nlinarith` calls (using `mul_pos_iff` and `mul_pos_of_neg_of_neg`) for the `μ<0` sign step. Promoted to 🔵 (drift_check D1–D3 green + faithful drift verdict).
**Sub-agent task id:** none
**Last updated:** 2026-06-02T21:30:00Z

## Step 8
**Location:** sections/04-bridge-and-dynamics.tex:38 (bridge statement `lem:bridge`)
**Content (≤ 2 lines):** Bridge: `L(x) = log(∑_c exp⟪W c,x⟫) − ⟪W a⋆,x⟫ < log 2 ⟹ Generated(a⋆,x)` (cross-entropy below log 2 ⟹ greedy decode).
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (`Decode.loss_below_log2_decodes`, `Bridge.lean`); `integrity_ok=true`, axiom closure `{propext, Classical.choice, Quot.sound}`. Promoted to 🔵 (drift_check D1–D3 green + faithful drift verdict; faithfulness-review.md "NEW (5)").
**Sub-agent task id:** none
**Last updated:** 2026-06-03T00:00:00Z

## Step 9
**Location:** sections/04-bridge-and-dynamics.tex:53 (`lem:bridge.1`)
**Content (≤ 2 lines):** The softmax partition is strictly positive: `Z = ∑_c exp(ℓ_c) > 0`.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (`Real.exp_pos` per summand + `Finset.sum_pos` over the nonempty `univ`, from `Nontrivial V`). Promoted to 🔵 (drift_check green + faithful).
**Sub-agent task id:** none
**Last updated:** 2026-06-03T00:00:00Z

## Step 10
**Location:** sections/04-bridge-and-dynamics.tex:62 (`lem:bridge.2`)
**Content (≤ 2 lines):** From `log Z − ℓ_{a⋆} < log 2`: `Z < 2 exp(ℓ_{a⋆})` (via `Real.log_exp`, `Real.log_mul`, `Real.log_lt_log_iff`, both sides positive).
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (rewrite `log(2·exp ℓ_{a⋆}) = log 2 + ℓ_{a⋆}`, then strict monotonicity of `log`). Promoted to 🔵 (drift_check green + faithful).
**Sub-agent task id:** none
**Last updated:** 2026-06-03T00:00:00Z

## Step 11
**Location:** sections/04-bridge-and-dynamics.tex:73 (`lem:bridge.3`)
**Content (≤ 2 lines):** Split `Z = exp(ℓ_{a⋆}) + ∑_{c≠a⋆} exp(ℓ_c)` (`Finset.add_sum_erase`); cancelling gives `exp(ℓ_{a⋆}) > ∑_{c≠a⋆} exp(ℓ_c)`.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (`Finset.add_sum_erase` at `a⋆ ∈ univ` + `linarith` cancellation against Step 10). Promoted to 🔵 (drift_check green + faithful).
**Sub-agent task id:** none
**Last updated:** 2026-06-03T00:00:00Z

## Step 12
**Location:** sections/04-bridge-and-dynamics.tex:81 (`lem:bridge.4`)
**Content (≤ 2 lines):** For each `b≠a⋆`: `exp(ℓ_b) ≤ ∑_{c≠a⋆} exp(ℓ_c) < exp(ℓ_{a⋆})` (`Finset.single_le_sum`); strip `exp` (`Real.exp_lt_exp`) ⟹ `⟪W b,x⟫ < ⟪W a⋆,x⟫`, i.e. `Generated`.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔵 lean-verified
**Verification method:** Machine-verified in Lean (`Finset.single_le_sum`, `lt_of_le_of_lt`, `Real.exp_lt_exp.mp`, then `simpa` to unfold `Generated`). Promoted to 🔵 (drift_check green + faithful).
**Sub-agent task id:** none
**Last updated:** 2026-06-03T00:00:00Z

## B2 items (classical / cited — NOT 🔵, recorded for completeness, NOT counted as verified steps)
- `prop:gd_rate` (sections/04-bridge-and-dynamics.tex): smooth-convex GD rate. **CITED** `\cite[Theorem~3.3]{bubeck2015}`; status = cited (not machine-verified). NOT 🔵.
- `cor:decode_time`: decode-correct in `O(1/Δ)` steps + monotone. Status = cited-not-verified (combines cited rate + verified bridge; no `@lx-from`, see `rem:cor-not-verified`). NOT 🔵.
- `rem:convex`, `rem:structural`, `rem:probability`: classical/exposition. NOT 🔵.

These B2 items deliberately carry NO 🔵 tag and NO `@lx-from`; they are listed here only to make
the verified/cited boundary explicit in the trace. They are NOT in the Lean axiom closure.
