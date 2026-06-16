# \cite{mohri2018foundations} — Foundations of Machine Learning (2nd ed.)

**Paper.** *Foundations of Machine Learning*, 2nd edition, Mehryar Mohri,
Afshin Rostamizadeh, Ameet Talwalkar. MIT Press, 2018. ISBN 9780262039406.

**Results used (exact names in book).**
- **Theorem 3.7 (Massart's lemma).** For a finite set $A\subseteq\mathbb R^m$
  with $r=\max_{a\in A}\|a\|_2$, $\E_\sigma[\frac1m\max_{a\in A}\sum_i\sigma_i a_i]
  \le \frac{r\sqrt{2\log|A|}}{m}$.
- **Theorem 3.17 (Sauer's lemma / growth function).** If $\mathrm{VCdim}(\mathcal H)=d$
  then $\Pi_{\mathcal H}(m)\le\sum_{i=0}^d\binom mi$, and for $m\ge d$,
  $\le (em/d)^d$.
- **Lemma 3.4 / Theorem 3.3 (Rademacher generalization & symmetrization).** The
  ghost-sample symmetrization bounding $\E\sup(P-\hat P)\le 2\mathfrak R_m$, and
  the two-sided Rademacher generalization bound.

**Statement (faithfully paraphrased).** As digested in
`massart.md`, `sauer-shelah.md`, `symmetrization.md`. Constants: Massart factor
$\sqrt2$; symmetrization factor $2$; Sauer bound $(em/d)^d$.

**Hypotheses.** finite class / finite VC dimension; i.i.d. sample; Rademacher
signs independent of data.

**Constants / dimension dependence.** All constants explicit and standard;
matches the digests in this folder.

**Project .bib key.** `\cite{mohri2018foundations}`
