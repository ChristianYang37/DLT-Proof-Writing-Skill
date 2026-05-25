# Dependency graph (post paper-scale rewrite)

The current graph reflects the **biased-SGD framework** instituted in
the rewrite of May 2026. The old anchor-based lemmas (anchor_decomposition,
anchor_accuracy_bound, anchor_count_lb, anchor_mass_lb, T_polynomial,
decoding_correctness) are obsolete and have been deleted from the
project; their .tex files are removed and their downstream consumers
have been re-routed to the new lemmas below.

## Headline result

### thm:main_convergence_biased_sgd
**Statement (1-line):** Under \Cref{ass:gradient_correctness_bounded_bias}
and four ancillary assumptions, with step size $\eta_j = \eta_0/\sqrt j$,
$\min_j \E\norm{\nabla \loss(x_j)}^2 \le 2 L_0/(\eta_0 \sqrt T) + \beta^2 + O(\log T/\sqrt T)$,
$\E[\loss(x_T)] \le c_1 L_0/\sqrt T + c_2 \beta^2/\eta_0$,
$\Pr[\dec(x_T) \notin \Cset(Q)] \le c_1 L_0/(\sqrt T \log 2) + c_2 \beta^2/(\eta_0 \log 2)$.
**Hypotheses:** ass:gradient_correctness_bounded_bias, ass:bounded_second_moment,
ass:bounded_value_norms, ass:unembedding_norm, ass:initial_loss.
**Downstream consumers:** (none — this is the theorem)
**Proof sketch:** Apply \Cref{lem:telescoping} for the gradient bound;
rearrange the telescoping for the loss bound; apply
\Cref{lem:expectation_to_failure} for the failure bound.

## Lemmas (topological order: leaves first)

### lem:softmax_running_average (SALVAGED from old graph, unchanged)
**Statement (1-line):** The recurrence
$x_j = (s_{j-1}/s_j) x_{j-1} + g_j$ unrolls to
$x_j = \sum_{k=1}^j w_{j,k} V_k$ with $w_{j,k} = e^{\inner{q}{k_k}}/s_j$
and $\sum w_{j,k} = 1$, $w_{j,k} \ge 0$.
**Hypotheses:** Definitions only.
**Downstream consumers:** lem:descent_inequality (uses $x_j = x_{j-1} + g_j$ form),
thm:lower_bound (uses convex-combination identity in instance bound check).
**Proof:** induction on $j$; algebraic.

### lem:gradient_form (NEW)
**Statement (1-line):** $\nabla \loss(x; Q) = W_U^\top (p(x) - \qcond(x; Q))$.
**Hypotheses:** Definitions only (no probability).
**Downstream consumers:** lem:smoothness (Hessian computation chain rule),
lem:descent_inequality (substitution in smoothness step).
**Proof:** Standard softmax-gradient + chain rule on $\loss = -\log \cmass$, 3 steps.

### lem:smoothness (NEW)
**Statement (1-line):** $\loss(\cdot; Q)$ is $L_{\mathrm{sm}}$-smooth with
$L_{\mathrm{sm}} \le (1/2) B_U^2$.
**Hypotheses:** ass:unembedding_norm.
**Downstream consumers:** lem:descent_inequality (smoothness expansion step),
thm:main_convergence_biased_sgd (constants).
**Proof:** Hessian computation in $z = W_U x$ + chain rule + op-norm bound on
covariance matrices.

### lem:descent_inequality (NEW — biased-SGD descent)
**Statement (1-line):** Under
\Cref{ass:gradient_correctness_bounded_bias,ass:bounded_second_moment,ass:unembedding_norm},
$\E[\loss(x_j) \mid \F_{j-1}] \le \loss(x_{j-1}) - (\eta_j/2) \norm{\nabla \loss(x_{j-1})}^2
+ (\eta_j/2) \beta^2 + (L_{\mathrm{sm}}/2) \eta_j^2 G^2$.
**Hypotheses:** ass:gradient_correctness_bounded_bias, ass:bounded_second_moment,
ass:unembedding_norm (for $L_{\mathrm{sm}}$ from lem:smoothness).
**Downstream consumers:** lem:telescoping, cor:pl_exponential_rate
(at constant step $\eta_j = \eta_0$), thm:lower_bound (in the
contradiction argument).
**Proof:** Standard biased-SGD descent (Bottou-Curtis-Nocedal 2018 §4.3 eq.~(4.10)).
4 steps: smoothness Taylor, conditional expectation, Young's, combine.

### lem:telescoping (NEW)
**Statement (1-line):** Under hypotheses of lem:descent_inequality + ass:initial_loss,
with $\eta_j = \eta_0/\sqrt j$, $\min_j \E\norm{\nabla \loss(x_j)}^2 \le 2L_0/(\eta_0\sqrt T) + \beta^2 + O(\log T/\sqrt T)$.
**Hypotheses:** lem:descent_inequality + ass:initial_loss + diminishing-step schedule.
**Downstream consumers:** thm:main_convergence_biased_sgd.
**Proof:** Telescope, weighted-average extraction, step-size sum evaluation.

