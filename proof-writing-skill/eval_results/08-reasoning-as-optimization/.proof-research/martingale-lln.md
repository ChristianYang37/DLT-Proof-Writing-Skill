# Martingale strong / weak laws and Azuma–Hoeffding

**Source.** Hall–Heyde, *Martingale Limit Theory and Its Applications*
(Academic Press, 1980); for the simple form needed here, Durrett,
*Probability: Theory and Examples* (5th ed., 2019), §4.4 and §5.2.

**Setup.** Let $(\mathcal F_j)$ be a filtration on a probability space, $V_j$
a $\mathcal F_j$-adapted sequence in $\R^d$ with $\|V_j\|\le M$. Define
the conditional means $\mu_j \coloneqq \E[V_j \mid \mathcal F_{j-1}]$.

**Strong-LLN-type statement (Durrett Thm 4.4.7 / Chow's LLN).** If
$\sum_j \|\mu_j\|^2/j^2 < \infty$ (deterministic) and $V_j$ are uniformly
bounded, then $\bar V_n - \bar\mu_n \to 0$ a.s., where $\bar V_n = (1/n) \sum_{j\le n} V_j$
and $\bar\mu_n = (1/n)\sum_{j \le n}\mu_j$.

**Azuma–Hoeffding (Durrett Thm 5.2.6).** Let $(M_j)$ be a martingale with
$|M_j - M_{j-1}|\le c_j$ a.s. Then for any $t > 0$,
$$
   \Pr\big[|M_n - M_0|\ge t\big] \;\le\; 2 \exp\!\Big(-\frac{t^2}{2 \sum_{j=1}^n c_j^2}\Big).
$$

**Why it might be relevant here.** If we model the value vectors $V_j$ along
the reasoning trajectory as random (treating the generated tokens as draws
under the LLM's own distribution, conditioned on the question $Q$), then
$\bar V_j$ has a martingale-difference decomposition and Azuma applies. This
delivers a high-probability $\mathcal O(1/\sqrt j)$ convergence rate around
the conditional mean trajectory.

**Caveats for the softmax-weighted case.**
- Softmax weights $w_{j,k} = e^{\langle q,k_k\rangle}/s_j$ are **random** (depend
  on the generated keys), so the weighted sum $x_j = \sum_k w_{j,k} V_k$ is
  not a simple martingale. One must condition on $\sigma(k_1,\ldots,k_j)$
  before applying martingale concentration.
- Boundedness of $V_j$ holds (the value projection has finite
  Lipschitz constant times bounded inputs); $M$ depends on weights and norms.

**Common misuses.**
- Applying Azuma to non-martingale partial sums.
- Forgetting the bounded-difference hypothesis (Azuma fails for unbounded
  differences without sub-Gaussian assumption).
- Using strong-LLN forms (a.s.) when only weak-LLN (in probability) is needed,
  resulting in stronger hypotheses than necessary.

**Project citation key.** `\cite{durrett2019probability}` if cited at all.
Often the LLN result is cited as folklore.

**Decision for THIS proof.** Probably **not used as primary tool**. The
deterministic Toeplitz route is cleaner. We may invoke this if the proof
adopts a stochastic mode of convergence (e.g. in-expectation or
high-probability rates).
