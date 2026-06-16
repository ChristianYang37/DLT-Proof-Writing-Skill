# Proof sketch — `decode_iff_gradient_separation` (+ corollary)

## Strategy (one sentence)
Reduce the biconditional pointwise over competitors `b ≠ a⋆`: each cone inequality
`⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫` is, after substituting `x⋆ = μ⁻¹·gradient L x⋆` (from stationarity)
and pulling the scalar out of the inner product, equivalent to the signed alignment
`μ·⟪W a⋆ − W b, gradient L x⋆⟫ > 0`; combine over `b`.

## Obligations and their discharge

**O0 (helper) — sign equivalence.** For `μ ≠ 0` and any `c : ℝ`,
`μ⁻¹·c > 0 ⟺ μ·c > 0`.
*Discharge:* `μ⁻¹·c` and `μ·c` differ by the strictly positive factor `μ² > 0`
(`positivity`), so they share a sign. Proved standalone in Phase 0 (`field_simp` for the
identity `μ⁻¹·c·μ² = μ·c`, then `nlinarith`/`linarith`). 🟢 (named-arithmetic, hand- &
machine-checked in Phase 0).

**O1 — express `x⋆` via the gradient.** From `hstat : gradient L x⋆ = μ • x⋆` and `μ ≠ 0`,
`x⋆ = μ⁻¹ • gradient L x⋆`.
*Discharge:* rewrite `hstat`, then `smul_smul`, `inv_mul_cancel₀ hμ`, `one_smul`. 🟢
(verified in Phase-0 smoke).

**O2 — gap inner product in gradient coordinates.** For `v := W a⋆ − W b`,
`⟪v, x⋆⟫ = μ⁻¹ * ⟪v, gradient L x⋆⟫`.
*Discharge:* substitute O1, then `real_inner_smul_right`. 🟢 (Phase-0 smoke).

**O3 — per-`b` sign bridge.** `⟪v, x⋆⟫ > 0 ⟺ μ * ⟪v, gradient L x⋆⟫ > 0`.
*Discharge:* rewrite by O2, then O0 with `c := ⟪v, gradient L x⋆⟫`. 🟢 (the composite O1→O2→O3
was proved end-to-end as a single `example` in Phase 0).

**O4 — unfold the cone inequality.** `⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫ ⟺ ⟪W a⋆ − W b, x⋆⟫ > 0`.
*Discharge:* `inner_sub_left`, `sub_pos` (with `gt_iff_lt`). 🟢 (Phase-0 smoke, both directions).

**O5 — assemble the biconditional.** `Generated W a⋆ x⋆ = ∀ b ≠ a⋆, ⟪W a⋆,x⋆⟫ > ⟪W b,x⋆⟫`;
push the per-`b` equivalence (O4 then O3) under the `∀ b, b ≠ a⋆ →`.
*Discharge:* unfold `Generated`; `forall_congr'` / `Iff.intro` with a per-`b` lambda applying
O4∘O3. 🟢 (structural; the only "memory" risk is the exact `forall_congr` plumbing, which the
Lean kernel will check — and which I will write as explicit intro/constructor if `forall_congr'`
is fussy).

**O6 (corollary) — μ<0 descent form.** Under `μ < 0`,
`μ * ⟪v, g⟫ > 0 ⟺ ⟪v, −g⟫ > 0`.
*Discharge:* `μ < 0 ⟹ (μ * c > 0 ⟺ c < 0)` (`mul_pos_iff` / sign reasoning with `hμ`), and
`⟪v, −g⟫ = −⟪v, g⟫` via `inner_neg_right`, so `⟪v,−g⟫ > 0 ⟺ −⟪v,g⟫ > 0 ⟺ ⟪v,g⟫ < 0`. Chain
with the main theorem under the `∀ b`. 🟡 (the `μ<0` sign step is elementary but the exact
Mathlib lemma name for `μ*c>0 ↔ c<0` may need a 1-line `nlinarith`/`constructor`; will pin in
Phase D).

## Risk assessment
All of O0–O5 were de-risked by live Phase-0 smoke tests (the composite O1–O4 and O0 elaborated
green). O6 is a short additional sign manipulation. No step depends on differentiability,
convexity, minimality, or the sphere radius value. The unused hypotheses `hr, hnorm` (and the
`Fintype/Nontrivial` instances) are expected to draw `unused variable` linter notes — benign
and documented (decisions.md D3).

## Occam check
No lemma is introduced that is not invoked. The only auxiliary is O0 (the sign equivalence),
used twice (main + corollary). No unrequested theorems.
