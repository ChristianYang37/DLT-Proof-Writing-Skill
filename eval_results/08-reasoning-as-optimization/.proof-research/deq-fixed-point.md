# Technique digest — Banach fixed-point / DEQ contraction (Bai et al. 2019)

**Purpose.** Provide a contraction-mapping argument for Round-3
Theorem **T6** (`thm:T6_contraction` in
`sections/11-contraction-fixed-point.tex`). T6 states that on a
deterministic subset $\mathcal B$ of the snowball region, the attention
recurrence map $f$ admits a contraction property in a suitable weighted
norm; consequently, by Banach's fixed-point theorem, the trajectory
$(x_t)$ converges to a unique fixed point $x_\infty \in \mathcal B$ with
exponential rate.

## Picked result — Banach fixed-point theorem

**Reference.** Banach 1922 (folklore in any functional-analysis
textbook). Statement (paraphrased to our setting):

**Theorem (Banach).** Let $(\mathcal B, d)$ be a non-empty complete
metric space and $f : \mathcal B \to \mathcal B$ a *strict
contraction*, i.e., there exists $\beta \in [0, 1)$ such that
$$d(f(x), f(y)) \;\le\; \beta \cdot d(x, y) \qquad \forall x, y \in \mathcal B.$$
Then $f$ has a unique fixed point $x_\infty \in \mathcal B$, and for
any starting point $x_0 \in \mathcal B$ the iterates
$x_t = f(x_{t-1})$ converge geometrically:
$$d(x_t, x_\infty) \;\le\; \beta^t \cdot d(x_0, x_\infty).$$

## The hard problem: $f$ is not memoryless

**This is the load-bearing issue.** Our attention recurrence in
\Cref{lem:softmax_running_average} is
$$x_j \;=\; \frac{s_{j-1}}{s_j}\, x_{j-1} \;+\; \frac{e^{\inner{q}{k_j}}}{s_j}\, V_j,
   \qquad s_j = \sum_{i \le j} e^{\inner{q}{k_i}}.$$
The coefficient $s_{j-1}/s_j$ depends on the *cumulative score*
$s_j$, which depends on the **entire history** $(k_1, \ldots, k_j)$
of keys, *not* just on $x_{j-1}$. In particular:
- $w_{j, j} = e^{\inner{q}{k_j}}/s_j$ depends on $s_j$, which depends
  on $j$ and the full key history.
- The map $x_{j-1} \mapsto x_j$ is *not* a fixed function
  $f: \R^d \to \R^d$; it is a time-varying map
  $f_j : \R^d \times (\text{history}) \to \R^d$.

**Three resolutions** (decreasing-strictness):

### (R1) Extend the state to include sufficient statistics

Define the augmented state $z_t \coloneqq (x_t, s_t)$ on
$\R^d \times \R_{> 0}$. The recurrence becomes
$$z_t \;=\; F(z_{t-1}, V_t, k_t)
   \;=\; \biggl(\frac{s_{t-1}}{s_{t-1} + e^{\inner{q}{k_t}}}\, x_{t-1}
                + \frac{e^{\inner{q}{k_t}}}{s_{t-1} + e^{\inner{q}{k_t}}}\, V_t,\;
                s_{t-1} + e^{\inner{q}{k_t}}\biggr).$$
This is still *not* a fixed map $F : \R^d \times \R_{>0} \to
\R^d \times \R_{>0}$ because $(V_t, k_t)$ are exogenous inputs that
vary in $t$. Banach's theorem **cannot apply** to a recurrence with
time-varying exogenous inputs unless those inputs themselves stabilise.

### (R2) Steady-state assumption (effective tokens drive $V_t$)

In the *snowball region*, the effective-token mechanism gives
$V_t = -\nabla\loss(x_{t-1})/\norm{\nabla\loss(x_{t-1})}_2$ on
$\{\xi_t = +1\}$. Conditional on $\{\xi_t = +1\}$, $V_t$ becomes a
*function of $x_{t-1}$* via the gradient $\nabla\loss(\cdot)$. The
keys $k_t$ are determined architecturally by $x_t$ as well in a
self-attention transformer (where $k_t = W_K x_t$). With these
identifications, the recurrence *becomes memoryless on
$\{\xi_t = +1\}$*: there exists $f : \R^d \to \R^d$ such that
$x_t = f(x_{t-1})$ on the all-positive-effective event.

This is the **right formulation for T6**: conditional on the
all-positive-effective event (a subset of the snowball region), the
recurrence is a memoryless map $f$, and Banach applies if $f$ is a
contraction.

