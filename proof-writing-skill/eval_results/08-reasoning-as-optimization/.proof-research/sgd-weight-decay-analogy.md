# The "SGD with decreasing weight decay" framing — what it does and doesn't give us

**The claim from the problem statement.** The recurrence
$$
   x_j = (1 - \lambda_j) x_{j-1} + g_j, \qquad \lambda_j = 1 - s_{j-1}/s_j \in (0,1)
$$
is *structurally identical* to one step of SGD with $\ell_2$-weight-decay
coefficient $\lambda_j$ and gradient $g_j$.

**What is true.**
- The functional form $x_j = (1-\lambda_j) x_{j-1} + g_j$ is identical to the
  SGD-with-weight-decay update $x_j = (1-\eta_j \mu) x_{j-1} - \eta_j \hat g_j$
  with $\eta_j \hat g_j = -g_j$ and $\eta_j \mu = \lambda_j$. The algebra checks.
- $\lambda_j \in (0,1)$ since $s_j > s_{j-1} > 0$, matching standard weight-decay
  ranges.

**What is *not* automatically true.**
1. **There need be no objective $F$ such that $g_j$ is a (stochastic) gradient of
   $F$ at $x_{j-1}$.** SGD-as-an-algorithm presumes $g_j$ comes from a loss; the
   LLM's $g_j$ is whatever the trained projection produces. Calling something
   "SGD" is meaningless without specifying *of what*.
2. **The weight-decay coefficient $\lambda_j$ depends on the input data (the keys
   $k_1,\dots,k_j$), not on a pre-set schedule.** This is unusual for SGD where
   $\lambda_j$ would be exogenous. It is in fact closer to *adaptive-learning-
   rate* methods (Adam, RMSProp) where the effective step size depends on
   observed gradients.
3. **Decreasing-weight-decay is not in itself a convergence guarantee.** SGD
   with weight decay converges only under additional assumptions (smoothness
   of $F$, bounded variance of $g_j$, summability of $\sum_j \eta_j^2$, ...).
   Inheriting the *form* of the update does not inherit the *theorems*.

**Equivalent (algebraic, not framing) view.** Unrolling the recurrence with
$x_0 = 0$ and $g_j = e^{q^\top k_j} V_j / s_j$:
$$
   x_j = \frac{1}{s_j} \sum_{k=1}^j e^{q^\top k_k} V_k.
$$
This is the **standard softmax-attention output**. The "SGD with weight decay"
view is one way to *read* the recurrence; the running-softmax-average view is
another. Both are exact algebraic restatements. The convergence theorem
should be proved on whichever form makes the math cleanest — and the
softmax-average form is dramatically cleaner because **Toeplitz** applies
directly (see `toeplitz-silverman.md`).

**The deepest tension.** The user's problem statement frames the result as
"reasoning = optimization", which is appealing rhetorically but rests on the
gradient interpretation. We have two paths:

- **Path A — Optimization framing.** Postulate a potential $F$ such that
  $\E[g_j] \approx -\nabla F(x_{j-1})$. Use Robbins–Siegmund or PL to conclude.
  Sellability: high (matches the headline). Provability: low (the
  potential is postulated, not constructed).

- **Path B — Toeplitz framing.** Assume the value vectors along the
  trajectory have a limit (or "consistency target"). Use Toeplitz to conclude
  $x_j \to V^*$. Sellability: medium (the headline becomes "reasoning =
  weighted averaging toward a consistency target"; one has to defend this as
  a form of "implicit optimization"). Provability: high (the math is clean).

The problem statement explicitly notes "the most sellable main assumption is
one that is (i) empirically plausible, (ii) testable from inference-time
observations alone, (iii) just strong enough." Of the two paths, Path B
satisfies (ii) much more cleanly — value-vector consistency is something one
can sample at inference time. The "potential $F$" of Path A is not.

**Related work the proof must reckon with.**
- Schuurmans et al. (NeurIPS 2024), *Autoregressive Large Language Models are
  Computationally Universal* — establishes Turing-completeness; orthogonal to
  convergence claims.
- von Oswald et al. (2023), *Transformers learn in-context by gradient
  descent* — shows that a transformer **layer** can implement one step of
  gradient descent on a constructed objective. Different claim: their gradient
  is over a *constructed* in-context loss, ours would need to be over the
  reasoning objective. Useful precedent but not directly transferable.
- Akyürek et al. (ICLR 2023), *What learning algorithm is in-context
  learning?* — same family. Identifies linear regression in-context as
  GD on the in-context loss.

**None of these prior works prove $x_j$ converges to a "correct answer
embedding" for any reasoning task.** The closest result is the
in-context-learning theory, which constructs an objective and shows transformer
layers approximate gradient steps on it. Our setting is harder: the LLM is
fixed, the objective is not given.

**Bottom line for the proof.** Frame the result honestly: the "SGD with
weight decay" identification is exact at the level of update form, but the
convergence theorem rests on a *consistency* assumption on the value vectors,
not on a postulated potential. Be explicit about this in the assumption block.
