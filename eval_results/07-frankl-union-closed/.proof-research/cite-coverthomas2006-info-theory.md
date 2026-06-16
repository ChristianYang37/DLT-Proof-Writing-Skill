# \cite{coverthomas2006} — Cover & Thomas, Elements of Information Theory

**Paper.** Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*,
2nd edition, Wiley-Interscience, 2006 (1st ed. 1991; Gilmer cites the 1999
printing). Standard graduate text.

**Facts used in this proof (all textbook-standard).**

1. **Maximum entropy on a finite support.** For a random variable $Z$ taking
   values in a finite set $\mathcal F$, $H(Z)\le \log|\mathcal F|$, with equality
   iff $Z$ is uniform on $\mathcal F$. Gilmer (arXiv:2211.09055) cites this as
   "[6] Theorem 2.6.4". Base-2 logarithm.

2. **Chain rule for entropy.** For a sequence $X_1,\dots,X_n$ with
   $X_{<i}=(X_1,\dots,X_{i-1})$,
   $H(X_1,\dots,X_n)=\sum_{i=1}^n H(X_i\mid X_{<i})$.
   (Cover–Thomas, Theorem 2.5.1.)

3. **Data-processing inequality.** If $X\to Y\to Z$ is a Markov chain then
   $I(X;Z)\le I(X;Y)$. Consequence used here: for any function $f$,
   $H(X\mid Y)\le H(X\mid f(Y))$, because $X\to Y\to f(Y)$ is Markov and
   $I(X;f(Y))\le I(X;Y)$ rearranges to the conditional-entropy inequality.
   (Cover–Thomas, Theorem 2.8.1 region.)

4. **Concavity of binary entropy.** $h(p)=-p\log p-(1-p)\log(1-p)$ is concave
   on $[0,1]$ with $h(0)=h(1)=0$. (Standard; Cover–Thomas §2.)

**Hypotheses.** All require only finite support / discrete variables, which hold
throughout (subsets of $[n]$, Bernoulli bits).

**Constants / dimension dependence.** None; these are exact identities /
inequalities, base-2 log.

**Project .bib key.** `\cite{coverthomas2006}`.
