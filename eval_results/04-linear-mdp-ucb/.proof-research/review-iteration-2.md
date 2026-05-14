# Review iteration 2 — LSVI-UCB regret proof

## Summary

Re-reading after iteration-1 fixes. The proof now:
- States the unit-vector assumption $\|u\|_2 = 1$ explicitly in \Cref{lem:weight_bound}.
- Derives the Bellman-residual identity Eq.~\eqref{eq:bellman_residual_identity} in three justified steps.
- Replaces the algebraically suspect "$2K(1/K)\sqrt k$" with the correct $(2/K)\sqrt d$ residual.

The proof skeleton and decomposition $T_1 + T_2 + T_3 = $ (martingale) + (cumulative bonus) + 0 is unchanged. The headline bound $\Otil(d^{3/2}\sqrt{H^3 T})$ now correctly follows from the algebra.

## Strengths

- Clean identity derivation in Eq.~\eqref{eq:bellman_residual_identity} replaces the previous unjustified assertion.
- Constant tracking through $\beta$ and the elliptical-potential step is now unambiguous.
- Residual bound $(2/K)\sqrt d$ is dimensionally consistent.

## Weaknesses

### Weakness #1 (severity: minor)
**Claim:** The proof in \Cref{lem:cover} still defers the Lipschitz computation to \cite{jin2020provably} Lemma D.6. A reader who does not have that paper at hand cannot independently verify the covering bound.
**Evidence:** `03-concentration.tex:34` "The detailed computation appears as Lemma D.6 in \cite{jin2020provably}"
**Severity:** minor

### Weakness #2 (severity: minor, style)
**Claim:** \Cref{lem:T2_bound}'s statement says "$T_2 \le 2\sqrt 2\, C_\beta\, d^{3/2}\, H^{3/2}\sqrt T \iota$" but the proof's intermediate algebra shows the dependence comes through $H \sqrt K \cdot \sqrt{H} \cdot \sqrt T$; the explicit $\sqrt{HT}$ form (which is what the proof actually derives) is replaced by a closed form. A reader following along may briefly lose the thread between $H\sqrt K$ and $H^{3/2}\sqrt T$.
**Evidence:** `06-elliptical.tex:42-50` (derivation chain)
**Severity:** minor (style)

## Questions

- Q1: Same as before — numerical $C_\beta$ for replicability?

## Verdict
accept-as-is

(The remaining issues are either INTENTIONAL deferrals to peer-reviewed prior work (W1) or style preferences (W2), and neither blocks correctness.)
