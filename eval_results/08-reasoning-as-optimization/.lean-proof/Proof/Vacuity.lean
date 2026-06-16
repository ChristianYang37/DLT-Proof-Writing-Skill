import Proof.Proofs.DecodeIff
import Mathlib.Analysis.Calculus.Deriv.Pow

/-! Vacuity / non-degeneracy witnesses for the anti-fake reviewer (NOT part of the
    delivered theorems; this file is a scratch check that the hypotheses are satisfiable
    and that `Generated` is contingent). -/

open RealInnerProductSpace
namespace Decode

-- A concrete model: E = ℝ (a real inner product space, complete), V = Bool (Fintype,
-- Nontrivial). Take L the squared norm so its gradient is 2•x (we only need the VALUE).
-- Here we just supply the hypotheses abstractly to confirm they are jointly satisfiable
-- and that the RHS of the iff can be both true and false.

-- (1) Hypotheses are satisfiable: pick x⋆ = (1:ℝ), r = 1, μ = 2, and L with gradient 2•x⋆.
--     We use `gradient (fun x => ‖x‖^2) ...`? Simpler: exhibit *some* L meeting hstat.
--     The cleanest witness: the statement is non-vacuous because for the identity-like
--     loss L x = μ/2 * ‖x‖² the gradient is μ • x. We avoid computing gradient here and
--     instead show the CONCLUSION predicate `Generated` is contingent (the real vacuity risk).

-- (2) `Generated` is genuinely contingent on V = Bool, E = ℝ:
--     W true = 1, W false = -1, x = 1  ⟹  ⟪W true, x⟫ = 1 > -1 = ⟪W false, x⟫, so Generated true 1 holds.
example : Generated (E := ℝ) (V := Bool) (fun a => if a then (1:ℝ) else -1) true (1:ℝ) := by
  intro b hb
  -- b ≠ true ⟹ b = false
  have : b = false := by cases b <;> simp_all
  subst this
  norm_num [inner]

--     Same W, but x = -1  ⟹  ⟪W true, x⟫ = -1 < 1 = ⟪W false, x⟫, so Generated true (-1) FAILS.
example : ¬ Generated (E := ℝ) (V := Bool) (fun a => if a then (1:ℝ) else -1) true (-1:ℝ) := by
  intro h
  have := h false (by simp)
  norm_num [inner] at this

end Decode

namespace Decode
-- (3) The full hypothesis bundle is jointly satisfiable by a concrete differentiable L.
--     On E = ℝ, L x = x^2 has gradient (= ordinary derivative as Riesz vector) 2 • x.
--     At x⋆ = 1, r = 1: ‖x⋆‖ = 1 = r, gradient L x⋆ = 2 • x⋆, μ = 2 ≠ 0. So the theorem's
--     premises are met by a real (differentiable, sphere-constrained, stationary) model.
example : gradient (fun x : ℝ => x ^ 2) (1 : ℝ) = (2 : ℝ) • (1 : ℝ) := by
  rw [gradient_eq_deriv]
  have hd : deriv (fun x : ℝ => x ^ 2) (1:ℝ) = 2 := by
    rw [deriv_pow_field]; norm_num
  rw [hd]; norm_num

-- (4) The cross-entropy hypothesis `hgrad` is genuinely SATISFIABLE (so
--     `decode_iff_softmax_residual` is not vacuously true via an impossible gradient form).
--     On E = ℝ, V = Bool, take W true = 1, W false = -1, a⋆ = true, and the residual
--     vector p with p true = 3, p false = 0. Then
--       ∑ c, (p c - [c = true]) • W c = (3-1)•1 + (0-0)•(-1) = 2•1,
--     which matches gradient (x ↦ x²) 1 = 2•1 from (3). So `hstat` (μ = 2) and `hgrad`
--     hold simultaneously for a real model — the cross-entropy specialization is non-vacuous.
example :
    (∑ c : Bool, ((fun a => if a then (3:ℝ) else 0) c
        - (if c = true then (1:ℝ) else 0)) •
      (fun a => if a then (1:ℝ) else -1) c) = (2 : ℝ) • (1 : ℝ) := by
  simp [Fintype.univ_bool]
  norm_num
end Decode

namespace Decode
-- (5) The BRIDGE hypothesis `L(x) < log 2` is genuinely SATISFIABLE and CONTINGENT, so
--     `loss_below_log2_decodes` is not vacuously true (no impossible premise) and not
--     trivially true (the premise can also FAIL). On E = ℝ, V = Bool, take W true = 0,
--     W false = 0 so both logits are 0; then Z = exp 0 + exp 0 = 2 and the loss at any x is
--     log 2 − 0 = log 2. We exhibit the hypothesis quantity at x = 0 equals log 2 (boundary),
--     and that lowering the competitor logit (W false = -1) makes the loss STRICTLY below log 2.

-- (5a) Boundary witness: with both rows 0, the loss equals exactly log 2 (premise FAILS, < is
--      strict). This shows the premise is contingent — it is NOT a tautology.
example :
    Real.log (∑ c : Bool, Real.exp ⟪(fun _ : Bool => (0:ℝ)) c, (0:ℝ)⟫)
        - ⟪(fun _ : Bool => (0:ℝ)) true, (0:ℝ)⟫ = Real.log 2 := by
  simp [Fintype.univ_bool, inner]

-- (5b) Satisfiable witness: take W true = 1, W false = 0, evaluate at x = 1 (so a⋆ = true is
--      strictly favored). Then ∑_c exp⟪W c, 1⟫ = exp 1 + exp 0 = e + 1 < 2e = 2·exp⟪W true,1⟫,
--      hence log(e+1) − 1 = log(e+1) − log e = log((e+1)/e) < log 2, i.e. the premise HOLDS.
--      (We state the key strict inequality e + 1 < 2e ⟺ 1 < e, which drives L(1) < log 2.)
example : (Real.exp 1 + Real.exp 0) < 2 * Real.exp 1 := by
  have h1 : (1:ℝ) < Real.exp 1 := by
    have := Real.add_one_lt_exp (x := (1:ℝ)) (by norm_num); linarith
  rw [Real.exp_zero]; linarith
end Decode
