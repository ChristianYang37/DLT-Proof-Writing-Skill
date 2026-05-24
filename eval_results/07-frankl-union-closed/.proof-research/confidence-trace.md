# Confidence trace — eval 07 (Gilmer / Frankl union-closed)

Enumeration of every non-trivial derivation step across the four proofs in
`sections/02-elementary-entropy.tex`, `sections/03-lemma-1.tex`,
`sections/04-theorem-entropy.tex`, and `sections/05-main-theorem.tex`.

Steps are flat-indexed for cross-reference with TodoWrite. Each step starts
🔴 `from-memory` and is upgraded via the dispatch table in
`references/confidence-sweep.md`.

---

## Lemma 2 (small-probability ratio bound), sections/02-elementary-entropy.tex

### Step 1
**Location:** sections/02-elementary-entropy.tex (Step 1 of proof)
**Content:** For $p, p' \in [0, 0.1]$, $p + p' - p p' \ge 0.9 (p + p')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $p p' \le 0.1 \min(p, p') \le 0.1 \cdot \tfrac{p+p'}{2}$ gives $p+p'-pp' \ge p+p' - 0.1\cdot\tfrac{p+p'}{2} \ge 0.9(p+p')$ via averaging the two one-sided bounds $p+p'-pp' \ge p+0.9p'$ and $p+p'-pp' \ge 0.9p+p'$.
**Sub-agent task id:** none

### Step 2
**Location:** sections/02-elementary-entropy.tex (Step 1)
**Content:** $\hbin(p + p' - p p') \ge \hbin(0.9 (p + p'))$ when both sides have argument in $[0, 1/2]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\hbin$ is non-decreasing on $[0,1/2]$ (textbook); since $0 \le 0.9(p+p') \le p+p'-pp' \le p+p' \le 0.2 < 1/2$, monotonicity applies.
**Sub-agent task id:** none

### Step 3
**Location:** sections/02-elementary-entropy.tex (Step 2)
**Content:** $\tfrac{\hbin(p)+\hbin(p')}{2} \le \hbin\bigl(\tfrac{p+p'}{2}\bigr)$ by concavity.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct Jensen with $\lambda = 1/2$; concavity of $\hbin$ is `\Cref{fac:hbin-concave}`.
**Sub-agent task id:** none

### Step 4
**Location:** sections/02-elementary-entropy.tex (Step 4, monotonicity of g)
**Content:** $g(s) = \hbin(0.9 s)/\hbin(0.5 s)$ is non-increasing on $(0, 0.2]$, so $\min g = g(0.2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Numerical sweep (60-point grid on $[0.001, 0.2]$) in Phase A confirmed that $g$ is decreasing and achieves minimum $\approx 1.4501$ at $s = 0.2$. The analytic derivative argument is sketched in `\Cref{rem:g-monotone}`; the proof retains a `\todo{}`-free elementary monotonicity claim verified by computation. Tag remains 🟡 (cross-checked) because we used numerical evidence rather than a closed-form derivative inequality.
**Sub-agent task id:** none

### Step 5
**Location:** sections/02-elementary-entropy.tex (Step 5)
**Content:** $g(0.2) = \hbin(0.18)/\hbin(0.10) \approx 1.4501 > 1.4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Python computation in Phase A: $\hbin(0.18) \approx 0.6801$, $\hbin(0.10) \approx 0.4690$, ratio $\approx 1.4501$.
**Sub-agent task id:** none

---

## Lemma 3 (mixed-regime bound), sections/02-elementary-entropy.tex

### Step 6
**Location:** sections/02-elementary-entropy.tex (Lemma 3 proof)
**Content:** $p + p' - p p' = p \cdot 1 + (1 - p) \cdot p'$ (convex combination identity).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-expansion: $p \cdot 1 + (1-p) p' = p + p' - p p'$.
**Sub-agent task id:** none

### Step 7
**Location:** sections/02-elementary-entropy.tex (Lemma 3 proof)
**Content:** $\hbin(p \cdot 1 + (1-p) p') \ge p \cdot \hbin(1) + (1-p) \hbin(p') = (1-p) \hbin(p')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of concavity of $\hbin$ (`\Cref{fac:hbin-concave}`); $\hbin(1) = 0$ by definition.
**Sub-agent task id:** none

---

## Lemma 1 / `lem:gap`, sections/03-lemma-1.tex

### Step 8
**Location:** sections/03-lemma-1.tex (Step 1, Markov)
**Content:** $\Pr[\Ccal_1] = \Pr[p_c > 0.1] \le \E[p_c]/0.1 \le 0.01/0.1 = 0.1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard Markov inequality applied to non-negative $p_c$ with threshold $0.1$ and mean $\le 0.01$.
**Sub-agent task id:** none

### Step 9
**Location:** sections/03-lemma-1.tex (Step 1, complement)
**Content:** $\Pr[\Ccal_0] \ge 0.9$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Complement of Step 8: $\Pr[\Ccal_0] = 1 - \Pr[\Ccal_1] \ge 1 - 0.1 = 0.9$.
**Sub-agent task id:** none

### Step 10
**Location:** sections/03-lemma-1.tex (Step 2)
**Content:** Decomposition $\H(X \mid C) = \Pr[\Ccal_0] \H(X \mid \Ccal_0) + \Pr[\Ccal_1] \H(X \mid \Ccal_1)$ and the analogous 4-way decomposition of $\H(X \cup X' \mid C, C')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard tower-property decomposition of conditional entropy over a partition; both lines are line-by-line expansions of the definition of conditional entropy via partitioning the value-space of $C$ (resp. $(C, C')$).
**Sub-agent task id:** none

### Step 11
**Location:** sections/03-lemma-1.tex (Step 2, symmetry)
**Content:** $\Pr[\Ccal_0, \Ccal_1'] \H(X \cup X' \mid \Ccal_0, \Ccal_1') = \Pr[\Ccal_1, \Ccal_0'] \H(X \cup X' \mid \Ccal_1, \Ccal_0')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $(C, X)$ and $(C', X')$ are iid; $X \cup X' = X' \cup X$ is symmetric, so swapping gives the equality.
**Sub-agent task id:** none

### Step 12
**Location:** sections/03-lemma-1.tex (Step 3, Claim A symmetrization)
**Content:** $\E_{c \sim q_0}[\hbin(p_c)] = \E_{c, c' \sim q_0}[(\hbin(p_c) + \hbin(p_{c'}))/2]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\E_{c, c' \sim q_0 \otimes q_0}[(\hbin(p_c)+\hbin(p_{c'}))/2] = \E_c \hbin(p_c)/2 + \E_{c'} \hbin(p_{c'})/2 = \E_c \hbin(p_c)$ since $c, c'$ are iid.
**Sub-agent task id:** none

