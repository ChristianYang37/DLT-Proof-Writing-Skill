# Linear-MDP value-function linearity (Bellman backup is linear in features)

**Source.** Jin-Yang-Wang-Jordan 2020 (arXiv:1907.05388), Proposition 2.3 +
Assumption A. Project .bib key: \cite{jin2020provably}.

**Statement.** Under the linear-MDP assumption ($P_h(\cdot|x,a)=\langle\phi(x,a),
\mu_h\rangle$, $r_h(x,a)=\langle\phi(x,a),\theta_h\rangle$), for ANY policy $\pi$
and any function $V:\mathcal S\to[0,H]$, the one-step Bellman backup is linear in
$\phi$:
$$(\mathbb T_h V)(x,a) := r_h(x,a)+(P_h V)(x,a)
= \big\langle \phi(x,a),\; \theta_h + \textstyle\int V(x')\,d\mu_h(x') \big\rangle.$$
Consequently $Q_h^\pi(x,a)=\langle\phi(x,a),w_h^\pi\rangle$ with
$w_h^\pi=\theta_h+\int V_{h+1}^\pi\,d\mu_h$, and $\|w_h^\pi\|\le 2H\sqrt d$.

**Derivation.** $(P_hV)(x,a)=\int V(x')P_h(dx'|x,a)=\int V(x')\langle\phi(x,a),
d\mu_h(x')\rangle=\langle\phi(x,a),\int V\,d\mu_h\rangle$ — pull the constant-in-$x'$
vector $\phi(x,a)$ out of the integral. Add $r_h=\langle\phi,\theta_h\rangle$.

**Norm bound.** $\|w_h^\pi\|\le\|\theta_h\|+\|\int V_{h+1}^\pi d\mu_h\|
\le\sqrt d + H\|\mu_h(\mathcal S)\|\le\sqrt d+H\sqrt d\le 2H\sqrt d$ (using
$\|\theta_h\|\le\sqrt d$, $0\le V\le H$, $\|\mu_h(\mathcal S)\|\le\sqrt d$).

**Why it matters.** This is what makes regularized least-squares value iteration
well-posed: the target $\mathbb T_h V_{h+1}$ lives in the $d$-dim span of $\phi$,
so the ridge estimate $w_h^k=\Lambda_h^{-1}\sum_\tau\phi_h^\tau[\dots]$ recovers it
up to a self-normalized error.

**Common misuses.**
- Forgetting that linearity holds for *every* $V$ (not just $V^\pi$) — needed
  because the algorithm backs up the *estimated* $V_{h+1}^k$, not a true value.
- Loose norm bound: using $\|w\|\le H\sqrt d$ instead of $2H\sqrt d$ (the reward
  contributes the extra $\sqrt d$).
