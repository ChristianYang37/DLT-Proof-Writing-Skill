# Contributing

> **PRs are not accepted at this stage.**

This repository is in active design. The test suite, grading rubric, and convergence criteria for the Phase D review loop are still maturing. Accepting external pull requests before those mechanisms are robust would degrade signal: changes proposed in good faith might pass a weak rubric but break in real use, and we have no reliable way to tell.

Once the following are in place, we will open the project to community contributions:

1. **Stronger eval coverage** — currently 5 representative proofs across optimization, learning theory, statistical rates, RL, and lower bounds. Need ≥ 15 evals spanning fine-grained complexity, mean-field analysis, online learning, and adversarial robustness.

2. **Grader sub-agent stability** — the v2 hand-graded run had 100% pass rate, but the grader sub-agent template (`agents/grader.md`) has not been stress-tested against intentionally-broken proofs (false negatives). A grader that always says "pass" is worthless as a signal.

3. **Anti-Goodharting checks** — once the eval rubric is mature, contributors might optimize for assertion pass rate at the expense of actual proof quality. Need anti-pattern detectors that watch for "specifies all assertions, real math is sloppy".

4. **Version stability of upstream skills format** — Anthropic's Agent Skills spec is evolving. We need to pin to a stable version before accepting changes that depend on bleeding-edge plugin features.

## How to provide feedback in the meantime

- **Open an Issue** describing the bug or improvement. Reproduction steps are essential. Tag with `skill-content`, `eval-coverage`, `tooling`, or `docs`.
- **Cite the failure** — if you ran the skill on your own proof and it produced a bad output, include the prompt, the bad output, the runner-log, and what should have happened instead. We collect these as candidate evals.
- **Do NOT** fork-and-rebrand for commercial purposes — the license is CC BY-NC 4.0.

## Why this caution

A proof skill that ships a wrong proof confidently is worse than no skill at all. The eval system is the only thing standing between "this approach works" and "this approach hallucinates eloquently". Until the evals are strong enough to catch hallucinations reliably, contributions risk introducing unmeasurable regressions.

We expect to revisit this policy as the project matures. Star the repo if you want to be notified when contributions open.
