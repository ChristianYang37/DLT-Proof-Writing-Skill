# Softmax attention output and saturation behaviour

**Source.** Vaswani et al. (2017), *Attention Is All You Need*, §3.2.
For saturation analysis: Hahn (TACL 2020), *Theoretical Limitations of
Self-Attention*; Yun et al. (ICLR 2020), *Are Transformers universal
approximators of sequence-to-sequence functions?*; Sanford-Hsu-Telgarsky
(NeurIPS 2023), *Representational Strengths and Limitations of Transformers*.

**Setup.** For query $q \in \R^{d_k}$ and keys/values $\{(k_i, V_i)\}_{i=1}^n$,
single-head softmax attention computes
$$
   \mathrm{Attn}(q, K, V) = \sum_{i=1}^n \frac{e^{q^\top k_i / \sqrt{d_k}}}{\sum_{i'} e^{q^\top k_{i'} / \sqrt{d_k}}} \, V_i.
$$
The scale factor $\sqrt{d_k}$ is universally absorbed into $q^\top k_i$; we
drop it (write $\langle q,k_i\rangle$) without loss of generality.

**Key identity used in the proof.** With $s_j \coloneqq \sum_{i=1}^j e^{\langle q, k_i\rangle}$
the cumulative softmax denominator:
$$
   x_j \coloneqq \sum_{i=1}^j \frac{e^{\langle q,k_i\rangle}}{s_j} V_i,
   \qquad
   x_j = \frac{s_{j-1}}{s_j}\, x_{j-1} + \frac{e^{\langle q,k_j\rangle}}{s_j} V_j.
$$
This is the user's recurrence, with $\lambda_j = 1 - s_{j-1}/s_j$.

**Two regimes.**

1. **Sub-additive $s_j$ (bounded attention scores below).** If
   $\langle q, k_i\rangle \in [-B, B]$ for all $i$, then $s_j \ge j e^{-B}$,
   $s_j \le j e^B$, hence $s_{j-1}/s_j = 1 - \Theta(1/j)$. The weights
   $w_{j,i} = e^{\langle q,k_i\rangle}/s_j$ are all $\le e^{2B}/j$. This
   is the **uniform-spread regime** — softmax does not concentrate.

2. **Super-additive $s_j$ (a key dominates).** If some $i^*$ has
   $\langle q, k_{i^*}\rangle \gg \langle q, k_i\rangle$ for $i \ne i^*$,
   then $s_j$ is dominated by $e^{\langle q, k_{i^*}\rangle}$ for all $j \ge i^*$
   and $w_{j, i^*} \to 1$. Softmax saturates on $V_{i^*}$.

**For reasoning convergence: which regime?** The thinking-trajectory generates
keys $k_1, k_2, \ldots$ as the reasoning progresses. The convergence claim
needs that $x_j$ stabilises. Two failure modes:
- If a single early reasoning token $k_{i^*}$ dominates, $x_j \approx V_{i^*}$
  forever — convergence holds but to the *first dominant token's value*, not
  obviously a "correct answer."
- If no token dominates and scores are bounded in $[-B,B]$, weights spread as
  $\Theta(1/j)$ and $x_j$ is approximately a uniform average of $\{V_i\}$.
  Convergence holds iff $\bar V_j = (1/j)\sum_{i \le j} V_i$ has a limit.

**Connection to the "anchor set" idea.** The problem statement hints at
"behaviour on a small anchor set within a problem field" as a possible main
assumption. This translates naturally to:
- **Anchored-attention assumption:** for any question $Q$ in field $F$, there
  exists a set of "anchor tokens" $\{a_1, \ldots, a_m\}$ such that the model's
  trained value projection produces $V(a_l)$ close to a common target $V^*$
  (the "correct answer embedding"), and the trajectory eventually emits enough
  of these anchors that the softmax-weighted average converges to $V^*$.

**Hahn's impossibility result (TACL 2020) and its scope.** Hahn proves that
soft-attention transformers without positional encodings cannot recognise
certain regular languages (e.g. $\mathrm{Dyck}_1$) at fixed depth. The result
exhibits *one* failure mode of softmax attention on sequence-classification
tasks; it does **not** directly bound our setting (which is about a fixed
trained model's inference dynamics, not approximation/expressivity).

**Common misuses.**
- Treating softmax attention as a contractive map — it is contractive in $V$
  but not in $q, k$ jointly.
- Forgetting that attention scores can be negative (i.e. $q^\top k_i < 0$);
  but $e^{\langle q,k_i\rangle} > 0$ always, so softmax weights are positive.
- Conflating attention saturation with information loss — saturation is a
  property of weights, not values.

**Project citation key.** `\cite{vaswani2017attention}` for the architecture;
`\cite{hahn2020theoretical}` for the impossibility direction (cite only if
used for the discussion / related-work footnote).

**Recommendation for THIS proof.** Use the "anchored-attention" framing as
the central sellable assumption. The two regimes (uniform-spread vs.
single-dominant) are *both* compatible with convergence; the proof can
exploit either, but anchored-attention is the cleanest unifier — it requires
only that the value vectors at attended-to positions are eventually close to
a common $V^*$, regardless of how the weights spread.