### (R3) Restrict to a single-effective-token-per-window analysis

A weaker formulation: T6 covers the *coarse-grained* recurrence where
each "time step" is one window of $\Delta$ reasoning tokens, of which
one is effective ($\xi_t = +1$). The effective token's value vector
is a function of $x_{t-1}$; the other $\Delta - 1$ noise tokens
average out. This is more rigorous (it embeds the snowball-region
restriction into the time-step definition itself) but requires defining
$f$ as the $\Delta$-step composition of one-effective-plus-noise.
Not recommended for T6's clean statement.

**Recommendation for T6: use (R2).** State T6 with the explicit
hypothesis "conditional on all-positive-effective event $\Ecal_+ =
\{\xi_t = +1 \,\forall t\}$, $f$ is a contraction." Then **on
$\Ecal_+$**, Banach applies, and the trajectory converges to $x_\infty$.

## Contraction subset $\mathcal B$ and Jacobian computation

The "contraction subset" $\mathcal B$ of the snowball region is the
set on which $\norm{\nabla_x f(x)}_{\mathrm{op}} \le \beta < 1$
deterministically. Compute the Jacobian:

**Setup.** On $\Ecal_+$, the recurrence simplifies (using
$w_{t} \coloneqq w_{t, t} = e^{\inner{q}{k_t}}/s_t$ for the
current-step weight):
$$x_t \;=\; (1 - w_t)\, x_{t-1} \;+\; w_t \cdot V_t,
   \quad V_t \;=\; -\frac{\nabla\loss(x_{t-1})}{\norm{\nabla\loss(x_{t-1})}_2}.$$
Here $w_t$ depends on $\inner{q}{k_t} = \inner{W_Q x_{t-1}}{W_K x_{t-1}}/\sqrt{d_k}$
and $s_t$ (which depends on past keys, fixed at the current
linearization point).

**Jacobian at fixed point $x_\infty$:** at a fixed point,
$\nabla\loss(x_\infty) = 0$ would give $V_t = 0$ (degenerate), so
the *natural* fixed point of T6 is **not** the bottom-of-basin
critical point — it is the (approximate) point where the attention
recurrence's *softmax-average* of past values equals the negative
gradient direction. Let $x^\star = x_\infty$ denote this fixed point.

By the chain rule, $\nabla_x f(x) = (1 - w(x)) \cdot I + (\text{terms in }
\nabla w, \nabla V)$. In the steady-state $\Ecal_+$ regime:
- The *direct* term $\nabla_x[(1 - w) x] = (1 - w(x)) I + (\text{small}
  \,\text{from}\,\nabla w \cdot x)$ has operator norm $\le 1 - w_\min
  + O(\nabla w)$.
- The *value-vector* term $\nabla_x[w \cdot V]$ involves
  $\nabla_x V = -\nabla_x[\nabla\loss/\norm{\nabla\loss}]$, which by
  the L-smoothness of $\loss$ (\Cref{fac:loss_smoothness}) is
  bounded in operator norm by
  $\norm{\nabla^2\loss}_{\mathrm{op}}/\norm{\nabla\loss} +
  \norm{\nabla\loss}^{-3} \cdot \norm{\nabla^2\loss \cdot \nabla\loss}
  \le 2 L_{\mathrm{sm}}/\norm{\nabla\loss}$ (rough bound from
  Hessian smoothness divided by gradient magnitude).
  Multiplied by $w$:
  $\norm{w \cdot \nabla_x V}_{\mathrm{op}} \le 2 w L_{\mathrm{sm}}/\norm{\nabla\loss}$.

**Contraction inequality:** combining,
$$\norm{\nabla_x f(x)}_{\mathrm{op}}
   \;\le\; (1 - w_\min) + 2 w_{\max} L_{\mathrm{sm}}/\norm{\nabla\loss(x)}.$$
For contraction $\beta < 1$, we need
$$2 w_{\max} L_{\mathrm{sm}}/\norm{\nabla\loss(x)} \;<\; w_\min,
   \quad\text{i.e.,}\quad
   \norm{\nabla\loss(x)} \;>\; \frac{2 w_{\max} L_{\mathrm{sm}}}{w_\min}.$$

