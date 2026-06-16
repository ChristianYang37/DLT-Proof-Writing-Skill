# McDiarmid's inequality (bounded differences)

**Source.** Boucheron–Lugosi–Massart, *Concentration Inequalities* (2013),
Theorem 6.2; also Wainwright, *High-Dimensional Statistics* (2019), Cor. 2.21.
Project cite key: `\cite{boucheron2013concentration}`, `\cite{wainwright2019high}`.

**Statement.** Let $X_1,\dots,X_n$ be independent random variables taking values
in a set $\mathcal Z$, and let $g:\mathcal Z^n\to\mathbb R$ satisfy the bounded-
differences property with constants $c_1,\dots,c_n$: for every $i$ and every
$z_1,\dots,z_n,z_i'$,
$$|g(z_1,\dots,z_i,\dots,z_n)-g(z_1,\dots,z_i',\dots,z_n)|\le c_i.$$
Then for every $t>0$,
$$\Pr\big[\,g(X)-\E g(X)\ge t\,\big]\le \exp\!\Big(-\tfrac{2t^2}{\sum_{i=1}^n c_i^2}\Big),$$
and the same bound holds for the left tail $\Pr[\E g(X)-g(X)\ge t]$.

**Hypotheses.**
- $X_1,\dots,X_n$ **independent** (not necessarily identically distributed).
- Bounded differences: changing one coordinate moves $g$ by at most $c_i$.
- No moment / distributional assumption beyond independence.

**Constants / dimension dependence.** Constant $2$ in the exponent is sharp for
the symmetric case; denominator is $\sum_i c_i^2$. For our use $g(S)=\sup_h|R(h)-
\hat R_n(h)|$ with the $\sup$ over $\mathcal H$: changing one sample point
$(x_i,y_i)$ changes $\hat R_n(h)$ by at most $1/n$ uniformly in $h$, and the sup
of $1/n$-Lipschitz functions is $1/n$-bounded-difference, so $c_i=1/n$ and
$\sum_i c_i^2=1/n$. Hence $\Pr[g-\E g\ge t]\le e^{-2nt^2}$, i.e. with prob
$\ge 1-\delta$, $g\le \E g+\sqrt{\log(1/\delta)/(2n)}$.

**Canonical use pattern.**
```latex
The map $g(S)=\sup_{h\in\mathcal H}|R(h)-\hat R_n(h)|$ has bounded differences
$c_i=1/n$ (replacing one example changes each $\hat R_n(h)$ by $\le 1/n$).
By McDiarmid's inequality, with probability $\ge 1-\delta$,
\begin{align*}
\sup_{h}|R(h)-\hat R_n(h)|\le \E\big[\sup_h|R(h)-\hat R_n(h)|\big]
   +\sqrt{\tfrac{\log(1/\delta)}{2n}}.
\end{align*}
```

**Common misuses.**
- Using $c_i=1$ instead of $1/n$ (forgetting the $1/n$ normalization of
  $\hat R_n$) — gives a vacuous $\sqrt{n}$ instead of $1/\sqrt n$.
- Applying it to $g$ that is not bounded-difference because the $\sup$ is over a
  data-dependent set; here the class $\mathcal H$ is fixed, so it is fine.
- One-sided vs two-sided: McDiarmid gives one tail; we use it on
  $g=\sup_h|R-\hat R|$ directly (already a two-sided sup inside), needing only
  the upper tail of $g$.

**Project citation key.** `\cite{boucheron2013concentration}`
