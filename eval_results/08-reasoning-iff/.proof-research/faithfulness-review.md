# Phase-B faithfulness review

Task (verbatim from lean-workflow.md §Faithfulness reviewer): compare the FORMAL Lean
statement against the INTENDED mathematical statement and detect HIDDEN WEAKENINGS — ways
the Lean says LESS than, or something DIFFERENT from, the math. The proof was NOT consulted
(only the signatures). Every custom predicate is unfolded below.

## INTENDED statement (NL + LaTeX), user-approved

**NL.** Let `E` be a real inner product space, `V` a finite vocabulary with ≥ 2 tokens,
`W : V → E` the unembedding (rows `W a`), `r > 0` the LayerNorm-sphere radius, `L` a
differentiable implicit loss. Given `x⋆` with `‖x⋆‖ = r`, the stationarity hypothesis
`∇L(x⋆) = μ·x⋆`, and `μ ≠ 0`, then for a designated token `a⋆`:

> (`a⋆` is generated at `x⋆`)  ↔  (∀ `b ≠ a⋆`,  `μ · ⟪W a⋆ − W b, ∇L(x⋆)⟫ > 0`),

where "`a⋆` is generated at `x⋆`" means `∀ b ≠ a⋆, ⟪W a⋆, x⋆⟫ > ⟪W b, x⋆⟫` (greedy argmax =
true decoder, single-token). Corollary for `μ < 0`: generated ⟺ `∀ b ≠ a⋆, ⟪W a⋆ − W b,
−∇L(x⋆)⟫ > 0`.

**LaTeX.** `\Generated(\astar,\xstar) \iff \forall b\ne\astar,\ \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} > 0`.

## FORMAL statement (Lean signatures)

```lean
def Generated (W : V → E) (a : V) (x : E) : Prop :=
  ∀ b, b ≠ a → ⟪W a, x⟫ > ⟪W b, x⟫            -- ⟪·,·⟫ = real inner product, open cone

theorem decode_iff_gradient_separation
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star → μ * ⟪W a_star - W b, gradient L x_star⟫ > 0

theorem decode_iff_descent_separation_of_neg
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ < 0) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star → ⟪W a_star - W b, -gradient L x_star⟫ > 0
```
Ambient: `[NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]`,
`[Fintype V] [Nontrivial V]`.

## Divergence checks (the 6 mandated)

**1. Quantifier order (∀∃ vs ∃∀).**
- `Generated`: math `∀ b ≠ a⋆, …` ↔ Lean `∀ b, b ≠ a_star → …`. Identical (the guard `b ≠ a`
  is the standard encoding of "for all competitors"). ✅
- RHS of iff: math `∀ b ≠ a⋆, μ·⟪…⟫ > 0` ↔ Lean `∀ b, b ≠ a_star → μ * ⟪…⟫ > 0`. Identical. ✅
- The iff itself is a single `↔`, no hidden ∃/∀ swap. The multiplier `μ` is a *parameter*
  (universally bound in the theorem statement, supplied by `hstat`), matching "given … the
  stationarity hypothesis `∇L(x⋆)=μ·x⋆`". No ∃ collapsed to ∀ or vice versa. ✅

**2. Missing conclusion conjuncts.** The conclusion is a single `↔`. Both directions are
present (an `↔` is symmetric; nothing dropped). The math statement is exactly one
biconditional. No `A∧B` reduced to `A`. ✅

**3. Hypothesis inflation (Lean hyp absent from math = weaker).**
- `hr : 0 < r`, `hnorm : ‖x_star‖ = r`: PRESENT in the math ("Given x⋆ with ‖x⋆‖=r",
  "r > 0"). Not inflation. (They happen to be unused by the proof — see decisions.md D3 —
  but they ARE in the intended statement, so keeping them is faithful, not inflationary. An
  unused-but-intended hypothesis does not weaken the theorem relative to the *intended*
  statement; it would only be a smell if it were absent from the math.) ✅
