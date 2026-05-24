# Lipschitz constants: softmax and the softmax-entropy composition

## Softmax Lipschitz in $\ell_2$

The softmax map $\softmax: \R^n \to \Delta^n$, defined as
$\softmax(\mathbf z)_i = e^{z_i} / \sum_j e^{z_j}$, has Jacobian
$$
J(\mathbf z) = \mathrm{diag}(p) - p p^\top, \qquad p \coloneqq \softmax(\mathbf z).
$$
Since $J$ is a symmetric matrix with non-negative spectrum, its
operator norm equals its largest eigenvalue. We have
$\norm{J}_{\mathrm{op}} = \lambda_{\max}(\mathrm{diag}(p) - p p^\top)
\le \max_i p_i \le 1$. A sharper bound: $\lambda_{\max}(\mathrm{diag}(p) - p p^\top) \le 1/4$
because the off-diagonal entries are $-p_i p_j \le 0$ and the trace is
$\sum_i p_i(1 - p_i) \le n/4$ at uniform $p$, but pointwise
$\max_i p_i (1 - p_i) \le 1/4$. So $\softmax$ is $1$-Lipschitz in $\ell_2$
(in fact $1/4$-Lipschitz, but $1$ is the standard usage).

Reference: Gao and Pavel, "On the properties of the softmax function
with application in game theory and reinforcement learning,"
arXiv:1704.00805 (2017), Proposition 4.
Also: Boyd and Vandenberghe, *Convex Optimization* (2004), §3.1.5.

## Entropy Lipschitz on the simplex

The Shannon entropy $H: \Delta^n \to \R$, $H(p) = -\sum_i p_i \log p_i$,
has gradient $\nabla H(p)_i = -\log p_i - 1$ (in the interior of the
simplex), which is unbounded as $p_i \to 0$. Hence $H$ is *not* globally
Lipschitz on $\Delta^n$.

However, on the *image* of $\softmax: \R^n \to \Delta^n$, points are
bounded away from the simplex boundary: $\softmax(\mathbf z)_i \ge e^{-2 \norm{\mathbf z}_\infty}/n$
for any $\mathbf z \in \R^n$. So on the relevant "softmax-reachable"
sub-simplex, the entropy is Lipschitz with constant
$L_H = \max_i |\log(\softmax(\mathbf z)_i) + 1|$ which is bounded by
$2 \norm{\mathbf z}_\infty + \log n + 1$.

For our application, we work in the regime where the inputs
$\mathbf z = W_U x$ have bounded norm: $\norm{W_U x}_2 \le B_U \norm{x}_2$,
and $\norm{x}$ stays in a finite range (bounded by $M + \norm{V^*(Q)}$
for $x$ on the convex hull of values).

## Composition: $\mathbf z \mapsto H(\softmax(\mathbf z))$

Composing, the map $\mathbf z \mapsto H(\softmax(\mathbf z))$ is
Lipschitz on any bounded ball $\{\mathbf z : \norm{\mathbf z}_2 \le R\}$,
with constant
$$
L_{\mathrm{sm}}(R) \;=\; (2R + \log n + 1) \cdot 1
\;=\; 2R + \log n + 1.
$$
For our application, $R = B_U (M + \max_{Q \in F} \norm{V^*(Q)})$ is a
trained-model constant, so $L_{\mathrm{sm}}$ is finite and computable
once the model is fixed.

## Hypotheses for our cite-site

In the proof of \Cref{cor:entropy_decay} we use this in the form: the
map $\mathbf x \mapsto H(\softmax(W_U \mathbf x))$ is Lipschitz with
constant $L_{\mathrm{sm}} B_U$ on a ball containing both $x_T$ and
$V^*(Q)$. This holds because $x_T$ is in the convex hull of values
(hence $\norm{x_T} \le M$) and $\norm{V^*(Q)} \le \max_Q \norm{V^*(Q)}$,
both bounded uniformly in $T$ and in the trajectory realisation.

## References

- Gao and Pavel, arXiv:1704.00805, Proposition 4 (softmax 1-Lipschitz).
- Boyd and Vandenberghe, *Convex Optimization*, §3.1.5.
- Standard entropy Lipschitz: any textbook on information theory, e.g.\
  Cover and Thomas, *Elements of Information Theory* (2006), §2.3.
