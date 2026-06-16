# \cite{vershynin2018high} — Hoeffding's inequality for bounded variables

**Paper.** Roman Vershynin, *High-Dimensional Probability: An Introduction with Applications
in Data Science*, Cambridge University Press, 2018.

**Exact name in book.** Theorem 2.2.6 ("Hoeffding's inequality, general case"); the
two-sided form $\Pr[|S-\E S|\ge t]\le 2\exp(-2t^2/\sum(\beta_i-\alpha_i)^2)$ follows by
applying the one-sided bound to $\pm(S-\E S)$ and a union bound (Remark following 2.2.6).

**Statement (faithful).** Let $X_1,\dots,X_N$ be independent random variables with
$X_i\in[m_i,M_i]$ a.s. Then for any $t\ge0$,
$\Pr\big[\sum_i (X_i-\E X_i)\ge t\big]\le\exp\!\big(-\frac{2t^2}{\sum_i(M_i-m_i)^2}\big)$.

**Hypotheses.** Independence; almost-sure boundedness in $[m_i,M_i]$. No identical
distribution required; no mean-zero required (centering is explicit).

**Constants / dimension dependence.** Constant $2$ in the exponent is sharp; bound is
dimension-free, depending only on $\sum_i(M_i-m_i)^2$.

**Use in this proof.** Cited as `\begin{fact}[\cite{vershynin2018high}]` (`fac:hoeffding`).
In `lem:init-gram-close` we actually use the closely related second-moment + Markov route
(which is even more elementary); Hoeffding is stated as the canonical bounded-RV tail and is
the standard reference for the entrywise Gram concentration. The fact is invoked via the
`\begin{fact}[\cite{...}]` form, so R5 is satisfied without a local proof.

**Project .bib key.** \cite{vershynin2018high}
