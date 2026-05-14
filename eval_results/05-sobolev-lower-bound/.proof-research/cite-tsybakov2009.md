# \cite{tsybakov2009introduction} — Tsybakov, Introduction to Nonparametric Estimation

**Paper.** *Introduction to Nonparametric Estimation*, A. B. Tsybakov, Springer Series in Statistics, 2009. ISBN 978-0-387-79051-0.

**Results we cite.**

- **Lemma 2.9 (Varshamov–Gilbert bound).** "Let $m \geq 8$. Then there exists a subset $\{\omega^{(0)},\ldots,\omega^{(M)}\}$ of $\Omega = \{0,1\}^m$ such that $\omega^{(0)} = (0,\ldots,0)$, $\rho(\omega^{(j)},\omega^{(k)}) \geq m/8 \ \forall\ 0 \leq j < k \leq M$, and $M \geq 2^{m/8}$." (page 104).

- **Theorem 2.5 (Fano-type bound).** Minimax tail bound via $M$ hypotheses with pairwise separation $\geq 2s$ and average KL $\leq \alpha \log M$ with $\alpha < 1/8$.

- **Section 2.5 (KL for Gaussian regression).** Closed form $\mathrm{KL}(P_f \| P_g) = \frac{1}{2\sigma^2} \sum_{i=1}^n (f(x_i) - g(x_i))^2$ for fixed-design Gaussian regression.

- **Chapter 2.6.1 (bump-function lower bound).** Construction of the scaled-bump family $f_\omega$ used to prove minimax lower bounds over Hölder/Sobolev classes.

**Hypotheses for our use.**
- VG: $K \geq 8$, satisfied for $m^d \geq 8$ (true for $m \geq 2$ and $d \geq 3$, or $m \geq 8$ for any $d$; we will assume $n$ large enough that $m^d \geq 8$).
- Fano: $\alpha < 1/8$ — verified by choosing the bump amplitude small enough.
- KL formula: requires Gaussian noise; given in the problem.

**Constants / dimension dependence.** VG gives $M \geq 2^{m^d/8}$; Fano gives prefactor $\geq c_0 > 0$ uniform in $M$ once $\alpha \leq 1/16$. These are universal.

**Project .bib key.** `\cite{tsybakov2009introduction}`.
