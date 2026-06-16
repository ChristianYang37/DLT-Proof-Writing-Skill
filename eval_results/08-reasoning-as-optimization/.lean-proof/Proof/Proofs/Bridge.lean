import Proof.Statements
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# Bridge: cross-entropy loss value ⟹ greedy decode

The single-token cross-entropy loss is `L(x) = log (∑_c exp ⟪W c, x⟫) − ⟪W a⋆, x⟫`
(`Decode.lossCE`), i.e. `−log p_{a⋆}(x)`. This file proves the **loss-to-margin bridge**:

> if `L(x) < log 2` then the greedy decoder outputs `a⋆` (`Decode.Generated W a⋆ x`).

Intuition: `L(x) < log 2 ⟺ p_{a⋆}(x) > 1/2`, and a token with softmax mass `> 1/2`
strictly beats the **combined** mass of all other tokens, hence beats each competitor's
logit individually. The argument is pure log/exp algebra over a finite nonempty sum; the
loss is never differentiated. This is the analytic link between the verified decode-iff
(WHICH token a stationary point decodes, §2–§3) and the convergence-rate story (how the
loss drops; §4 B2, classical/cited).

Mirrors `sections/04-bridge-and-dynamics.tex` (B1, verified part). The `@lx` step ids are
the join key for `drift_check.py`.
-/

open RealInnerProductSpace

namespace Decode

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable {V : Type*} [Fintype V] [Nontrivial V]

/-- **Bridge — cross-entropy below `log 2` ⟹ greedy decode.**

If the single-token cross-entropy loss at `x` is strictly below `log 2`
(`L(x) = log (∑_c exp ⟪W c, x⟫) − ⟪W a⋆, x⟫ < log 2`, i.e. the softmax probability of `a⋆`
exceeds `1/2`), then the greedy decoder outputs `a⋆`: `Generated W a⋆ x`.

The hypothesis `hlow` is stated on the unfolded loss (the `log`-partition minus the answer
logit) so that the statement is self-contained; it is definitionally `lossCE W a_star x < Real.log 2`.

