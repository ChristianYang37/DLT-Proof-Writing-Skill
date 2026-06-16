# Runner log — sobolev-minimax-lower-bound (eval id=5)

## What I built

A self-contained appendix-grade proof of the nonparametric minimax lower
bound for fixed-design regression over the Sobolev ball
$W^s_2([0,1]^d)$ with i.i.d. Gaussian noise: for any estimator $\hat f$,
$$\inf_{\hat f}\sup_{\|f^*\|_{W^s_2}\le 1}\E_{D_n}\|\hat f-f^*\|_{L^2}^2
\;\gtrsim\; n^{-2s/(2s+d)}.$$
The proof follows the standard **reduction to multiple hypothesis testing**
(statistical-rate lower-bound recipe from pattern-menu.md): build a finite
hypothesis subfamily inside the Sobolev ball, control its pairwise $L^2$
separation and pairwise KL divergence, and invoke Fano. Decomposition into
four lemmas: (i) Varshamov–Gilbert packing of the hypercube; (ii) a
localized bump-function family indexed by the packing, with both an $L^2$
separation lower bound and a Sobolev-norm upper bound; (iii) a pairwise KL
bound exploiting the Gaussian fixed-design likelihood; (iv) the Fano
inequality; assembled in the main theorem by balancing $m\asymp
n^{1/(2s+d)}$. Derivation pattern: trailing-justification blocks
throughout; organizational pattern: the statistical-rate
"minimax lower bound via Fano" row of pattern-menu.md.

## Patterns chosen
- Statement template: decomposed / condition-list for lemmas, plain formal for the theorem.
- Derivation pattern: trailing-justification block (templates.md §Derivation patterns).
- Organizational pattern: statistical-learning-rates row — minimax lower bound via Varshamov–Gilbert packing + local Fano, optimize $m$ at the very end.

## Phase A.1a — Socratic intake (self-Q&A; eval mode, no interactive user)

Adopting the STRONGER/TIGHTER default for each; recorded as
`\todo{user-decision: ...}` in the .tex and re-surfaced here.

**Q1 [loss / win condition].** State the bound for the *expected* squared
$L^2$ risk $\E_{D_n}\|\hat f-f^*\|_{L^2}^2$ (in-expectation lower bound), or
the weaker in-probability version?
  - Proposed (STRONGER): in-expectation, $\inf_{\hat f}\sup_f \E\|\hat
    f-f^*\|_{L^2}^2 \gtrsim n^{-2s/(2s+d)}$ — this is exactly the prompt's
    target and the standard headline.
  - Alternative: in-probability constant-probability lower bound.
  - Chosen: in-expectation. (Fano's testing lower bound delivers a
    constant-probability testing error, which converts to the in-expectation
    risk bound via Markov / the separation-to-risk reduction — both shown.)

**Q2 [norm on $f^*$ / Sobolev convention].** Which Sobolev norm bounds the
class — the full $W^s_2$ Sobolev norm (all weak derivatives up to order $s$
in $L^2$), with the ball radius normalized to $1$?
  - Proposed (STRONGER, matches prompt): unit ball
    $\{\|f^*\|_{W^s_2}\le 1\}$ in the full $W^s_2$ norm, integer smoothness
    $s\in\mathbb N$, $s>0$.
  - Alternative: homogeneous Sobolev seminorm (only top-order derivatives).
  - Chosen: full $W^s_2$ unit ball, integer $s$. We bound the full norm of
    each bump by an absolute constant and then *rescale* the family by that
    constant so the radius-$1$ constraint holds, which is the cleanest route
    and loses nothing in the rate.

**Q3 [design].** Fixed design (deterministic covariates $x_1,\dots,x_n$) or
random design?
  - Proposed (matches prompt): fixed design, with the covariates taken on a
    regular grid so the empirical $L^2$ and population $L^2$ norms of the
    bump family are comparable up to constants.
  - Alternative: random design (needs an extra design-concentration step).
  - Chosen: fixed design on a regular grid; we state the grid-regularity as
    an explicit assumption and use it only to relate $\frac1n\sum_i
    u(x_i)^2$ to $\|u\|_{L^2}^2$ for the localized bumps.

**Q4 [noise].** Gaussian noise with known variance $\sigma^2$, observations
$y_i=f^*(x_i)+\xi_i$, $\xi_i\sim\mathcal N(0,\sigma^2)$ i.i.d.?
  - Proposed (matches prompt): yes — exact Gaussian likelihood gives the
    closed-form KL $\KL(P_{f}\|P_{g})=\frac1{2\sigma^2}\sum_i (f(x_i)-g(x_i))^2$.
  - Chosen: Gaussian, known $\sigma^2>0$.

