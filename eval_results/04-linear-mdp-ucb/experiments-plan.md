# Experiments plan: LSVI-UCB regret on synthetic linear MDPs

## Theoretical claim

\Cref{thm:main} establishes that, under \Cref{ass:linear_mdp}, LSVI-UCB (\Cref{def:lsvi_ucb}) attains regret
$$\mathrm{Regret}(K) \;\le\; C \, d^{3/2} \, H^{3/2} \, \sqrt{T} \cdot \iota \;=\; \widetilde{O}\bigl(d^{3/2} \sqrt{H^3 T}\bigr)$$
with probability at least $1 - \delta$, where $T = K H$, $\iota = \log(2 d K H / \delta)$, and $C$ is a universal constant. The two predictions to verify empirically are:
- **Time scaling.** For fixed $d$ and $H$, cumulative regret scales as $\widetilde{\Theta}(\sqrt T)$, i.e., $\log(\mathrm{Regret}) \approx \tfrac{1}{2} \log T + \mathrm{const}$.
- **Feature-dimension scaling.** For fixed $T, H$, regret scales as $\widetilde{\Theta}(d^{3/2})$, i.e., $\log(\mathrm{Regret}) \approx \tfrac{3}{2} \log d + \mathrm{const}$.

## Empirical hypothesis

1. **H1 ($\sqrt T$ rate).** Fix $d = 5$, $H = 10$. Run LSVI-UCB for $K \in \{10^2, 10^{2.5}, \ldots, 10^4\}$ episodes (so $T = K H$). Plot $\log(\mathrm{Regret}(K))$ versus $\log T$ on synthetic linear MDPs (described below). The empirical least-squares slope $\widehat{\alpha}_T$ should satisfy $|\widehat{\alpha}_T - 0.5| \le 0.05$ (within $10\%$ of the predicted $0.5$).
2. **H2 ($d^{3/2}$ rate).** Fix $H = 10$, $K = 10^4$ (so $T = 10^5$). Sweep $d \in \{2, 4, 8, 16, 32\}$. Plot $\log(\mathrm{Regret})$ versus $\log d$. The slope $\widehat{\alpha}_d$ should satisfy $|\widehat{\alpha}_d - 1.5| \le 0.15$ (within $10\%$ of the predicted $1.5$).

## Setup

### Data: synthetic linear MDPs

Following \cite{jin2020provably}'s Appendix E experimental setup (also Russo–Van Roy 2013, Yang–Wang 2020):

- **State space.** $\cS = [N]$ with $N = 100$ (finite).
- **Action space.** $\cA = [A]$ with $A = 10$.
- **Feature map.** $\phi(s, a) \in \R^d$ generated as follows:
  - Draw $d$ random Fourier features $\psi_j(s, a) = \cos(\omega_j^\top [s; a] + b_j)$ with $\omega_j \sim \cN(0, I_2)$, $b_j \sim \mathrm{Unif}[0, 2\pi]$.
  - Normalize: $\phi(s, a) = \psi(s, a) / \max_{(s, a)} \|\psi(s, a)\|_2$, ensuring $\|\phi\| \le 1$.
