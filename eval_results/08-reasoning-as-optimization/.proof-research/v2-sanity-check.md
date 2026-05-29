# v2 sanity check — phase transition exists; λ_c is d-INDEPENDENT (not 1/d as predicted)

> **⚠ SUPERSEDED (2026-05-26) — POST-MORTEM.** This v2 sanity check correctly detected that the $\lambda_c \sim 1/d$ prediction was wrong, and led to an attempted $\sqrt d$-scaled rescue that ALSO turned out to be broken (see audit of `rem:critical_scaling_origin`). The correct empirical anchor is the v5b argmax-verifier experiment (`v5b-empirical-validation.md`), which shows $\lambda_c \sim \sqrt{\log V/(Td)}$ — derived from $W_U$ incoherence and Gumbel max, no postulated $\alpha(d)$ needed. See `v3-framework-notes.md` for the replacement framework.

---

## Model setup tested

State: $x_t \in \mathbb{R}^d$. Target: origin. Stylized loss: $L(x) = \tfrac{1}{2}\|x\|^2$.

Per step:
- $\text{effective} \sim \text{Bernoulli}(\lambda_0)$ if $\|x_t\| < r_\star$, else $0$.
- If effective: $g_t = \alpha \cdot (-x_t/\|x_t\|) + \sigma \cdot u_t$, $u_t \sim \text{Unif}(S^{d-1})$.
- Else: $g_t = \sigma \cdot u_t$.
- $x_{t+1} = x_t + g_t$ (unbounded); or $x_{t+1} = \Pi_{B(X_\max)}(x_t + g_t)$ (bounded, Revision A).

Parameters: $\alpha = 0.05$, $\sigma = 0.05$, $r_\star = 3$, $R_0 = 1.5$, basin = $0.3$, $T_{\max} = 3000$, $X_\max = 3$ (bounded case).

Sweep: $d \in \{16, 32, 64, 128, 256, 512, 1024, 2048, 3072\}$; $\lambda_0 \in [10^{-3}, 10^{-0.5}]$ on 14-point log grid; 50 trials per cell (30 at $d \ge 2048$).

## Findings

### (1) Phase transition EXISTS at all d

For every tested $d$, the success-rate curve has a sharp transition: success jumps from $\approx 0$ to $\approx 0.9$ between two consecutive λ values on the grid (factor ~1.6 apart). This **confirms the qualitative claim** of a critical effective-rate threshold.

### (2) λ_c is essentially d-INDEPENDENT (not 1/d as theory predicted)

Both bounded and unbounded variants give the same picture (extended to d=8192 with denser grid):

| $d$ | $\lambda_c$ |
|---|---|
| 16 | 0.0376 |
| 64 | 0.0444 |
| 256 | 0.0461 |
| 1024 | 0.0485 |
| 2048 | 0.0491 |
| 3072 | 0.0465 |
| 4096 | 0.0468 |
| 6144 | 0.0457 |
| 8192 | 0.0463 |

Log-log fits:
- **all d**: $\lambda_c \sim d^{+0.027}$, prefactor 0.0380
- **large-d asymptotic ($d \ge 256$)**: $\lambda_c \sim d^{-0.005}$ — completely flat

The slight positive slope when including small d is the $(1 - 1/d)$ finite-d correction in the centrifugal-drift formula. Asymptotically $\lambda_c \to \text{const} \approx 0.046$ independent of $d$.

### (2b) Worse: at marginal λ, large d has LOWER success rate

Success rate at fixed $\lambda = 0.040$ (just below $\lambda_c$):

| $d$ | $P(\text{succ})$ |
|---|---|
| 16 | 0.75 |
| 64 | 0.29 |
| 256 | 0.21 |
| 1024 | 0.12 |
| 3072 | 0.08 |
| 8192 | 0.03 |

Mechanism: concentration of measure means radial fluctuations have variance $\sigma^2/d$. At small $d$, the trajectory can reach the basin by lucky noise; at large $d$, only the deterministic drift can do it, and at marginal $\lambda$ the drift balance is exactly at the threshold. So **the model's original intuition is backwards** in this stylized setup: high $d$ doesn't help reasoning, it slightly hurts at the margin.

### (3) Earlier "wrong-signed" report ($d^{+0.14}$) was small-sample noise

My previous note found $\lambda_c \sim d^{+0.14}$ on $d \in [16, 512]$ with a coarser λ-grid. Extending to $d=3072$ with a denser grid shows the slope is actually within ±0.03 of zero. The previous "wrong-signed scaling" was an artifact of (a) noise in $\lambda_c$ estimates with the coarser grid, and (b) restricting to small d where small-d corrections matter more.

### (4) Diagnosis: why d-independent

In d-dim, for a step $g$ with $\mathbb{E}[g] = 0$, $\text{Cov}[g] = (\sigma^2/d)I$, Itô-style expansion gives:

$$\mathbb{E}[\Delta \|x\| \mid x] \;\approx\; \frac{\sigma^2}{2\|x\|}\left(1 - \frac{1}{d}\right) \;\xrightarrow[d \to \infty]{}\; \frac{\sigma^2}{2\|x\|}.$$

This **centrifugal drift in radius is d-independent in the large-d limit** (the $1-1/d$ factor approaches 1). The balance with inward drift gives:

$$\lambda_c \;\approx\; \frac{\sigma^2}{2 \alpha \cdot r_\text{eff}} \;+\; (\text{small d-correction})$$

