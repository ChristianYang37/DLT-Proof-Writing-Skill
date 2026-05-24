# Robbins–Siegmund supermartingale convergence

**Source.** Robbins & Siegmund, *A convergence theorem for non-negative almost
supermartingales and some applications*, in Rustagi (ed.), *Optimizing Methods
in Statistics* (Academic Press, 1971), pp. 233–257. Widely used in stochastic
approximation; clean modern statement in Bertsekas–Tsitsiklis,
*Neuro-Dynamic Programming* (1996), Prop. 4.2, or in Polyak,
*Introduction to Optimization* (1987), Lemma 2.2.10.

**Statement.** Let $(V_t), (b_t), (c_t), (d_t)$ be non-negative, $\mathcal F_t$-adapted
sequences on a probability space, with
$$
   \E[V_{t+1} \mid \mathcal F_t] \;\le\; (1 + b_t) V_t + c_t - d_t \qquad \text{a.s.}
$$
If $\sum_t b_t < \infty$ and $\sum_t c_t < \infty$ almost surely, then with
probability one:
1. $V_t \to V_\infty \ge 0$ (limit exists, finite);
2. $\sum_t d_t < \infty$.

**Hypotheses (verbatim).**
- $V_t \ge 0$ and $\mathcal F_t$-measurable.
- $b_t, c_t, d_t \ge 0$ and $\mathcal F_t$-measurable.
- $\sum b_t, \sum c_t < \infty$ a.s. (almost-sure summability of the *positive* drift terms).
- The decomposition inequality holds a.s.

**Why this matters here.** If one wanted to lean on the "$g_j$ is a stochastic
gradient" framing — i.e. $g_j$ is an unbiased estimate of $\nabla F(x_{j-1})$
under some explicit potential $F$ — then Robbins–Siegmund applied to
$V_j \coloneqq F(x_j)$ delivers $F(x_j) \to F_\infty$ a.s. and
$\sum_j \langle \nabla F(x_{j-1}), \E[g_j \mid \mathcal F_{j-1}]\rangle < \infty$,
from which (under PL-condition) $F(x_j) \to \min F$.

**Critical caveat for THIS project.** The hypothesis that $g_j$ is an unbiased
gradient estimator is **the load-bearing fragility** of the SGD framing. There
is no a-priori potential $F$ such that the LLM's $g_j$ is its stochastic
gradient — the LLM was trained by a different loss, and the inference-time
dynamics are not gradient descent on any objective unless we *postulate* one
post-hoc. Two ways to handle this:

1. **Postulate a potential:** assume the existence of a smooth $F$ such that
   $\E[g_j \mid \mathcal F_{j-1}] = -\nabla F(x_{j-1}) + \text{bias}_j$ with
   controlled bias. Then Robbins–Siegmund applies but the assumption is
   strongly non-sellable (the practitioner has no way to verify a postulated
   $F$ from inference observations).

2. **Sidestep the SGD framing entirely:** prove convergence of the weighted
   running average via Toeplitz (see `toeplitz-silverman.md`), assuming
   value-vector convergence directly. This is much more sellable but the
   "reasoning = optimization" headline becomes a *reframing* rather than a
   theorem about an objective.

**Common misuses.**
- Treating the bias term as zero without justification (the LLM's value
  projection is not unbiased w.r.t. any natural objective).
- Forgetting the a.s. nature of summability (deterministic summability is a
  much stronger condition).
- Conflating Robbins–Siegmund's $V_t \to V_\infty$ with $V_\infty = \min F$;
  the limit value depends on the trajectory and the initial point. To get
  $V_\infty = \min$ one needs additional structure (PL, convexity, ...).

**Project citation key.** `\cite{robbins1971convergence}` (Robbins-Siegmund
1971) if used. Most analysis using this result also cites Bertsekas-Tsitsiklis
`\cite{bertsekas1996neurodynamic}` for the standard form.

**Recommendation for THIS proof.** Prefer the Toeplitz route as the primary
backbone; cite Robbins–Siegmund only if a probabilistic / a.s. mode of
convergence is explicitly required *and* a clean potential is available.
