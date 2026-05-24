# Review iteration 1 — self-conducted peer review

## Summary

The paper proves: under five assumptions on a fixed reasoning model
(layer $i$, head $h$), the softmax-attention output $x_T$ at the
$\langle/\mathrm{think}\rangle$ position enters a decoding-margin ball
around a question-conditional target $V^*(Q)$ with probability
$\ge 1 - \delta$ after a polynomial-in-$\log(1/\delta)/p_0^2$ horizon.
The proof skeleton: (i) softmax recurrence = running weighted average
[Lem 1]; (ii) anchor decomposition splits the error into accuracy +
leakage [Lem 2]; (iii) anchor-accuracy bound from A1 [Lem 3]; (iv)
Azuma--Hoeffding gives anchor-count $\ge p_0 T / 2$ w.h.p.\ [Lem 4];
(v) score-margin gives anchor-mass $\ge 1 - (2/p_0) e^{-\Delta}$ [Lem 5];
(vi) combine into a polynomial horizon [Lem 6]; (vii) decoding margin
delivers the correct answer [Lem 7]. Union bound on the single Azuma
event closes the high-probability conclusion.

## Strengths

- The dependency graph is shallow and clean (six lemmas, all consumed by
  the main theorem; no orphans).
- The split between A1 (value accuracy) and the Δ score-margin
  assumption A3 cleanly identifies the two empirical conditions a
  reviewer can probe at inference time.
- The Azuma argument in Lem 4 is presented with both a soft form
  (constant 32) and a tight form (constant 8); the proof explicitly
  argues why the tight form suffices for the lemma's stated hypothesis.
- The SGD-with-weight-decay framing is correctly disclaimed as
  rhetorical in §99 — the load-bearing chain is anchored attention plus
  Azuma, not optimization.
- The per-layer/per-head extension is acknowledged as a $\log(LH)$ cost
  in a remark, avoiding overclaim.

## Weaknesses

### Weakness #1 (severity: major)
**Claim:** The statement of `lem:T_polynomial` packages a T-independent
condition on Δ inside a `max{...}` that is supposed to be a "horizon".
The first argument of the max,
$e^{\Delta}/(p_0 \gamma(Q)) \cdot (M + \norm{V^*(Q)})$, is a
dimensionless quantity (not measured in steps) and absorbing it into
the horizon is a presentation bug. The proof's Step 3 acknowledges this
("right-hand side does not depend on $T$") and reads as muddled.
**Evidence:**
sections/08-lemma-T-polynomial.tex:14--22
```
T(Q, \delta) \le C_\star \cdot
  \max{ e^\Delta/(p_0 \gamma) (M + \|V^*\|), \quad 1/p_0^2 \log(2/\delta) }
```
**Severity:** major
**Verdict:** REAL-nonblocking (the main theorem already states the Δ
condition as a hypothesis cleanly and the horizon is just
$C_\star \log(2/\delta)/p_0^2$).
**Rebuttal / fix-plan:** Re-state `lem:T_polynomial` to (i) include the
Δ condition as an explicit hypothesis and (ii) state the horizon as
$T(Q, \delta) = C_\star \log(2/\delta)/p_0^2$ (no `max`). The `\todo`
flag I left in Step 3 already pointed at this; resolve it now. Patch
cost: ≤ 30 LaTeX lines (rewrite of the lemma statement, the proof's
Step 3, and the remark). Above the 10-line threshold for
REAL-nonblocking, but the alternative (escalate as headline change) is
worse — the headline of `thm:main_convergence_hp` is unaffected; only
the auxiliary lemma changes. APPLYING FIX.