i.e. $\lambda_c$ depends on $\sigma, \alpha, r_\text{eff}$ but **not on d** in this stylized model.

The framework's prior "$1/d$ scaling" derivation in v2-framework-notes.md and the A1 proposal implicitly assumed a 1-d stylized model with **noise term $\sigma/\sqrt d$ hard-coded** — i.e. the $1/\sqrt d$ concentration was baked into the noise definition. In the actual d-dim physical model, this $1/\sqrt d$ shows up in *radial fluctuations* but is **dominated by the centrifugal $\sigma^2/(2r)$ term**, which is d-independent.

So the "$1/d$" scaling in the A1 proposal was an artifact of the reduced 1-d model, not a genuine prediction.

## What this means for the framework

The **good news**:
- The phase transition is **empirically real and robust** to (a) bounded vs unbounded, (b) d from 16 to 3072.
- T1 in the form "there exists a sharp $\lambda_c$ such that above it success, below it failure" is empirically supported.
- The phase-transition value $\lambda_c \approx 0.04$ has a clean analytic prediction: $\lambda_c \approx \sigma^2/(2\alpha \bar r)$ where $\bar r$ is the equilibrium radius without effective drift.

The **bad news**:
- The **headline narrative** "$\lambda_c \sim 1/d$ explains why large models reason and small ones don't" is NOT supported.
- In this stylized model, dimension $d$ does NOT directly help.
- The model-size dependence of reasoning must come from somewhere else: e.g., training-induced d-dependence in the $\lambda(L)$ profile, or d-dependence in basin size, or d-dependence in $\alpha$.

## Three options for framework revision

### Option 1 — Keep T1 as-is (d-INDEPENDENT phase transition); drop the "1/d" headline

Reformulate the headline. T1 becomes: "there exists $\lambda_c(\sigma, \alpha, L^*)$ — independent of d — such that snowball vs extinction is sharp". The model-size story moves to a separate observation: "for fixed-$L^*(Q)$ problems, $d$ enters only through (a) basin geometry, (b) training-induced $\lambda$ profile".

**Pros**: Empirically clean; T1 statement is solid; can prove rigorously.
**Cons**: Loses the dramatic "1/d explains scaling" narrative. The framework no longer addresses "why large models reason" directly.

### Option 2 — Modify the model: d-scaled drift α(d) or basin(d)

Let $\alpha = \alpha_0 \cdot d^p$ (effective tokens are "stronger" in larger models) or $\text{basin} = \text{basin}_0 \cdot d^p$. With $p > 0$ you can recover $\lambda_c \sim 1/d^q$ for some q. But this requires justifying the d-dependence of $\alpha$ or basin geometry from real LLM architecture.

**Pros**: Recovers the scaling narrative.
**Cons**: Adds an ad hoc d-scaling assumption that needs separate justification. May open up a new "why does $\alpha$ scale with $d$?" question.

### Option 3 — Move to L-space dynamics where $1/d$ scaling is exact

Work in $L_t = \|x_t\|^2/2$ space and derive the dynamics of $L_t$ directly. Effective steps contribute $-\alpha\sqrt{2L}$ to $\Delta L$. Noise step gives $\Delta L = x\cdot g + |g|^2/2$ with E[noise] = $\sigma^2/2$ (d-independent) but variance of fluctuation around mean is $\sigma^2 \cdot 2L/d$ (does scale 1/d). So in $L$-space, the **variance** of single-step change scales as $1/d$, even though the **mean** of single-step change is d-independent.

Phase transition in $L$-space: drift $-\lambda\alpha\sqrt{2L} + \sigma^2/2$, diffusion $\sigma^2 \cdot 2L/d$. Mean-zero crossing: $\lambda_c = \sigma^2/(2\alpha\sqrt{2L})$ — d-independent.

But: **time-to-basin** depends on diffusion magnitude. With higher d, the trajectory hugs the deterministic mean more closely → less likely to escape via fluctuation. The d-dependence shows up in **success probability at λ < λ_c** (extinction is less probable at small d), not in $\lambda_c$ itself.

**Pros**: Cleaner math; honest statement of where d enters.
**Cons**: Same as Option 1 — no $1/d$ headline.

## Recommendation to coordinator

The simulation says: **the phase transition is real but is d-independent in this stylized model.** The $1/d$ headline was an artifact of the A1 1-d reduction's noise parameterization.

Three concrete options for the user:
- (A) Accept d-independent $\lambda_c$, reformulate framework narrative (Option 1 above)
- (B) Add an ad hoc $\alpha(d)$ or basin($d$) assumption (Option 2)
- (C) Abandon the "why large models reason" angle and write a more modest paper about the phase transition itself (Option 3 / collapsed)

Before LaTeX drafting (Stage A2), the user should pick one. My recommendation is **(A)** — solid math, honest narrative shift — unless the user has a principled justification for (B).

## Files

- `/tmp/v2-sanity-bounded-large-d.py` — d up to 3072 sweep (superseded by xl-d)
- `/tmp/v2-sanity-bounded-xl-d.py` — **current** d-up-to-8192 sweep
- `/tmp/v2-sanity-xl-d-results.json` — full d=8192 sweep results (bounded & unbounded)
- `scripts-v2-sanity-bounded-large-d.py` — copy of d-3072 script preserved here
- This file (`.proof-research/v2-sanity-check.md`) — written notes
- (Earlier scripts `/tmp/v2-sanity-check{,-v2,-v3}.py` and `/tmp/v2-sanity-A1-protocol.py` superseded.)
