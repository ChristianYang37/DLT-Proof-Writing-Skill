# KL divergence between Gaussian fixed-design regression measures

**Source.** Standard; e.g. Tsybakov, *Introduction to Nonparametric
Estimation*, 2009, §2.4 (Gaussian-noise computations). Self-contained
one-line computation from the multivariate-Gaussian KL formula.

**Statement.** Fix design points $x_1,\dots,x_n$. Under regression functions
$f$ and $g$, the data is $y_i = f(x_i)+\xi_i$ resp. $y_i=g(x_i)+\xi_i$ with
$\xi_i\sim\mathcal N(0,\sigma^2)$ i.i.d. Then the data laws $P_f,P_g$ are
product Gaussians $\bigotimes_i \mathcal N(f(x_i),\sigma^2)$ resp.
$\bigotimes_i \mathcal N(g(x_i),\sigma^2)$, and
$$\KL(P_f\,\|\,P_g)
= \sum_{i=1}^n \KL\!\big(\mathcal N(f(x_i),\sigma^2)\,\|\,\mathcal N(g(x_i),\sigma^2)\big)
= \frac{1}{2\sigma^2}\sum_{i=1}^n \big(f(x_i)-g(x_i)\big)^2.$$

**Hypotheses.**
- Same design $x_1,\dots,x_n$ under both laws (only the mean shifts).
- Same known variance $\sigma^2$ under both laws (so the variance terms in
  the univariate Gaussian KL cancel, leaving only the mean-shift term).
- Independence across $i$ (tensorization: KL of a product is the sum of KLs).

**Constants and dimension dependence.** Exact, no hidden constants. The
univariate fact $\KL(\mathcal N(\mu_1,\sigma^2)\|\mathcal N(\mu_2,\sigma^2))
=(\mu_1-\mu_2)^2/(2\sigma^2)$ has no slack.

**Canonical use pattern.** Combine with the fixed-design grid: for localized
bumps $u_k$,
$\sum_i (u_k(x_i)-u_{k'}(x_i))^2 \le n\cdot \|u_k-u_{k'}\|_{L^2}^2 \cdot
(1+o(1))$ up to grid-regularity constants, so
$\KL \lesssim \frac{n}{\sigma^2}\|u_k-u_{k'}\|_{L^2}^2$.

**Common misuses.**
- Using the random-design KL (which would average over the design law) for a
  fixed design.
- Forgetting that differing variances add a $\frac12(\sigma_1^2/\sigma_2^2 -
  1 - \log\cdots)$ term — not present here since variances match.

**Project citation key.** No dedicated cite needed; restated inline as a
`\begin{fact}` and proved in one line. (`\cite{tsybakov2009introduction}`
also covers it.)
