# Round 3 scope — A (framing) + B (invariants) + C (asymptotic ODE limit, T5) + D (DEQ contraction, T6)

**Status.** Phase A reconnaissance for Round 3 of the v3 paper
rewrite. Post-Round-2 baseline: 45 pages, 3 gates green, including
the linear-decoder agreement assumption (Q1), the three-mode signed
indicator (Q2), and Theorem T4 critical-window Berry-Esseen
approximation (Q3). Round 3 addresses the
**deterministic-trajectory-vs-probabilistic-framing** tension across
four orthogonal axes:

- **A**: framing remarks in §2 and §10 distinguishing
  deterministic-equivalent assumptions from essentially-probabilistic
  ones.
- **B**: elevate three already-implicit trajectory invariants to a
  dedicated §1 subsection `subsec:deterministic_invariants` and add a
  deterministic-offspring GW corollary in §6.
- **C**: new Theorem **T5** in new section §12, BA-G-J-style
  asymptotic ODE limit for the order parameter $m_t =
  \inner{W_U^{a^\star}}{x_t}/R_U$.
- **D**: new Theorem **T6** in new section §11, Banach
  fixed-point/DEQ contraction on a subset of the snowball region.

This document is the Phase A deliverable: scope, file-touch list,
load-bearing checks, and explicit recommendations to the writer agent.

---

## §A scope — framing remarks (§2 and §10)

### A.1 — `rem:deterministic_interpretation` in §2

**Location.** After `rem:net_rate` and before
`rem:snowball_mildness` in `subsec:signed_snowball` of `02-assumptions.tex`
(i.e., insertion at approximately line 73, after the closing of
`rem:net_rate`). Placement rationale: the remark interprets the
snowball assumptions deterministically immediately after defining
the net rate; this is the natural place for a deterministic-equivalent
framing remark.

**Content sketch.**
- Post-Round-2 the snowball assumptions
  (\Cref{ass:snowball_aligned,ass:snowball_anti_aligned}) define
  $(\lambda_+, \lambda_-)$ as conditional firing probabilities, but
  the analysis uses only the *averaged* properties via expectations
  in Lemma~B Step~1 (mean signal $\snet \cos\theta_0 \rho_0$).
- The deterministic-equivalent reading is: $(\lambda_+, \lambda_-)$
  are the **time-average empirical rates** of a *single deterministic
  trajectory*, $\lambda_+(L) = \lim_{T \to \infty}
  T^{-1} \sum_{t \le T} \1\{\xi_t = +1, \loss_{t-1} \in [L, L+dL]\}$,
  and the assumption becomes a *deterministic* lower bound on this
  time-average empirical rate.
- Under this interpretation, the framework's "probability" statements
  in T1, T2, T3 are read as concentration statements about the
  empirical rate of a *single* trajectory rather than ensemble-level
  probabilities. The interpretation is compatible because the
  effective-token-population dynamics are ergodic in the high-d limit
  (i.e., for $T_{\max} \gg \rateinitp^{-1}$, ensemble average and
  time average coincide to within $O(1/\sqrt{T_{\max} d})$).

### A.2 — `rem:randomness_role` in §10

**Location.** As a new remark in `subsec:limitations` of
`10-discussion-empirical-implications.tex`, between
`rem:linear_decoder_realism_v8` and `rem:critical_window_realism`
(i.e., insertion at approximately line 275).

**Content sketch.** Enumerate which assumptions in the framework
are **deterministic-equivalent** vs **essentially probabilistic**:
- **Deterministic-equivalent** (can be reread as
  time-average / single-trajectory invariants without changing the
  proof structure):
  - \Cref{ass:incoherent_unembedding} (geometric property of $W_U$,
    intrinsically deterministic).
  - \Cref{ass:linear_decoder} (event $\Eld$, $\delta_{\mathrm{LD}}$ as
    *trajectory-fraction* failure budget).
  - \Cref{ass:effective_step_alignment} (per-step structural
    property of $V_t$, no probabilistic statement).
  - \Cref{ass:bounded_value_norms,ass:bounded_smoothness}
    (regularity, deterministic a.s.).
- **Essentially probabilistic** (require randomness for the
  *concentration* statements that drive T1, T4):
  - The **noise-step variance bound** of
    \Cref{lem:orthogonality_high_d} (concentration in high $d$
    requires an underlying measure-theoretic notion).
  - The **martingale-tail** invocations of
    \Cref{lem:concentration_radial_walk}, Bernstein
    (\cite{freedman1975tail}), and Hall-Heyde
    (\cite{hallheyde1980}) all use probability.
- **Hybrid** (have a probabilistic and a deterministic-equivalent
  reading):
  - \Cref{ass:snowball_aligned,ass:snowball_anti_aligned}
    (probabilistic statement of conditional rates; deterministic
    reading as time-average empirical rates).
- **Conclusion:** the *behavioural* assumptions (snowball, linear
  decoder, alignment) admit deterministic-equivalent reformulations;
  the *regularity* assumptions are intrinsically deterministic; only
  the *concentration* machinery is essentially probabilistic. T5 (§12)
  formalises the deterministic-equivalent reading via the BA-G-J ODE
  limit; T6 (§11) formalises it via the Banach fixed-point.

