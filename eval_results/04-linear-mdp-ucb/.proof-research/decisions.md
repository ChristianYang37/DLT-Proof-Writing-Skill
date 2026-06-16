# Autonomous decisions — LSVI-UCB regret

Headless/eval mode: no interactive user, so each user-decision dimension below
was resolved by adopting the stronger/tighter default and recorded here per
socratic-intake.md. These are settled setting choices, not open gaps; the
matching inline `% \todo{user-decision: ...}` annotations have been removed from
the `.tex` (genuine open gaps stay as inline `\todo{verify: ...}`).

## target-form (regret rate)
**Chosen:** $d^{3/2}\sqrt{H^3 T}$ — the stronger/correct Jin-Yang-Wang-Jordan (2020) rate; it is the tightest rate actually provable under the bonus $\beta=\Theta(dH\sqrt{\iota})$ used throughout, and is what Steps 5–6 of the main proof close.
**Alternative:** $d^{3/2}\sqrt{HT}$ (as literally written in the eval prompt) — drops two factors of $H$ that are not provable under $\beta=\Theta(dH\sqrt{\iota})$; would require a different (smaller) bonus and a tighter recursion to even state honestly.
**Reversible:** no — flipping to $\sqrt{HT}$ would falsify the closing arithmetic in 05-main-theorem.tex (Step 6, $H^2\sqrt K=\sqrt{H^3 T}$) and the $T_1$ bound; the bonus scaling $\beta=C_\beta dH\sqrt\iota$ and \Cref{lem:recursion} would all have to change.

## constant-discipline (bonus radius $\beta$)
**Chosen:** $\beta = C_\beta\, dH\sqrt{\iota}$ with a symbolic universal constant $C_\beta$ — stronger-where-honest and rate-exact: the exponents $dH\sqrt\iota$ are pinned and verified, while the numeric constant stays symbolic rather than over-claiming a specific optimized value.
**Alternative:** a fully optimized numeric constant (e.g. the implicit self-consistent $c_\beta$ from jin2020provably Eq. 14) — buys nothing at the rate level and risks an unverifiable/fabricated numeric claim.
**Reversible:** yes — flipping to a numeric $C_\beta$ changes only the displayed constant in \Cref{lem:concentration} and the floors $C_\beta\ge C$, $C_\beta\ge C+4$; no exponent, lemma, or structural step changes. The residual numeric pinning is the lone open `\todo{verify: C_beta}` in 02-concentration.tex.
