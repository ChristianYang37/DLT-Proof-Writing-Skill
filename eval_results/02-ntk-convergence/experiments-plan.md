# Experiments plan: linear convergence of GD on two-layer ReLU networks via NTK

## Theoretical claim

`\Cref{thm:main}` predicts that for a two-layer ReLU network of width $m$ initialized with $\wb_r(0) \sim \mathcal N(\mathbf 0, \I_d)$ and $a_r \sim \text{Unif}\{\pm 1\}$, gradient descent on the squared loss with step size $\eta = C_2 \lambda_0 / n^2$ satisfies, with probability $\ge 1 - \delta$ over initialization,
- (i) linear convergence: $\norm{\ub(t) - \yb}_2^2 \le (1 - \eta \lambda_0 / 2)^t \norm{\ub(0) - \yb}_2^2$ for all $t \ge 0$;
- (ii) stay-near-init: $\norm{\wb_r(t) - \wb_r(0)}_2 \le R = 4\sqrt n \norm{\ub(0)-\yb}_2 / (\sqrt m \lambda_0)$ for all $r, t$;
provided $m \ge C_1 n^6 / (\lambda_0^4 \delta^3)$.

The headline empirical predictions are:
1. **Slope of $\log L(\Wb(t))$ vs.\ $t$** equals $\log(1 - \eta\lambda_0/2)$, i.e., $\approx -\eta\lambda_0/2$ for small $\eta\lambda_0$.
2. **Maximum per-neuron displacement $\max_r \norm{\wb_r(t) - \wb_r(0)}_2$** decays in width as $\Theta(1/\sqrt m)$ at fixed $t$.
3. **Failure rate (non-convergence to small loss within budget)** drops sharply as $m$ crosses the predicted threshold $\sim n^6 / \lambda_0^4$.

## Empirical hypothesis

- **H1 (linear-rate).** For sufficiently wide $m$, $\log \norm{\ub(t) - \yb}_2^2$ is approximately linear in $t$ with slope $\hat\rho$ satisfying $|\hat\rho - \log(1 - \eta\lambda_0/2)| \le 0.10 \cdot |\log(1 - \eta\lambda_0/2)|$ (i.e., within 10\% of the predicted slope).
- **H2 (width scaling).** $\max_r \norm{\wb_r(T) - \wb_r(0)}_2 \asymp m^{-1/2}$ at fixed $T$, $n$, $\lambda_0$. Fit a power law $C \cdot m^{-\alpha}$ on log-log axes; predicted $\alpha = 0.5$, allowed range $[0.40, 0.60]$.
- **H3 (phase transition in width).** Probability of reaching training loss $\le 10^{-4}$ within $T = 10^5$ steps transitions from $\le 0.2$ to $\ge 0.8$ as $m$ sweeps below to above a threshold $m^* \asymp n^{p}/\lambda_0^q$ for some empirical $p, q$. The theory predicts $p \in [4, 6]$, $q \in [2, 4]$; empirical fit should fall in or near this range.

## Setup

### Data

Synthetic data designed to give a well-conditioned NTK:
- **Input generation.** $\xb_i \stackrel{\mathrm{iid}}{\sim} \mathcal N(\mathbf 0, \I_d)$, then normalized to $\norm{\xb_i}_2 = 1$. Choosing $\xb_i$ iid Gaussian and projecting to the sphere ensures (with high probability) no two inputs are collinear, so by \Cref{rem:lambda0} $\lambda_0 > 0$.
- **Labels.** $y_i \stackrel{\mathrm{iid}}{\sim} \text{Unif}\{-1, +1\}$ (the result is label-agnostic; this stresses the network).
- **Sample sizes.** $n \in \{50, 100, 200, 400\}$ (sweep for H3 width-scaling).
- **Input dimension.** $d = 100$ fixed (per \Cref{rem:data}, $d$ enters only through the rate at which $\Hb^\infty$ concentrates and not in $\lambda_0$ directly).
- **Empirical $\lambda_0$ measurement.** Compute $\Hb^\infty$ via the closed form $\Hb^\infty_{ij} = (\xb_i^\top \xb_j) \cdot (\pi - \arccos(\xb_i^\top \xb_j)) / (2\pi)$ (Cho-Saul kernel for ReLU) and report $\lambda_{\min}(\Hb^\infty)$ per dataset draw.

