# \cite{boucheron2013concentration} — Concentration Inequalities

**Paper.** *Concentration Inequalities: A Nonasymptotic Theory of Independence*,
Stéphane Boucheron, Gábor Lugosi, Pascal Massart. Oxford University Press, 2013.
ISBN 9780199535255.

**Results used (exact names in book).**
- **Theorem 6.2 (bounded differences inequality / McDiarmid).** For independent
  $X_1,\dots,X_n$ and $f$ with the bounded-differences property (constants
  $c_i$), $\Pr[f-\E f\ge t]\le\exp(-2t^2/\sum_i c_i^2)$ (one-sided; two-sided by
  applying to $\pm f$).
- **§11 (symmetrization and Rademacher averages).** The symmetrization inequality
  $\E\sup_{g}(Pg-\hat P_ng)\le 2\E\,\mathfrak R_n$, and Massart-type finite-class
  bounds for the Rademacher average.

**Statement (faithfully paraphrased).** See `mcdiarmid.md` and `symmetrization.md`.

**Hypotheses.** independence; bounded differences. No distributional assumptions.

**Constants / dimension dependence.** Exponent constant $2$, denominator
$\sum_i c_i^2$ (sharp). For $g=\sup_h|R-\hat R|$ with i.i.d. data, $c_i=1/n$, so
$\sum_i c_i^2=1/n$.

**Project .bib key.** `\cite{boucheron2013concentration}`
