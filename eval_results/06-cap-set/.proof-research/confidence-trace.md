# Confidence trace — Ellenberg–Gijswijt cap-set proof (Phase C.5)

Estimated derivation steps in project: 21. Enumerated and tagged below: 20
(coverage ~95%, well above the 50% gate). Every step starts 🔴 from-memory and is
upgraded by fast path (textbook algebra → 🟢; technique/citation digest match → 🟡)
or by independent script re-derivation (→ 🟢). No step remains 🔴.

Sweep outcome: 16 🟢 / 4 🟡 / 0 🔴. One transcription error in a non-load-bearing
constant ($t_\ast$) was caught and fixed; see sweep-step-numerics.md.

---

## Step 1
**Location:** sections/02-slice-rank.tex:8
**Content (≤ 2 lines):** Definition of a slice $T=f(x_i)g(\widehat{x}_i)$ and of slice rank as the minimal number of slices summing to $T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches the definition in .proof-research/slice-rank.md and cite-bccgnsu2017-slicerank.md (Definition 4.1); hypotheses (arbitrary field, finite index sets) identical.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 2
**Location:** sections/02-slice-rank.tex:40
**Content (≤ 2 lines):** Subadditivity $\sr(T+T')\le\sr(T)+\sr(T')$ by concatenating slice decompositions; $\sr(\lambda T)=\sr(T)$ for $\lambda\ne0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Elementary set-of-slices concatenation; hand-checked. A sum of $r+r'$ slices is a slice decomposition of $T+T'$; scaling preserves the slice form.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 3
**Location:** sections/02-slice-rank.tex:48
**Content (≤ 2 lines):** Diagonal upper bound: $D=\sum_{a\in X}c_a\one[x_1=a]\one[x_2=\dots=x_k=a]$ is a sum of $|X|$ slices.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Each summand is a function of $x_1$ times a function of the rest — a slice by definition Eq.(eq:slice); hand-checked count $=|X|$.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 4
**Location:** sections/02-slice-rank.tex:54
**Content (≤ 2 lines):** Diagonal lower bound base case $k=2$: a diagonal matrix with $|X'|$ nonzero entries has matrix rank $|X'|$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook linear algebra: rank of a diagonal matrix = number of nonzero diagonal entries. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 5
**Location:** sections/02-slice-rank.tex:60
**Content (≤ 2 lines):** $\dim U\le|S|$ and $\dim W\ge|X'|-|S|$ for the annihilator $W$ of $\{f_i:i\in S\}$ in $\F^{X'}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Rank–nullity: the annihilator of a span of $\le|S|$ functionals has codimension $\le|S|$, hence dimension $\ge|X'|-|S|$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 6
**Location:** sections/02-slice-rank.tex:62
**Content (≤ 2 lines):** A $w$-dimensional subspace of $\F^{X'}$ contains a vector of support size $\ge w$ (pivot-column argument).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Reduced row echelon form has $w$ pivot columns; a generic combination (sum of basis rows) is nonzero in each pivot column, so support $\ge w$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 7
**Location:** sections/02-slice-rank.tex:67
**Content (≤ 2 lines):** Contraction $\widetilde{D}(\cdot)=\sum_{x_k}v(x_k)D'(\cdot,x_k)=\sum_{a}c_a v(a)\one[x_1=\dots=x_{k-1}=a]$; a diagonal $(k-1)$-tensor on $\supp v$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches the Croot–Lev–Pach/Tao contraction in slice-rank.md and cite-tao2016slicerank-blog.md; the $S$-slices vanish (their $f_i$ killed by $v\in W$), $|S^c|$ slices survive, giving the inductive step $\sr(\widetilde{D})\le r-|S|$.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 8
**Location:** sections/02-slice-rank.tex:76
**Content (≤ 2 lines):** Combine $|X'|-|S|\le\sr(\widetilde{D})\le r-|S|$ to get $r\ge|X'|$, hence $\sr(D)=|X|$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Inductive hypothesis on the $(k-1)$-tensor gives $\sr(\widetilde D)\ge|\supp v|\ge|X'|-|S|$; chaining with $\le r-|S|$ cancels $|S|$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 9
**Location:** sections/02-slice-rank.tex:83
**Content (≤ 2 lines):** Restriction monotonicity: restricting each slice to $\prod A_j$ yields a slice, so $\sr(T|_{\prod A_j})\le\sr(T)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** A restricted product $f|_{A_i}\cdot g|_{\prod_{j\ne i}A_j}$ is still of the slice form; the slice count cannot increase. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 10
**Location:** sections/03-upper-bound.tex:24
**Content (≤ 2 lines):** $\F_3$ identity $1-u^2=\one[u=0]$ for $u\in\F_3$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script re-derivation (sweep-step-numerics.md (i)): checked all $u\in\{0,1,2\}$; verdict matches.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 11
**Location:** sections/03-upper-bound.tex:28
**Content (≤ 2 lines):** $\prod_i(1-(x_i+y_i+z_i)^2)=\prod_i\one[x_i+y_i+z_i=0]=\one[x+y+z=0]=T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Step (a) is Step 10 per coordinate; (b) product of indicators = indicator of intersection; (c) is the definition of $T$. Hand-checked; consistent with clp-polynomial-method.md.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 12
**Location:** sections/03-upper-bound.tex:46
**Content (≤ 2 lines):** Every reduced monomial of $T$ has total degree $\le 2n$, so $\min(\deeg x^a,\deeg y^b,\deeg z^c)\le 2n/3$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Three nonnegative integers summing to $\le 2n$ have minimum $\le 2n/3$ (pigeonhole). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 13
**Location:** sections/03-upper-bound.tex:50
**Content (≤ 2 lines):** Group monomials by the block of degree $\le 2n/3$: $T=T_1+T_2+T_3$ with each $T_i$ a sum over monomials $x^a$ (resp. $y^b,z^c$) of degree $\le 2n/3$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches the slice-rank form of the Croot–Lev–Pach decomposition in clp-polynomial-method.md (threshold $d/3=2n/3$, factor 3); each $x^a p_a(y,z)$ is a coordinate-1 slice.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 14
**Location:** sections/03-upper-bound.tex:60
**Content (≤ 2 lines):** $\#\{x^a:\deeg(x^a)\le 2n/3\}=M_n=\dim V_{\le 2n/3}$, so $\sr(T_i)\le M_n$ each.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** By Def. (def:monomial-space), $M_n$ is exactly that monomial count; each $T_i$ is a sum of $\le M_n$ slices. Hand-checked against the definition.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 15
**Location:** sections/03-upper-bound.tex:63
**Content (≤ 2 lines):** $\sr(T)\le\sr(T_1)+\sr(T_2)+\sr(T_3)\le 3M_n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Subadditivity (Step 2 / Lemma part (a)) applied to $T=T_1+T_2+T_3$, then Step 14. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 16
**Location:** sections/04-lower-bound.tex:24
**Content (≤ 2 lines):** For $x,y,z\in A$: $x+y+z=0\iff x=y=z$ (⇐ since $3=0$; ⇒ is the cap-set hypothesis).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** ⇐: $3a=0$ in $\F_3^n$. ⇒: exactly Assumption (ass:capset). Hand-checked; the hypothesis is used at exactly this point.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 17
**Location:** sections/04-lower-bound.tex:31
**Content (≤ 2 lines):** $T|_{A^3}=\one[x+y+z=0]=\one[x=y=z]=\sum_{a\in A}\one[x=y=z=a]$, a diagonal tensor with $c_a=1\ne0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** (a) definition of $T$; (b) Step 16; (c) expand diagonal indicator. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 18
**Location:** sections/04-lower-bound.tex:43
**Content (≤ 2 lines):** $\sr(T|_{A^3})=|A|$ by the diagonal lower bound with $X=A$, $k=3$, $c_a=1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of Lemma part (b) (Steps 3–8), whose hypotheses (nonzero diagonal entries) are met. Hand-checked at cite-site.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 19
**Location:** sections/05-monomial-count.tex:36
**Content (≤ 2 lines):** Chernoff/Cramér bound $M_n\le\sum_{s\le2n/3}[u^s](1+u+u^2)^n t^{s-2n/3}\le t^{-2n/3}(1+t+t^2)^n$ for $t\in(0,1]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script re-derivation (sweep-step-numerics.md (ii)): $M_n$ matches the coefficient-sum encoding for $n\le60$; the shift $t^{s-2n/3}\ge1$ for $s\le2n/3$, $t\le1$ is elementary. Verdict matches.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z

## Step 20
**Location:** sections/05-monomial-count.tex:65
**Content (≤ 2 lines):** $3\gamma=\min_{0<t\le1}(1+t+t^2)t^{-2/3}\approx 2.7551<2.7558$ at $t_\ast\approx0.5931$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script re-derivation (sweep-step-numerics.md (iii)): grid + Brent root of the FOC give minimizer $0.5931$ and value $2.75510<2.7558$. CAUGHT AND FIXED a wrong minimizer ($0.5085\to0.5931$); the value $3\gamma$ and the inequality are correct. Verdict matches.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T21:02:00Z
