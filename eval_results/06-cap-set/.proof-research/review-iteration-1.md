# Review iteration 1

## Reviewer output

### Summary
The paper proves the Ellenberg-Gijswijt cap-set upper bound $|A| \le 3 M_n$ for cap sets $A \subseteq \F_3^n$, where $M_n$ counts the monomials $\prod x_i^{a_i}$ ($a_i \in \{0,1,2\}$) with $\sum a_i \le 2n/3$. The proof uses the symmetric slice-rank reformulation of Croot--Lev--Pach / Ellenberg--Gijswijt due to Tao. The skeleton is: (a) a slice-rank lower bound for diagonal tensors (\Cref{lem:slice-rank-diagonal}), (b) showing the cap-set property forces $T_A$ to be diagonal (\Cref{lem:cap-set-diagonal}), (c) an upper bound on $\sr(T_A)$ via the polynomial $\prod_i (1 - (x_i + y_i + z_i)^2)$ partitioned by lowest-degree variable group (\Cref{lem:slice-rank-upper-bound}), and (d) composition to obtain $|A| \le 3 M_n$. The exposition is clear and the polynomial method step is correctly carried out.

### Strengths
- The polynomial identity $\1[w=0] = 1 - w^2$ for $w \in \F_3$ is used precisely; the expansion and degree bookkeeping are tight.
- The slice-rank lower bound proof is clean: pulling out $\phi \in W_1^\perp$, reducing to a diagonal matrix, applying the rank-of-diagonal formula.
- The three-way symmetric partition by lowest-degree variable group is exactly the move that yields the $3 M_n$ count (factor of 3), rather than a one-sided argument.
- Cap-set hypothesis is invoked only where needed (\Cref{lem:cap-set-diagonal}); the upper bound \Cref{lem:slice-rank-upper-bound} holds for all $A$.
- Citations to Tao, Croot-Lev-Pach, Ellenberg-Gijswijt are correctly attributed and resolve in refs.bib.

### Weaknesses

#### Weakness #1 (severity: minor)
**Claim:** In the proof of \Cref{lem:slice-rank-diagonal}, the induction-on-$|V|$ framing is invoked but the proof does not actually use the inductive hypothesis — the contradiction comes directly from the size-counting argument. This makes the "by induction on $|V|$" framing misleading.
**Evidence:** sections/02-slice-rank-lower-bound.tex:18 "We prove it by induction on $|V|$. The base case $|V| = 0$ is trivial..." but no inductive step is invoked downstream.
**Severity:** minor (style/exposition; correctness unaffected).

#### Weakness #2 (severity: minor)
**Claim:** The "Eliminating the $1$-slices" paragraph starts with a vague sentence ("Choose any subset $U \subseteq V$ that is killed by all $f_j^{(1)}$...") that is then immediately bypassed by the cleaner annihilator argument. This sentence is a noisy false start and should be removed.
**Evidence:** sections/02-slice-rank-lower-bound.tex:26 "Choose any subset $U \subseteq V$ that is \emph{killed by all $f_j^{(1)}$}, i.e.\ such that for some functions $h_j$, the linear combination $h = \sum_j h_j f_j^{(1)}$ (with $h_j$ depending on $x$) vanishes outside $U$. More directly: ..."
**Severity:** minor (clarity; not blocking).

#### Weakness #3 (severity: minor)
**Claim:** In Step 13 of the upper-bound proof (the expansion $(x_i + y_i + z_i)^2 = x_i^2 + y_i^2 + z_i^2 + 2 x_i y_i + 2 x_i z_i + 2 y_i z_i$), the proof asserts this is "in $\F_3$" but writes "$2 x_i y_i$" which would equal "$-x_i y_i$" in $\F_3$. While this is not an error (the coefficient $2$ is a valid representative of the field element), the statement "in $\F_3$" is decorative and could mislead readers — the expansion is the same over any commutative ring, and characteristic-3 plays no role until later.
**Evidence:** sections/04-slice-rank-upper-bound.tex, "Step 1: monomial expansion" paragraph: "using $(x_i + y_i + z_i)^2 = x_i^2 + y_i^2 + z_i^2 + 2 x_i y_i + 2 x_i z_i + 2 y_i z_i$ in $\F_3$".
**Severity:** minor / style.

#### Weakness #4 (severity: style)
**Claim:** Eq.~\eqref{eq:degree-bound} states $|\alpha| + |\beta| + |\gamma| \le 2n$ but the strict claim from $n$ factors each contributing $0$ or $2$ is $|\alpha| + |\beta| + |\gamma| \in \{0, 2, 4, \ldots, 2n\}$, i.e., the value is even. This stronger fact is not used downstream so the bound $\le 2n$ is correct as stated, but worth noting.
**Evidence:** sections/04-slice-rank-upper-bound.tex Eq.~\eqref{eq:degree-bound}.
**Severity:** style (no impact on correctness or downstream).

### Questions for the author
- Did you intend the induction framing in \Cref{lem:slice-rank-diagonal} to handle a degenerate case (e.g., $|V| = 0$ or $|V| = 1$), or could the entire induction structure be removed in favor of a direct contradiction?
- The bound $|A| \le 3 M_n$ in Eq.~\eqref{eq:main-bound} is stated as a finite-$n$ inequality. Is it intended that the absolute constant $C$ in Eq.~\eqref{eq:main-asymp} absorb the case $n = 0$ trivially?

### Verdict
**accept-with-minor-revisions**

The proof is correct and the exposition is clean apart from the noted minor issues. Fixing Weaknesses #1 and #2 would substantially tighten the exposition of the slice-rank lower bound; #3 and #4 are cosmetic.

---

## Author verification

### Weakness #1 (severity: minor)
**Claim:** Induction-on-$|V|$ framing is misleading.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The reviewer is correct that the induction is not used. The contradiction in "Combining" uses only the inequality $|V| - r_1 \le r_2 + r_3$ and arithmetic, with no recourse to a smaller-$|V|$ inductive hypothesis. Cost ≤ 5 lines (remove "by induction" / base case). Will fix.

### Weakness #2 (severity: minor)
**Claim:** Noisy false-start sentence about "$U \subseteq V$ killed by ...".
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Reviewer correct; this is residue from an earlier draft. Cost ≤ 3 lines (delete the parenthetical false-start sentence). Will fix.

### Weakness #3 (severity: minor)
**Claim:** "in $\F_3$" attached to $(x_i + y_i + z_i)^2$ expansion is decorative.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Reviewer correct that the expansion holds over any commutative ring. Cost = 1 token; will remove "in $\F_3$" from that displayed line for cleanliness. Will fix.

### Weakness #4 (severity: style)
**Claim:** Stronger evenness fact is true but unused.
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** The author chose to state the weaker bound $\le 2n$ because that is all the downstream argument uses; stating the stronger evenness fact would be noise. Will not fix.

---

## Fixes applied

### Fix for Weakness #1: remove induction framing.

### Fix for Weakness #2: remove the false-start sentence.

### Fix for Weakness #3: drop "in $\F_3$" from the displayed expansion.

(Fixes implemented in next commit; see post-fix compile check below.)