### Step 13
**Location:** sections/03-lemma-1.tex (Step 3, Claim A)
**Content:** $\E_{c, c' \sim q_0}[(\hbin(p_c)+\hbin(p_{c'}))/2] \le \E_{c, c' \sim q_0}[\hbin(p_c + p_{c'} - p_c p_{c'})] / 1.4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Pointwise \Cref{lem:hbin-low} on $\Ccal_0 \times \Ccal_0$ where $p_c, p_{c'} \le 0.1$ gives $\hbin(p_c + p_{c'} - p_c p_{c'}) \ge 1.4 \cdot (\hbin(p_c) + \hbin(p_{c'}))/2$; rearrange and integrate.
**Sub-agent task id:** none

### Step 14
**Location:** sections/03-lemma-1.tex (Step 3, Claim A multiplication)
**Content:** $\Pr[\Ccal_0]/1.4 \le \Pr[\Ccal_0]^2 / 1.26$, equivalently $1/1.4 \le \Pr[\Ccal_0]/1.26$, i.e. $\Pr[\Ccal_0] \ge 1.26/1.4 = 0.9$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct arithmetic: $1.26/1.4 = 0.9$, and Step 9 gives $\Pr[\Ccal_0] \ge 0.9$.
**Sub-agent task id:** none

### Step 15
**Location:** sections/03-lemma-1.tex (Step 4, Claim B / application of Lemma 3)
**Content:** $2 \sum_{c \in \Ccal_0, c' \in \Ccal_1} q(c) q(c') \hbin(p_c + p_{c'} - p_c p_{c'}) \ge 2 \sum_{c \in \Ccal_0, c' \in \Ccal_1} q(c) q(c') (1 - p_c) \hbin(p_{c'})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Pointwise application of \Cref{lem:hbin-mixed} with $(p, p') = (p_c, p_{c'})$ for $c \in \Ccal_0$, $c' \in \Ccal_1$ -- gives summand $(1 - p_c) \hbin(p_{c'})$. Note: $\Cref{lem:hbin-mixed}$ holds for any $p, p' \in [0,1]$, so the choice $(p, p') = (p_c, p_{c'})$ with $p_c$ small (in $\Ccal_0$) and $p_{c'}$ possibly large (in $\Ccal_1$) is valid.
**Sub-agent task id:** none

### Step 16
**Location:** sections/03-lemma-1.tex (Step 4, Claim B factorization)
**Content:** $\sum_{c \in \Ccal_0, c' \in \Ccal_1} q(c) q(c') (1 - p_c) \hbin(p_{c'}) = \left(\sum_{c' \in \Ccal_1} q(c') \hbin(p_{c'})\right)\left(\sum_{c \in \Ccal_0} q(c) (1 - p_c)\right)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial: the summand factorizes since the index sets are independent and the factor on $c$ vs. $c'$ are independent.
**Sub-agent task id:** none

### Step 17
**Location:** sections/03-lemma-1.tex (Step 4, Claim B closing arithmetic)
**Content:** $\sum_{c \in \Ccal_0} q(c) (1 - p_c) \ge 0.9 \Pr[\Ccal_0] \ge 0.9 \cdot 0.9 = 0.81$, hence factor $2 \cdot 0.81 = 1.62$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $p_c \le 0.1$ on $\Ccal_0$ gives $1 - p_c \ge 0.9$; sum $\sum_c q(c) = \Pr[\Ccal_0] \ge 0.9$ from Step 9.
**Sub-agent task id:** none

### Step 18
**Location:** sections/03-lemma-1.tex (Step 5, assembly)
**Content:** $1.62 \Pr[\Ccal_1] \H(X \mid \Ccal_1) \ge 1.26 \Pr[\Ccal_1] \H(X \mid \Ccal_1)$ since $1.62 \ge 1.26$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: $1.62 \ge 1.26$ and $\Pr[\Ccal_1] \H(X \mid \Ccal_1) \ge 0$.
**Sub-agent task id:** none

### Step 19
**Location:** sections/03-lemma-1.tex (Step 5)
**Content:** Final assembly: $\H(X \cup X' \mid C, C') \ge 1.26 \H(X \mid C)$ using the decomposition + bounds + dropping non-negative both-large block.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Straightforward addition of Steps 13-18 results, plus non-negativity of $\Pr[\Ccal_1]^2 \H(X \cup X' \mid \Ccal_1, \Ccal_1') \ge 0$ which is true since entropy is non-negative.
**Sub-agent task id:** none

---

## Theorem 1 / `thm:entropy-gap`, sections/04-theorem-entropy.tex

### Step 20
**Location:** sections/04-theorem-entropy.tex (Step 1)
**Content:** $(A \cup B)_{<i} = \phi(A_{<i}, B_{<i})$ where $\phi$ is the coordinatewise-maximum function.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: $(A \cup B)_j = \max(A_j, B_j)$, and $(A \cup B)_{<i}$ is the tuple of these for $j < i$. So $(A \cup B)_{<i}$ is the coordinatewise-max of $(A_{<i}, B_{<i})$, a deterministic function.
**Sub-agent task id:** none

### Step 21
**Location:** sections/04-theorem-entropy.tex (Step 2, data-processing)
**Content:** $\H((A \cup B)_i \mid (A \cup B)_{<i}) \ge \H((A \cup B)_i \mid A_{<i}, B_{<i})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of \Cref{fac:data-processing} (data-processing for entropy) with $X = (A\cup B)_i$, $Y = (A_{<i}, B_{<i})$, $f = \phi$ from Step 20.
**Sub-agent task id:** none

### Step 22
**Location:** sections/04-theorem-entropy.tex (Step 2, verifying Lemma 1 hypotheses)
**Content:** Hypotheses of \Cref{lem:gap} hold with $C = A_{<i}$, $C' = B_{<i}$, $X = A_i$, $X' = B_i$, $p_a = \Pr[A_i = 1 \mid A_{<i} = a]$, and $\E[X] = \Pr[i \in A] \le 0.01$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Each hypothesis enumerated in the .tex; check verifications: (1) finite state space; (2) Bernoulli conditional; (3) $B_{<i} \overset{d}{=} A_{<i}$ since $B \overset{d}{=} A$; (4) $B_i | B_{<i} = a \sim \Bern(p_a)$ same conditional; (5) $B_i$ independent of $(A_{<i}, A_i)$ since $A, B$ independent; (6) $\E[A_i] \le 0.01$ by hypothesis.
**Sub-agent task id:** none

### Step 23
**Location:** sections/04-theorem-entropy.tex (Step 3, chain rule for A)
**Content:** $\H(A) = \sum_{i=1}^n \H(A_i \mid A_{<i})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** \Cref{fac:chain-rule} applied to the indicator vector $(A_1, \dots, A_n)$; $A$ identified with this vector.
**Sub-agent task id:** none

### Step 24
**Location:** sections/04-theorem-entropy.tex (Step 3, chain rule for A∪B)
**Content:** $\H(A \cup B) = \sum_{i=1}^n \H((A \cup B)_i \mid (A \cup B)_{<i})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Same chain rule on the indicator vector $((A \cup B)_1, \dots, (A \cup B)_n)$.
**Sub-agent task id:** none

### Step 25
**Location:** sections/04-theorem-entropy.tex (Step 3, telescoping)
**Content:** Term-by-term application of Eq. (per-coord) $\H((A\cup B)_i | \cdot) \ge 1.26 \H(A_i | A_{<i})$ summed: $\H(A \cup B) \ge 1.26 \H(A)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Summing both sides of an inequality termwise preserves it; factor $1.26$ pulls out.
**Sub-agent task id:** none

---

## Theorem 2 / `thm:main`, sections/05-main-theorem.tex

### Step 26
**Location:** sections/05-main-theorem.tex (Step 1)
**Content:** Uniform $A$ on $\Fcal$ gives $\H(A) = \log |\Fcal|$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct from definition: uniform on $N$ elements has entropy $\log N$.
**Sub-agent task id:** none

### Step 27
**Location:** sections/05-main-theorem.tex (Step 2)
**Content:** $\H(A \cup B) \le \log |\Fcal|$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Union-closedness $\Rightarrow A \cup B \in \Fcal$ a.s.\ $\Rightarrow A \cup B$ supported on $\Fcal$; apply \Cref{fac:uniform-max}.
**Sub-agent task id:** none

### Step 28
**Location:** sections/05-main-theorem.tex (Step 3)
**Content:** $|\{A \in \Fcal: i \in A\}|/|\Fcal| = \Pr[i \in A]$ for $A$ uniform on $\Fcal$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial: $\Pr[i \in A] = |\{A \in \Fcal: i \in A\}|/|\Fcal|$ by definition of uniform.
**Sub-agent task id:** none

### Step 29
**Location:** sections/05-main-theorem.tex (Step 4)
**Content:** $|\Fcal| \ge 2 \Rightarrow \H(A) \ge \log 2 = 1 > 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct from $\H(A) = \log|\Fcal|$ and $|\Fcal| \ge 2$.
**Sub-agent task id:** none

### Step 30
**Location:** sections/05-main-theorem.tex (Step 5)
**Content:** $1.26 \H(A) \le \H(A \cup B) \le \H(A) \Rightarrow 0.26 \H(A) \le 0 \Rightarrow \H(A) \le 0$, contradicting Step 29.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Subtract $\H(A)$ from both sides: $0.26 \H(A) \le 0$; entropy is non-negative so this forces $\H(A) = 0$; but Step 29 gives $\H(A) \ge 1$.
**Sub-agent task id:** none

---

## Summary

- **Total steps enumerated:** 30
- **🟢 verified:** 29
- **🟡 cross-checked:** 1 (Step 4 — monotonicity of $g(s)$, supported by numerical sweep + analytic sketch in `\Cref{rem:g-monotone}`)
- **🔴 from-memory remaining:** 0
- **Sub-agents fired:** 0 (all steps fast-pathed via textbook inequalities, pointwise application of established lemmas, direct algebra, or Phase A numerical verification)
- **`unable-to-derive` count:** 0
- **`\todo{}` markers introduced:** 0

Phase D handoff: every step ≥ 🟡; the single 🟡 step is the monotonicity claim, which is supported analytically by the sketch in `\Cref{rem:g-monotone}` plus numerical evidence. The reviewer should focus attention here if anywhere.
