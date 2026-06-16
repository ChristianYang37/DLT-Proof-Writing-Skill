# Scope declaration

Appendix

## Rationale

This is an appendix-grade, paper-level proof in the style of Du–Zhai–Poczos–Singh
2019. It requires:

- **≥ 3 named lemmas**: `lem:init-gram-close` (initialization Gram concentration),
  `lem:gram-stability` (perturbation stability of the Gram matrix),
  `lem:contraction` (one-step loss contraction + weight-movement bound), plus a
  `lem:main` induction lemma tying them together via a fixed-point / contradiction
  argument.
- **A main theorem** `thm:main` whose proof is a short cross-reference assembly.
- **A high-probability statement** with an explicit `1 - \delta` budget and a union
  bound over the concentration events.
- **> 30 estimated derivation steps** across the four lemma proofs and the theorem.

All three criteria (≥ 3 lemmas, paper-level, > 30 steps) independently force the
**Appendix** classification. Phase C.5 (confidence sweep) and Phase D (five-reviewer
panel) are therefore MANDATORY.