### A.3 — file changes triggered by A

- `02-assumptions.tex`: insert `rem:deterministic_interpretation`
  (~30 lines).
- `10-discussion-empirical-implications.tex`: insert
  `rem:randomness_role` (~30 lines).

---

## §B scope — invariant elevation

### B.1 — Where to insert `subsec:deterministic_invariants` in §1

**Recommendation: BEFORE `subsec:ito` (i.e., after `subsec:filtration`
at approximately line 343).**

Rationale: `subsec:ito` is the **radial-coordinate** Ito expansion,
which is itself a *consequence* of the deterministic invariants
(specifically $\norm{x_t} \le M$, which constrains the radial
coordinate to be bounded). The invariants lemma is more general
than the Ito expansion and should logically precede it. Moreover,
`subsec:ito` is the only piece of §1 that uses the deterministic
norm bound $\norm{x_t} \le M$ implicitly via the "$\sigma \le c r
\sqrt d$" sub-condition; making the bound explicit in the invariants
subsection ahead of `subsec:ito` clarifies what hypotheses Lemma
`lem:radial_ito_expansion` is using.

### B.2 — `lem:trajectory_invariants` statement

**The three invariants:**
1. **Softmax weight convex-combination identity (deterministic):**
   For every $T \ge 1$, $\sum_{t=1}^T w_{T,t} = 1$ identically (i.e.,
   pointwise on every trajectory $\omega$). [Source:
   \Cref{lem:softmax_running_average} Step~2.]
2. **Trajectory norm bound (deterministic, a.s.):** For every
   $t \ge 0$, $\norm{x_t}_2 \le M$ a.s.,
   where $M$ is the value-norm bound of
   \Cref{ass:bounded_value_norms}. [Source: convex-combination
   representation $x_t = \sum_k w_{t,k} V_k$ from
   \Cref{lem:softmax_running_average} together with
   $\norm{V_k} \le M$ (\Cref{ass:bounded_value_norms}) and convexity
   of the norm: $\norm{x_t}_2 \le \sum_k w_{t,k} \norm{V_k}_2 \le M
   \cdot \sum_k w_{t,k} = M$.]
3. **Strict monotonicity of the cumulative score $s_T$
   (deterministic):** $s_T = \sum_{t \le T} e^{\inner{q}{k_t}}$ is
   strictly monotonically increasing in $T$, $s_T \ge s_{T-1} +
   e^{-S} > s_{T-1}$ for every $T \ge 1$. [Source: definition of
   $s_T$ in \Cref{def:softmax_attention} together with the bounded-score
   regime of \Cref{rem:bounded_score_regime}.]

**Statement:**
> **Lemma (Trajectory invariants).** Under
> \Cref{ass:bounded_value_norms}, the softmax-running-average trajectory
> $(x_t, s_t, w_{T,t})$ of \Cref{def:softmax_attention} satisfies the
> following three invariants on every trajectory $\omega \in \Omega$:
> (1) $\sum_{t=1}^T w_{T,t} = 1$ for every $T \ge 1$; (2)
> $\norm{x_t}_2 \le M$ for every $t \ge 0$; (3) $s_T$ is strictly
> monotonically increasing in $T$ with $s_T - s_{T-1} \ge e^{-S}$
> under the bounded-score regime of \Cref{rem:bounded_score_regime}.

**Proof (~10 lines): completely self-contained.** Uses only
`def:softmax_attention` + `ass:bounded_value_norms` +
`rem:bounded_score_regime` (the latter is itself a
consequence of `ass:bounded_value_norms` via Cauchy-Schwarz). No
circularity — none of the load-bearing proofs (Lemma~A, Lemma~B,
T1, T4) use the invariants as new objects; they use the underlying
facts (which were already implicit). Elevating the invariants is
purely *expository*: it makes explicit a deterministic structure
that was previously buried inside proofs.

### B.3 — Where to insert `rem:deterministic_offspring_corollary` in §6

**Location.** As a new remark after `rem:stochastic_domination_v3`
of `06-snowball-coupling.tex` (i.e., at approximately line 278).

