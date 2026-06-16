# Autonomous decisions (eval mode, no interactive user)

These are the Socratic-intake (Phase A.1a) decisions resolved autonomously by
adopting the stronger/tighter default. Recorded here per socratic-intake.md;
the inline `\todo{user-decision: ...}` markers have been removed from the `.tex`
(auto-resolved setting choices are not open gaps).

## single-variable-form
**Chosen:** Gilmer's actual single-variable Lemmas 2--3, the OR-entropy bounds $\hb(p+p'-pp')$ — faithful and strictly stronger: it yields the conditional per-coordinate bound, which the heuristic placeholder does not.
**Alternative:** the prompt's heuristic placeholder $\hb(p^2)-2\hb(p)$, which is only the i.i.d.-equal-marginal special case ($p=p'$) and does not yield the conditional bound.
**Reversible:** no — flipping to the placeholder would invalidate the key lemma (Lemma 1) assembly, since the placeholder cannot bound the correlated/conditional OR-entropy that the chain-rule argument in the entropy theorem consumes. The relationship is documented in `\Cref{rem:placeholder}` in sections/03-single-variable-bounds.tex.

## target-constant
**Chosen:** the explicit constant $c \ge 0.01$ (Gilmer's stated value) — strictly stronger and quantitative, reproducing Gilmer's $1.26$ entropy-amplification factor.
**Alternative:** a weaker abstract "some universal $c > 0$".
**Reversible:** yes — flipping to abstract $c>0$ only weakens the statement of `\Cref{thm:gilmer-frankl}` and its proof's conclusion (drop the numeral $0.01$); no upstream lemma changes, since the explicit value is already carried through. Remark `\Cref{rem:constant}` already notes the constant is unoptimized.
