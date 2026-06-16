import Proof.Statements

/-!
# Proof: decode ⟺ gradient separation (and the `μ < 0` descent corollary)

The biconditional is reduced pointwise over competitors `b ≠ a⋆`. Substituting
`x⋆ = μ⁻¹ • gradient L x⋆` (from stationarity, `μ ≠ 0`) turns each open-cone inequality
`⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫` into the signed alignment `μ * ⟪W a⋆ − W b, gradient L x⋆⟫ > 0`.

Mirrors `sections/02-theorem-decode-iff.tex` (the Lean module is named `DecodeIff` rather
than `01-decode-iff` because Lean module identifiers cannot contain hyphens; the section
file keeps the `NN-<slug>` convention and the `@lx` step ids are the join key for
`drift_check.py`, so file parity is preserved at the annotation level).
-/

open RealInnerProductSpace

namespace Decode

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
variable {V : Type*} [Fintype V] [Nontrivial V]

/- @lx step: lem:sign_equiv
   @lx kind: arith
   @lx latex: \mu^{-1} c > 0 \iff \mu c > 0
   @lx why: \mu^{-1}c and \mu c differ by the strictly positive factor \mu^2, so they share a sign
   @lx cite: -/
/-- **Sign equivalence.** For a nonzero multiplier `μ` and any real `c`, the quantities
`μ⁻¹ * c` and `μ * c` differ by the strictly positive factor `μ²`, hence are simultaneously
positive.

@lx step: lem:sign_equiv
-/
theorem sign_equiv {μ : ℝ} (hμ : μ ≠ 0) (c : ℝ) :
    μ⁻¹ * c > 0 ↔ μ * c > 0 := by
  -- μ² > 0
  -- @lx kind: internal
  have hsq : (0 : ℝ) < μ ^ 2 := by positivity
  -- clearing inverses: μ⁻¹ c · μ² = μ c
  -- @lx kind: internal
  have hid : μ⁻¹ * c * μ ^ 2 = μ * c := by field_simp
  constructor
  · intro hp
    nlinarith [mul_pos hp hsq, hid]
  · intro hp
    -- @lx kind: internal
    have hp' : (0 : ℝ) < μ * c * (μ ^ 2)⁻¹ := mul_pos hp (by positivity)
    -- @lx kind: internal
    have hid2 : μ * c * (μ ^ 2)⁻¹ = μ⁻¹ * c := by field_simp
    linarith [hid2 ▸ hp']

/-- **Main theorem — decode ⟺ gradient separation.**

Let `x⋆` lie on the LayerNorm sphere of radius `r` (`‖x⋆‖ = r`), suppose the implicit loss
is constrained-stationary at `x⋆` — the first-order/Lagrange condition
`gradient L x⋆ = μ • x⋆` — and let the multiplier be nonzero (`μ ≠ 0`). Then the designated
token `a⋆` is generated at `x⋆` (greedy argmax = true decoder) **iff** for every competitor
`b ≠ a⋆` the signed alignment `μ · ⟪W a⋆ − W b, gradient L x⋆⟫` is strictly positive.

@lx kind: named
@lx latex: \Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \mu\,\inner{W_{\astar} - W_b}{\grad\loss(\xstar)} > 0
@lx why: the main biconditional (theorem statement, rendered as the theorem environment)
@lx cite: --
@lx step: thm:main
-/
theorem decode_iff_gradient_separation
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star → μ * ⟪W a_star - W b, gradient L x_star⟫ > 0 := by
  -- name the (opaque) ambient gradient `g := gradient L x⋆`; the proof never differentiates
  -- L, and naming it prevents the stationarity rewrite from recursing into `gradient L x⋆`.
  set g : E := gradient L x_star with hg
  /- @lx step: thm:main.1
     @lx kind: arith
     @lx latex: \xstar = \mu^{-1}\,\grad\loss(\xstar)
     @lx why: rearrange the stationarity hypothesis \grad\loss(\xstar)=\mu\,\xstar using \mu \ne 0
     @lx cite: -/
  have hx : x_star = μ⁻¹ • g := by
    rw [hstat, smul_smul, inv_mul_cancel₀ hμ, one_smul]
  /- @lx step: thm:main.2
     @lx kind: arith
     @lx latex: \inner{W_{\astar}}{\xstar} > \inner{W_b}{\xstar} \iff \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} > 0
     @lx why: rewrite the cone gap as a single inner product (inner_sub_left, sub_pos), substitute \xstar=\mu^{-1}\grad\loss (thm:main.1) and pull the scalar out (real_inner_smul_right), then apply the sign equivalence (lem:sign_equiv)
     @lx cite: lem:sign_equiv -/
  have hpt : ∀ b, (⟪W a_star, x_star⟫ > ⟪W b, x_star⟫) ↔
      (μ * ⟪W a_star - W b, g⟫ > 0) := by
    intro b
    -- cone gap ⟺ positivity of the difference inner product
    -- @lx kind: internal
    have h1 : (⟪W a_star, x_star⟫ > ⟪W b, x_star⟫) ↔ (⟪W a_star - W b, x_star⟫ > 0) := by
      rw [inner_sub_left, gt_iff_lt, gt_iff_lt, sub_pos]
    -- difference inner product in gradient coordinates
    -- @lx kind: internal
    have h2 : ⟪W a_star - W b, x_star⟫ = μ⁻¹ * ⟪W a_star - W b, g⟫ := by
      rw [hx, real_inner_smul_right]
    rw [h1, h2]
    exact sign_equiv hμ _
  /- @lx step: thm:main.3
     @lx kind: named
     @lx latex: \Generated(\astar,\xstar) \iff \forall b \ne \astar,\ \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} > 0
     @lx why: unfold the decoder predicate and push the per-competitor equivalence (thm:main.2) under the universal quantifier over competitors b \ne \astar
     @lx cite: thm:main.2 -/
  show _ ↔ _   -- no-op; flush-trigger so the @lx step above is parsed by drift_check
  unfold Generated
  constructor
  · intro hgen b hb
    exact (hpt b).mp (hgen b hb)
  · intro hsep b hb
    exact (hpt b).mpr (hsep b hb)

