# Dependency graph — LSVI-UCB regret on linear MDPs

Flat tree: 1 fact + 4 lemmas feeding 1 theorem. Shallowest tree that fits
(SKILL.md A.4). Organizational pattern (pattern-menu §RL/bandit regret):
successful-event conditioning + $T_1+T_2+T_3$ decomposition + per-term lemma +
elliptical potential. Derivation pattern: trailing-justification block;
successful-event conditioning for the theorem.

## fac:value-linear
**Statement (1-line):** Under the linear-MDP assumption, $Q_h^\pi(x,a)=\langle
\phi(x,a),w_h^\pi\rangle$ with $w_h^\pi=\theta_h+\int V_{h+1}^\pi d\mu_h$,
$\|w_h^\pi\|\le 2H\sqrt d$; more generally $\mathbb T_h V$ is linear in $\phi$ for
any $V$.
**Hypotheses:** ass:linear-mdp
**Downstream consumers:** lem:recursion (cite-site §03 — least-squares target is
linear), lem:concentration (§02 — bounded weight), thm:regret (§05).

## lem:concentration
**Statement (1-line):** There is an absolute $C$ s.t. the event $\mathcal E=
\{\forall k,h:\ \|\sum_{\tau<k}\phi_h^\tau[V_{h+1}^k(x_{h+1}^\tau)-(P_hV_{h+1}^k)
(x_h^\tau,a_h^\tau)]\|_{(\Lambda_h^k)^{-1}}\le C\,dH\sqrt{\iota}\}$ has
$\Pr[\mathcal E]\ge 1-\delta/2$ (with $\beta=C_\beta dH\sqrt\iota$).
**Hypotheses:** ass:linear-mdp, ass:bounded-reward, fac:value-linear
**Downstream consumers:** lem:recursion (§03 — controls $q_2$ error term),
thm:regret (§05 — defines $\mathcal E$ and its prob).

## lem:recursion
**Statement (1-line):** On $\mathcal E$, for any $\pi$ and all $(x,a,h,k)$:
$\langle\phi(x,a),w_h^k\rangle-Q_h^\pi(x,a)=P_h(V_{h+1}^k-V_{h+1}^\pi)(x,a)+
\Delta_h^k(x,a)$ with $|\Delta_h^k(x,a)|\le\beta\|\phi(x,a)\|_{(\Lambda_h^k)^{-1}}$.
**Hypotheses:** ass:linear-mdp, fac:value-linear, lem:concentration
**Downstream consumers:** lem:optimism (§03 — induction step), thm:regret
(§05 — yields the per-step recursive bound $\delta_h^k$).

## lem:optimism
**Statement (1-line):** On $\mathcal E$, $Q_h^k(x,a)\ge Q_h^\star(x,a)$ for all
$(x,a,h,k)$ (UCB optimism), by backward induction on $h$ from $H+1$ to $1$;
hence $V_1^k(x_1^k)\ge V_1^\star(x_1^k)$.
**Hypotheses:** lem:recursion
**Downstream consumers:** thm:regret (§05 — bounds $\mathrm{Regret}(K)\le
\sum_k\delta_1^k$).

## lem:elliptical
**Statement (1-line):** [\cite{abbasi2011improved}] For $\|\phi_j\|\le1$,
$\Lambda_t=\lambda I+\sum_{j\le t}\phi_j\phi_j^\top$, $\lambda\ge1$:
$\sum_{j=1}^t\phi_j^\top\Lambda_{j-1}^{-1}\phi_j\le 2\log\frac{\det\Lambda_t}
{\det\Lambda_0}\le 2d\log\frac{\lambda+t}{\lambda}$.
**Hypotheses:** (external; only $\|\phi\|\le1$, $\lambda\ge1$)
**Downstream consumers:** thm:regret (§05 — closes the bonus term $T_2$).

## thm:regret  (main)
**Statement (1-line):** Under ass:linear-mdp + ass:bounded-reward, with
$\lambda=1$, $\beta=C_\beta dH\sqrt\iota$, $\iota=\log(2dT/\delta)$: w.p.
$\ge1-\delta$, $\mathrm{Regret}(K)\le C\,d^{3/2}\sqrt{H^3 T}\,\iota=
\tilde O(d^{3/2}\sqrt{H^3T})$.
**Hypotheses:** all of the above.
**Proof shape:** condition on $\mathcal E$ (lem:concentration); optimism
(lem:optimism) $\Rightarrow \mathrm{Regret}\le\sum_k\delta_1^k$; unroll the
recursion (lem:recursion) into $T_1$ (martingale $\sum\zeta$, Azuma) $+T_2$
(bonus $\sum\beta\|\phi\|_{\Lambda^{-1}}$); Cauchy-Schwarz + lem:elliptical close
$T_2$; union bound on $\mathcal E$ and the Azuma event gives $1-\delta$.

## Occam check
Every node has a non-empty Downstream consumers field. No orphan lemmas. The
three-term naming in the prompt ($T_1$ concentration, $T_2$ variance, $T_3$
martingale) maps onto: $T_3$=martingale $\sum\zeta$ (Azuma), $T_2$=bonus sum
(elliptical), and the $T_1$ "concentration error" is absorbed into the bonus via
lem:concentration/lem:recursion (the bonus dominates the concentration error on
$\mathcal E$). We keep the prompt's three labels in §05 for the assertion.
