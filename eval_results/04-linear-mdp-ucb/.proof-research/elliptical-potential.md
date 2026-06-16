# Elliptical potential / log-determinant lemma

**Source.** Abbasi-Yadkori, Pal, Szepesvari, "Improved Algorithms for Linear
Stochastic Bandits", NeurIPS 2011 (Lemma 11 / Lemma 19.4 in Lattimore-Szepesvari
*Bandit Algorithms*). Restated as Lemma D.2 in Jin-Yang-Wang-Jordan 2020
(arXiv:1907.05388). Project .bib key: \cite{abbasi2011improved}.

**Statement (log-determinant form, JYWJ Lemma D.2).** Let $\{\phi_t\}_{t\ge0}$
be a sequence in $\mathbb R^d$ with $\sup_t\|\phi_t\|\le 1$. Let $\Lambda_0$ be
PD with $\lambda_{\min}(\Lambda_0)\ge 1$, and $\Lambda_t=\Lambda_0+\sum_{j=1}^t
\phi_j\phi_j^\top$. Then
$$\log\frac{\det\Lambda_t}{\det\Lambda_0}\le \sum_{j=1}^t \phi_j^\top
\Lambda_{j-1}^{-1}\phi_j \le 2\log\frac{\det\Lambda_t}{\det\Lambda_0}.$$

**Companion (JYWJ Lemma D.1, trace bound).** With $\Lambda_t=\lambda I+\sum_{i=1}^t
\phi_i\phi_i^\top$, $\lambda>0$: $\sum_{i=1}^t \phi_i^\top\Lambda_t^{-1}\phi_i\le d$.
Proof: $\sum_i\phi_i^\top\Lambda_t^{-1}\phi_i=\mathrm{tr}(\Lambda_t^{-1}\sum_i
\phi_i\phi_i^\top)=\sum_{j=1}^d \lambda_j/(\lambda_j+\lambda)\le d$.

**Hypotheses.**
- $\|\phi_j\|\le 1$ for all $j$ (so $\phi_j^\top\Lambda_{j-1}^{-1}\phi_j\le 1$).
- $\lambda_{\min}(\Lambda_0)\ge 1$ (gives $\log(1+x)\le x\le 2\log(1+x)$ on $[0,1]$).
- $\phi_j$ may be adapted; no independence needed.

**Constants / dimension dependence.** The closed regret bound:
$\sum_{j=1}^t\phi_j^\top\Lambda_{j-1}^{-1}\phi_j \le 2d\log\frac{\lambda+t}{\lambda}$
because $\det\Lambda_t\le(\lambda+t)^d$ and $\det\Lambda_0\ge\lambda^d$ (AM-GM on
eigenvalues, trace $\le \lambda d + t$). With $\lambda=1$ this is $\le 2d\log(1+t)$.

**Canonical use pattern (JYWJ Thm 3.1 final step).**
```latex
\sum_{k=1}^K (\phi_h^k)^\top(\Lambda_h^k)^{-1}\phi_h^k
\le 2\log\frac{\det\Lambda_h^{K+1}}{\det\Lambda_h^1}
\le 2d\log\frac{\lambda+K}{\lambda}.
```

**Common misuses.**
- Using the *same-time* $\Lambda_t^{-1}$ (D.1, bound $d$) where the *previous-time*
  $\Lambda_{j-1}^{-1}$ (D.2, bound $2d\log$) is required, or vice versa. The
  regret sum uses $\Lambda_h^k$ which is built from episodes $1..k-1$ — this is
  the "previous-time" potential, so D.2 applies.
- Dropping the $\lambda_{\min}\ge1$ hypothesis: then $\phi_j^\top\Lambda_{j-1}^{-1}
  \phi_j$ may exceed 1 and $\log(1+x)\le x\le 2\log(1+x)$ fails.

**Project citation key.** \cite{abbasi2011improved}
