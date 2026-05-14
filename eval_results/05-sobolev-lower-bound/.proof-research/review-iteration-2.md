# Review iteration 2

## Reviewer review

## Summary

Same proof as iteration 1, with the critical sign-error in the choice of $m$ corrected, the redundancy in the KL-bound proof trimmed, and the $\alpha_\star$ constant reconciled between statement and proof. The proof now correctly establishes the canonical $n^{-2s/(2s+d)}$ minimax lower bound over the Sobolev unit ball $W^s_2([0,1]^d)$, via Varshamov--Gilbert + Tsybakov's Fano-type lemma + a Markov-to-expectation step. The constant $c_{\msf{lb}}$ has the expected $\sigma^{4s/(2s+d)}$ noise dependence.

## Strengths
- The four-lemma decomposition is clean and faithful to the Tsybakov 2009 recipe.
- Each external result (VG, Gaussian KL, Fano) is restated as a labeled \fact/\lemma with a citation digest.
- The numerical Fano constant is computed explicitly ($\geq 0.22$).
- The constant chain $c_\psi \to C_{\msf{KL}} \to \alpha_\star \to c_\rho \to c_{\msf{lb}}$ is tractable and the dependence on $s, d, \sigma, \psi$ is named at each stage.

## Weaknesses

### Weakness #1 (severity: minor)
**Claim:** In the proof of \Cref{lem:prob-lb}, the statement "$\log M \geq (m^d/8) \log 2 - 1$" should clarify the unit: is $-1$ a constant (in $\log$ units), or is $-1$ the additive term from $\log(2^{m^d/8} - 1)$? Strictly, $\log(2^{m^d/8} - 1) \geq (m^d/8)\log 2 - \log 2$ for $m^d \geq 8$ (using $2^{m^d/8} - 1 \geq 2^{m^d/8}/2$). The bound "$-1$" appears to mean "$-\log 2$" but is written ambiguously.
**Evidence:** sections/05-fano-application.tex line 39: "In particular, $\log M \geq (m^d / 8) \log 2 - 1 \geq (m^d / 16) \log 2$".
**Severity:** minor

### Weakness #2 (severity: style)
**Claim:** \Cref{rem:alt-fano} is decorative — it points at variant Fano proofs but doesn't add load-bearing content.
**Evidence:** sections/06-proof-of-thm.tex \Cref{rem:alt-fano}.
**Severity:** style

## Questions for the author
- Does \Cref{ass:design-noise}'s "balanced at scale $m$" condition need to hold uniformly over $m$ ranging up to $n^{1/(2s+d)}$, or just at the specific $m$ chosen in Step 2 of the theorem proof? The current statement is silent on this.

## Verdict
accept-with-minor-revisions

---

## Verification of weaknesses (Component 2)

### Weakness #1 (severity: minor)
**Claim:** Ambiguous "$-1$" in the logarithm bound.
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** Cost cap for minor + REAL-nonblocking is 3 lines. Fix: replace "$-1$" by "$-\log 2$" or rewrite. 1 line fix.

### Weakness #2 (severity: style)
**Claim:** \Cref{rem:alt-fano} is decorative.
**Verdict:** INTENTIONAL
**Rebuttal:** The remark documents alternative reductions; this is standard appendix practice in nonparametric statistics and does no harm. Keep.

## Fixes to apply

1. **Section 05**: clarify the $\log M$ bound.
