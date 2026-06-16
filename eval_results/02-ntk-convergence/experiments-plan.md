# Experiments plan: NTK linear convergence of two-layer ReLU GD (`\Cref{thm:main}`)

> Design only. **No results are reported here** — the Results section is intentionally blank and
> is filled by the user after running. No numerical values, fitted slopes, or conclusions are
> fabricated.

## Theoretical claim

`\Cref{thm:main}` predicts that, for the two-layer ReLU network
$f_W(x) = \tfrac1{\sqrt m}\sum_r a_r\sigma(w_r^\top x)$ trained by gradient descent on the
squared loss with step size $\eta = \kappa\lambda_0/n^2$ and width
$m \ge C\,n^6/(\lambda_0^4\delta^3)$, the training residual contracts geometrically:
$\|y - u(k)\|_2^2 \le (1 - \tfrac{\eta\lambda_0}{2})^k\|y-u(0)\|_2^2$ with probability $\ge 1-\delta$,
where $\lambda_0 = \lambda_{\min}(H^\infty)$ is the smallest eigenvalue of the population NTK Gram
matrix. The theory predicts two falsifiable behaviors: (i) the **log training loss is linear in
iteration** with slope $\log(1-\tfrac{\eta\lambda_0}{2})$; (ii) **wider networks track the kernel
better** — the deviation of the empirical convergence rate from the kernel-predicted rate, and the
distance $\|W(k)-W(0)\|_F$, both shrink as $m$ grows.

## Empirical hypothesis

- **H1 (linear convergence / rate).** $\log\|y-u(k)\|_2^2$ vs.\ $k$ is a straight line whose slope
  matches $\log(1-\tfrac{\eta\lambda_0}{2})$ computed from the measured $\lambda_0$ and chosen
  $\eta$, within a small relative tolerance. Verifies `\Cref{thm:main}` and `\Cref{lem:contraction}`.
- **H2 (width vs. convergence speed).** As width $m$ increases (holding $n,\eta$ fixed), the
  measured per-step contraction factor converges to the kernel value $1-\tfrac{\eta\lambda_0}{2}$,
  and the failure rate of reaching $\|y-u(k)\|^2\le\varepsilon$ within the predicted horizon drops.
  Verifies the width condition of `\Cref{thm:main}` and the stay-in-ball lemma `\Cref{lem:main}`.
- **H3 (stay-in-ball).** $\max_r\|w_r(k)-w_r(0)\|_2 = O(n/(\sqrt m\,\lambda_0))$ stays below the
  radius $R=\Theta(\delta\lambda_0/n^2)$ for all $k$, and shrinks as $1/\sqrt m$. Verifies
  `\Cref{lem:main}` Eq.~(main-stay) and `\Cref{lem:gram-stability}`.

## Setup

