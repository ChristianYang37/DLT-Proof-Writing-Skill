Standard

# Scope rationale

The task is to prove Hoeffding's inequality via the MGF/Chernoff route. The
project contains exactly two theorem-like environments:

- `lem:hoeffding` — Hoeffding's lemma (sub-Gaussian MGF bound for a bounded
  centered random variable), stated and proved.
- `thm:hoeffding` — the main two-sided tail inequality, stated and proved.

This is a single probabilistic statement assembled from one auxiliary lemma,
with an estimated 10–20 derivation steps (Markov → MGF factorization →
Hoeffding's lemma → λ-optimization → two-sided union). That matches the
**Standard** band (1–3 lemmas + ≤ 1 theorem; probabilistic component;
5 < steps ≤ 30). Phase C.5 (confidence sweep) and Phase D (review loop) are
therefore MANDATORY; this run executes A, B, C, and C.5 (Phase D is handled
by an independent panel).