### Model

- **Architecture.** Two-layer ReLU network with one hidden layer, output dimension 1, per Eq.~\eqref{eq:network}.
- **Width sweep.** $m \in \{100, 200, 500, 1000, 2000, 5000, 10000, 20000\}$ (8 widths, log-spaced).
- **Initialization.** $\wb_r(0) \sim \mathcal N(\mathbf 0, \I_d)$, $a_r \sim \text{Unif}\{\pm 1\}$, both iid, per \Cref{ass:init}. Second-layer weights $\ab$ frozen throughout training.

### Training

- **Optimizer.** Vanilla gradient descent (no momentum, no weight decay), per \Cref{thm:main}.
- **Step size.** $\eta = c \cdot \lambda_0 / n^2$ with $c = 0.5$ (well within the $C_2$ band suggested by the theory).
- **Iterations.** $T = 10^5$ (deep enough to enter the asymptotic linear regime and saturate the loss for over-parameterized $m$).
- **Loss.** Squared loss $L(\Wb) = \tfrac12 \sum_i (\ub_i(\Wb) - y_i)^2$, per Eq.~\eqref{eq:loss}.

### Random seeds

Seeds `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` (10 seeds). Each seed controls (data draw, $\Wb(0)$, $\ab$).

### Compute estimate

- **Per run:** width $m = 10000$, $T = 10^5$, GD step is $O(m n d)$ flops $\approx 10^{10}$, total $\approx 10^{15}$ flops. On a single GPU (e.g., A100, $\approx 3 \cdot 10^{14}$ flops/s in fp32), one run is $\le 60$ minutes.
- **Total budget:** $10 \text{ seeds} \times 8 \text{ widths} \times 4 \text{ } n \approx 320$ runs $\times$ 60 min $\approx 320$ GPU-hours.

## Metrics

| Metric | What it measures | Verifies |
|---|---|---|
| Training loss $L(\Wb(t))$ vs.\ $t$ | Convergence trajectory | `\Cref{thm:main}` (Eq.~\eqref{eq:thm_linconv}) |
| Slope of $\log L(\Wb(t))$ vs.\ $t$ in linear-decay regime | Empirical linear rate $\hat\rho$ | `\Cref{thm:main}` quantitative rate |
| $\max_r \norm{\wb_r(t) - \wb_r(0)}_2$ vs.\ $t$ and $m$ | Stay-near-init bound | `\Cref{thm:main}` (Eq.~\eqref{eq:thm_stayinit}) |
| $\lambda_{\min}(\Hb(\Wb(t)))$ vs.\ $t$ | Gram-matrix spectrum tracking | `\Cref{lem:perturbation}` + Step 3 of `\Cref{sec:proof_main}` |
| $\opnorm{\Hb(\Wb(0)) - \Hb^\infty}$ at init | Initial Gram concentration | `\Cref{lem:init_gram}` |
| Fraction of seeds reaching $L \le 10^{-4}$ within $T$ steps | Width-vs-success rate | Width hypothesis $m \gtrsim n^6/\lambda_0^4$ (rough) |

## Baselines

- **B1 (Kernel regression on $\Hb^\infty$).** Closed-form kernel regression with the population NTK as kernel. The loss after $t$ steps of GD on the kernel regression problem is exactly $\norm{(\I - \eta\Hb^\infty)^t \ub(0)_\infty - \yb}^2$ where $\ub(0)_\infty$ is the kernel-regression initial residual. This provides the *predicted* large-width limit; comparing the finite-width network's loss trajectory to the kernel-regression trajectory measures finite-width deviation.
- **B2 (Logistic regression / linear baseline).** A purely linear model on $\xb_i$: $\hat f(\xb) = \wb^\top \xb$ trained by GD on the same loss. Provides a lower-capacity reference; expected to have much higher final loss.

## Ablations

- **A1 (vary $\eta$).** Sweep $\eta / (\lambda_0/n^2) \in \{0.1, 0.25, 0.5, 1.0, 2.0\}$. Predicted: convergence rate slope scales linearly with $\eta$ in the small-$\eta$ regime; at large $\eta$ instability appears.
- **A2 (vary $\lambda_0$ via input correlation).** Inputs $\xb_i = \rho \mathbf v + \sqrt{1 - \rho^2} \xb_i^\perp$ for fixed unit vector $\mathbf v$ and varying $\rho \in \{0, 0.3, 0.6, 0.9\}$. As $\rho \to 1$, $\lambda_0 \to 0$; measure how $\hat\rho$ degrades and how $m^*$ grows.
- **A3 (vary $d$).** $d \in \{20, 50, 100, 200, 500\}$ with $n, m$ fixed. The theory predicts $d$ enters only through $\Hb^\infty$; should be a mild dependency.