@lx kind: named
@lx latex: \loss(x) < \log 2 \implies \Generated(\astar, x)
@lx why: the loss-to-margin bridge (theorem statement, rendered as the lemma environment)
@lx cite: --
@lx step: lem:bridge
-/
theorem loss_below_log2_decodes [DecidableEq V]
    (W : V → E) (x : E) (a_star : V)
    (hlow : Real.log (∑ c, Real.exp ⟪W c, x⟫) - ⟪W a_star, x⟫ < Real.log 2) :
    Generated W a_star x := by
  -- abbreviations: logits ℓ c := ⟪W c, x⟫ and partition Z := ∑_c exp (ℓ c)
  set ℓ : V → ℝ := fun c => ⟪W c, x⟫ with hℓ
  set Z : ℝ := ∑ c, Real.exp (ℓ c) with hZ
  -- each logit's exponential is strictly positive (absorbed into bridge.1)
  -- @lx kind: internal
  have hexp_pos : ∀ c, 0 < Real.exp (ℓ c) := fun c => Real.exp_pos _
  /- @lx step: lem:bridge.1
     @lx kind: arith
     @lx latex: Z = \sum_{c} \exp(\ell_c) > 0
     @lx why: each summand \exp(\ell_c) is strictly positive (Real.exp_pos) and the index type is nonempty (Nontrivial ⟹ univ.Nonempty), so the partition sum Z is strictly positive (Finset.sum_pos)
     @lx cite: -/
  have hZpos : 0 < Z := by
    rw [hZ]
    exact Finset.sum_pos (fun c _ => hexp_pos c) Finset.univ_nonempty
  /- @lx step: lem:bridge.2
     @lx kind: arith
     @lx latex: Z < 2\,\exp(\ell_{\astar})
     @lx why: the hypothesis \log Z - \ell_{\astar} < \log 2 rearranges (via \ell_{\astar} = \log\exp(\ell_{\astar}), Real.log_exp, and Real.log_mul with 2 \ne 0, \exp(\ell_{\astar}) \ne 0) to \log Z < \log (2\exp(\ell_{\astar})); both sides positive, so Real.log_lt_log_iff gives Z < 2\exp(\ell_{\astar})
     @lx cite: -/
  have hZlt : Z < 2 * Real.exp (ℓ a_star) := by
    -- @lx kind: internal
    have hlow' : Real.log Z < Real.log (2 * Real.exp (ℓ a_star)) := by
      rw [Real.log_mul (by norm_num) (Real.exp_ne_zero _), Real.log_exp]
      -- goal: log Z < log 2 + ℓ a_star ; from hlow : log Z - ℓ a_star < log 2
      have hsub : Real.log Z - ℓ a_star < Real.log 2 := hlow
      linarith
    -- @lx kind: internal
    have h2exp_pos : 0 < 2 * Real.exp (ℓ a_star) := by positivity
    exact (Real.log_lt_log_iff hZpos h2exp_pos).mp hlow'
  -- split the partition at a⋆ (absorbed into bridge.3)
  -- @lx kind: internal
  have hsplit : Real.exp (ℓ a_star) + (∑ c ∈ Finset.univ.erase a_star, Real.exp (ℓ c)) = Z := by
    rw [hZ]
    exact Finset.add_sum_erase Finset.univ (fun c => Real.exp (ℓ c)) (Finset.mem_univ a_star)
  /- @lx step: lem:bridge.3
     @lx kind: arith
     @lx latex: \exp(\ell_{\astar}) > \sum_{c \ne \astar} \exp(\ell_c)
     @lx why: split Z = \exp(\ell_{\astar}) + \sum_{c \ne \astar}\exp(\ell_c) (Finset.add_sum_erase at a⋆ ∈ univ); substituting into Z < 2\exp(\ell_{\astar}) and cancelling one \exp(\ell_{\astar}) leaves the competitors' total mass below \exp(\ell_{\astar})
     @lx cite: lem:bridge.2 -/
  have hrest : (∑ c ∈ Finset.univ.erase a_star, Real.exp (ℓ c)) < Real.exp (ℓ a_star) := by
    have hcomb : Real.exp (ℓ a_star) + (∑ c ∈ Finset.univ.erase a_star, Real.exp (ℓ c))
        < 2 * Real.exp (ℓ a_star) := by rw [hsplit]; exact hZlt
    linarith
  /- @lx step: lem:bridge.4
     @lx kind: named
     @lx latex: \forall b \ne \astar,\ \inner{W_b}{x} < \inner{W_{\astar}}{x}
     @lx why: for each competitor b \ne \astar, \exp(\ell_b) is one nonnegative summand of \sum_{c \ne \astar}\exp(\ell_c) (Finset.single_le_sum, b ∈ univ.erase a⋆), so \exp(\ell_b) ≤ that sum < \exp(\ell_{\astar}); strict monotonicity of exp (Real.exp_lt_exp) gives \ell_b < \ell_{\astar}, i.e. \inner{W_b}{x} < \inner{W_{\astar}}{x}; this is exactly Generated
     @lx cite: lem:bridge.3 -/
  show ∀ b, b ≠ a_star → ⟪W a_star, x⟫ > ⟪W b, x⟫
  intro b hb
  -- b lies in the competitor set univ.erase a⋆ (internal bookkeeping)
  -- @lx kind: internal
  have hbmem : b ∈ Finset.univ.erase a_star := Finset.mem_erase.mpr ⟨hb, Finset.mem_univ b⟩
  -- @lx kind: internal
  have hb_le : Real.exp (ℓ b) ≤ ∑ c ∈ Finset.univ.erase a_star, Real.exp (ℓ c) :=
    Finset.single_le_sum (fun c _ => (hexp_pos c).le) hbmem
  -- @lx kind: internal
  have hb_lt : Real.exp (ℓ b) < Real.exp (ℓ a_star) := lt_of_le_of_lt hb_le hrest
  -- strip exp (Real.exp_lt_exp), then unfold the logits: ⟪W b, x⟫ < ⟪W a⋆, x⟫
  have hlt : ℓ b < ℓ a_star := Real.exp_lt_exp.mp hb_lt
  simpa [hℓ, gt_iff_lt] using hlt

end Decode