- `hstat`, `hμ`: PRESENT in the math. ✅
- `[CompleteSpace E]`: NOT explicitly in the math, BUT it is forced by the use of the
  Mathlib `gradient` symbol (which the math's `∇L(x⋆)` denotes). It is satisfied by
  `EuclideanSpace ℝ (Fin d)` and every real Hilbert space, i.e. by every model the math
  intends. Technically this is a mild hypothesis the bare NL omits. **Assessment:** this is
  the standard, unavoidable cost of formalizing "the gradient ∇L" with Mathlib's total
  `gradient`; it does not change the mathematical content over the intended models. It is
  the only candidate for "inflation" and it is benign + documented. Recorded as a NOTE, not
  a divergence — the alternative (an abstract `g` with no completeness) was considered and
  the explicit `gradient` was preferred for faithfulness (decisions.md D1). NOT flagged
  WEAKER because no intended model is excluded.
- `[Fintype V] [Nontrivial V]`: "finite vocabulary with at least 2 tokens" — PRESENT in the
  math setting. Faithful. ✅
- `Differentiable ℝ L`: deliberately ABSENT from hypotheses (decisions.md D2). The math
  says "L differentiable" as setting flavor, but the theorem is TRUE and meaningful without
  it (Mathlib `gradient` is total). Omitting a hypothesis makes the theorem STRONGER, never
  weaker — so this cannot be a hidden weakening. The intended biconditional still holds.
  This is the correct Occam direction. ✅ (Surfaced to user in Phase G.)

**4. Conclusion deflation (≤ for =, big-O for exact, Nonempty for witness, True tail).**
- The conclusion is a strict-inequality biconditional with `> 0` on the signed alignment —
  EXACTLY the math's `μ · ⟪W a⋆ − W b, ∇L(x⋆)⟫ > 0`. No `≥` softening, no `≠ 0` weakening,
  no `True` tail. ✅
- SIGN: Lean has `μ * ⟪W a_star - W b, gradient L x_star⟫ > 0`. Math has
  `μ · ⟪W a⋆ − W b, ∇L(x⋆)⟫ > 0`. The vector inside is `W a⋆ − W b` (answer row minus
  competitor row), the multiplier is `μ` (not `μ⁻¹`, not `−μ`, not `μ²`), the relation is
  `> 0`. **Exact sign match — the frozen sign is preserved.** ✅
- Corollary: `⟪W a_star - W b, -gradient L x_star⟫ > 0` = math `⟪W a⋆ − W b, −∇L(x⋆)⟫ > 0`,
  with the extra hyp `μ < 0`. Exact. ✅

**5. Definition degeneracy (unfold each custom predicate; find a degenerate model).**
- Only custom predicate: `Generated W a x := ∀ b, b ≠ a → ⟪W a, x⟫ > ⟪W b, x⟫`. This is the
  open decoding cone, NOT `True` and NOT vacuous: with `Nontrivial V` there exists `b ≠ a`,
  so the predicate imposes a real strict inequality (it can fail — e.g. `W` constant makes
  `⟪W a,x⟫ = ⟪W b,x⟫`, so `Generated` is false there). Non-degenerate. ✅
- Could the iff be vacuously true (both sides always false / always true)? No: take
  `W a⋆` large positive multiple of `x⋆` and `W b = 0` — then LHS holds; take `W a⋆ = W b`
  — LHS fails. Both sides are genuinely contingent. (A concrete witness `example` will be
  built in Phase D for the anti-fake/vacuity gate.) ✅

**6. Type mismatch (ℕ/ℤ/ℝ, Finset/Set, strict/non-strict).**
- `μ, r : ℝ`; inner products real (`⟪·,·⟫_ℝ : ℝ`); `> 0` is strict on `ℝ` — matches math. ✅
- `‖x_star‖ = r` is real-valued norm equality — matches. ✅
- `V` finite via `Fintype` (the math's "finite vocabulary") — matches; not a `Finset`/`Set`
  confusion (V is the type of tokens). ✅
- `b ≠ a_star` is decidable-eq-free `Ne` on the type `V` — matches "b ≠ a⋆". ✅

## VERDICT: **FAITHFUL**

Divergence table (math side | Lean side | which stronger): **EMPTY** — no WEAKER, no
DIFFERENT divergence found.

Two benign, fully-documented NOTES (neither weakens the theorem vs the intended models):
1. `[CompleteSpace E]` is forced by Mathlib `gradient`; satisfied by all intended models
   (EuclideanSpace / Hilbert). Standard formalization cost, not a weakening.
2. `Differentiable ℝ L` is intentionally omitted as a hypothesis (the theorem is strictly
   more general without it; Mathlib `gradient` is total). Omission ⇒ stronger, never weaker.
   The NL "L differentiable" is rendered as a setting remark in the LaTeX, not a hypothesis.

Both notes are surfaced to the user in the Phase-G report and in `decisions.md`.
The frozen SIGN (`μ * ⟪W a⋆ − W b, ∇L(x⋆)⟫ > 0`) is preserved exactly.
