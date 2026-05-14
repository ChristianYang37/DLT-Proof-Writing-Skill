# Verification of iteration-1 review

### Weakness #1 (severity: major)
**Claim:** The proof of \Cref{lem:concentration} compresses the Bellman-residual identity without derivation.
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** The identity is correct (verified hand-derivation in Step 5 of confidence-trace.md). It is, however, asserted without derivation. The minimum-change fix: add a one-line derivation in section 3 showing how $\widehat w_h^k - w_h^* = (\Lambda_h^k)^{-1}\sum_\tau \phi_\tau \eta_\tau - \lambda (\Lambda_h^k)^{-1} w_h^*$ falls out of the definitions. Patch cost ≤ 4 lines, severity major + REAL-nonblocking → fix.

### Weakness #2 (severity: major)
**Claim:** Off-by-one in residual bound: "$2 \cdot K \cdot \tfrac{1}{K} \cdot \sqrt k$" is dimensional nonsense.
**Verdict:** REAL-nonblocking (the in-line trailer text fixes the bound correctly, but the displayed chain shows the wrong intermediate)
**Rebuttal / fix-plan:** Re-reading the source, the displayed chain has $2 \cdot K \cdot (1/K) \cdot \sqrt k$ which would expand to $2\sqrt k$ — actually that *is* algebraically correct in the rough form, but it's confusing. The trailer text correctly identifies $\bigl\|\sum_\tau e_\tau \phi_\tau\bigr\|_{(\Lambda)^{-1}}^2 \le (2/K)^2 d \le 4/K$, which gives a residual of $2/\sqrt K$. The "$2 K (1/K) \sqrt k$" in the display is a typo for "$\le 2 \cdot (1/K) \cdot \sqrt k \cdot \sqrt d$" or similar. Fix: replace the second line of the displayed chain with the corrected intermediate. Patch cost ≤ 3 lines.

### Weakness #3 (severity: minor)
**Claim:** $\Otil(d^{3/2}\sqrt{H^3 T})$ form is less standard than $\Otil(d^{3/2} H \sqrt{HK})$.
**Verdict:** INTENTIONAL
**Rebuttal:** Both forms are common in the literature. The current statement uses $T = KH$ as the iteration count, which is the form most aligned with bandit-style $\sqrt T$ regret. \Cref{rem:rate_unpacking} discusses the form match. No fix.

### Weakness #4 (severity: minor)
**Claim:** Lemma cover elides the Lipschitz computation.
**Verdict:** INTENTIONAL
**Rebuttal:** The Lipschitz computation is approximately 1.5 pages in Jin et al. (Lemma D.6). Reproducing it here would add no insight and bloat the document. The citation is to a peer-reviewed paper. No fix.

### Weakness #5 (severity: minor, style)
**Claim:** "$\|u\|_2 \le 1$" is implicit but not stated.
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** Make "for unit $u$" explicit in the opening line of the proof. Patch cost: 1 token. Fix.

## Decision summary

- Fix: W1 (add identity derivation), W2 (correct typo in display), W5 (clarify unit-vector).
- Don't fix: W3 (intentional rate form), W4 (intentional citation deferral).

Statement-change required: no.
