# \cite{abbasi2011improved} — self-normalized bound + elliptical potential

**Paper.** "Improved Algorithms for Linear Stochastic Bandits", Yasin
Abbasi-Yadkori, David Pal, Csaba Szepesvari. NeurIPS 2011. arXiv:1102.6557.

**Exact names in PDF.**
- "Theorem 1" — self-normalized bound for vector-valued martingales (p. 3).
- "Lemma 11" — the determinant-trace / elliptical-potential inequality
  $\sum_{t=1}^n \min(1,\|x_t\|_{V_{t-1}^{-1}}^2) \le 2\log(\det V_n/\det V_0)$
  (also reproduced as Lemma 19.4 in Lattimore-Szepesvari, *Bandit Algorithms*,
  2020, and as Lemma D.2 in Jin-Yang-Wang-Jordan 2020).

**Statement (Theorem 1, self-normalized).** For an $\mathcal F_t$-adapted
$\sigma$-sub-Gaussian noise $\{\eta_t\}$ and predictable $\{X_t\}\subset\mathbb
R^d$, with $\bar V_t=\lambda I+\sum_{s\le t}X_s X_s^\top$, for all $\delta>0$ with
probability $\ge 1-\delta$, for all $t\ge0$:
$\|\sum_{s=1}^t X_s\eta_s\|_{\bar V_t^{-1}}^2 \le 2\sigma^2\log\frac{\det(\bar
V_t)^{1/2}\det(\lambda I)^{-1/2}}{\delta}.$

**Statement (Lemma 11, elliptical potential).** If $\|X_t\|\le L$ and $\bar
V_t=\lambda I+\sum_{s\le t}X_sX_s^\top$, then
$\sum_{t=1}^n \|X_t\|_{\bar V_{t-1}^{-1}}^2 \le 2\log\frac{\det\bar V_n}{\det\bar
V_0} \le 2d\log\frac{\lambda d + nL^2}{\lambda d}.$

**Hypotheses.** sub-Gaussian conditionally-centered noise; predictable
regressors; $\lambda>0$ regularizer. For the log-det $\le$ trace step the
$\|X_t\|\le L$ bound is used.

**Constants / dimension dependence.** $d\log(\cdot)$ in the potential; the
self-normalized bound carries $\sqrt{\log\det/\delta}$, i.e. $\sqrt d$ before
covering arguments. Constants are absolute (the 2's are explicit).

**Project .bib key.** \cite{abbasi2011improved}
