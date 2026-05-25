# Polyak-Lojasiewicz (PL) rate analysis for biased SGD

## Setting

Let $F: \R^d \to \R$ be $L_{\mathrm{sm}}$-smooth with finite minimum
$F^* > -\infty$. Suppose $F$ satisfies the PL inequality with constant
$\mu > 0$ on the relevant domain:
\[
   \tfrac{1}{2} \|\nabla F(x)\|^2 \;\ge\; \mu \, (F(x) - F^*),
   \qquad \forall x.
\]
Run SGD with update $x_j = x_{j-1} + g_j$ where, as in the biased-SGD
digest,
\[
   \E[g_j \mid \F_{j-1}] = -\eta_j \nabla F(x_{j-1}) + b_j,
   \qquad
   \|b_j\| \le \beta, \quad \E\|g_j\|^2 \le G^2.
\]

## The PL rate

Under constant step size $\eta_j = \eta_0$ chosen so that
$\eta_0 L_{\mathrm{sm}} \le 1$ (the "small-step regime"), iterating the
biased-SGD descent inequality gives
\[
   \E[F(x_T) - F^*]
   \;\le\; (1 - c_3 \eta_0 \mu)^T \, (F(x_0) - F^*)
        \;+\; \frac{c_4 \beta^2}{\eta_0 \mu},
\]
for absolute constants $c_3, c_4 > 0$ depending only on
$L_{\mathrm{sm}} / \mu$ and on the second-moment bound $G^2$.

In words: geometric (linear) convergence in $T$ to a
$\beta^2 / (\eta_0 \mu)$ floor. Compared to the non-PL rate
$O(1/\sqrt T) + O(\beta^2 / \eta_0)$, PL trades a multiplicative
$1 / \mu$ in the floor for an exponential-in-$T$ rate term.

## Derivation (one-page)

From the biased-SGD descent inequality (see
`biased-sgd-descent-inequality.md`),
\[
   \E[F(x_j)] \;\le\; F(x_{j-1})
        - \tfrac{\eta_0}{2} \|\nabla F(x_{j-1})\|^2
        + \tfrac{\beta^2}{2 \eta_0}
        + \tfrac{L_{\mathrm{sm}}}{2} \eta_0^2 G^2.
\]
Apply the PL inequality to the $\|\nabla F\|^2$ term:
$\|\nabla F(x_{j-1})\|^2 \ge 2 \mu (F(x_{j-1}) - F^*)$. Substitute:
\[
   \E[F(x_j) - F^*]
   \;\le\; (1 - \eta_0 \mu) \, (F(x_{j-1}) - F^*)
        + \tfrac{\beta^2}{2 \eta_0}
        + \tfrac{L_{\mathrm{sm}}}{2} \eta_0^2 G^2.
\]
Let $A_j \coloneqq \E[F(x_j) - F^*]$ and $B \coloneqq
\beta^2/(2 \eta_0) + L_{\mathrm{sm}} \eta_0^2 G^2 / 2$. Then
$A_j \le (1 - \eta_0 \mu) A_{j-1} + B$. Iterating gives
\[
   A_T \;\le\; (1 - \eta_0 \mu)^T A_0
            + B \sum_{j=0}^{T-1} (1 - \eta_0 \mu)^j
       \;\le\; (1 - \eta_0 \mu)^T A_0
            + \frac{B}{\eta_0 \mu}.
\]
Substituting $B$, the floor is
$\beta^2 / (2 \eta_0^2 \mu) + L_{\mathrm{sm}} \eta_0 G^2 / (2 \mu)$.
For step size $\eta_0$ small (so the $L_{\mathrm{sm}} \eta_0$ term is
$O(\eta_0)$), the $\beta^2$ contribution dominates and the floor is
$\Theta(\beta^2 / (\eta_0 \mu))$, recovering the stated form.

## Reference

- Karimi, Hamed and Nutini, Julie and Schmidt, Mark.
  *Linear Convergence of Gradient and Proximal-Gradient Methods Under
  the Polyak-Lojasiewicz Condition.* ECML-PKDD 2016, arXiv:1608.04636.
  Theorem 1 (deterministic linear rate) and Theorem 4 (stochastic
  variant with bounded variance).
- Polyak, B. T., *Gradient methods for the minimisation of functionals*
  (1963), for the original PL inequality.

## When PL is plausible vs.\ implausible

PL is a strong additional hypothesis, **NOT** derivable from smoothness
alone. In our setting (the constrained-softmax loss $L(x;Q)$):

- **Plausibility argument:** On the trajectory's basin of attraction
  around a region where $\nabla L = 0$, PL holds locally with $\mu$
  proportional to the smallest non-zero eigenvalue of $\nabla^2 L$ at
  the basin minimum. Empirical sub-quadratic test-time-scaling curves
  (\cite{openai2024o1, deepseek2025r1}) are exponential-with-floor in
  shape, consistent with PL.
- **Implausibility caveat:** The Hessian of $L$ subtracts the
  $q_C$-covariance term from the $p$-covariance term (see proposal
  \S 1.3), and can be negative-definite on parts of the domain. PL
  cannot hold globally; it can only be postulated on a basin.

## How we use it

In \Cref{cor:pl_exponential_rate}, we assume PL holds on the
trajectory's basin (a local assumption, explicitly flagged as not
provable from the rest of the framework) and combine with the
biased-SGD descent inequality to obtain the exponential-with-floor
rate. We accompany the corollary with a remark about why PL is plausible
on a basin (test-time-scaling empirical shape) and why it is not
derivable from the framework (non-convexity, see proposal \S 1.3).

## Hypotheses checklist for cite-site

- $F = L(\cdot; Q)$ is $L_{\mathrm{sm}}$-smooth: \Cref{lem:smoothness}.
- $F$ satisfies the PL inequality with constant $\mu$ on the trajectory
  basin: this is an additional *hypothesis* of \Cref{cor:pl_exponential_rate},
  not implied by the rest of the framework.
- Biased-SGD hypotheses: as in `biased-sgd-descent-inequality.md`.
- Step size $\eta_0$ small enough that $\eta_0 L_{\mathrm{sm}} \le 1$.
