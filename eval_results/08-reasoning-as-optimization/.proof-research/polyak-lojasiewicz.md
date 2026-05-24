# Polyak–Łojasiewicz (PL) condition

**Source.** Polyak (1963), *Gradient methods for the minimization of
functionals*; Karimi–Nutini–Schmidt, *Linear Convergence of Gradient and
Proximal-Gradient Methods Under the Polyak–Łojasiewicz Condition*,
ECML-PKDD 2016 (arXiv:1608.04636) for the modern restatement and clean
proofs.

**Statement (PL inequality).** A differentiable function $F: \R^d \to \R$
with finite minimum $F^* = \inf_x F(x) > -\infty$ satisfies the PL condition
with constant $\mu > 0$ if for all $x \in \R^d$,
$$
   \tfrac{1}{2} \|\nabla F(x)\|^2 \;\ge\; \mu \big(F(x) - F^*\big).
$$
This implies $\mu$-strong-convexity-of-the-suboptimality-gap behaviour
without requiring convexity.

**Karimi-Nutini-Schmidt Theorem 1 (Cor.).** Under $L$-smoothness and PL with
constant $\mu$, gradient descent with step size $\eta = 1/L$ satisfies
$$
   F(x_t) - F^* \;\le\; \Big(1 - \frac{\mu}{L}\Big)^t \big(F(x_0) - F^*\big).
$$
For stochastic gradient with bounded variance $\sigma^2$, the same paper's
Theorem 4 gives $\E[F(x_t) - F^*] = \mathcal O(1/(\mu t))$ in expectation
with diminishing step sizes (Polyak averaging not required).

**Hypotheses (Theorem 1).**
- $F$ differentiable.
- $F$ is $L$-smooth: $\|\nabla F(x) - \nabla F(y)\| \le L \|x - y\|$.
- $F$ satisfies PL with constant $\mu$.
- For the stochastic variant: $\E[\hat g_t | \mathcal F_{t-1}] = \nabla F(x_{t-1})$
  and $\E\|\hat g_t - \nabla F(x_{t-1})\|^2 \le \sigma^2$.

**Why PL is attractive here.**
- Does **not** require convexity.
- Holds for the squared loss $\|f_\theta(x) - y\|^2$ when $f_\theta$ is in the
  NTK regime, for wide overparameterized neural networks (Du et al. 2019,
  Allen-Zhu-Li-Song 2019, ...).
- Empirically a defensible "implicit landscape" property of LLM inference if
  framed carefully.

**Why PL is also fragile here.**
- It must be PL with respect to a *specific potential $F$*. As discussed in
  `sgd-weight-decay-analogy.md`, the LLM's reasoning dynamics do not
  obviously gradient-descend any natural $F$.
- The hypothesis $\E[\hat g_t | \mathcal F_{t-1}] = \nabla F(x_{t-1})$ is
  unbiased SGD; the LLM's $g_j$ has no such unbiasedness property unless
  postulated.
- PL is a *global* condition — it must hold everywhere on the trajectory.
  Local-PL variants exist but require careful basin-of-attraction analysis.

**Common misuses.**
- Asserting PL on a domain where only convexity is known (PL implies
  invex-on-its-stationary-set, but not the other direction).
- Using PL with biased gradients without quantifying the bias contribution
  (in the bias term, smoothness + bias gives an additive penalty in the rate).
- Confusing PL with the (weaker) error-bound condition / quadratic-growth
  condition.

**Project citation key.** `\cite{karimi2016pl}` (Karimi-Nutini-Schmidt 2016)
for the modern reference; `\cite{polyak1963gradient}` for the original.

**Decision for THIS proof.**
- **Path B (Toeplitz):** PL is not needed. Drop the digest's relevance.
- **Path A (postulated potential):** PL is the cleanest hypothesis to give
  a linear / $1/T$ rate. But PL's $\mu$ is invisible from inference
  observations (it requires knowing $F$); so an Assumption stating "the
  implicit potential is PL with constant $\mu$" fails the sellability test
  (ii) — not testable from inference-time observations alone.

**Recommendation.** Avoid PL in the main route. If a Path-A "optimization
view" appendix is included for headline value, state PL as Assumption A2'
(secondary) marked with `\todo{verify: PL with respect to a postulated $F$;
practitioners cannot directly observe $\mu$}`.
