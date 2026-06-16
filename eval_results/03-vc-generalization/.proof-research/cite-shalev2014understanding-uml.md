# \cite{shalev2014understanding} — Understanding Machine Learning

**Paper.** *Understanding Machine Learning: From Theory to Algorithms*, Shai
Shalev-Shwartz and Shai Ben-David. Cambridge University Press, 2014. ISBN
9781107057135.

**Results used (exact names in book).**
- **Lemma 6.10 (Sauer–Shelah, via shifting).** If $\mathrm{VCdim}(\mathcal H)\le d$
  then for all $m$, $|\mathcal H_{|C}|\le\sum_{i=0}^d\binom mi$ for $|C|=m$.
  The book proves the stronger Pajor claim $|\mathcal H_{|C}|\le
  |\{B\subseteq C:\mathcal H\text{ shatters }B\}|$ by induction (Lemma 6.10
  proof), which is the downward-shifting argument digested in `sauer-shelah.md`.
- **Lemma 26.8 (Massart lemma).** Rademacher complexity of a finite set of
  vectors in a ball of radius $r$ is $\le \frac{r\sqrt{2\log|A|}}{m}$.

**Statement (faithfully paraphrased).** See `sauer-shelah.md` and `massart.md`.

**Hypotheses.** finite VC dimension (Sauer); finite set (Massart). Combinatorial,
no probability for Sauer.

**Constants / dimension dependence.** Sauer bound $\sum_{i\le d}\binom mi\le
(em/d)^d$ for $m\ge d$ (book's Lemma A.5 / standard binomial-sum bound). Massart
constant $\sqrt2$.

**Project .bib key.** `\cite{shalev2014understanding}`
