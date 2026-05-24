# Dependency graph

**Provisional — pending user approval of main-assumption choice (Phase A.5
decision list). The graph below is the structure consistent with the
**recommended Option B (anchored-attention via Toeplitz)**. Alternatives
in Options A and C are sketched at the bottom.**

## Headline result

### thm:main_convergence
**Statement (1-line):** Under the question-field assumptions
\Cref{ass:anchor_set_accuracy}, \Cref{ass:anchor_mass_growth}, and the
decoding margin \Cref{ass:decoding_margin}, for every $Q \in F$ the latent
trajectory $\{x_{i,h,j}\}$ at the (`</think>`) position satisfies
$\|x_{i,h,j} - V^*(Q)\| \le \varepsilon$ for all $j \ge T(\varepsilon)$ with
$T(\varepsilon) = \poly(1/\varepsilon, \text{problem params})$, and
$\mathrm{decode}(x_{i,h,j})$ outputs the correct answer for $j \ge T$.
**Hypotheses:** ass:anchor_set_accuracy, ass:anchor_mass_growth,
ass:decoding_margin, ass:bounded_value_norms.
**Downstream consumers:** (none — this is the theorem)
**Proof sketch:** Decompose $x_j - V^*$ via \Cref{lem:anchor_decomposition};
bound the anchor error by \Cref{lem:anchor_accuracy_bound}; bound the
non-anchor leakage by \Cref{lem:anchor_mass_lb}; combine to get rate
$\varepsilon(j) \to 0$; choose $j \ge T$ to fall inside the decoding-margin
ball via \Cref{lem:decoding_correctness}.

## Lemmas (topological order: leaves first)

### lem:softmax_running_average_identity
**Statement (1-line):** The user's recurrence $x_j = (s_{j-1}/s_j)x_{j-1} + g_j$
unrolls to $x_j = \sum_{k=1}^j w_{j,k} V_k$ with $w_{j,k} = e^{\langle q,k_k\rangle}/s_j$
and $\sum_k w_{j,k} = 1$, $w_{j,k} \ge 0$.
**Hypotheses:** the recurrence form (no extra assumption).
**Downstream consumers:** lem:anchor_decomposition (cite-site step 1),
                          thm:main_convergence (cite-site §step 1 of proof),
                          remark on the SGD framing (cite-site).
**Proof:** induction on $j$; algebraic.

### lem:anchor_decomposition
**Statement (1-line):** For any subset $\mathcal A \subseteq [j]$,
$\|\sum_k w_{j,k} V_k - V^*\| \le \sum_{k\in\mathcal A} w_{j,k}\|V_k-V^*\|
+ (1-\sum_{k\in\mathcal A}w_{j,k})\cdot D_j$, with $D_j = \max_k\|V_k-V^*\|$.
**Hypotheses:** convex weights ($w \ge 0$, $\sum w = 1$).
**Downstream consumers:** thm:main_convergence (cite-site §step 2 of proof),
                          lem:anchor_accuracy_bound (consumed implicitly).
**Proof:** triangle + convex-combination algebra.

### lem:anchor_accuracy_bound
**Statement (1-line):** Under \Cref{ass:anchor_set_accuracy}, for every
$k \in \mathcal A(Q)$, $\|V_k - V^*(Q)\| \le \varepsilon_{\mathrm{anc}}$.
**Hypotheses:** ass:anchor_set_accuracy.
**Downstream consumers:** thm:main_convergence (cite-site §step 3 of proof).
**Proof:** unpack the assumption; a 2-line restatement with explicit
question-conditional quantifiers.

### lem:anchor_mass_lb
**Statement (1-line):** Under \Cref{ass:anchor_mass_growth} (and
ass:bounded_value_norms), $\sum_{k\in\mathcal A(Q) \cap [j]} w_{j,k}
\ge 1 - C \cdot \rho^j$ (geometric saturation) OR $\ge 1 - C/j^\alpha$
(polynomial route) for explicit constants.
**Hypotheses:** ass:anchor_mass_growth, ass:bounded_value_norms.
**Downstream consumers:** thm:main_convergence (cite-site §step 4 of proof).
**Proof:** softmax algebra on the score-margin assumption + standard
geometric-series / averaging bound.

### lem:decoding_correctness
**Statement (1-line):** Under \Cref{ass:decoding_margin}, if
$\|x - V^*(Q)\| \le \gamma(Q)$ then $\mathrm{decode}(x)$ outputs the
correct answer for $Q$.
**Hypotheses:** ass:decoding_margin.
**Downstream consumers:** thm:main_convergence (cite-site §step 5 of proof).
**Proof:** direct unpacking of the assumption (decoding is a black-box
deterministic map; assumption gives the margin).

### lem:T_polynomial
**Statement (1-line):** Combining \Cref{lem:anchor_decomposition,lem:anchor_accuracy_bound,lem:anchor_mass_lb},
$\|x_j - V^*(Q)\| \le \varepsilon_{\mathrm{anc}} + C D_{\max} \rho^j$ (or
$\le \varepsilon_{\mathrm{anc}} + CD_{\max}/j^\alpha$); the horizon needed
to reach the decoding margin $\gamma$ is $T = \poly(1/\gamma, 1/(1-\rho),
D_{\max}, \log(1/\gamma))$.
**Hypotheses:** ass:anchor_set_accuracy, ass:anchor_mass_growth,
ass:bounded_value_norms, plus $\varepsilon_{\mathrm{anc}} \le \gamma/2$.
**Downstream consumers:** thm:main_convergence (cite-site §step 6 of proof).
**Proof:** invert the rate from \Cref{lem:anchor_mass_lb}.

## Total surviving nodes

- **Assumptions:** ass:anchor_set_accuracy, ass:anchor_emission_prob,
  ass:score_margin, ass:bounded_value_norms, ass:decoding_existence (5 main);
  ass:anchor_unbiased (local to §12).
- **Lemmas:** softmax_running_average_identity, anchor_decomposition,
  anchor_accuracy_bound, anchor_count_lb (Chernoff/Freedman), anchor_mass_lb,
  T_polynomial, decoding_correctness (7 total).
- **Theorem:** thm:main_convergence_hp (1 headline); plus
  thm:lower_bound (matching lower bound, §11) and thm:variance_reduced
  (accuracy-scaling, §12).
- **Corollaries:** cor:expected_error_scaling, cor:entropy_decay
  (entropy bound, links to Choi 2025).

Tree depth: 2 (leaves → headline). Occam pass: every lemma is consumed by
thm:main_convergence_hp or by another theorem (thm:lower_bound consumes
softmax_running_average_identity via the construction;
thm:variance_reduced consumes anchor_count_lb, anchor_mass_lb,
softmax_running_average_identity).

## Alternative graphs for Options A and C (deferred)

- **Option A — postulated potential + PL:** replaces lem:anchor_mass_lb
  with a lem:descent_lemma (one-step decrease of $F(x_j)$) and lem:PL_rate
  (linear rate). Adds Robbins-Siegmund / PL citation digests.
- **Option C — stochastic / a.s. mode:** wraps the proof in a probability
  space over the reasoning policy; adds lem:azuma_anchor_count
  for high-probability anchor frequency. Adds a $1-\delta$ probability
  parameter to thm:main_convergence.

These alternatives share lem:softmax_running_average_identity,
lem:anchor_decomposition, lem:decoding_correctness, and lem:T_polynomial
unchanged; only the "anchor mass" route differs.
