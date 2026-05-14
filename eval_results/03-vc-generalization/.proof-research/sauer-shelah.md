# Sauer–Shelah lemma

**Source.** Sauer 1972; Shelah 1972; Vapnik–Chervonenkis 1971. Restated e.g. in Vershynin, *High-Dimensional Probability*, Ch. 8; Wainwright Ch. 4; Boucheron-Lugosi-Massart Ch. 13.

**Statement.** Let $\mathcal{H} \subset \{0,1\}^{\mathcal{X}}$ have VC dimension $d$. For any finite set $A \subset \mathcal{X}$ with $|A| = m$, the projection $\mathcal{H}|_A := \{ (h(x))_{x \in A} : h \in \mathcal{H} \}$ satisfies
$$
|\mathcal{H}|_A| \;\le\; \sum_{i=0}^{d} \binom{m}{i} \;=:\; \binom{m}{\le d}.
$$
In particular, when $m \ge d \ge 1$,
$$
|\mathcal{H}|_A| \;\le\; \left( \frac{e m}{d} \right)^d.
$$

**Hypotheses.**
- $\mathcal{H}$ is a class of $\{0,1\}$-valued functions.
- $d := \mathrm{VC}(\mathcal{H}) < \infty$.
- $A$ is any finite subset of $\mathcal{X}$.

**Constants and dimension dependence.** Bound is sharp up to constants. The closed-form $(em/d)^d$ uses the elementary $\sum_{i \le d} \binom{m}{i} \le (em/d)^d$ for $m \ge d$.

**Canonical use.** After symmetrization, the supremum over $\mathcal{H}$ reduces to a supremum over $\mathcal{H}|_{S \cup S'}$, a finite class of size $\le (2en/d)^d$. We then take logs: $\log |\mathcal{H}|_{S \cup S'}| \le d \log(2en/d)$.

**Common misuses.**
- Confusing growth function $\Pi_{\mathcal{H}}(m) := \max_{|A|=m} |\mathcal{H}|_A|$ with shattering number.
- Forgetting that the $m \ge d$ side condition is needed for $(em/d)^d$.
- Applying to real-valued classes (need pseudo-dimension or fat-shattering).

**Project citation key.** \cite{sauer1972} or absorbed into a single \cite{vapnik1998}.
