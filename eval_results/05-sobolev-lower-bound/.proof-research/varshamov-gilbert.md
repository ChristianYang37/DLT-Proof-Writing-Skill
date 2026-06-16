# Varshamov–Gilbert bound (combinatorial packing of the hypercube)

**Source.** Tsybakov, *Introduction to Nonparametric Estimation*, Springer
2009, Lemma 2.9 (the "Varshamov–Gilbert bound"). Cite key
`tsybakov2009introduction`.

**Statement (faithfully paraphrased).** Let $M_0 \ge 8$. There exists a
subset $\{\tau^{(0)},\dots,\tau^{(M)}\}$ of the binary hypercube
$\{0,1\}^{M_0}$ such that $\tau^{(0)} = (0,\dots,0)$,
$$M \ge 2^{M_0/8}, \qquad
\rho_H(\tau^{(k)},\tau^{(k')}) \ge \frac{M_0}{8}
\quad \text{for all } 0 \le k < k' \le M,$$
where $\rho_H$ is the Hamming distance. (Tsybakov's version actually gives
$M \ge 2^{M_0/8}$ codewords pairwise $\ge M_0/8$ apart; the leading $\tau^{(0)}=0$
codeword is optional and not needed for the lower bound.)

**Hypotheses.**
- Dimension $M_0 \ge 8$ (here $M_0 = m^d$, automatically large for $m\ge 2$).
- No condition on the field; purely combinatorial / probabilistic
  (Gilbert–Varshamov greedy/volume argument).

**Constants and dimension dependence.** The $1/8$ in both the count exponent
and the Hamming radius is the standard Tsybakov constant; one can trade them
off (Plotkin / random-coding gives slightly different constants). We use the
$1/8$–$1/8$ pair exactly as the eval prompt requests.

**Canonical use pattern.** Index a family of localized perturbations
$u_k = \sum_{j} \tau^{(k)}_j \,\omega\, \phi_j$ by the codewords; the Hamming
separation $\ge M_0/8$ becomes an $L^2$ separation $\|u_k-u_{k'}\|_{L^2}^2
\ge (M_0/8)\,\omega^2\|\phi_j\|_{L^2}^2$, and $\log M \ge (M_0/8)\log 2$
feeds the Fano denominator.

**Common misuses.**
- Using $M \ge 2^{M_0}$ (the whole cube) — false at this Hamming radius; the
  exponent must carry the $1/8$.
- Forgetting that the bound needs $M_0 \ge 8$ (vacuous for tiny $M_0$).
- Conflating Hamming distance with $L^2$ distance without multiplying by the
  per-coordinate $L^2$ mass $\omega^2 \|\phi_j\|_{L^2}^2$.

**Project citation key.** `\cite{tsybakov2009introduction}`.
