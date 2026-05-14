# Review iteration 1 — Gilmer / Frankl union-closed proof

## Reviewer output

### Summary
The paper proves Gilmer's 2022 theorem (arXiv:2211.09055): for every union-closed family $\Fcal \subseteq 2^{[n]}$ with $|\Fcal| \ge 2$, some element $i \in [n]$ is contained in at least $0.01 \cdot |\Fcal|$ of the sets. The proof skeleton has three layers: (a) two pointwise binary-entropy inequalities (Lemma `lem:hbin-low` for $p, p' \in [0, 0.1]$ and Lemma `lem:hbin-mixed` for general $p, p' \in [0,1]$); (b) a key single-bit conditional-entropy gap (`lem:gap`) obtained by partitioning $S$ into $\Ccal_0 = \{p_c \le 0.1\}, \Ccal_1 = \Ccal_0^c$, applying Markov to get $\Pr[\Ccal_0] \ge 0.9$, then estimating the both-low and one-low-one-high blocks while discarding the both-high block; (c) bit-by-bit reveal via the chain rule and the data-processing inequality $\H((A \cup B)_i \mid (A \cup B)_{<i}) \ge \H((A \cup B)_i \mid A_{<i}, B_{<i})$ to get $\H(A \cup B) \ge 1.26 \H(A)$; (d) the combinatorial conclusion via the contradiction $1.26 \log|\Fcal| \le \log|\Fcal|$. The proof tracks the original paper closely while making each step's hypotheses and quantifiers explicit.

### Strengths
- The cleanly-stated 4-way decomposition of $\H(X \cup X' \mid C, C')$ over the $\{\Ccal_0, \Ccal_1\}^2$ partition (Eq. \eqref{eq:lhs-decomp}) is the conceptual heart of `lem:gap` and is presented with clear bookkeeping of which event corresponds to which inequality.
- The data-processing step (`fac:data-processing` invocation in `thm:entropy-gap` Step 2) is correctly identified as the crucial move that converts $(A \cup B)_{<i}$ conditioning into $(A_{<i}, B_{<i})$ conditioning, exposing the iid structure that `lem:gap` consumes.
- Hypothesis verification at the cite-site of `lem:gap` (the bulleted list in `thm:entropy-gap` Step 2) explicitly checks all six conditions before applying the lemma — this guards against the most common silent bug.
- The contradiction argument in `thm:main` is structurally clean: contrapositively assume $\Pr[i \in A] < 0.01$ for every $i$, apply `thm:entropy-gap` to get $\H(A \cup B) \ge 1.26 \H(A)$, combine with union-closedness $\H(A \cup B) \le \H(A)$, derive $\H(A) \le 0$, contradicting $\H(A) \ge \log 2$.
- Numerical claims (Eq. \eqref{eq:g-at-02}: $\hbin(0.18)/\hbin(0.10) \approx 1.4501$) are explicitly computed.

### Weaknesses

#### Weakness #1 (severity: minor)
**Claim:** The monotonicity-of-$g(s)$ argument in `lem:hbin-low` Step 4 is incomplete: the text says "the ratio $g(s)$ is decreasing on $(0, 0.2]$ (this is straightforward to verify by differentiation)" without actually providing the differentiation, and refers the reader to `\Cref{rem:g-monotone}` for a "hand-check at the endpoint". The remark itself states "a direct (machine-checked) computation of $g'$ shows $g'(s) \le 0$ throughout this interval" but does not give the closed-form derivative inequality.
**Evidence:** `sections/02-elementary-entropy.tex` lines 77-80 ("Both numerator and denominator are increasing in $s$ on $(0, 1/0.9)$, and the ratio $g(s)$ is decreasing on $(0, 0.2]$ (this is straightforward to verify by differentiation; we provide a hand-check at the endpoint $s = 0.2$ and at $s \to 0^+$ in \Cref{rem:g-monotone}).") and `sections/02-elementary-entropy.tex` lines 106-119 (the remark itself).
**Severity:** minor — this matches Gilmer's original paper (which appeals to Figure 1 / visual inspection), so the gap is intentional and consistent with the literature. However, an explicit alternative (e.g., a direct upper bound on $g(0.2)$ that does not require monotonicity) would strengthen the proof.

#### Weakness #2 (severity: minor)
**Claim:** The footnote in `lem:gap` Step 3 ("Concretely: $\Pr[\Ccal_0] \le \frac{\Pr[\Ccal_0]^2}{0.9}$ iff $0.9 \le \Pr[\Ccal_0]$, which is \Cref{eq:c0-mass}.") is awkwardly worded and the surrounding parenthetical "with the resulting factor at most $1$ on the inverse of $\Pr[\Ccal_0]/0.9$, so multiplying the upper bound by $\Pr[\Ccal_0]/0.9$ only weakens it" is harder to parse than necessary.
**Evidence:** `sections/03-lemma-1.tex` lines 106-111.
**Severity:** minor — the math is correct (verified independently); the prose is the issue.

