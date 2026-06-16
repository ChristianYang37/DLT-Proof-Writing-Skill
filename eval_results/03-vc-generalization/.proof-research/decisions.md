# Autonomous setting decisions

Decisions adopted autonomously (headless/eval mode) per the Socratic-intake
protocol (`references/socratic-intake.md` §6): each fork was resolved to its
stronger/tighter default, recorded here, and is NOT left as an inline
`\todo{user-decision: ...}` in the `.tex`.

## target-form (high-probability vs in-expectation)
**Chosen:** high-probability $1-\delta$ deviation bound (\Cref{lem:mcdiarmid-dev}, Eq.~\eqref{eq:mcdiarmid-conc}) — strictly stronger than an in-expectation statement: a $1-\delta$ tail bound implies the expectation bound by integrating over $\delta$, not conversely.
**Alternative:** an in-expectation bound on $\E_S\,\Phi(S)$ only.
**Reversible:** yes — flipping to in-expectation only deletes the McDiarmid concentration step (\Cref{lem:mcdiarmid-dev}) and the $\sqrt{\log(1/\delta)/(2n)}$ term, leaving $\E_S\Phi(S)\le 2\Rad_n(\Lbar)$; the rest of the pipeline (symmetrization, Sauer--Shelah, Massart) is unchanged.

## constant-discipline (absorbed universal $C$ vs tracked exact constant)
**Chosen:** explicit $\sqrt{(d\log(n/d)+\log(1/\delta))/n}$ rate with a single absorbed universal constant $C$ ($C=\sqrt{17}$, value not numerically optimized) — delivers the correct VC rate at full generality with the cleanest statement; tightening the constant does not improve the rate, which is the headline win.
**Alternative:** track the exact numerical constant via careful chaining (Dudley), which would also remove the $\sqrt{\log(n/d)}$ factor.
**Reversible:** yes — flipping to the tracked-constant program replaces the absorbing Cauchy--Schwarz step $(e)$ of Eq.~\eqref{eq:assemble} (and \Cref{rem:rate}) with an explicit chaining argument; the symmetrization/Sauer--Shelah/Massart lemmas are reused verbatim, only the final assembly constant changes.
