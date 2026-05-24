# Review iteration 1

## Reviewer review (peer-review-style)

## Summary

The paper proves the standard minimax lower bound $\mathfrak M_n \gtrsim n^{-2s/(2s+d)}$ for fixed-design Gaussian nonparametric regression over the Sobolev unit ball $W^s_2([0,1]^d)$. The proof follows the canonical Varshamov--Gilbert + bump-construction + Fano recipe. It is decomposed into four named lemmas: (i) norms of the bump family (\Cref{lem:bump-norms}), (ii) closed-form Gaussian KL (\Cref{fac:gaussian-kl}, restated), (iii) KL bound for the bump family (\Cref{lem:kl-bound}), (iv) Tsybakov's Fano-type bound (\Cref{lem:fano-tsybakov}, restated) leading to a probability lower bound (\Cref{lem:prob-lb}). The headline theorem is assembled in \Cref{sec:proof-of-thm} via Markov's inequality and a balance choice of $m$.

The decomposition is clean and follows the textbook treatment of Tsybakov 2009. Constants are tracked through the constant $c_{\msf{lb}}$ and the threshold $\alpha_\star$.

## Strengths

- Clean four-lemma decomposition that mirrors the canonical recipe and is easy to audit.
- Each cited result (VG, Gaussian KL, Fano-type bound) is restated as a \fact or \lemma block with a citation digest, rather than invoked from memory.
- The bump-construction lemma carefully accounts for both the Sobolev seminorm and the $L^2$ norm via disjoint supports.
- Explicit numerical computation of the Fano prefactor ($\geq 0.22$) rather than burying it in $\Omega(1)$.

## Weaknesses

### Weakness #1 (severity: critical)
**Claim:** In Step 2 of the proof of \Cref{thm:main}, the proof states that the choice $m := \lfloor (\alpha_\star \sigma^2 n)^{1/(2s+d)} \rfloor$ satisfies hypothesis Eq.~\eqref{eq:m-condition} of \Cref{lem:prob-lb}. This is wrong: hypothesis Eq.~\eqref{eq:m-condition} reads $n/(\sigma^2 m^{2s+d}) \leq \alpha_\star$, equivalently $m^{2s+d} \geq n/(\alpha_\star \sigma^2)$, i.e., $m \geq (n/(\alpha_\star \sigma^2))^{1/(2s+d)}$. The chosen $m$ goes in the **opposite direction** — $m$ is upper-bounded by $(\alpha_\star \sigma^2 n)^{1/(2s+d)}$, not lower-bounded by the required threshold.
**Evidence:** sections/06-proof-of-thm.tex lines 29--32:
> $m := \lfloor (\alpha_\star \sigma^2 n)^{1/(2s+d)} \rfloor$ ... "by construction $m \leq (\alpha_\star \sigma^2 n)^{1/(2s+d)}$, hence $m^{2s+d} \leq \alpha_\star \sigma^2 n$, which is exactly $n / (\sigma^2 m^{2s+d}) \leq \alpha_\star$ after rearrangement."

But $m^{2s+d} \leq \alpha_\star \sigma^2 n$ gives $\alpha_\star \geq m^{2s+d}/(\sigma^2 n)$, i.e., $n/(\sigma^2 m^{2s+d}) \geq 1/\alpha_\star$, not $\leq \alpha_\star$. The "rearrangement" reverses the inequality direction.
**Severity:** critical

### Weakness #2 (severity: critical, follow-on from #1)
**Claim:** Correspondingly, the final constant $c_{\msf{lb}}$ in Step 3 has $\sigma$-dependence $(\alpha_\star \sigma^2)^{-2s/(2s+d)}$, which gives $\sigma^{-4s/(2s+d)}$ — meaning $\sigma \to 0$ would make the lower bound diverge, contradicting the expected scaling. With the correct $m$ choice ($m \asymp (n/(\alpha_\star\sigma^2))^{1/(2s+d)}$), the constant becomes $c_{\msf{lb}} \asymp (\alpha_\star \sigma^2)^{+2s/(2s+d)}$, giving $\sigma^{+4s/(2s+d)}$, which is the standard $\sigma \to 0 \Rightarrow$ risk $\to 0$ behavior.
**Evidence:** sections/06-proof-of-thm.tex lines 60--62 ($c_{\msf{lb}} := c_\rho^2 c_{\msf{prob}} (\alpha_\star\sigma^2)^{-2s/(2s+d)}$) and sections/06-proof-of-thm.tex \Cref{rem:constants} (which claims the $\sigma$-dependence is $\sigma^{4s/(2s+d)}$ but derives it from a $(\sigma^2)^{-2s/(2s+d)}$ in the formula — the remark itself is inconsistent with the formula above).
**Severity:** critical

