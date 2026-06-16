# Autonomous setting decisions (Phase A.1a, headless mode)

Each block records a setting fork that was resolved autonomously by adopting the
stronger/tighter default (per socratic-intake.md §6). These are auto-resolved
choices, not open gaps; the corresponding inline `\todo{user-decision: ...}`
markers were removed from the `.tex`. Flip any of them only at the user's request.

## design (Q3 — design model)
**Chosen:** fixed design on a regular grid — closes the proof with an exact per-cell point count ($n/M_0$ points per subcube), giving the cleanest, assumption-light KL bound (\Cref{lem:kl}) with no extra randomness to control.
**Alternative:** random design with an added design-concentration step.
**Reversible:** yes — flipping requires inserting a design-concentration lemma (high-probability comparison of the empirical sum $\frac1n\sum_i u(x_i)^2$ to $\norm{u}_{L^2}^2$) before \Cref{lem:kl}; the bump family, Varshamov--Gilbert packing, and Fano core are unchanged.

## noise (Q4 — noise model)
**Chosen:** Gaussian noise with known variance $\sigma^2$ — yields the exact closed-form mean-shift KL (\Cref{fac:gauss-kl}) $\KL=\frac{1}{2\sigma^2}\sum_i(f(x_i)-h(x_i))^2$, the sharpest possible information bound with no slack.
**Alternative:** unknown / sub-Gaussian noise.
**Reversible:** yes — flipping replaces the exact Gaussian KL in \Cref{fac:gauss-kl} with a sub-Gaussian KL/$\chi^2$ surrogate (extra constant), leaving the rate $n^{-2s/(2s+d)}$ unchanged; only the constant $c$ and the proof of \Cref{fac:gauss-kl} move.

## target-form (Q1 — risk lower bound form)
**Chosen:** in-expectation $\Ltwo$ risk lower bound, $\E_{D_n}\norm{\hat f-f^*}_{\Ltwo}^2\ge c\,n^{-2s/(2s+d)}$ — the standard headline form, obtained directly from the Fano testing error via Markov-free averaging (Step 4 of \Cref{thm:main}).
**Alternative:** a constant-probability in-probability version.
**Reversible:** yes — the in-probability statement follows from the same Fano testing bound (Step 3) by stopping before the expectation step; only Step 4 of the \Cref{thm:main} proof changes, the rate and constants are identical.

## fano-method (Q6 — information-theoretic reduction)
**Chosen:** local Fano method with the $I(V;Y)+\log 2$ vs $\log M$ comparison — exploits the full Varshamov--Gilbert packing ($\log M\ge\frac{m^d}{8}\log2$), preserving the sharp dependence on the dimension $d$.
**Alternative:** a two-point / Le Cam reduction (simpler but loses the sharp constant in $d$).
**Reversible:** yes — flipping to Le Cam replaces \Cref{lem:fano} and Step 3 of \Cref{thm:main} with a two-hypothesis testing affinity bound; the bump family collapses to a single bump and the $d$-dependence in the constant weakens, but the $n$-rate is unaffected.

## rate-domain (Q3 — sample-size domain of the rate)
**Chosen:** state the rate along the regular-grid subsequence $m\mid n^{1/d}$ — keeps the per-cell point count exact (\Cref{lem:kl} hypothesis) and the constant clean, with no interpolation overhead.
**Alternative:** a general-$n$ statement via a standard nearest-grid interpolation that costs only constants.
**Reversible:** yes — flipping adds a nearest-grid interpolation argument (replacing exact $n/M_0$ with a $\Theta(n/M_0)$ count); the rate exponent is unchanged and only the constant $c$ and the resolution-choice paragraph of \Cref{thm:main} are touched.
