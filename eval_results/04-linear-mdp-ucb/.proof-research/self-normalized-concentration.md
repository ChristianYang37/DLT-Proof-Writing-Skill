# Self-Normalized Concentration for Vector-Valued Martingales

**Source.** Abbasi-Yadkori, Pál, Szepesvári (NeurIPS 2011), "Improved Algorithms for Linear Stochastic Bandits", Theorem 1 (page 5 of arXiv:1102.2670v3).

**Statement (faithful paraphrase).** Let $\{\mathcal{F}_t\}_{t \ge 0}$ be a filtration, $\{\eta_t\}_{t \ge 1}$ real-valued such that $\eta_t$ is $\mathcal{F}_t$-measurable and conditionally $R$-sub-Gaussian: $\E[e^{\lambda \eta_t} \mid \mathcal{F}_{t-1}] \le \exp(\lambda^2 R^2 / 2)$ for all $\lambda \in \R$. Let $\{X_t\}_{t \ge 1} \subset \R^d$ be $\mathcal{F}_{t-1}$-measurable (predictable). For any $\lambda > 0$, let $V_t = \lambda I + \sum_{s=1}^t X_s X_s^\top$ and $S_t = \sum_{s=1}^t \eta_s X_s$. Then with probability at least $1 - \delta$, for all $t \ge 0$,
$$\|S_t\|_{V_t^{-1}}^2 \;\le\; 2 R^2 \log\!\Bigl( \tfrac{\det(V_t)^{1/2} \det(\lambda I)^{-1/2}}{\delta} \Bigr).$$

**Hypotheses.**
- $\eta_t$ conditionally $R$-sub-Gaussian; $X_t$ predictable wrt $\mathcal{F}_{t-1}$; $\lambda > 0$.
- Uniform in $t \ge 0$ — the bound holds simultaneously for all $t$ on a single $1 - \delta$ event.

**Constants and dimension dependence.** $\log \det(V_t) \le d \log(1 + t L^2 / (d \lambda))$ if $\|X_t\| \le L$, yielding $\|S_t\|_{V_t^{-1}} \le R \sqrt{d \log((1 + tL^2/(d\lambda))/\delta)}$.

**Canonical use in LSVI-UCB (Jin et al. 2020, Lemma B.3).** Used to bound the value-iteration regression error $\|\widehat{w}_h^k - w_h^*\|_{\Lambda_h^k}$, where the noise comes from $V_{h+1}(s_{h+1}) - \E V_{h+1}(s_{h+1})$. Since $V_{h+1}$ depends on data, the standard Bernstein bound requires a covering argument over the function class $\mathcal{V}$ of plausible value functions; the per-function bound is then union-bounded over an $\varepsilon$-net.

**Common misuses.**
- Forgetting $V_{h+1}$ is data-dependent — covering argument over $\mathcal{V}$ is essential (Lemma D.4 of Jin et al.).
- Using non-predictable $X_t$ (e.g., $X_t = \phi(s_h^k, a_h^k)$ at step $t$ being the *current* step, not historical).
- Forgetting $V_t = \lambda I + \sum_{s \le t}$ uses the cumulative Gram matrix.

**Project citation key.** `\cite{abbasi2011improved}` (the self-normalized inequality).
