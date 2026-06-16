# Massart's finite-class lemma (Rademacher complexity of a finite set)

**Source.** Massart (2000); textbook: Mohri et al. (2018) Thm 3.7 (Massart's
lemma); Wainwright HDS (2019) Ex. 5.8 / §5.2; Shalev-Shwartz–Ben-David (2014)
Lemma 26.8. Project keys: `\cite{mohri2018foundations}`, `\cite{wainwright2019high}`.

**Statement.** Let $A\subset\mathbb R^N$ be a finite set of vectors with
$r:=\max_{a\in A}\|a\|_2$, and let $\sigma=(\sigma_1,\dots,\sigma_N)$ be i.i.d.
Rademacher. Then
$$\E_\sigma\Big[\max_{a\in A}\sum_{i=1}^N\sigma_i a_i\Big]
  \le r\sqrt{2\log|A|}.$$
Consequently, if $\mathcal G$ is a class whose restriction to a sample of size
$m$ takes values in $[0,1]^m$ and realizes at most $|\mathcal G_{|S}|$ distinct
vectors, then the empirical Rademacher complexity satisfies
$$\widehat{\mathfrak R}_S(\mathcal G)
  =\E_\sigma\Big[\sup_{g}\tfrac1m\sum_{i=1}^m\sigma_i g(z_i)\Big]
  \le \frac{\sqrt m\cdot\sqrt{2\log|\mathcal G_{|S}|}}{m}
  =\sqrt{\tfrac{2\log|\mathcal G_{|S}|}{m}},$$
using $\|a\|_2\le\sqrt m$ for $a\in[0,1]^m$ (in fact $a\in\{0,1\}^m$ gives
$\|a\|_2\le\sqrt m$).

**Hypotheses.**
- Finite set $A$ (or finite projection $\mathcal G_{|S}$).
- Rademacher signs independent of $A$.
- Radius bound $r=\max_a\|a\|_2$; for $\{0,1\}^m$ vectors $r\le\sqrt m$.

**Constants / dimension dependence.** Constant inside the root is exactly $2$.
Proof: Jensen/Hoeffding on the MGF — $\E\max_a e^{\lambda\langle\sigma,a\rangle}
\le|A|e^{\lambda^2 r^2/2}$, so $\E\max_a\langle\sigma,a\rangle\le
\frac{\log|A|}{\lambda}+\frac{\lambda r^2}{2}$, optimized at
$\lambda=\sqrt{2\log|A|}/r$ giving $r\sqrt{2\log|A|}$.

**Canonical use pattern.**
```latex
On the double sample $S\cup S'$ (size $2n$), the loss class realizes at most
$\Pi_{\mathcal H}(2n)$ distinct $\{0,1\}^{2n}$ vectors. By Massart's lemma,
\begin{align*}
\widehat{\mathfrak R}_{S\cup S'}(\mathcal L)
\le \sqrt{\tfrac{2\log\Pi_{\mathcal H}(2n)}{2n}}.
\end{align*}
```

**Common misuses.**
- Wrong radius: using $r=1$ instead of $r\le\sqrt m$ for $\{0,1\}^m$ vectors,
  losing a $\sqrt m$ and thus the $1/\sqrt n$ scaling.
- Forgetting the $1/m$ normalization in $\widehat{\mathfrak R}$.
- Using $|A|=\Pi_{\mathcal H}(n)$ at the wrong sample size (should be the size of
  the set the Rademacher average is taken over — here $2n$).
- The bound is on the **expected** max over signs; combined with symmetrization
  it bounds $\E\sup(P-\hat P)$, still requiring McDiarmid for high probability.

**Project citation key.** `\cite{mohri2018foundations}`