/-- **Corollary (constrained minimum, `μ < 0`) — descent-direction separation.**

When the multiplier is negative (the constrained-*minimum* case), `a⋆` is generated at `x⋆`
iff the descent direction `−gradient L x⋆` is strictly better aligned with the answer's row
than with every competitor's row: `∀ b ≠ a⋆, ⟪W a⋆ − W b, −gradient L x⋆⟫ > 0`.

@lx kind: named
@lx latex: \Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \inner{W_{\astar} - W_b}{-\grad\loss(\xstar)} > 0
@lx why: the descent-direction corollary (statement, rendered as the corollary environment)
@lx cite: --
@lx step: cor:neg
-/
theorem decode_iff_descent_separation_of_neg
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ < 0) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star → ⟪W a_star - W b, -gradient L x_star⟫ > 0 := by
  /- @lx step: cor:neg.1
     @lx kind: named
     @lx latex: \Generated(\astar,\xstar) \iff \forall b \ne \astar,\ \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} > 0
     @lx why: instantiate the main theorem at this x⋆, μ, r (using μ \ne 0 from μ < 0)
     @lx cite: thm:main -/
  have hmain := decode_iff_gradient_separation W L x_star a_star μ r hr hnorm hstat (ne_of_lt hμ)
  rw [hmain]
  /- @lx step: cor:neg.2
     @lx kind: arith
     @lx latex: \mu\,\inner{v}{\grad\loss(\xstar)} > 0 \iff \inner{v}{-\grad\loss(\xstar)} > 0
     @lx why: with μ < 0, \mu c > 0 \iff c < 0 \iff -c > 0; and \inner{v}{-\grad\loss(\xstar)} = -\inner{v}{\grad\loss(\xstar)} (inner_neg_right)
     @lx cite: -/
  show _ ↔ _   -- no-op; flush-trigger so the @lx step above is parsed by drift_check
  refine forall_congr' (fun b => ?_)
  refine imp_congr_right (fun _ => ?_)
  rw [inner_neg_right]
  constructor
  · intro hpos
    nlinarith [mul_pos_iff.mp hpos]
  · intro hpos
    nlinarith [mul_pos_of_neg_of_neg hμ
      (by linarith : ⟪W a_star - W b, gradient L x_star⟫ < 0)]

/-- **Corollary (failure characterization) — decode fails ⟺ a competitor wins.**

The contrapositive of the main theorem. Under the same hypotheses (sphere membership,
stationarity, `μ ≠ 0`), the designated token `a⋆` is **not** generated at `x⋆` iff some
competitor `b ≠ a⋆` defeats it in signed alignment: `μ · ⟪W a⋆ − W b, gradient L x⋆⟫ ≤ 0`.
This is the exact "when does reasoning fail" boundary — a single bad competitor suffices.

