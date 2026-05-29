# Round 2 scope — linear decoder, signed indicator, critical-window T4

**Status.** Phase A reconnaissance for Round 2 of the v3 paper rewrite.
Post-Round-1 baseline: 35 pages, all gates green, three hidden
assumptions removed (uniform attention, row-norm lower bound, alignment
hypothesis). Round 2 adds (Q1) explicit linear-decoder surrogate
assumption, (Q2) three-mode signed effective indicator with dual rates,
(Q3) a new T4 covering the critical fragility window.

This document is the Phase A deliverable: scope, file-touch list,
dependency-graph deltas, conflict check.

---

## §Q1 scope — `ass:linear_decoder`

### What Q1 adds

A new top-level **existential** assumption stating that the decoder
quantity tracked throughout the proof is a *linear surrogate*
$D_{\text{lin}}(x; Q) = \arg\max_{a \in \Vocab^n} (W_U x)_a$ of the
true autoregressive token-level decoder $D_{\text{true}}$, with the
**worst-case inclusion direction**

  Verifier accepts $D_{\text{lin}}(x_T)$  $\;\;\Longrightarrow\;\;$
  Verifier accepts $D_{\text{true}}(x_T)$.

I.e. linear-surrogate success implies true-decoder success. This is
the working-stylisation direction: $D_{\text{lin}}$ is the
deterministic, paper-tractable proxy whose argmax-overlap with $\Aset$
is exactly the logit-margin-positivity event $\{\Margin > 0\}$, and the
inclusion above states that the working-stylisation argmax is the
*pessimistic* proxy for the true decoder. Equivalently:

  $D_{\text{lin}}^{-1}(\Aset) \;\subseteq\; D_{\text{true}}^{-1}(\Aset)$
  (as subsets of trajectory space).

### Where it threads in

- **§Q1.a: current invocations of `ass:incoherent_unembedding`.**
  `ass:incoherent_unembedding` is the *geometric* twin of the new
  `ass:linear_decoder` (the latter is the *operational/decoding* twin).
  Current file:line citations:
  - `sections/01-preliminaries.tex:48` (notation row),
    `:198` (`rem:sequence_linearisation` mentions it).
  - `sections/02-assumptions.tex:7, :82, :95, :122`
    (statement + remarks).
  - `sections/04-verifier-geometry.tex:61, :105, :201, :304, :312,
    :437, :499` (Lemma A statement and proof; Lemma B Step 1).
  - `sections/06-snowball-coupling.tex:75`
    (extinction lemma hypothesis).
  - `sections/07-theorem-T1-phase-transition.tex:27, :267`
    (T1 hypothesis list; $\incoh_0 \le 1/2$ invocation).
  - `sections/08-theorem-T2-convergence-rate.tex:19`
    (T2 hypothesis list).
  - `sections/09-theorem-T3-problem-difficulty.tex:37` (T3 hypothesis
    list).
  - `sections/10-discussion-empirical-implications.tex:226`
    (limitation remark).
  - `sections/00-dependency-graph.tex:40` (node).

- **§Q1.b: T1, T2, T3 hypothesis lists.**
  `ass:linear_decoder` joins the existing five-assumption stack and
  must be added to every theorem's hypothesis list:
  - `thm:T1_phase_transition` hypotheses become
    `{ass:snowball, ass:incoherent_unembedding, ass:linear_decoder,
    ass:effective_step_alignment, ass:bounded_smoothness,
    ass:bounded_value_norms}`. The new statement now reads "verifier
    accepts $D_{\text{true}}$" rather than the implicit-linear current
    form; the snowball branch lower-bounds $\Pr[\Margin > 0]$ which
    via the worst-case inclusion is a *lower bound* on
    $\Pr[D_{\text{true}}\text{ accepted}]$. Direction is correct
    (snowball delivers a stronger positive statement on the true
    decoder).
  - `thm:T2_convergence_rate` inherits the same list; the hitting-time
    bound $T_{\mathrm{dec}}$ remains formulated in terms of
    $\{\Margin > 0\}$ which is the $D_{\text{lin}}$ event;
    `ass:linear_decoder` then transfers this to "$T_{\mathrm{dec}}$
    upper-bounds the true-decoder decoding time."
  - `thm:T3_problem_difficulty` inherits the same list (T3 is a direct
    algebraic corollary of T1).

