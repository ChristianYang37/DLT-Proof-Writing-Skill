# Technique digest — Hoeffding's lemma (sharp sub-Gaussian proxy)

**Slug:** hoeffding-lemma
**Used by:** sections/01-hoeffding-lemma.tex (lem:hoeffding); consumed by the
main theorem's MGF factorization.

## Statement

Let $Y$ be a random variable with $\E[Y]=0$ and $Y\in[a,b]$ almost surely.
Then for every $\lambda\in\mathbb{R}$,
$$\E\!\left[e^{\lambda Y}\right]\ \le\ \exp\!\left(\frac{\lambda^2 (b-a)^2}{8}\right).$$
I.e. $Y$ is sub-Gaussian with variance proxy $(b-a)^2/4$ (so the MGF bound
carries $(b-a)^2/8$ in the exponent).

## Proof skeleton (the canonical "log-MGF second-derivative" argument)

Let $\psi(\lambda)=\log \E[e^{\lambda Y}]$ be the cumulant generating function.

1. $\psi(0)=\log 1 = 0$ and $\psi'(0)=\E[Y]=0$ (differentiate under the
   expectation; the MGF of a bounded RV is finite and smooth for all $\lambda$).

2. **Tilted measure.** For fixed $\lambda$, define the tilted probability law
   $dQ_\lambda \propto e^{\lambda Y}\,dP$, i.e. the new RV has density
   proportional to $e^{\lambda y}$. A direct computation gives
   $$\psi'(\lambda)=\frac{\E[Y e^{\lambda Y}]}{\E[e^{\lambda Y}]}=\E_{Q_\lambda}[Y],
   \qquad
   \psi''(\lambda)=\frac{\E[Y^2 e^{\lambda Y}]}{\E[e^{\lambda Y}]}
     -\left(\frac{\E[Y e^{\lambda Y}]}{\E[e^{\lambda Y}]}\right)^2=\mathrm{Var}_{Q_\lambda}(Y).$$

3. **Popoviciu / variance-of-bounded-RV bound.** Under $Q_\lambda$ the variable
   $Y$ still lies in $[a,b]$ (the tilt only reweights, it does not move the
   support). For ANY random variable supported in $[a,b]$,
   $$\mathrm{Var}(Y)\ \le\ \Big(\frac{b-a}{2}\Big)^2=\frac{(b-a)^2}{4}.$$
   Proof of this sub-fact: $\mathrm{Var}(Y)=\E[(Y-c)^2]-(\E[Y]-c)^2\le\E[(Y-c)^2]$
   for the midpoint $c=(a+b)/2$, and $|Y-c|\le (b-a)/2$ pointwise, so
   $\E[(Y-c)^2]\le (b-a)^2/4$. (Equality is the two-point $\{a,b\}$ law with
   mass $1/2$ each, so the constant $1/4$ is sharp.)

4. **Taylor with remainder.** By Taylor's theorem there is $\xi\in[0,\lambda]$
   with
   $$\psi(\lambda)=\psi(0)+\lambda\psi'(0)+\tfrac{\lambda^2}{2}\psi''(\xi)
     =\tfrac{\lambda^2}{2}\psi''(\xi)\le\tfrac{\lambda^2}{2}\cdot\frac{(b-a)^2}{4}
     =\frac{\lambda^2(b-a)^2}{8}.$$
   Exponentiating gives the claim.

## Notes / pitfalls
- The constant is $(b-a)^2/8$ in the exponent, NOT $(b-a)^2/2$. The latter comes
  from a cruder convexity-only argument and would yield $\exp(-t^2/(2V))$ in the
  final bound instead of the sharp $\exp(-2t^2/V)$.
- The variance bound $\mathrm{Var}(Y)\le (b-a)^2/4$ is the single load-bearing
  inequality; it is sharp and elementary. This is the step graded as the "sharp
  proxy" decision in the runner log (Q2).
- $\psi$ is smooth on all of $\R$ because $Y$ is bounded ⇒ MGF entire.

## Cross-check (independent, no peeking at the above derivation)
Standard references (Boucheron–Lugosi–Massart, *Concentration Inequalities*,
Lemma 2.2/2.6; Vershynin, *HDP*, §2.6; Wainwright, *HDS*, Ex. 2.4) all give the
same $(b-a)^2/8$ exponent via this exact $\psi''=\mathrm{Var}_{Q_\lambda}\le
(b-a)^2/4$ argument. Verdict: matches.
