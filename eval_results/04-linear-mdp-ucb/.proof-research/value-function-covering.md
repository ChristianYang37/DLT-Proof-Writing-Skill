# Covering Argument over Value-Function Class

**Source.** Jin–Yang–Wang–Jordan (COLT 2020) Lemma D.4 (page 23 of arXiv:1907.05388v2). Related: Russo–Van Roy 2013 ("Eluder Dimension"), Wang–Salakhutdinov–Yang NeurIPS 2020 ("Provably Efficient Reinforcement Learning with General Value Function Approximation").

**Statement (faithful paraphrase).** Let $\mathcal{V}$ be the class of value functions of the form
$$V(s) = \min\!\bigl\{ \max_a [ \phi(s,a)^\top w + \beta \|\phi(s,a)\|_{\Lambda^{-1}} ], \, H \bigr\},$$
with $\|w\| \le L$, $\beta \in [0, B]$, and $\Lambda \succeq \lambda I$. Then for any $\varepsilon > 0$, the $\varepsilon$-covering number $\mathcal{N}_\varepsilon$ of $\mathcal{V}$ in $\|\cdot\|_\infty$ satisfies
$$\log \mathcal{N}_\varepsilon \;\le\; d \log(1 + 4 L / \varepsilon) + d^2 \log\!\bigl(1 + 8 d^{1/2} B^2 / (\lambda \varepsilon^2)\bigr).$$
In particular, taking $\varepsilon = 1/K$ gives $\log \mathcal{N}_\varepsilon = O(d^2 \log(dKB/\lambda))$.

**Why we need it.** The standard self-normalized concentration (Abbasi-Yadkori 2011 Thm 1) requires the regression target to be independent of the past — but in LSVI-UCB, the regression target $V_{h+1}^k$ depends on past data. The covering argument circumvents this: we union-bound over a fixed $\varepsilon$-net of *plausible* value functions, then use the closest net element to the actual target.

**Hypotheses.**
- $\|w\| \le L$ (bounded weight vector) — comes from $\|w_h^k\| \le H \sqrt{dK/\lambda}$ (Jin et al. Lemma B.2).
- $\beta \in [0, B]$ bounded — our $\beta = O(dH\sqrt{\iota})$.
- $\Lambda \succeq \lambda I$ — standard regularization.

**Canonical use pattern.**
```latex
By Lemma~\ref{lem:cover_V}, there exists a finite $\varepsilon$-cover $\mathcal{N}_\varepsilon$ of
$\mathcal{V}$ in $\|\cdot\|_\infty$ with $|\mathcal{N}_\varepsilon| \le \exp(C d^2 \log(\cdot))$.
For each $\widetilde{V} \in \mathcal{N}_\varepsilon$, apply the self-normalized inequality at
confidence $\delta / |\mathcal{N}_\varepsilon|$. By a union bound, with probability $1 - \delta$,
\[
\Big\| \sum_{s} \phi(s,a)\bigl(\widetilde{V}(s') - \E \widetilde{V}\bigr) \Big\|_{\Lambda^{-1}}
\le C H \sqrt{d \log( \mathcal{N}_\varepsilon / \delta )}.
\]
Taking $\varepsilon = 1/K$ closes the gap to the actual $V_{h+1}^k$.
```

**Common misuses.**
- Forgetting the covering and applying self-normalized directly: invalid since $V_{h+1}^k$ is not predictable.
- Net resolution too coarse: $\varepsilon$ must be $\le 1/K$ or the residual term dominates.
- Forgetting to bound $\|w_h^k\|$ — required to make the net finite.

**Project citation key.** `\cite{jin2020provably}` (we cite the paper for the lemma).
