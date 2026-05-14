# Cover & Thomas — Elements of Information Theory

**Source.** Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley, 2006. (Gilmer cites the 1999 1st edition; both contain the relevant facts.)

**Facts used in our proof.**

1. **Chain rule for entropy.** For random variables $X_1, \ldots, X_n$ taking values in finite sets,
$$H(X_1, \ldots, X_n) = \sum_{i=1}^{n} H(X_i \mid X_{<i}),$$
where $X_{<i} := (X_1, \ldots, X_{i-1})$ (and $X_{<1}$ is the empty tuple, so $H(X_1\mid X_{<1}) = H(X_1)$). (Cover-Thomas Theorem 2.5.1.)

2. **Data-processing inequality.** If $X \to Y \to Z$ forms a Markov chain (i.e., $X$ and $Z$ are conditionally independent given $Y$), then $I(X;Z) \le I(X;Y)$. In particular, for any function $f$, the chain $X \to Y \to f(Y)$ is Markov, so
$$I(X; f(Y)) \le I(X; Y) \quad\Longleftrightarrow\quad H(X \mid Y) \le H(X \mid f(Y)).$$
(Cover-Thomas Theorem 2.8.1.)

3. **Conditioning reduces entropy.** $H(X\mid Y) \le H(X)$, with equality iff $X$ and $Y$ are independent. (Cover-Thomas Theorem 2.6.5.)

4. **Uniform distribution maximizes entropy.** For a random variable $X$ supported on a finite set $\mathcal{X}$, $H(X) \le \log|\mathcal{X}|$, with equality iff $X$ is uniform on $\mathcal{X}$. (Cover-Thomas Theorem 2.6.4.)

5. **Concavity of binary entropy.** The function $h(p) := -p \log p - (1-p)\log(1-p)$ is concave on $[0,1]$. (Direct calculation: $h''(p) = -\tfrac{1}{(\ln 2)\, p(1-p)} < 0$.)

6. **Bernoulli entropy formula.** For $X \sim \mathrm{Bern}(p)$, $H(X) = h(p)$. Independence of $X, X' \sim \mathrm{Bern}(p), \mathrm{Bern}(p')$ gives $\Pr[\max(X,X')=1] = p+p'-pp'$, so $H(X \cup X') = h(p+p'-pp')$ where $X \cup X' := \max(X,X')$.

**Project .bib key.** \cite{cover2006elements}