**Q5 [packing radius / VG constants].** Use the exact Varshamov–Gilbert
constants from the prompt: $M\ge 2^{m^d/8}$ codewords at pairwise Hamming
distance $\ge m^d/8$?
  - Proposed (matches prompt): yes, the standard $1/8$ VG constants.
  - Chosen: $2^{m^d/8}$ codewords, Hamming separation $\ge m^d/8$.

**Q6 [Fano variant].** Plain Fano (global, over a $2$-point-free finite
family) or local Fano (the version comparing $I(V;X)+\log2$ to $\log M$)?
  - Proposed (STRONGER / standard for this rate): local Fano via the mutual
    information bound $I(V;Y)\le \max_{k,k'}\KL(P_k\|P_{k'})$, then the Fano
    testing inequality $\inf_\psi\Pr[\psi\ne V]\ge 1-\frac{I(V;Y)+\log2}{\log M}$.
  - Chosen: local Fano with the $I(V;Y)+\log2$ vs $\log M$ comparison (this
    is exactly assertion 4 of the eval).

**Q7 [architecture / decomposition axis].** Four-lemma sequence (VG packing →
bump family with separation+norm control → KL bound → Fano) assembled in one
main theorem?
  - Proposed (shallowest tree that fits): yes, four leaf lemmas feeding one
    theorem; no deeper nesting.
  - Chosen: four lemmas + one theorem, depth 2.

All seven defaults adopted; each recorded as a `\todo{user-decision: ...}`
in the relevant `.tex` file and re-surfaced in the Phase D report.

## Phase A.2 — Technical reconnaissance (digests written to .proof-research/)
- Varshamov–Gilbert / Gilbert–Varshamov bound — `varshamov-gilbert.md`
- Local Fano method for minimax lower bounds — `local-fano.md`
- KL divergence between Gaussian-noise regression measures — `gaussian-kl.md`
- Sobolev-norm scaling of a rescaled localized bump — `sobolev-bump-scaling.md`
(No external `\cite{}` is load-bearing in the derivations; standard results are
restated as `\begin{lemma}[\cite{...}]` and the cite keys are digested in
`cite-*.md`. See "Self-check results".)

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 27 (estimated total 45; coverage 60% ≥ 50% threshold).
- After sweep: 23 🟢 / 4 🟡 / 0 🔴.
  - 🟡 (cross-checked via digest, not independently re-derived): Step 13
    (VG Hamming→L² separation), Step 16 (grid-regularity per-cell count),
    Step 20 (VG cardinality $\log M$), Step 24 (Fano inequality + MI bound).
    All four lean on `\cite{tsybakov2009introduction}` (Lemma 2.9 / Thm 2.5)
    or the stated grid hypothesis, matched to citation/technique digests.
- Sub-agents fired: 0 (the load-bearing scaling and balance arithmetic were
  re-derived inline with sympy; report saved to
  `.proof-research/sweep-symbolic-check.md`). No `unable-to-derive`; no 🔴.
- **Two leading-constant slips caught and fixed by the sweep** (rate exponent
  unaffected in both):
  1. Step 23: an intermediate `=` that should have been `≤`
     ($\tfrac{\log2}{128}m^d\le\tfrac14\cdot\tfrac{m^d}{8}\log2$); the proof
     drafted it as equality. Fixed in `06-main-theorem.tex`.
  2. Steps 19/27: $\Delta^2=\tfrac{c_g\omega_0^2}{32 m^{2s}}$ (from
     $(2\Delta)^2=\tfrac{c_g\omega_0^2}{8m^{2s}}$), and $\tfrac{\Delta^2}{2}
     =\tfrac{c_g\omega_0^2}{64 m^{2s}}$; the draft had $128$ and $256$
     (a $4\times$ slip). Fixed in `06-main-theorem.tex`. The minimax rate
     $n^{-2s/(2s+d)}$ is exact and invariant to the leading constant.

## Phase D — Review loop summary
- Ran by the independent five-reviewer panel + author-agent merge/verify loop
  (review-loop.md Components 1–4). The runner agent executed Phases A, B, C, C.5;
  Phase D is the panel's record.
- **Iterations:** 2 (accept gate cleared at iteration 2; 3-iteration cap not hit).
- **Per-iteration mean history:** iteration 1 = 8.00 → iteration 2 = 8.40.
- **Final mean:** 8.40.
- **Accepted:** yes — mean 8.40 > 8 (strict) AND no unresolved REAL-blocking
  critical (Component 4, gate 1).