@lx kind: named
@lx latex: \neg\,\Generated(\astar, \xstar) \iff \exists b \ne \astar,\ \mu\,\inner{W_{\astar} - W_b}{\grad\loss(\xstar)} \le 0
@lx why: the failure characterization (statement, rendered as the corollary environment)
@lx cite: --
@lx step: cor:fail
-/
theorem decode_fails_iff_some_competitor
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0) :
    ¬ Generated W a_star x_star ↔
      ∃ b, b ≠ a_star ∧ μ * ⟪W a_star - W b, gradient L x_star⟫ ≤ 0 := by
  /- @lx step: cor:fail.1
     @lx kind: arith
     @lx latex: \neg\,\Generated(\astar,\xstar) \iff \exists b \ne \astar,\ \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} \le 0
     @lx why: negate the main iff (thm:main); pushing the negation through \forall and the strict inequality turns \neg\forall b\,(b\ne\astar\to c_b>0) into \exists b\,(b\ne\astar\wedge c_b\le 0)
     @lx cite: thm:main -/
  rw [decode_iff_gradient_separation W L x_star a_star μ r hr hnorm hstat hμ]
  show _ ↔ _   -- no-op; flush-trigger so the @lx step above is parsed by drift_check
  push_neg
  rfl

/-- **Corollary (cross-entropy instantiation) — softmax-residual separation.**

Specialize the gradient to the literal cross-entropy form `∇L = Wᵀ(p − e_{a⋆})`, written as
the vocabulary sum `gradient L x⋆ = ∑_c (p c − [c = a⋆]) • W c`, where `p : V → ℝ` is the
softmax probability vector and `e_{a⋆}` is the one-hot target. Under the same stationarity
and `μ ≠ 0`, `a⋆` is generated at `x⋆` iff, for every competitor `b ≠ a⋆`, the
`μ`-signed **softmax-residual separation score** is strictly positive:
`μ · ∑_c (p c − [c = a⋆]) (⟪W a⋆, W c⟫ − ⟪W b, W c⟫) > 0`.

The softmax-residual gradient form is taken as a hypothesis (`hgrad`); we do **not**
differentiate log-sum-exp here — we only rewrite the alignment functional through it.

@lx kind: named
@lx latex: \Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \mu \sum_{c} \bigl(p_c - \indicator{c = \astar}\bigr)\bigl(\inner{W_{\astar}}{W_c} - \inner{W_b}{W_c}\bigr) > 0
@lx why: the cross-entropy instantiation (statement, rendered as the corollary environment)
@lx cite: --
@lx step: cor:ce
-/
theorem decode_iff_softmax_residual [DecidableEq V]
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ) (p : V → ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0)
    (hgrad : gradient L x_star = ∑ c, (p c - (if c = a_star then 1 else 0)) • W c) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star →
        μ * (∑ c, (p c - (if c = a_star then 1 else 0)) *
              (⟪W a_star, W c⟫ - ⟪W b, W c⟫)) > 0 := by
  /- @lx step: cor:ce.1
     @lx kind: arith
     @lx latex: \inner{W_{\astar}-W_b}{\grad\loss(\xstar)} = \sum_{c}\bigl(p_c-\indicator{c=\astar}\bigr)\bigl(\inner{W_{\astar}}{W_c}-\inner{W_b}{W_c}\bigr)
     @lx why: substitute the softmax-residual gradient (hgrad), distribute the inner product over the vocabulary sum (inner_sum), pull each scalar out (real_inner_smul_right) and expand the gap inner product (inner_sub_left) termwise (Finset.sum_congr)
     @lx cite: hgrad -/
  have hexp : ∀ b, ⟪W a_star - W b, gradient L x_star⟫ =
      ∑ c, (p c - (if c = a_star then 1 else 0)) *
            (⟪W a_star, W c⟫ - ⟪W b, W c⟫) := by
    intro b
    rw [hgrad, inner_sum]
    refine Finset.sum_congr rfl (fun c _ => ?_)
    rw [real_inner_smul_right, inner_sub_left]
  /- @lx step: cor:ce.2
     @lx kind: named
     @lx latex: \Generated(\astar,\xstar) \iff \forall b \ne \astar,\ \mu \sum_{c}\bigl(p_c-\indicator{c=\astar}\bigr)\bigl(\inner{W_{\astar}}{W_c}-\inner{W_b}{W_c}\bigr) > 0
     @lx why: rewrite each per-competitor alignment in the main iff (thm:main) by the residual-sum identity (cor:ce.1) under the universal quantifier over competitors b \ne \astar
     @lx cite: thm:main, cor:ce.1 -/
  rw [decode_iff_gradient_separation W L x_star a_star μ r hr hnorm hstat hμ]
  show _ ↔ _   -- no-op; flush-trigger so the @lx step above is parsed by drift_check
  refine forall_congr' (fun b => ?_)
  refine imp_congr_right (fun _ => ?_)
  rw [hexp b]

end Decode
