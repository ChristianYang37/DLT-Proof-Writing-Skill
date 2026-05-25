# Karimi, Nutini, and Schmidt, "Linear Convergence ... Under the Polyak-Lojasiewicz Condition" (2016)

## Reference

Karimi, Hamed and Nutini, Julie and Schmidt, Mark.
*Linear Convergence of Gradient and Proximal-Gradient Methods Under
the Polyak-Lojasiewicz Condition.*
In Machine Learning and Knowledge Discovery in Databases
(ECML PKDD 2016), Lecture Notes in Computer Science, vol. 9851,
pp. 795--811, Springer, 2016.
arXiv: 1608.04636.

## What is cited

We cite this paper for the **Polyak--{\L}ojasiewicz (PL) rate analysis**
used in \Cref{cor:pl_exponential_rate}. Specifically, the paper's
Theorem 1 gives, for any $L$-smooth function $F$ satisfying the PL
inequality
\[
   \tfrac{1}{2} \|\nabla F(x)\|^2 \;\ge\; \mu \, (F(x) - F^*)
\]
with constant $\mu > 0$, that gradient descent with step size
$\eta = 1/L$ achieves
\[
   F(x_t) - F^* \;\le\; (1 - \mu/L)^t \, (F(x_0) - F^*),
\]
i.e.\ a linear (geometric) rate of convergence to the global minimum,
without requiring convexity. The paper's Theorem 4 extends the analysis
to stochastic gradients with bounded variance.

For our biased-SGD-under-PL setting, we use the extension (sketched in
\S 4 of Karimi et al.\ and folded into \Cref{cor:pl_exponential_rate}):
under PL with constant $\mu$, $L$-smoothness, and biased SGD with bias
$\beta$ and second-moment bound $G^2$, constant-step-size SGD satisfies
\[
   \E[F(x_T) - F^*] \;\le\; (1 - c_3 \eta_0 \mu)^T (F(x_0) - F^*)
   + \frac{c_4 \beta^2}{\eta_0 \mu},
\]
i.e.\ geometric decay to a $\beta^2 / (\eta_0 \mu)$ floor.

## Why we cite it

The PL condition is the cleanest hypothesis under which
exponential-rate convergence holds without convexity. We use it to
state \Cref{cor:pl_exponential_rate}, which addresses the practitioner
regime where the $O(1/\sqrt T)$ main rate is too slow to be informative
at $T \le 10^5$ (see the sanity-check evidence in
`.proof-research/risk-2-sanity-check.md`). Karimi et al.\ is the
standard modern reference for PL with non-convex objectives and is
self-contained for the rates we need.

## Verification

Citation verified against the ECML-PKDD 2016 proceedings (LNCS vol. 9851)
and the arXiv preprint [arXiv:1608.04636](https://arxiv.org/abs/1608.04636).
Author list, title, and pagination match. The PL inequality, Theorem 1
(deterministic linear rate), and Theorem 4 (stochastic variant) appear
as stated.
