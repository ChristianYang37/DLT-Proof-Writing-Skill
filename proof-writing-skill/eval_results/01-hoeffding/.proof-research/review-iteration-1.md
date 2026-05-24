# Review iteration 1 — Hoeffding's inequality

Reviewer pass executed by the author agent in reviewer mode (no separate Task /
Agent tool surface available in this environment); the author then verifies each
weakness in the second half of the file. The reviewer-mode pass was performed
top-to-bottom on the source `.tex` files (sections/01-preliminaries.tex,
sections/02-hoeffding-lemma.tex, sections/03-main-theorem.tex) and on the
compiled PDF; the confidence trace at `.proof-research/confidence-trace.md` was
used to focus on 🟡 / 🔴 steps.

---

## Summary

The submission proves Hoeffding's inequality
$\Pr[|S_n - \E S_n| \ge t] \le 2 \exp(-2t^2/\sum_i (b_i - a_i)^2)$ for sums of
independent bounded random variables via the standard Chernoff route: Markov
applied to $e^{\lambda (S_n - \E S_n)}$, factorization by independence,
Hoeffding's lemma per summand, optimization in $\lambda$, and a symmetry +
union-bound combination of the upper and lower tails. The decomposition is
shallow: one named lemma (Hoeffding's lemma, MGF bound for bounded centered
RVs) plus the main theorem. The lemma is proved by the log-MGF / exponential-tilt
/ Popoviciu route, integrating the second-derivative bound twice. Both proofs
use the trailing-justification block derivation pattern uniformly. The
preliminaries cleanly establish notation and one elementary fact about range
invariance under centering, which is invoked twice. Both the LaTeX compilation
gate and the lint pass with zero errors and zero warnings.

## Strengths

- Decomposition is at the right granularity: a single named lemma (Hoeffding's
  lemma) carries the technical content; the theorem proof is a 4-step Chernoff
  assembly. No bookkeeping lemmas inflate the dependency graph.
- The exponential-tilting / Popoviciu route for the lemma is the cleanest
  textbook derivation; the proof spells out the change-of-measure formula
  rather than waving at it, which makes the $\psi''(\lambda) = \Var_\lambda(Y)$
  identity reviewer-checkable.
- Range-invariance under centering is factored out into `fac:range-invariance`
  and cited at the cite-site in the theorem proof; this is the right level of
  factoring (the alternative — re-deriving inline in the theorem proof — would
  pollute the Chernoff calculation).
- The proof is honest about the case $t = 0$ and the case $v = 0$ (all summands
  a.s. constant); neither is silently swept aside.
- Trailing-justification block is used uniformly: every relation row in both
  derivations is accounted for in the trailer.

## Weaknesses

### Weakness #1 (severity: minor)
**Claim:** The Taylor-integration step in the lemma proof
(sections/02-hoeffding-lemma.tex:85, "the third uses the bound
Eq.~\eqref{eq:psi-pp-bound} on $\psi''$ pointwise on $[0, \lambda]$ (or $[\lambda, 0]$
if $\lambda < 0$, in which case the substitution $s \mapsto -s$ gives the same final
value because both $(\lambda - s)$ and the differential pick up a sign)") handles
the $\lambda < 0$ case via a one-sentence prose aside that is correct but terse.
A reader wanting to verify by hand has to reproduce the sign analysis; the unified
double-integration form $\psi(\lambda) - 0 - 0 = \int_0^\lambda \int_0^t \psi''(s)\,
ds\, dt$ would close this without case analysis.
**Evidence:** sections/02-hoeffding-lemma.tex lines 90-93.
**Severity:** minor

### Weakness #2 (severity: minor)
**Claim:** The case $t = 0$ is handled in the middle of Step 2
(sections/03-main-theorem.tex:68-70) rather than upfront, leaving the reader
momentarily confused at Step 1 about whether $\lambda > 0$ is actually achievable
when $t = 0$.
**Evidence:** sections/03-main-theorem.tex line 35 ("Fix $\lambda > 0$") happens
before line 68-70 ("the case $t = 0$ is trivial ... assume $t > 0$ from here on").
**Severity:** minor

### Weakness #3 (severity: style)
**Claim:** The preliminaries define $v := \sum_i (b_i - a_i)^2$ in the prelim
notation block but the theorem statement writes out the sum explicitly without
using $v$, while the theorem proof uses $v$ extensively. Minor inconsistency.
**Evidence:** sections/01-preliminaries.tex:23 defines $v$;
sections/03-main-theorem.tex:11 (theorem statement) writes $\sum_{i=1}^n (b_i -
a_i)^2$ rather than $v$; sections/03-main-theorem.tex:33 ("Write $v := \sum_i
(b_i - a_i)^2$") re-introduces $v$ as if it were new.
**Severity:** style

## Questions for the author

- Is the statement deliberately written with the raw sum $\sum_i (b_i - a_i)^2$
  in the conclusion rather than the abbreviation $v$, in order to match the
  user's prompt verbatim? (If yes, this is intentional and the style note above
  should be dismissed.)
- Would the author prefer the one-sided bound $\Pr[S_n - \mu \ge t] \le
  \exp(-2t^2/v)$ promoted to a top-level corollary, given that it is sometimes
  what users want from Hoeffding? Currently it is recorded as
  \Cref{rem:one-sided}.

## Verdict

`accept-with-minor-revisions` — all three weaknesses are minor or style; none
blocks the correctness of the proof. The Taylor sign-handling (Weakness #1) is
the one I would most want addressed, and a 2-line replacement closes it.

---

## Author verification and decisions

### Weakness #1 (severity: minor)
**Claim:** Taylor sign-handling for $\lambda < 0$ is terse.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The current prose is mathematically correct: for $\lambda
< 0$, the convention $\int_0^\lambda = -\int_\lambda^0$ together with the sign of
$(\lambda - s)$ on $[\lambda, 0]$ does yield the same value $\lambda^2(\beta -
\alpha)^2 / 8$. However, the reviewer's preferred phrasing — a unified treatment
via the double-integral identity $\psi(\lambda) = \int_0^\lambda \int_0^t \psi''(s)
\, ds\, dt$, which is sign-blind because $\psi''$ is nonneg-bounded — is cleaner
and removes the need for an aside. Cost-gated decision per review-loop.md table:
*minor + REAL-nonblocking, patch ≤ 3 lines → fix*. Apply.

### Weakness #2 (severity: minor)
**Claim:** $t = 0$ carve-out is placed mid-Step-2 rather than upfront.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Reviewer is correct that placing the trivial-case carve-out
upfront would be cleaner. Cost-gated: *minor + REAL-nonblocking, patch ≤ 3 lines
→ fix*. Apply.

### Weakness #3 (severity: style)
**Claim:** Theorem statement writes raw sum; proof uses $v$. Inconsistency.
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** The theorem statement deliberately mirrors the user's
prompt verbatim (which writes $\sum_i (b_i - a_i)^2$ in the exponent), and the
abbreviation $v$ is introduced in the proof body purely for compactness in the
chain of inequalities. Stating $v$ in the theorem statement would marginally
shorten line 11 but at the cost of a forward-pointing notational dependence on
the prelim's $v$ definition; the current choice keeps the headline self-contained.
**Action:** do not fix.

---

## Fixes applied

- Weakness #1: replace the Taylor-integration prose-aside with the unified
  double-integration identity.
- Weakness #2: relocate the $t = 0$ trivial-case carve-out to the start of
  Step 1, before fixing $\lambda > 0$.

Both fixes are local LaTeX edits with no statement changes. Post-fix compile
must succeed.

## Compile-check after fixes

(See post-iteration log.)
