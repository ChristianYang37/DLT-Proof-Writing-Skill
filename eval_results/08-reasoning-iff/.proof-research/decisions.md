# Decisions log (blank_handling_protocol)

No slots were intentionally blank. The conservative, truth-seeking choices made:

## D1 — `gradient L x⋆` vs abstract gradient vector `g`
**Decision:** use the explicit `gradient L x⋆` (Mathlib `gradient` from
`Mathlib.Analysis.Calculus.Gradient.Basic`), with `L : E → ℝ` an explicit variable and the
hypothesis `hstat : gradient L x⋆ = μ • x⋆`.
**Why:** the invocation prefers the explicit gradient "if it goes through cleanly"; Phase-0
smoke confirmed it elaborates. This is strictly more faithful: the hypothesis literally
reads "the gradient of the loss L at x⋆ is parallel to x⋆" (ambient gradient normal to the
sphere ⟺ Riemannian gradient zero), which is exactly the constrained-stationarity NL
statement.
**Cost:** `gradient` requires `[CompleteSpace E]`. We add it as an instance assumption. It
is satisfied by `EuclideanSpace ℝ (Fin d)` (finite-dim ⇒ complete) and by any real Hilbert
space, so generality is preserved. The proof never differentiates L; `gradient L x⋆` is used
only as an opaque vector.

## D2 — `Differentiable ℝ L`: documented, NOT a theorem hypothesis (Occam)
**Decision:** record "L is differentiable" in `Settings.lean` as a doc-comment / an unused
`def` note, but do NOT put `Differentiable ℝ L` into the hypotheses of
`decode_iff_gradient_separation`.
**Why:** the proof does not use differentiability at all — it only uses the *value*
`gradient L x⋆` via `hstat`. Adding `Differentiable ℝ L` would be **hypothesis inflation**
(a hypothesis Lean never consumes), which Occam + the faithfulness reviewer treat as a
smell, and which would make the theorem *weaker* (it would hold for fewer reasons than it
actually does). Mathlib's `gradient` is total (defined as 0 off the differentiability locus),
so the statement is meaningful with or without differentiability; the honest, maximally
general statement omits it. The NL/LaTeX "L differentiable" is faithfully rendered as a
*setting remark*, not a load-bearing hypothesis. (Documented for the faithfulness reviewer.)

## D3 — keep `hnorm : ‖x⋆‖ = r` as a hypothesis even though the proof does not use it
**Decision:** KEEP `hr : 0 < r` and `hnorm : ‖x⋆‖ = r` in the theorem signature.
**Why:** these encode the LayerNorm-sphere membership `x⋆ ∈ sphere 0 r` — the physical
setting and part of the USER-FROZEN statement. Dropping them would be a silent statement
change (the protocol forbids that). The proof genuinely needs only `μ ≠ 0` (which already
forces `x⋆ ≠ 0` via `hstat`), so Lean will emit an `unused variable` linter note for `hnorm`
/ `hr`. That note is EXPECTED and HONEST here: we are faithfully transcribing the frozen
statement, which includes the sphere constraint, rather than minimizing hypotheses past the
agreed statement. This is the one place where we accept an unused hypothesis, precisely
because the user fixed the statement. Documented so the faithfulness reviewer does not flag
it as inflation and the Phase-F panel does not flag the linter note as a defect.
**Surfaced in Phase G.**

## D4 — the μ<0 corollary IS worth shipping
**Decision:** include `decode_iff_descent_separation_of_neg`.
**Why:** the invocation lists it as the "constrained-minimum case" reading and says "if
cheap" — it is one short rewrite from the main theorem (`μ<0 ⟹ μ*c>0 ↔ c<0 ↔ ⟪v,−g⟫>0`).
It is the physically meaningful specialization (descent direction `−∇L` better aligned with
the answer row than every competitor). Cheap + requested ⇒ include. Not adding any other
unrequested theorem (Occam).

## D5 — sign convention is FROZEN as `μ * ⟪W a⋆ − W b, ∇L(x⋆)⟫ > 0`
The Phase-0 smoke test PROVED the iff closes with EXACTLY this sign (no flip needed):
`⟪v, x⋆⟫ > 0 ↔ μ * ⟪v, gradient L x⋆⟫ > 0` under `gradient L x⋆ = μ • x⋆`. So the math
matches the frozen statement; no HALT-for-sign needed. (If it had required a flipped sign we
would HALT per constraint 2, not edit the statement.)

## D6 — citations: none
Self-contained algebra. No `refs.bib`, no `\cite`. (If the faithfulness/aesthetics reviewers
disagree, revisit — but there is no external theorem invoked.)