## Plots and tables to produce

- **Figure 1: Training-loss trajectories.** $\log L(\Wb(t))$ vs.\ $t$ for each $m$ (8 lines), with $n = 100$ fixed. X-axis: $t \in [0, 10^5]$. Y-axis: $\log L$. Error bars: $\pm 1$ std over 10 seeds. **Predicts**: line in $t$ with slope matching $\log(1 - \eta\lambda_0/2)$ for $m \gtrsim m^*$. **Verifies**: `\Cref{thm:main}` (Eq.~\eqref{eq:thm_linconv}).
- **Figure 2: Width vs.\ max-neuron displacement.** $\log \max_r \norm{\wb_r(T) - \wb_r(0)}_2$ vs.\ $\log m$ for fixed $T = 5 \cdot 10^4$, $n = 100$. Single line, 8 widths, 10 seeds. Error bars: $\pm 1$ std. **Predicts**: slope $-1/2$ in $\log m$. **Verifies**: `\Cref{thm:main}` (Eq.~\eqref{eq:thm_stayinit}).
- **Figure 3: Width-vs-success phase transition.** Heatmap, x-axis $\log m$, y-axis $n$, cell value = fraction of seeds reaching $L \le 10^{-4}$ within $T$. **Predicts**: transition along a curve $m \asymp n^p / \lambda_0^q$ with $p \in [4, 6]$. **Verifies**: width hypothesis of `\Cref{thm:main}`.
- **Figure 4: Gram spectrum tracking.** $\lambda_{\min}(\Hb(\Wb(t)))$ vs.\ $t$ for fixed $m, n$. **Predicts**: stays above $\lambda_0/2$ throughout. **Verifies**: Eq.~\eqref{eq:hmin_bound} from `\Cref{sec:proof_main}` Step 3.
- **Table 1: Slope estimation.** For each $m$, fit $\log L(\Wb(t)) = \hat \rho \cdot t + b$ on $t \in [10^4, 10^5]$ via OLS; report $\hat \rho$, theoretical $\log(1 - \eta\lambda_0/2)$, ratio $\hat\rho / \log(1 - \eta\lambda_0/2)$, with 10-seed mean $\pm$ std.

## Pre-registered success criteria

**Confirms theory.**
- Figure 2 slope $\in [-0.60, -0.40]$ (predicted $-0.5$).
- Table 1: for $m \ge 5000$, ratio $\hat\rho / \log(1 - \eta\lambda_0/2)$ lies in $[0.90, 1.10]$ for all 4 values of $n$.
- Figure 3: the transition curve (defined as the 50\% iso-line) lies within constant factor 10 of any reasonable theory-predicted curve $m \propto n^p$ with $p \in [4, 6]$.
- Figure 4: $\lambda_{\min}(\Hb(\Wb(t))) \ge 0.5 \lambda_0$ at every $t \in [0, T]$ for all 10 seeds at $n = 100, m = 5000$.

**Refutes theory.**
- Figure 2 slope $\notin [-0.65, -0.35]$ (clearly wrong width scaling).
- Table 1: ratio $\notin [0.75, 1.25]$ for the largest 3 widths at any $n$.
- Figure 3: no monotone phase transition visible.
- Figure 4: $\lambda_{\min}(\Hb(\Wb(t)))$ drops below $0.5 \lambda_0$ at any seed.

## Reproducibility statement

- **Code path:** to be released alongside the camera-ready (placeholder: `https://github.com/<anonymous>/ntk-convergence-verify`).
- **Seeds:** `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`.
- **Configs:** `configs/{linear-rate, width-scaling, phase-transition, gram-tracking}.yaml`.
- **Library versions:** `torch 2.3.0`, `numpy 1.26.0`, `python 3.11`.
- **Hardware:** Single A100 80GB or equivalent. Total budget $\approx 320$ GPU-hours.

---

## Results

*(Section intentionally left blank. Populate after running experiments.)*
