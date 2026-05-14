# Massart's finite-class lemma

**Source.** Massart 2000; restated as Lemma 5.2 of Massart's *St-Flour Lectures*, and as Lemma 4.14 of Wainwright *High-Dimensional Statistics*. Also appears in Boucheron-Lugosi-Massart Ch. 13.

**Statement.** Let $A \subset \mathbb{R}^n$ be a finite set, $N = |A|$, and let $\varepsilon_1, \ldots, \varepsilon_n$ be i.i.d. Rademacher. Define $R := \max_{a \in A} \|a\|_2$. Then
$$
\mathbb{E} \max_{a \in A} \tfrac{1}{n} \sum_{i=1}^n \varepsilon_i a_i
\;\le\;
\frac{R \sqrt{2 \log N}}{n}.
$$

For the absolute-value variant (which we need),
$$
\mathbb{E} \max_{a \in A} \Bigl| \tfrac{1}{n} \sum_{i=1}^n \varepsilon_i a_i \Bigr|
\;\le\;
\frac{R \sqrt{2 \log(2N)}}{n}.
$$
(Replace $A$ by $A \cup (-A)$ to reduce $|\cdot|$ to plain max; this doubles the set.)

**Hypotheses.**
- $A$ is finite.
- $\varepsilon_i$ are i.i.d. Rademacher, independent of any other randomness.
- Vectors $a \in A$ are deterministic (or conditioned on); the bound is on expectation over $\varepsilon$ only.

**Constants and dimension dependence.** Tight constant $\sqrt{2}$; the bound is by union-bound over sub-Gaussian tails: each $\sum_i \varepsilon_i a_i / n$ is mean-zero sub-Gaussian with parameter $\|a\|_2 / n$, then $\mathbb{E} \max \le \sqrt{2 \sigma^2 \log N}$.

**Canonical use.**
```
By Massart's lemma applied to the finite class \mathcal{H}|_{S \cup S'} with
ambient vectors in \{0,1\}^{2n} (norm \le \sqrt{2n}):
\mathbb{E} \sup_h \tfrac{1}{n} \sum_i \varepsilon_i h(z_i) \le \sqrt{2n} \cdot \sqrt{2 \log N} / n
                                                                = \sqrt{4 \log N / n}.
```

**Common misuses.**
- Using $\sqrt{\log N}$ instead of $\sqrt{2 \log N}$ (off by $\sqrt{2}$).
- Forgetting the absolute-value doubling: $|\cdot|$ requires $\log(2N)$, not $\log N$.
- Applying to non-Rademacher signs without checking sub-Gaussian parameter.

**Tail version (via bounded differences / Hoeffding).** For Rademacher averages of bounded vectors, McDiarmid gives concentration at rate $\sqrt{\log(1/\delta)/n}$ around the Massart expectation bound.

**Project citation key.** \cite{massart2000} or absorbed into the Wainwright/BLM textbook reference.
