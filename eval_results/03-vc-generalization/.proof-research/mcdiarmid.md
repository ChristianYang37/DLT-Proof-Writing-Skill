# McDiarmid's bounded-differences inequality

**Source.** McDiarmid 1989. Restated in Boucheron-Lugosi-Massart Ch. 6, Wainwright Ch. 3.

**Statement.** Let $Z_1, \ldots, Z_n$ be independent random variables with $Z_i \in \mathcal{Z}_i$, and let $g: \prod_i \mathcal{Z}_i \to \mathbb{R}$ satisfy the bounded-differences condition: for all $i$ and all $z_1, \ldots, z_n, z_i'$,
$$
\bigl| g(z_1, \ldots, z_i, \ldots, z_n) - g(z_1, \ldots, z_i', \ldots, z_n) \bigr| \;\le\; c_i.
$$
Then for any $t > 0$,
$$
\Pr\bigl[ g(Z) - \mathbb{E} g(Z) \ge t \bigr] \;\le\; \exp\!\left( - \frac{2 t^2}{\sum_{i=1}^n c_i^2} \right),
$$
and similarly for the lower tail. A two-sided bound costs an extra factor 2.

**Hypotheses.**
- $Z_1, \ldots, Z_n$ are independent (not necessarily identically distributed).
- $g$ satisfies bounded differences with constants $c_1, \ldots, c_n$.

**Constants.** The $2$ in the exponent's numerator is tight (Hoeffding's lemma).

**Canonical use for VC bound.** Apply to $g(S) := \sup_{h \in \mathcal{H}} |R(h) - \widehat{R}_n(h)|$. Changing one sample point $(x_i, y_i) \mapsto (x_i', y_i')$ changes $\widehat{R}_n(h) = \tfrac{1}{n} \sum_j \mathbf{1}[h(x_j) \ne y_j]$ by at most $1/n$ for each $h$, hence the supremum changes by at most $1/n$. So $c_i = 1/n$ and $\sum c_i^2 = 1/n$. McDiarmid then gives
$$
\Pr[ g(S) - \mathbb{E} g(S) \ge t ] \le \exp(-2 n t^2).
$$

**Common misuses.**
- Forgetting the independence requirement.
- Computing $c_i$ for the inner function instead of the supremum.
- Confusing bound on $g(S) - \mathbb{E} g(S)$ with bound on $g(S)$ itself.

**Project citation key.** \cite{mcdiarmid1989} or absorbed into textbook reference.
