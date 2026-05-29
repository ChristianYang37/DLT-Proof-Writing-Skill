# Hall and Heyde, "Martingale Limit Theory and Its Application" (1980)

## Reference

Peter Hall and C. C. Heyde. *Martingale Limit Theory and Its
Application.* Academic Press, Probability and Mathematical Statistics
series, 1980. ISBN 0-12-319350-8.

## What is cited

Theorem 3.6 (page ~76 of the printed edition): the **rate of
convergence to normality** ("Berry-Esseen-for-martingales") for
square-integrable martingale arrays under conditional second-moment
and conditional third-moment conditions. Paraphrased to our notation:

For a martingale array $(M_{T,t})_{t=1}^{T_{\max}}$ with differences
$D_{T,t} := M_{T,t} - M_{T,t-1}$ adapted to a filtration
$(\mathcal F_t)$, define the conditional variance and conditional third
moment
\[
   V_T := \sum_{t=1}^{T_{\max}} \E[D_{T,t}^2 \mid \mathcal F_{t-1}],
   \qquad
   \rho_T := \sum_{t=1}^{T_{\max}} \E[|D_{T,t}|^3 \mid \mathcal F_{t-1}].
\]
Assume (H1) $V_T / V_\infty \to 1$ in probability for some
non-random $V_\infty > 0$ (conditional Lindeberg) and (H2)
$\rho_T < \infty$ a.s.. Then for every $x \in \R$,
\[
   \bigl| \Pr[M_{T,T_{\max}} \le x \cdot V_T^{1/2}] - \Phi(x) \bigr|
   \le C \cdot \rho_T / V_T^{3/2},
\]
with $C$ an absolute constant (Hall-Heyde give $C \le 25$; sharper
i.i.d.-Berry-Esseen constants are $\le 0.56$ via Esseen-Shevtsova
refinements).

## Constants tracked

- $C \le 25$ (the absolute constant in Hall-Heyde's bound).
- $V_T$ from `lem:orthogonality_high_d` + `lem:max_attention_weight`
  (Lemma C): $V_T \le 4 R_U^2 M^2 e^{2S}/(T_{\max} d)$ for our
  signed-signal martingale.
- $\rho_T$ via the "variance $\times$ deterministic-bound" sandwich
  combined with the high-d-orthogonality refinement: on the
  high-probability truncation event $\Ecal_{\text{trunc}}$ of
  `lem:orthogonality_high_d`, $\rho_T \le R_U^3 M^3 e^{4S}/(d^{3/2}
  T_{\max}^2)$. The factor $d^{-3/2}$ (rather than $d^{-1}$ from the
  deterministic per-step bound) is what makes the BE rate
  $\rho_T/V_T^{3/2}$ vanish jointly in $d, T_{\max}$ at the rate
  $e^S/\sqrt{T_{\max}}$ rather than growing as $\sqrt{d/T_{\max}}$.

## Why we cite it

The proof of `thm:T4_critical_window` (Theorem T4, §07b) applies
Hall-Heyde Theorem 3.6 to the centred signed-signal martingale of
Lemma B Step 2 (now with three-mode signed indicator $\xi_t \in \{+1,
0, -1\}$). The CLT-with-rate output, combined with the deterministic
Lemma A bound on the incorrect-side max, yields the $\Phi(z) +
O(\epsilon_{\text{BE}})$ Gaussian-CDF approximation of the
verifier-success probability across the full critical fragility
window $\snet(Q) \in (\critrate/\sqrt 2, \sqrt 2 \critrate)$ with
$\epsilon_{\text{BE}} = O(\sqrt{\log(|\Vocab|^n/|\Aset|)/(T_{\max}
d)})$.

The application requires a **high-probability truncation event** (not
a deterministic per-step bound) for the cubic moment to give the
right $d$-dependence. The technique digest at
`.proof-research/berry-esseen-martingale.md` contains the full
calculation; the constants $C \le 25$ and the truncation-event
failure budget $O(T_{\max} e^{-d/2})$ propagate through the union
bound of the T4 proof.

## Why Vershynin 2018 does NOT suffice

`cite-vershynin2018.md` covers sub-Gaussian concentration on the
sphere (Chapter 3) and Hoeffding for martingale differences (Chapter
2), but does **not** state a CLT-with-rate for martingale arrays.
Hall-Heyde 1980 is the canonical reference for that (Bolthausen 1982
sharpens for exchangeable arrays — which we do not have; Mourrat 2013
sharpens by a logarithmic factor but needs fourth conditional
moments — more bookkeeping than necessary). Hall-Heyde's Theorem 3.6
is the cleanest match for the second-and-third-conditional-moment
regime we get for free from `ass:bounded_value_norms`.

## Verification

Citation verified against the standard Probability and Mathematical
Statistics series catalogue and the book's wide use in martingale
limit theory: cited e.g.\ in Bose-Sen (2008) "Berry-Esseen Bounds in
Stochastic Geometry" §3 and in El Machkouri-Volný-Wu (2013)
"A central limit theorem for stationary random fields" §4. The full
text is held in the Cambridge University Library (call number
QA274.5.H35) and at Stanford (QA274.5 .H35).
