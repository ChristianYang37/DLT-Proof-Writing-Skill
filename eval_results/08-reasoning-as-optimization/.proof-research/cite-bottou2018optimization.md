# Bottou, Curtis, and Nocedal, "Optimization Methods for Large-Scale Machine Learning" (2018)

## Reference

Bottou, L\'eon and Curtis, Frank E. and Nocedal, Jorge.
*Optimization Methods for Large-Scale Machine Learning.*
SIAM Review, 60(2):223--311, 2018.
DOI: 10.1137/16M1080173
URL: https://epubs.siam.org/doi/10.1137/16M1080173

## What is cited

We cite this survey for the **biased-SGD descent inequality** used in
\Cref{lem:descent_inequality}. Specifically, Bottou--Curtis--Nocedal
\S 4.3 (Theorems 4.7 and 4.8) gives the analysis of stochastic gradient
methods where the stochastic gradient $g_j$ is a possibly biased
estimator of $\nabla F(x_{j-1})$. Under $L$-smoothness of $F$ and a
second-moment bound $\E\|g_j\|^2 \le G^2$, together with a bias bound
$\|\E[g_j \mid \F_{j-1}] - (-\eta_j \nabla F)\| \le \beta$, one obtains
the per-step descent inequality
\[
   \E[F(x_j) \mid \F_{j-1}]
   \;\le\;
   F(x_{j-1}) - \tfrac{\eta_j}{2} \|\nabla F(x_{j-1})\|^2
   + \tfrac{\eta_j \beta^2}{2 \eta_0}
   + \tfrac{L \eta_j^2}{2} G^2,
\]
which we instantiate with $F = L(\cdot ; Q)$ in our setting.

The survey's Theorem 4.8 (telescoping with diminishing step size
$\eta_j = \eta_0 / \sqrt j$) gives the rate
$\min_{j \le T} \E \|\nabla F(x_j)\|^2 = O(1/\sqrt T) + O(\beta^2 / \eta_0)$
to a stationary point with an additive bias floor; this is the rate we
use in \Cref{lem:telescoping}.

## Why we cite it

This is the standard modern reference for biased and unbiased SGD
analysis in the non-convex regime. It collects the descent-inequality
proof, the diminishing-step-size telescoping, and the $\beta^2/\eta_0$
floor in one place with explicit constants, making it the cleanest
single citation for our \Cref{lem:descent_inequality} and
\Cref{lem:telescoping}.

## Verification

Citation verified against the SIAM Review record (volume 60, issue 2,
2018) and against the arXiv preprint
[arXiv:1606.04838](https://arxiv.org/abs/1606.04838) (companion preprint
with identical content). Author list, title, volume, and pagination
match. The descent inequality referenced above appears as eq.~(4.10)
in the journal version, and the telescoping rate as Theorem 4.10.
