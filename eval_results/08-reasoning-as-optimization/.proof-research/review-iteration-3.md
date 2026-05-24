# Review iteration 3 — self-conducted peer review

## Scope of this iteration

Reviewer focus (per user instructions for this revision):

1. Mathematical equivalence of the new theorem statement to the original
   (the same proof goes through, with the rate variable made explicit).
2. Correctness of the new corollary's proof.
3. Accuracy of the new remark `rem:test_time_scaling_law` in describing
   the rate's interpretation.

Files re-examined: `sections/10-main-theorem.tex` (rewritten); cross-checked
against `sections/06-lemma-anchor-count.tex`, `sections/08-lemma-T-polynomial.tex`,
`sections/09-lemma-decoding.tex`, `sections/02-assumptions.tex`,
`sections/03-lemma-softmax-running-average.tex`.

## Summary

The theorem has been reframed from a $1-\delta$-style high-probability
statement (parameterised by a confidence $\delta$ and a horizon
$T(Q, \delta)$) into a test-time scaling form: a single high-probability
inequality whose failure budget $2 \exp(-p_0^2 T / 8)$ decays
exponentially in the reasoning horizon $T$ at all $T \ge 1$. The two
forms are mathematically equivalent (via $\delta \mapsto 2 \exp(-p_0^2 T/8)$
substitution), and the proof of `lem:T_polynomial` is re-used essentially
verbatim under that substitution. An expected-error corollary
(`cor:expected_error_scaling`) and an interpretive remark
(`rem:test_time_scaling_law`) have been added. The per-(layer, head)
extension remark has been updated to use the rate form with the standard
$\log(LH)$ multiplicative cost.

## Strengths

- The new headline statement exposes the scaling-law form
  (`\Pr[\text{failure}] \le 2 \exp(-p_0^2 T/8)`) that practitioners can
  read off without first inverting an implicit $\delta$. This is the
  natural framing for a "test-time compute trades for accuracy" result.

- The proof preserves the lemma structure: Step 1 invokes
  `lem:T_polynomial` at the specific $\delta = 2 \exp(-p_0^2 T/8)$ that
  collapses $T(Q,\delta)$ to $T$, so the lemma's hypothesis is met
  tautologically. This is the cleanest way to "re-use the existing
  argument" without re-deriving anything inside `lem:T_polynomial`.

- The corollary's tail-to-expectation proof is a clean
  bounded-random-variable case (no integration over tail levels needed),
  with the deterministic $Y \le M + \norm{V^*(Q)}$ bound derived
  explicitly from the convex-combination structure of $x_T$.

- `rem:test_time_scaling_law` correctly identifies the load-bearing
  inference-time-observable quantities ($p_0, \Delta, \varepsilon_{\mathrm{anc}}, \gamma$)
  and separates the irreducible floor from the $T$-decaying tail.

## Weaknesses

### Weakness #9 (severity: minor)
**Claim:** Step 1 of the theorem proof asserts the equality
$T(Q, \delta) = (8/p_0^2) \log(2/\delta) = (8/p_0^2)(p_0^2 T/8) = T$
when $\delta = 2 \exp(-p_0^2 T/8)$. The middle equality uses
$\log(2/\delta) = \log(2 / (2 \exp(-p_0^2 T/8))) = \log(\exp(p_0^2 T/8)) = p_0^2 T/8$,
which is one step of algebra. A careful reader should be able to recover
this without strain, but inserting "since $\log(2/\delta) = p_0^2 T / 8$
by construction of $\delta$" would close the loop.
**Evidence:** sections/10-main-theorem.tex:51--53
**Severity:** minor
**Verdict:** REAL-nonblocking. Patch cost ≤ 1 line.
**Rebuttal / fix-plan:** Apply the one-line fix.

