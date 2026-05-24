# Hoeffding's inequality (bounded-difference / sub-Gaussian sum)

**Source.** Boucheron, Lugosi, Massart — *Concentration Inequalities* (2013), Theorem 2.8. Also Vershynin, *High-Dimensional Probability* (2018), Theorem 2.2.6.

**Statement.** Let $X_1, \ldots, X_m$ be independent with $\E X_r = 0$ and $|X_r| \le b_r$ a.s. Then for all $t \ge 0$,
\[
\Pr\!\Big[\, \Big|\tfrac{1}{m}\sum_{r=1}^m X_r\Big| \ge t \,\Big] \;\le\; 2 \exp\!\Big( - \frac{m^2 t^2}{2 \sum_r b_r^2} \Big).
\]
In the equal-bound case $b_r = b$, this gives $2 \exp(-m t^2 / (2 b^2))$.

**Hypotheses.**
- $X_r$ independent (not just uncorrelated).
- Each bounded a.s. by $b_r$; mean zero.

**Constants and dimension dependence.** No dimension factor. Pure scalar.

**Canonical use pattern.** For each fixed pair $(i,j) \in [n]^2$, $\Hb_{ij}(0) - \E[\Hb_{ij}(0)]$ is a sum of $m$ independent bounded terms; apply Hoeffding to each entry, then union-bound over $n^2$ entries. Width condition: $m \gtrsim \log(n^2/\delta) / \varepsilon^2$ for entrywise accuracy $\varepsilon$.

**Common misuses.**
- Forgetting the factor of 2 (two-sided bound).
- Applying to non-independent variables.
- Conflating with sub-Gaussian Hoeffding (which uses $\|X_r\|_{\psi_2}^2$ rather than $b_r^2$, with different constants).

**Project citation key.** `\cite{boucheron2013concentration}` if textbook is cited; otherwise generic "Hoeffding's inequality" with no cite (a true textbook fact).
