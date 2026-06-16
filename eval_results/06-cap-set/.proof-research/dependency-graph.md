# Dependency graph — Ellenberg–Gijswijt cap-set bound

Target: `thm:cap-set` — $A\subseteq\mathbb{F}_3^n$ 3-AP-free $\Rightarrow
|A|\le 3M_n$, $M_n=\#\{a\in\{0,1,2\}^n:\sum a_i\le 2n/3\}$.

Two-sided bound on a single invariant: the slice rank of
$T(x,y,z)=\mathbf{1}[x+y+z=0]$ restricted to $A^3$.
$|A|\overset{\text{lower}}{\le}\operatorname{sr}(T|_{A^3})\overset{\text{upper}}{\le}3M_n.$

## lem:slice-rank-def
**Statement (1-line):** Defines slice rank of a $k$-tensor over a field and proves
(a) subadditivity and (b) a diagonal tensor with $D$ nonzero diagonal entries has
slice rank exactly $D$.
**Hypotheses:** none beyond a field $\mathbb{F}$ and finite index sets; part (b)
needs nonzero diagonal entries.
**Downstream consumers:** lem:upper (uses subadditivity to add slice counts),
lem:lower (uses the diagonal lower bound), thm:cap-set indirectly.
**Digest:** slice-rank.md; cite-bccgnsu2017-slicerank.md, cite-tao2016slicerank-blog.md.

## lem:monomial-count
**Statement (1-line):** $M_n:=\#\{a\in\{0,1,2\}^n:\sum a_i\le 2n/3\}$ satisfies, for
every $x\in(0,1]$, $M_n\le x^{-2n/3}(1+x+x^2)^n$; hence
$\limsup_n M_n^{1/n}\le\min_{0<x\le1}(1+x+x^2)x^{-2/3}=3\gamma$ with $3\gamma<2.7558$.
**Hypotheses:** none (pure counting / Cramér bound).
**Downstream consumers:** cor:numerical (turns $|A|\le 3M_n$ into $|A|\le C(2.7558)^n$).
**Digest:** monomial-counting-asymptotic.md; cite-ellenberggijswijt2017-capset.md
(for the closed-form minimizer value).

## lem:upper
**Statement (1-line):** For the indicator tensor
$T(x,y,z)=\mathbf{1}[x+y+z=0]=\prod_i(1-(x_i+y_i+z_i)^2)$ on $(\mathbb{F}_3^n)^3$,
$\operatorname{sr}(T)\le 3M_n$ via the low-degree-monomial slice decomposition
(threshold $2n/3=d/3$, $d=2n$).
**Hypotheses:** $T$ as above (polynomial of total degree $2n$, each var-exponent
$\le 2$). Uses lem:slice-rank-def(a).
**Downstream consumers:** thm:cap-set (upper side).
**Digest:** clp-polynomial-method.md; cite-crootlevpach2017-z4n.md,
cite-ellenberggijswijt2017-capset.md.

## lem:lower
**Statement (1-line):** If $A\subseteq\mathbb{F}_3^n$ is 3-AP-free, then
$T|_{A^3}(x,y,z)=\mathbf{1}[x=y=z]$ (a diagonal tensor with $|A|$ nonzero entries),
so $\operatorname{sr}(T|_{A^3})=|A|$; in particular $\ge|A|$.
**Hypotheses:** no-3-AP property: $x+y+z=0,\ x,y,z\in A\Rightarrow x=y=z$. Uses
lem:slice-rank-def(b).
**Downstream consumers:** thm:cap-set (lower side).
**Digest:** slice-rank.md.

## thm:cap-set
**Statement (1-line):** $|A|\le 3M_n$. 3-line proof: $|A|=\operatorname{sr}(T|_{A^3})$
(lem:lower) $\le\operatorname{sr}(T)$ restricted (monotonicity under restriction is
folded into lem:upper bounding $T$ on all of $\mathbb{F}_3^n$ then restricting),
$\le 3M_n$ (lem:upper).
**Hypotheses:** ass:capset.
**Downstream consumers:** cor:numerical.

## cor:numerical
**Statement (1-line):** $|A|\le C\cdot(2.7558)^n$ for an absolute $C$, equivalently
$\limsup|A|^{1/n}\le 3\gamma<2.7558$.
**Hypotheses:** thm:cap-set + lem:monomial-count.
**Downstream consumers:** (terminal — the headline numerical statement; consumed by
the reader / abstract, which is out of scope). Kept because the prompt explicitly
requests it as a corollary/remark.

## Restriction subtlety (resolved)
$\operatorname{sr}(T|_{A^3})\le\operatorname{sr}(T)$ holds because restricting each
slice $f(x_i)g(\dots)$ to $A$ in every coordinate gives a slice of $T|_{A^3}$;
slice count cannot increase. So we may bound $\operatorname{sr}(T)$ on all of
$\mathbb{F}_3^n$ (lem:upper) and restrict. This monotonicity is stated as
lem:slice-rank-def part (c) to keep thm:cap-set a clean 3-line citation.
