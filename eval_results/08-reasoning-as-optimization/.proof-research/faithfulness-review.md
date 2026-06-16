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

---

# New signatures (this paper) — faithfulness review of the two ADDED theorems

The two theorems above (`decode_iff_gradient_separation`, `decode_iff_descent_separation_of_neg`)
are carried over BYTE-FOR-BYTE from `08-reasoning-iff` and were already user-approved; their
`statement.lock` hashes are unchanged. The faithfulness reviewer was re-run **only on the two
NEW signatures**, per the Phase-B protocol (compare FORMAL Lean ↔ INTENDED math; the proofs
were not consulted). Every custom predicate (`Generated`) is unfolded as above.

## NEW (3) `decode_fails_iff_some_competitor` — failure characterization

**INTENDED (NL).** Under the same setting and hypotheses as the main theorem (sphere
membership `‖x⋆‖=r`, `r>0`, stationarity `∇L(x⋆)=μ·x⋆`, `μ≠0`): the designated token `a⋆`
is **not** generated at `x⋆` **iff** some competitor `b≠a⋆` defeats it in signed alignment,
`μ·⟪W a⋆−W b, ∇L(x⋆)⟫ ≤ 0`. (The contrapositive / De Morgan dual of the main iff.)

**INTENDED (LaTeX).**
`\neg\,\Generated(\astar,\xstar) \iff \exists b\ne\astar,\ \mu\,\inner{W_{\astar}-W_b}{\grad\loss(\xstar)} \le 0`.

**FORMAL (Lean).**
```lean
theorem decode_fails_iff_some_competitor
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0) :
    ¬ Generated W a_star x_star ↔
      ∃ b, b ≠ a_star ∧ μ * ⟪W a_star - W b, gradient L x_star⟫ ≤ 0
```

1. **Quantifier order.** LHS negates `Generated` (a `∀`); RHS is `∃ b, b≠a⋆ ∧ …`. This is the
   exact De Morgan dual of the main iff's `∀ b, b≠a⋆ → (…>0)`: `¬∀ → ∃`, and the guard
   `b≠a⋆` moves from an implication antecedent to a conjunct. The failure side is correctly
   existential ("SOME competitor wins"). No spurious ∃-for-∀ swap. ✅
2. **Missing conjuncts.** RHS is `b≠a⋆ ∧ (≤0)` — both conjuncts present (this is exactly the
   negation of `b≠a⋆ → (>0)`). ✅
3. **Hypothesis inflation.** Hypotheses are IDENTICAL to the main theorem (`hr, hnorm, hstat,
   hμ`); none added. The same two benign NOTES carry over (`CompleteSpace E` forced by
   `gradient`; `hr, hnorm` intended-but-unused). No new inflation. ✅
4. **Conclusion deflation.** The failure side uses NON-strict `≤ 0`. This is NOT a softening
   of an intended `<`: De Morgan of the strict `c > 0` is exactly `c ≤ 0`. The sign and the
   relation are the precise logical negation of the main theorem's `> 0`. No `True` tail. ✅
5. **Definition degeneracy.** `Generated` is contingent (witnesses in `Proof/Vacuity.lean`:
   a model where it holds, one where it fails); hence `¬Generated` is contingent too. Both
   sides are genuinely contingent, not vacuous. ✅
6. **Type mismatch.** `≤` strict-vs-nonstrict on `ℝ`; `∃ b : V`; real inner product. All
   match. ✅

**VERDICT: FAITHFUL.** It is the exact De Morgan dual of the user-approved main iff. Empty
divergence table.

## NEW (4) `decode_iff_softmax_residual` — cross-entropy / softmax-residual instantiation

**INTENDED (NL).** Under the same setting and hypotheses (sphere membership, stationarity,
`μ≠0`) AND the specialization that the gradient is the cross-entropy / softmax-residual form
`∇L(x⋆) = ∑_c (p_c − [c=a⋆]) W_c` (i.e. `∇L = Wᵀ(p − e_{a⋆})`, the literal cross-entropy
gradient with `p` the softmax probability vector and `e_{a⋆}` the one-hot target): `a⋆` is
generated at `x⋆` **iff** for every competitor `b≠a⋆`, the `μ`-signed softmax-residual
separation score is strictly positive,
`μ·∑_c (p_c − [c=a⋆])(⟪W a⋆,W c⟫ − ⟪W b,W c⟫) > 0`.

**INTENDED (LaTeX).**
`\Generated(\astar,\xstar) \iff \forall b\ne\astar,\ \mu\sum_c(p_c-\indicator{c=\astar})(\inner{W_{\astar}}{W_c}-\inner{W_b}{W_c}) > 0`.

