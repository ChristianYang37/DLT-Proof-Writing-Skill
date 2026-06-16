# Croot–Lev–Pach polynomial method (low-degree decomposition)

**Source.** Croot, Lev, Pach, "Progression-free sets in $\mathbb{Z}_4^n$ are
exponentially small," *Annals of Math.* 185 (2017), 331–337 (arXiv:1605.01506);
adapted to $\mathbb{F}_3^n$ by Ellenberg–Gijswijt (arXiv:1605.09223). Project key
`\cite{crootlevpach2017}`, `\cite{ellenberggijswijt2017}`.

**Setup.** $V$ = space of functions $\mathbb{F}_q^n\to\mathbb{F}_q$, identified
(via $x_i^q=x_i$ on $\mathbb{F}_q$, here $q=3$ so $x_i^3=x_i$, exponents reduce mod
"$\le 2$") with the space of multilinear-in-each-variable polynomials, i.e.
$\mathbb{F}_q$-span of monomials $\prod_i x_i^{a_i}$, $a_i\in\{0,1,\dots,q-1\}$.
Let $M_d$ = number of such monomials of total degree $\le d$, and let
$V_{\le d}=\operatorname{span}$ of those monomials, $\dim V_{\le d}=M_d$.

**Key lemma (CLP rank bound).** Let $P(x,y)=\sum_{(a,b)} c_{a,b}\,x^a y^b$ be a
polynomial on $\mathbb{F}_q^n\times\mathbb{F}_q^n$ of total degree $\le d$ (in the
$2n$ variables, with each individual exponent $\le q-1$). View its restriction to
the diagonal as a matrix $P\big(x,y\big)_{x,y}$. Then the number of monomials of
$P$ in which the $x$-part $x^a$ has degree $\le d/2$ plus the number in which the
$y$-part $y^b$ has degree $\le d/2$ bounds the matrix rank:
$$\operatorname{rank}\big(P(x,y)\big)_{x,y\in\mathbb{F}_q^n}\ \le\ 2\,M_{d/2}.$$
Reason: every monomial $x^a y^b$ of total degree $\le d$ has
$\deg x^a \le d/2$ OR $\deg y^b\le d/2$; group the sum accordingly into
$\sum_{\deg x^a\le d/2} x^a\,(\dots) + \sum_{\deg y^b\le d/2}(\dots)\,y^b$, each
group a sum of $\le M_{d/2}$ rank-one matrices.

**Slice-rank form (the one we use).** For a 3-variable tensor
$T(x,y,z)=\sum c_{a,b,c}\,x^a y^b z^c$ of total degree $\le d$ on
$(\mathbb{F}_q^n)^3$: every monomial $x^a y^b z^c$ with $\deg\le d$ has at least one
of $\deg x^a,\deg y^b,\deg z^c$ equal to $\le d/3$. Grouping by the smallest-degree
variable gives a slice decomposition with
$$\operatorname{sr}(T)\ \le\ 3\,M_{d/3},$$
where $M_{d/3}=\#\{\text{monomials of degree}\le d/3\}$ in $n$ variables with each
exponent $\le q-1$.

**Application to cap set ($q=3$, $d=2n$).** $T(x,y,z)=\mathbf{1}[x+y+z=0]=
\prod_{i=1}^n\big(1-(x_i+y_i+z_i)^2\big)$ on $\mathbb{F}_3^n$ (since $u^2=1$ iff
$u\ne 0$ in $\mathbb{F}_3$, so $1-u^2=\mathbf{1}[u=0]$). Each factor has degree $2$;
the product has total degree $2n$. With $d=2n$, $d/3=2n/3$, so
$$\operatorname{sr}(T)\le 3\,M_{2n/3}=3M_n,$$
where $M_n:=M_{2n/3}=\#\{a\in\{0,1,2\}^n:\sum_i a_i\le 2n/3\}$ (the prompt's $M_n$).

**Constants.** Factor $3$ = number of variables/slice-types; exact, not absorbed.
The degree threshold $2n/3 = d/3$ with $d=2n$ is exact.

**Common misuses.**
- Forgetting the reduction $x_i^3=x_i$ (so exponents live in $\{0,1,2\}$) — without
  it $M_n$ is wrong.
- Using $d/2$ (matrix/CLP form) instead of $d/3$ (slice form) — the 3-tensor split
  is by the *minimum* of three degrees, giving the threshold $d/3=2n/3$.
- Writing $\mathbf{1}[u=0]=1-u^2$ with the wrong sign or for $q\ne 3$.

**Project citation key.** `\cite{crootlevpach2017}`, `\cite{ellenberggijswijt2017}`.
