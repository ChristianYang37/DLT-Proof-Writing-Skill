# Sudakov minoration (lower bound on the expected supremum of a Gaussian process)

**Source.** Roman Vershynin, *High-Dimensional Probability* (2018),
**Theorem 7.4.1 (Sudakov inequality)**, Section 7.4 "Sudakov inequality"
(p. 207). \cite{vershynin2018}. (Verified verbatim against the official
PDF, https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.pdf, by
direct text extraction — see `cite-vershynin2018.md`.)

**Statement (verbatim, Theorem 7.4.1).** Let $(X_t)_{t\in T}$ be a
mean-zero Gaussian process. Then, for any $\varepsilon\ge0$,
$$
   \E\sup_{t\in T} X_t \;\ge\; c\,\varepsilon\,\sqrt{\log N(T,d,\varepsilon)},
$$
where $d$ is the **canonical metric** $d(t,s):=\norm{X_t-X_s}_{L^2}=
(\E(X_t-X_s)^2)^{1/2}$ (eq. 7.13) and $N(T,d,\varepsilon)$ is the
$\varepsilon$-covering number of $(T,d)$ (the smallest cardinality of an
$\varepsilon$-net). $c>0$ is an absolute constant.

**Hypotheses.**
- $(X_t)_{t\in T}$ is a **Gaussian** process (every finite linear
  combination of the $X_t$ is Gaussian), mean-zero. *This is the one
  binding hypothesis: Sudakov is a Gaussian statement.* It is proved in
  Vershynin from the Sudakov–Fernique comparison inequality
  (Theorem 7.2.8), which is itself Gaussian-only.
- $T$ arbitrary index set; the bound is in terms of the geometry of the
  canonical metric only.

**Constants / dimension dependence.** $c$ is absolute (no dimension
factor). The bound is scale-covariant: rescaling all $X_t$ by $\lambda$
rescales both sides by $\lambda$. The "scale" of the lower bound is set by
the packing radius $\varepsilon$ at which $\log N(T,d,\varepsilon)$ is
$\Theta(\log|T|)$.

**Canonical use pattern (finite index, well-separated points).** For a
finite Gaussian vector $(G_a)_{a\in S}$, $|S|=m$, that is *pairwise
$\delta$-separated in canonical metric*, $d(a,a')=\norm{G_a-G_{a'}}_2\ge
\delta$ for all $a\neq a'$, take $\varepsilon=\delta/2$: the open
$\varepsilon$-balls around the $m$ points are disjoint, so any
$\varepsilon$-net must contain $\ge m$ points,
$N(S,d,\varepsilon)\ge m$, giving
$$
   \E\max_{a\in S} G_a \;\ge\; c\,\tfrac{\delta}{2}\,\sqrt{\log m}.
$$
If additionally $\Var G_a\asymp\sigma^2$ and the correlations are
$\le\rho<1$, then $d(a,a')^2=\Var G_a+\Var G_{a'}-2\Cov\ge
2\sigma^2(1-\rho)$, so $\delta\ge\sigma\sqrt{2(1-\rho)}$ and
$\E\max_{a} G_a\ge c'\,\sigma\sqrt{(1-\rho)\log m}$.

**Common misuses.**
- **Applying it to a non-Gaussian process.** Sudakov minoration is FALSE
  in general for sub-Gaussian (non-Gaussian) processes: the lower bound on
  $\E\sup$ uses Gaussian comparison (Sudakov–Fernique), which has no
  sub-Gaussian analogue with the same direction. For a sub-Gaussian
  process one only gets the *upper* Dudley bound; the matching lower bound
  requires either exact Gaussianity or a CLT/Berry–Esseen transfer over
  growing dimension (clean only when the per-pair non-Gaussianity
  $\to0$). To use Sudakov unconditionally one must MAKE the process
  Gaussian (e.g. isotropic-Gaussian noise).
- **Forgetting it lower-bounds $\E\sup$, not $\sup$ itself.** It must be
  combined with a concentration inequality (Borell–TIS, see
  `borell-tis.md`) to turn the expectation bound into a
  high-probability bound.
- **Using the wrong metric.** $d$ is the $L^2$ (canonical) metric of the
  process, not the index-set metric; it must be computed from the
  covariance.

**Project citation key.** \cite{vershynin2018} (Theorem 7.4.1, §7.4).
