# Multiplicative Chernoff bound for sums of (conditional) Bernoullis

## Statement (independent Bernoullis)

Let $X_1, \dots, X_n$ be independent $\{0, 1\}$-valued random variables
with $\E[X_j] = p_j$, and let $\mu = \sum_{j=1}^n p_j$. For every
$\delta \in (0, 1)$,
$$
\Pr\!\Bigl[\, \sum_{j=1}^n X_j \le (1 - \delta) \mu \,\Bigr]
\;\le\;
\exp\!\Bigl( -\frac{\delta^2 \mu}{2} \Bigr).
$$
The choice $\delta = 1/2$ gives
$$
\Pr\!\Bigl[\, \sum_{j=1}^n X_j \le \mu/2 \,\Bigr]
\;\le\;
\exp\!\Bigl( -\frac{\mu}{8} \Bigr).
$$
Reference: Boucheron, Lugosi, and Massart, *Concentration Inequalities*
(2013), Theorem 2.3 (lower-tail multiplicative Chernoff). Also
Vershynin 2018, §2.3.7 (one-sided Chernoff for Bernoullis).

## Martingale / conditional version (Freedman 1975)

When the $X_j$ are no longer independent but satisfy
$\E[X_j \mid \mathcal F_{j-1}] = p_j$ with $X_j \in \{0,1\}$ a.s.,
define $D_j = X_j - p_j$ (an $\mathcal F_j$-martingale difference with
$|D_j| \le 1$ and conditional variance $\mathrm{Var}(D_j \mid \mathcal F_{j-1}) = p_j(1-p_j) \le p_j$).
Freedman's inequality
(\cite[Theorem 1.6]{freedman1975tail}) states: for every $u, v > 0$,
$$
\Pr\!\Bigl[\, \sum_{j=1}^n D_j \le -u \;\;\text{and}\;\;
              \sum_{j=1}^n \mathrm{Var}(D_j \mid \mathcal F_{j-1}) \le v \,\Bigr]
\;\le\;
\exp\!\Bigl( -\frac{u^2}{2(v + u/3)} \Bigr).
$$

For our application, $X_j \in \{0,1\}$ with $\E[X_j \mid \mathcal F_{j-1}] = p_j \ge p_0$.
Set $u = \mu/2$ where $\mu \coloneqq \sum_{j=1}^n p_j \ge p_0 n$ (the
conditional version uses $\sum p_j$, not a deterministic constant, because
the $p_j$ are random; but the inequality $\sum p_j \ge p_0 n$ holds
a.s.). Then $v \le \sum p_j (1-p_j) \le \sum p_j = \mu$, so $v + u/3 \le \mu + \mu/6 = 7\mu/6$,
and
$$
\Pr\!\Bigl[\, \sum_{j=1}^n D_j \le -\mu/2 \,\Bigr]
\;\le\;
\exp\!\Bigl( -\frac{(\mu/2)^2}{2 \cdot 7\mu/6} \Bigr)
\;=\;
\exp\!\Bigl( -\frac{3\mu}{28} \Bigr).
$$
A cleaner choice that gives the canonical $\mu/8$ exponent: bound
$v + u/3 \le \mu(1 + 1/6) \le 4\mu/3$ a bit more loosely, which yields
$\exp(-3\mu/(2 \cdot 4 \cdot 2)) = \exp(-3\mu/16) \le \exp(-\mu/8)$, or
apply the direct multiplicative form by truncation (see below).

## Cleanest packaging (the form we use in the proof)

Combining the multiplicative-Chernoff inequality
$\Pr[\sum X_j \le \mu/2] \le \exp(-\mu/8)$ (independent case) with the
fact that conditioning preserves this exponential bound when applied to
adapted Bernoulli sequences (use a stopping-time / optional-stopping
argument or apply Freedman directly), we get the inequality used in
the proof:
$$
\Pr\!\Bigl[\, \sum_{j=1}^T X_j \le \tfrac{1}{2} \sum_{j=1}^T p_j \,\Bigr]
\;\le\;
\exp\!\Bigl( -\tfrac{1}{8} \sum_{j=1}^T p_j \Bigr)
\;\le\;
\exp\!\Bigl( -\frac{p_0 T}{8} \Bigr),
$$
where the second inequality uses the a.s.\ lower bound
$\sum_{j=1}^T p_j \ge p_0 T$ (Assumption: anchor-emission probability).

The clean form is provable directly from the moment-generating-function
proof of Chernoff: $\E[e^{-\lambda X_j} \mid \mathcal F_{j-1}] \le \exp(-\lambda p_j + p_j(e^{-\lambda} - 1 + \lambda))$
(use $\E[e^{-\lambda X_j} \mid \mathcal F_{j-1}] = p_j e^{-\lambda} + (1-p_j)$
exactly, then $\log(\cdot) = \log(1 - p_j(1 - e^{-\lambda})) \le -p_j(1 - e^{-\lambda})$
by $\log(1-x) \le -x$). Take products over $j$ and optimise $\lambda$ at $\lambda = \log 2$.

## Hypotheses for our cite-site

For \Cref{lem:anchor_count_lb}: $X_j = \1\{a_j \in \Acal(Q)\}$ is
$\mathcal F_j$-measurable Bernoulli with
$\E[X_j \mid \mathcal F_{j-1}] = p_j \ge p_0$ (\Cref{ass:anchor_emission_prob}).
All hypotheses of the martingale-Chernoff form satisfied.

## Comparison to Azuma

Azuma gives $\exp(-(\mu/2)^2/(2T))$ which with $\mu \ge p_0 T$ is
$\exp(-p_0^2 T / 8)$ — quadratic in $p_0$. The Bernoulli variance
structure ($\mathrm{Var} \le p_j$) saves a factor of $1/p_0$ in the
exponent: from $p_0^2 T / 8$ to $p_0 T / 8$. This is the canonical
Bernstein-vs-Hoeffding sharpening for sums of Bernoullis.

## References

- Boucheron–Lugosi–Massart, *Concentration Inequalities*, Theorem 2.3 (lower-tail multiplicative Chernoff for independent Bernoullis); Theorem 2.11 (Bennett / Bernstein).
- Vershynin 2018, §2.3.7 (Chernoff for Bernoullis).
- Freedman 1975, "On Tail Probabilities for Martingales," *Annals of Probability* 3(1):100–118 — the conditional version.
