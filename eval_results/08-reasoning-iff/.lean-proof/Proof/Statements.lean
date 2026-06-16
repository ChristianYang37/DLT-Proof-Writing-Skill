import Proof.Settings

/-!
# Statements

The two frozen, user-approved results of this development:

* `Decode.decode_iff_gradient_separation` — the main biconditional
  (decode ⟺ gradient separation), and
* `Decode.decode_iff_descent_separation_of_neg` — the `μ < 0` (constrained-minimum)
  descent-direction corollary.

Both are **stated and proved** in `Proof/Proofs/01-decode-iff.lean` (one file per result,
mirroring `sections/02-theorem-decode-iff.tex`). Their signatures are frozen in
`statement.lock`; `lean_lint.py --lock` enforces SL1 against the proof file.

This module is the import hub for the settings; it declares no theorems itself (the
signatures live with their proofs to keep the statement-lock keyed to a single site).
-/
