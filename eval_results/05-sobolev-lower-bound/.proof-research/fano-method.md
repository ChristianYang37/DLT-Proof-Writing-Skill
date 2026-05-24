# Local Fano method for minimax lower bounds

**Source.** Tsybakov, *Introduction to Nonparametric Estimation*, 2009, Theorem 2.5 (and its Corollary 2.6).

**Statement (form used here).** Suppose $\Theta$ is a parameter space with a semi-metric $d(\cdot,\cdot)$, and $\{P_\theta : \theta \in \Theta\}$ a corresponding family of probability measures on a sample space. Let $\theta_0, \theta_1, \ldots, \theta_M \in \Theta$ with $M \geq 2$, and assume:
- (i) $d(\theta_j, \theta_k) \geq 2 s > 0$ for all $0 \leq j < k \leq M$;
- (ii) $\frac{1}{M} \sum_{j=1}^M \mathrm{KL}(P_{\theta_j} \| P_{\theta_0}) \leq \alpha \log M$ with $0 < \alpha < 1/8$.

Then
\[
\inf_{\hat\theta} \sup_{\theta \in \Theta} P_\theta\bigl(d(\hat\theta, \theta) \geq s\bigr)
\;\geq\;
\frac{\sqrt{M}}{1 + \sqrt{M}} \left(1 - 2\alpha - \sqrt{\frac{2\alpha}{\log M}}\right) \;>\; 0,
\]
where the infimum is over all (measurable) estimators.

**Hypotheses.**
- $M \geq 2$.
- Pairwise separation $d(\theta_j, \theta_k) \geq 2s$. (Often stated as separation $\geq 2s$ so that the radius-$s$ balls are disjoint.)
- KL bound averaged from each $\theta_j$ to a reference $\theta_0$. Sometimes alternatively stated with pairwise KL.
- $\alpha < 1/8$ is the textbook threshold giving a non-trivial constant. Any $\alpha < 1/2$ works with worse constants.

**Constants and dimension dependence.** The lower bound constant is uniform: as $M \to \infty$, the prefactor approaches $1 - 2\alpha > 0$. For $\alpha \leq 1/16$ one gets the very clean form $\geq c_0$ for some universal $c_0 > 0$.

**Canonical use pattern.** Apply with $\theta_j = f_j$, semi-metric $d = \|\cdot\|_{L^2}$, $s = \rho$ chosen so that the bumps separate at $L^2$-distance $\geq 2\rho$, and verify the KL bound on $P_{f_j} = N(f_j(X), \sigma^2 I)$ products. Convert tail bound to risk via Markov: $\sup \E \|\hat f - f\|^2 \geq \rho^2 \cdot \inf \sup P(\|\hat f - f\| \geq \rho)$.

**Common misuses.**
- Using the KL bound with $\alpha \geq 1/8$ — the textbook constant fails.
- Misinterpreting the separation: $d(\theta_j,\theta_k) \geq 2s$, not $\geq s$. The radius-$s$ balls must be disjoint for the test-error reduction to work.
- Confusing Markov's inequality direction when converting probability lower bound to expectation lower bound.

**Project citation key.** \cite{tsybakov2009introduction}
