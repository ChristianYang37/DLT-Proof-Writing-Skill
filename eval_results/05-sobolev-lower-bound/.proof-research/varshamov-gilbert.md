# Varshamov-Gilbert lemma

**Source.** Tsybakov, *Introduction to Nonparametric Estimation*, 2009, Lemma 2.9.

**Statement.** Let $K \geq 8$. Then there exists a subset $\{\omega^{(0)}, \omega^{(1)}, \ldots, \omega^{(M)}\}$ of $\{0,1\}^K$ such that $\omega^{(0)} = (0,\ldots,0)$,
\[
\rho_H(\omega^{(j)}, \omega^{(k)}) \geq K/8 \quad \forall\, 0 \leq j < k \leq M,
\]
and $M \geq 2^{K/8}$, where $\rho_H$ denotes the Hamming distance.

**Hypotheses.**
- $K \geq 8$ (so that the constants in the proof are valid).
- No other hypotheses; this is a purely combinatorial statement.

**Constants and dimension dependence.** The packing has $M+1 \geq 2^{K/8} + 1$ codewords. Pairwise Hamming distance lower bound is $K/8$. Both constants ($1/8$ in the exponent, $1/8$ in the distance) are tight up to standard improvements.

**Canonical use pattern.** In nonparametric lower-bound proofs over a grid of $m^d$ cells, one applies VG with $K = m^d$, obtaining $M \geq 2^{m^d/8}$ binary codewords (hypotheses). Each codeword $\omega^{(j)} \in \{0,1\}^{m^d}$ indexes a hypothesis $f_j = \frac{c}{m^s} \sum_k \omega^{(j)}_k \psi_k$, where $\psi_k$ are translates/scalings of a bump function.

**Common misuses.**
- Forgetting the requirement $K \geq 8$ (matters only for small $m^d$, but should be noted).
- Confusing Hamming distance with $L^2$ separation — VG gives Hamming, the proof must convert via the bump's $L^2$ norm.

**Project citation key.** \cite{tsybakov2009introduction}
