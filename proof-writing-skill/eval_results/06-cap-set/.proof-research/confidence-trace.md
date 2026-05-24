# Confidence trace — cap-set proof

This trace enumerates every derivation step in the proofs of \Cref{lem:slice-rank-diagonal}, \Cref{lem:cap-set-diagonal}, \Cref{lem:T-polynomial}, \Cref{lem:slice-rank-upper-bound}, and \Cref{thm:main}.

## Conventions
- Tag taxonomy: 🔴 from-memory; 🟡 cross-checked against digest or project lemma; 🟢 verified (textbook inequality, independent re-derivation, or trivial algebra).
- All steps start at 🔴.

---

## Steps in \Cref{lem:slice-rank-diagonal} (sections/02-slice-rank-lower-bound.tex)

### Step 1
**Location:** sections/02-slice-rank-lower-bound.tex, "diagonal decomposition" (paragraph after "We prove it by induction").
**Content:** $T(x,y,z) = \sum_{x_0 \in V} f_{x_0}(x) g_{x_0}(y,z)$ where $f_{x_0}(x) = \1[x=x_0]$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Trivial algebra — the sum sifts on the diagonal $x = x_0$, yielding $T(x_0, y, z)$ at that single $x = x_0$, which by definition is $T(x, y, z)$. Hand-checked.

### Step 2
**Location:** sections/02-slice-rank-lower-bound.tex, Eq.~\eqref{eq:slice-rank-decomposition} → multiplication by $\phi(x)$.
**Content:** $\sum_x \phi(x) \sum_j f_j^{(1)}(x) g_j^{(1)}(y,z) = \sum_j (\sum_x \phi(x) f_j^{(1)}(x)) g_j^{(1)}(y,z) = 0$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Linearity of summation; equals zero by definition of $\phi \in W_1^\perp$. Hand-checked.

### Step 3
**Location:** Eq.~\eqref{eq:Ttilde}.
**Content:** $\widetilde T(y,z) = \sum_j \widetilde g_j^{(2)}(z) f_j^{(2)}(y) + \sum_j \widetilde g_j^{(3)}(y) f_j^{(3)}(z)$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Direct substitution of definitions; same linearity argument as Step 2. Hand-checked.

### Step 4
**Location:** Eq.~\eqref{eq:rank-Ttilde}.
**Content:** $\rk(\widetilde T) \le r_2 + r_3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Each term in Eq.~\eqref{eq:Ttilde} is a rank-1 matrix (product of one-variable functions); sum of $r_2 + r_3$ rank-1 matrices has rank $\le r_2 + r_3$. Standard linear algebra.

### Step 5
**Location:** "The matrix $\widetilde T$ is diagonal" paragraph.
**Content:** $\widetilde T(y,z) = \phi(y) T(y,y,y) \1[y=z]$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Direct substitution using hypothesis~\Cref{lem:slice-rank-diagonal:diag}; the sum $\sum_x \phi(x) T(x,y,z)$ has only one surviving term at $x = y$, and only when $y = z$. Hand-checked.

### Step 6
**Location:** Eq.~\eqref{eq:phi-support}.
**Content:** $|\supp(\phi)| \le r_2 + r_3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Combines: rank of diagonal matrix = number of nonzero diagonal entries; nonzero diagonal entries of $\widetilde T$ equal $\supp(\phi)$ (using $T(y,y,y) \ne 0$). Hand-checked.

### Step 7
**Location:** "Choosing $\phi$ to maximize support" paragraph.
**Content:** $|\supp(\phi)| \ge |V| - r_1$ for some $\phi \in W_1^\perp$.
**Initial tag:** 🔴
**Current tag:** 🟡
**Verification method:** Standard linear-algebra fact: a $d$-dimensional subspace of $F^V$ contains a vector with $\ge d$ nonzero coordinates (use reduced row-echelon form basis). Matches digest entry. Cross-checked against Tao's blog post.

### Step 8
**Location:** "Combining" paragraph.
**Content:** $|V| - r_1 \le r_2 + r_3 \Rightarrow |V| \le r_1 + r_2 + r_3 = r$, contradiction with $r < |V|$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Elementary arithmetic. Hand-checked.

---

## Steps in \Cref{lem:cap-set-diagonal} (sections/03-cap-set-diagonal.tex)

### Step 9
**Location:** sections/03-cap-set-diagonal.tex, "Hypothesis (nonzero diagonal)".
**Content:** $T_A(x,x,x) = \1[3x = 0] = 1$ in $\F_3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Trivial: $3x = 0$ in $\F_3$ since $3 \equiv 0 \pmod 3$. Hand-checked.

### Step 10
**Location:** sections/03-cap-set-diagonal.tex, "Hypothesis (off-diagonal vanishing)".
**Content:** $T_A(x,y,z) \ne 0 \Rightarrow x = y = z$ (using cap-set property).
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Direct from \Cref{def:cap-set}. Hand-checked.

---

## Steps in \Cref{lem:T-polynomial} (sections/04-slice-rank-upper-bound.tex)

### Step 11
**Location:** sections/04-slice-rank-upper-bound.tex, Eq.~\eqref{eq:polynomial-identity}.
**Content:** $\1[w=0] = 1 - w^2$ for $w \in \F_3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Enumerate: $w=0 \Rightarrow 1 - 0 = 1$; $w=1 \Rightarrow 1 - 1 = 0$; $w=2 \Rightarrow 1 - 4 = 1 - 1 = 0$ in $\F_3$. Hand-checked.