### Data
- Synthetic: $n$ inputs drawn i.i.d.\ uniform on the unit sphere $\mathbb S^{d-1}$, then
  $\ell_2$-normalized to $\|x_i\|=1$ (matching the proof's normalization). Labels $y_i\in\{-1,+1\}$
  random balanced, or $y_i=\mathrm{sign}(\langle x_i,\theta^\star\rangle)$ for a fixed random
  $\theta^\star$ (two label regimes, reported separately).
- Reject any draw with two near-parallel inputs ($|x_i^\top x_j|>1-10^{-3}$) so that
  $\lambda_0=\lambda_{\min}(H^\infty)>0$ is bounded away from 0 (the assumption of `\Cref{ass:lambda0}`).
- Sample sizes to sweep: $n \in \{50, 100, 200, 400\}$.
- Input dimension: $d \in \{20, 50, 100\}$.

### Model
- Two-layer ReLU network Eq.~(network), first layer $W\in\R^{d\times m}$ trained, $a_r\in\{\pm1\}$
  fixed at init.
- Width sweep: $m \in \{500, 1000, 2000, 4000, 8000, 16000\}$ (geometric, to expose the $1/\sqrt m$
  and width-threshold trends of H2/H3).
- Initialization: $w_r(0)\sim\mathcal N(0,I_d)$ i.i.d., $a_r\sim\mathrm{Unif}\{\pm1\}$ i.i.d.,
  exactly as in `\Cref{def:gram}` / the preliminaries.

### Training
- Optimizer: full-batch gradient descent (GD), matching the proof (not SGD/Adam).
- Step size: $\eta = \kappa\,\lambda_0/n^2$ with $\kappa\in\{0.1, 0.25, 0.5\}$ (an ablation grid;
  $\lambda_0$ estimated as $\lambda_{\min}$ of the Monte-Carlo NTK Gram matrix — see Metrics).
- Iterations: run until $\|y-u(k)\|_2^2\le 10^{-8}$ or $k=k_{\max}$, with
  $k_{\max}=\lceil 20\cdot\tfrac{2}{\eta\lambda_0}\log(n/10^{-8})\rceil$ (20$\times$ the predicted
  horizon, so non-convergence is observable).
- Loss: $L(W)=\tfrac12\|y-u(W)\|_2^2$, matching Eq.~(loss).

### Random seeds
Five seeds minimum, listed explicitly: `[1, 2, 3, 4, 5]` (extend to `[1, ..., 10]` for the
headline width-sweep figure). All randomness — data draw, $W(0)$, $a_r$ — is seeded jointly.

### Compute estimate
CPU-only is sufficient for $n\le400$, $m\le16000$ (dense $n\times n$ Gram per step). Rough
estimate: the full grid (4 $n$ × 3 $d$ × 6 $m$ × 3 $\kappa$ × 5 seeds, headline width-sweep at
10 seeds) is on the order of low-hundreds of CPU-core-hours; single-GPU (one consumer GPU)
shrinks wall-clock to a few hours. Report measured core-hours in the Reproducibility statement.

## Metrics

| Metric | What it measures | Verifies |
|---|---|---|
| $\widehat\lambda_0$ | $\lambda_{\min}$ of the Monte-Carlo estimate of $H^\infty$ ($m'=10^5$ fresh neurons) | `\Cref{ass:lambda0}`, sets the predicted rate |
| log-residual curve $\log\|y-u(k)\|_2^2$ vs.\ $k$ | linearity + slope of convergence | `\Cref{thm:main}`, `\Cref{lem:contraction}` (H1) |
| measured contraction factor $\rho=\big(\tfrac{\|y-u(k_2)\|^2}{\|y-u(k_1)\|^2}\big)^{1/(k_2-k_1)}$ | per-step geometric rate | `\Cref{thm:main}` rate $1-\tfrac{\eta\lambda_0}{2}$ (H1, H2) |
| $\max_r\|w_r(k)-w_r(0)\|_2$ over $k$ | weight movement vs.\ radius $R$ | `\Cref{lem:main}` Eq.~(main-stay), `\Cref{lem:gram-stability}` (H3) |
| $\lambda_{\min}(H(k))$ over $k$ | Gram floor maintenance | `\Cref{lem:main}` Eq.~(main-gram), `\Cref{lem:gram-stability}` |
| $\|H(0)-H^\infty\|_2$ | init Gram concentration | `\Cref{lem:init-gram-close}` |

Every metric points at one theoretical claim; none are generic benchmarks.

## Baselines

- **B1 — Kernel (NTK) regression closed form.** Solve the linear ODE/recursion
  $u(k+1)-u(k) = -\eta H^\infty(u(k)-y)$ (fixed kernel $H^\infty$). This is the infinite-width
  limit the finite-width GD should track; comparison enables H2 (deviation $\to 0$ as $m\to\infty$).
- **B2 — Random-feature / frozen-features baseline.** Train only the readout on the fixed
  initial features $\sigma(w_r(0)^\top x)$ (no first-layer movement). Isolates how much of the
  convergence is kernel-regime vs.\ feature learning; the theory predicts the trained-first-layer
  GD and B2 should be close in the wide regime.

## Ablations

- **A1 — width $m$** over $\{500,\dots,16000\}$: predicted effect — measured contraction factor
  $\rho\to1-\tfrac{\eta\lambda_0}{2}$ and $\max_r\|w_r(k)-w_r(0)\|$ decreases as $\Theta(1/\sqrt m)$
  (H2, H3).
- **A2 — step size $\kappa$** over $\{0.1,0.25,0.5\}$: predicted effect — slope of log-residual
  scales linearly in $\eta$ (rate $\propto\kappa\lambda_0^2/n^2$); divergence expected if
  $\kappa$ is pushed past the $\eta\le\lambda_0/(2n^2)$ cap.
- **A3 — sample size $n$** over $\{50,\dots,400\}$: predicted effect — required width for
  reliable convergence grows polynomially in $n$ (consistent with $m\gtrsim n^6/\lambda_0^4\delta^3$);
  rate slows as $\propto1/n^2$.
- **A4 — dimension $d$** over $\{20,50,100\}$: predicted effect — convergence rate is governed by
  $\lambda_0$, largely insensitive to $d$ at fixed $n$ once inputs are normalized.

## Plots and tables to produce

- **Figure 1 (H1).** $\log\|y-u(k)\|_2^2$ (Y) vs.\ iteration $k$ (X), one line per width $m$;
  overlay the kernel-predicted line of slope $\log(1-\tfrac{\eta\lambda_0}{2})$. Error bars: ±1 std
  over 10 seeds. **Predicts:** curves are linear with slope matching the kernel slope as $m$ grows.
  **Verifies:** `\Cref{thm:main}`.
- **Figure 2 (H2).** Measured contraction factor $\rho$ (Y) vs.\ width $m$ (X, log scale); dashed
  horizontal line at the kernel value $1-\tfrac{\eta\lambda_0}{2}$. Error bars: ±1 std over 10 seeds.
  **Predicts:** $\rho\to$ kernel value as $m\to\infty$. **Verifies:** width condition of `\Cref{thm:main}`.
- **Figure 3 (H3).** $\max_r\|w_r(k)-w_r(0)\|_2$ (Y) vs.\ width $m$ (X, log–log); overlay the
  predicted $\Theta(1/\sqrt m)$ reference slope and the radius $R$. **Predicts:** movement below $R$,
  decaying as $1/\sqrt m$. **Verifies:** `\Cref{lem:main}`, `\Cref{lem:gram-stability}`.
- **Figure 4 (Gram floor).** $\lambda_{\min}(H(k))/\lambda_0$ (Y) vs.\ $k$ (X), per width; reference
  line at $1/2$. **Verifies:** `\Cref{lem:main}` Eq.~(main-gram).
- **Table 1.** For each $(n,d,m)$: $\widehat\lambda_0$, predicted vs.\ measured contraction factor,
  fraction of seeds converging within the predicted horizon, mean ± std $\max_r\|w_r-w_r(0)\|$.

## Pre-registered success criteria

- **Confirms theory** if: (i) Fig.~1 log-residual curves are linear (per-seed $R^2\ge0.98$ over the
  pre-$\varepsilon$ regime) with measured slope within $\pm15\%$ of $\log(1-\tfrac{\eta\lambda_0}{2})$
  at the two largest widths; (ii) in Fig.~2, $\rho$ at $m=16000$ is within $\pm10\%$ of the kernel
  value and monotonically approaches it as $m$ grows; (iii) in Fig.~3, $\max_r\|w_r(k)-w_r(0)\|$
  stays below $R$ for all $k$ at the two largest widths and its width-trend slope is within $\pm0.2$
  of the predicted $-1/2$ on the log–log plot.
- **Refutes theory** if: the log-residual is visibly sub-linear (concave) at the largest width, OR
  the measured contraction factor does not approach the kernel value as $m\to\infty$, OR weight
  movement grows with $k$ (escapes the ball) at the largest width.

These thresholds are fixed **before** running; they are not to be relaxed post-hoc.

## Reproducibility statement
- Code path / repo: to be released (`ntk_convergence_experiments/`).
- Seeds: `[1, 2, 3, 4, 5]` (headline width-sweep extended to `[1, ..., 10]`).
- Configs: one YAML per figure (`fig1_rate.yaml`, `fig2_width.yaml`, `fig3_movement.yaml`,
  `fig4_gram.yaml`, `table1_grid.yaml`), each pinning $n, d, m, \kappa, k_{\max}$, seed list.
- Library versions: `numpy 1.26.x`, `scipy 1.13.x` (for $\lambda_{\min}$), optionally
  `torch 2.3.x` for the GPU path; record exact versions at run time.
- Hardware: CPU model + core count (and GPU model if used); record measured core-hours.

---

## Results

**Leave this section blank.** To be filled by the user after running the experiments. Do NOT
populate with imagined numbers, predicted-as-actual values, or placeholder rows.
