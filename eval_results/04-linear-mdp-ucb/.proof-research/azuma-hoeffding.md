# Azuma-Hoeffding inequality (bounded martingale differences)

**Source.** Standard; textbook (e.g. Boucheron-Lugosi-Massart, *Concentration
Inequalities*, 2013, Thm 2.4; or Wainwright, *High-Dimensional Statistics*,
2019, Cor 2.20). Used as a *named textbook fact* — no project \cite needed.

**Statement.** Let $\{Z_t\}_{t\ge1}$ be a martingale-difference sequence w.r.t.
a filtration $\{\mathcal G_t\}$ ($\E[Z_t\mid\mathcal G_{t-1}]=0$) with $|Z_t|\le b$
a.s. Then for all $u>0$,
$$\Pr\Big[\sum_{t=1}^N Z_t \ge u\Big]\le \exp\!\Big(-\frac{u^2}{2Nb^2}\Big),$$
and by symmetry the two-sided version carries a factor 2. Equivalently, with
probability $\ge 1-\delta$, $\sum_{t=1}^N Z_t\le b\sqrt{2N\log(1/\delta)}$.

**Application here (term $T_1$).** The sequence $\zeta_h^k=\E[\delta_{h+1}^k\mid
x_h^k,a_h^k]-\delta_{h+1}^k$ is a martingale-difference indexed by $(k,h)$ in the
episode-step filtration, with $|\zeta_h^k|\le 2H$ (since $0\le\delta\le H$). With
$N=KH=T$ terms and $b=2H$, w.p. $\ge1-\delta/2$:
$$\sum_{k=1}^K\sum_{h=1}^H \zeta_h^k \le 2H\sqrt{2T\log(2/\delta)} = O(H\sqrt{T\iota}).$$

**Hypotheses.** bounded differences; adaptedness (conditional mean zero). The
key check: $V_h^k$ is computed *before* observing the fresh transition at episode
$k$, so $\zeta_h^k$ is genuinely a martingale difference.

**Common misuses.**
- Using $b=H$ instead of $2H$: $\delta_{h+1}^k\in[0,H]$ but the *difference*
  $\E[\cdot]-\delta$ ranges in $[-H,H]$, so $|\zeta|\le 2H$ is the correct bound.
  (JYWJ states $|\zeta_h^k|\le 2H$.)
- Counting $K$ terms instead of $KH=T$.