### lem:logit_margin_decoding (NEW — replaces old lem:decoding_correctness)
**Statement (1-line):** If $\loss(x; Q) \le \log 2$ then $\cmass(x; Q) \ge 1/2$;
and if additionally $|\Cset(Q)| \max_{v \notin \Cset(Q)} p(x)_v < \max_{v \in \Cset(Q)} p(x)_v$,
then $\dec(x) \in \Cset(Q)$.
**Hypotheses:** Definitions only.
**Downstream consumers:** lem:expectation_to_failure (in contrapositive form).
**Proof:** Direct: log of $1/2$; argmax preservation under softmax.

### lem:expectation_to_failure (NEW — Markov)
**Statement (1-line):** $\Pr[\loss(x_T; Q) > \log 2] \le \E[\loss(x_T; Q)] / \log 2$;
combined with lem:logit_margin_decoding gives
$\Pr[\dec(x_T) \notin \Cset(Q)] \le \E[\loss(x_T;Q)]/\log 2$.
**Hypotheses:** $\loss \ge 0$ (from rem:loss_nondegenerate) + lem:logit_margin_decoding.
**Downstream consumers:** thm:main_convergence_biased_sgd (failure-probability form).
**Proof:** Markov's inequality on non-negative $\loss(x_T)$.

## Lower bound + corollaries

### thm:lower_bound (NEW — floor tightness)
**Statement (1-line):** For every $(\eta_0, \beta)$, there is an instance
with $\liminf_T \min_j \E\norm{\nabla \loss(x_j; Q^*)}^2 \ge c_7 \beta^2$.
**Hypotheses:** the framework's assumptions (constructed to hold).
**Downstream consumers:** (none — supplementary tightness result)
**Proof:** Orthogonal-bias construction + contradiction argument with
descent inequality.

### cor:entropy_decay (NEW restatement — replaces old version)
**Statement (1-line):** $|H_T - H_\infty(Q)| \le c_3 B_U \norm{x_T - x^*(Q)}$
pointwise; expected version inherits the loss bound's rate.
**Hypotheses:** thm:main_convergence_biased_sgd's assumptions.
**Downstream consumers:** (none — supplementary empirical-link statement)
**Proof:** Lipschitz composition (softmax + entropy + linear $W_U$); 4 steps.

### cor:pl_exponential_rate (NEW)
**Statement (1-line):** Under additional PL inequality on the trajectory,
$\E[\loss(x_T) - L_*(Q)] \le (1-c_5 \eta_0 \mu)^T (L_0-L_*(Q)) + c_6 \beta^2/(\eta_0 \mu)$
with constant step $\eta_j = \eta_0$.
**Hypotheses:** thm:main_convergence_biased_sgd's assumptions + PL inequality.
**Downstream consumers:** (none — supplementary empirically-relevant rate)
**Proof:** Standard biased-SGD-under-PL (Karimi-Nutini-Schmidt 2016).

## Total surviving nodes

- **Assumptions:** ass:gradient_correctness_bounded_bias,
  ass:bounded_second_moment, ass:bounded_value_norms, ass:unembedding_norm,
  ass:initial_loss, ass:logit_margin_nondegen (6 main; the last added in
  review iteration 6 to make the failure-probability bridge fully
  self-contained).
- **Lemmas (7):** softmax_running_average (salvaged); gradient_form, smoothness,
  descent_inequality, telescoping, logit_margin_decoding,
  expectation_to_failure (6 new).
- **Theorems (2):** thm:main_convergence_biased_sgd (headline);
  thm:lower_bound (tight floor).
- **Corollaries (2):** cor:entropy_decay (next-token entropy, links to
  Choi 2025); cor:pl_exponential_rate (PL strengthening, empirically
  relevant at $T \le 10^5$).

Tree depth: 3 (preliminaries → leaves [grad_form, smoothness, log_margin] →
[descent_ineq, telescoping, exp_to_failure] → headline). Occam pass:
every lemma is consumed by the headline theorem or by a corollary.

## Old (obsolete) lemmas — DROPPED

- lem:anchor_decomposition — DROPPED (was sections/04, deleted)
- lem:anchor_accuracy_bound — DROPPED (was sections/05, deleted)
- lem:anchor_count_lb — DROPPED (was sections/06, deleted)
- lem:anchor_mass_lb — DROPPED (was sections/07, deleted)
- lem:T_polynomial — DROPPED (was sections/08, deleted)
- lem:decoding_correctness — REPLACED by lem:logit_margin_decoding (was sections/09)
- thm:variance_reduced — DROPPED (was sections/12, deleted; revisit in revision)
- sgd-aside — DROPPED (was sections/99, deleted)
- ass:anchor_set_accuracy, ass:anchor_emission_prob, ass:score_margin,
  ass:decoding_existence — DROPPED (replaced by the five new assumptions
  in sections/02-assumptions.tex)
