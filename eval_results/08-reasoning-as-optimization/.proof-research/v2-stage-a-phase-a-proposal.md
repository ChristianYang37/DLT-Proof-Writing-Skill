# v2 Stage A Phase-A reconnaissance proposal

> **⚠ SUPERSEDED (2026-05-26).** v2 framework discovered to have 12 bugs. Replaced by v3 verifier-argmax framework. See `v3-framework-notes.md`. This file preserved as historical record; do not use as orientation.

---

**Status.** Phase A only. No `.tex` files modified. Successor to v1's
`paper-rewrite-stage-1-proposal.md`. Reads the v2 framework
(`v2-framework-notes.md`) end-to-end and commits to a single decomposition,
assumption set, and dependency graph for the high-d random-walk + snowball
analysis of reasoning-token dynamics. Salvages
`sections/03-lemma-softmax-running-average.tex` unchanged.

This document is structured per the user's seven-part prompt. After
each part, an explicit `v1 vs v2` contrast is included.

---

> **⚠ REVISED post-sanity-check (2026-05-25):** The headline scaling
> $\lambda_c \sim 1/d$ stated below was derived under the assumption
> that the noise term in the 1-d stylized model is $\sigma/\sqrt d$
> with $\sigma$, $\alpha$ both $d$-independent. The Stage A3 numerical
> sanity check up to $d=8192$ revealed this gave $\lambda_c$ **flat in
> $d$** in the actual $d$-dim physical model, because the dominant
> radial drift term is $(d-1)\sigma^2/(2rd)$ which is $d$-independent
> in the limit. The framework was rescued by adopting the standard
> Saad–Solla / Ben Arous–Gheissari–Jagannath **critical step-size
> scaling** $\alpha(d) \sim \sqrt d$, which gives the revised headline
> $\lambda_c \sim 1/\sqrt d$. This is verified empirically (slope
> $-0.60$ in log-log fit; theory $-0.50$ plus finite-$d$ correction).
>
> Everything below is structurally correct (decomposition, dependency
> graph, lemma set) — only the explicit scaling prefactor in T1 needs
> updating to use $\alpha(d) = \alpha_0 \sqrt{d/d_0}$. See updated
> `v2-framework-notes.md` for the revised T1 statement and citation
> digests `cite-benarous2022highdim.md`, `cite-saad1995online.md`,
> `cite-tsiolis2025phase.md` for the foundational scaling-limit
> literature.

---

---

## 0. Executive frame

v1 sold reasoning as biased SGD; the binding cost was an empirically
intractable bias floor $\beta^2/\eta_0$, and the rate term itself was
shown (by the v1 sanity check) to be too slow at empirical $T \le 10^5$
for any honest interpretation. The user's deeper critique landed: most
reasoning tokens are not gradient steps at all. They are random walks on
a loss plateau, and the model survives them because the residual stream
is high-dimensional and orthogonal-by-default.

v2's headline is a **sharp phase transition**: there exists a critical
effective-token rate $\lambda_c(d, Q) \sim \sigma^2 / (\alpha \cdot d)$
such that above $\lambda_c$ a snowball event occurs w.h.p. and the loss
enters its correct basin; below $\lambda_c$ extinction dominates and the
loss is repelled from the basin by random-walk drift. The substantive
prediction is the $1/d$ scaling: this is where reasoning-scales-with-size
becomes a theorem, not a slogan.

The reconnaissance below commits to decomposition **(a) Hidden Markov
two-mode** as the formalization (selected over (b), (c) for tractability
+ interpretability), specifies a single load-bearing assumption (SS), and
builds a 9-lemma + 3-theorem dependency graph that aims at this
headline.

---

## Part 1 — Decomposition choice + formalization

### 1.1 Evaluation of three candidate decompositions

