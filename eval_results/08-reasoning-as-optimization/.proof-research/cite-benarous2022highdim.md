# Ben Arous, Gheissari, and Jagannath, "High-dimensional limit theorems for SGD: Effective dynamics and critical scaling" (2022)

## Reference

Ben Arous, G\'erard and Gheissari, Reza and Jagannath, Aukosh.
*High-dimensional limit theorems for SGD: Effective dynamics and
critical scaling.*
Communications on Pure and Applied Mathematics, 77(3):2030--2080,
2024 (online 2023; arXiv 2022).
DOI: 10.1002/cpa.22169
arXiv: https://arxiv.org/abs/2206.04030

## What is cited

We cite this work for the **scaling-limit framework** that underlies
our reasoning-trajectory analysis. Specifically, Ben Arous--Gheissari--
Jagannath establish a general limit theorem (their Theorem 2.3) for the
evolution of summary statistics $u_n(X_\ell)$ of constant-step-size
online SGD in the high-dimensional limit $d \to \infty$: under their
localizability and asymptotic-closability conditions, the rescaled
process $u_n(X_{\lfloor t \delta_n^{-1} \rfloor})$ converges weakly to
the solution of an SDE
$$
   du_t \;=\; h(u_t)\,dt \;+\; \sqrt{\Sigma(u_t)}\, dB_t,
$$
with effective drift $h$ and effective volatility $\Sigma$ determined
by the population gradient and gradient-covariance respectively.

For us, the **critical scaling regime** $\delta_n \asymp 1/d$ identified
in their work is exactly the regime in which our $\alpha(d) \sim \sqrt
d$ per-effective-token drift parameter lives. In that regime, their
analysis says (i) the effective drift acquires a correction term beyond
naive gradient flow, (ii) microscopic fluctuations near fixed points
become non-trivial SDE limits (Ornstein--Uhlenbeck or degenerate),
and (iii) sharp phase transitions emerge between mean-reverting and
mean-repellent behaviour at the fixed points. These three facts are
exactly the analytic content underlying our Theorem~T1 (snowball vs
extinction).

## Why we cite it

Three reasons:

1. **Foundational scaling framework.** The paper unifies the
   Saad--Solla / "order parameters" line of work into a single
   abstract scaling-limit theorem. Our $\alpha(d) \sim \sqrt d$
   assumption is not ad hoc; it is the standard critical step-size
   scaling these authors identify as the place where the scaling limit
   acquires non-trivial diffusive behaviour.
2. **Phase transitions made rigorous.** Their Sections~3--5 show
   precisely how high-dimensional SGD on spiked matrix/tensor models,
   two-layer networks for Gaussian-mixture classification, and the
   XOR problem exhibit phase transitions whose proof is exactly the
   ballistic-then-diffusive analysis we adapt to the snowball /
   extinction dichotomy for reasoning tokens.
3. **Lottery-ticket connection.** Their statement that the success
   probability of converging to a Bayes-optimal classifier goes to 1
   as the second-layer width grows is, in their words, "a
   mathematically rigorous example of the lottery ticket hypothesis."
   We borrow this framing for our Theorem~T3 (problem-difficulty
   characterization): the minimum dimension for supercriticality
   plays the role of the lottery-ticket threshold.

## Verification

Citation verified against the Communications on Pure and Applied
Mathematics record (online 2023, print 2024; volume 77, issue 3) and
against the arXiv preprint (2206.04030, posted 2022-06-08, last revised
2023-09-26). Author list, title, and abstract match. The "critical
scaling regime" terminology appears verbatim in the abstract and is
elaborated in their Section~2.2 and Remark~1. Theorem~2.3 is the
generic SDE limit theorem we invoke; Section~3 (spiked tensor) and
Section~5 (XOR) provide the worked phase-transition examples whose
technique we follow.
