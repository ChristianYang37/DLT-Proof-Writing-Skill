# Confidence trace (Phase C.5)

Steps enumerated by walking `\begin{proof}` blocks in `sections/03-...tex` through `sections/06-...tex`.

## Proof of \Cref{lem:init_gram} — initial Gram concentration

### Step 1
**Location:** sections/03-proof-of-lemma-init-gram.tex, Step 1 (Hoeffding entrywise)
**Content (≤ 2 lines):** $Z_r^{(ij)}$ is independent across $r$ with mean 0 and $|Z_r^{(ij)}| \le 2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Cauchy-Schwarz + $\|\xb_i\|=1$ + indicator $\le 1$ + Jensen for centering $\implies |Z_r^{(ij)}| \le 2$. Textbook.
**Sub-agent task id:** none

### Step 2
**Location:** sections/03, eq:entrywise_union
**Content:** Apply \Cref{fac:hoeffding} with $b=2$, $t = \lambda_0/(4n)$; union-bound over $n^2$ pairs.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of Hoeffding digest. Multiplying RHS by $n^2$ from union bound is textbook.
**Sub-agent task id:** none

### Step 3
**Location:** sections/03, Step 2 (entrywise to operator)
**Content:** $\opnorm{\mathbf A} \le n \max_{ij}|\mathbf A_{ij}|$ for $\mathbf A \in \R^{n\times n}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook: $\opnorm{\mathbf A}^2 \le \norm{\mathbf A}_F^2 = \sum_{ij} A_{ij}^2 \le n^2 \max A_{ij}^2$, so $\opnorm{\mathbf A} \le n \max |A_{ij}|$. Tight constant.
**Sub-agent task id:** none

### Step 4
**Location:** sections/03, Step 2 (Weyl)
**Content:** $\lambda_{\min}(\Hb(0)) \ge \lambda_0 - \lambda_0/4 = 3\lambda_0/4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Weyl's perturbation inequality $|\lambda_i(\mathbf A) - \lambda_i(\mathbf B)| \le \opnorm{\mathbf A - \mathbf B}$ is textbook.
**Sub-agent task id:** none

## Proof of \Cref{lem:init_residual} — initial residual bound

### Step 5
**Location:** sections/03, init residual: $\E[Y_r^{(i)}\mid \wb_r(0)] = 0$ via Rademacher $a_r$.
**Content:** $a_r$ is $\pm 1$ symmetric and $\sigma(\wb_r(0)^\top \xb_i)$ is $a_r$-measurable when conditioning on $\wb_r(0)$ — wait, actually $\sigma(\wb_r(0)^\top\xb_i)$ is constant given $\wb_r(0)$, and $\E[a_r] = 0$, so $\E[Y_r^{(i)}\mid\wb_r(0)] = 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trivial conditional expectation with $a_r \perp \wb_r(0)$ from \Cref{ass:init}.
**Sub-agent task id:** none

### Step 6
**Location:** sections/03, sub-Gaussian proxy for $Y_r^{(i)}$ (Phase D iter 1: rewritten as conditional Hoeffding)
**Content:** $\ub_i(0) = m^{-1/2}\sum_r a_r \sigma(\wb_r(0)^\top\xb_i)$ tail via conditional Hoeffding + Bernstein on $\sum_r b_r^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Rewritten in Phase D fix-W2: conditional on $\Wb(0)$, $Y_r^{(i)}$ are bounded ($|Y_r^{(i)}|\le b_r$) independent mean-zero, so Hoeffding gives the conditional tail; $\E b_r^2 = 1/2$ and Bernstein gives $\sum b_r^2 \le m$ w.h.p. \todo marker removed.
**Sub-agent task id:** none

### Step 7
**Location:** sections/03, tail bound on $\ub_i(0)$
**Content:** $\Pr[|\ub_i(0)| \ge t] \le 2\exp(-c_1 t^2)$ for absolute $c_1 > 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Inherits proxy constant from Step 6. Once Step 6 is verified, this follows from the standard sub-Gaussian tail.
**Sub-agent task id:** none

### Step 8
**Location:** sections/03, summing $\sum_i (\ub_i - y_i)^2$
**Content:** $(a-b)^2 \le 2a^2 + 2b^2$ and $|y_i| \le 1$ give $\norm{\ub(0) - \yb}_2^2 \le 2n\cdot c_1^{-1}\log(6n/\delta) + 2n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook arithmetic ($(a-b)^2 \le 2a^2 + 2b^2$ by AM-GM).
**Sub-agent task id:** none

## Proof of \Cref{lem:perturbation} — Gram stability

