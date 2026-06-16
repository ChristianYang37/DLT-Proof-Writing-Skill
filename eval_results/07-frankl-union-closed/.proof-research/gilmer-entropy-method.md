# Gilmer's entropy method for the union-closed sets conjecture

**Source.** Justin Gilmer, "A constant lower bound for the union-closed sets
conjecture", arXiv:2211.09055v2 (28 Nov 2022). `\cite{gilmer2022unionclosed}`.

Base-2 logarithm throughout: $\log = \log_2$, entropy $H(\cdot)$ in bits.
Binary entropy $H(p) = -p\log p - (1-p)\log(1-p)$ (Gilmer writes $H$ for both
the Shannon entropy and the binary-entropy function; we write $h(p)$ for the
binary-entropy scalar function to avoid overloading).

**Statement (Theorem 1, verbatim).** Let $A,B$ be independent samples from a
distribution over subsets of $[n]$. Assume that for all $i\in[n]$,
$\Pr[i\in A]\le 0.01$. Then $H(A\cup B)\ge 1.26\,H(A)$.

**Corollary (Theorem 2, verbatim).** Let $\mathcal F\subseteq 2^{[n]}$ be
union-closed, $\mathcal F\ne\{\emptyset\}$. Then there exists $i\in[n]$
contained in at least a $0.01$ fraction of the sets of $\mathcal F$.

**Why the corollary follows.** Take $A,B$ i.i.d. uniform on $\mathcal F$. Then
$A\cup B\in\mathcal F$ (union-closure), and the entropy of *any* distribution
supported on $\mathcal F$ is at most $\log|\mathcal F|$, attained by the uniform
distribution; since $A$ is uniform, $H(A) = \log|\mathcal F|\ge H(A\cup B)$.
If every $p_i=\Pr[i\in A]\le 0.01$, Theorem 1 gives $H(A\cup B)\ge 1.26\,H(A)$.
Because $|\mathcal F|\ge 2$ and $\mathcal F\ne\{\emptyset\}$ forces $H(A)>0$,
this yields $H(A\cup B) > H(A)\ge H(A\cup B)$, a contradiction. Hence some
$p_i > 0.01$.

**Proof skeleton of Theorem 1 (the load-bearing chain).**

- *Per-coordinate target (Eq. 1).* Reveal bits one at a time; show for each $i$
  $$H((A\cup B)_i \mid (A\cup B)_{<i}) \ge 1.26\, H(A_i\mid A_{<i}).$$
  Chain rule $H(Z) = \sum_i H(Z_i\mid Z_{<i})$ then gives Theorem 1.
- *Conditional-entropy monotonicity (property 2).* For any $X,Y$ and function
  $f$: $H(X\mid Y)\le H(X\mid f(Y))$. Proof: $X\to Y\to f(Y)$ is a Markov chain,
  so by data processing $I(X{:}f(Y))\le I(X{:}Y)$, i.e.
  $H(X)-H(X\mid f(Y))\le H(X)-H(X\mid Y)$.
- *Crucial step (Eq. 2).* Since $(A\cup B)_{<i}$ is a function of $(A_{<i},B_{<i})$,
  $$H((A\cup B)_i\mid (A\cup B)_{<i}) \ge H((A\cup B)_i \mid A_{<i}, B_{<i}).$$
  Conditioning on the i.i.d. richer history $A_{<i},B_{<i}$ makes $A_i,B_i$
  conditionally independent Bernoulli — exactly Lemma 1's hypotheses with
  $C = A_{<i}$, $C' = B_{<i}$, $X=A_i$, $X'=B_i$.