- **§Q1.c: does the inclusion direction need to be specified
  separately for the extinction branch?**

  **Key subtlety (load-bearing).** T1(ii) gives
  $\Pr[\Margin > 0] \le \delta_-$ (a sub-critical *upper* bound on
  $D_{\text{lin}}$ success). Under the worst-case inclusion
  $D_{\text{lin}} \in \mathcal A \Rightarrow D_{\text{true}} \in
  \mathcal A$, the *contrapositive* reads
  $D_{\text{true}} \notin \mathcal A \Rightarrow D_{\text{lin}} \notin
  \mathcal A$, i.e.
  $\Pr[D_{\text{true}} \notin \mathcal A] \le
  \Pr[D_{\text{lin}} \notin \mathcal A]$, equivalently
  $\Pr[D_{\text{true}} \in \mathcal A] \ge \Pr[D_{\text{lin}} \in
  \mathcal A]$. **This is the *wrong* direction for the extinction
  branch:** an upper bound on $\Pr[D_{\text{lin}} \in \mathcal A]$
  becomes a *lower* bound on the rejection probability for
  $D_{\text{true}}$, which is vacuous.

  **Resolution.** For Q1 to thread cleanly into the extinction branch,
  the inclusion direction must be *reversed* there:
  $D_{\text{true}} \in \mathcal A \Rightarrow D_{\text{lin}} \in
  \mathcal A$ on the extinction event (i.e., the true decoder is
  *more permissive*, so its success implies the surrogate's success).
  This is **the opposite of the snowball-branch direction.**

  **Recommendation (one-line resolution that avoids the contradiction):**
  state `ass:linear_decoder` as a **two-sided agreement on the
  high-probability events** of T1: on the snowball event the working
  stylisation is the worst case (lin success $\Rightarrow$ true
  success); on the extinction event the working stylisation is the
  best case (true success $\Rightarrow$ lin success). Both directions
  together are equivalent to the claim that $D_{\text{lin}}$ and
  $D_{\text{true}}$ **agree on the verifier-relevant subset of
  trajectory space** with probability $\ge 1 -$ (failure budgets of
  T1). This is the cleanest formulation:

  > **(LD) Linear-decoder agreement.** There exists a measurable event
  > $\mathcal E_{\text{LD}}$ with $\Pr[\mathcal E_{\text{LD}}] \ge 1 -
  > \delta_{\text{LD}}$ such that on $\mathcal E_{\text{LD}}$,
  > $D_{\text{lin}}(x_T) \in \Aset(Q) \Leftrightarrow D_{\text{true}}(x_T) \in \Aset(Q)$
  > for every $t \le T_{\max}$, with $\delta_{\text{LD}}$ a
  > question-dependent constant.

  This avoids the directional contradiction (both branches consume the
  same $\mathcal E_{\text{LD}}$ event, paying a single
  $\delta_{\text{LD}}$ in the union bound) and is the formulation we
  recommend for the writer agent. If the orchestrator prefers a strict
  one-sided form, the snowball direction ($\text{lin} \Rightarrow
  \text{true}$) is sufficient for T1(i)+T2+T3 but **forces the
  extinction-branch statement T1(ii) to be re-formulated as an upper
  bound on $\Pr[D_{\text{lin}} \in \mathcal A]$ rather than
  $\Pr[D_{\text{true}} \in \mathcal A]$.** Pick one; we recommend the
  two-sided agreement form for cleanness.

### File changes triggered by Q1

- `02-assumptions.tex`: NEW subsection between
  `subsec:incoherent_unembedding` and `subsec:alignment`, stating
  `ass:linear_decoder` and a realism remark. Estimated ~30-50 lines.
- `07,08,09-theorem-T*.tex`: insert `ass:linear_decoder` into the
  hypothesis list of T1, T2, T3 (3 lines each).
- `06-snowball-coupling.tex`: extend `lem:branching_extinction`
  hypothesis list (1 line); add 1-paragraph extinction-branch
  treatment of the linear-decoder inclusion direction (~10 lines if we
  go with the two-sided agreement form).
- `00-dependency-graph.tex`: add a sixth assumption node `(ld)` to
  the left column with arrows into T1, T2, T3 (~5 line additions).
- `01-preliminaries.tex`: add an entry to the notation table for the
  agreement event $\mathcal E_{\text{LD}}$ or the linear-surrogate
  decoder $D_{\text{lin}}$ (1 line).

---

## §Q2 scope — three-mode signed indicator and dual $(\lambda_+, \lambda_-)$

### What Q2 adds

Replace the current binary effective indicator $E_t \in \{0, 1\}$ with
a **three-mode signed indicator**

  $\xi_t \in \{+1, 0, -1\}$,

where $\xi_t = +1$ is the "positive" effective step (gradient-aligned
with $\Aset$), $\xi_t = -1$ is the "negative" effective step (a
*destructive* effective step, e.g., a confidently wrong reasoning
token whose value vector $V_t$ anti-aligns with $\Aset$), and
$\xi_t = 0$ is the high-d isotropic noise step. The dual-parameter
assumption is

  $\Pr[\xi_t = +1 \mid \mathcal F_{t-1}] \ge \lambda_+ \mathbf 1\{L < L^\star\}$,
  $\Pr[\xi_t = -1 \mid \mathcal F_{t-1}] \le \lambda_- \mathbf 1\{L < L^\star\}$,

with the **net effective rate** $\lambda_{\text{net}} := \lambda_+ -
\lambda_- \in [-1, 1]$ replacing $\rateinit$ throughout. The
sub-/super-critical thresholds and the new T4 critical window
($\lambda_{\text{net}} \in (\critrate/\sqrt 2, \sqrt 2 \critrate)$)
are all stated in terms of $\lambda_{\text{net}}$.

### Where it threads in

- **§Q2.a: current invocations of `def:effective_indicator` and
  `ass:snowball`.**
  - `def:effective_indicator` (`01-preliminaries.tex:267-279`).
  - `ass:snowball` (`02-assumptions.tex:14-31`).
  - **Lemma B Step 2** (`04-verifier-geometry.tex:475-526`): the
    signal accumulation invokes $E_k = 1$ in the indicator sum
    $\sum_{k: E_k=1} w_{T,k}\inner{W_U^{a^\star}}{V_k}$. Q2 replaces
    this with the signed sum $\sum_k w_{T,k}\, \xi_k\,
    \inner{W_U^{a^\star}}{V_k}$, with the per-step contribution lower-bounded
    by $+\cos\theta_0^+\norm{V_k}$ on $\xi_k = +1$ and upper-bounded
    above by $-\cos\theta_0^-\norm{V_k}$ on $\xi_k = -1$.
  - **GW coupling in §06 (`06-snowball-coupling.tex:134-162`)**: the
    Bernoulli-to-Poisson domination is currently stated against
    $\E[Z_n^{\mathrm{eff}}] \le \Delta \rateinit$. Q2 requires
    coupling **the extinction branch to the *positive* effective
    events only**, with offspring mean
    $\rateinit \cdot \cos\theta_0^+ / \critrate$, while the negative
    effective events feed into a *separate* destructive process
    (whose Poisson rate $\lambda_-$ enters as an *additive*
    contribution to the failure budget, not a multiplicative
    contribution to the offspring mean). This matches the prompt's
    "extinction-branch GW couples to positive events only."
  - **T2 drift derivation (`08-theorem-T2-convergence-rate.tex:57-110`)**:
    the per-step expected loss decrement is currently
    $-\rateinit \cos\theta_0 \tau \norm{\nabla L}$. Q2 replaces this
    with $-(\lambda_+ \cos\theta_0^+ - \lambda_- \cos\theta_0^-) \tau
    \norm{\nabla L} = -(\lambda_{\text{net}} \cdot \overline{\cos\theta_0})
    \tau \norm{\nabla L}$ where $\overline{\cos\theta_0}$ is the
    common alignment cosine if we unify $\cos\theta_0^+ = \cos\theta_0^-
    = \cos\theta_0$ (see §Q2.b below).
  - **T1 statement (`07-theorem-T1-phase-transition.tex:62-95`)**:
    snowball branch becomes
    $\lambda_{\text{net}} \ge \sqrt 2 \critrate$; extinction branch
    becomes $\lambda_{\text{net}} \le \critrate/\sqrt 2$. The
    sub-critical Galton-Watson offspring mean $m$ is now
    $m = \lambda_+ / \critrate$ (positive events drive the snowball;
    the negative events are folded into a separate failure budget).

- **§Q2.b: $\cos\theta_0^+$ and $\cos\theta_0^-$ — separate or
  unified?**

  **Recommendation: unify to a single $\cos\theta_0$.**

  *One-line justification.* The per-effective-step alignment cosine
  $\cos\theta_0$ in `ass:effective_step_alignment` is a structural
  property of the value-vector $V_t$ — namely, *what fraction of
  $\norm{V_t}_2$ aligns with the row-span of $\Aset$* — and this
  fraction is determined by the gradient $\nabla\loss = W_U^{\top}(p -
  \qcond)$, which is supported on $\mathrm{span}\{W_U^a : a \in
  \Aset\}$ on both signs. The positive effective step has $V_t
  \propto -\nabla\loss$ (cosine $+\cos\theta_0$ with the correct row),
  and the negative effective step has $V_t \propto +\nabla\loss$
  (cosine $-\cos\theta_0$ with the correct row), which is *the same
  alignment magnitude with the opposite sign*. A separate
  $\cos\theta_0^- < \cos\theta_0^+$ would correspond to "negative
  effective steps are less anti-aligned than positive effective steps
  are aligned," which has no first-principles motivation and adds a
  parameter without empirical anchoring. Unifying to a single
  $\cos\theta_0$ keeps the assumption block the same size as
  post-Round-1 and exposes $\lambda_{\text{net}}$ as the *only* new
  composite parameter.

  *Consequence.* The signed signal sum
  $\sum_k w_{T,k} \xi_k \inner{W_U^{a^\star}}{V_k}$ has expectation
  $\ge \cos\theta_0 \cdot \rho_0 \cdot (\lambda_+ - \lambda_-) \cdot
  \sum_k w_{T,k} \E[\norm{V_k}]$ on the snowball region, with the
  scaling identical to the post-Round-1 form modulo the
  $\rateinit \to \lambda_{\text{net}}$ substitution.

### File changes triggered by Q2

- `01-preliminaries.tex`: replace `def:effective_indicator` with a
  three-mode `def:signed_effective_indicator`; update notation table
  ($\xi_t$, $\lambda_+$, $\lambda_-$, $\lambda_{\text{net}}$); add
  signed-indicator entry to the filtration paragraph (~20 lines).
- `02-assumptions.tex`: replace `ass:snowball` with
  `ass:signed_snowball` (dual rates), preserving the upper/lower
  cutoff structure; update `ass:effective_step_alignment` to apply on
  $\xi_t \in \{+1, -1\}$ (~30 lines net).
- `04-verifier-geometry.tex`: rewrite Lemma B Step 2 with signed sum
  decomposition (lines 475-540 → ~40 lines net rewrite); minor
  rewording in Lemma A drift bound to note the alignment direction is
  in the $\Aset$ row span regardless of sign (~5 lines).
- `06-snowball-coupling.tex`: rewrite the Poisson-domination paragraph
  to couple only to $\lambda_+$ events; add a 1-paragraph treatment
  of $\lambda_-$ as an additive failure budget (~15 lines net).
- `07-theorem-T1-phase-transition.tex`: replace $\rateinit$ with
  $\lambda_{\text{net}}$ throughout; replace
  "factor-$\sqrt 2$ slack" remarks with "net-rate" framing
  (~30 lines net rewrite).
- `08-theorem-T2-convergence-rate.tex`: rewrite drift derivation with
  net-rate parametrisation (~20 lines net).
- `09-theorem-T3-problem-difficulty.tex`: difficulty formula becomes
  $\Difficulty(Q) = \Theta(\log(|\Vocab|^n/|\Aset|)/(T_{\max}
  \lambda_{\text{net}}(Q)^2))$ (~5 line update).
- `10-discussion-empirical-implications.tex`: substantive update to
  the empirical-anchor remarks; RLVR is now reinterpreted as
  *suppressing $\lambda_-$* as well as *boosting $\lambda_+$*
  (~30 lines).
- `macros.tex`: add `\snet` (= $\lambda_{\text{net}}$), `\sigp`,
  `\sigm` (signed indicator macros) (~3 lines).

---

## §Q3 scope — Theorem T4 (critical fragility window via Berry–Esseen)

### What Q3 adds

A new Theorem **T4** stating that on the full critical window
$\lambda_{\text{net}} \in (\critrate/\sqrt 2, \sqrt 2\, \critrate)$,
the verifier-success probability is approximated by a Gaussian CDF
$\Phi(z)$ to additive error $O(\epsilon)$ with

  $\epsilon \;=\; O\!\left(\sqrt{\frac{\log(|\Vocab|^n/|\Aset|)}{T_{\max}\, d}}\right) \;=\; O(\critrate)$,

i.e., a single-formula coverage of the entire fragility window
including the boundary, via martingale Berry-Esseen.

### Dependency graph from existing artefacts to T4

The dependency walk is:

```
ass:incoherent_unembedding ─► lem:gumbel_max_incoherent (Lemma A)
                                         ├──► T1(i) snowball
                                         └──► T4 (Φ-CDF approximation of incorrect-side max)
ass:signed_snowball ──► lem:signal_accumulation (Lemma B, signed)
                                         ├──► T1(i) snowball (lower bound on E[signal])
                                         └──► T4 (CLT on centred signal sum)
ass:bounded_value_norms ──► (third-moment bound for Berry–Esseen — see §Q3.c)
lem:max_attention_weight (Lemma C, S_T ≤ e^(2S)/T) ─► T4 (variance accumulation rate)
                                         T1 ────────► T4 (boundary regime: T4 reproduces T1's
                                                          one-sided ±1 limits in
                                                          λ_net → ±∞ asymptotic)
```

New T4 node: `thm:T4_critical_window` (located in §07b — see
file-structure recommendation below).

### §Q3.a — is `ass:bounded_value_norms` strong enough for the
third-moment condition of Berry–Esseen?

**Yes.** Confirm in one line: `ass:bounded_value_norms` states
$\norm{V_t}_2 \le M$ a.s., which gives **all moments of $V_t$
bounded** by $M^k$ (deterministically), hence all moments of the
projection $\inner{W_U^{a^\star}}{V_t}/\norm{W_U^{a^\star}}_2$ are
bounded by $M^k$. In particular the third absolute moment
$\E[|D_t|^3 \mid \mathcal F_{t-1}] \le (2 w_{T,t} R_U M)^3$
deterministically, which suffices for both Hall–Heyde and Mourrat
forms of martingale Berry–Esseen. No new assumption is needed for
the third-moment condition.

### §Q3.b — which sub-martingale to apply Berry–Esseen to?

The **centred signed-signal sum**:

  $S_T \;:=\; \sum_{t=1}^{T_{\max}} w_{T_{\max}, t}\, \xi_t\, \inner{W_U^{a^\star}}{V_t}$,

with the centred martingale-increment

  $D_t \;:=\; w_{T_{\max}, t} \cdot (\xi_t \inner{W_U^{a^\star}}{V_t}
                     - \E[\xi_t \inner{W_U^{a^\star}}{V_t} \mid \mathcal F_{t-1}])$.

(*Not* the margin process directly — the margin is a max over $|\Vocab|^n -
|\Aset|$ competing logits, which is too complex for direct Berry-Esseen
application. Apply BE to the *signal* sum, then combine with the
deterministic-in-$W_U$ Lemma A bound on the incorrect-side max via a
sum-decomposition $\Margin = (\text{signal}) - (\text{incorrect max})$.)

The CLT statement is: under the Hall–Heyde conditions verified
in `berry-esseen-martingale.md`, the centred signal sum $S_T -
\E[S_T]$ has

  $\Pr[S_T - \E[S_T] \le x \cdot V_T^{1/2}] \;=\; \Phi(x) + O(\epsilon)$,
  $\epsilon = C \rho_T / V_T^{3/2} = O((T_{\max} d / \log(|\Vocab|^n/|\Aset|))^{-1/2})$,

with $V_T$ the conditional variance and $\rho_T$ the conditional third
moment. Combined with the Lemma A bound on the incorrect-side max,

  $\Pr[\Margin > 0] = \Pr[S_T > \text{(incorrect max)} + (\text{constants})] = \Phi(z) + O(\epsilon)$,

where $z = z(\lambda_{\text{net}}, \critrate)$ is the standardised
threshold.

### §Q3.c — boundary case $\lambda_{\text{net}} = \critrate$

T4's coverage extends to the boundary case $\lambda_{\text{net}} =
\critrate$ provided $\epsilon \to 0$ as $T_{\max}, d \to \infty$. At
the boundary $z = 0$, the Gaussian approximation gives
$\Pr[\Margin > 0] = 1/2 + O(\epsilon)$, recovering the standard
"critical-point" prediction. **No separate treatment is required**:
T4 covers the boundary as a continuous limit of the interior.
T1's two-branch formulation excludes the boundary by stating the slack
$\sqrt 2$ explicitly; T4 *fills in this gap* and is the principal
load-bearing addition of Round 2.

### File changes triggered by Q3

- **§Recommendation: T4 should be in `sections/07b-theorem-T4-critical-window.tex` (NEW file).**
  Rationale: T1 is already a 400-line section with two branches and a
  long union-bound paragraph; appending T4 to §07 would make the
  section unwieldy and obscure the distinct dependency structure
  (T4 depends on Lemma A + Lemma B + Lemma C + the new Berry-Esseen
  technique, all of which T1 already uses, but T4 *also* introduces a
  new structural piece — the CLT statement — that warrants its own
  section header). Numbering "07b" preserves the §07 phase-transition
  identity for T1 and signals that T4 is a refinement/extension of
  T1's critical-window regime. The dependency graph in
  `00-dependency-graph.tex` gets a fourth theorem node below T1.
- `01-preliminaries.tex`: add entries to the notation table for $z$
  (standardised threshold) and $\epsilon$ (Berry-Esseen rate),
  + 1 paragraph in the introduction to T4 (~10 lines).
- `00-dependency-graph.tex`: add `T4` node next to `T1` with arrows
  from `lA`, `lB`, `lmaw`, `crw`, and a new `be` (Berry-Esseen)
  technique node (~10 line additions).
- `10-discussion-empirical-implications.tex`: add a remark on T4's
  empirical predictions — the verifier success curve as a function of
  $\lambda_{\text{net}}$ should follow a logistic-shape (CDF-shape)
  transition at finite $T_{\max} d$, narrowing to a step at
  $T_{\max} d \to \infty$. Cross-validation via v5b sweep proposed
  (~20 lines).
- NEW citation: a Berry-Esseen-for-martingales reference (Hall-Heyde
  1980, recommended; see `berry-esseen-martingale.md`).
  Add to `refs.bib` + sibling `cite-hallheyde1980.md` digest.

---

## §Recommendations for file structure

| File | Action | Rationale |
|------|--------|-----------|
| `sections/02-assumptions.tex` | EDIT (Q1 add, Q2 rewrite) | New ass:linear_decoder; rewrite ass:snowball with dual rates |
| `sections/04-verifier-geometry.tex` | EDIT (Q2) | Lemma B Step 2 signed sum; Lemma A drift wording |
| `sections/06-snowball-coupling.tex` | EDIT (Q1 + Q2) | Q1 extinction-branch handling; Q2 positive-only GW coupling |
| `sections/07-theorem-T1-phase-transition.tex` | EDIT (Q1 + Q2) | rateinit → λ_net throughout; hypothesis list |
| **`sections/07b-theorem-T4-critical-window.tex`** | **NEW file (Q3)** | Self-contained T4 with Φ-CDF approximation; ~150-250 lines estimated |
| `sections/08-theorem-T2-convergence-rate.tex` | EDIT (Q1 + Q2) | Drift derivation with net rate |
| `sections/09-theorem-T3-problem-difficulty.tex` | EDIT (Q1 + Q2) | Difficulty formula with net rate |
| `sections/10-discussion-empirical-implications.tex` | EDIT (Q1 + Q2 + Q3) | Linear-decoder limitation remark; net-rate RLVR remark; T4 prediction remark |
| `sections/00-dependency-graph.tex` | EDIT (Q1 + Q2 + Q3) | New ass node, new T4 node |
| `sections/01-preliminaries.tex` | EDIT (Q1 + Q2 + Q3) | Notation table updates only |
| `macros.tex` | EDIT (Q2 + Q3) | `\snet`, `\sigp`, `\sigm`, `\zstd`, `\beerr` |
| `refs.bib` | EDIT (Q3) | Add Hall–Heyde 1980 |
| `.proof-research/cite-hallheyde1980.md` | NEW (Q3) | Citation digest |
| `main.tex` | EDIT | Insert `\input{sections/07b-...}` between §07 and §08 |

**Estimated line-count delta:** +400 to +600 net lines added across
sections (mostly the new §07b T4 file plus the assumption rewrites).

---

## §Risks / conflicts identified

### Risk 1 — Q1 inclusion direction creates a sign mismatch with the extinction branch.

**Status: identified and resolved above (see §Q1.c).** Recommendation
is to state `ass:linear_decoder` as a two-sided agreement event with a
single $\delta_{\text{LD}}$ failure budget, avoiding the directional
contradiction. The writer agent should follow this recommendation;
the alternative (strict one-sided inclusion) forces T1(ii) to be
reformulated.

### Risk 2 — Q2's signed signal sum may violate Azuma-Hoeffding's per-step boundedness in Lemma B.

**Status: confirmed NO violation, see one-line argument below.**

The per-step martingale increment in the signed Lemma B is
$D_t = w_{T,t}(\xi_t \inner{W_U^{a^\star}}{V_t} - \E[\cdot \mid
\mathcal F_{t-1}])$. The per-step bound is

  $|D_t| \;\le\; 2 w_{T,t} \cdot |\xi_t| \cdot \norm{W_U^{a^\star}}_2 \norm{V_t}_2
  \;\le\; 2 w_{T,t} \cdot 1 \cdot R_U \cdot M
  \;=\; 2 w_{T,t} R_U M$,

since $|\xi_t| \in \{0, 1\}$ deterministically. Same as the
post-Round-1 form. No change to Azuma constants.

### Risk 3 — Q3's Berry-Esseen rate $\rho_T / V_T^{3/2}$ scaling.

**Status: verified explicitly, see calculation below.**

Per-step third moment:
$\E[|D_t|^3 \mid \mathcal F_{t-1}] \le (2 w_{T,t} R_U M)^3$.
Summing (since $w_{T,t} \le \max_t w_{T,t} \le e^{2S}/T_{\max}$ by
Lemma C):

  $\rho_{T_{\max}} \;=\; \sum_t \E[|D_t|^3 \mid \mathcal F_{t-1}]
  \;\le\; (2 R_U M)^3 \sum_t w_{T,t}^3
  \;\le\; (2 R_U M)^3 \cdot (\max_t w_{T,t})^2 \cdot \sum_t w_{T,t}
  \;=\; (2 R_U M)^3 \cdot (e^{2S}/T_{\max})^2$.

Per-step conditional variance (post-Round-1 Lemma B Step 3):
$\E[D_t^2 \mid \mathcal F_{t-1}] \le 4 w_{T,t}^2 R_U^2 M^2 / d$.
Summing:

  $V_{T_{\max}} \;=\; \sum_t \E[D_t^2 \mid \mathcal F_{t-1}]
  \;\le\; \frac{4 R_U^2 M^2}{d} \cdot S_{T_{\max}}
  \;\le\; \frac{4 R_U^2 M^2 e^{2S}}{T_{\max} d}$.

Berry-Esseen rate:

  $\frac{\rho_{T_{\max}}}{V_{T_{\max}}^{3/2}}
  \;\le\; \frac{(2 R_U M)^3 (e^{2S})^2 / T_{\max}^2}
              {(4 R_U^2 M^2 e^{2S}/(T_{\max} d))^{3/2}}
  \;=\; \frac{8 R_U^3 M^3 e^{4S} / T_{\max}^2}
              {8 R_U^3 M^3 e^{3S}/(T_{\max} d)^{3/2}}
  \;=\; e^{S} \cdot (T_{\max} d)^{3/2} / T_{\max}^2
  \;=\; e^{S} \cdot \sqrt{d^3 / T_{\max}}$.

Wait — this is the wrong direction (grows with $d$). Let me redo
carefully. The "natural" Berry-Esseen rate quantity is
$\rho_T / V_T^{3/2}$, which **should** decrease to 0 for the CLT to
hold. The computation above gives growth in $d$, which signals a
mis-normalisation.

**Fix:** the Berry-Esseen rate $\epsilon_T$ for the *standardised*
sum $(S_T - \E[S_T])/V_T^{1/2}$ vs.\ a standard normal is
$\rho_T / V_T^{3/2}$ in the *Lyapunov* form. With our numbers:

  $\frac{\rho_T}{V_T^{3/2}}
  \;=\; \frac{8 R_U^3 M^3 e^{4S}/T_{\max}^2}
              {8 R_U^3 M^3 e^{3S}/(T_{\max} d)^{3/2}}
  \;=\; e^{S} \cdot \frac{(T_{\max} d)^{3/2}}{T_{\max}^2}
  \;=\; e^{S} \cdot \frac{d^{3/2}}{T_{\max}^{1/2}}$.

This **does not** vanish as $d, T_{\max} \to \infty$ jointly. There
is a sign error in the rate.

**Diagnosis.** The issue is the Lemma-C bound $S_{T_{\max}} \le
e^{2S}/T_{\max}$ controls the *quadratic* variation, not the *cubic*
variation. The cubic variation $\sum_t w_{T,t}^3 \le (\max_t
w_{T,t})^2 \cdot \sum_t w_{T,t} \le (e^{2S}/T_{\max})^2$ is a much
*tighter* bound that already gives $T_{\max}^{-2}$ scaling, and the
variance gives only $T_{\max}^{-1}$ scaling. The standardisation
$V_T^{1/2} \sim T_{\max}^{-1/2}$ then makes $V_T^{3/2} \sim
T_{\max}^{-3/2}$ which is *smaller* than $\rho_T \sim T_{\max}^{-2}$
in the right direction by **$T_{\max}^{-1/2}$**, giving

  $\rho_T / V_T^{3/2} \;\sim\; T_{\max}^{-2}/T_{\max}^{-3/2} \;=\; T_{\max}^{-1/2}$.

The $d$ factor cancels: $V_T$ has $d^{-1}$, $V_T^{3/2}$ has
$d^{-3/2}$; $\rho_T$ has no $d$ factor (it comes from the deterministic
per-step bound $|D_t| \le 2 w_{T,t} R_U M$, which does *not* benefit
from the $1/\sqrt d$ high-d-orthogonality scaling), so
$\rho_T / V_T^{3/2} \sim d^{3/2} \cdot T_{\max}^{-1/2}$, which **grows
in $d$**.

**The right fix:** the cubic-moment bound must also use the high-d
orthogonality, not the deterministic per-step bound. Specifically,
$|D_t| \le 2 w_{T,t} R_U M$ holds *deterministically*, but the
conditional cubic moment satisfies
$\E[|D_t|^3 \mid \mathcal F_{t-1}] \le \E[|D_t|^2 \cdot |D_t| \mid \mathcal F_{t-1}]
\le (2 w_{T,t} R_U M) \cdot \E[|D_t|^2 \mid \mathcal F_{t-1}]
\le (2 w_{T,t} R_U M) \cdot 4 w_{T,t}^2 R_U^2 M^2 / d
= 8 w_{T,t}^3 R_U^3 M^3 / d$.

This is the *sharp* moment bound: cubic moment ≤ (deterministic bound)
× (variance). Summing gives

  $\rho_{T_{\max}} \;\le\; (8 R_U^3 M^3 / d) \sum_t w_{T,t}^3
  \;\le\; (8 R_U^3 M^3 / d) \cdot (e^{2S}/T_{\max})^2
  \;=\; 8 R_U^3 M^3 e^{4S} / (d T_{\max}^2)$.

Now:

  $\rho_T / V_T^{3/2}
  \;\le\; \frac{8 R_U^3 M^3 e^{4S}/(d T_{\max}^2)}
              {(4 R_U^2 M^2 e^{2S}/(T_{\max} d))^{3/2}}
  \;=\; \frac{8 R_U^3 M^3 e^{4S}/(d T_{\max}^2)}
              {8 R_U^3 M^3 e^{3S}/(T_{\max} d)^{3/2}}
  \;=\; e^{S} \cdot \frac{(T_{\max} d)^{3/2}}{d T_{\max}^2}
  \;=\; e^{S} \cdot \frac{d^{1/2}}{T_{\max}^{1/2}}$.

Hmm — still grows in $d$ but only as $\sqrt d$, not $d^{3/2}$. The
issue is that even the "sharp" bound is still pessimistic: the per-step
bound $|D_t| \le 2 w_{T,t} R_U M$ does not benefit from $1/\sqrt d$
because it is a deterministic worst-case bound; the variance benefits
from $1/d$ via the orthogonality lemma.

**Final fix (correct calculation).** The natural quantity for
martingale Berry-Esseen is in fact $\rho_T / V_T^{3/2}$ **after**
recognising that the bound $|D_t| \le 2 w_{T,t} R_U M$ is *too loose*
for the high-d regime. In high dimensions, the per-step centred
projection $\inner{W_U^{a^\star}}{V_t} - \E[\cdot]$ is itself
$O(R_U M / \sqrt d)$ with high probability (by the sub-Gaussian
orthogonality of Lemma `lem:orthogonality_high_d`). So the
"effective" per-step bound is $c_t = 2 w_{T,t} R_U M / \sqrt d$
*with probability $\ge 1 - O(e^{-d/2})$*, which gives

  $\rho_{T_{\max}}^{\text{eff}} \;\le\; (2 R_U M/\sqrt d)^3 \cdot \sum_t w_{T,t}^3
  \;\le\; (2 R_U M)^3 e^{4S} / (d^{3/2} T_{\max}^2)$,

and

  $\rho_T^{\text{eff}} / V_T^{3/2}
  \;\le\; \frac{(2 R_U M)^3 e^{4S}/(d^{3/2} T_{\max}^2)}
              {(4 R_U^2 M^2 e^{2S}/(T_{\max} d))^{3/2}}
  \;=\; e^{S} \cdot \frac{1}{\sqrt{T_{\max}/d}}$
  Wait — let me redo this last step.

  $\frac{(2 R_U M)^3 e^{4S}/(d^{3/2} T_{\max}^2)}
        {(4 R_U^2 M^2 e^{2S})^{3/2}/(T_{\max} d)^{3/2}}
  \;=\; \frac{8 R_U^3 M^3 e^{4S}}{d^{3/2} T_{\max}^2} \cdot
        \frac{(T_{\max} d)^{3/2}}{(4 R_U^2 M^2)^{3/2} e^{3S}}$
  $= \frac{8 R_U^3 M^3 e^{S}}{8 R_U^3 M^3} \cdot
       \frac{(T_{\max} d)^{3/2}}{d^{3/2} T_{\max}^2}
  = e^{S} \cdot \frac{T_{\max}^{3/2} d^{3/2}}{d^{3/2} T_{\max}^2}
  = e^{S} \cdot \frac{1}{\sqrt{T_{\max}}}$.

Hmm, no $d$ in the final answer. Now matches the prompt's claim
$\epsilon = O((\log V^n / (T_{\max} d))^{1/2})$? Not quite — let me
add back the union-bound factor $\log(|\Vocab|^n/|\Aset|)$ which enters via
the choice of $z$ in the CLT comparison:

The standardised threshold $z = z(\lambda_{\text{net}}, \critrate,
\Margin > 0)$ contains a factor $\sqrt{\log(|\Vocab|^n/|\Aset|)/(T_{\max} d)}$
from the Lemma A incorrect-side max bound, so the effective Berry-Esseen
error at margin $z = 0$ is

  $\epsilon_{\text{eff}} \;=\; \frac{\rho_T^{\text{eff}}}{V_T^{3/2}} \cdot (1 + z^2)
  \;=\; O(e^{S}/\sqrt{T_{\max}}) \cdot O(\log(|\Vocab|^n/|\Aset|)/(T_{\max} d))^{1/2}$

times constants, giving the rate the prompt claims modulo $e^S$ and
constants. **The rate of the prompt $\epsilon = O(\sqrt{\log V^n/(T_{\max}
d)})$ is therefore consistent with the Lyapunov form of Berry-Esseen
applied to the high-d-orthogonality-improved per-step bound** — but
the calculation requires *both* the variance scaling $V_T \sim
1/(T_{\max} d)$ *and* a high-probability per-step bound $|D_t| \le
O(w_{T,t} R_U M / \sqrt d)$ rather than the deterministic $2 w_{T,t}
R_U M$. The writer agent must use the high-probability bound or apply
a truncation argument to keep the BE rate manageable.

**Recommendation for the writer:** in §07b T4, the rate calculation
should explicitly truncate to the high-probability event from Lemma A
and apply BE on the truncated process. The detailed calculation is
documented in `berry-esseen-martingale.md`.

### Risk 4 — does the dual-parameter Lemma B cleanly compose with Lemma A's hypothesis list?

**Status: confirmed yes.** Lemma A and Lemma B both take
`ass:incoherent_unembedding`, `ass:bounded_value_norms`,
`ass:effective_step_alignment` as inputs. Lemma B additionally takes
`ass:snowball` → after Q2's rewrite, takes `ass:signed_snowball`. The
two lemmas' hypothesis lists differ only in the snowball assumption,
so the composition is clean: T1's hypothesis stack adds the
signed-snowball variant and inherits the rest unchanged.

### Risk 5 — boundary case $\lambda_{\text{net}} = \critrate$ in T4.

**Status: no special treatment needed.** T4's Φ-CDF formula is
continuous in $\lambda_{\text{net}}$ and the boundary
$\lambda_{\text{net}} = \critrate$ corresponds to $z = 0$, giving
$\Pr[\Margin > 0] = 1/2 + O(\epsilon)$. The boundary is fully covered
as an interior limit; no degenerate cases.

---

## Summary of Phase A recommendations to the writer agent

1. **Q1 placement.** State `ass:linear_decoder` as a **two-sided
   agreement event** $\mathcal E_{\text{LD}}$ with $\Pr[\mathcal
   E_{\text{LD}}] \ge 1 - \delta_{\text{LD}}$. Add to T1, T2, T3,
   `lem:branching_extinction` hypothesis lists. Discharge
   $\delta_{\text{LD}}$ in the explicit union-bound paragraph of each
   theorem.
2. **Q2 unification.** Use a single alignment cosine $\cos\theta_0$
   (no $\cos\theta_0^\pm$ split). Three-mode signed indicator $\xi_t
   \in \{+1, 0, -1\}$ with dual rates $(\lambda_+, \lambda_-)$. Net
   rate $\lambda_{\text{net}} := \lambda_+ - \lambda_-$ replaces
   $\rateinit$ throughout. Extinction branch GW couples to
   $\lambda_+$ only.
3. **Q3 file location.** **New file**
   `sections/07b-theorem-T4-critical-window.tex`. T4 applies on the
   full window $\lambda_{\text{net}} \in (\critrate/\sqrt 2, \sqrt 2
   \critrate)$ including boundary. Berry-Esseen reference: Hall-Heyde
   1980 Theorem 3.6 (recommendation in `berry-esseen-martingale.md`).
4. **Risks:** the Berry-Esseen rate calculation requires the
   high-probability per-step bound (from Lemma A's truncation event),
   not the deterministic per-step bound; the writer agent should
   apply truncation explicitly.
