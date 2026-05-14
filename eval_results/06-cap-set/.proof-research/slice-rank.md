# Slice rank of a tensor

**Source.** Tao's blog "A symmetric formulation of the Croot–Lev–Pach–Ellenberg–Gijswijt capset bound" (2016); subsequent formalization in Naslund–Sawin (2017), Tao–Sawin (2016). The notion as used in the cap-set proof is canonical and folklore-level by 2017.

**Definition.** Let $V_1, V_2, V_3$ be finite sets and $F$ a field. A function $T: V_1 \times V_2 \times V_3 \to F$ is called a **slice** if it has one of the three forms:
- $T(x_1, x_2, x_3) = f(x_1) g(x_2, x_3)$ (an $x_1$-slice),
- $T(x_1, x_2, x_3) = f(x_2) g(x_1, x_3)$ (an $x_2$-slice),
- $T(x_1, x_2, x_3) = f(x_3) g(x_1, x_2)$ (an $x_3$-slice),
for some $f: V_i \to F$ and bivariate $g$.

The **slice rank** $\mathrm{sr}(T)$ is the smallest $r$ such that $T = \sum_{j=1}^r T_j$ with each $T_j$ a slice (in any of the three orientations).

**Key lemma (diagonal lower bound).** If $T$ is supported on the diagonal $\{(x,x,x): x \in A\}$ of $A^3$ — i.e. $T(x_1, x_2, x_3) = 0$ when $x_1, x_2, x_3$ are not all equal — and the diagonal values $T(x,x,x)$ are all nonzero for $x \in A$, then $\mathrm{sr}(T|_{A \times A \times A}) = |A|$.

**Proof sketch of the diagonal lower bound (used in cap-set).** Suppose $T = \sum_j T_j$ with $r$ slices. Project onto the first coordinate: each $x_1$-slice $f_j(x_1) g_j(x_2, x_3)$ contributes a function in $x_2, x_3$ on a subspace of dimension 1 in $x_1$ (after pulling out the $f_j$); collecting, we get a linear-algebra argument showing that if $r < |A|$, the diagonal cannot be filled. Formal proof: see Tao's blog post or Naslund–Sawin Prop 4.10.

**Hypotheses.** Field arbitrary (we use $\F_3$). Domain $V_1 = V_2 = V_3 = A$ (or $\F_3^n$ then restricted).

**Common usage.**
```latex
By the diagonal-lower-bound property of slice rank
(\Cref{lem:slice-rank-diagonal}), since $T|_{A \times A \times A}$ is a
nonzero diagonal tensor, $\mathrm{sr}(T|_{A \times A \times A}) \ge |A|$.
```

**Common misuses.**
- Confusing slice rank with tensor rank (slice rank $\le$ tensor rank but not equal).
- Applying the diagonal lower bound when the tensor is only "essentially diagonal" — the diagonal entries must be all nonzero on $A$.
- Forgetting that the three slice orientations are symmetric; the count $r$ is the total across all orientations.

**Project citation key.** \cite{Tao2016blog} (Tao's blog) or absorbed into \cite{EllenbergGijswijt2017} / \cite{CrootLevPach2017} for the cap-set application.
