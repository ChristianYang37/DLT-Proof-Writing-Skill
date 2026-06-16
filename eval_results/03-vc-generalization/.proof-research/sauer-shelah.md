# Sauer–Shelah lemma (growth function vs. VC dimension)

**Source.** Sauer (1972); Shelah (1972); textbook proofs: Shalev-Shwartz–Ben-David,
*Understanding Machine Learning* (2014), Lemma 6.10 (shifting); Mohri et al.
(2018) Thm 3.17; Bousquet–Boucheron–Lugosi survey. Project keys:
`\cite{shalev2014understanding}`, `\cite{mohri2018foundations}`.

**Statement.** For a class $\mathcal H\subset\{0,1\}^{\mathcal X}$ with
$\mathrm{VC}(\mathcal H)=d<\infty$, the growth function (shatter coefficient)
$$\Pi_{\mathcal H}(n):=\max_{x_1,\dots,x_n\in\mathcal X}
   \big|\{(h(x_1),\dots,h(x_n)):h\in\mathcal H\}\big|$$
satisfies, for all $n$,
$$\Pi_{\mathcal H}(n)\le \sum_{i=0}^d\binom{n}{i}=\binom{n}{\le d}.$$
Moreover for $n\ge d\ge 1$, $\sum_{i=0}^d\binom ni\le(en/d)^d$, hence
$\log\Pi_{\mathcal H}(n)\le d\log(en/d)=d\log(n/d)+d$.

**Hypotheses.** $\mathrm{VC}(\mathcal H)\le d$; no shattered set of size $d+1$.
Pure combinatorics — no probability.

**Proof technique (downward shifting / Pajor's induction).** Show the stronger
claim: for any finite $A\subseteq\mathcal X$, $|\mathcal H_{|A}|\le|\{B\subseteq A:
\mathcal H\text{ shatters }B\}|$. Induct on $|A|$ via the shift operator $T_x$
that flips $h(x)$ from $1$ to $0$ when the flipped pattern is not already
present; shifting does not increase the projection size and only removes
shattered sets that contain $x$. Since $\mathcal H$ has no shattered set of size
$>d$, the number of shattered subsets is $\le\sum_{i=0}^d\binom ni$. **This is a
genuinely combinatorial (set-counting) argument — its write-up is prose-bound, so
the lemma's proof carries `% lint: ignore R19`.**

**Constants / dimension dependence.** Bound $(en/d)^d$ valid for $n\ge d$; for
$n<d$ use the trivial $\Pi_{\mathcal H}(n)\le 2^n$. The $+d$ additive term is
absorbed into the universal constant in the final rate.

**Canonical use pattern.**
```latex
By \Cref{lem:sauer-shelah}, $\Pi_{\mathcal H}(2n)\le(2en/d)^d$, so
$\log\Pi_{\mathcal H}(2n)\le d\log(2en/d)\le C\,d\log(n/d)$ for $n\ge d$.
```

**Common misuses.**
- Stating $\Pi_{\mathcal H}(n)\le n^d$ and then claiming $d\log(n/d)$ — the
  cleaner $d\log(n/d)$ needs the $(en/d)^d$ form, not $n^d$.
- Applying at sample size $n$ when the double sample $S\cup S'$ has size $2n$ —
  the projection that Massart sees has cardinality $\Pi_{\mathcal H}(2n)$, not
  $\Pi_{\mathcal H}(n)$.
- Confusing growth function of $\mathcal H$ with that of the loss class; for 0/1
  loss against fixed labels they coincide up to the same VC dimension.

**Project citation key.** `\cite{shalev2014understanding}`
