# Autonomous setting decisions (eval / headless mode)

Per `socratic-intake.md` step 6: running with no interactive user, the stronger/tighter
default was adopted for each Socratic-intake dimension and recorded here (not as inline
`\todo`). One block per decision.

## target-form
**Chosen:** Prove $|A| \le 3M_n$ rigorously AND state the explicit numerical corollary $|A| \le C\cdot(2.7558)^n$ (with the $M_n^{1/n}\to 3\gamma$ asymptotic sketched) — strongest win the task supports, and the eval prompt explicitly asks for the numerical consequence.
**Alternative:** Stop at the combinatorial bound $|A| \le 3M_n$ and only remark on the asymptotic.
**Reversible:** yes — drop `cor:numerical` and the monomial-counting asymptotic section; the core two-sided slice-rank argument is untouched.

## cap-condition-form
**Chosen:** Algebraic form — $A$ is 3-AP-free iff the only solutions of $x+y+z=0$ with $x,y,z\in A$ are the diagonal $x=y=z$ — this is the exact algebraic hypothesis the slice-rank lower bound consumes, so it is the tightest framing.
**Alternative:** Geometric "no three distinct collinear points" phrasing, then translate to the algebraic condition.
**Reversible:** yes — swap the assumption-block wording and add one translation remark; the lower-bound lemma proof is unchanged because it already uses $x+y+z=0$.

## slice-rank-generality
**Chosen:** Define slice rank over an arbitrary field and prove subadditivity + the diagonal lower bound in that generality; specialize to $\mathbb{F}_3$ only at the cap-set application — stronger because the properties are field-agnostic and the general lemma is reusable.
**Alternative:** Work entirely over $\mathbb{F}_3$.
**Reversible:** yes — replace "$\mathbb{F}$" by "$\mathbb{F}_3$" in `lem:slice-rank-def`; no proof step depends on field generality.

## upper-bound-constant
**Chosen:** Exact $3M_n$, tracking the factor $3$ explicitly (the three slice-types from which variable's monomial-degree is low) — sharp constant, not an absorbed asymptotic.
**Alternative:** An absorbed $O(M_n)$.
**Reversible:** yes — relax the statement of `lem:upper` to $O(M_n)$ and drop the factor-3 bookkeeping; downstream the corollary's base constant would degrade.

## decomposition-axis
**Chosen:** Four named lemmas — `lem:slice-rank-def`, `lem:upper`, `lem:lower`, `lem:monomial-count` — feeding `thm:cap-set` and `cor:numerical`; the diagonal lower bound (the crux) lives inside `lem:slice-rank-def` as a reusable part. Shallowest tree matching the prompt's named lemmas, each with a downstream consumer.
**Alternative:** Fold the diagonal lower bound into `lem:lower` (three lemmas).
**Reversible:** yes — merge the diagonal-tensor part into `lem:lower`; the mathematics is identical, only the lemma boundaries move.

## citations
**Chosen:** Cite Croot–Lev–Pach 2017, Ellenberg–Gijswijt 2017, and BCCGNSU 2017 (symmetric slice-rank packaging), each digested, while proving the slice-rank properties and both bounds internally (do not black-box the method).
**Alternative:** Cite the final cap-set bound directly without reproducing the method.
**Reversible:** yes — replace the internal slice-rank lemmas with a single cited theorem; the proof collapses to a few lines but loses self-containedness.
