# DZPS one-step contraction algebra (discrete GD)

**Source.** Du–Zhai–Poczos–Singh (ICLR 2019), proof of Theorem 4.1 (discrete-time GD).

**Setup.** Residual $u(k)\in\R^n$, $u_i(k)=f_{W(k)}(x_i)$, $y$ labels, loss
$L(W)=\tfrac12\|y-u\|_2^2$. GD: $W(k+1)=W(k)-\eta\nabla L(W(k))$. Define the (time-varying)
Gram matrix $H(k)$ with
$H_{ij}(k)=\frac1m\sum_r x_i^\top x_j\,\mathbf 1\{w_r(k)^\top x_i\ge0,\,w_r(k)^\top x_j\ge0\}$.

**One-step residual identity.** A first-order expansion of $u(k+1)-u(k)$ along the GD step
gives, with ReLU,
$u(k+1) - u(k) = -\eta H(k)(u(k)-y) + \varepsilon(k)$,
where $\varepsilon(k)$ is the second-order remainder from neurons that flip activation pattern
between $W(k)$ and $W(k+1)$.

**Residual recursion.** Therefore
$\|y-u(k+1)\|_2^2 = \|y-u(k)\|_2^2 - 2\eta (y-u(k))^\top H(k)(y-u(k))
+ \eta^2\|H(k)(y-u(k))\|^2 + \langle\text{cross terms with }\varepsilon\rangle$.
Bounding the middle term below by $2\eta\lambda_{\min}(H(k))\|y-u(k)\|^2$, the $\eta^2$ term
above by $\eta^2 n^2\|y-u(k)\|^2$ (since $\|H(k)\|_2\le n$, as $|H_{ij}|\le1$ entrywise), and the
remainder by lower-order terms controlled by the width, one obtains:
if $\lambda_{\min}(H(k))\ge\lambda_0/2$ and $\eta\le\lambda_0/(2n^2)$, then
$\|y-u(k+1)\|_2^2 \le (1-\eta\lambda_0/2)\,\|y-u(k)\|_2^2$.

**Weight-movement bound.** Per-neuron gradient
$\big\|\frac{\partial L}{\partial w_r}\big\|
= \big\|\frac1{\sqrt m}\sum_i (u_i-y_i)a_r\sigma'(w_r^\top x_i)x_i\big\|
\le \frac1{\sqrt m}\sum_i|u_i-y_i| \le \frac{\sqrt n}{\sqrt m}\|y-u(k)\|_2$,
using $|a_r|=1$, $|\sigma'|\le1$, $\|x_i\|=1$, and Cauchy–Schwarz on $\sum_i|u_i-y_i|$.
Summing along the trajectory with the geometric residual decay:
$\|w_r(k)-w_r(0)\| \le \eta\sum_{s<k}\big\|\tfrac{\partial L}{\partial w_r}(s)\big\|
\le \frac{\eta\sqrt n}{\sqrt m}\sum_{s\ge0}(1-\eta\lambda_0/2)^{s/2}\|y-u(0)\|
\le \frac{4\sqrt n\,\|y-u(0)\|}{\sqrt m\,\lambda_0}$,
using $\sum_{s\ge0}(1-\eta\lambda_0/2)^{s/2}\le \frac{2}{1-(1-\eta\lambda_0/2)^{1/2}}\le\frac{4}{\eta\lambda_0}$
(since $1-\sqrt{1-x}\ge x/2$ for $x\in[0,1]$), and the $\eta$ cancels.

**Initial residual bound.** $\|y-u(0)\|_2^2 = O(n)$ w.p. $\ge1-\delta$: each $u_i(0)$ is mean-zero
with $O(1)$ variance by the $\pm1$ symmetry of $a_r$ (conditioned on $W(0)$), so
$\E\|y-u(0)\|^2 = \|y\|^2 + \sum_i\E u_i(0)^2 = O(n)$ for $O(1)$ labels; Markov gives the bound.
Hence $\|w_r(k)-w_r(0)\| \le \frac{4\sqrt n\cdot O(\sqrt n)}{\sqrt m\,\lambda_0}
= O\!\big(\frac{n}{\sqrt m\,\lambda_0}\big)$, which is $\le R=\Theta(\delta\lambda_0/n^2)$ once
$m \ge \mathrm{poly}(n,1/\lambda_0,1/\delta)$.

**Constants / dimension dependence.** Contraction factor $1-\eta\lambda_0/2$; step
$\eta=O(\lambda_0/n^2)$; the $\eta^2$ term needs $\eta\le\lambda_0/(2\|H\|_2^2)$ and $\|H\|_2\le n$.

**Common misuses.**
- Dropping the $\eta^2$ term without checking $\eta\le\lambda_0/(2n^2)$.
- Forgetting that $\lambda_{\min}(H(k))\ge\lambda_0/2$ is an *inductive* hypothesis maintained
  by the stay-in-ball argument — secured by the fixed-point / contradiction closure.
- Using $\|H\|_2\le n$ loosely: it follows from $|H_{ij}|\le1$ and $\|H\|_2\le\|H\|_F\le n$.

**Project citation.** \cite{du2019gradient} (structure attribution; algebra reproduced).