**Content sketch.** Show that the GW extinction conclusion of
\Cref{lem:branching_extinction} is **monotone in the offspring
distribution**, so the same conclusion holds under any
deterministic-equivalent offspring count satisfying the same mean
upper bound $\le m$. Concretely: if instead of a random
$Z_n^{\mathrm{eff,+}}$ we use a deterministic count
$z_n^{\mathrm{eff,+}}$ with $z_n^{\mathrm{eff,+}} \le \Delta \cdot
\lambda_+(\loss_t)$ on the snowball region, the same extinction
inequality $\Pr[\Snowball] \le m^N$ holds. **Self-contained**: the
proof is one line ("monotonicity of extinction probability in the
offspring distribution"). No GW machinery needed beyond what's
already in §06.

This corollary is the *deterministic-equivalent companion* of
Lemma `lem:branching_extinction`: it allows the same conclusion to
be stated about a *deterministic* trajectory whose effective-token
count is upper-bounded by the snowball rate.

### B.4 — Circularity check for B

**Claim: no circularity.**
- The three invariants are *derived* facts from
  `def:softmax_attention` and `ass:bounded_value_norms`.
- Existing proofs (Lemma~A, Lemma~B, T1, T4) use the facts
  (i) $\sum_t w_{T,t} = 1$ explicitly (in Lemma~A Step~2 drift bound,
  and Lemma~B's signal calculation), and (ii) $\norm{x_t} \le M$
  implicitly (in Lemma~A's drift bound via convexity, and in
  `rem:bounded_score_regime` via Cauchy-Schwarz).
- Elevating these facts to a named lemma `lem:trajectory_invariants`
  does not introduce a new chain of reasoning — it merely consolidates
  the underlying inequalities into one place.
- No proof loop is created: `lem:trajectory_invariants` uses only
  `def:softmax_attention` + `ass:bounded_value_norms`; the load-bearing
  proofs may reference `lem:trajectory_invariants` instead of
  re-deriving each invariant. **Recommendation**: do NOT rewrite
  Lemma~A or Lemma~B to formally cite `lem:trajectory_invariants` —
  instead, the existing inline proofs continue to derive the
  invariants on-demand, and `lem:trajectory_invariants` is a
  consolidated reference for readers (a structural/expository
  contribution, not a logical/proof-graph contribution).

### B.5 — file changes triggered by B

- `01-preliminaries.tex`: insert new `subsec:deterministic_invariants`
  with `lem:trajectory_invariants` between `subsec:filtration` and
  `subsec:ito` (~40 lines for the subsection + lemma + proof).
- `06-snowball-coupling.tex`: insert `rem:deterministic_offspring_corollary`
  after `rem:stochastic_domination_v3` (~15 lines).
- `00-dependency-graph.tex`: add node for `lem:trajectory_invariants`
  in the §1 column with arrows to Lemma~A, Lemma~B, and the new T5/T6
  (~5 lines).
- `01-preliminaries.tex` notation table: add `lem:trajectory_invariants`
  to the `First in` column for $x_t$, $s_j$, $w_{T,t}$ (or leave
  unchanged — these are already pointed to `def:softmax_attention`).

---

## §C scope — Theorem T5 (asymptotic ODE limit)

### C.1 — Structure of §12 `sections/12-asymptotic-limit.tex`

**Recommended file structure (~150-200 lines):**

1. **Section header** (`sec:asymptotic-limit`, ~5 lines).
2. **Subsection: Setup and step-size identification** (~30 lines).
   - Define $m_t \coloneqq \inner{W_U^{a^\star}}{x_t}/R_U$.
   - Identify $\delta_d \coloneqq 1/T_{\max}$ with critical scaling
     $T_{\max} \asymp d$.
   - State the additional working stylisation (AS) needed for closability
     and explain its provenance from the snowball-region
     incorrect-side-max being dominated by the correct-side max.
3. **Subsection: T5 statement** (~30 lines).
   - State `thm:T5_asymptotic_ode` as a weak convergence theorem:
     the rescaled process $m^{(d)}_t \coloneqq m_{\lfloor t \cdot T_{\max}\rfloor}$
     converges weakly to the deterministic ODE solution
     $\dot m = h(m)$ in Skorokhod topology, where
     $h(m) = \snet(Q) \cos\theta_0 - m$ on $\{m > m^\star\}$.
4. **Subsection: Proof of T5** (~80 lines).
   - **Stage 1: Verify (BAGJ-H1) closability.** Use Lemma~B Step~1
     calculation to show the per-step conditional mean of $m_{t+1}
     - m_t$ closes onto a function of $m_t$ alone under (AS).
   - **Stage 2: Verify (BAGJ-H2) localizability.** Use
     `lem:max_attention_weight` and `lem:trajectory_invariants` to
     bound per-step increment by $O(1/T_{\max}) \to 0$.
   - **Stage 3: Verify (BAGJ-H3) drift Lipschitz.** Strengthen
     \Cref{ass:snowball_aligned} to require Lipschitz $\lambda_+(\loss)$
     (stated as a hypothesis of T5).
   - **Stage 4: Identify $\Sigma \equiv 0$.** Sum of per-step
     variances is $O(1/(T_{\max} d)) \to 0$, ODE not SDE.
   - **Stage 5: Apply BA-G-J Theorem 2.3** and conclude weak
     convergence to ODE.
5. **Subsection: Fixed-point and bistability** (~30 lines).
   - $m_\infty = \snet \cdot \cos\theta_0$ is the unique attracting
     stationary point on $(m^\star, 1]$.
   - $m^\star$ is unstable equilibrium (snowball boundary).
   - Connection to T1 phase transition: T5 is the deterministic
     equivalent of T1 in the $d \to \infty$ limit.
6. **Subsection: Discussion** (~30 lines).
   - Remark on why $m_t$ rather than $\loss_t$ (linearity, closability).
   - Remark on why ODE not SDE (sub-critical step size).
   - Remark on relation to T6 fixed-point (T5's $m_\infty$ matches
     T6's fixed-point projection onto $m$-coordinate).

### C.2 — Summary statistic choice

**Recommendation: $m_t = \inner{W_U^{a^\star}}{x_t}/R_U$.**

Rationale:
- **Linearity in $x_t$**: enables closed-form drift computation
  via Lemma~B Step~1 calculation.
- **Match to T1/T4**: T1 and T4 are stated in terms of
  $\Margin = \max_a \inner{W_U^a}{x_t} - \max_{a' \notin \Aset}
  \inner{W_U^{a'}}{x_t}$; $m_t = \inner{W_U^{a^\star}}{x_t}/R_U$
  is the leading correct-side contribution to $\Margin$ after
  normalising by $R_U$.
- **Bounded range**: $m_t \in [-1, 1]$ by Cauchy-Schwarz +
  `lem:trajectory_invariants` (item 2), automatic localizability
  on the compact $[-1, 1]$.
- **Match to the BA-G-J framework**: their order parameters
  $R_{in} = w_i \cdot B_n / d$ (Saad-Solla notation) are also
  unit-norm projections of the trajectory onto a fixed direction;
  $m_t$ is the direct analog.

Alternatives considered and rejected:
- **$\loss_t = -\log\cmass(x_t; Q)$**: non-linear (log-sum-exp), would
  require Taylor expansion + curvature corrections at every step,
  obscuring the BA-G-J closability check.
- **$r_t = \norm{x_t}$**: bounded but not aligned with the verifier's
  geometry; insensitive to the correct-row direction.
- **$\Margin_t$ itself**: the max over $|\Vocab|^n - |\Aset|$
  incorrect rows is non-smooth in $x_t$; not directly amenable to
  BA-G-J Lipschitz drift.

### C.3 — BA-G-J hypotheses to verify

See `.proof-research/ba-gj-summary-statistic-limit.md` for the
detailed check. Summary:
- **(BAGJ-H1) Asymptotic closability**: holds under additional
  working stylisation **(AS) Asymptotic single-coordinate dominance**.
  This is the **load-bearing strengthening** for T5.
- **(BAGJ-H2) Localizability**: holds via
  `lem:max_attention_weight` (per-step increment $\le e^{2S}/T_{\max}
  \to 0$ as $d \to \infty$ in the critical scaling).
- **(BAGJ-H3) Drift Lipschitz**: holds under strengthening
  `lambda_+(\loss)` Lipschitz (stated as T5 hypothesis only).
- **(BAGJ-H4) Diffusion non-degenerate**: **does not hold** — our
  per-step variance is $O(1/T_{\max}^2 d)$, summing to $O(1/T_{\max} d)
  \to 0$ in critical scaling. **Consequence**: BA-G-J SDE limit
  degenerates to a deterministic ODE in our scaling, which is what we
  want.

### C.4 — Strengthening of `ass:bounded_value_norms` and friends

**Required for T5**:
- **(AS) Asymptotic single-coordinate dominance**: a new working
  stylisation, stated only as a hypothesis of T5 (not used by T1, T2,
  T3, T4). States that in the snowball region, $\loss_t \approx
  \phi(m_t)$ for an explicit Lipschitz $\phi$. **Provenance**: holds
  when the incorrect-side max in Lemma~A is dominated by the
  correct-side max; this is the case in the snowball region with high
  probability by T1's snowball analysis.
- **Lipschitz $\lambda_+(\loss)$**: structural property of trained
  policies. Stated as a T5-only hypothesis.

**Not required**: no strengthening of `ass:bounded_value_norms`,
`ass:incoherent_unembedding`, `ass:bounded_smoothness`,
`ass:effective_step_alignment`, `ass:linear_decoder`, or
`ass:snowball_anti_aligned` is needed.

### C.5 — Dependency graph adjustments for T5

```
ass:snowball_aligned + (Lipschitz ext) ──┐
ass:effective_step_alignment            ├──► lem:signal_accumulation
ass:incoherent_unembedding              │        └──► (Step 1 calc reused)
ass:bounded_value_norms                 ├──► lem:trajectory_invariants
                                        │        └──► (per-step bound for BAGJ-H2)
(AS asymptotic single-coordinate)       │
                                        ├──► T5 (BA-G-J Thm 2.3 ODE limit)
                                        └──► (cite benarous2022highdim)
lem:max_attention_weight ──────────────►┘
                                          T1 ─► T5 (T5 is the deterministic
                                                      companion of T1)
                                          T5 ─► T6 (T5's fixed point
                                                      identified with T6's)
```

### C.6 — File changes triggered by C

- **NEW file** `sections/12-asymptotic-limit.tex` (~150-200 lines).
- `main.tex`: add `\input{sections/12-asymptotic-limit}` after
  `\input{sections/10-discussion-empirical-implications}` (or between
  §10 and the bibliography). Recommended: insert after §10 so the
  discussion section flows naturally into the asymptotic-limit refinement.
  *Alternative*: insert between §09 (T3) and §10 (discussion) if T5 is
  considered a *theorem* result rather than a discussion-section
  refinement. **Recommendation: between §10 and the bibliography**,
  keeping §10 as the empirical-implications discussion and §12 as the
  asymptotic deterministic-limit theorem.
- `00-dependency-graph.tex`: add T5 node with arrows from
  `ass:snowball_aligned (+L)`, `ass:effective_step_alignment`,
  `lem:trajectory_invariants`, `lem:max_attention_weight`, and the
  new `AS` working stylisation node (~10 lines).
- `01-preliminaries.tex` notation table: add `$m_t$` row with first
  appearance `Cref{thm:T5_asymptotic_ode}` (~1 line).
- `02-assumptions.tex`: add hypothesis-strengthening remark for
  `ass:snowball_aligned` noting that T5 requires Lipschitz
  $\lambda_+(\loss)$ (~5 lines, as a new remark).
- `macros.tex`: add `\snorder` (the order parameter $m$, distinct from
  `\Margin` which is the logit margin) (~1 line).

---

## §D scope — Theorem T6 (DEQ contraction / Banach fixed-point)

### D.1 — Structure of §11 `sections/11-contraction-fixed-point.tex`

**Recommended file structure (~120-180 lines):**

1. **Section header** (`sec:contraction-fixed-point`, ~5 lines).
2. **Subsection: Setup — memoryless reformulation** (~30 lines).
   - State the issue: $f$ depends on the entire history.
   - Resolution (R2): condition on the all-positive-effective event
     $\Ecal_+$, on which $V_t$ becomes a function of $x_{t-1}$ via
     the gradient.
   - Define the *conditional* memoryless map
     $f : \R^d \to \R^d$ on $\Ecal_+$.
3. **Subsection: T6 statement** (~30 lines).
   - State `thm:T6_contraction` in the **weak form**: $x_\infty$ is
     an exponentially stable fixed point of $f$ in the
     $\Pi$-weighted norm.
   - Strong form (uniform contraction on $\mathcal B_\Pi$) as a
     corollary under additional convexity hypothesis.
4. **Subsection: Proof of T6** (~70 lines).
   - **Stage 1: Existence of $x_\infty$.** Identify the fixed point
     of $f$ on $\Ecal_+$ via Brouwer (compactness from
     `lem:trajectory_invariants` item 2: $\norm{x_t} \le M$
     keeps the iteration in a compact ball).
   - **Stage 2: Jacobian computation.** Compute
     $\norm{\Pi \nabla_x f(x_\infty) \Pi}_{\mathrm{op}}$ explicitly
     using the L-smoothness of $\loss$ (`fac:loss_smoothness`) and the
     bounded-score regime.
   - **Stage 3: Verify contraction.** Show
     $\norm{\Pi \nabla_x f(x_\infty) \Pi}_{\mathrm{op}} \le \beta < 1$
     for explicit $\beta$.
   - **Stage 4: Apply Banach's theorem in a neighborhood.** Conclude
     exponential stability.
5. **Subsection: Identification of $x_\infty$ with T1/T5 attractor** (~20 lines).
   - The fixed point of $f$ on $\Ecal_+$ matches T5's deterministic
     ODE attractor $m_\infty = \snet \cdot \cos\theta_0$ projected
     onto the $W_U^{a^\star}$ direction.
6. **Subsection: Discussion** (~25 lines).
   - Remark: T6 is conditional on $\Pr[\Ecal_+] \ge \rateinitp^{T_{\max}}$,
     an exponentially-small event. Frame as a
     "deterministic-equivalent" companion of T1's snowball branch.
   - Remark: relation to DEQ literature (Bai et al. 2019).
   - Remark: why weighted norm, not Euclidean.

### D.2 — Contraction subset $\mathcal B$

**Recommendation: weighted contraction in the $\Pi$-projected
norm**, with $\Pi$ = projection onto
$\mathrm{span}\{W_U^a : a \in \Aset(Q)\}$.

The Euclidean operator norm is empty in any non-trivial subset of the
snowball region (as derived in `deq-fixed-point.md`). The
$\Pi$-projection exploits the effective-step alignment property
(\Cref{ass:effective_step_alignment}) to localise the Jacobian to the
correct-row subspace, where the Hessian is
$|\Aset|/|\Vocab|^n$-suppressed.

**$\mathcal B_\Pi$ (refined contraction subset):**
$$\mathcal B_\Pi \;\coloneqq\; \bigl\{x \in \R^d :
   \norm{\Pi \nabla\loss(x; Q)}_2 \;>\; 2 e^{4S} L_{\mathrm{sm}} \cdot
   |\Aset|/|\Vocab|^n\bigr\}.$$

In the snowball region $\{\loss < \Lstar\}$, $\norm{\Pi \nabla\loss}$
is bounded below by $\rho_0 \cdot (1 - e^{-\Lstar})/\sqrt{|\Aset|}$
(via the conditional posterior $\qcond$ supported on $\Aset$), so
$\mathcal B_\Pi$ is non-empty for sufficient $\Lstar$ and
sufficient $|\Vocab|^n/|\Aset|$.

### D.3 — Jacobian bound

See `.proof-research/deq-fixed-point.md` for the detailed calculation.
Summary:
$$\norm{\Pi \nabla_x f(x)}_{\mathrm{op}, \Pi}
   \;\le\; (1 - w_\min) + 2 w_{\max} L_{\mathrm{sm}} \cdot |\Aset|/(|\Vocab|^n \cdot \norm{\Pi\nabla\loss(x)}_2).$$
The first term comes from the convex-combination update; the second
from the value-vector $V$'s derivative.
**Inputs**:
- $w_{\max} \le e^{2S}/T_{\max}$ from
  \Cref{lem:max_attention_weight} (Lemma~C).
- $w_\min$ a comparable lower bound on the softmax weight in the
  bounded-score regime (derivable via similar Cauchy-Schwarz argument,
  ~3 lines in the proof).
- $L_{\mathrm{sm}} \le \norm{W_U}_{\mathrm{op}}^2/2$ from
  \Cref{fac:loss_smoothness}.
- $\norm{\Pi \nabla\loss(x)}_2$ lower-bounded in the snowball region by
  the gradient calculation $\nabla\loss = W_U^\top(p - \qcond)$.

### D.4 — Relation to T1 phase transition

**No conflict:**
- T6's contraction subset $\mathcal B_\Pi$ is *inside* the snowball
  region $\{\loss < \Lstar\}$. T6 applies on the snowball event,
  consistent with T1's snowball branch.
- T6 does **not** contradict T1's extinction branch: in the extinction
  branch $\snet < 0$ (or near zero with $\loss > \Lstar$), the
  effective-token rate is small, $\Pr[\Ecal_+]$ is even smaller, and
  the fixed-point existence does not contradict extinction (the
  trajectory does not reach $x_\infty$ because $\Ecal_+$ fails).
- T6's fixed point $x_\infty$ matches T5's ODE attractor $m_\infty$
  projected onto the $W_U^{a^\star}$ direction: $m(x_\infty) =
  \snet \cdot \cos\theta_0$.
- T6 is the **finite-$d$ deterministic companion** of T5's
  $d \to \infty$ ODE limit, both restricted to the snowball region.

### D.5 — File changes triggered by D

- **NEW file** `sections/11-contraction-fixed-point.tex` (~120-180 lines).
- `main.tex`: add `\input{sections/11-contraction-fixed-point}` between
  §10 and §12 (i.e., after `\input{sections/10-discussion-empirical-implications}`
  and before the new §12). *Alternative*: insert between §09 and §10.
  **Recommendation**: insert between §10 (discussion) and §12
  (asymptotic limit), giving the ordering §07/§07b/§08/§09/§10/§11/§12,
  so the discussion section flows naturally into the deterministic
  refinements §11 (T6) and §12 (T5).
- `refs.bib`: add `bai2019deq` entry (~10 lines).
- `00-dependency-graph.tex`: add T6 node with arrows from
  `ass:snowball_aligned`, `ass:effective_step_alignment`,
  `ass:linear_decoder`, `fac:loss_smoothness`,
  `lem:max_attention_weight`, `lem:trajectory_invariants` (~10 lines).
- `macros.tex`: add `\equilstate` (the fixed point $x_\infty$) and
  `\contract` (the Banach contraction constant $\beta$) (~2 lines).
- **NEW digest** `.proof-research/cite-bai2019deq.md` (~30 lines,
  written by Phase B writer).

---

## §Risks & load-bearing checks (critical)

### Risk 1 — Does BA-G-J Theorem 2.3 actually apply to our setup?

**Status: applies, with one mandatory strengthening.**

Per the detailed verification in
`.proof-research/ba-gj-summary-statistic-limit.md`:
- (BAGJ-H1) Asymptotic closability **fails without strengthening**;
  the per-step drift on $m_t$ depends on $\loss_t$ (via the snowball
  indicator $\1\{\loss_t < \Lstar\}$), which is not closable in
  $m_t$ alone.
- **Required strengthening (AS)**: assume $\loss_t \approx \phi(m_t)$
  for an explicit Lipschitz $\phi$ in the snowball region, which
  holds when the incorrect-side max is dominated by the correct-side
  max (an asymptotic property of the snowball region by Lemma~A).
- (BAGJ-H3) Drift Lipschitz **fails without strengthening**;
  requires $\lambda_+(\loss)$ Lipschitz, a structural assumption on the
  trained policy.
- (BAGJ-H2) Localizability and (BAGJ-H4) diffusion are OK
  (diffusion vanishes in our scaling, giving an ODE not SDE — this
  is *intended*).

**Recommendation**: state T5 with two explicit strengthenings:
1. **(AS) Asymptotic single-coordinate dominance** (Lipschitz $\phi$
   such that $\loss_t = \phi(m_t) + o_d(1)$ in the snowball region).
2. **Lipschitz $\lambda_+(\loss)$**.

Both are working stylisations stated as hypotheses of T5 only, not
imposed on the rest of the framework. This keeps T1, T2, T3, T4
unchanged.

### Risk 2 — Is $\norm{\nabla_x f}_{\mathrm{op}} < 1$ achievable for T6?

**Status: not in Euclidean norm; only in a weighted norm AND only
near the fixed point.**

Per the detailed analysis in `.proof-research/deq-fixed-point.md`:
- **Euclidean operator-norm contraction subset is empty** in any
  non-trivial subset of the snowball region. The $L_{\mathrm{sm}}/
  \norm{\nabla\loss}$ ratio that controls the Jacobian's value-vector
  derivative is too large (by a factor of $|\Vocab|^n$) in the snowball
  region.
- **Resolution**: weighted norm $\norm{\cdot}_\Pi$ with
  $\Pi = \mathrm{proj}_{\mathrm{span}\{W_U^a : a \in \Aset\}}$
  exploits the effective-step alignment to localise the Jacobian to
  the correct-row subspace, where the Hessian is
  $|\Aset|/|\Vocab|^n$-suppressed.
- **Even with weighted norm, the contraction may hold only locally**
  (at $x_\infty$), not uniformly on $\mathcal B_\Pi$.

**Recommendation**: state T6 in the **weak form**: $x_\infty$ is an
exponentially stable fixed point of $f$ in the $\Pi$-weighted norm,
with local convergence in a neighborhood of $x_\infty$. The strong
form (uniform contraction on $\mathcal B_\Pi$) is stated as a
corollary under additional convexity hypothesis.

**Severity of the weakening**: T6's weak form still delivers
"deterministic-trajectory contraction" — once the trajectory enters
the basin of attraction, exponential convergence at rate $\beta^t$
follows. The local-vs-global distinction is recovered by the
empirical observation that snowball-region trajectories typically lie
near the basin.

### Risk 3 — Memoryless reformulation for T6

**Status: $f$ is not memoryless on the unconditional trajectory;
T6 must be conditional on $\Ecal_+$.**

The attention recurrence $x_t = f_t(x_{t-1}, V_t, k_t)$ is
*time-varying* and depends on the cumulative score $s_t$ (which
depends on the entire history of keys). Banach's theorem requires a
**fixed** map $f : \mathcal B \to \mathcal B$.

**Resolution**: condition on the all-positive-effective event
$\Ecal_+ = \{\xi_t = +1 \,\forall t\}$. On $\Ecal_+$, the value vectors
$V_t = -\nabla\loss(x_{t-1})/\norm{\nabla\loss}$ are functions of
$x_{t-1}$, and the keys $k_t = W_K x_{t-1}$ are also functions of
$x_{t-1}$, giving a memoryless map $f : \R^d \to \R^d$.

**Severity**: $\Pr[\Ecal_+] \ge \rateinitp^{T_{\max}}$, an
*exponentially-small* event in the snowball region. This means T6's
conclusion is conditional on an exponentially-small event, which is
the cleanest rigorous formulation but somewhat weak as a
"deterministic-trajectory" statement.

**Recommendation**: state T6 conditionally on $\Ecal_+$ with the
caveat made explicit in a remark. Frame T6 as a
"deterministic-equivalent" companion of T1's snowball branch, valid
on the snowball event. Alternatively, formulate T6 as an
*expected*-trajectory statement: in expectation over the
non-effective steps, the trajectory contracts to $x_\infty$ at
average rate $\beta_{\mathrm{avg}}^t = (\rateinitp \beta + (1 -
\rateinitp))^t$.

### Risk 4 — Hypothesis-strengthening for T5

**Status: requires (AS) and Lipschitz $\lambda_+$. No
strengthening of `ass:bounded_value_norms` or other regularity
assumptions.**

The two strengthenings are stated as **T5-only** hypotheses, not
imposed on the rest of the framework. T1, T2, T3, T4 do not invoke
T5's hypotheses; the round-3 changes to §02-09 are additions, not
modifications.

### Risk 5 — Hypothesis-strengthening for T6

**Status: requires weighted-norm formulation and conditioning on
$\Ecal_+$. No strengthening of existing assumptions.**

T6's strengthenings are *structural* (weighted norm, conditional
formulation) rather than additional assumptions. T1, T2, T3, T4, T5
do not invoke T6's structural choices.

### Risk 6 — Self-containedness of `lem:trajectory_invariants` proof

**Status: completely self-contained.**

Uses only `def:softmax_attention` + `ass:bounded_value_norms` +
`rem:bounded_score_regime` (the latter being a derivable consequence
of `ass:bounded_value_norms` via Cauchy-Schwarz). No circular
dependencies; no GW or martingale machinery needed.

### Risk 7 — Self-containedness of deterministic GW corollary in §6

**Status: completely self-contained.**

The proof is one line ("monotonicity of extinction probability in the
offspring distribution"). Uses only `def:GW_offspring` and
`fac:gw_trichotomy_v3`, both of which are in §6 already. No new GW
machinery needed.

### Risk 8 — Possible interaction with confidence-trace v8 sweep

The Round-3 additions do not change T1, T2, T3, T4 statements or
proofs (only add framing remarks and new theorems T5, T6). The
confidence sweep should not be affected.

---

## §Recommendations for file structure

| File | Action | Rationale |
|------|--------|-----------|
| `sections/01-preliminaries.tex` | EDIT (B) | NEW `subsec:deterministic_invariants` with `lem:trajectory_invariants` BEFORE `subsec:ito` |
| `sections/02-assumptions.tex` | EDIT (A, B) | Add `rem:deterministic_interpretation`; add Lipschitz $\lambda_+$ remark for T5 |
| `sections/06-snowball-coupling.tex` | EDIT (B) | Add `rem:deterministic_offspring_corollary` |
| `sections/10-discussion-empirical-implications.tex` | EDIT (A) | Add `rem:randomness_role` |
| **`sections/11-contraction-fixed-point.tex`** | **NEW file (D)** | T6 contraction theorem, ~120-180 lines |
| **`sections/12-asymptotic-limit.tex`** | **NEW file (C)** | T5 BA-G-J ODE limit, ~150-200 lines |
| `sections/00-dependency-graph.tex` | EDIT (B, C, D) | New nodes for `lem:trajectory_invariants`, T5, T6 |
| `main.tex` | EDIT | Insert `\input{sections/11-...}` and `\input{sections/12-...}` after §10 |
| `macros.tex` | EDIT (C, D) | Add `\snorder`, `\equilstate`, `\contract` |
| `refs.bib` | EDIT (D) | Add `bai2019deq` |
| `.proof-research/cite-bai2019deq.md` | NEW (D) | Citation digest by Phase B writer |

**Section ordering after Round 3:**
- §00: dependency graph
- §01: preliminaries (with new `subsec:deterministic_invariants`)
- §02: assumptions (with `rem:deterministic_interpretation`)
- §03: softmax running average
- §04: verifier geometry (Lemma A, Lemma B, Lemma C, loss-to-margin)
- §05: high-d concentration
- §06: GW coupling (with `rem:deterministic_offspring_corollary`)
- §07: T1
- §07b: T4
- §08: T2
- §09: T3
- §10: discussion (with `rem:randomness_role`)
- §11: T6 (DEQ contraction) — **NEW**
- §12: T5 (BA-G-J ODE limit) — **NEW**

**Estimated line-count delta**: +400 to +500 net lines (~150 for §11,
~180 for §12, ~30 for framing remarks, ~50 for invariants subsection,
~15 for GW corollary, ~10 for `bai2019deq`, ~5 for macros).
**Estimated final paper length: ~50-52 pages** (from 45 in
post-Round-2 baseline).

---

## §Summary of Phase A recommendations to the writer agent

1. **A — framing remarks.** Add `rem:deterministic_interpretation`
   in §02 (after `rem:net_rate`); add `rem:randomness_role` in §10
   (in `subsec:limitations`). Both ~30 lines each. The
   `rem:randomness_role` should explicitly enumerate
   deterministic-equivalent vs essentially-probabilistic assumptions
   per the §A.2 list above.

2. **B — invariant elevation.** Add `subsec:deterministic_invariants`
   in §01 **BEFORE** `subsec:ito`. State and prove
   `lem:trajectory_invariants` with the three invariants in §B.2. Add
   `rem:deterministic_offspring_corollary` to §06 after
   `rem:stochastic_domination_v3`. No proof changes to Lemma~A, Lemma~B,
   T1, T4 — they continue to derive the invariants inline.

3. **C — T5 asymptotic ODE.** New section §12
   `sections/12-asymptotic-limit.tex`. Summary statistic
   $m_t = \inner{W_U^{a^\star}}{x_t}/R_U$. State T5 with TWO
   T5-only hypothesis strengthenings: (AS) asymptotic
   single-coordinate dominance + Lipschitz $\lambda_+(\loss)$.
   Use existing `\cite{benarous2022highdim}`. The limit is an
   **ODE** (not SDE) because diffusion vanishes in our
   $T_{\max} \asymp d$ scaling. ODE: $\dot m = \snet \cos\theta_0 - m$
   in the snowball region. Fixed point: $m_\infty = \snet \cos\theta_0$.

4. **D — T6 DEQ contraction.** New section §11
   `sections/11-contraction-fixed-point.tex`. State T6 in the
   **weak form** (local exponential stability at $x_\infty$ in
   $\Pi$-weighted norm), conditional on the all-positive-effective
   event $\Ecal_+$. The strong form (global contraction on
   $\mathcal B_\Pi$) is a corollary under convexity. Use weighted
   norm $\Pi = \mathrm{proj}_{\mathrm{span}\{W_U^a : a \in \Aset\}}$.
   Cite Bai et al. 2019 DEQ; add `bai2019deq` to `refs.bib` and
   `cite-bai2019deq.md` digest.

5. **Risks**:
   - T5 requires (AS) + Lipschitz $\lambda_+$ (T5-only hypotheses).
   - T6 is conditional on $\Ecal_+$ of probability
     $\ge \rateinitp^{T_{\max}}$ (frame as
     "deterministic-equivalent companion of T1 snowball branch").
   - T6 weak form only; strong form needs convexity.
   - No changes to T1, T2, T3, T4 statements or proofs.

6. **Section ordering**: §11 (T6) before §12 (T5). Rationale: T6 is
   finite-$d$ deterministic, T5 is asymptotic ($d \to \infty$); the
   natural reading order is finite → asymptotic. Both are after §10
   (discussion) to keep the four main theorems §07/§07b/§08/§09
   together.
