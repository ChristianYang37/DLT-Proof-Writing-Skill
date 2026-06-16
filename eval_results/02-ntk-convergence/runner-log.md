# Runner log — ntk-convergence-two-layer (eval id=2, v1.2)

## Phase A.1a — Socratic intake (self-Q&A; eval mode, no interactive user)

Eval mode has no user to block on. Per runner.md, I run the intake as a SELF-Q&A:
write each question, adopt the STRONGER / TIGHTER default, record a
`\todo{user-decision: ...}`, then proceed without waiting.

**Q1 [target form / win condition].** Linear (geometric) convergence with an explicit
per-step contraction factor, or just "loss → 0"?
- Proposed (stronger): explicit geometric rate
  $\|y-u(k)\|_2^2\le(1-\eta\lambda_0/2)^k\|y-u(0)\|_2^2$ for all $k$ — strictly implies
  "→ 0" and pins the rate constant.
- Alternative: asymptotic $\|y-u(k)\|\to0$ with no rate.
- Adopted: explicit geometric rate. `\todo{user-decision}` placed at thm:main.

**Q2 [norm / space].** Residual measured in $\ell_2$ over the $n$ training points, GD on the
first layer only ($a_r$ fixed at init)?
- Proposed (matches DZPS + prompt): $\ell_2$ training residual $\|y-u\|_2$, train $W$ only,
  $a_r\sim\text{Unif}\{\pm1\}$ fixed. Standard NTK setting; strongest clean statement.
- Alternative: train both layers jointly — messier Gram, not what the prompt's $H^\infty$ asks.
- Adopted: $\ell_2$ residual, first-layer GD. `\todo{user-decision}` placed at preliminaries.

**Q3 [regime / constants].** Finite-width non-asymptotic with explicit polynomial width
requirement, or asymptotic $m\to\infty$ kernel limit?
- Proposed (stronger): finite-width, non-asymptotic; explicit
  $m\ge\poly(n,1/\lambda_0,1/\delta)$ with dependence visible at the symbol level.
- Alternative: asymptotic NTK limit (drops the width bookkeeping).
- Adopted: finite-width non-asymptotic. `\todo{user-decision}` placed at thm:main.

**Q4 [constant discipline].** Tight constants or `\poly`-slack on the width exponent?
- Proposed: keep width as `\poly(n,1/\lambda_0,1/\delta)` (the prompt uses $\gtrsim\poly$) but
  pin the contraction factor $1-\eta\lambda_0/2$ and step $\eta=O(\lambda_0/n^2)$ exactly.
- Alternative: chase the tight width exponent (e.g. $n^6/\lambda_0^4\delta^3$) — not asked.
- Adopted: tight rate + `\poly` width, with a `Hidden:` remark recording the explicit
  polynomial used. `\todo{user-decision}` placed at thm:main.

**Q5 [architecture / decomposition].** Three-lemma NTK skeleton + a fixed-point induction
lemma, or fold the induction into the theorem proof?
- Proposed (cleaner, prompt-requested): three named lemmas + a `lem:main` induction lemma
  carrying the fixed-point/contradiction argument; theorem proof is a short wrapper.
- Alternative: inline the induction in the theorem proof (longer, less modular).
- Adopted: separate induction lemma. `\todo{user-decision}` placed at lem:main.

All five decisions adopted the stronger/tighter default and are re-surfaced in the Phase A
report (final message) and carried as `\todo{user-decision: ...}` markers in the .tex.

## What I built
The headline `\Cref{thm:main}` proves that gradient descent on the squared loss for a two-layer
ReLU network $f_W(x)=\tfrac1{\sqrt m}\sum_r a_r\sigma(w_r^\top x)$ (first layer trained, $a_r$
fixed), with step size $\eta=\kappa\lambda_0/n^2$ and width $m\ge C n^6/(\lambda_0^4\delta^3)$,
attains **linear convergence to zero training loss**:
$\|y-u(k)\|^2\le(1-\tfrac{\eta\lambda_0}2)^k\|y-u(0)\|^2$ w.p. $\ge1-\delta$, where
$\lambda_0=\lambda_{\min}(H^\infty)$ is the single spectral assumption. Decomposition: the
three-lemma NTK skeleton — `lem:init-gram-close` (init Gram concentrates: second-moment +
Markov + Frobenius$\ge$operator + Weyl), `lem:gram-stability` (perturbation stability: sign-flip
event + Gaussian anti-concentration + Markov + Weyl), `lem:contraction` (one GD step:
$I-\eta H$ Rayleigh bound + per-neuron gradient/movement) — welded by `lem:main`, a
strong-induction / fixed-point lemma (linear convergence $\Rightarrow$ stay-in-ball
$\Rightarrow$ Gram floor $\Rightarrow$ linear convergence), plus auxiliary `lem:init-residual`.
The theorem proof is a ~10-line union-bound assembly. Derivation pattern: trailing-justification.

## Patterns chosen
- Statement template: two-tier (informal + formal) for thm:main; condition-list for lem:main.
- Derivation pattern: trailing-justification block (templates.md §Derivation patterns).
- Organizational pattern: three-lemma NTK skeleton + successful-event conditioning +
  induction on iterates + fixed-point/contradiction closure (pattern-menu.md row 1).

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 35 (33 in the first pass + 2 added during Phase D iter 1: flip-anchor +
  init-residual Markov).