| Decomposition | Tractability of phase transition | Empirical realism | Headline novelty |
|---|---|---|---|
| **(a) HMM two-mode** | High — reduces to mixture of Bernoulli + spherical noise; clean coupling to a comparison Markov chain; phase transition follows from drift–diffusion balance | Medium — discrete "effective vs noise" dichotomy is a caricature; most tokens are partially effective | High — clean dichotomy interpretable as "this token did productive work" |
| **(b) Continuous decomposition** | Medium — coefficients $\alpha_j, \beta_j$ are state-dependent random variables, so the per-step law is a random measure indexed by $L_{j-1}$; Lyapunov drift argument still works but constant tracking gets messy; phase transition becomes a comparison between $\E[\alpha_j \mid L]$ and $\E[\beta_j^2 \mid L]/d$ rather than a clean Bernoulli rate | High — matches what one actually observes in logit-lens probes (mostly small alignment, occasional spikes) | Medium — the "novel" parameter is a continuous distribution rather than a single rate $\lambda$; harder to sell as "the critical rate is $\lambda_c$" |
| **(c) Poisson point process** | Medium-low — requires continuous-time limit, hence a separate convergence-of-discrete-to-continuous step; phase transition becomes a comparison of Poisson intensity to diffusion coefficient (classical birth–death + diffusion = a Wright–Fisher-style SDE); the SDE limit is well-understood but the discretization step is a 20-page detour | Medium — Poisson assumption (independent arrivals) is shaky once one acknowledges the policy state-dependence; CTMC framing is unfamiliar to ML reviewers | Medium-high — gives sharpest mathematical statement of the transition (it's literally a CTMC bifurcation) but trades off audience comprehension |

### 1.2 Commitment — decomposition (a) Hidden Markov two-mode

I commit to **(a)** as the v2 decomposition. Rationale, in priority
order:

1. **Tractability is highest.** The Bernoulli + spherical-noise structure
   makes every per-step calculation a textbook computation: the drift
   conditional on the effective event is $-\alpha$ (deterministic), and
   the noise is a centered, isotropic spherical perturbation. This
   decouples the "is this step effective?" question from the "how big a
   step?" question, which is exactly what we need for a clean snowball
   argument.
2. **The phase transition is a direct drift-vs-diffusion comparison.**
   Above the threshold, the conditional drift $-\lambda \cdot \alpha$
   dominates the diffusion variance $\sigma^2/d$ per unit time, so the
   process is a supermartingale on the level set $\{L < L^*\}$. Below
   the threshold, the diffusion dominates the drift and the process
   makes positive-loss excursions of magnitude $\Omega(\log d)$ with
   constant probability (standard random-walk hitting-time argument).
3. **The Bernoulli rate $\lambda$ is exactly the v1 inference-time
   observable** that the entire research program is pitched on. v2 turns
   it from a "lower bound" into "the rate parameter" — much sharper.
4. **Loss of (b)'s realism is recoverable as a remark.** A 2-paragraph
   "robustness" remark observes that (a) can be viewed as a Bernoullified
   surrogate for (b) with the calibration $\lambda \mapsto \E[\alpha_j]/\alpha$;
   this preserves all qualitative conclusions and is the standard
   stylization-of-continuous-process move in the random-walk literature.
5. **(c) is the right limit for the proof but the wrong starting point.**
   In a hypothetical follow-up paper, we would derive (c) from (a) by
   the standard discrete-to-continuous CTMC limit. For v2 we stay in
   discrete time.

### 1.3 Precise formalization

**State space.** $L_t \in \R_{\ge 0}$, the loss along the trajectory at
reasoning step $t \in \N$. The loss is the constrained-softmax loss
$L(x;Q) = -\log \pi(x;Q)$ from v1; the gradient form
$\nabla L = W_U^\top(p - q_C)$ and the smoothness bound
$L_{\mathrm{sm}} \le \|W_U\|^2/2$ are inherited unchanged from
`paper-rewrite-stage-1-proposal.md` §1.

**Filtration.** $\mathcal F_t = \sigma(L_0, L_1, \ldots, L_t)$, augmented
with the indicator history (defined below).

**Effective indicator.** A Bernoulli random variable $E_t \in \{0,1\}$
defined per step, with
$$
   \Pr[E_t = 1 \mid \mathcal F_{t-1}] \;=\; \lambda(L_{t-1}),
$$
where $\lambda : \R_{\ge 0} \to [0, 1]$ is measurable, non-increasing in
$L$ (smaller loss $\Rightarrow$ larger rate), $\lambda(L) = 0$ for
$L > L^*(Q)$ (bad-region cutoff), and $\lambda(L) \ge \lambda_0 > 0$ for
$L < L^*(Q)$ (snowball region). $L^*(Q)$ is a question-dependent
"basin boundary" — see Part 2 (SS).

**Step update.**
$$
   L_t - L_{t-1} \;=\; -E_t \cdot \alpha \;+\; \frac{\sigma}{\sqrt d}\, \xi_t,
   \qquad \xi_t \mid \mathcal F_{t-1}, E_t \;\sim\; \mathcal N(0, 1).
$$
Here:

- $\alpha > 0$ is the per-effective-token drift magnitude (a postulated
  constant, with empirical interpretation in Part 2).
- $\sigma > 0$ is the per-step noise scale (a postulated constant).
- $d$ is the residual-stream dimension (the "model size" parameter).
- The $1/\sqrt d$ is the high-dimensional orthogonality concentration:
  when projected onto a fixed direction (here $\nabla L$), a unit-norm
  random vector in $\R^d$ has variance $1/d$.

**Measurability.** $(E_t, \xi_t)$ are conditionally independent given
$\mathcal F_{t-1}$. $E_t$ is $\mathcal F_t$-measurable.

**Boundary at zero.** $L_t \ge 0$ by definition (negative cross-entropy
is impossible); enforce a reflecting boundary at $L = 0$ — under the
snowball regime the process spends almost-all of its time strictly
above $0$ so the boundary is decorative.

**"Effective"** is defined intrinsically: token $t$ is effective iff
the indicator $E_t = 1$ fires, where the firing probability is the
function $\lambda(L_{t-1})$. v2 does not commit to an *external*
oracle determining effectiveness — the rate $\lambda$ is the
inference-time observable, exactly as in v1, but now without the
margin/anchor conditions C2 + C3.

### 1.4 What this commits to (and what it deliberately does not)

**Does commit to.**
- A single state variable $L_t \in \R$ (vs. v1's $x_t \in \R^d$ with
  $L = L(x_t)$). The reduction to scalar $L_t$ is the *stylization*; in
  Part 5 risk R1 we note that the snowball argument is genuinely 1d.
- A specific noise model: i.i.d. Gaussian per step, scaled by
  $1/\sqrt d$. The Gaussianity is convenient; the structural fact is
  the high-d orthogonality concentration, which holds for any
  rotationally symmetric noise.
- A constant per-effective drift $\alpha$. The proof allows $\alpha$ to
  be replaced by a state-dependent $\alpha(L)$ bounded away from zero;
  for clarity v2 uses the constant version in the main statement and
  notes the generalization in a remark.

**Does not commit to.**
- A specific functional form for $\lambda$. Only the cutoff structure
  matters: $\lambda > 0$ in the snowball region, $\lambda = 0$ in the
  bad region. The argument is robust to whether $\lambda$ is
  step-function, linear, sigmoidal, etc.
- A specific dependence of $\alpha$ on $d$ or $Q$. Both could be
  $\alpha = \alpha(d, Q)$ and the phase-transition statement is then a
  joint scaling claim. The headline T1 statement keeps $\alpha$ fixed
  for clarity.

### 1.5 v1 vs v2 contrast for this part

v1 modeled $g_j$ as $\E[g_j] = -\eta_j \nabla L + b_j$ with $\|b_j\| \le
\beta$, i.e. **every token attempts a gradient step**. The sanity check
showed half of untrained-model tokens have $\hat\eta_j < 0$, so the v1
decomposition fails its precondition — it requires *trained* policies
even to make sense. v2 explicitly models the dichotomy "this token did a
gradient step" vs "this token did a random walk", with the proportion
determined by an emergent rate $\lambda$. **v2 does not require
trained-policy alignment to make sense**; the rate $\lambda$ is allowed
to be very small in untrained-model regimes (extinction), and the
theorem still says something meaningful: "untrained models extinct
under this dynamics, trained models snowball, the boundary is sharp".

---

## Part 2 — Full assumption set

The v1 trio C1+C2+C3 (per-step gradient correctness, anchor probability
lower bound, score margin) collapses to a single load-bearing assumption
(SS) plus four auxiliary conditions. Each is listed with mathematical
statement, empirical interpretation, and a mildness check that
explicitly contrasts to v1.

### 2.1 (SS) Snowball / state-dependent effective rate (load-bearing)

**Statement.** There exists a measurable function $\lambda : \R_{\ge 0}
\to [0, 1]$, a threshold $L^*(Q) > 0$, and a constant $\lambda_0 > 0$
such that, conditional on $\mathcal F_{t-1}$,
$$
   \Pr[E_t = 1 \mid \mathcal F_{t-1}] \;=\; \lambda(L_{t-1}),
$$
with the cutoff structure:
- $\lambda(L) \ge \lambda_0 \cdot \mathbb 1[L < L^*(Q)]$ (snowball region active),
- $\lambda(L) \le \overline\lambda \cdot \mathbb 1[L < L^*(Q)]$ (bounded above).

**Empirical interpretation.** A practitioner trains a probe to detect
"effective" tokens (e.g., tokens whose ablation harms downstream
accuracy by more than $\tau$), measures the empirical fraction of
effective tokens conditional on a coarse loss bucket $L \in [L^* -
\Delta, L^*]$, and reports a lower bound. This is *one number per
loss bucket*, qualitatively similar to the v1 anchor-emission-probability
estimate but without the "anchor set" overhead.

**Mildness check.** Strictly weaker than v1's C2 in three concrete
senses:

1. **No uniform lower bound across all $L$**: $\lambda$ may be zero in
   bad regions ($L > L^*$). v1's C2 required a uniform $p_0 > 0$
   across all trajectory states.
2. **No per-token assertion about alignment**: $\lambda$ is just a
   rate, not a per-step gradient condition. v1's C2 was bundled with
   the C1 alignment condition.
3. **No anchor set required.** The "effective" indicator is intrinsic to
   the loss process. v1 needed a fixed anchor set $A(Q) \subseteq
   \mathcal V$ with sub-token measurement infrastructure.

vs. "model knows the answer": (SS) is *much* milder. "Model knows the
answer" would require $\lambda$ to be close to $1$ uniformly on a
large region; (SS) requires only that $\lambda$ be **positive** on the
snowball region, with $\lambda$ allowed to be small enough that the
critical $\lambda_c$ is comparable.

### 2.2 (SM) Smoothness inheritance

**Statement.** The constrained-softmax loss $L(\cdot; Q)$ on $\R^d$ is
$L_{\mathrm{sm}}$-smooth with $L_{\mathrm{sm}} \le \|W_U\|^2 / 2$.

**Empirical interpretation.** A single number: the operator norm of the
unembedding matrix, available at inference time.

**Mildness check.** Identical to v1's lem:smoothness. Verified by direct
Hessian computation; no new condition imposed.

### 2.3 (BD) Bounded drift magnitude

**Statement.** The per-effective-token loss decrement satisfies
$\alpha \ge \alpha_{\min} > 0$.

**Empirical interpretation.** Same probe as (SS): conditional on $E_t = 1$,
measure the average loss decrement. This is *one number*, period.

**Mildness check.** Auxiliary; this is essentially the "informativeness
of effective tokens" parameter. Stronger than (GC-correlated) (v1
§3.3) in that we ask for a positive *decrement* in $L$, not just a
positive cosine.

