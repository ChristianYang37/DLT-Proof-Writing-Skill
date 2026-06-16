# Dependency graph

Single result; minimal graph. Nodes marked `[Lean]` become Lean declarations.

```
Settings  [Lean: Proof/Settings.lean]
  E : real InnerProductSpace, [CompleteSpace E]      -- carrier (general; EuclideanSpace ℝ (Fin d) is a model)
  V : Fintype, Nontrivial                            -- vocabulary, ≥ 2 tokens
  W : V → E                                          -- unembedding (token rows)
  r : ℝ, hr : 0 < r                                  -- sphere radius
  L : E → ℝ                                          -- implicit loss (Differentiable noted; never differentiated)
  Generated (a x) := ∀ b ≠ a, ⟪W a, x⟫ > ⟪W b, x⟫    -- decoder predicate (greedy argmax = true decoder)
        │
        ▼
sign_equiv_of_ne_zero  [Lean: helper in Proofs/01-decode-iff.lean]
  for μ ≠ 0:  μ⁻¹ * c > 0  ↔  μ * c > 0             -- crux algebra (multiply by μ² > 0)
        │
        ▼
decode_iff_gradient_separation  [Lean: Statements.lean sig, Proofs/01-decode-iff.lean proof]   ← MAIN
  hyps: ‖x⋆‖ = r,  gradient L x⋆ = μ • x⋆,  μ ≠ 0
  concl: Generated a⋆ x⋆  ↔  ∀ b ≠ a⋆, μ * ⟪W a⋆ − W b, gradient L x⋆⟫ > 0
        │
        ▼
decode_iff_descent_separation_of_neg  [Lean: Proofs/DecodeIff.lean]   ← COROLLARY (μ<0)
  extra hyp: μ < 0
  concl: Generated a⋆ x⋆  ↔  ∀ b ≠ a⋆, ⟪W a⋆ − W b, −gradient L x⋆⟫ > 0

decode_fails_iff_some_competitor  [Lean: Proofs/DecodeIff.lean]   ← COROLLARY (failure / De Morgan dual)
  same hyps as MAIN
  concl: ¬ Generated a⋆ x⋆  ↔  ∃ b ≠ a⋆, μ * ⟪W a⋆ − W b, gradient L x⋆⟫ ≤ 0
  derivation: rw [MAIN]; push_neg; rfl   (¬∀→∃, ¬(c>0) ↦ c≤0)

decode_iff_softmax_residual  [Lean: Proofs/DecodeIff.lean]   ← COROLLARY (cross-entropy instantiation)
  extra: [DecidableEq V], p : V → ℝ,  hgrad : gradient L x⋆ = ∑_c (p_c − [c=a⋆]) • W c
  concl: Generated a⋆ x⋆  ↔  ∀ b ≠ a⋆, μ · ∑_c (p_c − [c=a⋆]) (⟪W a⋆,W c⟫ − ⟪W b,W c⟫) > 0
  derivation: per-b identity ⟪W a⋆−W b, ∇L⟫ = ∑_c (p_c−[c=a⋆])(⟪W a⋆,W c⟫−⟪W b,W c⟫)
              (inner_sum, real_inner_smul_right, inner_sub_left, Finset.sum_congr);
              then rw [MAIN]; forall_congr'; imp_congr_right; rw [identity].
```

(MAIN's per-`b` reduction below is unchanged; the two new corollaries reuse it.)

## Per-`b` reduction inside the main proof (the heart)

For a fixed competitor `b ≠ a⋆`, set `v := W a⋆ − W b`:
1. `Generated a⋆ x⋆` ⟺ `∀ b ≠ a⋆, ⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫`  (unfold def)
2. `⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫` ⟺ `⟪v, x⋆⟫ > 0`               (`inner_sub_left` + `sub_pos`)
3. from `gradient L x⋆ = μ • x⋆`, `μ ≠ 0`:  `x⋆ = μ⁻¹ • gradient L x⋆`   (`smul_smul`, `inv_mul_cancel₀`, `one_smul`)
4. `⟪v, x⋆⟫ = μ⁻¹ * ⟪v, gradient L x⋆⟫`                     (`real_inner_smul_right`)
5. `μ⁻¹ * ⟪v, gradient L x⋆⟫ > 0` ⟺ `μ * ⟪v, gradient L x⋆⟫ > 0`  (sign_equiv, μ²>0)
6. combine pointwise over `b` with `forall_congr`.

## Corollary derivation

`μ < 0`, so `μ * c > 0 ⟺ -c > 0 ⟺ ⟪v, -g⟫ > 0`. Use `μ * c > 0 ⟺ c < 0` (since μ<0),
and `⟪v, -g⟫ = -⟪v, g⟫` via `inner_neg_right`. Pointwise rewrite under the ∀.
