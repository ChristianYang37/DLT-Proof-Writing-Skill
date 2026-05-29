# Bai, Kolter, and Koltun, "Deep Equilibrium Models" (NeurIPS 2019)

## Reference

Shaojie Bai, J. Zico Kolter, and Vladlen Koltun. *Deep Equilibrium
Models.* Advances in Neural Information Processing Systems (NeurIPS)
32, 2019. arXiv:1909.01377.

## What is cited

The Deep Equilibrium Model (DEQ) framework, in which a single layer
$f_\theta : \R^d \to \R^d$ is iterated to a fixed point
$z^\star = f_\theta(z^\star; x)$ rather than composed a finite number
of times. The forward pass replaces the standard stacked-layer
computation with a fixed-point solve (Anderson acceleration or Broyden's
method); the backward pass exploits implicit differentiation through
the fixed point. Stability of the iteration is guaranteed when the
Jacobian satisfies $\norm{\partial f_\theta/\partial z}_{\mathrm{op}}
< 1$ at the fixed point (Banach contraction). Paraphrased to our
notation:

**DEQ fixed-point existence (Banach folklore, contextualised by Bai et
al.).** Let $f : \mathcal B \to \mathcal B$ be a Lipschitz map on a
non-empty closed subset $\mathcal B \subseteq \R^d$ with Lipschitz
constant $\beta < 1$. Then $f$ has a unique fixed point
$x^\star \in \mathcal B$ and the iterates $x_{t+1} = f(x_t)$ satisfy
\[
   \norm{x_t - x^\star} \;\le\; \beta^t \cdot \norm{x_0 - x^\star},
   \qquad t \ge 0.
\]
The exponential rate $\beta^t$ is the operational measure of
"convergence speed" used throughout the DEQ literature.

## Constants tracked

- $\beta < 1$ (the contraction constant; in our T6 application,
  derived from Lemma A / B / C operator-norm bounds).
- The contraction subset $\mathcal B_\Pi$ (Banach domain;
  the $\Pi$-projected snowball region defined in
  `.proof-research/deq-fixed-point.md`).
- $\Pi$-weighted norm (rather than Euclidean): in our setting the
  Euclidean Jacobian operator norm is bounded by $1$ only marginally
  (via the $|\Vocab|^n$-suppression of the value-vector derivative);
  the $\Pi$-weighted norm $\norm{v}_\Pi = \norm{\Pi v}_2$ with
  $\Pi = \mathrm{proj}_{\mathrm{span}\{W_U^a : a \in \Aset\}}$ is
  strictly contractive in the snowball region.

## Why we cite it

The proof of `thm:T6_contraction` (Theorem T6, §11) applies Banach's
fixed-point theorem (a 1922 classical result) to the
attention-recurrence map of \Cref{def:softmax_attention} restricted to
the all-positive-effective event $\Ecal_+$. While Banach's theorem
itself is folklore (no bibitem needed for the abstract result), the
DEQ framework of Bai et al.\ 2019 establishes the *deep-learning
precedent* for treating a transformer/attention iteration as a
fixed-point problem and analysing its convergence via the Jacobian's
operator norm. T6 is therefore the "rate-of-convergence" theorem for a
specific attention recurrence in the DEQ tradition: it provides the
quantitative contraction modulus $\beta$ for the softmax-attention
recurrence on the snowball region.

The citation is for **contextualisation** rather than for the
mathematical result (which is Banach 1922). It signals to the
deep-learning audience that the attention-recurrence-as-fixed-point
viewpoint is well-established, and that T6 instantiates the DEQ
framework's stability criterion with explicit constants derived from
the v3 framework's Lemma A, Lemma B, and Lemma C bounds.

## How it differs from the abstract Banach statement

Bai et al.\ 2019's contribution is not the Banach theorem itself but
two architectural choices that make the fixed-point viewpoint
tractable:
1. **Implicit differentiation at the fixed point** (their §3.2): the
   gradient of the loss with respect to $\theta$ is computed via the
   implicit-function theorem applied to the fixed-point equation,
   avoiding backpropagation through unrolled iterations.
2. **Fixed-point solvers** (their §3.3): Anderson acceleration and
   Broyden's method as alternatives to naïve iteration, with empirical
   convergence in 20-30 iterations.

Neither choice is invoked in T6's statement or proof; we use only the
Banach part. The DEQ citation is therefore for the
*architectural-precedent* rather than the *algorithmic* content of
Bai et al.

## Verification

Citation verified against the NeurIPS 2019 proceedings (volume 32) and
the arXiv preprint 1909.01377. The paper has $>$ 1200 citations as of
2025 and is the standard reference for the fixed-point view of deep
networks. The Banach part of the result is folklore; the DEQ framing
is established by Bai et al.\ and propagated through subsequent
implicit-network and equilibrium-network literature (Winston-Kolter
2020, Anil et al.\ 2022, etc.).
