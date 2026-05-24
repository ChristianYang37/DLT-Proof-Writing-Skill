# Confidence trace — Phase C.5 sweep

This trace enumerates every derivation step in the proofs of
\Cref{lem:softmax_running_average,lem:anchor_decomposition,lem:anchor_accuracy_bound,lem:anchor_count_lb,lem:anchor_mass_lb,lem:T_polynomial,lem:decoding_correctness,thm:main_convergence_hp}
(in topological order) and tags each step with a confidence level per
the taxonomy of `references/confidence-sweep.md`.

Tag taxonomy:
- 🔴 from-memory — not yet verified
- 🟡 cross-checked — matched against an external reference / project lemma
- 🟢 verified — independently re-derived, hand-checked, or named textbook fact

## Step 1
**Location:** sections/03-lemma-softmax-running-average.tex:27
**Content (≤ 2 lines):** $s_j = s_{j-1} + e^{\inner{q}{k_j}}$ from
$s_j \coloneqq \sum_{i=1}^j e^{\inner{q}{k_i}}$ by splitting off the last term.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial algebra — summation of one extra term.
Hand-checked: $\sum_{i=1}^j a_i = \sum_{i=1}^{j-1} a_i + a_j$ for any
finite sum.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 2
**Location:** sections/03-lemma-softmax-running-average.tex:30
**Content (≤ 2 lines):** $s_j x_j = \sum_{k=1}^j e^{\inner{q}{k_k}} V_k$
by multiplying \Cref{eq:cumulative_softmax} through by $s_j$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebraic manipulation of
$x_j = (1/s_j) \sum_k e^{\inner{q}{k_k}} V_k$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 3
**Location:** sections/03-lemma-softmax-running-average.tex:32
**Content (≤ 2 lines):** $\sum_{k=1}^{j-1} e^{\inner{q}{k_k}} V_k + e^{\inner{q}{k_j}} V_j = s_{j-1} x_{j-1} + e^{\inner{q}{k_j}} V_j$
by induction (applying \Cref{eq:cumulative_softmax} at index $j-1$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Inductive base case $s_0 x_0 = 0$ (vacuous sum)
plus inductive step. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 4
**Location:** sections/03-lemma-softmax-running-average.tex:44
**Content (≤ 2 lines):** $\sum_k w_{j,k} = (1/s_j) \sum_k e^{\inner{q}{k_k}} = s_j / s_j = 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution of definitions. Trivial.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 5
**Location:** sections/04-lemma-anchor-decomposition.tex:38
**Content (≤ 2 lines):** $\sum_k w_{j,k} V_k - V^* = \sum_k w_{j,k} (V_k - V^*)$
using $\sum_k w_{j,k} = 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebraic identity:
$\sum_k w_{j,k} (V_k - V^*) = \sum_k w_{j,k} V_k - V^* \sum_k w_{j,k} = \sum w V_k - V^* \cdot 1$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 6
**Location:** sections/04-lemma-anchor-decomposition.tex:46
**Content (≤ 2 lines):** Triangle inequality applied to the convex
combination: $\|\sum_k w_{j,k} (V_k - V^*)\| \le \sum_k w_{j,k} \|V_k - V^*\|$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Minkowski / triangle
inequality for sums) with non-negative weights. Standard.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 7
**Location:** sections/04-lemma-anchor-decomposition.tex:48
**Content (≤ 2 lines):** Splitting sum at anchor set and bounding
non-anchor terms by $D_j$:
$\sum_{k \notin \mathcal A} w_{j,k} \|V_k - V^*\| \le D_j \sum_{k \notin \mathcal A} w_{j,k}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of $D_j$ as the max gives
$\|V_k - V^*\| \le D_j$ for all $k$, in particular for $k \notin \mathcal A$;
factoring the non-anchor weights out is algebraic.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 8
**Location:** sections/04-lemma-anchor-decomposition.tex:50
**Content (≤ 2 lines):** $\sum_{k \notin \mathcal A} w_{j,k} = 1 - \sum_{k \in \mathcal A} w_{j,k}$
using $\sum_k w_{j,k} = 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebraic rearrangement of a partition sum.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 9
**Location:** sections/05-lemma-anchor-accuracy.tex:18
**Content (≤ 2 lines):** $\norm{V(a_k) - V^*(Q)} \le \varepsilon_{\mathrm{anc}}$
for $a_k \in \mathcal A(Q)$, by direct invocation of
\Cref{ass:anchor_set_accuracy}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Re-checked \Cref{ass:anchor_set_accuracy}
(at sections/02-assumptions.tex:18) — assumption hypothesis matches exactly.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 10
**Location:** sections/05-lemma-anchor-accuracy.tex:21
**Content (≤ 2 lines):** Taking max over $k \in \mathcal A^{\mathrm{traj}}_j$
preserves the per-element upper bound $\varepsilon_{\mathrm{anc}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial — max of bounded quantities is bounded
by the bound.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 11
**Location:** sections/06-lemma-anchor-count.tex:30
**Content (≤ 2 lines):** $X_j = \1\{a_j \in \mathcal A(Q)\}$ and
$p_j = \Pr[X_j = 1 \mid \mathcal F_{j-1}] \ge p_0$ by \Cref{ass:anchor_emission_prob}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{ass:anchor_emission_prob} (at
sections/02-assumptions.tex:43) states this bound exactly, conditional
on the active question being $Q$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 12
**Location:** sections/06-lemma-anchor-count.tex:39
**Content (≤ 2 lines):** $M_t = \sum_{j=1}^t (X_j - p_j)$ is an
$(\mathcal F_t)$-martingale with $M_0 = 0$ and bounded differences
$|M_t - M_{t-1}| \le 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Centred-indicator martingale construction; each
$D_j = X_j - p_j$ has $\E[D_j \mid \mathcal F_{j-1}] = 0$. Bounded
differences: $X_j \in \{0,1\}$, $p_j \in [0,1]$, so $D_j \in [-1, 1]$
and $|D_j| \le 1$. Textbook construction.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 13
**Location:** sections/06-lemma-anchor-count.tex:55
**Content (≤ 2 lines):** Multiplicative-Chernoff for conditional Bernoullis
gives $\Pr[\sum X_j \le \mu/2] \le \exp(-\mu/8) \le \exp(-p_0 T/8)$,
using $\mu = \sum p_j \ge p_0 T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches chernoff-bernoulli.md digest exactly
(multiplicative-Chernoff at $\delta = 1/2$ gives exponent $-\mu/8$).
Conditional / martingale version follows from Freedman 1975.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 14
**Location:** sections/06-lemma-anchor-count.tex:58
**Content (≤ 2 lines):** $|\mathcal A^{\mathrm{traj}}_T| = M_T + \sum_j p_j \ge -p_0T/2 + p_0 T = p_0 T / 2$
on the complement of the Azuma failure event.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebraic substitution.
$\sum X_j = M_T + \sum p_j$ by definition of $M_T$, and
$\sum p_j \ge p_0 T$ by \Cref{ass:anchor_emission_prob}.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 15
**Location:** sections/06-lemma-anchor-count.tex:70
**Content (≤ 2 lines):** Inverting $e^{-p_0 T/8} \le \delta_1$ gives
$T \ge 8 \log(1/\delta_1) / p_0$ as the sufficient horizon.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct log inversion. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 16
**Location:** sections/07-lemma-anchor-mass.tex:36
**Content (≤ 2 lines):** $e^{\inner{q}{k_\ell}} \le e^{-\Delta} e^{\inner{q}{k_{k^\star}}}$
for any anchor $k^\star$ and non-anchor $\ell$, by exponentiating the
score margin from \Cref{ass:score_margin}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{ass:score_margin} (sections/02-assumptions.tex:67)
gives the score gap; exponentiating preserves the inequality (monotonicity of $e^x$).
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 17
**Location:** sections/07-lemma-anchor-mass.tex:44
**Content (≤ 2 lines):** Averaging Step 16 over anchor positions:
$e^{\inner{q}{k_\ell}} \le (e^{-\Delta}/|\mathcal A^{\mathrm{traj}}_j|) \sum_{k \in \mathcal A^{\mathrm{traj}}_j} e^{\inner{q}{k_k}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Sum Step 16 over $k^\star \in \mathcal A^{\mathrm{traj}}_j$,
divide both sides by $|\mathcal A^{\mathrm{traj}}_j|$. Direct algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 18
**Location:** sections/07-lemma-anchor-mass.tex:54
**Content (≤ 2 lines):** Summing the pointwise bound over non-anchors:
$\sum_\ell e^{\inner{q}{k_\ell}} \le r \cdot \sum_{k \in \mathcal A^{\mathrm{traj}}_j} e^{\inner{q}{k_k}}$
with $r = (|\text{non-anchors}|/|\mathcal A^{\mathrm{traj}}_j|) e^{-\Delta}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Summation of Step 17 over $\ell$; the RHS pulls
$|\text{non-anchors}|$ out of the sum. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 19
**Location:** sections/07-lemma-anchor-mass.tex:74
**Content (≤ 2 lines):** $\sum_{k \in \mathcal A^{\mathrm{traj}}_j} w_{j,k} = A/(A+B)$
where $A = \sum_{k \in \mathcal A} e^{\inner{q}{k_k}}$ and
$B = \sum_{\ell \notin \mathcal A} e^{\inner{q}{k_\ell}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $w_{j,k} = e^{\inner{q}{k_k}}/s_j$ with $s_j = A + B$.
Summing over anchors: $\sum w_{j,k} = A/(A+B)$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 20
**Location:** sections/07-lemma-anchor-mass.tex:78
**Content (≤ 2 lines):** $A/(A+B) = 1/(1 + B/A) \ge 1/(1+r) \ge 1 - r$
using $B/A \le r$ and the elementary inequality $1/(1+r) \ge 1 - r$ for $r \ge 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named elementary inequality:
$(1+r)(1-r) = 1 - r^2 \le 1$ for $r \ge 0$, so $1 - r \le 1/(1+r)$.
Combined with monotonicity of $1/(1+x)$ on $x \ge 0$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 21
**Location:** sections/08-lemma-T-polynomial.tex:46
**Content (≤ 2 lines):** Decomposition step: invoke
\Cref{lem:anchor_decomposition} with $\mathcal A = \mathcal A^{\mathrm{traj}}_T$,
giving $\norm{x_T - V^*} \le \sum_{\mathcal A^{\mathrm{traj}}_T} w \norm{V_k - V^*} + (1 - \sum_{\mathcal A^{\mathrm{traj}}_T} w) D_T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:anchor_decomposition} holds for any
subset of $\{1,\dots,j\}$; $\mathcal A^{\mathrm{traj}}_T \subseteq \{1,\dots,T\}$
is a valid subset. Hypotheses (non-negative weights, sum to 1) hold by
\Cref{lem:softmax_running_average}.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 22
**Location:** sections/08-lemma-T-polynomial.tex:55
**Content (≤ 2 lines):** Anchor-error term bounded by
$\varepsilon_{\mathrm{anc}} \sum_{\mathcal A^{\mathrm{traj}}_T} w \le \varepsilon_{\mathrm{anc}}$
using \Cref{lem:anchor_accuracy_bound} and $\sum w \le 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 23
**Location:** sections/08-lemma-T-polynomial.tex:64
**Content (≤ 2 lines):** $D_T \le \max_k \norm{V_k} + \norm{V^*} \le M + \norm{V^*}$
by triangle inequality and \Cref{ass:bounded_value_norms}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Triangle:
$\norm{V_k - V^*} \le \norm{V_k} + \norm{V^*}$; take max over $k$ and
apply $\norm{V_k} \le M$ from \Cref{ass:bounded_value_norms}.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 24
**Location:** sections/08-lemma-T-polynomial.tex:67
**Content (≤ 2 lines):** On $\Ecal_1$, leakage bounded:
$1 - \sum w \le (T / (p_0 T/2)) e^{-\Delta} = (2/p_0) e^{-\Delta}$
via \Cref{lem:anchor_mass_lb}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute $|\text{non-anchors}| \le T$ and
$|\mathcal A^{\mathrm{traj}}_T| \ge p_0 T/2$ (event $\Ecal_1$) into
\Cref{eq:anchor_mass_bound}.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 25
**Location:** sections/08-lemma-T-polynomial.tex:84
**Content (≤ 2 lines):** Combined bound on $\Ecal_1$:
$\norm{x_T - V^*} \le \varepsilon_{\mathrm{anc}} + (2/p_0) e^{-\Delta}(M + \norm{V^*})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct combination of Step 22, 23, 24 plugged
into Step 21.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 26
**Location:** sections/08-lemma-T-polynomial.tex:93
**Content (≤ 2 lines):** Condition $(2/p_0) e^{-\Delta}(M + \norm{V^*}) \le \gamma/2$
inverts to $\Delta \ge \log(4(M + \norm{V^*})/(p_0 \gamma))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Solve for $\Delta$: $e^{-\Delta} \le p_0 \gamma / (4(M + \norm{V^*}))$,
take logs. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 27
**Location:** sections/08-lemma-T-polynomial.tex:75
**Content (≤ 2 lines):** Equivalence of \Cref{eq:Delta_condition}
($\Delta \ge \log(4(M+\norm{V^*})/(p_0\gamma))$) and the leakage bound
$(2/p_0) e^{-\Delta}(M + \norm{V^*}) \le \gamma/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebraic manipulation: take log of both
sides of $e^{-\Delta} \le p_0 \gamma / (4(M + \norm{V^*}))$, multiply
through by $(2/p_0)(M + \norm{V^*})$. Hand-checked.
**Sub-agent task id:** none
**Sub-agent task id:** sweep-step-27-self
**Last updated:** 2026-05-24T22:00:00Z

## Step 28
**Location:** sections/09-lemma-decoding.tex:19
**Content (≤ 2 lines):** $\gamma > 2\varepsilon_{\mathrm{anc}}$ implies
$\varepsilon_{\mathrm{anc}} \le \gamma/2$ (rearranging).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial division by 2.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 29
**Location:** sections/09-lemma-decoding.tex:25
**Content (≤ 2 lines):** $\gamma/2 + \varepsilon_{\mathrm{anc}} \le \gamma/2 + \gamma/2 = \gamma$
by combining the hypothesis and Step 28.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial arithmetic addition.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 30
**Location:** sections/09-lemma-decoding.tex:30
**Content (≤ 2 lines):** $\norm{x - V^*} \le \gamma$ implies
$\dec(x) \in \Correct(Q)$ by direct invocation of
\Cref{ass:decoding_existence}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{ass:decoding_existence} (sections/02-assumptions.tex:106)
states the implication exactly; hypothesis $\norm{x - V^*} \le \gamma(Q)$
is met by Step 29.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 31
**Location:** sections/10-main-theorem.tex:48
**Content (≤ 2 lines):** Definition of $\Ecal_1 = \{|\mathcal A^{\mathrm{traj}}_T| \ge p_0 T/2\}$
as the deterministic-bound-driving event.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct setup; no inference. The event is well-defined
and measurable w.r.t.\ $\sigma(a_1,\dots,a_T)$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 32
**Location:** sections/10-main-theorem.tex:53
**Content (≤ 2 lines):** On $\Ecal_1$,
$\norm{x_T - V^*(Q)} \le \gamma(Q)/2 + \varepsilon_{\mathrm{anc}}$
via \Cref{lem:T_polynomial}, when $T \ge T(Q,\delta)$ and \Cref{eq:thm_main_Delta_condition}
holds.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:T_polynomial} hypothesis check:
(i) the five assumptions hold (theorem-level hypotheses); (ii)
\Cref{eq:thm_main_Delta_condition} subsumes the per-question condition
\Cref{eq:Delta_condition} for any $Q \in F$ since
$\gamma(Q) \ge \gamma_{\min}$ and $\norm{V^*(Q)} \le \max_Q \norm{V^*(Q)}$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 33
**Location:** sections/10-main-theorem.tex:61
**Content (≤ 2 lines):** $\dec(x_T) \in \Correct(Q)$ on $\Ecal_1$, via
\Cref{lem:decoding_correctness} applied to $x = x_T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:decoding_correctness} hypothesis check:
$\norm{x_T - V^*(Q)} \le \gamma(Q)/2 + \varepsilon_{\mathrm{anc}}$ is
exactly the bound from Step 32.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 34
**Location:** sections/10-main-theorem.tex:68
**Content (≤ 2 lines):** $\Pr[\Ecal_1] \ge 1 - \delta/2$ via
\Cref{lem:anchor_count_lb} at confidence $\delta_1 = \delta/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:anchor_count_lb} hypothesis check:
$T \ge 8 \log(1/\delta_1)/p_0^2 = 8 \log(2/\delta)/p_0^2$, which is
implied by $T \ge T(Q,\delta) = C_\star \log(2/\delta)/p_0^2$ when
$C_\star \ge 8$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 35
**Location:** sections/10-main-theorem.tex (theorem proof Step 1)
**Content (≤ 2 lines):** Setting $\delta = 2 \exp(-p_0 T/8)$ makes
$T(Q,\delta) = T$ tautologically, so \Cref{lem:T_polynomial} applies
and gives the deterministic bound with prob $\ge 1 - \delta/2 = 1 - \exp(-p_0 T/8)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution:
$T(Q,\delta) = (8/p_0) \log(2/\delta) = (8/p_0) \log(2/(2 \exp(-p_0 T/8))) = (8/p_0)(p_0 T/8) = T$.
The lemma's hypothesis $T \ge T(Q,\delta)$ holds with equality.
$\delta \in (0,1)$ requires $T > 8 \log 2 / p_0 \approx 5.55/p_0$;
for smaller $T$ the theorem statement is vacuous (RHS $\le 0$).
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 36
**Location:** sections/10-main-theorem.tex (theorem proof Step 3)
**Content (≤ 2 lines):** Slack absorption
$1 - \exp(-p_0 T/8) \ge 1 - 2 \exp(-p_0 T/8)$ for $T \ge 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial: $2 \exp(\cdot) \ge \exp(\cdot)$, so
$1 - 2 \exp(\cdot) \le 1 - \exp(\cdot)$. The factor 2 is inserted to
make the theorem and corollary use the same rate constant.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 37
**Location:** sections/10-main-theorem.tex (corollary proof)
**Content (≤ 2 lines):** Deterministic upper bound $Y \le G$ where
$Y = \norm{x_T - V^*(Q)}$ and $G = M + \norm{V^*(Q)}$, via convex
combination and \Cref{ass:bounded_value_norms}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $x_T = \sum_k w_{T,k} V_k$
(\Cref{lem:softmax_running_average}) is a convex combination with
$\sum w_{T,k} = 1$ and $w_{T,k} \ge 0$. Triangle inequality:
$\norm{x_T} \le \sum_k w_{T,k} \norm{V_k} \le M \sum_k w_{T,k} = M$.
Then $Y \le \norm{x_T} + \norm{V^*(Q)} \le M + \norm{V^*(Q)} = G$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 38
**Location:** sections/10-main-theorem.tex (corollary proof)
**Content (≤ 2 lines):** Tail-to-expectation conversion
$\E[Y] = \E[Y \1_{\Ecal^\star}] + \E[Y \1_{(\Ecal^\star)^c}]
       \le (\gamma/2 + \varepsilon_{\mathrm{anc}}) + G \cdot \Pr[(\Ecal^\star)^c]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Law of total expectation: split $\E[Y]$ over