Using \Cref{lem:max_attention_weight}, $w_{\max} \le e^{2S}/T$ and
$w_\min$ is comparable (running-average weights are concentrated when
scores are bounded), so $w_{\max}/w_\min \le e^{4S}$ deterministically.
Hence the contraction subset is
$$\mathcal B \;\coloneqq\; \bigl\{x \in \R^d :
   \norm{\nabla\loss(x; Q)}_2 \;>\; 2 e^{4S} L_{\mathrm{sm}}\bigr\}.$$

## Critical question: is $\mathcal B$ non-empty in the snowball region?

The snowball region $\{\loss(x; Q) < \Lstar(Q)\}$ is by assumption
the region where the effective-token rate is $\ge \rateinitp$. The
question is: does $\norm{\nabla\loss(x)}_2 > 2 e^{4S} L_{\mathrm{sm}}$
hold in this region?

**Lower bound on $\norm{\nabla\loss}$ in snowball.** Recall
$\nabla\loss = W_U^\top(p - \qcond)$. Near the boundary
$\loss = \Lstar$, $\cmass = e^{-\Lstar}$, and the
$\qcond$-mass (a normalized supported-on-$\Aset$ distribution) is far
from the actual softmax distribution $p$ (since the actual mass on
$\Aset$ is only $e^{-\Lstar}$, away from the target). Hence
$\norm{p - \qcond}_1 \ge 1 - e^{-\Lstar}$, so by Cauchy-Schwarz +
the row-norm lower bound (\Cref{ass:incoherent_unembedding}):
$$\norm{\nabla\loss}_2 \;\ge\; \rho_0 \cdot \norm{p - \qcond}_2 /
   \sqrt{|\Vocab|^n}
   \;\ge\; \rho_0 \cdot (1 - e^{-\Lstar})/(|\Vocab|^n)^{1/2}.$$
This lower bound is **dimension-suppressed** by $\sqrt{|\Vocab|^n}$,
which makes the contraction condition
$\norm{\nabla\loss} > 2 e^{4S} L_{\mathrm{sm}}$ **demanding** when
$|\Vocab|^n$ is large.

**Diagnosis.** The crude contraction subset $\mathcal B$ derived above
is **likely empty** for realistic $|\Vocab|^n \sim 10^4$–$10^6$ and
$L_{\mathrm{sm}} \sim \norm{W_U}_{\mathrm{op}}^2/2 \sim R_U^2 \cdot
|\Vocab|^n/d$ (by random-matrix theory of the spectral norm).
**Resolution:** the contraction must be in a *weighted* norm that
exploits the high-d orthogonality, *not* the Euclidean operator norm.
Specifically:

**Weighted-norm contraction.** Define the weighted norm
$\norm{v}_\Pi \coloneqq \norm{\Pi v}_2$ where $\Pi$ projects onto
$\mathrm{span}\{W_U^a : a \in \Aset\}$ (the row span of correct
rows). On this subspace, the relevant Jacobian
$\Pi \nabla_x f(x) \Pi$ has:
- $\Pi (1 - w(x)) I \Pi = (1 - w(x)) \Pi$ (same as Euclidean).
- $\Pi (w \cdot \nabla_x V) \Pi$ benefits from the
  effective-step alignment: by \Cref{ass:effective_step_alignment},
  $V$ lies in $\mathrm{span}\{W_U^a\}$, so $\Pi V = V$, and the
  derivative $\Pi \nabla_x V$ is bounded by the *restricted*
  Hessian of $\loss$ on the correct-row span, which is much smaller
  ($\approx L_{\mathrm{sm}} \cdot |\Aset|/|\Vocab|^n$ rather than
  $L_{\mathrm{sm}}$ on the full $\R^d$).

**Refined contraction subset:**
$$\mathcal B_{\Pi} \;\coloneqq\; \bigl\{x \in \R^d :
   \norm{\Pi \nabla\loss(x; Q)}_2 \;>\; 2 e^{4S} L_{\mathrm{sm}} \cdot \tfrac{|\Aset|}{|\Vocab|^n}\bigr\}.$$
This is non-empty in the snowball region because (i) the $\Pi$
projection of $\nabla\loss$ is exactly the load-bearing gradient
direction in Lemma~B; (ii) the effective Hessian on $\Pi$-subspace
is $|\Aset|/|\Vocab|^n$-suppressed.

## Hypothesis: contraction holds locally at $x_\infty$ only

Even with the weighted-norm refinement, the contraction
$\norm{\nabla_x f}_{\mathrm{op}, \Pi} < 1$ likely holds only in a
*neighborhood* of the fixed point $x_\infty$, **not uniformly** on
$\mathcal B_{\Pi}$. This degrades T6's conclusion from "global
contraction → unique fixed point in $\mathcal B$" to "local
contraction → local exponential stability of $x_\infty$ in a
neighborhood."

