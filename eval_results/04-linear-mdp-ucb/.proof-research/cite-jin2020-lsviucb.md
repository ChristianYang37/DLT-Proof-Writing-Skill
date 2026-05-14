# \cite{jin2020provably} — LSVI-UCB main theorem

**Paper.** "Provably Efficient Reinforcement Learning with Linear Function Approximation", Chi Jin, Zhuoran Yang, Zhaoran Wang, Michael I. Jordan, COLT 2020, arXiv:1907.05388, pages 1–35.

**Exact name in PDF.** "Theorem 3.1" (regret bound, page 5 of arXiv v2).

**Statement (faithful paraphrase).** Under \Cref{ass:linear_mdp} (linear MDP with feature dimension $d$), fix $\delta \in (0, 1)$. Set $\beta = C \cdot d H \sqrt{\iota}$ for $\iota = \log(2 d T / \delta)$ and some absolute constant $C$. Then with probability at least $1 - \delta$, the regret of LSVI-UCB after $K$ episodes satisfies
$$\text{Regret}(K) \;=\; \sum_{k=1}^K \bigl[V_1^*(s_1^k) - V_1^{\pi^k}(s_1^k)\bigr] \;\le\; C' \sqrt{d^3 H^3 T \cdot \iota^2}.$$
Here $T = KH$ is the total number of steps.

**Hypotheses (Assumption A in paper).**
1. **Linear transition**: $P_h(\cdot \mid s, a) = \langle \phi(s, a), \mu_h(\cdot) \rangle$ for vector-measure $\mu_h$ with $\|\mu_h(\mathcal{S})\| \le \sqrt{d}$.
2. **Linear reward**: $r_h(s, a) = \langle \phi(s, a), \theta_h \rangle$ with $\|\theta_h\| \le \sqrt{d}$.
3. **Bounded features**: $\|\phi(s, a)\| \le 1$ for all $(s, a)$.

**Constants / dimension dependence.** Final bound is $\widetilde{O}(\sqrt{d^3 H^3 T})$, equivalently $\widetilde{O}(d^{3/2} H^{3/2} \sqrt{T})$. With $T = KH$, this is $\widetilde{O}(d^{3/2} H \sqrt{HK})$. The user's prompt asks for $\widetilde{O}(d^{3/2} \sqrt{HT})$ — these match if we read $\sqrt{HT}$ with $H$ inside the square root as $\sqrt{H \cdot KH} = H\sqrt{K}$, but more naturally with $T$ being total interactions we have $\widetilde{O}(d^{3/2} H \sqrt{T})$ overall.

**Key lemmas in the paper used in the proof.**
- Lemma B.1 (Bellman error bounding): $|\phi(s,a)^\top \widehat{w}_h^k - Q_h^*(s,a) - P_h V_{h+1}^*(s,a) + V_{h+1}^*(s,a)| \le \beta \|\phi\|_{\Lambda^{-1}}$ on the good event.
- Lemma B.3 (concentration of self-normalized noise): provides $\beta = O(dH\sqrt{\iota})$.
- Lemma B.4 (regret recursion / decomposition).
- Lemma D.2 (elliptical potential): $\sum_{k,h} \|\phi_h^k\|_{\Lambda_h^k{}^{-1}}^2 \le 2 d H \log(1 + K/(d\lambda))$.
- Lemma D.4 ($\varepsilon$-net over $\mathcal{V}$): covers the value-function class used in concentration.

**Project .bib key.** `\cite{jin2020provably}`

**Common usage in our proof.** We cite this paper for the algorithm definition (LSVI-UCB) and for the headline theorem statement. We prove the result from scratch using only the elliptical-potential lemma (Abbasi-Yadkori 2011) and self-normalized concentration.
