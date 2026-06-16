# Dependency graph — Hoeffding's inequality

The shallowest tree that fits: one auxiliary lemma feeding the main theorem.

## lem:hoeffding
**Statement (1-line):** A centered random variable $Y\in[a,b]$ a.s. satisfies
$\E[e^{\lambda Y}]\le \exp(\lambda^2(b-a)^2/8)$ for all $\lambda\in\R$.
**Hypotheses:** $\E[Y]=0$, $Y\in[a,b]$ a.s.
**Technique digest:** .proof-research/hoeffding-lemma.md
**Downstream consumers:** thm:hoeffding (cite-site: MGF factorization step in the
proof of the main theorem — bounds each per-coordinate factor
$\E[e^{\lambda(X_i-\E X_i)}]$).

## thm:hoeffding
**Statement (1-line):** For independent $X_i\in[a_i,b_i]$ and $S_n=\sum_i X_i$,
$\Pr[|S_n-\E S_n|\ge t]\le 2\exp(-2t^2/\sum_i(b_i-a_i)^2)$.
**Hypotheses:** $X_1,\dots,X_n$ independent; $X_i\in[a_i,b_i]$ a.s.; $t>0$.
**Depends on:** lem:hoeffding.
**Downstream consumers:** (root) — the headline result.

## Occam check
Both nodes have non-empty downstream consumers (lem:hoeffding → thm:hoeffding;
thm:hoeffding is the root). No orphan lemmas. No unused definitions. No
citations required (self-contained). Tree depth = 2, which is minimal for a
"lemma + theorem" assembly.
