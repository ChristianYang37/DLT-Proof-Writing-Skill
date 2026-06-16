# Dependency graph — Gilmer union-closed bound

Topological order (leaves first). Each lemma's `Downstream consumers` is
non-empty (Occam pass passed). Base-2 logarithm throughout; $h(\cdot)$ is the
scalar binary-entropy function, $H(\cdot)$ the Shannon entropy.

## fac:entropy-facts (Fact, cited)
**Statement (1-line):** Max-entropy on finite support ($H(Z)\le\log|\mathcal F|$,
equality iff uniform), chain rule, and data-processing facts from Cover–Thomas.
**Hypotheses:** finite/discrete support.
**Downstream consumers:** lem:cond-mono (data processing), thm:gilmer-entropy
(chain rule), thm:gilmer-frankl (max-entropy). Cited via `[\cite{coverthomas2006}]`.

## lem:cond-mono (Lemma)
**Statement (1-line):** $H(X\mid Y)\le H(X\mid f(Y))$ for any function $f$.
**Hypotheses:** $X\to Y\to f(Y)$ Markov (automatic).
**Downstream consumers:** thm:gilmer-entropy (the crucial Eq. (2) step).

## lem:concavity-half (Lemma 2)
**Statement (1-line):** $p,p'\le 0.1 \Rightarrow h(p+p'-pp')\ge 1.4\cdot\frac{h(p)+h(p')}{2}$.
**Hypotheses:** $p,p'\in[0,0.1]$; concavity of $h$.
**Downstream consumers:** lem:region-low.

## lem:concavity-mix (Lemma 3)
**Statement (1-line):** $h(p+p'-pp')\ge (1-p)h(p')$ for all $p,p'\in[0,1]$.
**Hypotheses:** concavity of $h$, $h(1)=0$.
**Downstream consumers:** lem:region-mix.

## lem:region-low (Lemma 4)
**Statement (1-line):** $\Pr[C_0]^2 H(X\cup X'\mid C_0,C_0')\ge 1.26\,\Pr[C_0]H(X\mid C_0)$.
**Hypotheses:** $\E[X]\le 0.01$; uses lem:concavity-half + Markov ($\Pr[C_0]\ge 0.9$).
**Downstream consumers:** lem:single-var (region 1).

## lem:region-mix (Lemma 5)
**Statement (1-line):** $2\Pr[C_0,C_1']H(X\cup X'\mid C_0,C_1')\ge 1.62\,\Pr[C_1]H(X\mid C_1)$.
**Hypotheses:** $\E[X]\le 0.01$; uses lem:concavity-mix + $\Pr[C_0]\ge 0.9$, $p_c\le0.1$.
**Downstream consumers:** lem:single-var (region 2).

## lem:single-var (Lemma 1, key technical)
**Statement (1-line):** $\E_c[p_c]\le 0.01 \Rightarrow \E_{c,c'}[h(p_c+p_{c'}-p_cp_{c'})]\ge 1.26\,\E_c[h(p_c)]$,
equivalently $H(X\cup X'\mid C,C')\ge 1.26\,H(X\mid C)$.
**Hypotheses:** $C,C'$ i.i.d. finite; conditional Bernoulli; $\E[X]\le 0.01$.
**Downstream consumers:** thm:gilmer-entropy (per-coordinate inequality (1)/(3)).

## thm:gilmer-entropy (Theorem 1)
**Statement (1-line):** $A,B$ i.i.d., $\Pr[i\in A]\le 0.01\ \forall i$
$\Rightarrow H(A\cup B)\ge 1.26\,H(A)$.
**Hypotheses:** marginal cap; uses lem:cond-mono, lem:single-var, chain rule.
**Downstream consumers:** thm:gilmer-frankl.

## thm:gilmer-frankl (Theorem 2, main combinatorial result)
**Statement (1-line):** $\mathcal F$ union-closed, $|\mathcal F|\ge 2$
$\Rightarrow \exists i: |\{A\in\mathcal F: i\in A\}|\ge 0.01\,|\mathcal F|$.
**Hypotheses:** union-closure, $|\mathcal F|\ge 2$; uses thm:gilmer-entropy +
max-entropy fact.
**Downstream consumers:** (headline result — the eval target).

## File layout (R5: theorem + proof co-located)
- sections/01-preliminaries.tex — notation, def union-closed, def binary entropy,
  fac:entropy-facts (cited), the universal-constant convention sentence.
- sections/02-cond-entropy-monotone.tex — lem:cond-mono + proof.
- sections/03-single-variable-bounds.tex — lem:concavity-half, lem:concavity-mix
  (each + immediate proof). [Two lemmas, each with its own immediate proof — R5 ok.]
- sections/04-region-bounds.tex — lem:region-low, lem:region-mix (each + proof).
- sections/05-key-lemma.tex — lem:single-var + proof (assembles regions).
- sections/06-main-theorem.tex — thm:gilmer-entropy + proof (chain rule).
- sections/07-frankl-corollary.tex — thm:gilmer-frankl + proof (max-entropy
  contradiction).