**FORMAL (Lean).**
```lean
theorem decode_iff_softmax_residual [DecidableEq V]
    (W : V → E) (L : E → ℝ) (x_star : E) (a_star : V) (μ : ℝ) (r : ℝ) (p : V → ℝ)
    (hr : 0 < r) (hnorm : ‖x_star‖ = r)
    (hstat : gradient L x_star = μ • x_star) (hμ : μ ≠ 0)
    (hgrad : gradient L x_star = ∑ c, (p c - (if c = a_star then 1 else 0)) • W c) :
    Generated W a_star x_star ↔
      ∀ b, b ≠ a_star →
        μ * (∑ c, (p c - (if c = a_star then 1 else 0)) *
              (⟪W a_star, W c⟫ - ⟪W b, W c⟫)) > 0
```

1. **Quantifier order.** `∀ b, b≠a⋆ → (…>0)` — same outer ∀-over-competitors as the main iff.
   The inner `∑ c` is `Finset.sum Finset.univ` over the (finite) vocabulary `V`; it is a
   *term*, not a quantifier, matching "∑ over the vocabulary". No ∀/∃ swap. ✅
2. **Missing conjuncts.** Conclusion is a single strict inequality `> 0`; no dropped
   conjunct. ✅
3. **Hypothesis inflation.** Adds `(p : V→ℝ)`, `(hgrad : ∇L = ∑_c (p_c−[c=a⋆])•W_c)`, and the
   instance `[DecidableEq V]`. Assessment:
   - `p` and `hgrad` are the **defining specialization** of this corollary — they ARE the
     cross-entropy hypothesis, not covert weakenings of an unconditional claim. The theorem is
     explicitly "the iff *for the cross-entropy gradient form*"; `hgrad` is the intended
     antecedent. ✅
   - `[DecidableEq V]` is a benign typeclass needed merely to *write* the one-hot indicator
     `[c=a⋆] = if c=a_star then 1 else 0`. Every finite vocabulary has decidable token
     equality; it excludes no intended model. Recorded as a NOTE (analogous to `CompleteSpace
     E`), not a weakening. ✅
   These are intended hypotheses of a specialization; they do not weaken the result relative
   to its intended (cross-entropy) statement.
4. **Conclusion deflation.** Strict `> 0`, matching the main theorem's strict separation
   (the residual sum equals `⟪W a⋆−W b, ∇L⟫` exactly under `hgrad`, so no strength is lost
   in the rewrite). No `≥`, no `True` tail. ✅
5. **Definition degeneracy.** `Generated` contingent (as above). The RHS is a genuine
   bilinear functional of `W` and `p` (a Gram-matrix-weighted residual), not `True`/vacuous;
   `hgrad` is satisfiable (e.g. choose `L` whose gradient at `x⋆` equals that sum). ✅
6. **Type mismatch.** `∑ c` over `Finset.univ : Finset V`; `[c=a⋆]` is `(1:ℝ)`/`(0:ℝ)`;
   `μ * (∑…)` real; `⟪·,·⟫_ℝ : ℝ`; `> 0` strict on `ℝ`. All match. ✅

**VERDICT: FAITHFUL.** It is the cross-entropy/softmax specialization of the user-approved
main iff; the added hypotheses (`p`, `hgrad`) are the defining specialization and
`[DecidableEq V]` is a benign decidability instance. Empty divergence table.

## Combined verdict for the two new signatures

Both NEW signatures: **FAITHFUL**, empty divergence tables. They are *logical consequences*
of the already-approved main iff (a De Morgan dual; a substitution specialization), preserving
its exact sign convention `μ·⟪W a⋆−W b, ∇L⟫`. No quantifier swap, no conclusion deflation, no
degeneracy. One benign NOTE specific to (4): `[DecidableEq V]` to express the one-hot target.

---

# NEW (5) `loss_below_log2_decodes` — the loss-to-margin BRIDGE (2nd layer)

The faithfulness reviewer was run on the NEW bridge signature only (compare FORMAL Lean ↔
INTENDED math; the proof was NOT consulted). `Generated` is unfolded as above; `lossCE` is
unfolded below.

## INTENDED statement (NL + LaTeX)

**NL.** Let `E` be a real inner product space, `V` a finite vocabulary with ≥ 2 tokens,
`W : V → E` the unembedding. Define the single-token cross-entropy loss
`L(x) = log(∑_c exp⟪W c, x⟫) − ⟪W a⋆, x⟫` (= −log of the softmax probability of `a⋆`). Then:

> if `L(x) < log 2` (equivalently, the softmax mass on `a⋆` exceeds `1/2`), the greedy
> decoder outputs `a⋆`, i.e. `∀ b ≠ a⋆, ⟪W a⋆, x⟫ > ⟪W b, x⟫`.

