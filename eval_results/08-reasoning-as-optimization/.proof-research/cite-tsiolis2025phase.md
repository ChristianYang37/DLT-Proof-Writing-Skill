# Tsiolis, Mousavi-Hosseini, and Erdogdu, "From Information to Generative Exponent: Learning Rate Induces Phase Transitions in SGD" (2025)

## Reference

Tsiolis, Konstantinos Christopher and Mousavi-Hosseini, Alireza and
Erdogdu, Murat A.
*From Information to Generative Exponent: Learning Rate Induces Phase
Transitions in SGD.*
arXiv:2510.21020, October 2025.
URL: https://arxiv.org/abs/2510.21020

## What is cited

We cite this work as the **most recent precedent** for our
learning-rate-induced phase transition. Tsiolis et al. study online
SGD on Gaussian single-index models $y_i = \sigma_*(\langle x_i,
\theta_*\rangle) + \zeta_i$ with $x_i \sim \mathcal N(0, I_d)$, and
show that the sample complexity exhibits a sharp phase transition as
a function of the learning rate $\eta$:

- For $\eta \lesssim d^{-(p-1)/2}$ (small learning rate):
  sample complexity scales as $n = \tilde\Theta(d^{p-1})$, governed by
  the **information exponent** $p$ of the target link function $\sigma_*$.
- For $\eta \gtrsim 1/\mathrm{polylog}\,d$ (large learning rate):
  sample complexity scales as $n = \tilde\Theta(d^{p_*-1})$, governed by
  the **generative exponent** $p_* \le p$.

The transition occurs at $\eta \asymp d^{-1/2}$ for certain link
functions. The mechanism: large learning rates push the dynamics
beyond the correlational-statistical-query (CSQ) regime, unlocking
faster sample complexity.

For us, this is the **direct contemporary analog** of our snowball /
extinction transition. The information-vs-generative-exponent
dichotomy plays the same structural role as our subcritical / super-
critical $\lambda_0$ regimes: above the threshold, qualitatively
different (faster) convergence; below the threshold, slower (or
non-)convergence.

## Why we cite it

Two reasons:

1. **Validates the "phase transition in learning rate" template** as a
   live research direction. Our paper joins a small but growing
   literature on **learning-rate-induced regime shifts in
   high-dimensional SGD**: Ben Arous--Gheissari--Jagannath 2022
   (general framework), Damian--Pillaud-Vivien--Lee--Bruna 2024
   (generative exponent definition), Lee--Oko--Suzuki--Wu 2024 (batch
   reuse and learning rate), Tsiolis et al. 2025 (this paper). Citing
   this work places our reasoning-time transition in a contemporary
   mathematical context.
2. **Specific scaling precedent.** They explicitly use $\eta \asymp
   d^{-1/2}$ in their main phase-transition statement (Theorem 3.3 in
   their paper), matching the scaling we recover in our numerical
   sanity check via the $\alpha(d) \sim \sqrt d$ parametrization. The
   conversion $\eta \cdot \|\nabla L\| \sim \alpha$ with $\|\nabla L\|
   \sim \sqrt d$ gives $\eta \sim \alpha / \sqrt d$ in their convention.

## Verification

Citation verified against arXiv (2510.21020, posted 2025-10-23, last
revised 2025-10-29). Author list, title, and abstract match. The
$\eta \asymp d^{-1/2}$ scaling and the information / generative
exponent dichotomy appear in the abstract and are formalized in their
Theorem 3.3 and Section 4.

The transitions they prove are for **sample complexity**, not for
**reasoning success probability** as in our setting; the analogy is
structural (sharp phase change as $\eta$ crosses a $d$-dependent
threshold), not literal.