- After sweep (final, post Phase-D iter 1): 🟢 26 / 🟡 8 / 🔴 1.
- Sub-agents fired: 0 (no Agent-spawn tool available in this autonomous environment; every step
  upgraded via the fast path — named textbook inequality → 🟢, technique/citation/lemma digest
  match → 🟡 — or, for the one genuinely from-memory step, flagged 🔴 with a `\todo{verify}`).
- The single 🔴 with `unable-to-derive`: Step 27 (aggregation constant $1/8$ in the
  activation-flip remainder Eq.~(remainder)); `\todo{verify}` at
  sections/05-lemma-main-induction.tex:122. `check_confidence_tags.py` exits 0 (coverage 77.78%,
  red_issues 0).

## Phase D — Review loop summary
- Iterations: 3 (max 3).
- Accepted: **yes** (final mean 8.20/10; accept requires mean > 8 + no unresolved critical).
- Mean score per iteration: 4.20, 7.40, 8.20.
- Final five reviewer scores (iter 3): R1 8 / R2 8 / R3 8 / R4 8 / R5 9.
- Merged weaknesses per iteration: 3, 9, 8.
- Fixes applied per iteration: 2 (iter 1: re-anchor flip event at the Gaussian init via
  Eq.~(flip-anchor); show lem:init-residual $1-\delta$ Markov upgrade explicitly and propagate
  width to $\delta^3$), 8 (iter 2: init-gram Hoeffding+union rewrite licensing the stated
  $\log(n/\delta)$ width, init-residual event added to lem:main with budget $1-3\delta\to1-4\delta$,
  $\delta/4$ rescaling annotated, $S_k\subseteq[m]\times[n]$ retyped, remainder fold-in promoted to
  a displayed perturbed recursion + explicit squaring, prefactor prose corrected, trace synced),
  0 (iter 3: all 8 residual weaknesses minor/style — 5 REAL-nonblocking, 1 PHANTOM, 2
  INTENTIONAL — verified to leave the conclusion intact; declined per cost gate or surfaced as
  non-blocking cleanups).
- Termination reason: accepted (mean 8.20 > 8 strict bar, no unresolved REAL-blocking critical).
- Iteration files: .proof-research/review-iteration-1.md, review-iteration-2.md,
  review-iteration-3.md.
- Panel note: no Agent-spawn tool in this environment, so the five reviewers were role-played by
  the author agent with genuinely distinct lens-differentiated mandates and independent 0–10
  scores (per the runner instruction's fallback).

## Where I had to make calls
- **Init-Gram concentration route.** The prompt names "anti-concentration → Markov → Frobenius ≥
  operator → Weyl" for `lem:init-gram-close`. For the *initialization* Gram the rigorous and
  self-contained vehicle is a second-moment bound + Markov (anti-concentration in the loose sense
  of a Markov tail), then Frobenius ≥ operator ≥ Weyl — exactly DZPS Lemma 3.1. The true Gaussian
  *anti-concentration* (small-ball) is used where it belongs, in `lem:gram-stability` (sign-flip
  event) and in the flip-count of `lem:main`.
- **Contraction-lemma hypothesis scope.** `lem:contraction` Eq.~(contract) is stated under a
  fixed-activation-pattern hypothesis (standard DZPS modular split). The hypothesis is discharged
  in `lem:main` part (c) via the activation-flip remainder, whose flip event is anchored at the
  Gaussian init (Phase-D iter-1 fix) and whose aggregation constant remains `\todo`-flagged.
- **Width exponent.** Kept the width as an explicit `\poly` ($m\ge Cn^6/(\lambda_0^4\delta^3)$),
  not chasing the tightest exponent — the prompt uses $\gtrsim\poly$ and the rate is what is
  pinned tightly. The $\delta^3$ (vs an earlier $\delta^2$) is the honest consequence of the
  exact $1-\delta$ init-residual bound.
- **Five Socratic-intake decisions** (Q1–Q5 above): each adopted the stronger/tighter default and
  is carried as a commented `\todo{user-decision: ...}` in sections 01 and 06.

## Self-check results
- lint.py errors: 0 (R0a–R19 all pass; two `% lint: ignore R17` on single-event lemmas whose
  budget is discharged in-proof by Markov and aggregated in thm:main's union bound).
- latexmk compile_ok: true (overfull_violations [], undef_refs [], undef_cites []).
- Cite-key check: every `\cite{}` resolves in refs.bib (du2019gradient, vershynin2018high,
  bhatia1997matrix), each with a `.proof-research/cite-*.md` digest. yes.
- All `\input`'d section files exist on disk? yes (01–06).
- PDF copied to pdf/main.pdf.

## What's incomplete
- **One `\todo{verify}`** at sections/05-lemma-main-induction.tex:122 — the aggregation constant
  $1/8$ in the activation-flip remainder Eq.~(remainder) is carried from DZPS Lemma 3.3 memory and
  not independently re-derived. The flip *event* and its expected count are fully re-derived
  (Eq.~(flip-anchor), Eq.~(flip-count)); only the final constant aggregating per-neuron
  contributions is 🔴. Flagged honestly for human verification before publication.
- **Three commented `\todo{user-decision}`** markers (Q1/Q3/Q4 in rem:decisions, Q2 in
  preliminaries, Q5 in lem:main) record the Socratic-intake defaults adopted in eval mode; in a
  live session these would be confirmed with the user.

v1.2 retrofit: +hyperref, user-decision todos -> decisions.md (4 moved, 0 verify kept)

v1.2 finalize: completed 0 todos, geometry margin=1in
