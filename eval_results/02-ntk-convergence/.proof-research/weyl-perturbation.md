# Weyl's perturbation inequality (eigenvalues)

**Source.** Bhatia, *Matrix Analysis*, GTM 169, Springer 1997, Corollary III.2.6;
also Horn & Johnson, *Matrix Analysis* 2nd ed., Theorem 4.3.1.

**Statement.** Let $A, B$ be $n\times n$ symmetric (Hermitian) matrices with eigenvalues
$\lambda_1(\cdot)\ge\cdots\ge\lambda_n(\cdot)$. Then for every $i\in[n]$,
$|\lambda_i(A) - \lambda_i(B)| \le \|A - B\|_{2}$,
where $\|\cdot\|_2$ is the operator (spectral) norm. In particular
$\lambda_{\min}(A) \ge \lambda_{\min}(B) - \|A-B\|_2$.

**Hypotheses.**
- $A, B$ symmetric (we only ever apply it to symmetric Gram matrices, so satisfied).
- Eigenvalues sorted in the same (decreasing) order.

**Constants / dimension dependence.** None hidden; the bound is dimension-free and tight.

**Canonical use pattern (LaTeX excerpt).**
```latex
By Weyl's inequality (\Cref{fac:weyl}) applied to the symmetric matrices $H(W)$ and $H(0)$,
\begin{align*}
\lambda_{\min}(H(W)) \;\ge\; \lambda_{\min}(H(0)) - \|H(W) - H(0)\|_2.
\end{align*}
```

**Common misuses.**
- Applying it to non-symmetric matrices (eigenvalues need not be real / ordered).
- Confusing operator norm with Frobenius norm in the RHS — Weyl uses operator norm; using
  Frobenius is still a valid *upper* bound on the RHS (since $\|\cdot\|_2\le\|\cdot\|_F$),
  which is exactly how we go Frobenius $\ge$ operator in the concentration lemma.

**Project citation.** Stated as a `\begin{fact}[\cite{bhatia1997matrix}]` and used in
`lem:init-gram-close` and `lem:gram-stability`.
