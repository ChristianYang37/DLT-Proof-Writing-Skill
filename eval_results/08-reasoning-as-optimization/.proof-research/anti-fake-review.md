# Anti-fake reviewer (Phase D, before declaring VERIFIED)

`#print axioms` already certifies no hole / no custom axiom / no `native_decide` (closure =
{propext, Classical.choice, Quot.sound} for all three declarations). This adversarial pass
checks the things the axiom closure CANNOT catch.

## 1. Vacuity (hypotheses unsatisfiable ⇒ theorem trivially true)
**Verdict: NOT VACUOUS.** Witnesses in `Proof/Vacuity.lean` (all build green):
- The hypothesis bundle is jointly satisfiable by a concrete differentiable loss: on
  `E = ℝ`, `L x = x²` has `gradient L x⋆ = 2 • x⋆`; at `x⋆ = 1`, `r = 1`, `μ = 2` we have
  `‖x⋆‖ = 1 = r`, `gradient L x⋆ = μ • x⋆`, `μ ≠ 0`. (`example : gradient (fun x:ℝ=>x^2) 1 = 2•1`.)
- So the premises are met by a real (differentiable, sphere-constrained, constrained-stationary)
  model — the theorem is not over a contradictory hypothesis set.

## 2. Triviality / degeneracy of the conclusion predicate
**Verdict: NOT DEGENERATE.** `Generated W a x := ∀ b ≠ a, ⟪W a,x⟫ > ⟪W b,x⟫` is contingent —
witnessed both ways on `E = ℝ, V = Bool, W true = 1, W false = -1`:
- `Generated true (1:ℝ)` **holds** (`⟪1,1⟫ = 1 > -1 = ⟪-1,1⟫`).
- `Generated true (-1:ℝ)` **fails** (`⟪1,-1⟫ = -1 < 1 = ⟪-1,-1⟫`).
Both `example`s build. Hence neither side of the iff is constantly true or constantly false;
the biconditional has genuine content. (`Generated` is not `def _ := True`.)

## 3. Unsound instance / smuggled `decide`
**Verdict: CLEAN.** No new `instance`, no `@[instance]`, no `decide`/`native_decide` in the
proof (confirmed: `lean_lint.py` S5/S7/S8 silent; closure has no `Lean.ofReduceBool`). All
typeclass instances (`NormedAddCommGroup`, `InnerProductSpace ℝ`, `CompleteSpace`, `Fintype`,
`Nontrivial`) are Mathlib's standard ones, supplied as ordinary hypotheses/section variables.

## 4. Circularity
**Verdict: NONE.** The helper `sign_equiv` is pure real-field algebra (`positivity`,
`field_simp`, `nlinarith`), independent of the main theorem. `decode_iff_gradient_separation`
uses only `sign_equiv` + Mathlib inner-product lemmas. The corollary
`decode_iff_descent_separation_of_neg` invokes the main theorem (a legitimate downstream use,
not a cycle — the main theorem does not depend on the corollary). No declaration is proved
using itself.

## 5. Sign sanity (the frozen-sign guard, constraint 2)
The iff closes with EXACTLY the frozen sign `μ * ⟪W a⋆ − W b, gradient L x⋆⟫ > 0` — no flip
was needed (the Phase-0 smoke and the final proof both close with this orientation). The
corollary's `μ<0` rewrite preserves it (`μ*c>0 ⟺ c<0 ⟺ ⟪v,−g⟫>0`). No statement was edited
to match a proof.

## Conclusion (original two theorems)
0 unrebutted CRITICAL findings (vacuity / triviality / unsound instance / circularity). The
verification stands. Iterations: 1 (single adversarial pass; all checks passed first time
given the explicit witnesses).

---

# Anti-fake review — the two NEW theorems (this paper)

`#print axioms` certifies all FOUR delivered theorems have closure = {propext,
Classical.choice, Quot.sound} (no hole / no custom axiom / no native_decide). This pass
covers what the closure cannot.

## NEW (3) `decode_fails_iff_some_competitor`
- **Vacuity:** hypotheses are IDENTICAL to the main theorem (already shown satisfiable in
  `Proof/Vacuity.lean`). NOT vacuous.
- **Triviality:** `¬Generated` is contingent because `Generated` is contingent (both
  witnesses in Vacuity build). The `∃ b, b≠a⋆ ∧ (≤0)` side is the exact De Morgan dual of
  the main iff's `∀ b, b≠a⋆ → (>0)`; it is not constantly true/false. NOT trivial.
- **Circularity:** proved by `rw [decode_iff_gradient_separation …]; push_neg; rfl`. It is a
  legitimate downstream consequence of the main theorem (the main theorem does not depend on
  it). No cycle.
- **Smuggled tactics:** `push_neg` is a sound logical rewrite (De Morgan + `not_lt`); `rfl`
  closes a definitional equality. No `decide`, no new instance/simp/macro. CLEAN.
- **Sign sanity:** the failure side is `μ * ⟪W a⋆ − W b, gradient L x⋆⟫ ≤ 0` — the precise
  negation of the frozen `> 0`. No flip introduced.

## NEW (4) `decode_iff_softmax_residual`
- **Vacuity:** adds `(p : V→ℝ)` and `hgrad : ∇L = ∑_c (p_c−[c=a⋆])•W_c`. The danger is that
  `hgrad` could be unsatisfiable jointly with `hstat`, making the iff vacuously true. **Ruled
  out by a new explicit witness** (`Proof/Vacuity.lean`, item (4)): on `E=ℝ, V=Bool`,
  `W true=1, W false=-1`, `a⋆=true`, residual `p=(3,0)`, the sum `∑_c (p_c−[c=a⋆])•W_c = 2•1`,
  matching `gradient (x↦x²) 1 = 2•1`. So `hstat` (μ=2) and `hgrad` hold together. NOT vacuous.
- **Triviality:** the RHS is `μ·∑_c (p_c−[c=a⋆])(⟪W a⋆,W c⟫−⟪W b,W c⟫)`, a genuine
  Gram-matrix-weighted residual functional of `(W,p)` — not `True`, not a constant. `Generated`
  is contingent. NOT trivial.
- **Circularity:** proved by an inner-product identity `hexp` (distribute `inner_sum`, pull
  scalars `real_inner_smul_right`, expand `inner_sub_left`) + `rw [decode_iff_gradient_separation
  …]` + `forall_congr'`/`imp_congr_right`. Downstream consequence of the main theorem; no cycle.
- **Smuggled tactics / instances:** the only added instance is the *hypothesis* `[DecidableEq
  V]` (a benign typeclass to write the one-hot indicator; supplied as an instance ARGUMENT,
  not a new global `instance` declaration — so S8 does not fire and it cannot let a false fact
  synthesize). No `decide`, no `@[simp]`, no `native_decide`. The closure still has no
  `Lean.ofReduceBool`. CLEAN.
- **Sign sanity:** the RHS keeps the frozen `μ·(…) > 0` orientation; the residual sum *equals*
  `⟪W a⋆ − W b, ∇L⟫` under `hgrad`, so the sign is inherited verbatim from the main theorem.

## Combined conclusion (all four)
0 unrebutted CRITICAL findings across vacuity / triviality / unsound instance / circularity
for all four delivered theorems. The new `hgrad` satisfiability witness closes the only new
vacuity surface. Iterations: 1.
