# Confidence trace — Phase C.5 sweep

This trace enumerates every derivation step in the proofs of the
biased-SGD rewrite (sections 03-11) and tags each step with a confidence
level per the taxonomy of `references/confidence-sweep.md`. Old anchor-based
trace entries (anchor-decomposition, anchor-accuracy, anchor-count,
anchor-mass, T-polynomial, variance-reduced) are obsolete and have been
removed; their sections are deleted from the project as part of the
paper-scale rewrite.

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
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 2
**Location:** sections/03-lemma-softmax-running-average.tex:30
**Content (≤ 2 lines):** $s_j x_j = \sum_{k=1}^j e^{\inner{q}{k_k}} V_k$
by multiplying \Cref{eq:cumulative_softmax} through by $s_j$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebra. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 3
**Location:** sections/03-lemma-softmax-running-average.tex:32
**Content (≤ 2 lines):** Inductive step via $\sum_{k=1}^{j-1} = s_{j-1} x_{j-1}$
plus the new term $e^{\inner{q}{k_j}} V_j$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Inductive base ($s_0 x_0 = 0$) + step. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 4
**Location:** sections/03-lemma-softmax-running-average.tex:44
**Content (≤ 2 lines):** $\sum_k w_{j,k} = s_j/s_j = 1$ by substitution.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 5
**Location:** sections/04-lemma-gradient-form.tex:17 (Step 1 of lem:gradient_form)
**Content (≤ 2 lines):** $\log p(x)_v = (W_U x)_v - \log Z$ with
$Z = \sum_w e^{(W_U x)_w}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of softmax + log; standard.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 6
**Location:** sections/04-lemma-gradient-form.tex:23 (Step 1, gradient identity)
**Content (≤ 2 lines):** $\nabla_x \log p(x)_v = W_U^{(v)} - W_U^\top p(x)$
via chain rule on log-Z and the softmax identity
$\sum_w (e^{z_w}/Z) W_U^{(w)} = W_U^\top p(x)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard softmax-gradient derivation; matches
biased-sgd-descent-inequality.md and any textbook (e.g., Bishop §4.3).
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 7
**Location:** sections/04-lemma-gradient-form.tex:32 (Step 1, multiplication)
**Content (≤ 2 lines):** $\nabla_x p(x)_v = p(x)_v (W_U^{(v)} - W_U^\top p(x))$
via $\nabla p = p \cdot \nabla \log p$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: $p = e^{\log p}$ and $\nabla e^f = e^f \nabla f$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 8
**Location:** sections/04-lemma-gradient-form.tex:38 (Step 2, sum-of-gradients)
**Content (≤ 2 lines):** $\nabla \cmass(x; Q) = \sum_{v \in \Cset(Q)} \nabla p(x)_v
= W_U^\top \mathrm{diag}(\1_{\Cset(Q)}) p(x) - \cmass(x;Q) W_U^\top p(x)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute Step 7, collect linear-combination
sum-over-rows of $W_U$. Pull scalar factor
$\sum_{v \in \Cset(Q)} p(x)_v = \cmass(x;Q)$ out. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 9
**Location:** sections/04-lemma-gradient-form.tex:54 (Step 3, log derivative)
**Content (≤ 2 lines):** $\nabla \loss = -\nabla \cmass / \cmass$ via
chain rule on $\loss = -\log \cmass$, then divide Step 8 through by $\cmass$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard chain rule on logarithm; recognise
$W_U^\top \mathrm{diag}(\1_C) p / \cmass = W_U^\top \qcond$ by definition of $\qcond$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 10
**Location:** sections/05-lemma-smoothness.tex:25 (Step 1, $z$-space gradient)
**Content (≤ 2 lines):** $\nabla \ell(z) = p(z) - \qcond(z)$ at the
$|\mathcal V|$-dimensional level (replace $W_U$ by identity in Step 9).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Special case of \Cref{lem:gradient_form} with
unembedding = identity. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 11
**Location:** sections/05-lemma-smoothness.tex:33 (Step 1, softmax Jacobians)
**Content (≤ 2 lines):** $\nabla p = \mathrm{diag}(p) - p p^\top$ and
$\nabla \qcond = \mathrm{diag}(\qcond) - \qcond \qcond^\top$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard softmax-Jacobian identity (textbook;
e.g., Goodfellow-Bengio-Courville §6.2.2). Hand-checked: differentiate
$p_i = e^{z_i}/Z$ in $z_j$ → $\delta_{ij} p_i - p_i p_j$. Similarly $\qcond$
is itself the softmax of $z$ restricted to $\Cset$.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 12
**Location:** sections/05-lemma-smoothness.tex:43 (Step 1, Hessian of $\ell$)
**Content (≤ 2 lines):** $\nabla^2 \ell(z) = (\mathrm{diag}(p) - pp^\top) - (\mathrm{diag}(\qcond) - \qcond \qcond^\top)$
by combining Steps 10-11.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Difference of two softmax-Jacobians; direct
algebraic combination. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 13
**Location:** sections/05-lemma-smoothness.tex:55 (Step 2, op-norm bound on covariance)
**Content (≤ 2 lines):** $\norm{\mathrm{diag}(p) - p p^\top}_{\mathrm{op}}
\le \max_v p_v (1 - p_v) \le 1/4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Standard covariance-matrix op-norm bound; $p_v(1-p_v) \le 1/4$
by $t(1-t)$ maximised at $t=1/2$. Matches softmax-lipschitz.md digest.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 14
**Location:** sections/05-lemma-smoothness.tex:62 (Step 2, triangle for $\ell$)
**Content (≤ 2 lines):** $\norm{\nabla^2 \ell(z)}_{\mathrm{op}} \le 1/4 + 1/4 = 1/2$
by triangle on \Cref{eq:Hess_ell}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Triangle inequality applied to the difference of two PSD
matrices. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 15
**Location:** sections/05-lemma-smoothness.tex:69 (Step 3, chain rule)
**Content (≤ 2 lines):** $\nabla^2 \loss = W_U^\top \nabla^2 \ell W_U$ and
$\norm{\cdot} \le B_U^2 \cdot (1/2)$ via op-norm submultiplicativity.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard chain rule for second derivatives of $\ell \circ \text{linear}$.
Op-norm submultiplicativity. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 16
**Location:** sections/06-lemma-descent-inequality.tex:30 (Step 1, smoothness Taylor)
**Content (≤ 2 lines):** $\loss(x_j) \le \loss(x_{j-1}) + \inner{\nabla \loss(x_{j-1})}{g_j}
+ (L_{\mathrm{sm}}/2) \norm{g_j}^2$ pointwise by smoothness.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Standard $L$-smoothness second-order Taylor inequality;
matches biased-sgd-descent-inequality.md digest.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 17
**Location:** sections/06-lemma-descent-inequality.tex:43 (Step 2, conditional expectation)
**Content (≤ 2 lines):** Take $\E[\cdot \mid \mathcal F_{j-1}]$; substitute
\Cref{eq:gc_bb_def} and \Cref{eq:second_moment_def}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\mathcal F_{j-1}$-measurability of $\loss(x_{j-1})$
and $\nabla \loss(x_{j-1})$; substitution. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 18
**Location:** sections/06-lemma-descent-inequality.tex:57 (Step 3, Young's)
**Content (≤ 2 lines):** Young: $\inner{a}{b} \le (\eta_j/2) \norm{a}^2 + (1/(2\eta_j)) \norm{b}^2$;
then $\norm{b_j}^2 \le \eta_j^2 \beta^2$ gives $(1/(2\eta_j))\norm{b_j}^2 \le (\eta_j/2) \beta^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Young's inequality with $\alpha = \eta_j$; relative-scale
bound from \Cref{eq:gc_bb_bias}. Matches biased-sgd-descent-inequality.md
digest. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 19
**Location:** sections/06-lemma-descent-inequality.tex:79 (Step 4, combine)
**Content (≤ 2 lines):** Combine the gradient-norm terms:
$-\eta_j \norm{\nabla \loss}^2 + (\eta_j/2) \norm{\nabla \loss}^2 = -(\eta_j/2) \norm{\nabla \loss}^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebra. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 20
**Location:** sections/07-lemma-telescoping.tex:38 (Step 1, telescope)
**Content (≤ 2 lines):** Total-expectation sum of descent inequality
yields $\E[\loss(x_T)] - \loss(x_0) \le \sum$ on right side.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Tower property $\E[\E[\cdot \mid \F_{j-1}]] = \E[\cdot]$
and telescoping on $\loss(x_T)-\loss(x_0)$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 21
**Location:** sections/07-lemma-telescoping.tex:55 (Step 2, weighted-average)
**Content (≤ 2 lines):** $\min_j a_j \le (\sum_j \eta_j a_j)/(\sum_j \eta_j)$
for non-negative weights and values.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial: min is bounded above by weighted average
with non-negative weights summing to a positive quantity. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 22
**Location:** sections/07-lemma-telescoping.tex:74 (Step 3, step-size sums)
**Content (≤ 2 lines):** $\sum_{j=1}^T \eta_0/\sqrt j \ge \eta_0 \sqrt T$ by
integral comparison + algebra.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Integral comparison $\sum j^{-1/2} \ge \int_1^{T+1} x^{-1/2} dx
= 2(\sqrt{T+1} - 1) \ge \sqrt T$ for $T \ge 1$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 23
**Location:** sections/07-lemma-telescoping.tex:87 (Step 3, sum of squares)
**Content (≤ 2 lines):** $\sum_{j=1}^T \eta_0^2/j \le \eta_0^2 (1 + \log T)$ by
harmonic-series bound.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Harmonic-series upper bound $H_T \le 1 + \log T$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 24
**Location:** sections/07-lemma-telescoping.tex:93 (Step 4, substitution)
**Content (≤ 2 lines):** Substitute step-size sums; the bias term simplifies
to $\beta^2$ (cancellation of $\sum_j \eta_j$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebra: $\beta^2 \sum_j \eta_j / \sum_j \eta_j = \beta^2$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 25
**Location:** sections/08-lemma-logit-margin-decoding.tex:21 (Part (i))
**Content (≤ 2 lines):** $\loss(x;Q) \le \log 2 \Leftrightarrow \cmass(x;Q) \ge 1/2$
via monotone $t \mapsto e^{-t}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\loss = -\log \cmass$ and $e^{-\log 2} = 1/2$;
$e^{-t}$ strictly decreasing reverses the inequality. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 26
**Location:** sections/08-lemma-logit-margin-decoding.tex:30 (Part (ii), argmax preservation)
**Content (≤ 2 lines):** Softmax is strictly monotone, so argmax_v $p(x)_v$
coincides with argmax_v $(W_U x)_v$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $p(x) = e^{W_U x} / Z$ and exponential is strictly
increasing, so order is preserved. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 27
**Location:** sections/08-lemma-logit-margin-decoding.tex:38 (Part (ii), pigeonhole)
**Content (≤ 2 lines):** Non-degeneracy
$|\Cset(Q)| \max_{v \notin \Cset} p_v < \max_{v \in \Cset} p_v$ implies
$\max_{v \notin \Cset} p_v < \max_{v \in \Cset} p_v$ since $|\Cset(Q)| \ge 1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: $|C| \ge 1$ ⟹ $|C| \cdot a \ge a$ for $a \ge 0$.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 28
**Location:** sections/09-lemma-expectation-to-failure.tex:25 (Step 1, Markov)
**Content (≤ 2 lines):** Markov on non-negative $\loss(x_T;Q)$ at threshold $\log 2$
gives $\Pr[\loss > \log 2] \le \E[\loss]/\log 2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Markov's inequality, textbook (e.g., Vershynin 2018
Theorem 1.2.1). Non-negativity of $\loss$ from \Cref{rem:loss_nondegenerate}.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 29
**Location:** sections/09-lemma-expectation-to-failure.tex:34 (Step 2, contrapositive)
**Content (≤ 2 lines):** $\{\dec(x_T) \notin \Cset\} \subseteq \{\loss(x_T) > \log 2\}$
via contrapositive of \Cref{lem:logit_margin_decoding}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** \Cref{lem:logit_margin_decoding} states
$\{\loss \le \log 2\} \cap \{\text{non-degen}\} \Rightarrow \{\dec \in \Cset\}$;
contrapositive: $\{\dec \notin \Cset\} \Rightarrow \{\loss > \log 2\} \cup \{\text{degen}\}$;
under the assumed non-degeneracy this collapses to $\{\loss > \log 2\}$.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 30
**Location:** sections/10-main-theorem.tex:65 (Theorem proof, Step 1, gradient bound)
**Content (≤ 2 lines):** Direct invocation of \Cref{lem:telescoping}: hypotheses match.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Hypothesis check: thm uses same assumptions plus
$\eta_j = \eta_0/\sqrt j$ schedule, matches lemma exactly.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 31
**Location:** sections/10-main-theorem.tex:75 (Theorem proof, Step 2, loss bound rearrange)
**Content (≤ 2 lines):** From \Cref{eq:telescoping_summed}: drop non-negative
gradient-sum term, get $\E[\loss(x_T)] \le L_0 + (\beta^2/2)\sum\eta_j + (L_{\mathrm{sm}} G^2/2)\sum\eta_j^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct rearrangement of \Cref{eq:telescoping_summed},
dropping non-negative $\sum_j \eta_j \E\norm{\nabla \loss}^2 \ge 0$ on right side
(this preserves the upper bound direction since it adds positive quantity to RHS in
the rearranged form). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 32
**Location:** sections/10-main-theorem.tex:88 (Theorem proof, Step 2, time-averaging)
**Content (≤ 2 lines):** Time-averaging trick for $\E[\loss(\bar x_T)]$ or
$\E[\loss(x_R)]$ for random $R$ uniform on $\{1,\dots,T\}$ gives the
$O(L_0/\sqrt T) + O(\beta^2/\eta_0)$ form.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Standard biased-SGD averaging trick from
\cite{bottou2018optimization} §4.3, Theorem 4.10. Matches digest
biased-sgd-descent-inequality.md.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 33
**Location:** sections/10-main-theorem.tex:106 (Theorem proof, Step 3, Markov)
**Content (≤ 2 lines):** Invoke \Cref{lem:expectation_to_failure} with the
bound \Cref{eq:main_loss_bound}; divide by $\log 2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 34
**Location:** sections/10-main-theorem.tex:139 (cor:entropy_decay, Lipschitz softmax)
**Content (≤ 2 lines):** Softmax is 1-Lipschitz $\ell_2 \to \ell_2$
($\mathrm{diag}(p) - pp^\top$ has op-norm $\le \max p_i(1-p_i) \le 1/4 \le 1$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches softmax-lipschitz.md digest; reference Gao-Pavel
arXiv:1704.00805 Prop 4.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 35
**Location:** sections/10-main-theorem.tex:146 (cor:entropy_decay, entropy Lipschitz)
**Content (≤ 2 lines):** $H \circ \softmax$ on bounded inputs is Lipschitz
with finite constant $c_3$ depending on $|\mathcal V|, R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches softmax-lipschitz.md digest. Image of softmax
with $\norm{\mathbf z} \le R$ lies away from simplex boundary, where entropy
is gradient-bounded.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 36
**Location:** sections/10-main-theorem.tex:150 (cor:entropy_decay, composition)
**Content (≤ 2 lines):** Compose three Lipschitz constants:
$|H_T - H_\infty| \le c_3 \cdot B_U \cdot \norm{x_T - x^*(Q)}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Chain of Lipschitz constants on composition.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 37
**Location:** sections/10-main-theorem.tex:155 (cor:entropy_decay, loss-to-distance)
**Content (≤ 2 lines):** Under local strong-convexity,
$\norm{x_T - x^*(Q)} \le \sqrt{2(\loss(x_T) - \loss(x^*))/\mu}$; take expectations
and apply Jensen.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct algebra: $\loss(x) - \loss(x^*) \ge \mu \norm{x-x^*}^2/2$
inverts to $\norm{x-x^*} \le \sqrt{2(\loss(x)-\loss(x^*))/\mu}$. Jensen:
$\E\sqrt Y \le \sqrt{\E Y}$ for concave $\sqrt{\cdot}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 38
**Location:** sections/10-main-theorem.tex:210 (cor:pl_exponential_rate, descent at const step)
**Content (≤ 2 lines):** Per-step descent inequality at $\eta_j = \eta_0$ from
\Cref{lem:descent_inequality}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Specialise \Cref{eq:descent_inequality} to constant
$\eta_j = \eta_0$.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 39
**Location:** sections/10-main-theorem.tex:222 (cor:pl_exponential_rate, PL substitution)
**Content (≤ 2 lines):** Substitute PL: $\norm{\nabla \loss}^2 \ge 2\mu(\loss - L_*)$,
get $A_j \le (1-\eta_0 \mu) A_{j-1} + B$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches pl-condition-rate.md digest; standard
Karimi-Nutini-Schmidt 2016 argument.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 40
**Location:** sections/10-main-theorem.tex:236 (cor:pl_exponential_rate, iterate)
**Content (≤ 2 lines):** Iterate $A_T \le (1-\eta_0 \mu)^T A_0 + B/(\eta_0 \mu)$
via geometric-series sum.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Geometric series: $\sum_{j=0}^{T-1} (1-\eta_0 \mu)^j
\le 1/(\eta_0 \mu)$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 41
**Location:** sections/11-lower-bound.tex:55 (Step 1, instance construction)
**Content (≤ 2 lines):** $\mathcal V = \{v_1, v_2\}$ with $W_U^{(v_i)} = e_i$,
$\Cset = \{v_1\}$, $x_0 = 0$; bounded-norm constants computable.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct construction; all constants explicit.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 42
**Location:** sections/11-lower-bound.tex:68 (Step 2, orthogonal bias)
**Content (≤ 2 lines):** $g_j$ with $\E[g_j \mid \F_{j-1}] = -\eta_j \nabla\loss + \eta_j \beta u_j$
for $u_j \perp \nabla \loss$, saturating bound \Cref{eq:gc_bb_bias}.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: in $\R^{d \ge 2}$ orthogonal unit vector
always exists. Construction is valid; deterministic $g_j$ realises it
with zero conditional variance. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

## Step 43
**Location:** sections/11-lower-bound.tex:83 (Step 3, contradiction)
**Content (≤ 2 lines):** If $\min_j \E\norm{\nabla \loss}^2 < c_7 \beta^2$ then
bias variance dominates and $\loss$ increases back away from stationary point
at rate $\Theta(\eta_j^2 \beta^2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Standard biased-SGD lower-bound argument; matches
\cite{bottou2018optimization} §4.3 lower-bound discussion. The orthogonal-bias
construction is well-known in the bias-floor literature.
**Sub-agent task id:** none
**Last updated:** 2026-05-25T10:00:00Z

