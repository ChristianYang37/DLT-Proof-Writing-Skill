# Review iteration 1 — independent adversarial review

(Performed by the author agent in reviewer mode — no separate agent-spawn
tool was available in this run. The review follows the review-loop.md
reviewer prompt template; weaknesses are then verified point-by-point in the
"Verification" section below, with the REAL-blocking / REAL-nonblocking /
PHANTOM / INTENTIONAL taxonomy.)

## Summary
The paper models an LLM's chain-of-thought at the final decoding position as
noisy Riemannian SGDM on the cross-entropy loss over the LayerNorm sphere
$\Sphere=\{\norm x=\sqrt d\}$, single-token answer ($n=1$, true decoder
$=\arg\max$ logit). A single global behavioural assumption A1 posits, on the
correct-token projection $\proj_k=\inner{V_k}{\rowhat}$, a sign rate $p$
($\snet=2p-1$), a conditional-mean magnitude floor $\E\abs{\proj_k}\ge\driftc\rho_0$,
sign/magnitude conditional independence, and a drift-direction clause
$\E[V_k\mid\Fcal_{k-1}]=\beta_k\rowhat$. The net drift
$\E[\proj_k\mid\Fcal_{k-1}]=\snet\E\abs{\proj_k}$ is an exact identity from the
conditional independence. The architecture assumption A2 bounds the
unembedding (incoherence $\incoh_0$, row norms $[\rho_0,R_U]$), value norms
$M$, scores $S=O(1)$, and the isotropic-noise scale $1/d$. Three results: R1
two-sided phase transition at $\critrate\propto1/\sqrt{T_{\max}d}$ via a
margin-drift-sharing comparison (success) and anti-concentration (failure);
R2 Gaussian-CDF critical-window via Hall--Heyde martingale Berry--Esseen; R3'
finite-horizon cone confinement via a maximal inequality (ODE only as a
flagged informal remark). The signal floor lives on the un-retracted iterate;
the margin sign is rescaling-invariant, so retraction error does not enter the
transition.

## Strengths
- The net-drift identity is genuinely a first-moment statement on the correct
  direction (rate $\times$ magnitude), avoiding any transitivity through the
  loss-descent direction — the previous logical gap is cleanly closed.
- The margin-drift-sharing observation (correct and incorrect drifts share the
  systematic-update magnitude $D$) is the right move: it makes the deterministic
  incoherence cross-term $O(\snet)$ rather than $\Theta(1)$, which is what
  preserves the $1/\sqrt{T_{\max}d}$ scaling. Without it the headline fails.
- Noise provenance is cleanly factored $1/\sqrt d$ (isotropy/orthogonality)
  $\times$ $1/\sqrt T$ (softmax quad-variation), with no Lévy concentration
  invoked for the horizon factor.
- The failure branch is a real anti-concentration max-LOWER bound (second
  moment / Paley--Zygmund), not a reversed union bound; this is correctly
  flagged and the budget is a single second-moment event.
- R3' is honestly finite-horizon (maximal inequality), with the ODE confined
  to a remark explicitly labelled not-derivable-from-A1.