the success event $\Ecal^\star$ and its complement. On $\Ecal^\star$,
$Y \le \gamma(Q)/2 + \varepsilon_{\mathrm{anc}}$; on the complement,
$Y \le G$ (Step 37). Bound each piece, drop $\Pr[\Ecal^\star] \le 1$
on the success term. Standard tail-to-expectation pattern for a bounded
random variable (no integration needed — the trivial case).
**Sub-agent task id:** none
**Last updated:** 2026-05-24T22:00:00Z

## Step 39
**Location:** sections/10-main-theorem.tex (corollary proof)
**Content (≤ 2 lines):** Substitution
$G \cdot \Pr[(\Ecal^\star)^c] \le 2 G \exp(-p_0 T/8)$ via
\Cref{thm:main_convergence_hp}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution:
$\Pr[(\Ecal^\star)^c] \le 2 \exp(-p_0 T/8)$ is the contrapositive of
\Cref{eq:test_time_scaling}; multiply through by
$G = M + \norm{V^*(Q)}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 40
**Location:** sections/10-main-theorem.tex (cor:entropy_decay proof, step i)
**Content (≤ 2 lines):** Softmax is 1-Lipschitz in $\ell_2$: Jacobian
$\mathrm{diag}(p) - p p^\top$ has operator norm $\le \max_i p_i(1-p_i) \le 1/4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches softmax-lipschitz.md digest. Reference:
Gao and Pavel arXiv:1704.00805 Prop 4. Hand-checked: $\mathrm{diag}(p) - p p^\top$
is symmetric PSD with eigenvalues in $[0, \max_i p_i] \subseteq [0, 1]$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 41
**Location:** sections/10-main-theorem.tex (cor:entropy_decay proof, step ii)
**Content (≤ 2 lines):** Shannon entropy $H(p) = -\sum p_i \log p_i$ is
Lipschitz on the image of softmax (bounded away from simplex boundary)
with finite constant $L_H$ depending on $|\mathcal V|$ and input bound.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches softmax-lipschitz.md digest. The image
of softmax with bounded input lies away from the simplex boundary
(softmax probability lower-bounded by $e^{-2R}/n$); entropy gradient is
bounded on this image. Standard textbook result.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 42
**Location:** sections/10-main-theorem.tex (cor:entropy_decay proof, step iii)
**Content (≤ 2 lines):** Linear map $x \mapsto W_U x$ is $B_U$-Lipschitz
in $\ell_2$ where $B_U = \norm{W_U}_{\mathrm{op}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of operator norm: $\norm{W_U x - W_U y} = \norm{W_U(x-y)} \le \norm{W_U}_{\mathrm{op}} \norm{x-y}$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 43
**Location:** sections/10-main-theorem.tex (cor:entropy_decay proof, step iv)
**Content (≤ 2 lines):** Composition: pointwise
$|H_T - H_\infty| \le L_{\mathrm{sm}} B_U \norm{x_T - V^*}$; take
expectations and substitute \Cref{cor:expected_error_scaling}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct composition of Lipschitz constants
(Steps 40-42). Linearity of expectation gives \Cref{eq:entropy_decay};
substituting the cor:expected_error_scaling bound gives \Cref{eq:entropy_decay_rate}.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 44
**Location:** sections/11-lower-bound.tex (thm:lower_bound proof, Step 1)
**Content (≤ 2 lines):** Hard instance construction:
$\mathcal V = \{a, a'\}$, $V(a) = V^*$, $V(a') = V^* + 2 v_\perp$,
i.i.d.\ Bernoulli($p_0$) emission policy.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct construction; no inference. All
parameters explicit and bounded.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 45
**Location:** sections/11-lower-bound.tex (thm:lower_bound proof, Step 2)
**Content (≤ 2 lines):** All five assumptions
(ass:anchor_set_accuracy, ass:anchor_emission_prob, ass:score_margin,
ass:bounded_value_norms, ass:decoding_existence) hold for the construction.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Each assumption checked explicitly in the
proof. Hand-checked against sections/02-assumptions.tex statements.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 46
**Location:** sections/11-lower-bound.tex (thm:lower_bound proof, Step 3)
**Content (≤ 2 lines):** $\Pr[\mathcal E^*] = (1-p_0)^T$ where $\mathcal E^*$
is the event of zero anchor emissions; on this event $x_T = V^* + 2 v_\perp$,
so $\norm{x_T - V^*} = 2 > \gamma(Q^*)$, decoding fails.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Independence of Bernoullis gives the product;
convex combination algebra (all $V_k = V(a') = V^* + 2 v_\perp$ implies
$x_T = V^* + 2 v_\perp$ by $\sum w = 1$); direct comparison
$2 > \gamma(Q^*) \in (0, 1)$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 47
**Location:** sections/11-lower-bound.tex (thm:lower_bound proof, Step 4)
**Content (≤ 2 lines):** $(1 - p_0)^T = \exp(-T \log(1/(1-p_0)))$ and
$\log(1/(1-p_0)) = p_0 + \mathcal{O}(p_0^2)$ for $p_0 \in (0, 1/2]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebraic identity (exponential of log).
Taylor expansion: $\log(1/(1-p_0)) = -\log(1-p_0) = p_0 + p_0^2/2 + \cdots$
gives the asymptotic; on $(0, 1/2]$, $p_0 \le \log(1/(1-p_0)) \le 2 p_0$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 48
**Location:** sections/12-variance-reduced.tex (thm:variance_reduced proof, Step 1)
**Content (≤ 2 lines):** $\Pr[\Ecal_1^c] \le \exp(-p_0 T/8)$ via
\Cref{lem:anchor_count_lb} at $\delta_1 = \exp(-p_0 T/8)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of lem:anchor_count_lb;
hypothesis $T \ge 8 \log(1/\delta_1)/p_0$ becomes $T \ge T$ (tautology).
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 49
**Location:** sections/12-variance-reduced.tex (thm:variance_reduced proof, Step 2)
**Content (≤ 2 lines):** Off-$\Ecal_1$ contribution
$\E[\norm{x_T-V^*}^2 \1_{\Ecal_1^c}] \le (M + \norm{V^*})^2 \Pr[\Ecal_1^c] \le (M + \norm{V^*})^2 \exp(-p_0 T/8)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Convex-combination bound $\norm{x_T} \le M$
(as in cor:expected_error_scaling), triangle to get $\norm{x_T - V^*} \le M + \norm{V^*}$;
square, take expectation over $\Ecal_1^c$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 50
**Location:** sections/12-variance-reduced.tex (thm:variance_reduced proof, Step 3 anchor part)
**Content (≤ 2 lines):** Under ass:anchor_unbiased + rem:anchor_internal_uniform
(anchor-internal score gap $\le \Delta'$),
$\E[\norm{S_A}^2 \mid \Ecal_1] \le \sigma^2 \sum_{k \in \Acal} w_{T,k}^2 \le 2 e^{\Delta'} \sigma^2/(p_0 T)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches variance-of-averaged-estimator.md
digest. Unbiasedness gives $\E[V_k - V^* \mid \text{anchor}, \mathcal F_{k-1}] = 0$;
conditional second moment bound gives variance $\le \sigma^2 \sum w^2$;
under anchor-internal uniformity ($\Delta'$-bounded score gap),
$\max_{k \in \Acal} w_{T,k} \le e^{\Delta'} / |\Acal^{\mathrm{traj}}_T| \le 2 e^{\Delta'}/(p_0 T)$ on $\Ecal_1$;
elementary $\sum w^2 \le \max_k w_k \cdot \sum w_k$ then gives the bound.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:58:00Z

## Step 51
**Location:** sections/12-variance-reduced.tex (thm:variance_reduced proof, Step 3 non-anchor part)
**Content (≤ 2 lines):** Non-anchor leakage on $\Ecal_1$: $\norm{S_N} \le (1 - \sum_{k \in \Acal} w_{T,k})(M + \norm{V^*}) \le (2/p_0) e^{-\Delta} (M + \norm{V^*}) \le \gamma(Q)/2$
under Delta-condition.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Same algebra as in lem:T_polynomial Step 3:
lem:anchor_mass_lb gives $1 - \sum w \le (2/p_0) e^{-\Delta}$ on $\Ecal_1$;
Delta-condition rearranges to $(2/p_0) e^{-\Delta} (M + \norm{V^*}) \le \gamma/2$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z

## Step 52
**Location:** sections/12-variance-reduced.tex (thm:variance_reduced proof, Step 4)
**Content (≤ 2 lines):** Combine via parallelogram inequality
$\norm{a+b}^2 \le 2\norm{a}^2 + 2\norm{b}^2$ and law of total expectation,
absorbing constants into the exponential term.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Parallelogram is standard (from Cauchy-Schwarz);
total expectation $\E[Y^2] = \E[Y^2 \1_{\Ecal_1}] + \E[Y^2 \1_{\Ecal_1^c}]$
combines the two contributions; Jensen converts $L^2$ to $L^1$.
**Sub-agent task id:** none
**Last updated:** 2026-05-24T23:55:00Z
