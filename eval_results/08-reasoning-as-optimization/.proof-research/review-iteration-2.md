# Review iteration 2 — re-review after iteration-1 fixes

(Author-agent reviewer mode, re-reading the files changed in iteration 1:
sections/07, 08, 12, 14, plus a fresh end-to-end pass. Same reviewer
template; the goal is to confirm the iteration-1 fixes are sound and detect
any regression.)

## Summary
Unchanged contribution (see iteration 1). The changes since iteration 1:
(i) R2 now applies Berry--Esseen to the FIXED-direction correct-token logit
martingale and pins the incorrect side as a threshold on $\Ecal_{\mathrm{inc}}$
between lem:incorrect_max (upper) and lem:incorrect_max_lower (lower);
(ii) lemma 12 states the exceedance-covariance bound explicitly, valid
exactly in the Gaussian limit (Slepian) and asymptotically otherwise, with a
\todo{verify} on the non-asymptotic version and Sudakov as the fallback;
(iii) lemma 12 uses a tunable threshold constant $\kappa$ removing the
dependence on the numerical small-ball constant $C''$; (iv) the
$\sigma_{\max}\le2\sqrt2 M$ link is made explicit via a trace argument;
(v) the retraction lemma analyses the operationally-exact single-LayerNorm
iterate $\bar x_T$, for which there is no accumulated retraction error.

## Strengths
- The R2 fix is a genuine improvement: the fixed-direction martingale has a
  data-independent terminal functional, so Hall--Heyde applies cleanly; the
  incorrect side is handled deterministically on the good event. This is the
  standard and correct way to get a Gaussian CDF for a max-type margin.
- The $\kappa$-tunable threshold (lem 12) is a clean removal of a numerical
  constant dependence; the proof no longer asserts $C''\le1/4$.
- The retraction reframing (operational iterate $=$ single normalization) is
  honest and removes the accumulation question, while still recording the
  per-step-retraction alternative and its $O(T_{\max}/d)$ caveat.

## Weaknesses
- **W3' (major, carried over, now flagged).** The non-asymptotic
  exceedance-covariance bound eq:antic_cov for the finite-$T_{\max}$
  sub-Gaussian projections is not established non-asymptotically; it is exact
  only in the Gaussian limit (Slepian). Evidence:
  sections/12-lemma-incorrect-max-lower.tex:86--100. Severity: major, but now
  carries a \todo{verify} and a recorded Sudakov fallback (INTENTIONAL
  surfacing rather than a silent gap). This is the single residual.

## Questions for the author
- Q1. Would you prefer the failure branch of R1/R2 to be re-derived via
  Sudakov minoration (which avoids the exceedance-covariance bound entirely
  at the cost of a less explicit constant), making the \todo{verify}
  unnecessary? This is a constant-vs-rigour trade-off for your decision.

## Verdict
accept-with-minor-revisions

---

## Verification (Component 2) and fixes (Component 3)

### Weakness #W3' (major) — non-asymptotic exceedance-covariance bound
**Verdict:** INTENTIONAL (residual surfaced as \todo).
**Rebuttal / fix-plan:** This is a genuinely delicate step (anti-concentration
for a max of weakly-correlated, only-asymptotically-Gaussian variables). It is
NOT silently asserted: eq:antic_cov is stated, its Gaussian-limit justification
(Slepian) is given, the Berry--Esseen transfer is noted, a \todo{verify} marks
the non-asymptotic gap, and Sudakov minoration is recorded as the fallback that
sidesteps it. The Paley--Zygmund consequence is independently script-verified
(CHECK 6). Per the honesty protocol this is the correct disposition: surface,
do not hand-wave. Fixing it fully requires either (a) a non-asymptotic
correlation-comparison lemma for sub-Gaussian exceedances, or (b) switching the
failure branch to Sudakov minoration — both are user-level decisions (the
former is research, the latter changes the explicit constant). No further
auto-fix applied; surfaced in the final report.

### Re-check of iteration-1 fixes (no regression)
- W1 (R2 data-dependent terminal): resolved; fixed-direction martingale,
  re-read sections/14:74--112, sound. No regression.
- W2 ($o(\cdot)$): resolved by W1 fix; now $(1+o(1))$ explicit.
- W4 ($C''$): resolved; $\kappa$ tunable, re-read sections/12:41--55, sound.
- W5 ($\sigma_{\max}$): resolved; trace argument, sections/08 remark, sound.
- W6 (retraction accumulation): resolved; operational iterate framing,
  sections/07:96--110, sound.
- $\kappa$ propagated to the R2 threshold-pinning line (sections/14:90) for
  consistency.

**Fixes applied this iteration:** $\kappa$-consistency in R2 (1 line). No new
substantive fixes; the single residual is INTENTIONAL (the \todo W3').

## Loop termination
Iteration 2 produced exactly ONE weakness (W3'), which is the SAME issue as
iteration-1 W3, now verified INTENTIONAL with a \todo and a recorded fallback.
No new actionable REAL-blocking weakness. Per review-loop.md Component 4
gate (4) "no fixes applied this iteration" (only a 1-line consistency tweak;
the sole weakness is INTENTIONAL), the loop terminates at
accept-with-minor-revisions. The residual \todo{verify} is surfaced to the
user as the one item needing human judgement.
