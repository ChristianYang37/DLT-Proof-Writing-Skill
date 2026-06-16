# \cite{gilmer2022unionclosed} — Gilmer's constant lower bound for union-closed sets

**Paper.** "A constant lower bound for the union-closed sets conjecture",
Justin Gilmer (Google Research), arXiv:2211.09055v2, 28 Nov 2022, 11 pages.
math.CO.

**Exact names in PDF.**
- "Theorem 1" (p. 2): the entropy inequality $H(A\cup B)\ge 1.26\,H(A)$ under
  $\Pr[i\in A]\le 0.01$.
- "Theorem 2" (p. 2): the combinatorial corollary — some element in $\ge 0.01$
  fraction.
- "Lemma 1" (p. 4): the key per-coordinate technical lemma
  $\E_{c,c'}[h(p_c+p_{c'}-p_cp_{c'})]\ge 1.26\,\E_c[h(p_c)]$ when $\E_c[p_c]\le 0.01$.
- "Lemma 2" (p. 6): $p,p'\le 0.1 \Rightarrow h(p+p'-pp')\ge 1.4\cdot(h(p)+h(p'))/2$.
- "Lemma 3" (p. 6): $h(p+p'-pp')\ge (1-p)h(p')$ for all $p,p'\in[0,1]$.
- "Lemma 4" (p. 6), "Lemma 5" (p. 7): the two region bounds.

**Statement (Theorem 1, verbatim).** "Let $A$ and $B$ denote independent
samples from a distribution over subsets of $[n]$. Assume that for all
$i\in[n]$, $\Pr[i\in A]\le 0.01$. Then $H(A\cup B)\ge 1.26\,H(A)$."

**Statement (Theorem 2, verbatim).** "Let $\mathcal F\subseteq 2^{[n]}$ be a
union-closed family, $\mathcal F\ne\{\emptyset\}$. Then there exists $i\in[n]$
that is contained in at least a $0.01$ fraction of the sets in $\mathcal F$."

**Hypotheses.** Finite universe $[n]$; $A,B$ i.i.d. from an *arbitrary*
distribution over $2^{[n]}$ (Theorem 1) — for Theorem 2 the distribution is
uniform on $\mathcal F$. Marginal cap $\Pr[i\in A]\le 0.01$ for every $i$.

**Constants / dependence.** $0.01$ explicitly *not* optimized; $1.26$ is the
amplification factor; region threshold $0.1$, region probability $\ge 0.9$ via
Markov. Sharp threshold $\frac{3-\sqrt5}{2}\approx 0.38$ proven in follow-up
work (arXiv:2211.11504, 2211.11689, 2211.11731), cited but not reproduced.

**Auxiliary fact used (Cover–Thomas).** Entropy of a distribution on a finite
support of size $|\mathcal F|$ is $\le \log|\mathcal F|$, with equality iff
uniform (Cover & Thomas, *Elements of Information Theory*, Thm 2.6.4 region).
Chain rule and data-processing inequality also from Cover–Thomas.

**Project .bib key.** `\cite{gilmer2022unionclosed}`. Cover–Thomas keyed
`\cite{coverthomas2006}`.