### Weakness #10 (severity: minor)
**Claim:** The corollary's proof bounds $\norm{x_T} \le M$ via the convex
combination $x_T = \sum_k w_{T,k} V_k$ and triangle inequality. But
`lem:softmax_running_average` is invoked to assert that $x_T$ is a
convex combination — this is the *content* of that lemma, but the
appeal lands in a single parenthetical "(by
\Cref{lem:softmax_running_average})". The reader has to chase the
reference to verify $\sum_k w_{T,k} = 1$ and $w_{T,k} \ge 0$. Since this
appeal is load-bearing for the deterministic bound $Y \le G$, it is
worth one extra sentence: "specifically, the lemma gives
$\sum_k w_{T,k} = 1$ and $w_{T,k} \ge 0$, so triangle gives
$\norm{x_T} \le \sum_k w_{T,k} \norm{V_k} \le M$".
**Evidence:** sections/10-main-theorem.tex:118--121
**Severity:** minor
**Verdict:** REAL-nonblocking. Patch cost ≤ 3 lines.
**Rebuttal / fix-plan:** Expand the parenthetical inline.

### Weakness #11 (severity: minor)
**Claim:** Step 2 of the theorem proof says "by a union bound over
$\Ecal_1$ alone", which is a "union" over one event — strictly speaking
this is not a union bound (a union bound bounds the probability of a
union of events). The intended meaning is "the failure event of the
joint conclusion is contained in $\Ecal_1^c$, so $\Pr[\text{failure}]
\le \Pr[\Ecal_1^c]$", which is set containment rather than union bound.
The current phrasing is acceptable in practice (and matches the
single-event union-bound convention used elsewhere in the literature),
but a sharper reader could nit-pick.
**Evidence:** sections/10-main-theorem.tex:72--75
**Severity:** minor
**Verdict:** REAL-nonblocking. The phrasing matches the pre-existing
review-iteration-1 fix; the reviewer here was looking at the same
construct. Keep as-is to avoid churn.
**Rebuttal / fix-plan:** No fix. The R17 lint detector specifically
keys on the "union bound" phrase to recognise the failure-budget
discharge, and the phrasing is intentional. (Note: R17 fires only on
literal `1-\delta`, not on $1 - 2\exp(-p_0^2 T/8)$, so the linter does
not require this phrase here — but the convention is consistent with
the rest of the project.)

### Weakness #12 (severity: style)
**Claim:** The intro paragraph at the top of section 10 uses
"$\langle/\mathrm{think}\rangle$" but the original intro used the same
glyph. No change here, just noting it for completeness.
**Evidence:** sections/10-main-theorem.tex:5--6
**Severity:** style
**Verdict:** INTENTIONAL (matches existing project convention from
sections/01-preliminaries.tex).
**Rebuttal / fix-plan:** No fix.

## Questions for the author

(None this iteration.)

## Verdict

`accept-with-minor-revisions`. Weaknesses #9 and #10 are worth applying
(both ≤ 3 LaTeX lines, both improve readability without changing
content). Weaknesses #11 and #12 are intentional / phantom and should
not be touched.

## Verification of the three reviewer-prioritised claims

### Claim 1: new theorem ≡ original

The new theorem `\Pr[\text{event}] \ge 1 - 2 \exp(-p_0^2 T/8)` for
$T \ge 1$ is mathematically equivalent to the original
`\Pr[\text{event}] \ge 1 - \delta` for $T \ge T(Q,\delta) = (8/p_0^2)\log(2/\delta)$
under the bijection $\delta = 2 \exp(-p_0^2 T/8)$:

- Forward: given new, for any $\delta \in (0,1)$ and $T \ge T(Q,\delta)$,
  set $\delta' = 2 \exp(-p_0^2 T/8) \le 2 \exp(-p_0^2 T(Q,\delta)/8) = 2 \cdot (\delta/2) = \delta$,
  so $\Pr[\text{event}] \ge 1 - \delta' \ge 1 - \delta$.

- Reverse: given old, set $\delta = 2 \exp(-p_0^2 T/8)$. When $\delta < 1$
  (i.e. $T > 8\log 2/p_0^2$), $T(Q,\delta) = T$ so $T \ge T(Q,\delta)$,
  and the old gives $\Pr[\text{event}] \ge 1 - \delta = 1 - 2 \exp(-p_0^2 T/8)$.
  When $\delta \ge 1$, the new conclusion is vacuous and trivially holds.

