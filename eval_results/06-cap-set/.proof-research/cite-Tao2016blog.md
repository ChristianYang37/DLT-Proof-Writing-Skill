# \cite{Tao2016blog} — Tao's symmetric formulation via slice rank

**Paper.** Blog post: "A symmetric formulation of the Croot-Lev-Pach-Ellenberg-Gijswijt capset bound", Terence Tao, May 18, 2016. URL: https://terrytao.wordpress.com/2016/05/18/a-symmetric-formulation-of-the-croot-lev-pach-ellenberg-gijswijt-capset-bound/

**Status.** Blog post; not peer-reviewed but widely cited as the standard reference for the slice-rank formulation. Folded into Naslund-Sawin (2017) for the formal write-up.

**Key contribution.** Introduces the **slice rank** of a $k$-tensor as a generalization of matrix rank, and gives the lemma: a diagonal tensor whose diagonal entries are all nonzero on a set $A$ has slice rank exactly $|A|$. This is the lower bound used in the cap-set proof.

**Statement of the diagonal lower bound (paraphrased).** Let $V$ be a finite set and $T: V \times V \times V \to F$ be a 3-tensor with $T(x,y,z) = 0$ for $(x,y,z)$ not on the diagonal $x=y=z$. If $T(x,x,x) \ne 0$ for all $x \in V$, then $\mathrm{sr}(T) = |V|$.

**Proof technique.** Induction on the slice rank; pull out one slice at a time and reduce to a smaller diagonal tensor.

**Project .bib key.** `Tao2016blog`.

**Note.** The slice-rank machinery is folklore — versions appear earlier in tensor literature. The capset-application labeling is due to Tao 2016.
