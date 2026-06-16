# Ghost-sample symmetrization (Rademacher)

**Source.** Mohri–Rostamizadeh–Talwalkar, *Foundations of Machine Learning*
(2018, 2nd ed.), Lemma 3.4 / proof of Thm 3.3; Wainwright HDS (2019) §4.2;
Boucheron–Lugosi–Massart (2013) §11. Project keys: `\cite{mohri2018foundations}`,
`\cite{wainwright2019high}`.

**Statement.** Let $\mathcal G$ be a class of functions $z\mapsto g(z)\in[0,1]$,
$S=(Z_1,\dots,Z_n)$ i.i.d. $\sim P$, and $S'=(Z_1',\dots,Z_n')$ an independent
*ghost* sample i.i.d. $\sim P$. With $\sigma_1,\dots,\sigma_n$ i.i.d. Rademacher
($\Pr[\sigma_i=\pm1]=1/2$), independent of $S,S'$, and
$\hat P_n g=\frac1n\sum_i g(Z_i)$, $Pg=\E_{Z}g(Z)$,
$$\E_S\Big[\sup_{g\in\mathcal G}\big(Pg-\hat P_n g\big)\Big]
  \le 2\,\E_{S,\sigma}\Big[\sup_{g\in\mathcal G}\tfrac1n\sum_{i=1}^n\sigma_i g(Z_i)\Big]
  = 2\,\mathfrak R_n(\mathcal G).$$
The factor $2$ is the symmetrization constant. The same holds for the two-sided
quantity $\E_S\sup_g|Pg-\hat P_n g|$ with the absolute value inside the
Rademacher average.

**Hypotheses.**
- i.i.d. sample; ghost sample independent and identically distributed.
- Rademacher signs independent of both samples.
- $\mathcal G$ a fixed (data-independent) class.

**Constants / dimension dependence.** The constant is exactly $2$. Two steps:
(i) $Pg=\E_{S'}\hat P'_n g$, so $\sup_g(Pg-\hat P_ng)\le\E_{S'}\sup_g(\hat P'_ng-
\hat P_ng)$ by Jensen (sup of expectation $\le$ expectation of sup); (ii)
introduce signs: $g(Z'_i)-g(Z_i)$ is symmetric, so multiplying by $\sigma_i$
leaves the distribution unchanged, then split the sup → two Rademacher averages,
each $\le\mathfrak R_n(\mathcal G)$, summing to $2\mathfrak R_n$.

**Canonical use pattern.**
```latex
\begin{align*}
\E_S\Big[\sup_{g}\big(Pg-\hat P_ng\big)\Big]
&\le \E_{S,S'}\Big[\sup_g\tfrac1n\textstyle\sum_i\big(g(Z'_i)-g(Z_i)\big)\Big]\\
&= \E_{S,S',\sigma}\Big[\sup_g\tfrac1n\textstyle\sum_i\sigma_i\big(g(Z'_i)-g(Z_i)\big)\Big]\\
&\le 2\,\mathfrak R_n(\mathcal G).
\end{align*}
```

**Common misuses.**
- Dropping the factor $2$.
- Forgetting that the inequality is on the **expected** sup; the high-probability
  version still needs a separate concentration step (McDiarmid) — symmetrization
  alone does not give $\log(1/\delta)$.
- Applying with a data-dependent $\mathcal G$ (then signs are not independent).

**Project citation key.** `\cite{mohri2018foundations}`