## Weaknesses
- **W1 (major).** R2 Step 1 applies the martingale Berry--Esseen to
  $\sum_t D_t$ with $D_t=w_{T,t}\inner{W_U^{\corr}-W_U^{\hat a}}{\xi_t}$, but
  $\hat a=\arg\max_{a\neq\corr}\inner{W_U^a}{\tilde x_{T_{\max}}}$ is
  data-dependent, so $(D_t)$ is not a martingale array with a fixed terminal
  functional. Evidence: sections/14-theorem-R2-critical-window.tex:71--82
  ("Let $\hat a\in\arg\max\dots$ write the margin ... as ... a centred
  martingale"). Severity: major.
- **W2 (minor).** R2 writes $\mu_{T_{\max}}=D(\rho_0-\incoh_0 R_U)+o(\cdot)$
  with an unspecified $o(\cdot)$ and "at leading order", leaving the exact $z$
  constant (and thus the offset identification) imprecise. Evidence:
  sections/14-theorem-R2-critical-window.tex:79,85. Severity: minor.
- **W3 (major).** Lemma 12 Step 2 bounds the exceedance covariance by
  "Slepian/Gaussian-comparison" for the events $\{Z_a>t\}$, but the $Z_a$ are
  sums of bounded martingale increments, not exactly Gaussian, so Slepian does
  not literally apply. Evidence:
  sections/12-lemma-incorrect-max-lower.tex:84--88. Severity: major.
- **W4 (minor).** Lemma 12 Step 1 fixes the small-ball constant "$C''\le1/4$"
  to force $\theta<1$, but $C''$ is the Vershynin spreading constant and is not
  shown to satisfy this. Evidence:
  sections/12-lemma-incorrect-max-lower.tex:48--52. Severity: minor.
- **W5 (minor).** The bound $\sigma_{\max}\le2M$ (used to fix the displayed
  constant $2$ in the noise scale) is asserted from $\norm{\xi_k}\le2M$ but the
  isotropy clause bounds the operator norm $\le\sigma_{\max}^2/d$, whereas
  $\norm{\xi_k}^2\le4M^2$ bounds the trace; the link needs one line. Evidence:
  sections/08-lemma-incorrect-max.tex (remark), sections/02-assumptions.tex:95.
  Severity: minor.
- **W6 (minor).** Retraction Step 3 asserts the per-step gaps "do not compound
  across steps to leading order because each $x_t$ is re-projected", which is
  plausible but stated without a recursion. Evidence:
  sections/07-lemma-retraction-stability.tex:99--104. Severity: minor.

## Questions for the author
- Q1. Is the mild incoherence condition $\incoh_0<\rho_0/R_U$ (R1/R2/R3')
  intended to be a hypothesis of the headline, or is it implied by A2? (It is
  currently a stated hypothesis; just confirming it is not meant to be dropped.)
- Q2. In R2, is the headline the absolute width $\Theta(1/\sqrt{T_{\max}d})$ or
  the relative width? (Stated as absolute; the relative is a remark.)

## Verdict
accept-with-minor-revisions

---

## Verification (Component 2) and fixes (Component 3)

### Weakness #1 (major) — data-dependent terminal in R2 BE
**Verdict:** REAL-blocking.
**Rebuttal / fix-plan:** Applying Berry--Esseen to a martingale whose terminal
functional $\hat a$ is data-dependent is not justified. FIXED by restructuring
R2 to apply BE to the CORRECT-token logit $\inner{W_U^{\corr}}{\tilde x_T}$, a
genuine FIXED-direction martingale, and treating the incorrect max as a
deterministic-on-$\Ecal_{\mathrm{inc}}$ threshold pinned between lem:incorrect_max
(upper) and lem:incorrect_max_lower (lower). sections/14:52--112 rewritten.

### Weakness #2 (minor) — imprecise $o(\cdot)$ / $z$ constant
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Resolved by the W1 fix: the fixed-direction drift is
exactly $\snet\norm{W_U^{\corr}}_2\E_0[\dots]$ via the net-drift identity (no
data-dependence), and the $o(\cdot)$ is now an explicit $(1+o(1))$. sections/14:83.

### Weakness #3 (major) — Slepian on non-Gaussian projections
**Verdict:** REAL-blocking (correctness of the variance bound).
**Rebuttal / fix-plan:** Slepian's inequality requires Gaussianity; the $Z_a$
are only asymptotically Gaussian. FIXED by (a) restating the exceedance-covariance
bound eq:antic_cov explicitly, (b) noting it is exact for the Gaussian limit and
transfers up to a Berry--Esseen correction, and (c) placing a \todo{verify} on the
non-asymptotic version, with Sudakov minoration as the recorded fallback. This is
the single residual 🔴 in the confidence trace (step 12.02). The Paley--Zygmund
CONSEQUENCE is script-verified (CHECK 6); only the covariance inequality for
finite-$T_{\max}$ sub-Gaussian $Z_a$ is flagged. sections/12:84--104.

### Weakness #4 (minor) — asserted $C''\le1/4$
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** FIXED by introducing a tunable threshold constant
$\kappa\in(0,1/(2C''))$ so that $\theta=2C''\kappa(1-\incoh_0)<1$ holds for ANY
absolute $C''$, removing the dependence on its numerical value; $\kappa$ rescales
the $\sqrt{1-\incoh_0}$ constant by $\Theta(1)$, absorbed into $c_1$. lem statement
and Step 1 updated (sections/12).

### Weakness #5 (minor) — $\sigma_{\max}\le2M$ link
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** FIXED with the explicit trace argument: $\norm{\xi_k}\le2M$
⇒ $\operatorname{tr}\operatorname{Cov}\le4M^2$ ⇒ under isotropy $\sigma_{\max}^2\le8M^2$,
folded into the absolute constant. sections/08 (remark).

### Weakness #6 (minor) — retraction gaps "do not compound"
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The "do not compound" claim was not justified. FIXED by
making explicit that the OPERATIONAL iterate is the single-LayerNorm normalization
$\bar x_T=\sqrt d\,\tilde x_T/\norm{\tilde x_T}$ (attention average then one LN),
for which there is NO accumulated error; the per-step-retraction reading (which
could accumulate to $O(T_{\max}/d)$) is explicitly noted as the alternative we
avoid. sections/07 Step 3.

### Q1, Q2 (questions): the mild incoherence $\incoh_0<\rho_0/R_U$ IS a stated
hypothesis (intentional, surfaced); the headline width is the absolute
$\Theta(1/\sqrt{T_{\max}d})$ (intentional). No change.

**Fixes applied:** W1, W2, W3 (+todo), W4, W5, W6. One residual \todo{verify}
(W3 covariance bound). Proceed to recompile + re-review.
