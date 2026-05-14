# Elliptical Potential Lemma

**Source.** Abbasi-Yadkori, Pál, Szepesvári (NeurIPS 2011), "Improved Algorithms for Linear Stochastic Bandits", Lemma 11 (page 16 of arXiv:1102.2670v3); also Lemma 19.4 in Lattimore & Szepesvári, *Bandit Algorithms* (CUP 2020).

**Statement (faithful paraphrase).** Let $\{\phi_t\}_{t=1}^T \subset \mathbb{R}^d$ with $\|\phi_t\|_2 \le 1$, and let $\Lambda_t = \lambda I + \sum_{s=1}^{t-1} \phi_s \phi_s^\top$ with $\lambda \ge 1$. Then
$$\sum_{t=1}^T \min\bigl\{1,\, \|\phi_t\|_{\Lambda_t^{-1}}^2 \bigr\} \;\le\; 2 \log \det(\Lambda_{T+1}) - 2 \log \det(\lambda I) \;\le\; 2 d \log\!\Bigl(1 + \tfrac{T}{d\lambda}\Bigr).$$
Combined with Cauchy–Schwarz,
$$\sum_{t=1}^T \min\bigl\{1, \|\phi_t\|_{\Lambda_t^{-1}}\bigr\} \;\le\; \sqrt{T \cdot 2 d \log(1 + T/(d\lambda))}.$$

**Hypotheses.**
- $\|\phi_t\|_2 \le 1$ for all $t$ (else: replace bound by $\le 2 d \log(1 + T L^2 / (d\lambda))$ for $\|\phi_t\| \le L$).
- $\lambda \ge 1$ so that $\Lambda_t \succeq I$ (else: $\min\{1, \cdot\}$ truncation still holds, constants change).
- $\Lambda_t$ uses *past* features only (predictable filtration).

**Constants and dimension dependence.** The leading factor is $2 d \log(1 + T/(d\lambda))$. Hidden in $\widetilde{O}$. No dimension factor beyond the $d$ inside the log.

**Canonical use pattern in LSVI-UCB regret proof (Jin et al. 2020, Lemma B.4 / D.2).**
```latex
By the elliptical-potential lemma (\Cref{lem:elliptical}),
\begin{align*}
\sum_{k=1}^K \sum_{h=1}^H \min\bigl\{1, \|\phi(s_h^k, a_h^k)\|_{\Lambda_h^k{}^{-1}}\bigr\}
&\le H \sqrt{K \cdot 2 d \log(1 + K/(d\lambda))} \\
&= O\bigl(\sqrt{H^2 K d \iota}\bigr),
\end{align*}
where $\iota = \log(\cdot)$ collects log factors.
```

**Common misuses.**
- Forgetting the $\min\{1, \cdot\}$ truncation: without it the sum is only bounded when $\|\phi_t\|_{\Lambda_t^{-1}} \le 1$ a.s.
- Using $\Lambda_t$ that includes $\phi_t$ (non-predictable): the inequality fails — must use past Gram matrix.
- Forgetting Cauchy–Schwarz step: the lemma bounds $\sum \min\{1, \|\cdot\|^2\}$, not $\sum \|\cdot\|$ directly.

**Project citation key.** `\cite{abbasi2011improved}`
