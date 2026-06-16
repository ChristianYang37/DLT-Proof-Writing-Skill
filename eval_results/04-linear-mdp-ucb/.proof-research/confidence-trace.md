# Confidence trace — LSVI-UCB regret (Phase C.5)

Every derivation step starts 🔴 `from-memory` and is upgraded via fast-path
(textbook inequality → 🟢; project-lemma / digest match → 🟡) or kept 🔴 with a
`\todo{verify}` marker. Sweep date: 2026-06-09. v1.2 finalize (2026-06-09): the
last 🔴 step (the $C_\beta$ covering constant, Step 13) was cross-checked against
cite-jin2020provably Theorem 3.1 and upgraded to 🟡; its `\todo{verify}` is
resolved and removed. $C_\beta$ is a universal constant with verified $dH\sqrt\iota$
scaling (no closed-form numeric value in the source — none fabricated). No 🔴 steps
remain.

Summary after sweep: 🟢 31 / 🟡 19 / 🔴 0  (50 steps enumerated).

---

## Step 1
**Location:** sections/01-preliminaries.tex:111
**Content (≤ 2 lines):** $\T_h g(x,a)=r_h+\int g\,d P_h = \langle\phi,\theta_h\rangle + \int g\langle\phi,d\mu_h\rangle$ (definition of backup, substitute Assumption A).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches .proof-research/linear-mdp-value-linearity.md and cite-jin2020provably (Prop 2.3 / Assumption A); pure substitution of the linear-MDP definition.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 2
**Location:** sections/01-preliminaries.tex:111
**Content (≤ 2 lines):** Pull $\phi(x,a)$ out of the $x'$-integral: $\int g\langle\phi,d\mu_h\rangle=\langle\phi,\int g\,d\mu_h\rangle$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Linearity of the inner product in a fixed vector; hand-checked (Fubini / pull-out of constant vector).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 3
**Location:** sections/01-preliminaries.tex:123
**Content (≤ 2 lines):** $\|w\|\le\|\theta_h\|+\|\int g\,d\mu_h\|\le\sqrt d+H\sqrt d\le 2H\sqrt d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Triangle inequality + $0\le g\le H$ + normalization $\|\theta_h\|,\|\mu_h(\mathcal S)\|\le\sqrt d$; hand-checked. Matches JYWJ Lemma B.1 norm $2H\sqrt d$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 4
**Location:** sections/02-concentration.tex:17
**Content (≤ 2 lines):** $|v^\top w_h^k|=|\sum_\tau v^\top(\Lambda_h^k)^{-1}\phi_h^\tau y_h^\tau|$ (expand ridge weight).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct substitution of Eq.(weight-def); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 5
**Location:** sections/02-concentration.tex:17
**Content (≤ 2 lines):** $\le H\sum_\tau|v^\top(\Lambda_h^k)^{-1}\phi_h^\tau|$ using $|y_h^\tau|\le H$ + triangle inequality.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (triangle) + bound $|y|\le H$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 6
**Location:** sections/02-concentration.tex:17
**Content (≤ 2 lines):** Cauchy–Schwarz in $(\Lambda_h^k)^{-1}$ inner product: $\le H(\sum_\tau v^\top(\Lambda_h^k)^{-1}v)^{1/2}(\sum_\tau(\phi_h^\tau)^\top(\Lambda_h^k)^{-1}\phi_h^\tau)^{1/2}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Cauchy–Schwarz in a PD inner product); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 7
**Location:** sections/02-concentration.tex:17
**Content (≤ 2 lines):** $\le H\cdot\|v\|\cdot(dk)^{1/2}=H\sqrt{dk}$ via $v^\top(\Lambda_h^k)^{-1}v\le\|v\|^2$ and trace bound $\le d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Uses $\lambda_{\min}(\Lambda)\ge\lambda=1$ (Rayleigh) and \Cref{lem:trace-bound} (proved in §04, itself 🟢); hypotheses hold here.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 8
**Location:** sections/02-concentration.tex:45
**Content (≤ 2 lines):** Definition of successful event $\mathcal E$: $\|\sum_\tau\phi_h^\tau[V_{h+1}^k-P_hV_{h+1}^k]\|_{(\Lambda_h^k)^{-1}}\le C\,dH\sqrt\iota$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-jin2020provably (Lemma B.3) verbatim in form; the radius $C\,dH\sqrt\iota$ is the digested value.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 9
**Location:** sections/02-concentration.tex:55
**Content (≤ 2 lines):** $\varepsilon_h^\tau(V)=V(x_{h+1}^\tau)-(P_hV)(x_h^\tau,a_h^\tau)$ is a martingale-difference, $|\varepsilon|\le H$, $H$-sub-Gaussian.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Conditional mean zero by definition of $P_h$; bounded by $H$ since $0\le V\le H$; bounded → sub-Gaussian (Hoeffding's lemma). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 10
**Location:** sections/02-concentration.tex:70
**Content (≤ 2 lines):** Self-normalized bound (fixed $V$): $\|\sum_\tau\phi_h^\tau\varepsilon_h^\tau\|_{(\Lambda_h^k)^{-1}}^2\le 2H^2\log(\det(\Lambda_h^k)^{1/2}\det(\lambda I)^{-1/2}/\delta')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches \Cref{lem:self-normalized} = cite-abbasi2011improved (Theorem 1) with $\sigma=H$; hypotheses (predictable $\phi$, sub-Gaussian $\varepsilon$) verified at Step 9.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 11
**Location:** sections/02-concentration.tex:70
**Content (≤ 2 lines):** $\le 2H^2(\tfrac d2\log\tfrac{\lambda+k}{\lambda}+\log\tfrac1{\delta'})$ via $\det(\Lambda_h^k)\le(\lambda+k)^d$, $\det(\lambda I)=\lambda^d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** AM–GM on eigenvalues of $\Lambda_h^k$ (trace $\le\lambda d+k$ ⇒ det $\le(\lambda+k/d)^d\le(\lambda+k)^d$); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 12
**Location:** sections/02-concentration.tex:91
**Content (≤ 2 lines):** Covering number of the value-function class $\mathcal V$: $\log|\mathcal V_\epsilon|\le C_1 d^2\log(1+HdK/(\epsilon\lambda))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-jin2020provably (Lemma D.6); the $d^2$ comes from covering $(w,A)$ with $w\in\R^d$, $A\in\R^{d\times d}$. Cited, not re-derived.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 13
**Location:** sections/02-concentration.tex:110
**Content (≤ 2 lines):** Union bound + discretization: $\|\sum_\tau\phi_h^\tau\varepsilon_h^\tau(V_{h+1}^k)\|_{(\Lambda_h^k)^{-1}}^2\le 2H^2(\tfrac d2\iota+C_2 d^2\iota)\le C^2 d^2H^2\iota$; pick $C_\beta\ge C$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Sub-agent re-derivation of the constant absorption (covering term $\log(1/\delta')\le C_2 d^2\iota$ folding into $C^2$) at .proof-research/sweep-step-13.md (verdict: matches at rate level). Cross-checked against cite-jin2020provably (Theorem 3.1, $\beta=c\,dH\sqrt\iota$): $C_\beta$ is a universal constant with the SAME $dH\sqrt\iota$ scaling, fixed only implicitly by the self-consistency / union-bound balance $c'\sqrt{\log2+\log(c_\beta+1)}\le c_\beta\sqrt{\log2}$ (their Eq. 14) — no closed-form numeric value exists in the source. Honest completion: proof now states $C_\beta$ is a universal constant with verified $dH\sqrt\iota$ scaling (no fabricated number); `\todo{verify: C_beta}` removed from sections/02-concentration.tex. Rate exponents $dH\sqrt\iota$ are exact.
**Sub-agent task id:** sweep-13-cbeta
**Last updated:** 2026-06-09T17:30:00Z

## Step 14
**Location:** sections/03-optimism.tex:28
**Content (≤ 2 lines):** $w_h^k-w_h^\pi=(\Lambda_h^k)^{-1}\sum_\tau\phi_h^\tau[r+V_{h+1}^k]-w_h^\pi$ (expand ridge minus true weight).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitution of Eq.(weight-def); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 15
**Location:** sections/03-optimism.tex:28
**Content (≤ 2 lines):** $=(\Lambda_h^k)^{-1}\{-\lambda w_h^\pi+\sum_\tau\phi_h^\tau[V_{h+1}^k-P_hV_{h+1}^\pi]\}$ using $w_h^\pi=(\Lambda_h^k)^{-1}\Lambda_h^k w_h^\pi$ + normal-eq identity.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-jin2020provably (Lemma B.4 proof, the $q_1$ split). Uses $\langle\phi_h^\tau,w_h^\pi\rangle=r+P_hV_{h+1}^\pi$ (Bellman, fac:value-linear). Re-derived against digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 16
**Location:** sections/03-optimism.tex:28
**Content (≤ 2 lines):** Three-term split $w_h^k-w_h^\pi=q_1+q_2+q_3$ by adding/subtracting $P_hV_{h+1}^k$ inside the sum.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-jin2020provably (Lemma B.4); algebraic add-subtract, re-derived against digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 17
**Location:** sections/03-optimism.tex:43
**Content (≤ 2 lines):** Inner-product with $\phi(x,a)$: $\langle\phi,w_h^k-w_h^\pi\rangle=\langle\phi,q_1\rangle+\langle\phi,q_2\rangle+\langle\phi,q_3\rangle$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Linearity of inner product; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 18
**Location:** sections/03-optimism.tex:49
**Content (≤ 2 lines):** $\langle\phi,q_3\rangle=P_h(V_{h+1}^k-V_{h+1}^\pi)(x,a)-\lambda\langle\phi,(\Lambda_h^k)^{-1}\int(V_{h+1}^k-V_{h+1}^\pi)d\mu_h\rangle$ via $(\Lambda_h^k)^{-1}\sum\phi\phi^\top=I-\lambda(\Lambda_h^k)^{-1}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Sub-agent re-derivation at .proof-research/sweep-step-18.md (verdict: matches). Uses linear-MDP $P_hg=\langle\phi,\int g\,d\mu_h\rangle$ + the resolvent identity $(\Lambda)^{-1}(\Lambda-\lambda I)=I-\lambda\Lambda^{-1}$.
**Sub-agent task id:** sweep-18-q3
**Last updated:** 2026-06-09T05:00:00Z

## Step 19
**Location:** sections/03-optimism.tex:59
**Content (≤ 2 lines):** Define $\Delta_h^k=\langle\phi,q_1\rangle+\langle\phi,q_2\rangle-\lambda\langle\phi,(\Lambda_h^k)^{-1}\int(\cdot)d\mu_h\rangle$ ⇒ recursion identity Eq.(recursion).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Collecting terms from Steps 17–18; hand-checked algebra.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 20
**Location:** sections/03-optimism.tex:69
**Content (≤ 2 lines):** $|\Delta_h^k|\le\|\phi\|_{(\Lambda_h^k)^{-1}}(\lambda\|w_h^\pi\|_{(\Lambda)^{-1}}+\|\sum\phi\varepsilon\|_{(\Lambda)^{-1}}+\lambda\|\int(\cdot)d\mu_h\|_{(\Lambda)^{-1}})$ via Cauchy–Schwarz per term.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Cauchy–Schwarz in $(\Lambda_h^k)^{-1}$) + triangle; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 21
**Location:** sections/03-optimism.tex:69
**Content (≤ 2 lines):** $\le\|\phi\|_{(\Lambda)^{-1}}(\sqrt\lambda\|w_h^\pi\|+C\,dH\sqrt\iota+\sqrt\lambda\|\int(\cdot)d\mu_h\|)$ using $\|u\|_{(\Lambda)^{-1}}\le\|u\|/\sqrt\lambda$ and event $\mathcal E$ on the middle term.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Rayleigh bound $\|u\|_{(\Lambda)^{-1}}\le\|u\|/\sqrt{\lambda_{\min}}$ (🟢) + def of $\mathcal E$ (Step 8, 🟡 via lem:concentration). Hypotheses of $\mathcal E$ hold (conditioning on $\mathcal E$).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 22
**Location:** sections/03-optimism.tex:69
**Content (≤ 2 lines):** $\le\|\phi\|_{(\Lambda)^{-1}}(2H\sqrt d+C\,dH\sqrt\iota+2H\sqrt d)\le\beta\|\phi\|_{(\Lambda)^{-1}}$, $C_\beta\ge C+4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** $\|w_h^\pi\|\le2H\sqrt d$ (fac:value-linear, 🟢) + $\|\int(V^k-V^\pi)d\mu_h\|\le H\sqrt d\le 2H\sqrt d$; constants fold into $\beta=C_\beta dH\sqrt\iota$. Rate-exact; numeric $C_\beta$ tracked at Step 13.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 23
**Location:** sections/03-optimism.tex:105
**Content (≤ 2 lines):** Optimism base case $h=H+1$: $V_{H+1}^k\equiv0\equiv V_{H+1}^\star$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Convention $V_{H+1}\equiv0$; trivial.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 24
**Location:** sections/03-optimism.tex:105
**Content (≤ 2 lines):** Inductive step: $\langle\phi,w_h^k\rangle-Q_h^\star=P_h(V_{h+1}^k-V_{h+1}^\star)+\Delta_h^k\ge0-\beta\|\phi\|_{(\Lambda)^{-1}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** lem:recursion (Step 19–22, 🟡) + inductive hypothesis $V_{h+1}^k\ge V_{h+1}^\star$ ⇒ $P_h(\cdot)\ge0$ ($P_h$ monotone). Matches cite-jin2020provably (Lemma B.5).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 25
**Location:** sections/03-optimism.tex:117
**Content (≤ 2 lines):** $Q_h^\star\le\min\{\langle\phi,w_h^k\rangle+\beta\|\phi\|_{(\Lambda)^{-1}},H\}=Q_h^k$; then $\max_a$ ⇒ $V_h^k\ge V_h^\star$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Rearrange Step 24 + $Q^\star\le H$ + monotonicity of $\max_a$; hand-checked. Closes the induction.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 26
**Location:** sections/04-elliptical.tex:19
**Content (≤ 2 lines):** Trace bound: $\sum_i\phi_i^\top\Lambda_t^{-1}\phi_i=\mathrm{tr}(\Lambda_t^{-1}\sum_i\phi_i\phi_i^\top)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $u^\top Mu=\mathrm{tr}(Muu^\top)$ + trace cyclicity + linearity; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 27
**Location:** sections/04-elliptical.tex:19
**Content (≤ 2 lines):** $=\sum_{j=1}^d\sigma_j/(\sigma_j+\lambda)\le d$ via eigendecomposition.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Each summand $\le1$; hand-checked. Matches digest elliptical-potential.md (D.1) and cite-jin2020provably (Lemma D.1).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 28
**Location:** sections/04-elliptical.tex:52
**Content (≤ 2 lines):** $\phi_j^\top\Lambda_{j-1}^{-1}\phi_j\le\lambda_{\min}(\Lambda_0)^{-1}\|\phi_j\|^2\le1$ (Rayleigh + $\lambda_{\min}\ge1$, $\|\phi\|\le1$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Rayleigh quotient bound; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 29
**Location:** sections/04-elliptical.tex:63
**Content (≤ 2 lines):** $\sum_j\phi_j^\top\Lambda_{j-1}^{-1}\phi_j\le\sum_j 2\log(1+\phi_j^\top\Lambda_{j-1}^{-1}\phi_j)=2\sum_j\log\frac{\det\Lambda_j}{\det\Lambda_{j-1}}=2\log\frac{\det\Lambda_t}{\det\Lambda_0}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $x\le2\log(1+x)$ on $[0,1]$ (Step 28 gives $x\in[0,1]$) + matrix-determinant lemma + telescoping; hand-checked. Matches digest (D.2).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 30
**Location:** sections/04-elliptical.tex:63
**Content (≤ 2 lines):** $2\log\frac{\det\Lambda_t}{\det\Lambda_0}\le 2d\log\frac{\lambda_{\max}(\Lambda_0)+t}{\lambda_{\min}(\Lambda_0)}$ (AM–GM: $\det\Lambda_t\le(\lambda_{\max}(\Lambda_0)+t)^d$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Trace $\le d\lambda_{\max}(\Lambda_0)+t$ ⇒ AM–GM on eigenvalues; $\det\Lambda_0\ge\lambda_{\min}^d$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 31
**Location:** sections/04-elliptical.tex:101
**Content (≤ 2 lines):** Self-normalized bound statement (lem:self-normalized) — external, cited.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Restatement of cite-abbasi2011improved (Theorem 1); cited via the `[\cite]` bracket form (R5 form 2). No re-derivation needed (external).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 32
**Location:** sections/05-main-theorem.tex:30
**Content (≤ 2 lines):** Definitions $\delta_h^k=V_h^k(x_h^k)-V_h^{\pi^k}(x_h^k)$, $\zeta_{h+1}^k=\E[\delta_{h+1}^k|x_h^k,a_h^k]-\delta_{h+1}^k$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definitions (no inference); matches cite-jin2020provably (Lemma B.6). Listed for completeness.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 33
**Location:** sections/05-main-theorem.tex:38
**Content (≤ 2 lines):** $\mathrm{Regret}(K)=\sum_k[V_1^\star-V_1^{\pi^k}]\le\sum_k[V_1^k-V_1^{\pi^k}]=\sum_k\delta_1^k$ via optimism.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** lem:optimism ($V_1^k\ge V_1^\star$, Step 25, 🟢) applied termwise; hypotheses (on $\mathcal E$) hold. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 34
**Location:** sections/05-main-theorem.tex:51
**Content (≤ 2 lines):** $\delta_h^k=Q_h^k(x_h^k,a_h^k)-Q_h^{\pi^k}(x_h^k,a_h^k)$ (greedy/optimal action identities).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $V_h^k=Q_h^k$ at greedy $a_h^k$; $V_h^{\pi^k}=Q_h^{\pi^k}$ at $\pi^k$-action; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 35
**Location:** sections/05-main-theorem.tex:51
**Content (≤ 2 lines):** $\le P_h(V_{h+1}^k-V_{h+1}^{\pi^k})(x_h^k,a_h^k)+2\beta\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}$ via Eq.(Q-def)+lem:recursion.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** $Q_h^k\le\langle\phi,w_h^k\rangle+\beta\|\phi\|_{(\Lambda)^{-1}}$ + recursion identity (Step 19, $|\Delta|\le\beta\|\phi\|$) gives factor $2\beta$. Matches cite-jin2020provably (Lemma B.6).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 36
**Location:** sections/05-main-theorem.tex:51
**Content (≤ 2 lines):** $=\delta_{h+1}^k+\zeta_{h+1}^k+2\beta\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}$ via $P_h(\cdot)=\E[\delta_{h+1}^k|\cdot]=\delta_{h+1}^k+\zeta_{h+1}^k$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of $\zeta$ (Step 32); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 37
**Location:** sections/05-main-theorem.tex:65
**Content (≤ 2 lines):** Unroll $h=1..H$ with $\delta_{H+1}^k=0$: $\delta_1^k\le\sum_h\zeta_{h+1}^k+2\beta\sum_h\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Telescoping the per-step recursion (Step 36); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 38
**Location:** sections/05-main-theorem.tex:72
**Content (≤ 2 lines):** Sum over $k$: $\mathrm{Regret}(K)\le 2\beta\sum_{k,h}\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}(=T_1+T_2)+\sum_{k,h}\zeta_{h+1}^k(=T_3)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Combine Step 33 + Step 37; the three-term naming is bookkeeping. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 39
**Location:** sections/05-main-theorem.tex:90
**Content (≤ 2 lines):** $\{\zeta_{h+1}^k\}$ is a martingale-difference sequence with $|\zeta_{h+1}^k|\le2H$ ($T$ terms).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** $V_{h+1}^k$ measurable before episode-$k$ transition (rem:filtration) ⇒ conditional mean zero; $0\le\delta\le H$ ⇒ $|\zeta|\le2H$. Matches azuma-hoeffding.md digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 40
**Location:** sections/05-main-theorem.tex:90
**Content (≤ 2 lines):** Azuma–Hoeffding: w.p. $1-\delta/2$, $T_3\le 2H\sqrt{2T\log(2/\delta)}\le4H\sqrt{T\iota}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Azuma–Hoeffding, $N=T$, $b=2H$); $\log(2/\delta)\le\iota$, $\sqrt2\le2$; hand-checked vs azuma-hoeffding.md.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 41
**Location:** sections/05-main-theorem.tex:101
**Content (≤ 2 lines):** $\sum_{k,h}\|\phi_h^k\|_{(\Lambda_h^k)^{-1}}=\sum_h\sum_k((\phi_h^k)^\top(\Lambda_h^k)^{-1}\phi_h^k)^{1/2}$ (reorder).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Reordering finite double sum; trivial.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 42
**Location:** sections/05-main-theorem.tex:101
**Content (≤ 2 lines):** $\le\sum_h(K\sum_k(\phi_h^k)^\top(\Lambda_h^k)^{-1}\phi_h^k)^{1/2}$ by Cauchy–Schwarz $\sum_k a_k\le(K\sum_k a_k^2)^{1/2}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Cauchy–Schwarz / power-mean); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 43
**Location:** sections/05-main-theorem.tex:101
**Content (≤ 2 lines):** $\le\sum_h(K\cdot2d\iota)^{1/2}=H\sqrt{2dK\iota}$ via elliptical potential $\sum_k(\phi_h^k)^\top(\Lambda_h^k)^{-1}\phi_h^k\le2d\log(1+K)\le2d\iota$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:elliptical} with $\Lambda_0=I$, $t=K$ (Steps 28–30, 🟢); previous-time structure $\Lambda_h^k$ (episodes $1..k-1$) matches the lemma. $\log(1+K)\le\iota$ since $\iota=\log(2dT/\delta)\ge\log(1+K)$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 44
**Location:** sections/05-main-theorem.tex:115
**Content (≤ 2 lines):** $T_1+T_2=2\beta\sum_{k,h}\|\phi\|_{(\Lambda)^{-1}}\le2\beta H\sqrt{2dK\iota}=2C_\beta dH\sqrt\iota\cdot H\sqrt{2dK\iota}\le4C_\beta d^{3/2}H^2\sqrt K\iota$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute Step 43 + $\beta=C_\beta dH\sqrt\iota$; collect $\sqrt2\le2$; hand-checked. (Numeric $C_\beta$ tracked at Step 13; exponents exact.)
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 45
**Location:** sections/05-main-theorem.tex:130
**Content (≤ 2 lines):** $H^2\sqrt K=\sqrt{H^3\cdot KH}=\sqrt{H^3 T}$ (since $T=KH$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebra: $H^2\sqrt K=\sqrt{H^4 K}=\sqrt{H^3\cdot HK}=\sqrt{H^3 T}$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 46
**Location:** sections/05-main-theorem.tex:130
**Content (≤ 2 lines):** $H\sqrt{T\iota}\le d^{3/2}\sqrt{H^3 T}\iota$ (since $d,H,\iota\ge1$), so $T_3$ is dominated by $T_1+T_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Monotonicity in $d,H,\iota\ge1$: $H\sqrt T\le H^{3/2}\sqrt T\le d^{3/2}H^{3/2}\sqrt T=d^{3/2}\sqrt{H^3T}$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 47
**Location:** sections/05-main-theorem.tex:130
**Content (≤ 2 lines):** $\mathrm{Regret}(K)\le4C_\beta d^{3/2}\sqrt{H^3T}\iota+4d^{3/2}\sqrt{H^3T}\iota\le C d^{3/2}\sqrt{H^3T}\iota$, $C=4C_\beta+4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute Steps 40, 44, 45, 46; collect constants; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 48
**Location:** sections/05-main-theorem.tex:140
**Content (≤ 2 lines):** Union bound: $\Pr[\mathcal E\cap\mathcal E']\ge1-\delta/2-\delta/2=1-\delta$ ($\mathcal E$ from lem:concentration, $\mathcal E'$ Azuma).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\Pr[\mathcal E^c]\le\delta/2$ (lem:concentration), $\Pr[(\mathcal E')^c]\le\delta/2$ (Step 40); union bound; hand-checked. Discharges the $1-\delta$ in the theorem (R17).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 49
**Location:** sections/05-main-theorem.tex:140
**Content (≤ 2 lines):** Conclude $\mathrm{Regret}(K)=\Otil(d^{3/2}\sqrt{H^3 T})$ since $\iota=\log(2dT/\delta)$ is logarithmic.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\iota$ absorbed into $\Otil$; definitional. Matches cite-jin2020provably (Theorem 3.1, rate $\sqrt{d^3H^3T}$).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 50
**Location:** sections/01-preliminaries.tex:63
**Content (≤ 2 lines):** Gram/weight/$Q$ definitions (Eqs. gram-def, weight-def, Q-def, V-def) — algorithm specification.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-jin2020provably (Algorithm 1) verbatim: $\lambda=1$, $w=\Lambda^{-1}\sum\phi[r+\max_aQ_{h+1}]$, $Q=\min\{w^\top\phi+\beta(\phi^\top\Lambda^{-1}\phi)^{1/2},H\}$. Specification, not inference.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z