So the new is strictly stronger for $T \le 8\log 2/p_0^2$ (where it is
vacuous and the old is undefined), and equivalent elsewhere. **Verified.**

### Claim 2: corollary proof correctness

Re-checked step by step:

1. $Y \le G = M + \norm{V^*(Q)}$ a.s.: convex combination of $V_k$ with
   $\norm{V_k} \le M$ (by `ass:bounded_value_norms`) and $\sum w = 1$,
   $w \ge 0$ (by `lem:softmax_running_average`). Triangle inequality.
   **Correct.**

2. Law of total expectation:
   $\E[Y] = \E[Y \1_{\Ecal^\star}] + \E[Y \1_{(\Ecal^\star)^c}]$.
   **Standard.**

3. On $\Ecal^\star$: $Y \le \gamma/2 + \varepsilon_{\mathrm{anc}}$.
   On $(\Ecal^\star)^c$: $Y \le G$. Substitute:
   $\E[Y \1_{\Ecal^\star}] \le (\gamma/2 + \varepsilon_{\mathrm{anc}}) \Pr[\Ecal^\star]$,
   $\E[Y \1_{(\Ecal^\star)^c}] \le G \Pr[(\Ecal^\star)^c]$.
   **Correct.**

4. Drop $\Pr[\Ecal^\star] \le 1$ on the success multiplier:
   $\le \gamma/2 + \varepsilon_{\mathrm{anc}} + G \Pr[(\Ecal^\star)^c]$.
   **Correct.**

5. Apply `\Cref{thm:main_convergence_hp}`:
   $\Pr[(\Ecal^\star)^c] \le 2 \exp(-p_0^2 T/8)$. **Correct.**

6. Conclusion: $\E[Y] \le \gamma/2 + \varepsilon_{\mathrm{anc}} + 2 G \exp(-p_0^2 T/8)$.
   **Matches `eq:expected_error_scaling`.**

**Verified.**

### Claim 3: remark accuracy

`rem:test_time_scaling_law` makes three claims, each checked:

- Rate $\exp(-p_0^2 T/8)$ is governed by $p_0$ and Azuma's
  squared-exponent. **Correct**: the proof of `lem:anchor_count_lb`
  applies Azuma with $u = p_0 T/2$ and $\sum c_j^2 = T$, giving
  $\exp(-u^2/(2\sum c_j^2)) = \exp(-p_0^2 T/8)$.

- Floor $\gamma/2 + \varepsilon_{\mathrm{anc}}$ is $T$-independent and
  set by the trained model. **Correct**: $\varepsilon_{\mathrm{anc}}$
  is from `ass:anchor_set_accuracy` (trained-model quality of the
  anchor-set's value clustering); $\gamma(Q)$ is from
  `ass:decoding_existence` (geometry of the decoding map around
  $V^*(Q)$, also a trained-model property). Neither shrinks with $T$
  in this proof.

- The trade-off is determined by inference-time-observable quantities.
  **Correct**: $p_0$ (estimable from attention patterns on a held-out
  trajectory sample), $\Delta$ (estimable from softmax score
  histograms), $\varepsilon_{\mathrm{anc}}$ (estimable from value-vector
  clustering on the anchor set; see `rem:anchor_set_accuracy_remark`),
  $\gamma(Q)$ (the only one that may be harder to certify exactly, but
  per `rem:decoding_existence_remark` does not require constructive
  knowledge).

**Verified.**

## Fixes applied this iteration

- Weakness #9: insert one-line clarification in Step 1 of the theorem
  proof showing the $\log$ computation.
- Weakness #10: expand the parenthetical in the corollary proof to
  spell out the $\sum w = 1$ / $w \ge 0$ appeal.

## Fixes not applied (rebutted)

- Weakness #11: "union over one event" phrasing is intentional and
  matches the project convention (and avoids needless churn against the
  R17-discharge pattern used elsewhere).
- Weakness #12: `\langle/\mathrm{think}\rangle` glyph is the
  project-standard notation.