### 2.4 (HD) High-dimensional projection of noise

**Statement.** Conditional on $\mathcal F_{t-1}$ and $E_t = 0$, the
projection of the per-step noise onto any fixed direction has variance
$\sigma^2 / d$. Equivalently: the random-walk component of $g_t$ is
$\sigma$-sub-Gaussian per coordinate before $\sqrt d$ rescaling.

**Empirical interpretation.** Probe: at a held-out trajectory, compute
the empirical covariance of the random-walk component (defined as
$g_t - \E[g_t \mid \mathcal F_{t-1}]$) and check that the projection
onto $\nabla L / \|\nabla L\|$ has variance scaling as $1/d$.

**Mildness check.** This is the **substantive new assumption of v2**
relative to v1. It encodes the high-d orthogonality intuition. It is
not "uniformly distributed activations" — it only asserts a per-direction
variance bound that follows from isotropy *of the noise component*. Random-init
transformers satisfy this; trained transformers almost certainly
satisfy it (their value vectors lie in a subspace of low effective
rank, but the per-step *increment* is still bounded in $\ell^2$ and is
not concentrated in the gradient direction except via the $\lambda$
mechanism).

### 2.5 (BV) Bounded value norms (salvaged)

**Statement.** Per-token value vectors satisfy $\|V_t\| \le M$
uniformly.

**Empirical interpretation.** Standard. Identical to v1's
ass:bounded_value_norms.

**Mildness check.** Mild and unchanged.

### 2.6 What was abandoned

- **v1 C1 (gradient correctness)**: GONE. Most tokens are not
  gradient steps; only the effective-token fraction is.
- **v1 C2 (uniform anchor probability)**: REPLACED by (SS), which
  allows the rate to vanish in bad regions.
- **v1 C3 (score margin)**: COMPLETELY ABANDONED. v2 makes no
  margin assumption. The "model concentrates on correct tokens"
  story is replaced by the snowball dynamics itself.

### 2.7 v1 vs v2 contrast for this part

v1: 5 conditions (C1-C5), of which 2 (C2, C3) were "diagnose-don't-prove"
postulates whose empirical estimability was open (v1 risk R1
estimated probability 40%-70% that C2 + C3 are intractable). v2: 1
load-bearing condition (SS) + 4 auxiliaries, all directly measurable
from a single probe-and-bucket inference experiment. Net: from 5
postulates to 1 + 4 = 5, but the load-bearing one is *strictly weaker*
and *strictly more measurable*.

---

## Part 3 — Dependency graph for stylized 1-d model

Three theorems (T1, T2, T3) supported by 9 lemmas. Tree depth = 3
(leaves → intermediate Lyapunov / coupling tools → theorems). Topological
order below.

### 3.1 The three theorems

#### thm:phase_transition (T1) — Sharp phase transition
**Statement (informal).** There exists $\lambda_c(d, Q) = c \cdot \sigma^2
/ (\alpha \cdot d)$ such that:
- if $\lambda_0 > \lambda_c$, then $\Pr[L_t \to 0 \text{ as } t \to \infty
  \mid L_0 < L^*] \ge 1 - \delta(d, Q, \lambda_0)$ (snowball);
- if $\lambda_0 < \lambda_c$, then $\Pr[\sup_t L_t > L^* \mid L_0 < L^*]
  \ge 1 - \delta'(d, Q, \lambda_0)$ (extinction).

**Hypotheses.** (SS), (SM), (BD), (HD), (BV).

**Headline novelty.** The $1/d$ scaling of $\lambda_c$ is the
substantive prediction. It says: doubling the model dimension halves
the critical rate, so larger models snowball at lower effective-token
density.