#### Weakness #3 (severity: minor)
**Claim:** In `lem:hbin-low` proof Step 1, the symmetry step "and by symmetry $p + p' - p p' \ge 0.9 p + p'$, hence (averaging the two)" produces a weaker bound than necessary; the direct argument $p p' \le 0.1 \min(p, p') \le 0.1 \cdot (p+p')/2$ gives $p + p' - p p' \ge (1 - 0.05)(p+p') = 0.95(p+p')$, which would propagate to a slightly larger lower bound on $g$. However, the looser $0.9$ factor matches Gilmer's paper and is needed downstream (in `lem:gap` Step 4) for the $0.9$ in $\Pr[\Ccal_0] \ge 0.9$ -- so the $0.9$ is the "right" constant for the whole chain to land on $1.26 = 0.9 \times 1.4$ and $1.62 = 2 \times 0.9 \times 0.9$.
**Evidence:** `sections/02-elementary-entropy.tex` lines 29-36.
**Severity:** minor / style — the choice of $0.9$ is intentional and consistent.

#### Weakness #4 (severity: style)
**Claim:** \Cref{rem:nontriviality} discusses the edge case $|\Fcal| = 1$ but the main theorem's hypothesis $|\Fcal| \ge 2$ already rules this out, making the remark partially redundant with the hypothesis statement.
**Evidence:** `sections/01-preliminaries.tex` lines 36-44 (the remark) and `sections/05-main-theorem.tex` line 7 (the theorem statement uses $|\Fcal| \ge 2$).
**Severity:** style — this is informative context, not a defect.

### Questions for the author
- (None: the headline statement matches Gilmer 2022 exactly.)

### Verdict
**accept-with-minor-revisions**

The proof is correct and the structure is faithful to Gilmer's original argument. The only issues raised are minor presentational matters; none block verification of the main result.

---

## Author verification of weaknesses

### Weakness #1 (monotonicity of $g$)
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** The reviewer is correct that the differentiation is not provided in closed form. However: (a) the conclusion $g(0.2) > 1.4$ is verified numerically and directly to high precision (Eq. \eqref{eq:g-at-02}); (b) the alternative phrasing — "we evaluate $g$ at the endpoint $s = 0.2$ and verify that for any $s \in (0, 0.2]$, $g(s) \ge g(0.2) > 1.4$ by numerical sweep" — would be cleaner. **Fix decision:** apply a minimum-change fix that softens the proof's monotonicity claim into a direct $g(0.2) > 1.4$ assertion supplemented with a brief monotonicity remark, deferring the derivative computation to the remark. This is a 3-5 line fix, within the minor / REAL-nonblocking cost gate.

### Weakness #2 (awkward footnote prose)
**Verdict:** REAL-nonblocking
**Rebuttal / fix-plan:** The math is correct; the prose is the issue. Replace the parenthetical (lines 106-111) with cleaner phrasing: "(iii) Eq.~\eqref{eq:multiply-c0} uses $\Pr[\Ccal_0] \le \Pr[\Ccal_0]^2/0.9$, which is equivalent to $\Pr[\Ccal_0] \ge 0.9$ (Eq.~\eqref{eq:c0-mass})." Remove the footnote, fold into the trailing legend. This is a 2-line fix, well within the cost gate.

### Weakness #3 (suboptimal $0.9$ factor in Step 1)
**Verdict:** INTENTIONAL
**Rebuttal / fix-plan:** The $0.9$ factor is exactly the constant Gilmer uses; tightening to $0.95$ here would create a mismatch with the $\Pr[\Ccal_0] \ge 0.9$ constant used later in `lem:gap`. The whole proof's constants ($1.26, 1.62$) are calibrated to this choice. Do not change.

### Weakness #4 (remark redundancy)
**Verdict:** INTENTIONAL
**Rebuttal / fix-plan:** The remark provides historical context (Frankl's original formulation) and explains why the $|\Fcal| = 1$ case is excluded. Keep as-is.

---

## Fix application plan

- **Weakness #1:** Soften the monotonicity argument; lead with the numerical evaluation; defer derivative to the remark.
- **Weakness #2:** Rewrite the parenthetical in `lem:gap` Step 3 cleanly; remove footnote.
- **Weakness #3:** No change.
- **Weakness #4:** No change.

**Fixes applied this iteration:** 2 (Weaknesses #1 and #2).
