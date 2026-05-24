# Anchor-set decomposition — splitting the weighted average

**Source.** Folklore decomposition lemma in stochastic approximation and
in-context learning analyses; specific form below is standard.

**Statement (decomposition).** Let $w_{j,1},\ldots,w_{j,j}\ge 0$ with
$\sum_{k\le j}w_{j,k} = 1$, $V_1,\ldots,V_j \in \R^d$, and $V^* \in \R^d$.
For any subset $\mathcal A \subseteq \{1,\ldots,j\}$,
$$
   \Big\|\sum_{k\le j} w_{j,k} V_k - V^*\Big\|
   \;\le\;
   \underbrace{\sum_{k\in\mathcal A} w_{j,k} \|V_k - V^*\|}_{\text{anchor error}}
   \;+\;
   \underbrace{\Big(\sum_{k\notin\mathcal A} w_{j,k}\Big) \cdot D_j}_{\text{non-anchor leakage}},
$$
where $D_j \coloneqq \max_{k\le j}\|V_k - V^*\|$ is the worst-case deviation
(taken over all $k$, anchor or not).

**Proof.** Write $\sum_k w_{j,k}V_k - V^* = \sum_k w_{j,k}(V_k - V^*)$
(using $\sum w_{j,k} = 1$), split the index set at $\mathcal A$, apply triangle
and use $\|V_k - V^*\| \le D_j$ on the complement.

**Why it is the workhorse here.** The proof of the headline theorem will
choose $\mathcal A$ = "anchor positions" — the reasoning steps at which the
LLM emits a token from a designated anchor set within field $F$. Two
quantities then drive the bound:
1. **Anchor accuracy**: $\max_{k \in \mathcal A}\|V_k - V^*\|$ is small by
   assumption (the LLM's value projection on anchors is close to the answer
   embedding). Call this $\varepsilon_{\mathrm{anc}}$.
2. **Anchor mass**: $W_{\mathcal A}(j) \coloneqq \sum_{k\in\mathcal A}w_{j,k}$ is
   bounded below by some $\alpha_j \uparrow 1$. This is the convergence
   driver.

The bound becomes $\|x_j - V^*\| \le \varepsilon_{\mathrm{anc}} + (1 - \alpha_j) D$,
which converges to $\varepsilon_{\mathrm{anc}}$ as $j$ grows. If
$\varepsilon_{\mathrm{anc}} = 0$ exactly we get convergence to $V^*$; otherwise
to an $\varepsilon_{\mathrm{anc}}$-ball.

**Quantitative rates.**
- If $\alpha_j \ge 1 - C/j$, the bound is $\varepsilon_{\mathrm{anc}} + CD/j$,
  giving $\mathcal O(1/T)$ convergence to an $\varepsilon$-ball.
- If $\alpha_j \ge 1 - C/\sqrt j$ (e.g. via Azuma on a stochastic anchor
  policy), the rate is $\mathcal O(1/\sqrt T)$.

**Where the anchor mass comes from.** Two natural routes:

- **Combinatorial route.** Assume the reasoning policy emits an anchor at
  every step with probability $\ge p_0 > 0$ (independent of history). Then
  $|\mathcal A \cap [1,j]| \ge p_0 j / 2$ w.h.p. by Chernoff, and the softmax
  mass on $\mathcal A$ is at least $|\mathcal A| e^{-2B}/j$ when scores are
  in $[-B,B]$. Combining yields $W_{\mathcal A}(j) \ge (p_0/2) e^{-2B}$ — a
  *constant* lower bound, not a converging-to-1 one. Insufficient on its own.

- **Saturation route.** Assume the model's attention scores on anchors are
  uniformly higher than on non-anchors: there exists $\Delta > 0$ such that
  $\langle q, k_{\mathrm{anc}}\rangle - \langle q, k_{\mathrm{non}}\rangle \ge \Delta$
  for every anchor/non-anchor key pair. Then the softmax mass on anchors
  satisfies $W_{\mathcal A}(j) \ge 1 - e^{-\Delta} j_{\mathrm{non}}/j_{\mathrm{anc}}$
  which $\to 1$ if anchors are not vanishing in count. This route gives the
  cleanest convergence.

**The interplay.** A robust proof would assume **either** route as a sufficient
condition and let the reader pick whichever is empirically more defensible.
The headline assumption could combine them: "either anchors are emitted with
positive frequency AND attended-to with a positive margin, OR the value
projection is uniformly close to $V^*$ on the trajectory."

**Common misuses.**
- Treating $D_j$ as if bounded uniformly without justification (the value
  projection has finite Lipschitz norm but $D_j$ depends on the trajectory).
- Forgetting that $W_{\mathcal A}$ is random (depends on which tokens are
  emitted) and using it in a deterministic bound without conditioning.
- Cherry-picking $\mathcal A$ after seeing the trajectory — the assumption
  must specify $\mathcal A$ in a question-conditional but
  trajectory-independent way (e.g. "tokens of vocabulary class $V_F$").

**Project citation key.** No external key needed; this is a one-line bound.

**Recommendation for THIS proof.** Make the anchor-set decomposition the
central technical lemma. Phrase the main assumption around (i) value-projection
accuracy on anchors and (ii) anchor mass under softmax weighting.