**Lemma 1 (key technical, verbatim restatement).** Let $\{p_c\}_{c\in S}\subset[0,1]$
with $C$ a r.v. over finite $S$, $X\sim\mathrm{Ber}(p_C)$ given $C=c$, $C'$ an
i.i.d. copy, $X'\sim\mathrm{Ber}(p_{C'})$ given $C'$, independent of $(X,C)$.
If $\E[X]\le 0.01$ then $H(X\cup X'\mid C,C')\ge 1.26\,H(X\mid C)$.
Succinctly: if $\E_c[p_c]\le 0.01$ then
$$\E_{c,c'}\!\big[h(p_c+p_{c'}-p_cp_{c'})\big]\ \ge\ 1.26\,\E_c[h(p_c)].$$
(Note $\Pr[X\cup X'=1\mid c,c'] = p_c+p_{c'}-p_cp_{c'}$, the OR of two
independent bits.)

**Lemma 2 (verbatim).** If $p,p'\le 0.1$ then
$h(p+p'-pp')\ge 1.4\cdot\frac{h(p)+h(p')}{2}$.
Proof idea: concavity gives $\frac{h(p)+h(p')}{2}\le h(\frac{p+p'}{2})$; and
$p+p'-pp'\ge 0.9(p+p')$ on $[0,0.1]^2$, so the ratio is
$\ge \min_{u\in(0,0.2]} h(0.9u)/h(0.5u) = h(0.18)/h(0.1) > 1.4$ (min at $u=0.2$).

**Lemma 3 (verbatim).** For any $p,p'\in[0,1]$, $h(p+p'-pp')\ge (1-p)h(p')$.
Proof: $p+p'-pp' = p\cdot 1 + (1-p)p'$; concavity of $h$ gives
$h(p\cdot 1+(1-p)p')\ge p\,h(1)+(1-p)h(p') = (1-p)h(p')$ since $h(1)=0$.

**Lemma 4.** With $C_0=\{c:p_c\le 0.1\}$, $C_1=C_0^c$ and $\E[X]\le 0.01$:
$\Pr[C_0]^2 H(X\cup X'\mid C_0,C_0')\ge 1.26\,\Pr[C_0]H(X\mid C\in C_0)$.
Uses Lemma 2 and $\Pr[C_0]\ge 0.9$ (Markov: $\Pr[p_c>0.1]\le 0.01/0.1=0.1$).

**Lemma 5.** Under $\E[X]\le 0.01$:
$2\Pr[C_0,C_1']H(X\cup X'\mid C_0,C_1')\ge 1.62\,\Pr[C_1]H(X\mid C\in C_1)$.
Uses Lemma 3 with $p=p_c\le 0.1$ (so $1-p_c\ge 0.9$) and $\Pr[C_0]\ge 0.9$;
factor $2\cdot 0.9\cdot 0.9 = 1.62$.

**Assembly of Lemma 1.** Split $H(X\cup X'\mid C,C')$ into the three disjoint
region-events $\{C_0,C_0'\}$, $\{C_0,C_1'\}\cup\{C_1,C_0'\}$ (factor 2 by
symmetry), $\{C_1,C_1'\}$. Lemma 4 covers region 1, Lemma 5 region 2, region 3
is $\ge 0$ and discarded. Sum $\ge 1.26\,\Pr[C_0]H(X\mid C_0)+1.62\,\Pr[C_1]H(X\mid C_1)
\ge 1.26\,H(X\mid C)$ since $1.62\ge 1.26$ and
$H(X\mid C)=\Pr[C_0]H(X\mid C_0)+\Pr[C_1]H(X\mid C_1)$.

**Markov-region bound (Eq. 6).** $\Pr[p_c>0.1]\le \E_c[p_c]/0.1\le 0.01/0.1=0.1$,
hence $\Pr[C_0]\ge 0.9$.

**Constants / dependence.** $0.01$ is *not* optimized; any threshold $\mu$ with
the region constants re-tuned works. The sharp threshold is $\frac{3-\sqrt5}{2}\approx0.38$
(later work: Sawin, Chase–Lovett, Alweiss–Huang–Sellke), not reproduced here.
The eval asks only for $c\ge 0.01$.

**Common misuses.**
- Forgetting that $A,B$ must be **uniform** on $\mathcal F$ for $H(A)=\log|\mathcal F|$;
  for non-uniform $A$ the corollary's $H(A\cup B)\le H(A)$ step fails.
- Trying Jensen directly on $f(p,p')=h(p+p'-pp')-h(p)$ — *not convex in $p'$*
  (Gilmer §4); the region split is necessary.
- Dropping region 3 is legitimate (non-negative), but only because regions 1+2
  already exceed $H(X\mid C)$; do not claim region 3 is zero.
- Base of log: must be 2 consistently so $H(\text{uniform on }\mathcal F)=\log_2|\mathcal F|$.

**Project citation key.** `\cite{gilmer2022unionclosed}`.
