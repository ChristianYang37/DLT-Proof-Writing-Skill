# Scope declaration

Standard

## Rationale

- **Result count:** one main theorem (`decode_iff_gradient_separation`, an iff) plus one
  cheap corollary (`decode_iff_descent_separation_of_neg`, the μ<0 specialization). That is
  one theorem-like result + one corollary — within the Standard band (1–3 lemmas + ≤ 1
  theorem), above Quick.
- **Derivation steps:** the proof of the main iff is a pointwise-over-`b` chain with ~5–7
  named sub-steps (rewrite stationarity → express ⟪v,x⋆⟫ via the gradient → sign
  equivalence via μ²>0 → unfold `Generated`). This is > 5 steps, so it exceeds the Quick
  ceiling.
- **No probability:** there is NO probability parameter δ, NO asymptotics, NO expectation.
  Pure inner-product geometry + a first-order optimality hypothesis. (This is why it is not
  Appendix either — no concentration, no induction, no multi-lemma dependency web.)

Quick was deliberately NOT chosen: Quick skips Phase C.5 (confidence sweep) and is the
most-abused escape hatch. Standard runs the full sweep + Phase D verification loop, which is
appropriate here even though the math is elementary — the value is the machine-checked
guarantee and the faithful sign.

## Consequences (per check_scope.py / SKILL.md)

- Confidence sweep (Phase C.5) is MANDATORY.
- Review panel sized for Standard.
- Lean verification mandatory for every tier (unchanged).
