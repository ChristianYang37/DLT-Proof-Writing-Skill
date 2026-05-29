# Review loop complete (iterations: 2, verdict: accept-with-minor-revisions)

## What was reviewed
The three results (R1 two-sided phase transition, R2 critical-window Gaussian,
R3' finite-horizon cone confinement) and their supporting lemmas, after the
Step-0 framing correction. Files: sections/01--15, 99 in
`eval_results/08-reasoning-as-optimization/`.

## What was fixed (iteration 1)
- **W1 (major, R2 data-dependent BE terminal):** restructured R2 to apply
  Hall--Heyde to the FIXED-direction correct-token logit martingale; incorrect
  side pinned as a deterministic threshold on the good event. (sections/14)
- **W2 (minor, vague $o(\cdot)$):** resolved by W1; drift now exact via the
  net-drift identity, error $(1+o(1))$. (sections/14)
- **W3 (major, Slepian on non-Gaussian):** stated the exceedance-covariance
  bound explicitly (exact in the Gaussian limit), flagged the non-asymptotic
  version with `\todo{verify}`, recorded Sudakov fallback. (sections/12)
- **W4 (minor, asserted $C''\le1/4$):** introduced tunable threshold constant
  $\kappa$, removing dependence on the numerical small-ball constant. (sections/12)
- **W5 (minor, $\sigma_{\max}\le2M$):** added the explicit trace argument
  ($\sigma_{\max}^2\le8M^2$). (sections/08)
- **W6 (minor, retraction accumulation):** reframed to the operationally-exact
  single-LayerNorm iterate (no accumulation); per-step alternative noted. (sections/07)

## What was fixed (iteration 2)
- $\kappa$-consistency propagated to the R2 threshold-pinning line. (sections/14)
- (Separately, Occam pass: `cor:min_dimension` demoted to `rem:min_dimension`,
  since it had no downstream consumer — a direct algebraic inversion of R1.)

## What was NOT fixed and why
- **W3' (the anti-concentration exceedance-covariance bound):** INTENTIONAL
  residual. The bound is exact in the Gaussian limit (Slepian) and transfers
  to the asymptotically-Gaussian projections up to a Berry--Esseen correction;
  the non-asymptotic version is genuinely delicate. It is surfaced as the
  single `\todo{verify}` in the source (sections/12-lemma-incorrect-max-lower.tex:95)
  with Sudakov minoration as the recorded fallback. Its Paley--Zygmund
  consequence is independently script-verified (CHECK 6). This is the one item
  needing human judgement.

## Residual weakness needing your decision
- **Anti-concentration covariance bound (failure branch, lem:incorrect_max_lower).**
  - Reviewer's claim: the exceedance-covariance bound for the finite-horizon,
    only-asymptotically-Gaussian incorrect-logit projections is not established
    non-asymptotically (Slepian needs exact Gaussianity).
  - Proposed resolutions: (a) prove a non-asymptotic correlation-comparison
    lemma for sub-Gaussian exceedances; or (b) re-derive the failure branch via
    Sudakov minoration (avoids the covariance bound, at the cost of a less
    explicit constant). Both are user-level decisions.
  - Your call.

## Iteration trace
- `.proof-research/review-iteration-1.md`, `.proof-research/review-iteration-2.md`.

## Termination
Converged at iteration 2: the only weakness remaining is the INTENTIONAL,
flagged anti-concentration residual; all other weaknesses resolved with
minimum-change fixes. Verdict: accept-with-minor-revisions. All three Phase-D
gates exit 0.
