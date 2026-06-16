# Runner log — linear-mdp-ucb-regret (eval id=4)

## Phase A.1a — Socratic intake (self-Q&A, Appendix depth)

No interactive user (eval mode). Each question below adopts the STRONGER /
TIGHTER default; each is recorded as a `\todo{user-decision: ...}` in the
relevant `.tex` and re-surfaced here.

### A — Setting

**Q1 [target form / rate].** Should the regret bound be the headline
`d^{3/2} sqrt(H^3 T)` (the correct JYWJ-2020 rate) or the literally-printed
`d^{3/2} sqrt(HT)` from the eval prompt?
- Proposed (STRONGER, CORRECT): prove the honest `\tilde O(d^{3/2}\sqrt{H^3 T})`
  bound that the LSVI-UCB analysis actually yields. The prompt's `sqrt(HT)`
  drops two factors of `H` that the per-step bonus `beta * ||phi||_{Lambda^{-1}}`
  with `beta = \tilde O(dH)` provably incurs.
- Alternative: parrot `sqrt(HT)`, which is not provable under the stated
  bonus and would be a fabricated rate.
- Decision: prove `d^{3/2}\sqrt{H^3 T}`; log the prompt's `sqrt(HT)` as a
  `user-decision` discrepancy. (This mirrors the README note for eval 4.)

**Q2 [confidence radius / bonus constant].** Tight constant on `beta` or
`\poly`-slack?
- Proposed (STRONGER where honest): keep `beta = C_beta * d H \sqrt{\iota}`
  with `\iota = \log(2 d T / \delta)` and an explicit but un-optimized
  universal `C_beta`. The exact numeric constant in JYWJ is not load-bearing
  for the rate; pinning it would be false precision.
- Alternative: a fully optimized constant — not what the rate-level claim needs.
- Decision: symbolic `C_beta`, dependency-tagged; `\todo{verify: C_beta}` so a
  human can pin it. Rate exponents are exact.

**Q3 [norm / space].** Which norm for the confidence ellipsoid and which
filtration?
- Proposed (STANDARD, STRONGEST): the `Lambda_{k,h}^{-1}` (Mahalanobis /
  elliptical) norm on `R^d`, with the natural per-episode filtration
  `F_{k,h}`. This is the norm the self-normalized bound and elliptical
  potential are stated in.
- Alternative: Euclidean `\ell_2` — too weak; loses the data-adaptive bonus.
- Decision: elliptical norm `||.||_{Lambda^{-1}}`.

**Q4 [regime].** Finite-sample (all `K, H, T`) or asymptotic?
- Proposed (STRONGER): non-asymptotic, valid for every `K >= 1`, `H >= 1`.
- Decision: non-asymptotic.

**Q5 [win condition].** Cumulative regret `Regret(K) = sum_k (V_1^*(s_1^k) -
V_1^{pi^k}(s_1^k))` bounded high-probability, with `T = KH`.
- Decision: yes — high-probability (`>= 1 - delta`) bound on cumulative
  regret; `T := KH` is the number of steps.

**Q6 [citations].** Which results may be cited vs proved?
- Proposed (CONSERVATIVE = research-from-scratch unless named): cite only
  (i) the elliptical-potential / determinant-trace lemma
  (Abbasi-Yadkori-Pal-Szepesvari 2011, Lemma 11), and (ii) the
  Hoeffding/self-normalized concentration scaffold (same paper, Theorem 1).
  Everything else (linear-MDP value-function linearity, optimism induction,
  regret decomposition) is proved in-file.
- Decision: two citations, both digested in `.proof-research/`.

### B — Architecture

**Q7 [decomposition axis].** Shallowest tree that fits.
- Proposed: four leaf lemmas feeding one theorem:
  1. `lem:linear-q` — under the linear-MDP assumption the LSVI Q-iterate is
     linear in `phi`, with a closed-form weight `w_{k,h}`.
  2. `lem:concentration` — self-normalized bound controlling the LSVI
     fixed-point error, giving the successful event `\mathcal E`.
  3. `lem:optimism` — on `\mathcal E`, backward induction shows
     `Q_{k,h} >= Q^*_h` (optimism) and a per-step bonus bound.
  4. `lem:elliptical` — elliptical potential lemma (cited).
  Main theorem `thm:regret` assembles the `T_1 + T_2 + T_3` decomposition,
  bounds each, and closes `T_2` with `lem:elliptical`.
- Decision: this 4-lemma + 1-theorem flat tree.

**Q8 [lemma boundaries].** Each named lemma has >= 1 downstream consumer
(checked in dependency-graph.md). No orphan lemmas.

**Q9 [reductions off-limits].** None requested; the slice is the standard
JYWJ optimism + elliptical-potential route. No off-limits reductions.

## What I built
(to be filled through Phase C.5)

## Phase D — Review loop (five-reviewer panel)

**Status:** COMPLETE — **ACCEPTED** at iteration 2.
**Iterations run:** 2 (of 3-iteration hard cap).
**Per-iteration mean history:** iteration 1 = 8.00 → iteration 2 = 8.40.
**Final mean:** 8.40.
**Accept gate:** mean 8.40 > 8 (strict) AND no unresolved REAL-blocking critical ⇒ **accepted = yes**.

### Final five scores (iteration 2)
| Reviewer | Lens | Score | Blocking |
|---|---|---|---|
| R1 | correctness: line-by-line | 8 | no |
| R2 | correctness: assumptions/generality | 8 | no |
| R3 | correctness: ML-significance | 9 | no |
| R4 | math-taste | 8 | no |
| R5 | derivation-integrity | 9 | no |
| **mean** | | **8.40** | |

### Outcome
Six merged/deduped weaknesses verified: 4 REAL-nonblocking (imprecise-but-lower-order discretization chain at 02-concentration.tex:113–120; stale `eq:T3/T12-bound` labels + confidence-trace term names; Azuma increment over-attributed to optimism; prose P_h-monotonicity), 2 INTENTIONAL (symbolic C_β constant — the sole 🔴, a flagged A.1a Q2 user decision; P_h-monotonicity also graded INTENTIONAL), 0 PHANTOM, 0 REAL-blocking, 0 critical. **No fixes applied** (accepted proofs are recorded, not modified); each REAL-nonblocking item carries a ≤3-line deferred fix-plan. Iteration-1 fixes (CS-factor naming, two-term relabel, discretization display, predictability clause, dead-macro removal) lifted four lenses from 8.00 → 8.40.

### Trace
- `.proof-research/review-iteration-1.md` (iteration 1, mean 8.00, fixes applied)
- `.proof-research/review-iteration-2.md` (iteration 2, mean 8.40, accepted, no changes)

v1.2 retrofit: +hyperref, user-decision todos -> decisions.md (2 moved, 1 verify kept)

- v1.2 finalize: completed 1 todos, geometry margin=1in
