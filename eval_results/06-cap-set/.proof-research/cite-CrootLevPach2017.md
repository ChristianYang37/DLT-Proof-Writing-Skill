# \cite{CrootLevPach2017} — Croot–Lev–Pach polynomial method on $(\Z/4\Z)^n$

**Paper.** "Progression-free sets in $\Z_4^n$ are exponentially small", Ernie Croot, Vsevolod F. Lev, Péter Pál Pach, *Annals of Mathematics*, 185 (2017), 331–337. arxiv: 1605.01506.

**Status.** Published version: Ann. of Math., Vol. 185 (2017), Issue 1, pp. 331–337. DOI: 10.4007/annals.2017.185.1.7.

**Key innovation.** The polynomial-method gambit later refined into slice rank: any polynomial $P(x,y)$ on $(\Z/4\Z)^n$ of degree $\le d$ can be written as $\sum_i F_i(x) G_i(y)$ with the number of summands bounded by twice the dimension of the degree-$\le d/2$ monomial space. This bounds the rank of any matrix on a progression-free set indexed by $A \times A$.

**Hypotheses (Lemma 1 of CLP, the key technical lemma).** For the group $G = (\Z/4\Z)^n$ (and analogous statements hold for $\F_q^n$, $q$ odd prime, used in EG): if $P: G \times G \to F$ comes from a polynomial of total degree $\le d$, then $\operatorname{rank}(P|_{S \times S}) \le 2 |\{m: \deg m \le d/2\}|$ for any $S \subseteq G$.

**Statement (paraphrased from arxiv v1).** *Theorem 1.* For every $n \ge 1$, every subset $A \subseteq (\Z/4\Z)^n$ with no three-term arithmetic progression has $|A| \le C \cdot c^n$ with $c < 4$ (explicit $c \approx 3.611$).

**Constants / dimension dependence.** The bound is genuinely exponential with base strictly less than the trivial $|G|^{1/n} = 4$.

**Project .bib key.** `CrootLevPach2017`.

**Note on use in cap-set proof.** Ellenberg-Gijswijt adapted the CLP polynomial argument to $\F_3^n$, and the exact algebraic step we invoke — "a polynomial of degree $\le d$ on $\F_3^n$ factors through its low-degree monomial restrictions" — is the CLP Lemma transposed.
