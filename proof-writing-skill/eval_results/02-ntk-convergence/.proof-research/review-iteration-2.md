# Phase D review — iteration 2

## Reviewer output

### Summary

Re-reviewing the revised proof after iteration-1 fixes. The proof still establishes linear convergence of GD on the squared loss for a two-layer ReLU network with $m \gtrsim n^6/(\lambda_0^4 \delta^3)$ width and $\eta = O(\lambda_0/n^2)$ step size, following the three-lemma DZPS19 skeleton. Iteration 1 strengthened the proof of \Cref{lem:linear_conv} by lifting the perturbation event and flip-count event into explicit hypotheses, and rewrote the proof of \Cref{lem:init_residual} via conditional Hoeffding + Bernstein-on-norms. Both `\todo{verify}` markers have been removed.

### Strengths

- **Bookkeeping at the assembly step is now explicit.** The proof of \Cref{thm:main} Step 3 names which clause of \Cref{lem:linear_conv}'s hypothesis each of $\mathcal E_1, \mathcal E_2$, and $(\star_t)$ supplies.
- **The flip-set inclusion $T_i(s) \subseteq S_i$ is rigorously justified.** The witness argument in \Cref{sec:proof_linear_conv} Step 2 is correct.
- **The sub-Gaussian tail is now derived from conditional Hoeffding** (\Cref{fac:hoeffding}) rather than invoked from memory; no fabricated proxy constant remains.

### Weaknesses

**W6.** [minor / REAL-nonblocking] In the rewritten proof of \Cref{lem:init_residual}, the step "$\E[g_+^2] = 1/2$ for $g \sim \mathcal N(0,1)$" is asserted without derivation. While true (since by symmetry $\E[g^2 \one[g \ge 0]] = (1/2) \E[g^2] = 1/2$), the assertion is one degree of compression too tight; a one-clause parenthetical "(by symmetry of $g$)" suffices. Severity: minor.

**W7.** [minor / REAL-nonblocking] The use of "Bernstein's inequality for sub-exponential variables" in the proof of \Cref{lem:init_residual} is named but not cited or stated as a Fact. The reader has to take on faith that the sub-exponential Bernstein bound applies to $b_r^2 = \sigma(\wb_r(0)^\top \xb_i)^2$. This is a textbook fact (the square of a half-Gaussian is sub-exponential with parameters that give the stated tail), but a one-line reference to a textbook (e.g.\ Vershynin Theorem 2.8.1) or a \Cref{fac:bernstein} would close the gap. Severity: minor.

**W8.** [minor / REAL-nonblocking] In the proof of \Cref{lem:perturbation} Step 2, the chain "$\Pr[\one[A_{i,r}]/m \ge 2R] \le \Pr[\sum_r (\one[A_{i,r}] - \Pr[A_{i,r}])/m \ge R]$" uses $\Pr[A_{i,r}] \le R$ from Eq.~\eqref{eq:flip_prob}, but the inequality "$\le$" instead of "$=$" needs to be justified: the event $\{X \ge 2R\}$ is contained in $\{X - \E X \ge 2R - E X\} \supseteq \{X - \E X \ge R\}$ when $\E X \le R$. The current text says "absorb the centering" but doesn't make explicit that we're taking a *superset* of the centered event. Severity: minor (style).

### Questions for the author

- Q3. The Bernstein-on-$\sum b_r^2$ step requires $m \ge \Omega(\log(1/\delta))$ for the tail $\exp(-cm)$ to be small; this is dominated by the headline width $m \gtrsim n^6 / (\lambda_0^4 \delta^3)$ but worth a sentence noting that this requirement is non-vacuous.

### Verdict

**accept-as-is** (modulo three trivial style minorities). The proof skeleton and all derivations are now airtight. The three remaining weaknesses are all style-level minor.

---

## Author verification + decisions

### Weakness #W6 (severity: minor)
**Claim:** "$\E[g_+^2] = 1/2$" needs a derivation cue.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Fix. 1 line.

### Weakness #W7 (severity: minor)
**Claim:** Sub-exponential Bernstein needs citation or Fact.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Fix. Add a one-line citation to \cite{du2019gradient} (which uses the same fact) or just inline a sub-Gaussian-square argument. Actually the cleanest fix is to replace Bernstein with a direct argument: since $b_r^2 \le (\wb_r(0)^\top \xb_i)^2 \sim \chi^2_1$, and $\E[(\wb_r(0)^\top \xb_i)^2] = 1$, a standard $\chi^2$ tail gives $\Pr[\sum_r (\wb_r(0)^\top \xb_i)^2 \ge 2m] \le \exp(-c m)$. Use $b_r^2 \le (\wb_r(0)^\top \xb_i)^2$ and take this as a Fact. 2 lines.

### Weakness #W8 (severity: minor / style)
**Claim:** "Absorb the centering" needs the superset framing.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Fix. Reword the justification clause. 1 line.

---

## Iteration outcome

Applied fixes for W6, W7, W8 (all 1-2 line patches). Reviewer verdict was `accept-as-is` (modulo three trivial style minorities); per Termination Gate 1 of [review-loop.md](../../references/review-loop.md), the loop terminates here.

**Final verdict:** accept-as-is (post-fix). Loop iterations: 2.
