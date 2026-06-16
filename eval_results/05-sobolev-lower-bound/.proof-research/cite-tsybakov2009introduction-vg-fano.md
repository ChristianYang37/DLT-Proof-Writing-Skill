# \cite{tsybakov2009introduction} — Varshamov–Gilbert bound and Fano method

**Paper.** *Introduction to Nonparametric Estimation*, A. B. Tsybakov,
Springer Series in Statistics, 2009 (English edition). Standard graduate
reference for nonparametric minimax theory.

**Exact names in the book.**
- **Varshamov–Gilbert bound:** Lemma 2.9 (Chapter 2, §2.6). States: for
  $M_0 \ge 8$ there exist $M \ge 2^{M_0/8}$ binary strings in
  $\{0,1\}^{M_0}$ pairwise at Hamming distance $\ge M_0/8$.
- **Fano-type minimax lower bound:** Theorem 2.5 and Corollary 2.6 (§2.2),
  together with the reduction scheme of §2.2 ("from estimation to testing")
  and the KL-to-mutual-information bound of §2.4. The combined statement used
  here: if $M\ge 2$, hypotheses are $2\Delta$-separated and the pairwise KL
  satisfies $\frac{1}{M}\sum_k \KL(P_k\|P_0)\le \alpha\log M$ with
  $0<\alpha<1/8$, then the minimax probability of error is bounded below by a
  positive constant, hence $\inf_{\hat f}\sup_k\E\,\rho^2(\hat f,f_k)\ge
  c\,\Delta^2$.

**Statement (faithfully paraphrased, as used).**
- (VG, Lemma 2.9) $\exists\,\{\tau^{(0)},\dots,\tau^{(M)}\}\subset\{0,1\}^{M_0}$
  with $M\ge 2^{M_0/8}$ and $\rho_H(\tau^{(k)},\tau^{(k')})\ge M_0/8$ for $k\ne k'$.
- (Fano testing, from Thm 2.5/Cor 2.6) For $V$ uniform on $\{1,\dots,M\}$ and
  observation law $P_V$,
  $\inf_\psi \Pr[\psi(Y)\ne V]\ge 1-\frac{I(V;Y)+\log2}{\log M}$, with
  $I(V;Y)\le \frac1{M^2}\sum_{k,k'}\KL(P_k\|P_{k'})$.

**Hypotheses.** $M_0\ge 8$ for VG; $M\ge 2$, common dominating measure, finite
pairwise KL for Fano. Both purely information-theoretic / combinatorial.

**Constants / dimension dependence.** VG constants are the universal $1/8$
(count exponent) and $1/8$ (Hamming radius). Fano carries the explicit
$+\log 2$; no hidden dimension factors.

**Project .bib key.** `\cite{tsybakov2009introduction}`.