- **Final five scores (iteration 2):** R1 (line-by-line) = 9, R2
  (assumptions/generality) = 8, R3 (ML-significance) = 7, R4 (math-taste) = 9,
  R5 (derivation-integrity) = 9; mean = 8.40.
- **Fixes at iteration 2:** none — accepted as-is (record only). The iteration-1
  fixes held (no recurrence of the four fixed items #2/#5/#6/#8).
- **Open, surfaced to user (non-blocking):** the "for all $n$" headline vs the
  $m\mid n^{1/d}$ regular-grid subsequence (user-decision Q3, statement-change —
  not auto-applied) and the entangled `lem:kl` exact-count hypothesis. Two
  further iter-2 notes were a narration gloss (Fano diagonal-zero, math valid)
  and a phantom ($Y=D_n$ binding, unambiguous in context); `\todo` markers are
  intentional scaffolding.
- **Iteration traces:** `.proof-research/review-iteration-1.md`,
  `.proof-research/review-iteration-2.md`.

## Where I had to make calls
- **Bump amplitude form.** Used the height-scaling form $\omega\,m^{-s}$ per
  cell with the cell measure $m^{-d}$ tracked explicitly, rather than the
  prompt's $\omega\,m^{-s-d/2}$ (which folds the $L^2$ normalization into the
  amplitude). Both are rate-equivalent; the explicit form makes every change
  of variables auditable. Documented in `.proof-research/sobolev-bump-scaling.md`.
- **Feasibility by rescaling.** Bounded $\|u_\tau\|_{W^s_2}^2\le C_g\omega^2$
  and then set $\omega_0:=C_g^{-1/2}$ so the whole family lies in the unit
  ball — cleaner than threading an unspecified constant through the radius.
- **Resolution as a ceiling.** $m=\lceil Bn^{1/(2s+d)}\rceil$ with the KL
  constraint as the binding lower bound on $m$ (so $m\asymp n^{1/(2s+d)}$ from
  both sides). Stated along the regular-grid subsequence $m\mid n^{1/d}$;
  flagged as a `\todo{user-decision}` (general $n$ needs only a nearest-grid
  interpolation costing constants).
- **Fano constants.** Drove the KL diameter to $\le\tfrac14\log M$ so the
  testing error is $\ge\tfrac12$; chose $B$ to make the substitution cancel
  to $\tfrac{\log2}{128}m^d$.
- All seven Socratic-intake defaults adopted the stronger/tighter option;
  each is a `\todo{user-decision: ...}` in the relevant `.tex` (Q1 in
  `06-main-theorem.tex`, Q3 in `01-preliminaries.tex` and
  `06-main-theorem.tex`, Q4 in `01-preliminaries.tex`, Q6 in `05-fano.tex`).

## Self-check results
- lint.py errors: 0 (R0a–R19 all pass; R19 clean — every proof is
  display-first; no `% lint: ignore` annotations needed).
- latexmk compile_ok: true; `overfull_violations: []`; `undef_refs: []`;
  `undef_cites: []`.
- check_confidence_tags.py: exit 0 (27 tagged, 60% coverage, 0 red issues).
- check_scope.py: exit 0 (declared Appendix; conservative-up allowed).
- Cite-key check: the single `\cite{tsybakov2009introduction}` resolves in
  `refs.bib` and has a citation digest
  (`cite-tsybakov2009introduction-vg-fano.md`). No fabricated citations.
- All `\input`'d section files exist on disk (01–06).

## What's incomplete
- **Phase D** (five-reviewer panel) is intentionally not run here — handled by
  the independent panel.
- **Residual `\todo{user-decision}` markers** (5), all from the Socratic
  self-Q&A defaults, awaiting a human's confirmation:
  Q1 (in-expectation vs in-probability risk), Q3 (regular-grid subsequence
  vs general $n$, appears twice), Q4 (Gaussian known $\sigma^2$), Q6 (local
  Fano vs Le Cam). None blocks the rate; each notes its stronger-default
  rationale and the alternative.
- The external `\cite{gine2016mathematical}` mentioned in a digest as an
  optional Sobolev reference is **not** used in the source (no `\cite` to it),
  so it is correctly absent from `refs.bib`.

v1.2 retrofit: +hyperref, user-decision todos -> decisions.md (5 moved, 0 verify kept)
v1.2 finalize: completed 0 todos, geometry margin=1in
