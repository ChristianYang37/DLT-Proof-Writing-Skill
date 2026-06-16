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

## D6 — citations: none (REVISED by D8 for the 2nd layer)
Self-contained algebra for the iff base (§2–§3). No `\cite` there. The 2nd layer (§4 B2) DOES
invoke one external theorem and ships `refs.bib` + a digest; see D8.

## D7 — 2nd layer: the loss-to-margin BRIDGE is the verified link (NEW)
**Decision:** add ONE Lean-verified theorem, `Decode.loss_below_log2_decodes`
(`Bridge.lean`): `L(x) = log(∑_c exp⟪W c,x⟫) − ⟪W a⋆,x⟫ < log 2 ⟹ Generated W a⋆ x`, with the
single-token cross-entropy `def lossCE` added to `Settings.lean`.
**Why:** it is the analytic bridge from the loss VALUE to decoding — it connects the verified iff
(WHICH token a stationary point decodes) to the convergence-rate story (HOW FAST the loss drops).
The threshold `log 2` is exact: `L(x) < log 2 ⟺ p_{a⋆}(x) > 1/2`, and mass > 1/2 beats the
combined competitor mass. Proof is pure log/exp algebra over a finite nonempty sum (light
Mathlib: `Real.exp_pos`, `Finset.sum_pos`, `Real.log_mul`, `Real.log_exp`, `Real.log_lt_log_iff`,
`Finset.add_sum_erase`, `Finset.single_le_sum`, `Real.exp_lt_exp`); all lemma names verified
present in the pinned Mathlib (v4.30.0) before writing. The loss is never differentiated.
**Cost:** `[DecidableEq V]` added to the signature (benign decidability instance, needed only to
form `univ.erase a⋆`; already used by `decode_iff_softmax_residual`). Recorded as a NOTE in the
faithfulness review, not a weakening. The existing four signatures are UNTOUCHED (SL1 unchanged).

## D8 — the verified/cited SPLIT in §4 (truth-seeking boundary) (NEW)
**Decision:** §4 has two explicitly separated parts. **B1 (verified):** the bridge lemma, rendered
🔵 with `% @lx-from` provenance and drift-checked. **B2 (classical, cited — NOT verified):** the
dynamics/rate/probability story under the model "reasoning = gradient descent on the convex loss
`L`". Every B2 claim is either CITED or labeled classical/exposition; NONE carries `@lx-from`;
NONE is tagged 🔵.
**Why:** the smooth-convex GD rate and its decode-time/probability corollaries are genuine
convex-optimization theory, not something we machine-checked. Honesty-over-output requires the
boundary to be unmistakable. We therefore (i) open §4 with a boxed disclaimer, (ii) open B2 with
an explicit "cited, not machine-verified" sentence, (iii) cite Bubeck (2015) Theorem 3.3 for the
rate via the R5 `[\cite{}]` bracket (no local proof), (iv) give the decode-time corollary a SHORT
proof for transparency but flag it "cited-not-verified" in `rem:cor-not-verified` and withhold any
`@lx-from`/🔵 from it, (v) keep the structural-success and probability statements as exposition
tying back to the verified geometry (the iff is the exact necessary-and-sufficient boundary).
**Citation honesty (R13):** shipped `refs.bib` (key `bubeck2015`) + digest
`.proof-research/cite-bubeck2015-gd-smooth-convex-rate.md` with the EXACT theorem number
(Theorem 3.3, §3.2, p. 267) and the EXACT constant `2β‖x₁−x⋆‖²/(t−1)` as printed in the source —
we render Bubeck's exact constant (not the looser textbook `β‖x₀−x⋆‖²/(2t)` variant the prompt
sketched) to keep the cite faithful; the decode-time corollary needs only the `O(1/t)` shape.
**Optional items NOT shipped:** the SGD-noise `Φ(·)` smoothing is stated in `rem:probability`
WITHOUT a `\cite` (one sentence, no digest shipped → no citation, per the honesty constraint); the
Soudry et al. 2018 implicit-bias remark was omitted entirely (no digest shipped → not claimed).
