# Benchmark report — DLT Proof Writing Skill v1.0

**Skill version:** v1.0 (full workflow: Phase A → B → C → C.5 → D, with experiment design)
**Eval run date:** 2026-05-14
**Configuration:** with-skill (5 parallel `general-purpose` sub-agents each loading the skill)
**Grader:** hand-grade per [`proof-writing-skill/agents/grader.md`](../proof-writing-skill/agents/grader.md) using `scripts/lint.py` + `scripts/latexmk-wrapper.py` + manual file inspection

## Summary

```
==============================================================================
Eval                              Pass  Fail   N/V  Total   Phase D verdict
==============================================================================
1 hoeffding-prove                    9     0     0      9   accept-as-is
2 ntk-convergence-two-layer         12     0     0     12   accept-as-is
3 vc-generalization                  8     0     0      8   accept-with-minor
4 linear-mdp-ucb-regret             12     0     0     12   accept-as-is
5 sobolev-minimax-lower-bound        9     0     0      9   accept-as-is
==============================================================================
TOTAL                               50     0     0     50   100% pass rate
==============================================================================
```

## Per-eval verdicts

### Eval 1 — Hoeffding's inequality ([proof PDF](01-hoeffding/pdf/main.pdf))
- 5-page PDF, 0 lint errors, 0 LaTeX warnings, all cross-refs resolve
- **Phase C.5**: 29 steps → 🟢 26 / 🟡 3 / 🔴 0 (zero sub-agents fired, all fast-path verifiable)
- **Phase D**: 2 iterations → `accept-as-is` (3 weaknesses iter 1: 2 fixed + 1 INTENTIONAL; 1 weakness iter 2 already addressed)
- No fabricated citations (textbook material, no `\cite{}` used)
- See: [grading.json](01-hoeffding/grading.json) · [runner-log](01-hoeffding/runner-log.md)

### Eval 2 — NTK two-layer convergence ([proof PDF](02-ntk-convergence/pdf/main.pdf) · [experiments plan](02-ntk-convergence/experiments-plan.md))
- 0 lint errors, compile_ok, all cite keys verified in `refs.bib`
- **Phase C.5**: 32 steps → 🟢 29 / 🟡 3 / 🔴 0; two initial 🔴 with `\todo{verify}` markers resolved to 🟢 during Phase D iter 1 fixes (exemplary C.5 → D handoff)
- **Phase D**: 2 iterations → `accept-as-is` (5 weaknesses iter 1: W1,W2 major fixed + W4,W5 minor fixed + W3 INTENTIONAL; 3 minor style iter 2 all fixed)
- **Experiments plan**: 10 seeds, 2 baselines (kernel regression, linear), 3 ablations (η, λ_0, d), 4 figures + 1 table, pre-registered confirm/refute thresholds, **Results section blank**
- See: [grading.json](02-ntk-convergence/grading.json) · [runner-log](02-ntk-convergence/runner-log.md)

### Eval 3 — VC generalization bound ([proof PDF](03-vc-generalization/pdf/main.pdf))
- 8-page PDF, 0 lint errors, compile_ok
- **Phase C.5**: 35 steps → pre-D 🟢 26 / 🟡 7 / 🔴 2 (Sauer property (b) sketch + main-proof Step 4 absorption); post-D 🟢 28 / 🟡 7 / 🔴 0 — both 🔴 fixed by Phase D iter 1
- **Phase D**: 2 iterations → `accept-with-minor-revisions` (5 weaknesses iter 1: 4 fixes; 2 weaknesses iter 2 all PHANTOM/INTENTIONAL → no-fixes-applied termination)
- See: [grading.json](03-vc-generalization/grading.json) · [runner-log](03-vc-generalization/runner-log.md)

