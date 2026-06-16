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
end Decode
