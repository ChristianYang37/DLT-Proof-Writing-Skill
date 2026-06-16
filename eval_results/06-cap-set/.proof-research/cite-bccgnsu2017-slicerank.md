# \cite{bccgnsu2017} — slice rank, symmetric formulation

**Paper.** "On cap sets and the group-theoretic approach to matrix
multiplication," Jonah Blasiak, Thomas Church, Henry Cohn, Joshua A. Grochow,
Eric Naslund, William F. Sawin, Chris Umans, *Discrete Analysis* 2017:3, 27 pp.
arXiv:1605.06702.

**Exact name in PDF.** Slice rank is introduced in §4 ("Definition 4.1, slice
rank"); the diagonal lower bound is "Lemma 4.7" (a tensor that is diagonal with
$D$ nonzero entries has slice rank exactly $D$). Attributed there to Tao.

**Statement (faithfully paraphrased).**
- Definition (slice rank): $\operatorname{sr}(T)$ is the least number of "slices"
  $f(x_i)\cdot g(\text{remaining variables})$ summing to $T$.
- Lemma (diagonal lower bound): if $T(x_1,\dots,x_k)=\sum_{x\in X}c_x
  \mathbf{1}[x_1=\dots=x_k=x]$ with all $c_x\ne 0$, then
  $\operatorname{sr}(T)=|X|$.
- Subadditivity: $\operatorname{sr}(T+T')\le\operatorname{sr}(T)+\operatorname{sr}(T')$.

**Hypotheses.** Field arbitrary; diagonal entries nonzero for the exact lower
bound. The lower bound is the load-bearing direction.

**Constants / dimension dependence.** Exact integer equalities; no constants.

**Project .bib key.** `\cite{bccgnsu2017}`.
