# Review iteration 2 — self-conducted peer review

## Summary

After iteration 1's fixes, the proof skeleton is clean: `lem:T_polynomial`
now separates the score-margin condition from the time-horizon
explicitly, the main theorem's union-bound paragraph is uncluttered,
and the per-layer extension acknowledges per-(layer, head) targets.
The headline statement is unchanged. Residual exposition issues remain
in the proof of `lem:anchor_count_lb`.

## Strengths

- The two-role separation between the $\Delta$ hypothesis and the
  $T$ horizon in the new `lem:T_polynomial` is the right move; the
  remark `rem:T_polynomial_remark` explains the load-bearing structure
  cleanly.
- The union-bound paragraph in `thm:main_convergence_hp` is now
  minimal and discharges the $1 - \delta$ headline via the single
  Azuma event.
- The per-layer extension correctly notes the $\log(LH)$ cost.

## Weaknesses

### Weakness #6 (severity: minor)
**Claim:** The proof of `lem:anchor_count_lb` is overlong. Step 2
states the Azuma bound at $u = p_0 T / 4$ and obtains
$\exp(-p_0^2 T / 32)$, then Step 4 says "we use the slightly more
generous bound $T \ge 32 / p_0^2 \cdot \log(1/\delta_1)$" but then
also says "to match the lemma's stated hypothesis we tighten Step 2"
and re-derives with $u = p_0 T / 2$. The reader walks through two
different choices of $u$ for the same lemma. The cleaner pattern is
to pick the tight form up front.
**Evidence:** sections/06-lemma-anchor-count.tex:43--99
**Severity:** minor
**Verdict:** REAL-nonblocking. The proof is correct but reads as
"author thinks aloud". Cost to clean: ≤ 20 LaTeX lines.
**Rebuttal / fix-plan:** Rewrite the proof to apply Azuma directly at
$u = p_0 T / 2$ and obtain $\exp(-p_0^2 T / 8)$ in one shot.

### Weakness #7 (severity: minor)
**Claim:** The proof of `lem:softmax_running_average` Step 1 is
slightly circular: it uses "the last equality used
$s_{j-1} x_{j-1} = \sum_{k=1}^{j-1} e^{\inner{q}{k_k}} V_k$
from \Cref{eq:cumulative_softmax} at index $j-1$ (and the base case
$s_0 x_0 = 0$)". \Cref{eq:cumulative_softmax} is the *definition* of
$x_j$, so the proof is using the definition at $j-1$, which is fine
but the "base case $s_0 x_0 = 0$" should be the convention introduced
in the lemma's preamble. Adding "(by the convention $x_0 = 0$, $s_0 = 0$
in the lemma statement)" would close the loop.
**Evidence:** sections/03-lemma-softmax-running-average.tex:35--37
**Severity:** minor
**Verdict:** REAL-nonblocking, fixable in ≤ 1 line.
**Rebuttal / fix-plan:** Edit to add the convention reminder.

### Weakness #8 (severity: style)
**Claim:** The footnote in \Cref{ass:anchor_set_accuracy} introduces
the dependence of $V(\cdot)$ on the trajectory through positional
embeddings and prior context, but the assumption itself never makes
the trajectory dependence explicit — $V_k = V(a_k)$ is treated as if
it depends only on the token. The footnote's hedge ("we assume this
dependence is mild enough") is fine but could be moved into a remark
for legibility.
**Evidence:** sections/02-assumptions.tex:24--28
**Severity:** style
**Verdict:** INTENTIONAL. The footnote is the right place for this
nuance; promoting to a remark would over-emphasize a technical point.

## Questions for the author

(None this iteration.)

## Verdict

`accept-with-minor-revisions`. Apply Weakness #6 and #7 fixes, then
the proof is at acceptance quality.
