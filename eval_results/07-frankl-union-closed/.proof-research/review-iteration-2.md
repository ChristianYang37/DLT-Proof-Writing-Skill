# Review iteration 2 — Gilmer / Frankl union-closed proof

## Reviewer output

### Summary
Same headline result as iteration 1: Gilmer's $0.01$ lower bound on the union-closed sets conjecture, decomposed into two elementary binary-entropy inequalities (`lem:hbin-low`, `lem:hbin-mixed`), a key conditional-entropy gap (`lem:gap`), an information-theoretic strengthening (`thm:entropy-gap`), and a final contradiction argument (`thm:main`). The previous iteration's fixes have been applied: the monotonicity discussion in `lem:hbin-low` has been streamlined and pushed to a clean remark, and the awkward footnote in `lem:gap` Step 3 has been replaced with cleaner trailing-justification prose. The proof now reads more directly.

### Strengths
- Both pointwise entropy inequalities (`lem:hbin-low` and `lem:hbin-mixed`) are stated with explicit hypotheses on $(p, p')$ and proven independently — `lem:hbin-mixed` in particular gets a clean two-line concavity proof.
- The hypothesis-verification list at the cite-site of `lem:gap` in `thm:entropy-gap` enumerates all six conditions and provides a justification for each — a strong defense against the "hallucinated lemma application" failure mode.
- The arithmetic $0.9 \cdot 1.4 = 1.26$ and $2 \cdot 0.9 \cdot 0.9 = 1.62$ that drives the final assembly (`lem:gap` Step 5) is internally consistent and matches Gilmer 2022 exactly.
- The strict-inequality conclusion in `thm:entropy-gap` (separating the $\H(A) > 0$ from $\H(A) = 0$ cases) sets up the contradiction in `thm:main` cleanly.

### Weaknesses

#### Weakness #1 (severity: minor)
**Claim:** In `lem:hbin-low`, the proof claims that $g(s)$ is monotone non-increasing on $(0, 0.2]$ as the basis for $\min g = g(0.2)$, but the actual derivative computation is deferred to "elementary but tedious" remark; the proof does not provide a self-contained algebraic verification. A reader cannot finish verifying the lemma without trusting the numerical sweep or doing the differentiation themselves. The deferred verification is consistent with Gilmer 2022 (which appeals to Figure 1), but is still a verification gap.
**Evidence:** `sections/02-elementary-entropy.tex` `\Cref{rem:g-monotone}`: "A direct (elementary but tedious) computation of $g'(s)$ on $(0, 0.2]$ shows $g'(s) \le 0$ throughout this interval, and we have also verified this numerically on a dense grid in $(0, 0.2]$."
**Severity:** minor — the conclusion is correct (numerically verified to 4+ decimal places) and matches the literature.

#### Weakness #2 (severity: style)
**Claim:** In `sections/03-lemma-1.tex` line 130, the equation label `\label{eq:factor-mixed}` is placed on an intermediate line of a multi-line `\begin{align}` chain, but the final equation in this chain (after the factor pulled out as $\cdot \sum_{c \in \Ccal_0} q(c)(1-p_c)$) does not carry its own label; subsequent references to "Eq.~\eqref{eq:factor-mixed}" use the labeled intermediate line. This is consistent with project style (label only the line you intend to reference), so the choice is intentional.
**Evidence:** `sections/03-lemma-1.tex` line 130: `&\;=\; 2 \, \Pr[\Ccal_1] \, \H(X \mid C \in \Ccal_1) \cdot \sum_{c \in \Ccal_0} q(c) (1 - p_c). \label{eq:factor-mixed}`
**Severity:** style — intentional convention.

### Questions for the author
- (None.)

### Verdict
**accept-as-is**

The remaining weakness (#1) is a "soft gap" rather than a defect: the conclusion is numerically verified and matches the literature. The proof is internally consistent and follows the standard Gilmer argument faithfully.

---

## Author verification of weaknesses

### Weakness #1 (deferred monotonicity)
**Verdict:** INTENTIONAL
**Rebuttal / fix-plan:** This is the same issue raised in iteration 1, after our minimum-change fix. The remaining gap matches Gilmer's original treatment, which similarly defers to numerical / visual verification. Adding a closed-form derivative inequality would require several pages of calculus — far outside the cost gate for a minor / soft weakness. The 🟡 tag in the confidence trace flags this for downstream reviewer attention.

### Weakness #2 (intermediate label)
**Verdict:** INTENTIONAL
**Rebuttal / fix-plan:** Labeling only the line we reference is standard project convention; the choice is deliberate.

---

## Fix application plan

**Fixes applied this iteration:** 0 (all remaining weaknesses are INTENTIONAL).

## Termination decision

Verdict is `accept-as-is`. **Exit loop after iteration 2.**
