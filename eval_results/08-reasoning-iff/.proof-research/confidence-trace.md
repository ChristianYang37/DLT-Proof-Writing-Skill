# Confidence trace

Phase-C authoring scores the **approach** at proof-obligation granularity (see
`sketch.md`). Initial tag for every step is 🔴 from-memory; Phase-0 live Lean smoke tests
upgraded the algebraic obligations to 🟢. In **Phase E** each step that is rendered to LaTeX
and passes `drift_check.py` + a `faithful` verdict is upgraded to 🔵 `lean-verified` (the
locations are then re-pointed at `sections/02-theorem-decode-iff.tex`).

## Phase-E status (2026-06-02) — 🔵 GRANTED (all gates green)

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
