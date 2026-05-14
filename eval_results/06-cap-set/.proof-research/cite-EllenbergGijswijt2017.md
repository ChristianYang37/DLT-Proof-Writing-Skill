# \cite{EllenbergGijswijt2017} — Cap-set upper bound

**Paper.** "On large subsets of $\F_q^n$ with no three-term arithmetic progression", Jordan S. Ellenberg, Dion Gijswijt, *Annals of Mathematics*, 185 (2017), 339–343. arxiv: 1605.09223.

**Status.** Published version: Ann. of Math., Vol. 185 (2017), Issue 1, pp. 339–343. DOI: 10.4007/annals.2017.185.1.8.

**Main theorem.** *Theorem 1.* Let $q$ be a fixed odd prime power. Then any subset of $\F_q^n$ containing no three-term arithmetic progression has size at most $3 N$, where $N$ is the number of monomials $\prod_{i=1}^n x_i^{a_i}$ with $0 \le a_i \le q-1$ and $\sum_i a_i \le n(q-1)/3$.

**Cap-set specialization ($q=3$).** Theorem 1 of [Ellenberg-Gijswijt 2017] with $q=3$: $|A| \le 3 M_n$ where $M_n = |\{(a_1,\dots,a_n) \in \{0,1,2\}^n : \sum a_i \le 2n/3\}|$.

**Asymptotic.** They show $M_n^{1/n} \to 3\gamma$ where $\gamma = \frac{1}{6}(\alpha^{-2n/3}(\alpha^3+\alpha+1)/3)$ via an entropy / Chernoff calculation; numerically $3\gamma < 2.7558$, so $|A| \le C \cdot 2.7558^n$.

The relevant numerical fact, from their paper (and re-derived in Tao's blog post):
$$
M_n \le 3^{n} \cdot \exp\Big( -n \cdot I(1/3) \Big)
$$
where $I$ is the large-deviation rate function for the sum $\sum a_i$ with $a_i$ uniform on $\{0,1,2\}$. The explicit answer is the unique $\gamma \in (0, 1)$ with $\gamma = (1 + \alpha + \alpha^2)/3$ at the saddle-point value of $\alpha$ that solves the entropy optimization; this yields $3\gamma \approx 2.7551$.

**Hypotheses.** Field $\F_q$ with $q$ odd; no other assumptions on $A$ beyond being 3-AP-free.

**Proof structure (as we follow).**
1. Define the tensor $T(x,y,z) = \delta_{x+y+z=0}$ on $\F_3^n$, and consider $T|_{A^3}$.
2. The slice-rank upper bound: $T(x,y,z) = \mathbf{1}[x+y+z=0]$ can be expressed using the polynomial identity $\prod_i (1 - (x_i+y_i+z_i)^2)$ (for $\F_3$), expanded and re-grouped by which variable carries the highest-degree factor; this yields a sum of $3 M_n$ slices.
3. The slice-rank lower bound: $A$ being 3-AP-free means $x+y+z=0$ in $A^3$ forces $x=y=z$, so $T|_{A^3}$ is diagonal with nonzero entries; slice rank $\ge |A|$.
4. Combine: $|A| \le 3 M_n$.

**Project .bib key.** `EllenbergGijswijt2017`.

**Note on Tao's reformulation.** The "slice rank" reformulation of CLP/EG appeared in Tao's blog (May 2016, shortly after both arxiv preprints). The proof we write uses this cleaner formulation but the result is exactly Ellenberg-Gijswijt Theorem 1 with $q=3$.