**Recommendation for T6 statement.** Two viable forms:

1. **Strong form (Banach):** Conditional on $\Ecal_+$ on the
   contraction subset $\mathcal B_\Pi$, $f$ is a strict contraction
   in the $\Pi$-weighted norm, and the trajectory converges to the
   unique fixed point $x_\infty$ at rate $\beta^t$.

2. **Weak form (local stability):** $x_\infty$ is an exponentially
   stable fixed point of $f$ in the $\Pi$-weighted norm: there exists
   a neighborhood $U \subset \mathcal B_\Pi$ such that
   $\norm{x_t - x_\infty}_\Pi \le \beta^t \norm{x_0 - x_\infty}_\Pi$
   for $x_0 \in U$.

**Recommendation: state both forms but only prove the weak form.**
The strong form requires global verification of the contraction
inequality on all of $\mathcal B_\Pi$, which depends on uncontrolled
geometry (e.g., near-singularities of $\nabla\loss/\norm{\nabla\loss}$
when $\nabla\loss$ approaches zero). The weak form is rigorous and
delivers the "deterministic-trajectory contraction" claim of Round 3
without overclaiming.

## Citation

**Yes, a `\cite{}` is recommended** — citing Bai et al. 2019 (Deep
Equilibrium Models, DEQ) for the architectural-precedent argument
that attention recurrences admit fixed-point analyses. Even though
our T6 only uses Banach (which is folklore), the DEQ citation
contextualises the result for the deep-learning audience and signals
that the attention-recurrence-as-fixed-point view is well-established.

**Proposed `refs.bib` entry:**
```bibtex
@inproceedings{bai2019deq,
  author    = {Shaojie Bai and J. Zico Kolter and Vladlen Koltun},
  title     = {Deep Equilibrium Models},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2019},
  volume    = {32},
  eprint    = {1909.01377},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  url       = {https://arxiv.org/abs/1909.01377}
}
```

**Sibling citation digest** at
`.proof-research/cite-bai2019deq.md` to be created by the writer
agent (Phase B), with content:
- DEQ formulation: an equilibrium model is a single layer iterated to
  convergence, with the forward pass solving $z = f_\theta(z, x)$ for
  $z$ via a fixed-point solver (e.g., Anderson acceleration,
  Broyden).
- Stability: DEQs are stable when the Jacobian
  $\norm{\partial f/\partial z}_{\mathrm{op}} < 1$ at the fixed point.
  This is the *operational version* of the Banach hypothesis we use.
- Connection to our setting: the attention recurrence in
  \Cref{def:softmax_attention} is the DEQ-style infinite-iteration
  limit of self-attention; T6 establishes when it admits a stable
  fixed-point analysis.

Banach 1922 itself does not need a citation — it is folklore in any
analysis textbook; T6's statement-and-proof body can simply name
"Banach's fixed-point theorem" without bibitem.

## What T6 delivers (relative to T1, T4, T5)

- **T1**: probabilistic snowball/extinction with explicit failure
  budgets.
- **T4**: Gaussian-CDF in the critical fragility window.
- **T5**: deterministic ODE limit $\dot m = h(m)$ in
  $d \to \infty$.
- **T6**: deterministic *exponential-contraction* statement on a
  subset of the snowball region: on $\mathcal B_\Pi$ (or in a
  neighborhood of $x_\infty$), the discrete attention recurrence
  is contractive in the $\Pi$-weighted norm, and the trajectory
  converges to the unique fixed point at geometric rate $\beta^t$.
  This is the **finite-$d$ deterministic** companion of T5: T5
  gives the $d \to \infty$ ODE limit, T6 gives the finite-$d$
  contraction in the snowball region.

## Caveats / load-bearing assumptions

1. **$f$ memoryless on $\Ecal_+$.** Requires conditioning on the
   all-positive-effective event (or restricting to a subsequence of
   $\xi_t = +1$ steps). On the unconditional trajectory, $f$ is
   time-varying via $s_t$ and the recurrence is not directly a
   Banach iteration. **The clean T6 statement is conditional on
   $\Ecal_+$, with $\Pr[\Ecal_+] \ge \rateinitp^{T_{\max}}$ — an
   exponentially-small high-probability event in the snowball
   region.** This is severe: T6's conclusion is **conditional on an
   exponentially-small event** (rate $\rateinitp^{T_{\max}}$).
   Reformulating as a "in-expectation" or "with probability
   $\rateinitp^{T_{\max}}$" statement is the only viable rigorous
   path.

