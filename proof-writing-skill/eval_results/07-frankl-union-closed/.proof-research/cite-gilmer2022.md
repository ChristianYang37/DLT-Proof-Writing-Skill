# \cite{gilmer2022} — A constant lower bound for the union-closed sets conjecture

**Paper.** "A constant lower bound for the union-closed sets conjecture",
Justin Gilmer, arXiv:2211.09055v2, 28 Nov 2022 (Google Research, Brain Team).

**Exact theorems in PDF.**
- **Theorem 1 (p. 2).** Let $A,B$ be iid samples from a distribution over subsets of $[n]$.
  Assume $\Pr[i\in A] \le 0.01$ for all $i$. Then $H(A\cup B) \ge 1.26\, H(A)$.
- **Theorem 2 (p. 2).** Let $\mathcal{F} \subseteq 2^{[n]}$ be union-closed, $\mathcal{F}\ne\{\varnothing\}$.
  Then there exists $i\in[n]$ contained in at least a $0.01$ fraction of the sets in $\mathcal{F}$.

**Key technical lemma (Lemma 1, p. 4).** Let $C$ over $S$ finite, $\{p_c\}\subset[0,1]$,
$X|C{=}c \sim \mathrm{Bern}(p_c)$, $C'\overset{iid}{\sim} C$, $X'|C'{=}c \sim \mathrm{Bern}(p_{c})$
independent of $X,C$. If $\E[X] \le 0.01$ then $H(X\cup X' \mid C,C') \ge 1.26\, H(X\mid C)$.

Equivalent form (Eq. 5): assuming $\{p_c\}\subset[0,1]$ with $\E_c[p_c]\le 0.01=\mu$,
$$\E_{c,c'}[H(p_c + p_{c'} - p_c p_{c'})] \ge 1.26\, \E_c[H(p_c)].$$

**Subsidiary lemmas (p. 6-7).**
- **Lemma 2.** If $p,p' \le 0.1$ then $H(p+p'-pp') \ge 1.4 \cdot \tfrac{H(p)+H(p')}{2}$.
- **Lemma 3.** For any $p,p' \in [0,1]$: $H(p+p'-pp') \ge (1-p) H(p')$.
- **Lemma 4.** Under $\E[X]\le 0.01$: $\Pr[\mathcal{C}_0]^2 H(X\cup X'\mid \mathcal{C}_0,\mathcal{C}_0') \ge 1.26\, \Pr[\mathcal{C}_0] H(X\mid \mathcal{C}_0)$.
- **Lemma 5.** Under $\E[X]\le 0.01$: $2\Pr[\mathcal{C}_0,\mathcal{C}_1']H(X\cup X'\mid \mathcal{C}_0,\mathcal{C}_1') \ge 1.62\, \Pr[\mathcal{C}_1]H(X\mid \mathcal{C}_1)$.

**Proof strategy of Theorem 1 (p. 4).** Reveal bits one at a time and show
$H((A\cup B)_i \mid (A\cup B)_{<i}) \ge 1.26 H(A_i \mid A_{<i})$ for each $i$.
Two key tools:
1. Property: $(A\cup B)_{<i}$ is a deterministic function of $(A_{<i},B_{<i})$, so
   $H((A\cup B)_i \mid (A\cup B)_{<i}) \ge H((A\cup B)_i \mid A_{<i},B_{<i})$ (data-processing).
2. Apply Lemma 1 with $C=A_{<i}$, $C'=B_{<i}$, $X = A_i$, $X' = B_i$.
Then sum over $i$ by chain rule.

**Proof strategy of Theorem 2.** If $A,B$ iid uniform on union-closed $\mathcal{F}$ then
$A\cup B$ has support in $\mathcal{F}$ so $H(A\cup B) \le \log|\mathcal{F}| = H(A)$.
Combined with Theorem 1 (which would force $H(A\cup B) \ge 1.26 H(A) > H(A)$ when $H(A)>0$),
some element must satisfy $\Pr[i\in A]>0.01$.

**Constants in $\mathcal{C}_0,\mathcal{C}_1$ partition.** $\mathcal{C}_0 := \{c : p_c \le 0.1\}$, $\mathcal{C}_1 := \mathcal{C}_0^c$.
By Markov on $\E[p_c]\le 0.01$: $\Pr[\mathcal{C}_1] \le 0.01/0.1 = 0.1$, so $\Pr[\mathcal{C}_0] \ge 0.9$.

**Lemma 2 proof sketch (p. 6).** Concavity of $H$ gives $\tfrac{H(p)+H(p')}{2} \le H(\tfrac{p+p'}{2})$.
For $p,p'\le 0.1$, $p+p'-pp' \ge 0.9(p+p')$. So
$\tfrac{2H(p+p'-pp')}{H(p)+H(p')} \ge \tfrac{H(0.9(p+p'))}{H(0.5(p+p'))}$.
Function $g(p)=H(0.9p)/H(0.5p)$ on $(0,0.2]$ is minimized at $p=0.2$ giving $g(0.2)>1.45 > 1.4$.

**Project .bib key.** \cite{gilmer2022}

**Citation discipline.** Use form `\begin{X}[\cite{gilmer2022}]` only for results we restate verbatim from the paper. Our own re-proof of Theorems 1, 2, and Lemmas 1-5 follows the paper line-by-line and is presented in main text (form 1: theorem-then-proof in same file).