### Eval 4 — Linear MDP UCB regret ([proof PDF](04-linear-mdp-ucb/pdf/main.pdf) · [experiments plan](04-linear-mdp-ucb/experiments-plan.md))
- 0 lint errors, compile_ok, refs.bib resolves 3 cite keys (Jin 2020, Abbasi-Yadkori 2011, Azuma 1967)
- **Phase C.5**: 15 steps → 🟢 10 / 🟡 4 / 🔴 1 (bonus-constant tightness, honestly flagged with `\todo{}`)
- **Phase D**: 2 iterations → `accept-as-is` (5 weaknesses iter 1: 3 fixed + 2 INTENTIONAL; 2 weaknesses iter 2: 1 fix + 1 INTENTIONAL)
- **Runner caught a math error in the eval prompt** ($\widetilde O(d^{3/2}\sqrt{HT})$ should be $\widetilde O(d^{3/2}\sqrt{H^3 T})$ per Jin et al. 2020 Thm 3.1), documented in `rem:rate_unpacking`
- **Experiments plan**: 10 seeds [1..10], 3 baselines (eps-greedy, random, Thompson-style LSVI), 3 ablations, 4 figures, pre-registered slope intervals $\widehat\alpha_T \in [0.45, 0.55]$, $\widehat\alpha_d \in [1.35, 1.65]$, **Results blank**
- See: [grading.json](04-linear-mdp-ucb/grading.json) · [runner-log](04-linear-mdp-ucb/runner-log.md)

### Eval 5 — Sobolev minimax lower bound ([proof PDF](05-sobolev-lower-bound/pdf/main.pdf))
- 7-page PDF, 0 lint errors, compile_ok, Tsybakov 2009 cites verified via citation digest
- **Phase C.5**: 25 steps → 🟢 21 / 🟡 4 / 🔴 0 (no `\todo{}` residuals)
- **Phase D**: **3 iterations** → `accept-as-is`. **Iter 1 caught 2 critical sign errors** (the $m$-choice exponent + a $\sigma$-exponent sign bug), both REAL-blocking and fixed. Iter 2: 1 fix + 1 INTENTIONAL. Iter 3: 0 weaknesses, accept.
- **Strongest demonstration in this benchmark of why Phase D matters**: without the review loop, two critical sign errors would have shipped.
- See: [grading.json](05-sobolev-lower-bound/grading.json) · [runner-log](05-sobolev-lower-bound/runner-log.md)

## What the workflow caught (highlights)

| Failure mode | Where caught | Outcome |
|---|---|---|
| Sign error in $m$-choice (Sobolev lower bound) | Phase D reviewer iter 1 | fixed before final |
| Sign error in $\sigma$-exponent (Sobolev) | Phase D reviewer iter 1 | fixed before final |
| Missing absolute value in Rademacher def (VC) | Phase D reviewer iter 1 | fixed |
| `\todo{verify}` markers on 🔴 steps (NTK) | Phase C.5 sweep | resolved by D iter 1 fixes |
| Bonus-constant tightness gap (Linear MDP UCB) | Phase C.5 sweep | flagged with `\todo{}` for human review |
| Math error in the eval prompt itself (Linear MDP UCB rate) | Runner during Phase A | flagged in `rem:rate_unpacking`, prompt acknowledged |
| Mathematical normalization mismatch (Sobolev bump family) | Runner during Phase A | deviated to Tsybakov-standard parametrization, documented |

## Limitations of this benchmark

1. **No "without-skill" baseline run.** This iteration's evals were run only with the skill loaded. A proper benchmark needs a no-skill baseline to measure the skill's value-add. (Planned for next iteration.)

2. **Hand-graded, not sub-agent-graded.** The grader sub-agent template exists at `proof-writing-skill/agents/grader.md` but quota constraints forced hand-grading by the parent agent. A separate sub-agent grader run would be more independent.

3. **Five evals are too few.** Coverage gaps: fine-grained complexity reductions, mean-field / Langevin dynamics, online learning regret, adversarial robustness. Plan: expand to ≥ 15 evals before v2.0.

4. **No anti-Goodharting tests.** All 5 evals are designed to be solvable; we have no eval where the "correct answer" is "the claim is false / under-specified". Adding such evals tests whether the skill will report negative results honestly.

## Reproducing the benchmark

```bash
# 1. Install the skill
cp -r proof-writing-skill ~/.claude/skills/dlt-proof-writing

# 2. Run each eval in a fresh sub-agent context (parallel recommended)
#    See agents/runner.md for the prompt template

# 3. Grade (either via sub-agent per agents/grader.md, or by hand)

# 4. Aggregate into a per-eval grading.json + this benchmark.md
```
