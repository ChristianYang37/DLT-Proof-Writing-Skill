# Symmetrization (ghost-sample argument)

**Source.** Boucheron-Lugosi-Massart, *Concentration Inequalities*, Ch. 11; Wainwright, *High-Dimensional Statistics*, Ch. 4; Vapnik 1998.

**Statement (expectation form).** Let $\mathcal{F} \subset \{f: \mathcal{X} \to [0,1]\}$. If $S = (Z_1, \ldots, Z_n)$ and $S' = (Z'_1, \ldots, Z'_n)$ are independent i.i.d. samples and $\varepsilon_1, \ldots, \varepsilon_n$ are independent Rademacher signs (also independent of $S, S'$), then
$$
\mathbb{E} \sup_{f \in \mathcal{F}} \bigl| \mathbb{E}_{\mathcal{D}} f - \tfrac{1}{n} \sum_{i=1}^n f(Z_i) \bigr|
\;\le\;
2 \, \mathbb{E} \sup_{f \in \mathcal{F}} \Bigl| \tfrac{1}{n} \sum_{i=1}^n \varepsilon_i f(Z_i) \Bigr|.
$$

**Tail form (the version we use).** For any $t > 0$,
$$
\Pr\!\left[ \sup_{f \in \mathcal{F}} | \mathbb{E} f - \widehat{\mathbb{E}}_n f | \ge t \right]
\;\le\;
2 \, \Pr\!\left[ \sup_{f \in \mathcal{F}} | \widehat{\mathbb{E}}_n f - \widehat{\mathbb{E}}'_n f | \ge t/2 \right],
$$
valid provided $n t^2 \ge 2$ (so $\sup |\widehat{\mathbb{E}}_n - \mathbb{E} f| \le 1/2$ holds for the relevant pair via Chebyshev). For losses in $[0,1]$, a clean statement: when $n \ge 2/t^2$,
$$
\Pr\!\left[ \sup_{f \in \mathcal{F}} | \mathbb{E} f - \widehat{\mathbb{E}}_n f | > t \right]
\;\le\;
2 \, \Pr\!\left[ \sup_{f \in \mathcal{F}} | \widehat{\mathbb{E}}_n f - \widehat{\mathbb{E}}'_n f | > t/2 \right].
$$

**Hypotheses.**
- $f$ takes values in $[0,1]$ (or bounded).
- $S, S'$ are independent samples of size $n$ from the same distribution.
- The supremum is over a class $\mathcal{F}$ that is countable or has a measurable suitability/separability (universal measurability suffices in practice; in proofs we assume measurability tacitly).

**Constants and dimension dependence.** Factor 2 in front; the $t \to t/2$ in the inner probability. The $n \ge 2/t^2$ side condition removes via Chebyshev on the ghost sample.

**Canonical use.** Given a class with VC-dim $d$, after symmetrization we apply Rademacher complexity bounds — the ghost-sample probabilities involve only $2n$ realized points, so the supremum effectively ranges over the projection $\mathcal{F}|_{S \cup S'}$ (a set of size $\le \Pi_{\mathcal{F}}(2n)$). This is the key reduction that brings the growth function into play.

**Common misuses.**
- Forgetting the $n \ge 2/t^2$ side condition (mild but needed for the cleanest constant 2).
- Applying to unbounded functions without checking moment conditions.
- Forgetting that the Rademacher variables are independent of $(S, S')$.

**Project citation key.** \cite{vapnik1998} or \cite{boucheronLugosiMassart2013}; we use the textbook version.
