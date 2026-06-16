# Technique digest: inner-product sign algebra + Mathlib `gradient`

This proof is self-contained algebra; no external paper citation is needed. The "technique"
is elementary real inner-product manipulation. This digest records the CONFIRMED Mathlib
lemma names (probed live in Phase 0, Lean 4.30.0 / Mathlib v4.30.0) so Phase D is mechanical.

## Setting

- `E : Type*`, `[NormedAddCommGroup E] [InnerProductSpace ℝ E]`.
- Real inner product notation: `open RealInnerProductSpace` gives `⟪x, y⟫` for `⟪x, y⟫_ℝ`
  (`inner ℝ x y`), valued in `ℝ`.

## Confirmed Mathlib lemmas (all verified to elaborate in Phase 0 smoke tests)

| Need | Mathlib lemma | Statement (real case) |
|---|---|---|
| linearity in 1st slot over `−` | `inner_sub_left` | `⟪x - y, z⟫ = ⟪x, z⟫ - ⟪y, z⟫` |
| pull real scalar out of 2nd slot | `real_inner_smul_right` | `⟪x, c • y⟫ = c * ⟪x, y⟫` (c : ℝ) |
| negate 2nd slot | `inner_neg_right` | `⟪x, -y⟫ = -⟪x, y⟫` |
| collapse nested scalars | `smul_smul` | `a • b • x = (a * b) • x` |
| cancel μ⁻¹·μ | `inv_mul_cancel₀` | `a ≠ 0 → a⁻¹ * a = 1` |
| identity scalar | `one_smul` | `1 • x = x` |
| `>` over difference | `sub_pos` | `0 < a - b ↔ b < a` |
| `0 < μ²` from `μ≠0` | `positivity` tactic | closes `0 < mu^2` given `mu ≠ 0` in context |
| clear inverses | `field_simp` | closes `mu⁻¹ * c * mu^2 = mu * c` (with `mu ≠ 0`) |

## The crux sign equivalence (proved standalone in Phase 0)

```lean
lemma sign_equiv (mu c : ℝ) (h : mu ≠ 0) : mu⁻¹ * c > 0 ↔ mu * c > 0 := by
  have hsq : (0:ℝ) < mu^2 := by positivity
  have hid : mu⁻¹ * c * mu^2 = mu * c := by field_simp
  constructor
  · intro hp; nlinarith [mul_pos hp hsq, hid]
  · intro hp
    have hp' : (0:ℝ) < mu * c * (mu^2)⁻¹ := mul_pos hp (by positivity)
    have hid2 : mu * c * (mu^2)⁻¹ = mu⁻¹ * c := by field_simp
    linarith [hid2 ▸ hp']
```
Idea: `μ⁻¹·c` and `μ·c` differ by the factor `μ² > 0`, so they share a sign.

## `gradient` (Mathlib `Mathlib.Analysis.Calculus.Gradient.Basic`)

- `gradient L x : E` is the Riesz representative of `fderiv ℝ L x`. It is `noncomputable`
  and **requires `[CompleteSpace E]`** (confirmed: synthInstanceFailed without it).
- `EuclideanSpace ℝ (Fin d)` is a `CompleteSpace` automatically (finite-dimensional).
- We NEVER differentiate `L`. `gradient L x⋆` appears only as the value inside the
  hypothesis `hstat : gradient L x⋆ = μ • x⋆`. The proof treats `gradient L x⋆` as an
  opaque vector `g : E`. So `[CompleteSpace E]` is the only cost of using the faithful
  `gradient` symbol rather than an abstract `g`.

## Decision: use `gradient L x⋆` (not an abstract g)

Per the invocation's preference ("PREFER the explicit `gradient L x⋆` if it goes through
cleanly"). Phase-0 smoke confirmed it elaborates with `[CompleteSpace E]`. This is the more
faithful encoding (the hypothesis literally says "the gradient of L at x⋆ is normal to the
sphere"), so we pay the one-line `[CompleteSpace E]` and keep `L : E → ℝ` explicit, with
`Differentiable ℝ L` recorded in Settings as documentation (it is NOT used by the proof and
is therefore kept OUT of the theorem hypotheses for Occam — see decisions.md).
