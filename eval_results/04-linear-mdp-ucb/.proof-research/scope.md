Appendix

# Scope justification

This task proves a high-probability sublinear regret bound for LSVI-UCB on
linear MDPs (Jin-Yang-Wang-Jordan 2020). It requires:

- A concentration / self-normalized lemma (`lem:concentration`).
- A successful-event definition with `Pr >= 1 - delta` union bound.
- An optimism lemma via backward induction over the horizon (`lem:optimism`).
- A per-step recursive regret-decomposition lemma (`lem:recursion`).
- The elliptical-potential lemma (`lem:elliptical`), restated/cited from
  Abbasi-Yadkori-Pal-Szepesvari 2011.
- A main theorem assembling the three-term decomposition T_1 + T_2 + T_3.

That is >= 4 lemmas + 1 theorem, a delta-probabilistic statement, and well
over 30 derivation steps. By the boundaries in SKILL.md Phase A.0a this is
unambiguously **Appendix** scope. Phase C.5 and Phase D are MANDATORY.