### Step 12
**Location:** sections/04-slice-rank-upper-bound.tex, $\1[x+y+z = 0] = \prod_i \1[x_i+y_i+z_i = 0]$.
**Content:** Coordinatewise factorization of indicator.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Trivial; indicator of conjunction = product. Hand-checked.

---

## Steps in \Cref{lem:slice-rank-upper-bound} (sections/04-slice-rank-upper-bound.tex)

### Step 13
**Location:** "Step 1: monomial expansion" paragraph.
**Content:** $(x_i + y_i + z_i)^2 = x_i^2 + y_i^2 + z_i^2 + 2 x_i y_i + 2 x_i z_i + 2 y_i z_i$ in $\F_3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Direct expansion of $(a+b+c)^2$; characteristic $3$ does not collapse any cross terms. Hand-checked.

### Step 14
**Location:** Eq.~\eqref{eq:degree-bound}, $c_{\alpha,\beta,\gamma} \ne 0 \Rightarrow |\alpha| + |\beta| + |\gamma| \le 2n$.
**Content:** Each factor contributes degree $0$ or $2$ in total over $(x_i, y_i, z_i)$; over $n$ factors, max combined degree $2n$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Each factor $1 - (x_i + y_i + z_i)^2$ expands to $1 - (\text{degree-2 stuff})$; selecting one summand from each of the $n$ factors gives a monomial of degree $0$ or $2$ per factor. Hand-checked.

### Step 15
**Location:** "Step 2: partition" paragraph.
**Content:** $|\alpha| + |\beta| + |\gamma| \le 2n \Rightarrow \min\{|\alpha|, |\beta|, |\gamma|\} \le 2n/3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Pigeonhole: if all three exceed $2n/3$, sum exceeds $2n$. Hand-checked.

### Step 16
**Location:** "Step 3" paragraph, $T^{(1)}(x,y,z) = \sum_{\alpha: |\alpha| \le 2n/3} x^\alpha (\sum_{\beta,\gamma} c_{\alpha,\beta,\gamma} y^\beta z^\gamma)$.
**Content:** Re-grouping of $T^{(1)}$ as a sum of $M_n$ many 1-slices.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Direct grouping by outer index $\alpha$; the inner sum is a function of $(y, z)$ only. The count of admissible $\alpha$'s is exactly $M_n$ by \Cref{def:Mn}. Hand-checked.

### Step 17
**Location:** Eq.~\eqref{eq:T1-bound} / Eq.~\eqref{eq:T2-T3-bound}.
**Content:** $\sr(T^{(k)}) \le M_n$ for $k = 1, 2, 3$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Each $T^{(k)}$ written explicitly as a sum of $M_n$ slices (in the appropriate orientation $k$) by the same argument as Step 16, permuting variable roles. Hand-checked.

### Step 18
**Location:** "Combining" paragraph in upper-bound proof.
**Content:** $\sr(T_A) \le \sr(T^{(1)}) + \sr(T^{(2)}) + \sr(T^{(3)}) \le 3 M_n$.
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Subadditivity of slice rank under tensor addition (concatenate slice decompositions). Standard / trivial. Hand-checked.

---

## Steps in \Cref{thm:main} (sections/05-main-theorem.tex)

### Step 19
**Location:** sections/05-main-theorem.tex, $|A| = \sr(T_A) \le 3 M_n$.
**Content:** Combining \Cref{lem:cap-set-diagonal} (gives $\sr(T_A) = |A|$) and \Cref{lem:slice-rank-upper-bound} (gives $\sr(T_A) \le 3 M_n$).
**Initial tag:** 🔴
**Current tag:** 🟢
**Verification method:** Trivial composition of two prior lemmas. Hand-checked.

### Step 20
**Location:** sections/05-main-theorem.tex, $|A| \le C (2.7558)^n$ via \Cref{fac:Mn-asymp}.
**Content:** Substituting $M_n \le C' \cdot (2.7558)^n$ from \Cref{fac:Mn-asymp}.
**Initial tag:** 🔴
**Current tag:** 🟡
**Verification method:** \Cref{fac:Mn-asymp} is explicitly cited to \cite{EllenbergGijswijt2017}; the numerical value $2.7558$ matches the citation digest. Not independently re-derived (entropy optimization). Cross-checked against the digest.

---

## Summary

- **Total steps:** 20
- 🟢 verified: **18**
- 🟡 cross-checked: **2** (Steps 7, 20)
- 🔴 from-memory: **0**
- Sub-agents fired: 0 (all steps fell into the fast-path)
- Sub-agent reports: none
- `\todo{verify: ...}` markers in .tex: none

The two yellow steps both involve appeals to standard/cited facts that are matched against digests but not independently re-derived here:
- Step 7: standard linear-algebra fact about generic elements of a subspace (covered by reduced row-echelon-form argument inline).
- Step 20: numerical entropy optimization $3\gamma < 2.7558$, treated as black-box and explicitly cited to \cite{EllenbergGijswijt2017}.

All other 18 steps are 🟢 (named textbook fact or hand-checked elementary arithmetic).

**Outcome: proceed to Phase D.**