- **Transition kernel.** For each $h$, draw a target measure $\mu_h \in \R^{d \times N}$ with $\mu_h[\cdot, s'] \sim \cN(0, I_d/d)$, normalized so $\|\mu_h(\cS)\|_2 \le \sqrt d$. Set $P_h(s' \mid s, a) \propto \max\{0, \langle \phi(s, a), \mu_h(s')\rangle\}$ (project to non-negative, renormalize), then mix with $0.01$ uniform noise to ensure ergodicity.
- **Reward.** $\theta_h \sim \cN(0, I_d / d)$ rescaled so $\|\theta_h\|_2 = \sqrt d$, then $r_h(s, a) = \mathrm{clip}(\langle \phi(s, a), \theta_h\rangle, 0, 1)$.
- **Initial state.** $s_1^k$ uniform over $\cS$.

### Sample sizes / sweep ranges

- **H1 sweep (time):** $K \in \{100, 316, 1000, 3162, 10000\}$ ($T = K H \in \{10^3, \ldots, 10^5\}$), $d$ fixed at $5$, $H$ fixed at $10$.
- **H2 sweep (dimension):** $d \in \{2, 4, 8, 16, 32\}$, $K = 10000$, $H = 10$.

### Algorithm parameters

- **Regulariser.** $\lambda = 1$ (matching the theorem statement).
- **Bonus.** $\beta = c \cdot d \cdot H \cdot \sqrt{\iota}$ with $c \in \{0.01, 0.1, 1.0\}$ swept as **A1**; the theoretical $c = C_\beta$ is universal and not known numerically.
- **Episode count.** $K$ as in the sweep.

### Random seeds

10 seeds, listed: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`. For each $(d, K)$ configuration, run with all 10 seeds; report mean ± 1 std.

### Compute estimate

- Each `(d, K)` run with $K \le 10^4$, $d \le 32$ takes approximately 1-5 CPU-minutes (LSVI-UCB step time is $O(d^3 + d^2 K H)$ per backward pass per episode; for $d = 32, K = 10^4, H = 10$ this is $\sim 10^9$ operations per seed).
- Total: $5 \times 5 \times 10 = 250$ runs at $\le 5$ minutes each = $\le 21$ CPU-hours; manageable on a 32-core machine in $\le 1$ hour.

## Metrics

| Metric | What it measures | Verifies |
|---|---|---|
| Cumulative regret $\mathrm{Regret}(K)$ | $\sum_{k=1}^K [V_1^*(s_1^k) - V_1^{\pi^k}(s_1^k)]$, with $V_1^*$ computed by value iteration on the known model | \Cref{thm:main} |
| Per-episode regret $\mathrm{Regret}(K) / K$ | rate of decrease in average regret | empirical $T^{-1/2}$ scaling |
| Slope $\widehat \alpha_T = \mathrm{slope}(\log\mathrm{Regret}, \log T)$ | empirical exponent | H1 |
| Slope $\widehat \alpha_d = \mathrm{slope}(\log\mathrm{Regret}, \log d)$ | empirical $d$-exponent | H2 |
| $\beta$-sensitivity | regret as function of $c$ in $\beta = c\, d H \sqrt\iota$ | A1 (ablation) |

## Baselines

- **B1: $\varepsilon$-greedy with optimistic init.** $\varepsilon = 0.1$, optimistic initial $Q$-values $H$. Expected regret: $\Theta(T)$ (linear), so this is a sanity check that LSVI-UCB beats the trivial baseline.
- **B2: Random policy.** Uniform action selection. Expected regret: $\Theta(T)$.
- **B3: Thompson-sampling–style LSVI** (\cite{jin2020provably} Algorithm 2). Sample $w_h^k \sim \cN(\widehat w_h^k, \beta^2 (\Lambda_h^k)^{-1})$ instead of using a bonus. Expected regret: $\widetilde{O}(d^{3/2}\sqrt{H^3 T})$ (same theoretical rate, possibly tighter constants).

## Ablations

- **A1: Bonus coefficient $c$ in $\beta = c \cdot d H \sqrt\iota$.** Sweep $c \in \{0.01, 0.1, 1.0, 10.0\}$. Predicted effect: regret decreases then increases as $c$ traverses the optimal range; minimum should be at $c \asymp$ universal constant.
- **A2: Regulariser $\lambda \in \{0.1, 1.0, 10.0\}$.** Predicted: $\lambda$ enters the bound only through $\iota$ and the $\sqrt{d/\lambda}$ term in the proof of \Cref{lem:concentration}, so small variations should produce small (logarithmic) effects.
- **A3: Horizon $H \in \{5, 10, 20\}$ at fixed $T$.** Slope $\partial \log\mathrm{Regret} / \partial \log H$ predicted to be $3/2$ (via $H^{3/2}$ in the bound).

## Plots and tables to produce

- **Figure 1: $\log\mathrm{Regret}$ vs.\ $\log T$.** X-axis: $\log T$. Y-axis: $\log \mathrm{Regret}$. Lines: LSVI-UCB + B1 + B3. Error bars: $\pm 1$ std over 10 seeds. **Predicts:** LSVI-UCB slope $\approx 0.5$. **Verifies:** H1, \Cref{thm:main}.
- **Figure 2: $\log\mathrm{Regret}$ vs.\ $\log d$.** X-axis: $\log d$. Y-axis: $\log \mathrm{Regret}$ at $K = 10^4$, $H = 10$. Lines: LSVI-UCB + B3. Error bars: $\pm 1$ std over 10 seeds. **Predicts:** LSVI-UCB slope $\approx 1.5$. **Verifies:** H2, $d^{3/2}$ scaling in \Cref{thm:main} and \Cref{rem:T2_d_three_halves}.
- **Figure 3: Bonus-coefficient ablation.** X-axis: $c$ (log-scale). Y-axis: cumulative regret at $K = 10^4$. **Verifies:** A1, identifies the empirical range for $C_\beta$.
- **Figure 4: Horizon ablation.** X-axis: $\log H$. Y-axis: $\log\mathrm{Regret}$ at fixed $T$. **Predicts:** slope $\approx 3/2$. **Verifies:** A3, $H^{3/2}$ scaling.
- **Table 1: Slopes with confidence intervals.** Columns: $(\widehat\alpha_T, 95\% \text{ CI})$, $(\widehat\alpha_d, 95\% \text{ CI})$, $(\widehat\alpha_H, 95\% \text{ CI})$. Rows: LSVI-UCB, B3.

## Pre-registered success criteria

- **Confirms theory.** All of the following must hold:
  - $\widehat\alpha_T \in [0.45, 0.55]$ for LSVI-UCB (Fig.~1).
  - $\widehat\alpha_d \in [1.35, 1.65]$ for LSVI-UCB (Fig.~2).
  - $\widehat\alpha_H \in [1.35, 1.65]$ for LSVI-UCB (Fig.~4).
  - LSVI-UCB strictly outperforms B1 and B2 at the largest $T$ (Fig.~1).
- **Refutes theory.** Any of:
  - $\widehat\alpha_T > 0.6$ (sub-$\sqrt T$ regret growing faster than predicted).
  - $\widehat\alpha_d > 1.75$ (worse-than-$d^{3/2}$ dimension scaling).
  - LSVI-UCB worse than B1 at the largest $T$ (algorithm broken).
- **Ambiguous (re-investigate).** $\widehat\alpha_T \in (0.55, 0.6]$ or $\widehat\alpha_d \in (1.65, 1.75]$ — within noise but suggests either constants are tight or the theoretical bound is loose.

## Reproducibility statement

- **Code path / repo.** To be released alongside the paper at `https://github.com/<author>/lsvi-ucb-verification` (placeholder).
- **Seeds.** `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`.
- **Configs.** YAML files at `configs/h1.yaml`, `configs/h2.yaml`, `configs/a1.yaml`, etc.
- **Library versions.** `numpy 1.26+`, `scipy 1.11+`, `matplotlib 3.8+`. No deep-learning framework needed.
- **Hardware.** Any modern CPU; GPU not required. We used a 32-core Intel Xeon Gold for our timing estimate.

---

## Results

*This section is left intentionally blank. It will be filled in after running the experiments.*
