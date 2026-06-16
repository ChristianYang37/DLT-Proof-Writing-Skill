# \cite{wainwright2019high} — High-Dimensional Statistics

**Paper.** *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*, Martin J.
Wainwright. Cambridge University Press, 2019. Series: Cambridge Series in
Statistical and Probabilistic Mathematics. ISBN 9781108498029.

**Results used (exact names in book).**
- **Corollary 2.21 (bounded-differences / McDiarmid inequality).** For
  independent $X_i$ and $g$ with bounded differences $c_i$,
  $\Pr[|g-\E g|\ge t]\le 2\exp(-2t^2/\sum_i c_i^2)$.
- **§4.2 / Proposition 4.11 (Rademacher symmetrization upper bound).** Expected
  uniform deviation $\le 2\,\mathfrak R_n(\mathcal F)$.
- **§5.2 (Massart finite-class / one-step discretization).** Rademacher
  complexity of a finite class $\le \sqrt{2\log|\mathcal F_{|S}|/n}$ (radius
  $\sqrt n$ for $[0,1]^n$ vectors).

**Statement (faithfully paraphrased).** See `mcdiarmid.md`, `symmetrization.md`,
`massart.md` in this folder for the precise statements and constants used.

**Hypotheses.** independence (McDiarmid); i.i.d. + fixed class (symmetrization);
finiteness (Massart). No tail assumptions beyond boundedness.

**Constants / dimension dependence.** McDiarmid exponent constant $2$,
denominator $\sum_i c_i^2$; symmetrization factor $2$; Massart $\sqrt2$.

**Project .bib key.** `\cite{wainwright2019high}`
