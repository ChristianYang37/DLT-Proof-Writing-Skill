# \cite{crootlevpach2017} — Croot–Lev–Pach polynomial method

**Paper.** "Progression-free sets in $\mathbb{Z}_4^n$ are exponentially small,"
Ernie Croot, Vsevolod F. Lev, Péter Pál Pach, *Annals of Mathematics* 185 (2017),
no. 1, 331–337. arXiv:1605.01506.

**Exact name in PDF.** The core rank bound is "Lemma 1" (the statement that a
low-degree polynomial's evaluation matrix on the diagonal has rank bounded by the
number of low-degree monomials). The main result is "Theorem 1".

**Statement (faithfully paraphrased, Lemma 1).** Let $\mathbb{F}$ be a field,
$P\in\mathbb{F}[x_1,\dots,x_n]$ a polynomial of degree $\le d$ that is reduced
(each variable degree $\le q-1$ over $\mathbb{F}_q$). Consider the matrix
$(P(a+b))_{a,b\in S}$ for $S\subseteq\mathbb{F}_q^n$. Then its rank is at most
$2\cdot\#\{$monomials of degree $\le d/2\}$, because $P(a+b)$ expands into
monomials each of which has either the $a$-part or the $b$-part of degree $\le d/2$.

**Hypotheses.** $P$ reduced (exponents $\le q-1$); degree $\le d$. The split is by
the variable group carrying the lower-degree half of each monomial.

**Constants / dimension dependence.** Factor $2$ (two variable groups); for the
3-tensor slice-rank adaptation the analogous factor is $3$ and the threshold is
$d/3$. Exact, no hidden constants.

**Project .bib key.** `\cite{crootlevpach2017}`.
