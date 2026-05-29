# Technique digest — BA-G-J summary-statistic SDE limit (Ben Arous-Gheissari-Jagannath 2022)

**Purpose.** Provide a high-dimensional limit theorem for a scalar
summary statistic of the reasoning trajectory, used to state Round-3
Theorem **T5** (`thm:T5_asymptotic_ode` in
`sections/12-asymptotic-limit.tex`). T5 states that in the
high-$d$ limit with the critical step-size scaling of the v3 framework,
the order parameter $m_t \coloneqq \inner{W_U^{a^\star}}{x_t}/R_U$
(or equivalently $\inner{W_U^{a^\star}}{x_t}/\norm{W_U^{a^\star}}_2$)
satisfies a *deterministic* ODE / SDE limit governed by the population
drift induced by $\snet$ and the population gradient covariance of the
attention recurrence.

## Picked result — BA-G-J Theorem 2.3

**Reference.** Ben Arous, Gheissari, Jagannath, *High-dimensional
limit theorems for SGD: Effective dynamics and critical scaling*,
Communications on Pure and Applied Mathematics 77(3):2030–2080,
2024 (arXiv 2022, 2206.04030). Theorem~2.3 is the generic
scaling-limit theorem; see also their Section~2.2 ("Critical scaling
regime") and Remark~1 for the $\delta_n \asymp 1/d$ identification.

## Statement (paraphrased to our notation)

Let $(X_\ell)_{\ell \ge 0}$ be a discrete-time process on $\R^d$
(in our setting: $X_\ell \equiv x_\ell$, the residual stream at
reasoning step $\ell$). Let $u : \R^d \to \R$ be a scalar
*summary statistic*. Define the rescaled process
$$u^{(d)}_t \;\coloneqq\; u\bigl(x_{\lfloor t\,\delta_d^{-1}\rfloor}\bigr)$$
for a step-size schedule $\delta_d > 0$ converging to $0$ as
$d \to \infty$.

**Hypotheses** (their Defs.\ 2.1, 2.2):
- **(BAGJ-H1) Asymptotic closability.** There exist measurable
  $h : \R \to \R$ (population drift) and $\Sigma : \R \to \R_{\ge 0}$
  (population diffusion) such that the conditional mean increment
  and conditional second moment of the increments of $u$ close
  asymptotically onto functions of $u$ alone:
  $$\E\!\left[u(x_{\ell+1}) - u(x_\ell) \,\big|\, x_\ell\right]
    \;=\; \delta_d \cdot h(u(x_\ell)) \;+\; o(\delta_d),$$
  $$\E\!\left[\bigl(u(x_{\ell+1}) - u(x_\ell)\bigr)^2 \,\big|\, x_\ell\right]
    \;=\; \delta_d \cdot \Sigma(u(x_\ell)) \;+\; o(\delta_d),$$
  uniformly on compact subsets of $u$-values.
- **(BAGJ-H2) Localizability.** For each compact set
  $K \subset \R$ the increments of $u$ along the trajectory are
  bounded ($\sup_\ell \abs{u(x_{\ell+1}) - u(x_\ell)} \to 0$ in
  probability uniformly on $\{u(x_\ell) \in K\}$), and the residual
  martingale-difference fluctuations after subtracting the drift are
  $L^2$-tight under $\delta_d^{-1}$ rescaling.
- **(BAGJ-H3) Drift Lipschitz.** $h$ is Lipschitz on compacta.
- **(BAGJ-H4) Diffusion regular.** $\Sigma$ is continuous and
  non-degenerate ($\Sigma \ge c_0 > 0$ on the relevant compact set)
  *if* an SDE limit (rather than ODE) is desired. For ODE limits
  $\Sigma \equiv 0$ is permitted provided **(BAGJ-H1)** holds with
  $o(\delta_d)$ tightness in the second-moment sense.

**Conclusion.** Under (H1)-(H4) and a tightness condition (their
Eq.~(2.8)), the rescaled process $u^{(d)}_t$ converges weakly (in
the Skorokhod topology on $D([0, T_\infty]; \R)$) to the solution
of the SDE
$$du_t \;=\; h(u_t)\,dt \;+\; \sqrt{\Sigma(u_t)}\, dB_t,
   \qquad u_0 \;=\; \lim_{d\to\infty} u(x_0).$$
If $\Sigma \equiv 0$, the limit is the deterministic ODE
$\dot u = h(u)$.

## Hypothesis verification for our $m_t$

Our candidate summary statistic is
$$m_t \;\coloneqq\; \frac{\inner{W_U^{a^\star}}{x_t}}{R_U}
   \;\in\; \R,$$
where $a^\star \in \arg\max_{a \in \Aset} \norm{W_U^a}_2$
(\Cref{lem:signal_accumulation}). Why $m_t$ rather than the loss
$\loss(x_t; Q)$: $m_t$ is *linear* in $x_t$, which makes
(BAGJ-H1) computable in closed form from the per-step value-vector
distribution; $\loss(x_t;Q)$ involves log-sum-exp non-linearity in
$x_t$ and requires Taylor-expanding before applying BA-G-J,
introducing curvature corrections at every step.

**Step-size identification.** The natural step size in our setting
is the average softmax weight $\tau = 1/T_{\max}$ of
\Cref{eq:tau_def}. We take $\delta_d \coloneqq 1/T_{\max}(d)$ with
$T_{\max}(d) = c \cdot d$ (the critical scaling identified by
Saad-Solla 1995 / BA-G-J 2022; matches the
$\Theta(1/\sqrt{T_{\max} d})$ critical-rate scaling of T1 evaluated
at $\snet = \Theta(1/\sqrt d)$, the snowball threshold).

**(BAGJ-H1) Asymptotic closability — yes, with caveat.** Per-step
increment of $m_t$ from \Cref{lem:softmax_running_average} is
$$m_{t+1} - m_t
   \;=\; \frac{w_{T_{\max}, t+1}}{R_U}\,
         \bigl(\inner{W_U^{a^\star}}{V_{t+1}} - m_t \cdot R_U\bigr)$$
(after rewriting the running-average recurrence
$x_{t+1} = (1 - w_{t+1})\, x_t + w_{t+1}\, V_{t+1}$ and projecting
onto $W_U^{a^\star}/R_U$). Conditional mean given $\Fcal_t$:
$$\E[m_{t+1} - m_t \mid \Fcal_t]
   \;=\; \frac{w_{T_{\max}, t+1}}{R_U} \cdot
         \bigl(\E[\inner{W_U^{a^\star}}{V_{t+1}} \mid \Fcal_t] - m_t R_U\bigr).$$
By the three-mode signed-effective decomposition
(\Cref{def:effective_indicator}) together with
\Cref{ass:effective_step_alignment}, the conditional expectation
of $\inner{W_U^{a^\star}}{V_{t+1}}$ given $\Fcal_t$ in the snowball
region $\{\loss_t < \Lstar\}$ is
$\snet(Q) \cdot \cos\theta_0 \cdot R_U$ (Lemma~B Step~1 calculation,
folded into the absolute scale).

**Closability requires:** the conditional drift on the RHS depends
on $m_t$ only through the indicator $\1\{\loss_t < \Lstar\}$ and an
additive $-m_t R_U$ term. The first dependence is **not closable
in $m_t$ alone** in general: $\loss_t$ is a log-sum-exp functional
of the full state $x_t$, not of $m_t$. *Closability holds only
under the additional assumption that $\loss_t$ is itself a
(known, monotone) function of $m_t$ in the asymptotic
high-confidence regime.* This is the **strengthening** required
for T5 to apply BA-G-J cleanly — see §Risks below.

**Verdict on (H1).** Holds under the following **derived
assumption** (to be stated explicitly as a working stylisation in §12):
$$\text{(AS) Asymptotic single-coordinate dominance: }
\loss_t \;=\; \phi(m_t) + o_d(1)\text{ on the trajectory},$$
for an explicit Lipschitz function $\phi : [-1, 1] \to \R_{\ge 0}$
with $\phi(1) = 0$ and $\phi(0) \approx \log(|\Vocab|^n)$. Under
(AS), the snowball indicator $\1\{\loss_t < \Lstar\}$ becomes
$\1\{m_t > \phi^{-1}(\Lstar)\}$, a function of $m_t$ alone.

**Provenance of (AS).** When the trajectory is in the snowball region
near the basin around $a^\star$, the correct-mass functional
$\cmass(x_t; Q)$ is dominated by the single largest correct logit
$(W_U x_t)_{a^\star}$, so
$\loss_t \approx \log(\sum_v e^{(W_U x_t)_v}) - (W_U x_t)_{a^\star}$
$\approx \log(|\Vocab|^n - 1) e^{-(W_U x_t)_{a^\star}} \cdot (1 + o(1))$
in the regime where $(W_U x_t)_{a^\star}$ dominates the incorrect-side
max. Since $(W_U x_t)_{a^\star} = m_t R_U$, this gives $\phi(m) =
\log(|\Vocab|^n) - m R_U + o(1)$ in the *asymptotic regime*. The
*non-asymptotic* regime (when the incorrect-side max competes with the
correct logit) requires Lemma~A's incoherence bound, which T1 already
uses, but BA-G-J does not. **This is the load-bearing
strengthening.**

**(BAGJ-H2) Localizability — yes.** The per-step increment satisfies
$\abs{m_{t+1} - m_t} \le w_{T_{\max}, t+1} \cdot (M + R_U)/R_U \le
e^{2S}/(T_{\max} \cdot R_U) \cdot (M + R_U) = O(1/T_{\max})$
by \Cref{lem:max_attention_weight} (deterministic max softmax-weight
bound) together with $\norm{V_{t+1}} \le M$ from
\Cref{ass:bounded_value_norms} and $\norm{x_t} \le M$ from the
convex-combination representation. Hence per-step increments shrink
as $1/T_{\max} \to 0$ as $d \to \infty$ in the critical scaling
$T_{\max} \asymp d$, satisfying the localizability condition uniformly
in $m_t$.

**(BAGJ-H3) Drift Lipschitz — yes under (AS).** The drift is
$$h(m) \;=\; \snet(Q) \cdot \cos\theta_0 \cdot \1\{m > m^\star\}
   - m \cdot \1\{m > m^\star\}$$
plus boundary-region terms. The indicator term is discontinuous at
$m = m^\star$, technically violating Lipschitz; this can be
**regularised** in three ways: (a) smoothed snowball assumption
$\lambda_+(\loss)$ Lipschitz in $\loss$ (a natural strengthening of
\Cref{ass:snowball_aligned} for T5 only); (b) restrict the ODE
limit to a one-sided interval $m \in (m^\star, 1]$ avoiding the
discontinuity; (c) accept a weak-solution limit with an
absorbing/reflecting boundary at $m = m^\star$. Recommendation (a) is
cleanest and only used for T5.

**(BAGJ-H4) Diffusion regular — no, only marginally.** The conditional
second moment is
$\E[(m_{t+1} - m_t)^2 \mid \Fcal_t] = w_{T_{\max}, t+1}^2 \cdot
\Var[\inner{W_U^{a^\star}}{V_{t+1}} \mid \Fcal_t] / R_U^2 + \text{drift}^2$,
and the noise-step variance is $O(M^2 R_U^2/(d R_U^2)) = O(M^2/d)$
by \Cref{lem:orthogonality_high_d}. Per step,
$\E[(m_{t+1} - m_t)^2 \mid \Fcal_t] \le (e^{2S}/T_{\max})^2 \cdot M^2/d
= O(1/(T_{\max}^2 d))$. Over $1/\delta_d = T_{\max}$ steps, the
cumulative second-moment contribution is $T_{\max} \cdot
O(1/(T_{\max}^2 d)) = O(1/(T_{\max} d))$. In the critical scaling
$T_{\max} \asymp d$, this is $O(1/d^2) \to 0$.

**This means $\Sigma(m) = 0$ — the BA-G-J limit is an *ODE*, not an SDE.**

**Verdict on (H4).** Diffusion vanishes in the critical scaling
$T_{\max} \asymp d$ because our per-step variance is
$O(1/(T_{\max}^2 d))$ rather than the BA-G-J-canonical $1/(T_{\max} d)$.
This is because our softmax-running-average weights $w_{T_{\max}, t}$
are $O(1/T_{\max})$ rather than $O(1)$ — i.e., our setting is
*sub-critical* in the BA-G-J sense, and the natural BA-G-J scaling for
non-trivial diffusion would be $T_{\max} \asymp \sqrt d$. With this
alternative scaling, $\Sigma(m) = O(1)$ and we get a non-trivial SDE
limit. Either choice is defensible; we recommend the ODE limit because
it matches the v3 framework's $T_{\max} \asymp d$ regime and gives a
cleaner statement.

## Limit ODE for $m_t$

Under (AS) + the strengthened snowball assumption with
$\lambda_+(\loss)$ Lipschitz, the limit ODE is
$$\boxed{\;\dot m_t \;=\; \snet(Q) \cdot \cos\theta_0 \cdot
                     \1\{m_t > m^\star\} \;-\; m_t \cdot \1\{m_t > m^\star\}
                     \;+\; o_d(1),\;}$$
where $m^\star = \phi^{-1}(\Lstar)$ is the snowball-region threshold
in $m$-coordinates. Stationary points of the ODE on
$(m^\star, 1]$ satisfy $\dot m = 0 \Leftrightarrow
m = \snet \cdot \cos\theta_0$, giving the **deterministic
fixed-point prediction**
$$m_\infty \;=\; \snet(Q) \cdot \cos\theta_0,$$
the high-$d$ limit value of the correct-row alignment at convergence
(matches Lemma~B's mean signal calculation evaluated at $T_{\max}\tau
= 1$, as expected).

The ODE is **bistable** with attracting fixed point $m_\infty$ for
$\snet > 0$ and the boundary $m^\star$ as an unstable equilibrium
(reflecting the snowball/extinction dichotomy of T1 in the
deterministic limit). The basin of attraction of $m_\infty$ is
$(m^\star, 1]$.

## Citation

**Yes, a `\cite{}` is needed** — `\cite{benarous2022highdim}` is
already in `refs.bib` from the v3 framework discussion of
\Cref{rem:orthogonality_structural}. The existing citation digest
`.proof-research/cite-benarous2022highdim.md` documents the same
result. **No new citation entry is needed**, but the existing digest
should be referenced from the new §12. We also re-cite
`\cite{saad1995online}` for the order-parameter historical precedent.

## What T5 delivers (relative to T1, T4)

- **T1**: probabilistic snowball/extinction dichotomy with explicit
  failure budgets $\delta_\pm$.
- **T4**: Gaussian-CDF interpolation in the critical fragility window
  with Berry-Esseen rate.
- **T5**: deterministic ODE limit $\dot m = h(m)$ in the
  $d \to \infty$ scaling, showing $m_t$ converges *as a deterministic
  trajectory* to the predicted fixed point $\snet \cdot \cos\theta_0$.
  This is the **deterministic-equivalent** companion of T1/T4: the
  *probabilistic* trajectory of T1/T4 is concentrated around the
  deterministic ODE solution of T5 to within $O(1/\sqrt d)$.

## Caveats / load-bearing assumptions

1. **(AS) Asymptotic single-coordinate dominance.** Required to close
   the conditional drift on $m_t$ alone (not on the full state $x_t$).
   This is a strengthening of the v3 framework and must be stated
   explicitly as a hypothesis of T5 (not used by T1, T2, T3, T4).
   **Provenance:** holds approximately when the trajectory is in a
   neighbourhood of the basin around $a^\star$ where the
   incorrect-side max is dominated; needs an extra logarithmic
   factor to make rigorous (the Lemma~A drift bound). Adding (AS) as
   an *assumption* for T5 only is the cleanest path; the
   alternative is to do a Lemma-A-style joint analysis of the
   incorrect-side max which complicates the BA-G-J framework.

2. **Lipschitz $\lambda_+(\loss)$.** Strengthening of
   \Cref{ass:snowball_aligned} to ensure (BAGJ-H3) drift Lipschitz.
   Easiest fix: state "if $\lambda_+$ is Lipschitz in its argument"
   as a hypothesis of T5; this is a structural property of trained
   policies (no discontinuity at $\loss = \Lstar$ in real models).

3. **Critical scaling $T_{\max} \asymp d$.** Required for the
   localizability condition (BAGJ-H2). The headline v3
   $\critrate \sim 1/\sqrt{T_{\max} d}$ has this scaling baked in
   (taking $T_{\max} = c \cdot d$ gives $\critrate \sim 1/d$). For
   $T_{\max} = o(d)$ (e.g., $T_{\max}$ constant), the BA-G-J limit
   does not apply directly and the per-step localizability fails;
   T5's regime of validity excludes this.

4. **Diffusion vanishes; ODE limit only.** The natural BA-G-J SDE
   limit reduces to an ODE in our scaling. This is *good news* for
   T5's deterministic-equivalent role but means we cannot use the
   SDE-limit machinery (e.g., Wong-Zakai stochastic averaging) — the
   limit is a deterministic ODE with explicit $h$.

## Regime of validity for T5

T5 applies in the **high-d critical-scaling regime**
$T_{\max} \asymp d \to \infty$ with $\snet(Q), \cos\theta_0, R_U, M$
held fixed. The ODE limit $\dot m = h(m)$ is valid uniformly on
compact subsets of $m \in [m^\star + \epsilon, 1 - \epsilon]$ for any
$\epsilon > 0$; near the boundary $m = m^\star$ the limit ODE has
discontinuous drift and the BA-G-J framework needs a smoothed
$\lambda_+$.

T5 does **not** apply to the extinction branch directly (where
$\snet < 0$ or $\loss > \Lstar$ and the snowball assumption
gives no lower bound on the drift) — extinction is properly
covered by T1(ii) and the GW machinery of §06.