**LaTeX.** `\loss(x) < \log 2 \implies \Generated(\astar, x)`, where
`\loss(x) = \log\bigl(\sum_c \exp\inner{W_c}{x}\bigr) - \inner{W_{\astar}}{x}`.

## FORMAL statement (Lean)

```lean
noncomputable def lossCE [Fintype V] (W : V → E) (a_star : V) (x : E) : ℝ :=
  Real.log (∑ c, Real.exp ⟪W c, x⟫) - ⟪W a_star, x⟫

theorem loss_below_log2_decodes [DecidableEq V]
    (W : V → E) (x : E) (a_star : V)
    (hlow : Real.log (∑ c, Real.exp ⟪W c, x⟫) - ⟪W a_star, x⟫ < Real.log 2) :
    Generated W a_star x
```
Ambient: `[NormedAddCommGroup E] [InnerProductSpace ℝ E]`, `[Fintype V] [Nontrivial V]`.

## Divergence checks (the 6 mandated)

**1. Quantifier order.** Conclusion `Generated W a⋆ x` = `∀ b, b ≠ a_star → ⟪W a⋆,x⟫ > ⟪W b,x⟫`
— identical to the math's `∀ b ≠ a⋆`. The hypothesis `hlow` is quantifier-free (a single real
inequality). No ∀/∃ swap. ✅

**2. Missing conjuncts.** Conclusion is one universally-quantified strict inequality; the
hypothesis is one inequality. Nothing dropped. ✅

**3. Hypothesis inflation.** Hypotheses: `W, x, a_star, hlow, [DecidableEq V], [Fintype V],
[Nontrivial V]`.
- `hlow` is EXACTLY the intended loss bound (the unfolded `lossCE W a_star x < Real.log 2`;
  `lossCE` is definitionally this expression). It is the defining antecedent, not a covert
  restriction. ✅
- `[Fintype V]` is intrinsic — the partition sum `∑_c exp⟪W c,x⟫` is over the finite
  vocabulary; cross-entropy is only defined for a finite (here) token set. Present in the
  standing setting (§1). ✅
- `[Nontrivial V]` is intrinsic — ≥ 2 tokens is the standing setting; it makes `univ`
  nonempty (so `Z > 0`) and guarantees competitors exist. A 1-token vocabulary is excluded by
  the intended setting itself. ✅
- `[DecidableEq V]` is a benign decidability instance (already used by
  `decode_iff_softmax_residual`), needed only to form `univ.erase a⋆` in the proof. Every
  finite vocabulary has it; excludes no intended model. Recorded as a NOTE (analogous to
  `CompleteSpace E` / the softmax corollary's `[DecidableEq V]`), not a weakening. ✅
None of these is a mathematically restrictive inflation; they encode the finite-vocabulary
setting that the existing four theorems already assume.

**4. Conclusion deflation.** Conclusion is the EXACT decoder predicate `Generated` with strict
`>` — no `≥` softening, no `Nonempty`, no `True` tail. The hypothesis uses strict `<` matching
"below log 2". The threshold is `Real.log 2` exactly (not `log 2 − ε`, not a `≤`). ✅

**5. Definition degeneracy.** Two custom symbols:
- `Generated` — contingent (Vacuity (2): holds at x=1, fails at x=−1). Not `True`. ✅
- `lossCE` — the genuine `−log p_{a⋆}` (log-partition minus the answer logit), not `True`/
  constant. ✅
- Is `hlow` vacuously false (making the theorem vacuously true)? NO: Vacuity (5b) exhibits a
  concrete model (`E=ℝ`, `V=Bool`, `W true=1, W false=0`, `x=1`) where the premise HOLDS
  (`e+1 < 2e` ⟹ `L(1) < log 2`); Vacuity (5a) exhibits the boundary (`L = log 2`, premise
  FAILS). So the premise is satisfiable AND contingent — non-vacuous and non-trivial. ✅

**6. Type mismatch.** `Real.log`, `Real.exp`, `⟪·,·⟫_ℝ : ℝ`, threshold `Real.log 2 : ℝ`;
strict `<` and `>` on `ℝ`. `∑ c` is `Finset.sum Finset.univ` over the finite `V` (matches "sum
over the vocabulary"). No ℕ/ℤ/ℝ or Finset/Set confusion. ✅

## VERDICT: **FAITHFUL**

Divergence table (math | Lean | which stronger): **EMPTY**. One benign NOTE: `[DecidableEq V]`
is a decidability instance used only to write `univ.erase a⋆`; it excludes no intended model
(same status as in the softmax corollary). The hypothesis is stated on the *unfolded* loss
(definitionally `lossCE W a_star x`), which is faithful and self-contained; the LaTeX renders
it as `L(x) < log 2` and notes the identity `L(x) = lossCE W a_star x`. The threshold `log 2`
and the strict inequalities are preserved exactly.