**Proof strategy.** Two-sided. (i) Above $\lambda_c$: construct a
Lyapunov function $V(L) = L$ itself, show $V$ is a supermartingale on
$\{L < L^*\}$ using (SS) + (HD), apply optional-stopping + martingale
convergence. (ii) Below $\lambda_c$: comparison to a positively-drifting
random walk; use classical hitting-time lower bound for the
diffusion-dominant regime (Gambler's ruin in continuous space).

#### thm:conditional_convergence (T2) — Given snowball, polynomial time
**Statement (informal).** Conditional on the snowball event of T1, the
hitting time $T_{\mathrm{converge}} := \inf\{t : L_t \le \log 2\}$
satisfies
$$
   \E[T_{\mathrm{converge}} \mid \text{snowball}] \;\le\; \poly(d, 1/\lambda_0, 1/L^*).
$$

**Hypotheses.** (SS), (BD), (HD) + T1's snowball event.

**Proof strategy.** Apply a drift lemma (lem:drift_quantitative below)
to bound expected loss decrease per step by $\lambda_0 \alpha / 2$ in
the snowball region; standard mean-hitting-time lemma for a drifted
random walk on $\R_{\ge 0}$ gives $\E[T] \le L_0 / (\lambda_0 \alpha / 2)$,
which is $\poly$ in the listed parameters.

#### thm:problem_difficulty (T3) — Minimum model dimension
**Statement (informal).** Define
$$
   \mathcal D(Q) \;:=\; \inf\{d : \lambda_c(d, Q) < \lambda_0(Q)\}.
$$
Then $\mathcal D(Q)$ is a question-intrinsic "minimum reasoning
dimension". For any $d < \mathcal D(Q)$, T1's extinction branch fires
(no chain-of-thought of any length, in this model class, succeeds with
nontrivial probability). For $d \ge \mathcal D(Q)$, T1's snowball branch
fires.

**Hypotheses.** T1.

**Proof strategy.** Direct corollary of T1 by solving
$\lambda_c(d, Q) = \lambda_0(Q)$ for $d$. The interpretation as
"problem difficulty" relies on (i) $\lambda_0$ being a property of $Q$
(and the model class), and (ii) $\lambda_c \propto 1/d$, so
$\mathcal D(Q) \sim \sigma^2 / (\alpha \cdot \lambda_0(Q))$.

### 3.2 The nine lemmas

#### lem:softmax_running_average (SALVAGED — unchanged from v1)
**Statement.** $x_j = (s_{j-1}/s_j) x_{j-1} + g_j$; equivalent
convex-combination form.
**Hypotheses.** Definitions only.
**Downstream consumers.** lem:loss_recursion (one-step loss decomposition).
**Technique.** Direct algebra. No technique digest needed.
**File status.** `sections/03-lemma-softmax-running-average.tex` —
verified still applies. The lemma's content is *purely* algebraic about
the softmax recurrence and makes no reference to the assumption set
(v1 or v2). Salvage with no edit.

#### lem:loss_decomposition (NEW)
**Statement.** Under the formalization in Part 1, the per-step loss
update has the decomposition
$$
   L_t - L_{t-1} \;=\; -E_t \alpha \;+\; (\sigma / \sqrt d) \xi_t \;+\; R_t,
$$
where $R_t$ is a remainder bounded by $L_{\mathrm{sm}} M^2 / 2$ via
(SM) + (BV).
**Hypotheses.** (SM), (BV).
**Downstream consumers.** lem:drift_one_step, lem:concentration_one_step.
**Technique.** Descent lemma + Taylor expansion of $L$ around $x_{t-1}$.
Standard.
**Technique digest needed.** No (textbook).

#### lem:drift_one_step (NEW)
**Statement.** $\E[L_t - L_{t-1} \mid \mathcal F_{t-1}] = -\lambda(L_{t-1})
\alpha + O(L_{\mathrm{sm}} M^2 / d)$.
**Hypotheses.** (SS), (HD), (BD), lem:loss_decomposition.
**Downstream consumers.** lem:lyapunov_drift, lem:drift_quantitative.
**Technique.** Conditional expectation of the indicator + Gaussian noise
projection. Direct.
**Technique digest needed.** No.

#### lem:lyapunov_drift (NEW — load-bearing)
**Statement.** On $\{L < L^*\}$, in the regime $\lambda_0 \alpha >
c \sigma^2 / d$, the process $L_t$ is a non-negative supermartingale
modulo a controllable error term.
**Hypotheses.** (SS), (HD), (BD), lem:drift_one_step.
**Downstream consumers.** thm:phase_transition (snowball branch).
**Technique.** Lyapunov drift analysis. **Digest needed:
`.proof-research/lyapunov-drift-supermartingale.md`** covering the
Foster-Lyapunov criterion and standard supermartingale-convergence
applications.

#### lem:concentration_one_step (NEW)
**Statement.** $\Pr[|L_t - L_{t-1} - \E[L_t - L_{t-1}]| > x \mid
\mathcal F_{t-1}] \le 2 \exp(-x^2 d / (2 \sigma^2))$ for $x \ge 0$.
**Hypotheses.** (HD).
**Downstream consumers.** lem:union_bound_excursions,
lem:hitting_time_lower.
**Technique.** Gaussian tail bound. Vershynin Prop 2.5.2.
**Technique digest needed.** Existing `cite-vershynin2018.md` suffices.

#### lem:union_bound_excursions (NEW)
**Statement.** For any horizon $T$, $\Pr[\max_{t \le T} |L_t - L_{t-1}|
> R \sqrt{\log T / d}] \le 1/T$ for some constant $R$ depending on
$\sigma$.
**Hypotheses.** lem:concentration_one_step.
**Downstream consumers.** thm:conditional_convergence (polynomial
horizon bound), thm:phase_transition (snowball branch — control
hard-region escapes).
**Technique.** Union bound over $T$ events.
**Technique digest needed.** No.

#### lem:hitting_time_lower (NEW — load-bearing for extinction branch)
**Statement.** In the regime $\lambda_0 \alpha < c' \sigma^2 / d$
(extinction), starting from $L_0 \in (0, L^*)$, $\Pr[\sup_t L_t > L^*
\text{ before reaching } 0] \ge 1 - \exp(-c'' (L^* - L_0)^2 / \sigma^2)$.
**Hypotheses.** (SS), (HD), lem:concentration_one_step.
**Downstream consumers.** thm:phase_transition (extinction branch).
**Technique.** Birth-death chain / random walk hitting time. **Digest
needed: `.proof-research/random-walk-hitting-times.md`** covering the
classical Doob martingale + optional-stopping argument for hitting
times of a drifted Gaussian random walk on an interval (Gambler's-ruin
type).

#### lem:drift_quantitative (NEW)
**Statement.** On the event $\{L_t \le L^*\}$, $\E[L_{t+1} - L_t \mid
\mathcal F_t, L_t \le L^*] \le -\lambda_0 \alpha / 2$ provided the
high-d term $\sigma^2 / d$ is at most $\lambda_0 \alpha / 2$.
**Hypotheses.** (SS), (BD), (HD), lem:drift_one_step.
**Downstream consumers.** thm:conditional_convergence.
**Technique.** Algebraic regrouping of lem:drift_one_step.
**Technique digest needed.** No.

#### lem:branching_extinction (NEW — backup for extinction branch)
**Statement.** Couple the "effective-token process" $(E_t)_{t \ge 0}$
to a sub-critical Galton-Watson branching process with offspring mean
$\lambda_0 / \lambda_c$. Extinction probability of the GW process upper-bounds
$\Pr[\text{snowball}]$ in the sub-critical regime.
**Hypotheses.** (SS).
**Downstream consumers.** thm:phase_transition (extinction branch,
alternative to lem:hitting_time_lower; choose whichever gives the cleaner
constant).
**Technique.** Galton-Watson coupling. **Digest needed:
`.proof-research/galton-watson-branching.md`** covering the
sub/critical/super-critical trichotomy from Athreya-Ney Chapter 1.

### 3.3 Lemma dependency graph (textual)

```
lem:softmax_running_average ─── (algebraic) ─────────────────────┐
                                                                 │
(SM), (BV)  ──► lem:loss_decomposition ─┐                        │
                                        │                        ▼
                                        ▼                  lem:loss_recursion (collapses
(SS), (HD), (BD)  ──► lem:drift_one_step ──┬─► lem:lyapunov_drift ──► T1 snowball
                                            │                            │
                                            └─► lem:drift_quantitative ──┴──► T2
(HD)  ──► lem:concentration_one_step ──┬─► lem:union_bound_excursions ──► T1/T2
                                       │
                                       └─► lem:hitting_time_lower ────► T1 extinction
                                                                          (or: lem:branching_extinction)
(SS) ──► lem:branching_extinction ──────────────────────────────────────► T1 extinction (alt.)

T1 ──► T3 (corollary)
```

Tree depth = 3 (assumptions → one-step lemmas → multi-step lemmas →
theorems). Width = 4-5 at the second level. Acceptable for an appendix
proof; comparable to v1's depth and width.

### 3.4 Technique digests required (Stage A2)

Three non-trivial techniques need digests before Phase C drafting:

1. **`.proof-research/lyapunov-drift-supermartingale.md`** —
   Foster-Lyapunov criterion (Meyn-Tweedie), Robbins-Siegmund
   convergence, supermartingale almost-sure convergence (Williams
   "Probability with Martingales" Ch. 11), explicit constants for the
   discrete-time case with bounded one-step variance.
2. **`.proof-research/random-walk-hitting-times.md`** — Doob optional
   stopping for hitting times of an interval, classical Gambler's-ruin
   in continuous space (drifted Gaussian random walk hitting $\{0, L^*\}$),
   explicit constants in the sub-critical-drift regime.
3. **`.proof-research/galton-watson-branching.md`** — Athreya-Ney
   sub/critical/super-critical trichotomy, extinction probability =
   smallest root of $f(s) = s$ for the offspring PGF, scaling of
   extinction probability near criticality.

Two existing digests will be re-used:

- `cite-vershynin2018.md` for high-dimensional concentration of measure
  (already on disk, suffices for lem:concentration_one_step).
- `cite-karimi2016pl.md` is *not* used in v2 (no PL condition assumed);
  flag for possible removal in cleanup but keep for now in case
  reviewers ask for the PL variant of T2.

### 3.5 v1 vs v2 contrast for this part

v1: 7 lemmas, depth 2, all linear chain ending at a single
expectation-bound theorem. v2: 9 lemmas (8 new + 1 salvaged), depth 3,
**branching** dependency graph ending at three theorems. The branching
structure is intrinsic to phase-transition results: above + below the
threshold are different mathematical arguments (Lyapunov vs.
hitting-time / branching). v1 had a single rate; v2 has a critical rate
with two qualitatively different behaviors on either side.

---

## Part 4 — Lit-survey supplement

The v1 lit-survey covered: CoT-as-GD analogies (e.g., Akyurek et al.
2023, von Oswald et al. 2023), scaling-by-aggregation (Snell et al.
2024), looped-latent (Geiping et al. 2025), and stochastic-process
viewpoints. v2 inherits these but adds the following six entries.

### 4.1 New citations needed

#### Frankle-Carbin 2019 — Lottery ticket hypothesis
**Citation key proposal.** `frankle2019lottery`.
**Key result.** Trained dense networks contain sparse subnetworks
("winning tickets") that, when trained in isolation from the original
initialization, match the dense network's accuracy. Implication: most
of a network's parameters are not actively contributing; effective
contribution is concentrated in a small subset.
**Relation to v2.** This is the most direct intellectual ancestor of
the "rare effective tokens" intuition. v2's $\lambda$ is the *temporal*
analogue of the lottery-ticket *spatial* sparsity claim — most reasoning
tokens contribute nothing; the rare effective ones determine the
trajectory.

#### Athreya-Ney textbook — Branching Processes
**Citation key proposal.** `athreya1972branching`.
**Key result.** Complete treatment of Galton-Watson, Markov branching,
and continuous-time branching processes. Theorem 1 of Chapter 1: a GW
process with offspring mean $m$ goes extinct a.s. iff $m \le 1$.
**Relation to v2.** Direct reference for lem:branching_extinction.
This is **the** classical text for the sub/critical/super-critical
trichotomy that underlies T1's phase transition. Athreya-Ney also
contains the explicit extinction-probability scaling near criticality
that gives the rate $\delta(d, Q, \lambda_0)$ in T1.

#### Vershynin 2018 (already cited) — relevant chapters
**Citation key.** `vershynin2018` (already in `cite-vershynin2018.md`).
**Specific chapters needed for v2.**
- Ch. 3 (random vectors in high dimensions): concentration of inner
  products; isotropy in high $d$. The fact $\E\langle u, v\rangle^2 = 1/d$
  for uniform $u, v$ on $S^{d-1}$ is in §3.2.
- Ch. 7 (matrix concentration): not needed for v2 main results.
- Ch. 8 (chaining): not needed.
**Relation to v2.** Required for (HD) and lem:concentration_one_step.
The existing digest covers the citation but the *specific chapter
references* for v2 differ from v1 (which used Vershynin for
sub-Gaussian concentration alone).

#### Mei-Nguyen-Misiakiewicz 2021 (or similar) — mean-field neural net analysis
**Citation key proposal.** `mei2018meanfield`.
**Key result.** Two-layer neural networks in the infinite-width / mean-field
limit have training dynamics governed by a McKean-Vlasov PDE. Implication:
in the wide-network limit, individual neuron contributions become
"random walks" around a population mean.
**Relation to v2.** Provides the theoretical *backing* for the (HD)
assumption: in wide networks, the per-step contribution of any
individual computation is well-approximated by a centered fluctuation
around the mean, with variance scaling inversely with width. This is
the intellectual bridge from v2's stylized 1d model to actual
transformer dynamics. Not load-bearing for any proof; cited in the
discussion to justify (HD).

#### NTK vs feature learning regimes — Yang & Hu 2021
**Citation key proposal.** `yang2021tp4`.
**Key result.** $\mu$P (maximal update parametrization) and the
distinction between lazy / kernel-like training (NTK) and rich /
feature-learning regimes. Implication: large models in the feature-learning
regime do *not* behave like fixed kernels; they actively learn
representations.
**Relation to v2.** Indirect: provides the high-$d$ scaling intuition
for why $\lambda_c \propto 1/d$ makes physical sense. In a feature-learning
regime, the effective dimension of the "useful" subspace grows with
$d$, so the random-walk component has more "room to be orthogonal"
in larger models. Cited in the discussion of T1 / T3 to argue the $1/d$
scaling is consistent with empirical scaling laws.

#### Chizat-Bach 2018 (lazy vs rich training) — for completeness
**Citation key proposal.** `chizat2018lazy`.
**Key result.** In sufficiently overparameterized models, gradient
descent on a non-convex loss behaves like linearized (NTK) training.
The "rich" regime requires escaping this linearization.
**Relation to v2.** Same as Yang & Hu — provides the high-$d$
intuition. Cite jointly with `yang2021tp4` in the discussion.

### 4.2 Additions to the bibliography in Stage A2

All six citations above need `.proof-research/cite-<key>-*.md`
digests written in Stage A2 before the corresponding LaTeX is drafted.
Priority order (load-bearing first):

1. `athreya1972branching` — load-bearing for lem:branching_extinction
   (and for the headline T1).
2. `frankle2019lottery` — load-bearing for the "rare effective tokens"
   framing in the introduction *of the relevant proof remarks* — note,
   per SKILL.md, this skill does not write the paper introduction, but
   it does write remarks inside lemma statements.
3. `mei2018meanfield`, `yang2021tp4`, `chizat2018lazy` — discussion-only,
   not load-bearing. Lower priority but still needed for citation hygiene
   (lint R13).
4. Vershynin chapter-specific addition — update the existing digest
   with the §3.2 reference.

### 4.3 v1 vs v2 contrast for this part

v1's lit-survey was framed around the "CoT-as-SGD" analogy and was
heavily skewed toward optimization references (Bottou et al. SGD review,
Karimi PL condition). v2 swings toward probability theory (branching
processes, random walks on intervals, high-d concentration) and is much
more eclectic across ML interpretability (lottery ticket) and theory
(mean-field, $\mu$P). The lit-survey supplement reflects the framework
shift from "convergence of biased SGD" to "phase transition of a random
walk + Poisson-like arrival process".

---

## Part 5 — Risk analysis specific to v2

Three primary risks plus two secondary. Probability, severity,
mitigation for each. Honest assessment includes "we'd rather know now
than after 1000 lines of LaTeX".

### R1 — Tractability: phase transition might not be provable in (a) without further stylization

**Description.** The 1d stylized model in Part 1 has a clean
drift–diffusion balance, but the actual derivation of the *sharpness*
of the transition (i.e., that the boundary at $\lambda_c$ is a true
discontinuity in the limit $d \to \infty$, not a smooth crossover)
requires careful control of the noise-fluctuation tail. The Lyapunov
argument (lem:lyapunov_drift) gives one half of T1 cleanly, but the
extinction branch (lem:hitting_time_lower or lem:branching_extinction)
needs hitting-time bounds that depend on the noise distribution
details. If we cannot get a *sharp* threshold (only a $\lambda_c$-window
of width $1/\sqrt{\log d}$ within which behavior is unclear), the
headline weakens from "sharp phase transition" to "phase transition with
$o(1)$ critical window", which is still publishable but less striking.

**Probability of firing.** Medium (35%). Sharp thresholds for
drift–diffusion balance are *typically* provable when the noise is
Gaussian and the drift is bounded, but constants are delicate.

**Severity.** Medium. Sharpness is the headline; a smooth-crossover
version still publishes but is no longer "the phase transition" paper.

**Mitigation.**
- **Primary.** Run the Stage A3 sanity check (Part 6) early. If
  simulation shows a smooth crossover empirically, we know to weaken the
  T1 statement to "polynomially-sharp" rather than "exponentially-sharp"
  before drafting.
- **Secondary.** If the proof breaks down at sharpness, fall back to a
  *qualitative* version of T1 ("exists $\lambda_c$ such that
  $\lambda_0 > 2\lambda_c \Rightarrow$ snowball w.h.p., $\lambda_0 < \lambda_c
  / 2 \Rightarrow$ extinction w.h.p.") with a slack factor of 2 (or
  $\log d$, etc.). This is a standard publishable form and avoids the
  delicate window analysis.
- **Tertiary.** If even the qualitative version is fragile, retreat to
  (c) Poisson point process: the CTMC limit is *cleaner* for sharpness
  analysis but requires the 20-page discretization detour. This is the
  worst-case fallback.

### R2 — High-d orthogonality formalization without uniform activations

**Description.** (HD) asserts a $1/d$ variance scaling for the random-walk
component projected onto $\nabla L$. The natural justification is "in
high d, random vectors are orthogonal". But this requires either: (i)
the random-walk component to be uniformly distributed on the sphere (or
isotropic Gaussian), which is empirically *false* for trained
transformers (their activations lie on a low-dimensional manifold), or
(ii) the *projection* onto $\nabla L$ specifically to have $1/d$
variance, which is a *direction-specific* claim that might fail if
$\nabla L$ happens to lie in the activation manifold's principal
direction.

**Probability of firing.** Medium-low (20%) for the proof itself
(the proof works under (HD) as stated, which is a *postulate*);
medium-high (50%) for the sellability to a reviewer who knows
representational geometry. A skeptical reviewer will ask: "what if the
gradient direction happens to be the dominant principal direction of
the residual stream?"

**Severity.** Medium. The proof goes through cleanly under (HD); the
risk is reviewer skepticism about (HD)'s empirical plausibility.

**Mitigation.**
- **Primary.** Frame (HD) carefully: it is a *postulate* about the
  *non-effective* component of $g_t$, defined as $g_t - \E[g_t \mid
  \mathcal F_{t-1}, E_t = 1]$. Effective tokens are *allowed* to be
  in the $\nabla L$ direction (that's the point of $\lambda$); the
  postulate is only about what's left over after subtracting the
  effective component.
- **Secondary.** Add a 1-paragraph empirical-check protocol in the
  discussion: probe a trained transformer on held-out trajectories,
  compute the projection variance of the non-effective component onto
  $\nabla L$, report whether it scales as $1/d$ across model sizes.
  This is a falsifiable prediction — and it's exactly the kind of
  thing the Stage A3 sanity-check protocol (Part 6) should include.
- **Tertiary.** Weaken (HD) to a *projection variance ratio* of $1/d$
  vs. the largest principal direction. This costs some constants but
  preserves the qualitative $1/d$ scaling of T1.

### R3 — Numerical sanity check might not exhibit sharp phase transition

**Description.** The Stage A3 simulator (Part 6) sweeps
$(\lambda_0, d, \alpha, \sigma)$ and checks for a sharp boundary
between snowball and extinction regimes. If the boundary turns out
smooth (e.g., probability of snowball vs. $\lambda_0$ is a logistic
curve with width $\Omega(1)$ regardless of $d$), then the v2 framework's
substantive prediction is *empirically wrong on its own stylized model*,
which is fatal.

**Probability of firing.** Low-medium (15%) for the 1d stylized
model exactly as specified in Part 1 (the math is fairly standard
drift–diffusion). Medium (30%) if we additionally check that the
simulation reproduces the predicted $\lambda_c \propto 1/d$ scaling
(i.e., if it's a fixed $\lambda_c$ independent of $d$, the headline
prediction is wrong).

**Severity.** High. If the sanity check fires, v2 has the same fate
as v1: we know the math will be intractable / vacuous before
writing the LaTeX.

**Mitigation.**
- **Primary.** Run the Stage A3 sanity check **before** Phase C
  drafting. The 1d simulator should be cheap (under 30 s of compute).
  If it doesn't reproduce a sharp transition or $1/d$ scaling, *stop*
  and revisit decomposition choice (Part 1) before writing any proof.
- **Secondary.** If sanity check passes for the 1d model but fails for
  a slightly more realistic surrogate (e.g., a small actual
  transformer), this is still publishable as "phase transition is a
  property of the stylized model" with explicit acknowledgement.
- **Tertiary fallback if sanity fails entirely.** Retreat to a much
  weaker T1: "**existence** of a critical region", with no claim
  about sharpness or $1/d$ scaling. The "$\mathcal D(Q)$ is well-defined"
  framing of T3 can survive even a smooth-crossover T1.

### R4 (secondary) — Constant-tracking explosion

**Description.** The 1d stylized model has at least 5 constants
$(\alpha, \sigma, d, L^*, \lambda_0)$ entering every bound. With the
universal-constants convention required by lint R15, the LaTeX
risks becoming an "alphabet soup" of subscripts.

**Probability.** High (80%) that constant tracking gets messy.
**Severity.** Low. Annoying but not fatal.
**Mitigation.** Establish a constant-naming convention in Phase B
(e.g., $c_{\mathrm{lyap}}, c_{\mathrm{hit}}, c_{\mathrm{drift}}, \ldots$)
and stick to it. Use the universal-constant macro liberally.

### R5 (secondary) — Salvaged lemma 03 might not apply
**Description.** `sections/03-lemma-softmax-running-average.tex`
is the salvaged v1 lemma. v2 reformulates around $L_t \in \R$ rather
than $x_t \in \R^d$, so the running-average lemma might not directly
plug into the new proof.

**Probability.** Low (10%). The lemma's content is *purely
algebraic* about the softmax recurrence and makes no reference to the
assumption set (v1 or v2). It will be invoked in lem:loss_decomposition
to connect $L_t = L(x_t)$ to the softmax-recurrence form.
**Severity.** Very low.
**Mitigation.** None needed; verified during reconnaissance (read on
2026-05-25; algebra is decomposition-agnostic).

### 5.6 v1 vs v2 contrast for this part

v1 had 5 risks; the binding one (R2, bias floor) was diagnosed
quantitatively by `risk-2-sanity-check.md` as YELLOW with structural
caveat — the v1 framework would have published but in a vacuous
regime. v2's risks are *different in kind*: R1 (tractability) and R3
(sanity check) are mathematical risks that admit a 30-minute fix
(stylize harder); R2 (HD postulate) is a *framing* risk. The v2 risk
profile is therefore much more "honest" — we know upfront where to
push back.

---

## Part 6 — Recommended Stage A3 sanity check protocol

The simulator below is the v2 analogue of `risk-2-sanity-check.py`. It
runs in parallel with this reconnaissance and feeds Phase B / C
drafting.

### 6.1 Simulator architecture

**Language.** Python, NumPy only (no PyTorch), to mirror v1's sanity
check.

**Module.** `/tmp/v2-sanity-check.py` writing to `/tmp/v2-sanity.json`.

**Core loop.** Discrete-time simulation of Part 1's 1d stylized model:

```python
def simulate(d, lambda_0, lambda_func, alpha, sigma, L_star, L_0,
             T_max, n_runs, seed):
    rng = np.random.default_rng(seed)
    outcomes = []
    for run in range(n_runs):
        L = L_0
        trajectory = [L]
        for t in range(T_max):
            lam = lambda_func(L, lambda_0, L_star)  # state-dependent rate
            E = rng.binomial(1, lam)
            xi = rng.standard_normal()
            L = L - E * alpha + (sigma / np.sqrt(d)) * xi
            L = max(L, 0.0)  # reflecting at 0
            trajectory.append(L)
            if L <= np.log(2):
                outcomes.append(('snowball', t, trajectory))
                break
            if L >= 2 * L_star:
                outcomes.append(('extinction', t, trajectory))
                break
        else:
            outcomes.append(('timeout', T_max, trajectory))
    return outcomes
```

**State-dependent rate function.** Default to the step function
$\lambda(L) = \lambda_0 \mathbb 1[L < L^*]$ (matches (SS) cleanly). Also
test smooth variants:
```python
def lambda_smooth_sigmoid(L, lambda_0, L_star):
    return lambda_0 / (1 + np.exp(5 * (L - L_star)))
def lambda_smooth_linear(L, lambda_0, L_star):
    return lambda_0 * max(0, 1 - L / L_star)
```

### 6.2 Parameter sweep design

**Core sweep.** Vary $d \in \{16, 64, 256, 1024\}$ (factor-of-4 steps
across 2 orders of magnitude). For each $d$:
- Fix $\alpha = 0.1, \sigma = 1, L^* = 5, L_0 = 2.5$ (midpoint of
  snowball region).
- Sweep $\lambda_0 \in \{0.001, 0.003, 0.01, 0.03, 0.1, 0.3\}$
  (6 values, log-spaced over 2.5 orders of magnitude).
- Predicted $\lambda_c = c \cdot \sigma^2 / (\alpha d) = c \cdot 10/d$
  for $c = O(1)$. So predicted $\lambda_c$ values across $d$:
  $\lambda_c(16) \approx 0.6, \lambda_c(64) \approx 0.16,
  \lambda_c(256) \approx 0.04, \lambda_c(1024) \approx 0.01$.
- $n_{\mathrm{runs}} = 1000$ per $(d, \lambda_0)$ cell.
- $T_{\mathrm{max}} = 10000$.

**Secondary sweep.** For the best-fit $\lambda_c(d)$ from the core sweep,
fit a power law $\lambda_c(d) = A \cdot d^{-\gamma}$ and report $\gamma$
with 95% bootstrap CI. Predicted $\gamma = 1$.

**Sensitivity sweep.** Vary $\alpha \in \{0.05, 0.1, 0.2\}$ and
$\sigma \in \{0.5, 1, 2\}$ holding $d = 256$ fixed; verify $\lambda_c$
scales as $\sigma^2 / \alpha$ (slope $+2$ in $\sigma$, slope $-1$ in
$\alpha$ when plotted log-log).

**Robustness sweep.** Repeat core sweep with smooth-sigmoid and
smooth-linear $\lambda$ functions; verify the transition still appears
(maybe rounded) and the inferred $\lambda_c(d)$ scaling is unchanged.

### 6.3 Acceptance criteria

**GREEN (v2 framework validated):**
- For each $d$, the success probability $\Pr[\text{snowball}]$ as a
  function of $\lambda_0$ is sigmoidal (S-curve) with midpoint
  $\hat\lambda_c(d)$ and width $W(d)$.
- $\hat\lambda_c(d)$ scales as $\hat\lambda_c(d) \propto d^{-\gamma}$
  with $\gamma \in [0.7, 1.3]$ (i.e., consistent with the predicted
  $1/d$ scaling).
- The transition width $W(d)$ shrinks with $d$ (consistent with
  "sharper at higher dimension").

**YELLOW (qualitative framework OK, but headline weakens):**
- S-curves exist but widths don't shrink with $d$ (transition is
  smooth at all dimensions).
- Or: $\hat\lambda_c(d)$ scales but with $\gamma \in [0.3, 0.7]$ or
  $[1.3, 2]$ (substantially off the $1/d$ prediction).
- Action: weaken T1 to qualitative form (existence + monotonicity in
  $d$ only); drop the specific $\lambda_c \propto \sigma^2/(\alpha d)$
  formula in favor of "$\lambda_c(d, Q)$ exists and is decreasing in
  $d$".

**RED (v2 framework falsified on its own stylized model):**
- No transition observed: $\Pr[\text{snowball}]$ is monotonically
  varying with $\lambda_0$ but with no clear inflection, across all $d$.
- Or: $\hat\lambda_c$ is roughly *constant* in $d$ (no scaling).
- Action: stop. Re-evaluate decomposition. Likely the (HD) assumption
  needs strengthening or the noise model needs revision.

### 6.4 Failure-fallback protocol

If RED at any stage:
1. **First fallback (5 min):** check the simulator for off-by-one in
   the $\sqrt d$ factor; re-run.
2. **Second fallback (1 hour):** try decomposition (c) Poisson
   continuous-time limit explicitly. Use `scipy.integrate` to numerically
   solve the SDE
   $$dL_t = -\lambda(L_t) \alpha dt + (\sigma/\sqrt d) dW_t.$$
   This is the continuous-time analogue of Part 1's discrete model and
   should exhibit a *sharper* transition than discrete time.
3. **Third fallback (project-level decision):** if continuous-time
   also fails, the framework needs structural revision. Surface to user
   with simulation evidence; do not proceed to Phase C drafting.

### 6.5 Estimated runtime

Core sweep: 4 $d$ values $\times$ 6 $\lambda_0$ values $\times$ 1000 runs
$\times$ 10000 steps = $2.4 \times 10^8$ steps. At ~$10^7$ steps/s in
NumPy (each step is one rng + one float op), runtime ~24 s. Sensitivity
+ robustness sweeps: another ~30 s. Total ~1-2 minutes.

This is *cheaper* than the v1 sanity check (which was ~19 s) per data
point but covers a larger grid.

### 6.6 Output deliverable

A markdown file `.proof-research/v2-sanity-check.md` with the same
structure as `risk-2-sanity-check.md`: tables of $\hat\lambda_c(d)$ vs.
prediction, log-log plot text descriptions, GREEN/YELLOW/RED verdict
per Acceptance Criteria above.

### 6.7 v1 vs v2 contrast for this part

v1's sanity check focused on *measuring* the assumption's
preconditions ($\hat\eta_j, \hat\beta$ across real-ish models). v2's
sanity check focuses on *verifying the predicted phase transition in
the stylized model itself*. Both are necessary; v1's check is the
"does our assumption hold on real data?" check, and v2's check is the
"does our theorem describe its own model correctly?" check. v2 inherits
the v1 question (does (SS) hold on real models?) as a
discussion-section empirical-check protocol; the proof-side sanity
check is the new one.

---

## Part 7 — Self-recommendation

### Single sharpest claim to commit to

**Recommended headline.** The conjunction T1 (sharp phase transition
at $\lambda_c \sim \sigma^2/(\alpha d)$) + T3 (corollary defining
$\mathcal D(Q)$). Stated as a single theorem in the paper if that reads
better; structurally they should be presented as headline + corollary.

**Headline statement (informal, for the abstract).**

> Under the stylized 1d random-walk model of reasoning-token
> dynamics, there exists a critical effective-token rate
> $\lambda_c(d, Q) \sim \sigma^2/(\alpha d)$ such that above
> $\lambda_c$, the chain-of-thought converges to a correct-answer
> region with probability $1 - o_d(1)$, and below $\lambda_c$, the
> chain-of-thought drifts away from any correct-answer region with
> probability $1 - o_d(1)$. Consequently, every question $Q$
> admits a minimum reasoning dimension
> $\mathcal D(Q) := \inf\{d : \lambda_c(d, Q) < \lambda_0(Q)\}$
> below which no chain-of-thought of any length succeeds.

### Justification (2-3 sentences)

This is the right primary result because (a) the $1/d$ scaling is a
*novel*, *sharp*, *substantive*, and *empirically falsifiable*
prediction that no prior theory in the reasoning-as-optimization
literature makes — it directly explains why reasoning scales with model
size in a way that v1's biased-SGD framing fundamentally could not;
(b) the minimum-reasoning-dimension corollary $\mathcal D(Q)$
operationalizes "problem difficulty" as a *measurable quantity tied to
model architecture*, which is exactly the kind of bridge between
algorithm and practice that reasoning-theory papers are missing; (c)
the proof technique (drift-diffusion balance + branching coupling) is
classical and well-understood — meaning the load-bearing risk is
*framing* (does our model describe real LLMs?), not *mathematics*
(can we prove what we claim?). T2 (polynomial convergence given
snowball) is supportive but not the headline; the phase-transition is
what changes the conversation about reasoning theory.

### Risk reminder for the headline

Per Part 5 R1 + R3, the sharpness and $1/d$ scaling components of this
headline are the highest-risk parts of v2. The Stage A3 sanity check
(Part 6) **must** pass before this headline goes to LaTeX. If the
sanity check only achieves YELLOW (qualitative transition without
sharp $1/d$ scaling), the recommendation downgrades to "qualitative T1
+ T3, with the $\sigma^2/(\alpha d)$ formula relegated to a remark".

---

## Appendix A: Inventory of artifacts and status

### What survives Stage 0 reset, into v2

- `sections/03-lemma-softmax-running-average.tex` — applies unchanged
  (verified in Part 3, lem:softmax_running_average).
- `cite-*.md` digests: `openai2024o1`, `deepseek2025r1`,
  `qwen2025thinking`, `wei2022cot`, `vaswani2017attention`,
  `choi2025entropy`, `freedman1975tail`, `vershynin2018`,
  `bottou2018optimization`, `karimi2016pl`.
  - Used in v2: all except `bottou2018optimization` (which was v1-specific)
    and possibly `karimi2016pl` (only if PL variant of T2 is added).
- `scope.md` — Appendix scope still applies (≥ 3 lemmas, paper-level
  proof, > 30 steps).
- v1 Phase A proposal + v1 sanity check — kept for compare/contrast.

### What needs to be created in Stage A2 (next stage)

- `.proof-research/lyapunov-drift-supermartingale.md`
- `.proof-research/random-walk-hitting-times.md`
- `.proof-research/galton-watson-branching.md`
- `.proof-research/cite-frankle2019lottery.md`
- `.proof-research/cite-athreya1972branching.md`
- `.proof-research/cite-mei2018meanfield.md`
- `.proof-research/cite-yang2021tp4.md`
- `.proof-research/cite-chizat2018lazy.md`
- Update to `cite-vershynin2018.md` (add Ch. 3 §3.2 reference).

### What is created in Stage A3 (sanity check, parallel)

- `/tmp/v2-sanity-check.py`
- `/tmp/v2-sanity.json`
- `.proof-research/v2-sanity-check.md`

### What gets written in Phase C (later)

- `sections/01-preliminaries.tex` — definitions of $L_t$, the formalization
  in Part 1.
- `sections/02-assumptions.tex` — (SS), (SM), (BD), (HD), (BV) with
  remarks.
- `sections/03-lemma-softmax-running-average.tex` — already exists.
- `sections/04-loss-decomposition.tex` — lem:loss_decomposition.
- `sections/05-drift-and-concentration.tex` — lem:drift_one_step,
  lem:concentration_one_step.
- `sections/06-lyapunov-and-hitting.tex` — lem:lyapunov_drift,
  lem:hitting_time_lower, lem:branching_extinction,
  lem:union_bound_excursions, lem:drift_quantitative.
- `sections/07-thm-phase-transition.tex` — T1.
- `sections/08-thm-conditional-convergence.tex` — T2.
- `sections/09-thm-problem-difficulty.tex` — T3.
- `sections/10-discussion.tex` — empirical-check protocol for (HD) and
  (SS), connection to lottery ticket / mean-field, future work.

### Estimated effort

- Stage A2 (this reconnaissance + Stage A1 commit + technique/citation
  digests): 1-2 days of dedicated time.
- Stage A3 (sanity check Python + report): 1 day in parallel.
- Phase B-D (LaTeX drafting + review): 5-7 days.

This is *longer* than v1's estimated 4-6 days because v2's tree depth
is 3 vs. v1's 2, and the branching dependency graph introduces more
proof boundaries. But v2 should *not* have v1's "we know the framework
will be intractable / vacuous before writing" problem if the Stage A3
sanity check passes — so the LaTeX work is more likely to be
productive end-to-end.