2. **Weighted-norm contraction.** Required because Euclidean
   contraction subset is empty. Cleanest formulation: contract in the
   $\Pi$-weighted norm with $\Pi$ = projection onto
   $\mathrm{span}\{W_U^a : a \in \Aset\}$.

3. **Local vs global.** Strong "global on $\mathcal B$" form requires
   uniform contraction; weak "local at $x_\infty$" form requires only
   pointwise Jacobian. Recommend stating the weak form rigorously
   and the strong form as a corollary under stronger hypotheses (e.g.,
   convexity of $\loss$ on $\mathcal B_\Pi$).

4. **Existence of $x_\infty$.** The fixed-point existence is given by
   Banach in the weak form. The fixed point may *not* satisfy
   $\nabla\loss(x_\infty) = 0$: it is the equilibrium of the
   attention recurrence (the fixed point of $f$), not of gradient
   flow. The relationship is $x_\infty$ = limit of softmax-running
   average where the running average of past effective directions
   balances. **Need a separate one-line argument identifying
   $x_\infty$ with the predicted snowball-region attractor.**

5. **Relation to T1 phase transition.** T6's contraction subset
   $\mathcal B_\Pi$ lies in the snowball region; T6 does **not**
   contradict T1's extinction branch (where there is no fixed point in
   $\mathcal B_\Pi$ because $\snet < 0$ or $\loss > \Lstar$).
   T6 is **fully consistent** with T1: snowball implies fixed-point,
   extinction implies no fixed-point. The fixed-point existence at
   $x_\infty$ encodes the snowball-side attracting basin.

## Regime of validity for T6

T6 applies in the **snowball region**
$\{\loss(x_t; Q) < \Lstar(Q)\}$ on the all-positive-effective event
$\Ecal_+$, conditional on $\Pr[\Ecal_+] \ge \rateinitp^{T_{\max}} > 0$.
Within $\mathcal B_\Pi$ (the $\Pi$-projected contraction subset), $f$
is a contraction in the $\Pi$-weighted norm; the trajectory converges
to the unique fixed point $x_\infty \in \mathcal B_\Pi$ at rate
$\beta^t$ for $\beta < 1$ explicit in $S, L_{\mathrm{sm}}, w_{\max},
w_\min$.

**Outside the snowball region:** T6 does not apply (no lower bound on
the effective rate). **Outside $\mathcal B_\Pi$:** Jacobian norm
could exceed $1$; T6 only delivers local stability at $x_\infty$.

The exponential rate $\beta$ in T6's contraction can be bounded
explicitly: under \Cref{ass:bounded_value_norms} and
\Cref{ass:incoherent_unembedding},
$$\beta \;\le\; 1 - w_\min + 2 e^{4S} L_{\mathrm{sm}} \cdot |\Aset|/(|\Vocab|^n \cdot \norm{\Pi\nabla\loss})$$
on $\mathcal B_\Pi$, with $w_\min$ a lower bound on the softmax
weight in the bounded-score regime (also $O(e^{-2S}/T_{\max})$ from
\Cref{lem:max_attention_weight}-style symmetry).

## Summary recommendation for the writer agent

1. **State T6 in the weak form** (local exponential stability at
   $x_\infty$ in $\Pi$-weighted norm), with the strong form (global
   contraction on $\mathcal B_\Pi$) as a corollary under additional
   convexity hypothesis.
2. **Condition T6 on the all-positive-effective event $\Ecal_+$**
   (with $\Pr[\Ecal_+] \ge \rateinitp^{T_{\max}}$ noted as a caveat
   in a `\begin{remark}` that frames T6 as a "deterministic-equivalent
   companion of T1 on the snowball event".)
3. **Cite Bai et al. 2019** (`\cite{bai2019deq}`) for DEQ context.
   Add `cite-bai2019deq.md` digest.
4. **Use the $\Pi$-weighted norm** for the contraction inequality;
   discuss in a remark why Euclidean norm fails.
5. **Identify $x_\infty$** with the snowball-region attractor of T1
   via a one-line argument: the fixed point of $f$ on $\Ecal_+$ is the
   equilibrium where softmax-average past effective steps balance —
   matches T5's deterministic ODE attractor
   $m_\infty = \snet \cdot \cos\theta_0$ to leading order.
