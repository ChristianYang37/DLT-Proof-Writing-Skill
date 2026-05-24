# ReLU gradient norm bound and per-neuron gradient

For $f(\Wb, \ab, \xb) = \tfrac{1}{\sqrt m} \sum_{r=1}^m a_r \sigma(\wb_r^\top \xb)$ with $\sigma(z) = \max(z, 0)$:

**Gradient w.r.t. $\wb_r$.**
\[
\frac{\partial f(\Wb, \ab, \xb_i)}{\partial \wb_r}
\;=\; \tfrac{a_r}{\sqrt m} \, \mathbf 1\!\big[ \wb_r^\top \xb_i \ge 0 \big] \, \xb_i.
\]
Note ReLU is non-differentiable at 0; we treat $\sigma'(0) = 0$ by convention (the set where this matters has zero Lebesgue measure under continuous initialization).

**Per-neuron gradient norm of the loss.** With $L = \tfrac12 \sum_i (f_i - y_i)^2$ and $\ub_i := f(\Wb, \ab, \xb_i)$:
\[
\frac{\partial L}{\partial \wb_r}
\;=\; \sum_{i=1}^n (\ub_i - y_i) \cdot \tfrac{a_r}{\sqrt m} \, \mathbf 1\!\big[ \wb_r^\top \xb_i \ge 0 \big] \, \xb_i.
\]

Triangle inequality + $|a_r| = 1$ + $\|\xb_i\|=1$:
\[
\Big\| \frac{\partial L}{\partial \wb_r} \Big\|_2
\;\le\; \tfrac{1}{\sqrt m} \sum_{i=1}^n |\ub_i - y_i|
\;\le\; \tfrac{\sqrt n}{\sqrt m} \|\ub - \yb\|_2,
\]
by Cauchy-Schwarz on the second inequality.

**Use.** This bound feeds into the perturbation-from-init estimate $\|\wb_r(t) - \wb_r(0)\|_2 \le \eta \sum_{s<t} \|\nabla_{\wb_r} L(s)\|_2$. Telescoping with the linear-convergence inductive hypothesis $\|\ub(s) - \yb\|_2 \le (1 - \eta\lambda_0/2)^{s/2} \|\ub(0) - \yb\|_2$ yields the standard $\|\wb_r(t) - \wb_r(0)\|_2 \le 4\sqrt n \|\ub(0) - \yb\|_2 / (\sqrt m \lambda_0)$.

**Common misuses.**
- Forgetting the $1/\sqrt m$ scaling on the gradient.
- Forgetting that $\sigma'$ takes values in $\{0,1\}$ and bounds it accordingly.
- Confusing $\partial / \partial \wb_r$ (one neuron) with $\partial / \partial \Wb$ (full Jacobian).
