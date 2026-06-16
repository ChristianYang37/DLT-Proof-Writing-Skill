# \cite{jin2020provably} — LSVI-UCB on linear MDPs

**Paper.** "Provably Efficient Reinforcement Learning with Linear Function
Approximation", Chi Jin, Zhuoran Yang, Zhaoran Wang, Michael I. Jordan. COLT
2020. arXiv:1907.05388 (v2). Verified against the arXiv PDF.

**Exact names in PDF.**
- "Assumption A (Linear MDP)" — p. 4: $P_h(\cdot|x,a)=\langle\phi(x,a),\mu_h(\cdot)
  \rangle$, $r_h(x,a)=\langle\phi(x,a),\theta_h\rangle$, with $\|\phi\|\le1$,
  $\max\{\|\mu_h(\mathcal S)\|,\|\theta_h\|\}\le\sqrt d$.
- "Algorithm 1 (LSVI-UCB)" — p. 5: $\Lambda_h=\sum_{\tau=1}^{k-1}\phi_h^\tau
  (\phi_h^\tau)^\top+\lambda I$; $w_h=\Lambda_h^{-1}\sum_\tau\phi_h^\tau[r_h^\tau
  +\max_a Q_{h+1}(x_{h+1}^\tau,a)]$; $Q_h=\min\{w_h^\top\phi+\beta(\phi^\top
  \Lambda_h^{-1}\phi)^{1/2},H\}$.
- "Proposition 2.3" — p. 5: in a linear MDP, $Q_h^\pi(x,a)=\langle\phi(x,a),
  w_h^\pi\rangle$ for all policies $\pi$ (value functions are linear in $\phi$).
- "Theorem 3.1" — p. 6: set $\lambda=1$, $\beta=c\,dH\sqrt\iota$,
  $\iota=\log(2dT/p)$; then w.p. $1-p$, $\mathrm{Regret}(K)\le O(\sqrt{d^3H^3T
  \iota^2})=\tilde O(\sqrt{d^3H^3T})=\tilde O(d^{3/2}\sqrt{H^3T})$.
- "Lemma B.2" (weight bound $\|w_h^k\|\le 2H\sqrt{dk/\lambda}$),
  "Lemma B.3" (concentration / event $\mathcal E$, $\Pr\ge1-p/2$),
  "Lemma B.4" (recursion $\langle\phi,w_h^k\rangle-Q_h^\pi=P_h(V_{h+1}^k-
  V_{h+1}^\pi)+\Delta_h^k$, $|\Delta_h^k|\le\beta\|\phi\|_{(\Lambda_h^k)^{-1}}$),
  "Lemma B.5" (UCB / optimism $Q_h^k\ge Q_h^\star$, by backward induction),
  "Lemma B.6" (recursive formula $\delta_h^k\le\delta_{h+1}^k+\zeta_{h+1}^k+
  2\beta\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}$).

**Final-rate fact.** The headline rate is $\tilde O(\sqrt{d^3H^3T})$, i.e.
$d^{3/2}\sqrt{H^3T}$ up to log. NOTE: the eval prompt writes $d^{3/2}\sqrt{HT}$,
which drops two factors of $H$; the honest provable rate is $\sqrt{H^3T}$.
Recorded as a user-decision discrepancy.

**Project .bib key.** \cite{jin2020provably}
