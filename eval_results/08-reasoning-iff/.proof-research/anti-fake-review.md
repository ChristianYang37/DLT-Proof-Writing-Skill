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

## Conclusion
0 unrebutted CRITICAL findings (vacuity / triviality / unsound instance / circularity). The
verification stands. Iterations: 1 (single adversarial pass; all checks passed first time
given the explicit witnesses).
