# \cite{tao2016slicerank} — Tao's symmetric slice-rank exposition

**Paper.** Terence Tao, "A symmetric formulation of the Croot–Lev–Pach–
Ellenberg–Gijswijt capset bound," blog post, terrytao.wordpress.com, 17 May 2016.
(Widely cited as the origin of the "slice rank" name and the clean diagonal
lower-bound argument.)

**Exact name in PDF/post.** "Lemma 1" (diagonal tensor has slice rank equal to the
number of nonzero diagonal entries) and the surrounding definition of slice rank.

**Statement (faithfully paraphrased).** Define the slice rank of
$T:X^k\to\mathbb{F}$ as the minimal number of functions of the form
$x_i\mapsto f(x_i)$ times a function of the other coordinates whose sum is $T$.
Lemma: a diagonal tensor $\sum_{a\in X}c_a\,\mathbf{1}[x_1=\dots=x_k=a]$ with
$c_a\ne 0$ for all $a$ has slice rank exactly $|X|$. Proof by induction /
linear-algebra: any decomposition into $<|X|$ slices yields a nonzero vector in
the kernel of the relevant coordinate functions, forcing a vanishing diagonal
entry — contradiction.

**Hypotheses.** Diagonal, all nonzero entries. Field arbitrary.

**Constants / dimension dependence.** Exact equality $\operatorname{sr}=|X|$.

**Project .bib key.** `\cite{tao2016slicerank}`.
