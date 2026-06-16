# Experiments plan: LSVI-UCB regret on linear MDPs (\Cref{thm:regret})

> Design-only. No results are reported here; the **Results** section is left
> blank for the user to fill after running. No fabricated numbers, slopes, or
> conclusions appear anywhere in this file.

## Theoretical claim

\Cref{thm:regret} predicts that LSVI-UCB on a linear MDP with feature dimension
$d$, horizon $H$, and $K$ episodes (so $T=KH$ steps) incurs cumulative regret
$\Reg(K)=\Otil(d^{3/2}\sqrt{H^3 T})$ with probability at least $1-\delta$, under
\Cref{ass:linear-mdp} with $\lambda=1$ and bonus radius
$\beta=C_\beta dH\sqrt{\iota}$, $\iota=\log(2dT/\delta)$. The two falsifiable
quantitative predictions are:

1. **Time scaling.** For fixed $(d,H)$, $\Reg(K)$ grows as $\sqrt{T}$ up to log
   factors, i.e. $\Reg(K)/\sqrt{T\,\iota}$ is bounded by a constant in $T$.
2. **Dimension scaling.** For fixed $(H,T)$, $\Reg(K)$ grows as $d^{3/2}$ up to
   log factors.

## Empirical hypothesis

- **H1 (sqrt-T).** On a log--log plot of $\Reg(K)$ vs.\ $T$ at fixed $(d,H)$,
  the asymptotic slope is $\tfrac12$ (regret $\propto T^{1/2}$). The fitted
  slope should lie in $[0.45, 0.60]$ once $T$ is large enough that the log term
  $\iota$ varies slowly.
- **H2 (d^{3/2}).** On a log--log plot of $\Reg(K)$ vs.\ $d$ at fixed $(H,T)$,
  the asymptotic slope is $\tfrac32$ (regret $\propto d^{3/2}$). The fitted
  slope should lie in $[1.3, 1.7]$.
- **H3 (optimism / coverage).** Empirical failure probability that
  $V_1^k(x_1^k)\ge V_1^\star(x_1^k)$ is violated stays $\le\delta$ across all
  episodes, verifying \Cref{lem:optimism}.

## Setup

### Data — synthetic linear MDPs
- Generation: sample a random linear MDP with $S$ states, $A$ actions, feature
  dimension $d$. Draw feature vectors $\featmap(s,a)\in\R^d$ (random rows of a
  $d$-dim simplex so \Cref{ass:linear-mdp} normalization holds:
  $\norm{\featmap}\le1$), random signed measures $\mu_h$ over states normalized
  to $\norm{\mu_h(\mathcal S)}\le\sqrt d$, and reward parameters $\theta_h$ with
  $\norm{\theta_h}\le\sqrt d$. This realizes the *exact* linear-MDP model the
  theorem assumes (no misspecification), isolating the rate.
- Episode counts to sweep (H1): $K\in\{2{\cdot}10^3, 5{\cdot}10^3, 10^4,
  2{\cdot}10^4, 5{\cdot}10^4, 10^5\}$ (six points, $\ge1.5$ decades in $T$).
- Feature dimensions to sweep (H2): $d\in\{5, 10, 20, 40, 80\}$ (five points,
  $>1$ decade), at fixed $K$ chosen so the agent reaches the asymptotic regime.
- Horizons (secondary sweep / sanity): $H\in\{5, 10, 20\}$.
- States/actions: $S\in\{10, 50\}$, $A\in\{5, 10\}$ — chosen so that the
  tabular baseline is feasible and so that regret is *independent of $S,A$* as
  the theory predicts (this independence is itself a check).

### Model / algorithm
- LSVI-UCB exactly as in \Cref{sec:prelim}: Gram matrix
  Eq.~\eqref{eq:gram-def}, ridge weights Eq.~\eqref{eq:weight-def}, optimistic
  $Q$ Eq.~\eqref{eq:Q-def}.
- Regularizer $\lambda=1$ (as in the theorem).
- Bonus radius $\beta=c_\beta\, dH\sqrt{\iota}$ with $\iota=\log(2dT/\delta)$,
  $\delta=0.05$. Treat $c_\beta$ as a tuned scalar (see hyperparameter
  protocol); the *exponents* $d,H,\sqrt\iota$ are fixed by theory and NOT tuned.

### Training / interaction
- Run for $K$ episodes; record cumulative regret using the known $V_1^\star$
  (computable in closed form on the synthetic MDP via exact value iteration).
- No gradient training; the "optimizer" is the per-episode ridge solve.

### Random seeds
Seeds `[1, 2, 3, 4, 5, 6, 7, 8]` (eight seeds). Report mean $\pm$ 1 std and a
95% bootstrap CI over seeds. Never a single-run number.

### Compute estimate
Each run is CPU-bound (small $d$, exact ridge solves). Rough estimate: a single
$(d,H,K)$ configuration at $K=10^5$, $d=80$ is dominated by $O(KHd^2)$ linear
algebra; budget on the order of a few CPU-hours per configuration $\times$ 8
seeds. Hardware class: a standard multi-core workstation CPU. (No GPU needed.)

## Metrics