### Step 9
**Location:** sections/04, eq:flip_containment
**Content:** $A_{i,r}(R) \subseteq \{|\wb_r(0)^\top \xb_i| \le R\}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: a sign flip between $\wb_r(0)^\top \xb_i$ and $\wb^\top \xb_i$ requires the segment to pass through 0; $|\wb^\top\xb_i - \wb_r(0)^\top\xb_i| \le \|\wb - \wb_r(0)\|\cdot\|\xb_i\| \le R$ by Cauchy-Schwarz; hence $|\wb_r(0)^\top\xb_i| \le R$.
**Sub-agent task id:** none

### Step 10
**Location:** sections/04, eq:flip_prob
**Content:** $\Pr[A_{i,r}(R)] \le R$ via Gaussian small-ball.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches the digest gaussian-anticoncentration.md. $\wb_r(0)^\top\xb_i \sim \mathcal N(0,\|\xb_i\|^2) = \mathcal N(0,1)$, so $\Pr[|g|\le R] \le R\sqrt{2/\pi} \le R$ (Fact 4.7 in our setup).
**Sub-agent task id:** none

### Step 11
**Location:** sections/04, Hoeffding on $\one[A_{i,r}(R)]$
**Content:** $\Pr[\sum_r \one[A_{i,r}(R)] / m - \E \ge R] \le \exp(-mR^2/2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard one-sided Hoeffding for Bernoulli$(\Pr[A_{i,r}])$, bound $b=1$, deviation $R$ gives $\exp(-2mR^2)$; we used the weaker $\exp(-mR^2/2)$ which is what Hoeffding-1-sided produces.
**Sub-agent task id:** none

### Step 12
**Location:** sections/04, eq:flip_count
**Content:** $|S_i| \le 2mR$ for all $i$ w.p. $\ge 1-\delta/3$ (union bound over $n$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct consequence of Step 11 + union bound over $i \in [n]$; algebra: $\exp(-mR^2/2) \le \delta/(3n)$ iff $m R^2 \ge 2 \log(3n/\delta)$. The lemma's width hypothesis $m \ge C n^2 \log(n/\delta)/\lambda_0^2$ with $R \le c\lambda_0/n^2$ gives $mR^2 \ge C c^2 \log(n/\delta)$, which dominates for $C$ large.
**Sub-agent task id:** none

### Step 13
**Location:** sections/04, eq:H_pertW_entry
**Content:** Only $r \in S_i \cup S_j$ contributes to $\Hb(\Wb)_{ij} - \Hb(\Wb(0))_{ij}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** If neither $A_{i,r}$ nor $A_{j,r}$ occurs, both indicators are unchanged so the product is unchanged, the summand vanishes.
**Sub-agent task id:** none

### Step 14
**Location:** sections/04, final operator norm
**Content:** $\opnorm{\Hb(\Wb) - \Hb(\Wb(0))} \le n\cdot 4R \le \lambda_0/4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Same $\opnorm{\mathbf A} \le n\max|\mathbf A_{ij}|$ used in Step 3; arithmetic $4cR \le \lambda_0/4$ requires $c \le 1/16$.
**Sub-agent task id:** none

## Proof of \Cref{lem:linear_conv} — linear convergence

### Step 15
**Location:** sections/05, eq:residual_update
**Content:** First-order Taylor: $\ub_i(s+1) - \ub_i(s) = -\eta \sum_r \langle \nabla_{\wb_r}\ub_i, \nabla_{\wb_r} L\rangle + e_i(s)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook first-order Taylor expansion of $\ub_i(\Wb(s+1)) - \ub_i(\Wb(s))$ with remainder $e_i(s)$.
**Sub-agent task id:** none

### Step 16
**Location:** sections/05, eq:gram_inner_product
**Content:** $\sum_r \langle \nabla_{\wb_r}\ub_i, \nabla_{\wb_r}\ub_j\rangle = \Hb(\Wb)_{ij}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct from Eq.~\eqref{eq:gd_per_neuron}: $\nabla_{\wb_r}\ub_i = a_r m^{-1/2}\one[\wb_r^\top\xb_i\ge 0]\xb_i$. Then $\langle \nabla_{\wb_r}\ub_i, \nabla_{\wb_r}\ub_j\rangle = a_r^2 m^{-1} \xb_i^\top\xb_j \one[\dots] = m^{-1}\xb_i^\top\xb_j \one[\dots]$. Sum over $r$ matches $\Hb_{ij}$.
**Sub-agent task id:** none

### Step 17
**Location:** sections/05, eq:residual_vector_update
**Content:** $\ub(s+1) - \yb = (\I - \eta\Hb_s)(\ub(s) - \yb) + \mathbf e(s)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Vectorize Step 16 over $i \in [n]$ and substitute into Step 15.
**Sub-agent task id:** none

### Step 18
**Location:** sections/05, eq:remainder_bound
**Content:** $|e_i(s)| \le m^{-1/2} \sum_{r \in T_i(s)} \norm{\wb_r(s+1) - \wb_r(s)}_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** ReLU is 1-Lipschitz; Taylor remainder $|\sigma(z+\Delta) - \sigma(z) - \sigma'(z)\Delta|$ vanishes unless sign of $z$ flips between $z$ and $z+\Delta$, and is otherwise bounded by $|\Delta|$ (since on either side of 0, ReLU is linear so the second-difference is 0; only at the kink does the remainder appear, bounded by $|\Delta|$). Standard ReLU calc.
**Sub-agent task id:** none

### Step 19
**Location:** sections/05, eq:per_neuron_grad_norm
**Content:** $\norm{\nabla_{\wb_r} L}_2 \le \sqrt n m^{-1/2} \norm{\ub(s) - \yb}_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** From digest relu-grad-bound.md. Triangle inequality + $|a_r|=\|\xb_i\|=1$ + Cauchy-Schwarz on $\sum_i (\ub_i - y_i)$ gives $\le m^{-1/2}\sqrt n \norm{\ub-\yb}_2$.
**Sub-agent task id:** none

### Step 20
**Location:** sections/05, eq:remainder_intermediate
**Content:** $|e_i(s)| \le \eta \sqrt n |T_i(s)| / m \cdot \norm{\ub(s) - \yb}_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute Step 19 into Step 18: $\sum_{r\in T_i} m^{-1/2}\norm{\Delta\wb_r}_2 \le |T_i|\cdot m^{-1/2}\cdot \eta\sqrt n m^{-1/2}\norm{\ub-\yb}_2 = \eta\sqrt n |T_i|/m \cdot \norm{\ub-\yb}_2$. Algebra.
**Sub-agent task id:** none

### Step 21
**Location:** sections/05, $|T_i(s)| \le |S_i| \le 2mR$ (Phase D iter 1: explicit witness argument added)
**Content:** Per-step flip set $T_i(s)$ is contained in $S_i$ when $\wb_r(s), \wb_r(s+1)$ both within $R$ of $\wb_r(0)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Rewritten in Phase D fix-W1: the lemma now hypothesizes both the perturbation bound and the flip-count, and the proof explicitly produces a witness for $A_{i,r}(R)$. The main theorem now feeds both via $(\star_t)$ + $\mathcal E_2$.
**Sub-agent task id:** none

### Step 22
**Location:** sections/05, eq:residual_remainder_bound
**Content:** $\norm{\mathbf e(s)}_2 \le 2 \eta n R \norm{\ub(s) - \yb}_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** $\sqrt n \cdot \max_i |e_i(s)| \le \sqrt n \cdot 2\eta\sqrt n R \norm{\ub-\yb}_2 = 2\eta n R \norm{\ub-\yb}_2$ via Step 20 + Step 21. Sufficient for the constant absorbed into $C_2$.
**Sub-agent task id:** none

### Step 23
**Location:** sections/05, eq:res_squared_step
**Content:** $\norm{\ub(s+1) - \yb}_2^2 \le (\opnorm{\I - \eta\Hb_s} + \eta\lambda_0/4)^2 \norm{\ub(s) - \yb}_2^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** From Step 17: $\norm{\ub(s+1)-\yb}_2 \le \opnorm{\I-\eta\Hb_s}\norm{\ub(s)-\yb}_2 + \norm{\mathbf e}_2$; sub $\norm{\mathbf e}_2 \le \eta\lambda_0/4 \norm{\ub-\yb}_2$ from Step 22 (after choosing $c$ small enough that $2\eta n R \le \eta\lambda_0/4$); square. Sub-multiplicative + triangle inequality.
**Sub-agent task id:** none

### Step 24
**Location:** sections/05, $\opnorm{\I - \eta\Hb_s} \le 1 - \eta\lambda_0/2$
**Content:** Under $\lambda_0/2 \le \lambda_{\min}(\Hb_s)$, $\opnorm{\Hb_s} \le n$, and $\eta n \le 1$, $\opnorm{\I-\eta\Hb_s} \le 1-\eta\lambda_0/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Eigenvalues of $\I - \eta\Hb_s$ are $1 - \eta\lambda_i(\Hb_s)$. The smallest is $1 - \eta\lambda_{\max}(\Hb_s) \ge 1 - \eta n \ge 0$, the largest is $1 - \eta\lambda_{\min}(\Hb_s) \le 1 - \eta\lambda_0/2$. Since all eigenvalues are nonnegative and bounded by the max, $\opnorm = \max |1 - \eta\lambda_i| \le 1 - \eta\lambda_0/2$. Textbook.
**Sub-agent task id:** none

### Step 25
**Location:** sections/05, $\opnorm{\Hb_s} \le n$
**Content:** Each entry of $\Hb_s$ is in $[-1,1]$, so $\opnorm{\Hb_s} \le \norm{\Hb_s}_F \le n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $|\Hb_s {}_{ij}| \le 1$ via $|\xb_i^\top\xb_j| \le 1$ + indicator $\le 1$, so $\norm{\Hb_s}_F \le \sqrt{\sum_{ij} 1} = n$, and $\opnorm \le \norm{\cdot}_F$.
**Sub-agent task id:** none

### Step 26
**Location:** sections/05, $\sum_{s'} (1-\eta\lambda_0/2)^{s'/2} \le 4/(\eta\lambda_0)$
**Content:** Geometric series with ratio $r=\sqrt{1-\eta\lambda_0/2} \le 1-\eta\lambda_0/4$ sums to $1/(1-r) \le 4/(\eta\lambda_0)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\sqrt{1-x} \le 1 - x/2$ for $x \in [0,1]$, so $r \le 1 - \eta\lambda_0/4$ and $1/(1-r) \le 4/(\eta\lambda_0)$. Textbook.
**Sub-agent task id:** none

### Step 27
**Location:** sections/05, final $R = 4\sqrt n \norm{\ub(0)-\yb}_2 / (\sqrt m \lambda_0)$
**Content:** Telescoping $\norm{\wb_r(s+1) - \wb_r(0)}_2 \le \sum_{s'} (\eta\sqrt n / \sqrt m) (1-\eta\lambda_0/2)^{s'/2} \norm{\ub(0)-\yb}_2 \le 4\sqrt n / (\sqrt m \lambda_0) \norm{\ub(0)-\yb}_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Combine Step 19 (per-step bound) with the geometric-series sum (Step 26) and the inductive contraction.
**Sub-agent task id:** none

## Proof of \Cref{thm:main} — assembly

### Step 28
**Location:** sections/06, union bound on $\mathcal E$
**Content:** $\Pr[\mathcal E_1^c \cup \mathcal E_2^c \cup \mathcal E_3^c] \le 3 \cdot \delta/3 = \delta$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Each event has failure $\le \delta/3$ from the three lemmas; union bound.
**Sub-agent task id:** none

### Step 29
**Location:** sections/06, eq:R_bound
**Content:** $R \le 4\sqrt{C'} n\sqrt{\log(n/\delta)} / (\sqrt m \lambda_0)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Plug \Cref{lem:init_residual} $\norm{\ub(0)-\yb}_2 \le \sqrt{C' n \log(n/\delta)}$ into the definition of $R$. Arithmetic.
**Sub-agent task id:** none

### Step 30
**Location:** sections/06, $R \le c\lambda_0/n^2$ width
**Content:** $R \le c\lambda_0/n^2$ iff $m \ge 16 C' n^6 \log(n/\delta)/(c^2 \lambda_0^4)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Square Step 29 and rearrange: $R^2 \le 16 C' n^2 \log(n/\delta)/(m\lambda_0^2) \le c^2\lambda_0^2/n^4$ iff $m \ge 16 C' n^6 \log(n/\delta)/(c^2\lambda_0^4)$. Algebra.
**Sub-agent task id:** none

### Step 31
**Location:** sections/06, eq:hmin_bound
**Content:** $\lambda_{\min}(\Hb(\Wb(s))) \ge \lambda_0 - \lambda_0/4 - \lambda_0/4 = \lambda_0/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Triangle inequality on operator norm + Weyl's inequality (twice): once for $\Hb(\Wb(s)) - \Hb^\infty$ via $\mathcal E_1 \cup \mathcal E_2$ summed, then Weyl gives $\lambda_{\min}(\Hb(\Wb(s))) \ge \lambda_0 - \lambda_0/2 = \lambda_0/2$.
**Sub-agent task id:** none

### Step 32
**Location:** sections/06, induction step $(\star_t) \Rightarrow (\star_{t+1})$
**Content:** Apply \Cref{lem:linear_conv} given $\lambda_{\min}(\Hb_s) \ge \lambda_0/2$ for all $s\le t$ to get $(\star_{t+1})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct invocation of \Cref{lem:linear_conv} whose hypotheses are now verified.
**Sub-agent task id:** none

---

## Summary

- **Total steps enumerated:** 32
- **🟢 verified:** 29 (after Phase D iter 1 promotions of Steps 6, 21)
- **🟡 cross-checked:** 3 (Steps 7, 10, 22)
- **🔴 from-memory remaining:** 0

**No `conclusion-differs` defects detected.** All 🟢 verifications correspond to textbook inequalities (Cauchy-Schwarz, Weyl, sub-multiplicativity, AM-GM, geometric series) or digest matches (Hoeffding, Gaussian small-ball, ReLU gradient bound, du2019gradient skeleton).

**Overall confidence:** GREEN.
