# Slice rank of a tensor (polynomial method)

**Source.** Tao, "A symmetric formulation of the Croot–Lev–Pach–Ellenberg–Gijswijt
capset bound" (blog, 2016); formalized in Blasiak–Church–Cohn–Grochow–Naslund–
Sawin–Umans, *Discrete Analysis* 2017:3 (arXiv:1605.06702). Project key
`\cite{bccgnsu2017}` and `\cite{tao2016slicerank}`.

**Definition (slice rank).** Let $\mathbb{F}$ be a field and $X_1,\dots,X_k$ finite
sets. A function $T:\prod_j X_j \to \mathbb{F}$ is a **slice** (or "rank-one slice")
if there is an index $i \in [k]$ and functions $f:X_i\to\mathbb{F}$,
$g:\prod_{j\ne i}X_j \to \mathbb{F}$ with
$$T(x_1,\dots,x_k) = f(x_i)\, g(x_1,\dots,\hat{x_i},\dots,x_k).$$
The **slice rank** $\operatorname{sr}(T)$ is the least $r$ such that $T$ is a sum
of $r$ slices. (For $k=2$ this is ordinary matrix rank.)

**Property 1 — Subadditivity.** $\operatorname{sr}(T_1+T_2)\le
\operatorname{sr}(T_1)+\operatorname{sr}(T_2)$, and $\operatorname{sr}(\lambda T)=
\operatorname{sr}(T)$ for $\lambda\ne 0$. Immediate from the definition (concatenate
slice decompositions).

**Property 2 — Diagonal lower bound (Tao's lemma).** Let $X$ be finite and
$T:X^k\to\mathbb{F}$ a *diagonal* tensor: $T(x_1,\dots,x_k)=\sum_{x\in X'}
c_x\,\mathbf{1}[x_1=\dots=x_k=x]$ for some $X'\subseteq X$ and nonzero scalars
$c_x\ (x\in X')$. Then $\operatorname{sr}(T)=|X'|$. In particular the identity-type
tensor on $A$ with all $c_x\ne 0$ has slice rank exactly $|A|$.
  Proof idea (the part we reproduce): the $\le$ direction is the obvious
  decomposition $\sum_{x\in X'} c_x \mathbf{1}[x_1=x]\cdot\mathbf{1}[x_2=\dots=x_k=x]$.
  The $\ge$ direction is the crux: suppose $T=\sum_{i=1}^r f_i^{(j_i)}\otimes(\cdots)$
  with $r<|X'|$. By a pigeonhole/dimension count, there are at most $r$ slices, and
  one can find a function $v:X'\to\mathbb{F}$, not identically zero, that is
  orthogonal to all the $f_i$ associated to the $k$-th (say) coordinate; contracting
  $T$ against $v$ in the appropriate coordinates yields a smaller diagonal tensor
  that must vanish — contradiction. Formal statement: for a diagonal tensor with
  $|X'|$ nonzero diagonal entries, any slice decomposition has $\ge|X'|$ terms.
  (See Tao 2016 / BCCGNSU 2017 Lemma; reproduced as `lem:slice-rank-def` part (b).)

**Constants / dimension dependence.** No hidden constants; $\operatorname{sr}$ is
an integer in $[0,\min_j|X_j|\cdot\text{(...)}]$. Diagonal lower bound is exact.

**Canonical use pattern (cap set).** $T(x,y,z)=\mathbf{1}[x+y+z=0]$ on $A^3$,
$A\subseteq\mathbb{F}_3^n$. Restricted to $A^3$ with the no-3-AP property,
$x+y+z=0\Rightarrow x=y=z$, so $T|_{A^3}(x,y,z)=\mathbf{1}[x=y=z]$ — a diagonal
tensor with all entries $1$, hence $\operatorname{sr}(T|_{A^3})=|A|$ (Property 2).

**Common misuses.**
- Confusing slice rank with tensor (CP) rank — they differ for $k\ge 3$; slice
  rank is always $\le$ CP rank and is the right notion here.
- Forgetting the diagonal entries must be *nonzero* for the lower bound $=|X'|$.
- Applying Property 2 to a non-diagonal tensor (the no-3-AP property is exactly
  what makes the restricted tensor diagonal).

**Project citation key.** `\cite{tao2016slicerank}`, `\cite{bccgnsu2017}`.