| Metric | What it measures | Verifies |
|---|---|---|
| Cumulative regret $\Reg(K)$ vs.\ $T$ | growth rate in steps | \Cref{thm:regret} (H1) |
| Cumulative regret $\Reg(K)$ vs.\ $d$ | feature-dimension dependence | \Cref{thm:regret} (H2) |
| Fitted log--log slope (time) | asymptotic exponent in $T$ | \Cref{thm:regret} (H1) |
| Fitted log--log slope (dim) | asymptotic exponent in $d$ | \Cref{thm:regret} (H2) |
| Optimism-violation rate $\Prob[V_1^k<V_1^\star]$ | coverage of the bonus | \Cref{lem:optimism} |
| Mean bonus sum $\sum_{k,h}\Mnorm{\featmap_h^k}{(\Gram_h^k)^{-1}}$ vs.\ $\sqrt{dKH}\cdot\sqrt{\iota}$ | tightness of the elliptical-potential step | \Cref{lem:elliptical} |

Every metric maps to one claim; metrics without a theoretical target are dropped.

## Baselines

- **B1 — $\varepsilon$-greedy LSVI (no bonus).** LSVI with $\beta=0$ and
  $\varepsilon$-greedy exploration. Expected to suffer linear regret on hard
  instances; isolates the contribution of the UCB bonus.
- **B2 — Tabular UCB (UCBVI).** A tabular optimistic algorithm ignoring the
  linear structure. Its regret scales with $\sqrt{SA}$; comparison shows the
  $d$-vs-$\sqrt{SA}$ advantage when $d\ll SA$.
- **B3 — Oracle / lower-reference.** The information-theoretic
  $\Omega(d\sqrt{HT})$ reference (Zhou et al.\ lower bound), plotted as a slope
  guide, NOT as an achieved curve.

## Ablations

- **A1 — bonus scale $c_\beta$.** Vary $c_\beta\in\{0.1,0.3,1,3\}$ at fixed
  exponents. Predicted effect: too-small $c_\beta$ breaks optimism (H3 fails and
  regret can turn linear); large $c_\beta$ inflates regret by a constant but
  preserves the $\sqrt T$ slope.
- **A2 — regularizer $\lambda$.** Vary $\lambda\in\{0.1, 1, 10\}$. Predicted
  effect: changes the constant via $\log((\lambda+K)/\lambda)$ but not the
  exponents.
- **A3 — horizon $H$.** Vary $H\in\{5,10,20\}$ at fixed $T=KH$. Predicted
  effect: regret scales as $H^{3/2}$ in the $H$-direction (from $\sqrt{H^3}$).
- **A4 — misspecification $\zeta$.** Inject a $\zeta$-approximate linear MDP and
  vary $\zeta\in\{0,0.01,0.05\}$. Predicted effect: an additive $\Otil(\zeta
  dHT)$ linear-in-$T$ term appears, matching the misspecified bound; with
  $\zeta=0$ the $\sqrt T$ rate is recovered.

## Plots and tables to produce

- **Figure 1.** $\Reg(K)$ vs.\ $T$ (log--log), one line per $d\in\{10,40\}$,
  fixed $H=10$. X-axis: $T$. Y-axis: cumulative regret. Error bars: $\pm1$ std
  over 8 seeds. **Predicts**: slope $\approx \tfrac12$. **Verifies**:
  \Cref{thm:regret} (H1).
- **Figure 2.** $\Reg(K)$ vs.\ $d$ (log--log), fixed $(H,T)$. Error bars:
  $\pm1$ std over 8 seeds. Overlay a reference line of slope $\tfrac32$.
  **Predicts**: slope $\approx \tfrac32$. **Verifies**: \Cref{thm:regret} (H2).
- **Figure 3.** Regret curves of LSVI-UCB vs.\ B1 ($\varepsilon$-greedy) vs.\
  B2 (tabular UCBVI) on a fixed instance. **Verifies**: the necessity of the UCB
  bonus and the $d$-vs-$\sqrt{SA}$ advantage.
- **Figure 4 (ablation A1).** $\Reg(K)$ and optimism-violation rate vs.\
  $c_\beta$. **Verifies**: \Cref{lem:optimism} coverage / \Cref{lem:concentration}.
- **Table 1.** Fitted log--log slopes (time and dimension) with 95% CIs across
  seeds, per $(H)$ setting. Columns: setting, time-slope $\pm$ CI, dim-slope
  $\pm$ CI.

## Pre-registered success criteria

- **Confirms theory** if: the fitted time-slope $\in[0.45,0.60]$ (H1) AND the
  fitted dimension-slope $\in[1.3,1.7]$ (H2) AND the optimism-violation rate
  stays $\le\delta=0.05$ across episodes (H3), each holding for $\ge 7$ of 8
  seeds.
- **Refutes theory** if: the time-slope is $\ge0.7$ (regret growing
  super-$\sqrt T$ in the well-specified case), OR the optimism-violation rate
  exceeds $2\delta$ persistently at the theory-prescribed $\beta$, OR the
  dimension-slope is $\ge2.2$ or $\le0.8$.
- Thresholds are fixed BEFORE running; they are not to be adjusted after seeing
  the curves.

## Reproducibility statement

- Code path / repo: `to be released` (single-file Python; numpy + a small MDP
  simulator; no deep-learning framework needed).
- Seeds: `[1, 2, 3, 4, 5, 6, 7, 8]`.
- Configs: one YAML per sweep — `configs/time_sweep.yaml`,
  `configs/dim_sweep.yaml`, `configs/ablation_beta.yaml`,
  `configs/ablation_misspec.yaml`.
- Library versions: `numpy 1.26.x`, `scipy 1.13.x`, `python 3.11`.
- Hardware: standard multi-core CPU workstation; no GPU required.

---

## Results

**Leave this section blank.** The user fills it in after running experiments.
Do NOT populate with imagined numbers, predicted-as-actual values, or
placeholder rows.