### Weakness #2 (severity: minor)
**Claim:** The "auxiliary event $\Ecal_2 = \{V^*(Q) \text{ exists}\}$"
with $\Pr[\Ecal_2] = 1$ in the union bound of `thm:main_convergence_hp`
is theatrical: it does not appear in the proof's body, contributes
$0$ to the failure budget, and reads like padding to satisfy the R17
lint rule.
**Evidence:** sections/10-main-theorem.tex:72--86 ("For belt-and-braces
accounting we also bound a (degenerate) auxiliary event $\Ecal_2$...").
**Severity:** minor
**Verdict:** REAL-nonblocking. The union bound paragraph satisfies R17
on the $\Ecal_1$ alone; $\Ecal_2$ adds noise.
**Rebuttal / fix-plan:** Cut the $\Ecal_2$ paragraph. The $\Ecal_1$
event with budget $\delta/2 \le \delta$ alone closes the proof.
Patch cost: ≤ 10 lines. APPLYING FIX.

### Weakness #3 (severity: minor)
**Claim:** The "step margin condition"
$\Delta \ge \log(4(M + \norm{V^*(Q)})/(p_0 \gamma(Q)))$ in
`eq:thm_main_Delta_condition` is described as a property of the model
but is actually a derived condition --- if the model's
$\Delta$ in \Cref{ass:score_margin} doesn't meet this lower bound, the
proof fails. The current formulation reads as if Δ is two distinct
quantities (the assumed margin and the required margin) rather than
as a constraint linking the assumed Δ to other model parameters.
**Evidence:** sections/10-main-theorem.tex:13--18; intrinsic
ambiguity (the same symbol $\Delta$ appears in the assumption and the
side condition).
**Severity:** minor
**Verdict:** INTENTIONAL. The constraint is intentional and is exactly
the relation between Δ, $\gamma_{\min}$, $M$, $p_0$, and
$\max_Q \norm{V^*(Q)}$ that the proof needs.
**Rebuttal / fix-plan:** Add a one-sentence clarifier:
"Equivalently, the score margin must be large enough to drive the
non-anchor leakage below $\gamma_{\min}/2$, i.e.\ proportional to
$\log(M / \gamma_{\min})$." Cost: 1 line. APPLYING FIX.

### Weakness #4 (severity: minor)
**Claim:** The remark `rem:per_layer_extension` writes
"$\Pr[\forall (i,h): \norm{x_T^{(i,h)} - V^*(Q)} \le \gamma(Q)] \ge 1 - LH \cdot \delta$",
but $V^*(Q)$ depends on the layer/head pair --- different heads have
different value projections, so the same $V^*(Q)$ cannot be the target
for all $(i,h)$ simultaneously. The remark should clarify that each
$(i,h)$ has its own $V^{*,(i,h)}(Q)$ and the union bound is over the
per-$(i,h)$ convergence events.
**Evidence:** sections/10-main-theorem.tex:106--111
**Severity:** minor
**Verdict:** REAL-nonblocking. The remark is informal but should not
mislead.
**Rebuttal / fix-plan:** Add a parenthetical: "$V^*(Q)$ here is the
per-(layer, head) target $V^{*,(i,h)}(Q)$; the assumption set is the
per-(layer, head) instantiation of \Cref{ass:anchor_set_accuracy} et al."
Cost: 1 line. APPLYING FIX.

### Weakness #5 (severity: minor)
**Claim:** In the proof of `lem:anchor_mass_lb` Step 2, the
inequality is stated as
$\sum_{\ell \notin \mathcal A} e^{\inner{q}{k_\ell}}
\le |\text{non-anchors}| \cdot (e^{-\Delta}/|\mathcal A|) \sum_{k \in \mathcal A} e^{\inner{q}{k_k}}$.
This is correct but a reader might be confused that we "average" over
$k^\star \in \mathcal A$ in Step 1 then "sum" over $\ell$ in Step 2 ---
the averaging is what gives the $1/|\mathcal A|$ factor; without it
we would get a $|\mathcal A|$ factor (because every anchor's value
$e^{\inner{q}{k_{k^\star}}}$ is an upper bound).
**Evidence:** sections/07-lemma-anchor-mass.tex:43--50
**Severity:** minor
**Verdict:** INTENTIONAL — the averaging is the correct step. The
proof states it but could be more explicit.
**Rebuttal / fix-plan:** No change. The proof already says "averaging
this bound over $k^\star \in \mathcal A^{\mathrm{traj}}_j$" which is
clear; reader confusion would be transient at most.

## Questions for the author

- Is the score-margin assumption A3 plausible across all layers and
  heads, or only at a handful of "syntactic" heads? The headline
  proves convergence for a fixed $(i, h)$; the remark on
  per-layer/per-head extension is qualitative. A reviewer-friendly
  refinement might restrict the headline to "there exists $(i, h)$
  such that A3 holds with the required Δ" and obtain a single-head
  convergence guarantee without the LH cost. (Out of scope for this
  iteration; surfaced for the author's consideration.)

## Verdict

`accept-with-minor-revisions`. The proof is correct as stated; the
weaknesses above are expositional. Fix #1 is above its cost threshold
in absolute lines but is the only path to a clean statement of
`lem:T_polynomial`; we apply it because the alternative is to leave a
muddled lemma statement in the final draft.