### Weakness #3 (severity: minor)
**Claim:** \Cref{lem:prob-lb} introduces $\alpha_\star := \log 2 / (128 C_{\msf{KL}})$ in its statement Eq.~\eqref{eq:m-condition}, but the proof then says it "redefines $\alpha_\star := \log 2 / (256 C_{\msf{KL}})$" to get $\alpha = 1/16 < 1/8$. The lemma statement should match the actual value used.
**Evidence:** sections/05-fano-application.tex Eq.~\eqref{eq:m-condition} (states 128) vs. proof body (redefines to 256). The discrepancy is harmless mathematically but confusing.
**Severity:** minor

### Weakness #4 (severity: minor)
**Claim:** The proof of \Cref{lem:kl-bound} Step 2 has a redundant computation — the bound $\sum_i f_\omega(x_i)^2 \leq (c_\psi/m^s)^2 \|\psi\|_\infty^2 \cdot n$ is derived and then "tightened" by the same factor only via the balance assumption. Without balance, the same bound is recovered; the redundancy adds words without adding content. Suggest deleting the first bound or stating it more economically.
**Evidence:** sections/04-kl-bound.tex Step 2, lines 33--36.
**Severity:** minor

## Questions for the author

- Has the author verified the floor/ceiling careful constant tracking? The factor of 2 from $\lfloor \cdot \rfloor \geq x/2$ is mentioned in Step 3 but does not appear to enter the final constant.
- Should \Cref{lem:fano-tsybakov} be restated as a Fact or external Lemma rather than a Lemma (per the project conventions for restated external results)?

## Verdict
major-revision-required

---

## Verification of weaknesses (Component 2)

### Weakness #1 (severity: critical)
**Claim:** The choice of $m$ satisfies the wrong direction of the hypothesis.
**Verdict:** REAL-blocking
**Rebuttal / fix-plan:** Real bug. Correct fix: replace floor with ceiling and flip the formula. The right choice is $m := \lceil (n / (\alpha_\star \sigma^2))^{1/(2s+d)} \rceil$. With $\lceil x \rceil \geq x$ this gives $m^{2s+d} \geq n/(\alpha_\star\sigma^2)$, i.e., the required $n/(\sigma^2 m^{2s+d}) \leq \alpha_\star$.

### Weakness #2 (severity: critical, follow-on from #1)
**Claim:** Constant has wrong sign on $\sigma^2$ exponent.
**Verdict:** REAL-blocking
**Rebuttal / fix-plan:** Direct consequence of #1. After fixing $m \asymp (n/(\alpha_\star\sigma^2))^{1/(2s+d)}$, $m^{-2s}$ scales as $(\alpha_\star\sigma^2)^{2s/(2s+d)} n^{-2s/(2s+d)}$. The exponent on $(\alpha_\star\sigma^2)$ flips from $-$ to $+$. The remark's $\sigma^{4s/(2s+d)}$ statement was actually correct in spirit but the formula above contradicted it; both will agree after fix.

### Weakness #3 (severity: minor)
**Claim:** $\alpha_\star$ value inconsistent between statement and proof.
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** Fix the lemma statement to use the final value $\log 2 / (256 C_{\msf{KL}})$ throughout.

### Weakness #4 (severity: minor)
**Claim:** Redundant computation in KL bound proof.
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** Cost cap for minor + REAL-nonblocking is 3 lines. Removing the redundant bound is 3 lines. Apply.

## Fixes to apply

1. **Section 06**: rewrite Step 2 with the correct $m$ choice. Update the constant chain in Step 3. Update \Cref{rem:constants}.
2. **Section 05**: change the stated $\alpha_\star$ in Eq.~\eqref{eq:m-condition} to $\log 2 / (256 C_{\msf{KL}})$, and remove the "redefine" paragraph in the proof.
3. **Section 04**: delete the redundant bound in Step 2.
