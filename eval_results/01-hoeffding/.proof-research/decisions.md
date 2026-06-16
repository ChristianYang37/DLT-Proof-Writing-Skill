# Autonomous setting decisions (Phase A.1a)

Resolved in headless/eval mode by adopting the stronger/tighter default in each
case (Socratic-intake protocol §6). Each block records the option drafted into
the proof, the alternative not taken, and what flips if the user reverses it.

## target-form / constant-discipline
**Chosen:** exact constant $2\exp(-2t^2/V)$ with no slack, $V=\sum_i(b_i-a_i)^2$ — the sharp textbook Hoeffding rate, matching the displayed target verbatim with the leading $2$ and exponent $-2t^2/V$, strictly stronger than any universal-$C$ form.
**Alternative:** a looser universal-$C$ exponent $\exp(-ct^2/V)$ (constants absorbed), provable from a cruder sub-Gaussian bound.
**Reversible:** yes — flipping to the looser form only relaxes the final exponent (`eq:hoeffding-main`, `eq:two-sided`); the proof skeleton (Chernoff + Hoeffding's lemma + $\lambda$-optimisation) is unchanged, and one would simply stop tracking the exact constant after `eq:exponent-opt`.

## variance-proxy / lemma-constant
**Chosen:** sharp variance proxy $(b-a)^2/8$ in Hoeffding's lemma, via $\psi''(\lambda)=\Var_{Q_\lambda}(Y)\le(b-a)^2/4$ — this is exactly the proxy that produces the leading constant $2$ in the tail bound, tighter than the convexity-only proxy by a factor of $4$ in the exponent.
**Alternative:** the cruder convexity proxy $(b-a)^2/2$, which is shorter to prove but doubles the lemma constant and fails to reproduce the target rate.
**Reversible:** yes — flipping replaces Step 3 of the lemma proof (`eq:var-bound`, the Popoviciu variance bound) with a convexity argument; the lemma exponent becomes $\lambda^2(b-a)^2/2$ and the downstream constant in `eq:hoeffding-main` degrades from $2$ to a smaller value. Everything else in the theorem proof is untouched.

## two-sided
**Chosen:** two-sided bound via a union bound over both tails (factor $2$), applying the one-sided result to $-X_i$ — this is the full stated theorem, controlling $\abs{S_n-\E S_n}$.
**Alternative:** the one-sided bound $\Pr[S_n-\E S_n\ge t]\le\exp(-2t^2/V)$ only, which is strictly weaker than the claimed two-sided event.
**Reversible:** yes — flipping drops Step 3 of the theorem proof (`eq:lower-sided`, `eq:two-sided`) and the leading factor $2$; the one-sided bound `eq:one-sided` is already isolated, so reversal is a deletion with no re-derivation.
