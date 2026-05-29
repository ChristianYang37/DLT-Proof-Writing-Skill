# Confidence trace — Stage-2 proof bodies (clean-slate rewrite)

Phase C.5 sweep over the proof bodies written in Stage 2 (sections 03--15,
plus the A1 net-drift derivation in 02). The Step-0 framing correction
(two-constant A1 on the correct direction; `lem:riem_gradient` demoted to a
motivation remark) is reflected throughout.

**Verification environment note.** No general-purpose agent-spawn tool was
available in this run, so independent re-derivation was performed by (a)
named-textbook-inequality hand-checks and (b) **numeric/symbolic script
validation** in `.proof-research/sweep-numeric-checks.py` (8 load-bearing
chains, all PASS). Script validation and named textbook facts are the two
sanctioned 🟢 paths used here. Steps cross-checked only against a project
lemma or citation digest are 🟡. No step remained 🔴.

Script-validated chains (→ 🟢): (1) net-drift identity
`E[s_k|F]=δE[|s_k|]`; (2) Azuma/Bernstein constant; (3) quad-variation
bounds; (4) retraction exponent `1/d` raw, `d^{-3/2}` angular;
(5) orthogonality variance `1/d`; (6) Paley--Zygmund lower bound
[RETIRED 2026-05-29: `lem:incorrect_max_lower` no longer uses Paley--Zygmund;
the failure branch is now Sudakov minoration + Borell--TIS, see the
Stage-2 revision note above the Step 12.xx block];
(7) margin-drift-sharing positivity under `μ0<ρ0/R_U`; (8) loss-to-margin.

---

## Step 02.01
**Location:** sections/02-assumptions.tex:74
**Content (≤ 2 lines):** Net-drift identity $\E[\proj_k\mid\Fcal_{k-1}]=\E[\descent_k\mid\Fcal_{k-1}]\E[\abs{\proj_k}\mid\Fcal_{k-1}]=\snet\E[\abs{\proj_k}\mid\Fcal_{k-1}]$ via conditional independence of sign and magnitude.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (sweep-numeric-checks.py CHECK 1, PASS across p∈{0.5,0.62,0.8,0.95}); the factorisation is the definition of conditional independence applied to $\proj_k=\descent_k\abs{\proj_k}$, $\E[\descent_k\mid\Fcal_{k-1}]=p-(1-p)=2p-1$.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 02.02
**Location:** sections/02-assumptions.tex:84
**Content (≤ 2 lines):** Drift floor $\E[\proj_k\mid\Fcal_{k-1}]\ge\snet\driftc\rho_0$ (for $\snet\ge0$) from the identity + magnitude floor $\E[\abs{\proj_k}\mid\Fcal_{k-1}]\ge\driftc\rho_0$; two-sided $\abs{\cdot}\le\abs{\snet}M$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: multiply identity by floor; $\abs{\proj_k}\le\norm{V_k}\le M$ gives the upper side. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 02.03
**Location:** sections/02-assumptions.tex:104
**Content (≤ 2 lines):** Clause (d) consistency: projecting $\E[V_k\mid\Fcal_{k-1}]=\beta_k\rowhat$ onto $\rowhat$ gives $\beta_k=\E[\proj_k\mid\Fcal_{k-1}]$; incorrect-row bound $\abs{\inner{W_U^a}{\E[V_k\mid\Fcal_{k-1}]}}\le M\incoh_0 R_U$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\norm{\rowhat}=1$; $\abs{\inner{W_U^a}{\rowhat}}=\abs{\inner{W_U^a}{W_U^{\corr}}}/\norm{W_U^{\corr}}\le\incoh_0 R_U$ by Cauchy--Schwarz + incoherence def.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 02.04
**Location:** sections/02-assumptions.tex:185 (eq:noise_gaussian, added 2026-05-29)
**Content (≤ 2 lines):** Isotropic-Gaussian specialisation $\xi_t\mid\Fcal_{t-1}\sim\mathcal N(0,\tau_t^2 I_d)$, $\sigma_{\min}^2/d\le\tau_t^2\le\sigma_{\max}^2/d$; a scalar-covariance Gaussian refinement of eq:noise_isotropy, used ONLY by lem:incorrect_max_lower (rem:gaussian_noise_scope).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Consistency hand-check, not a derivation: (a) scalar $\tau_t^2 I_d$ satisfies the comparable-to-isotropic bounds of eq:noise_isotropy (a scalar in $[\sigma_{\min}^2/d,\sigma_{\max}^2/d]$ times $I$ lies between the two PSD bounds), so it is a special case, not a contradiction; (b) the success branch (lem:incorrect_max, lem:signal_floor, lem:azuma) and R2 (thm:hallheyde_be) invoke eq:noise_isotropy ONLY via the conditional-variance UPPER bound $\inner{W_U^a}{\Cov(\xi_t)W_U^a}\le\sigma_{\max}^2\norm{W_U^a}^2/d$ and the a.s. increment bound $\norm{\xi_t}\le2M$ — verified by grep (eq:noise_isotropy cited at 08:86/122/131, 09:91, 14:103, all second-moment), never the Gaussian law; R2 DERIVES normality via martingale CLT (would be circular if assumed). Scope confirmed in rem:gaussian_noise_scope.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 03.01
**Location:** sections/03-lemma-running-average.tex:43
**Content (≤ 2 lines):** Softmax-average representation $\tilde x_T=\sum_{k=0}^T w_{T,k}V_k$, $w_{T,k}=e^{s_{T,k}}/\sum_j e^{s_{T,j}}$, $\sum_k w_{T,k}=1$ (single attention head over values + residual).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches the attention-head computation of cite-vaswani2017attention.md (softmax-weighted value average); numerators sum to denominator ⇒ $\sum w=1$ (trivial). Architectural identity.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 03.02
**Location:** sections/03-lemma-running-average.tex:48
**Content (≤ 2 lines):** On-sphere iterate $x_T=\sqrt d\,\tilde x_T/\norm{\tilde x_T}$ is the exact positive rescaling of the convex combination (direction preserved).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\tilde x_T$ is a nonneg combination with $\sum w=1$; normalisation scales by the positive scalar $\sqrt d/\norm{\tilde x_T}$, preserving direction. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 03.03
**Location:** sections/03-lemma-running-average.tex:62
**Content (≤ 2 lines):** $w_{T,0}\le\max_{0\le k\le T}w_{T,k}\le e^{2S}/T=O(1/T)$ (one weight $\le$ max weight; max bound from lem:quad_variation, non-circular).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Cross-check against lem:quad_variation eq:max_weight (whose max bound uses only bounded scores, not $\sum w=1$); $w_{T,0}$ is one of the $T+1$ weights. Hypotheses met.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 05.01
**Location:** sections/05-lemma-orthogonality.tex:25
**Content (≤ 2 lines):** $\E[uu^\top]=(1/d)I$ by rotational invariance; $\E\inner{e}{u}^2=1/d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 5, PASS for d∈{10,50,200}); trace argument $\lambda d=\E\norm u^2=1$. Standard.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 05.02
**Location:** sections/05-lemma-orthogonality.tex:33
**Content (≤ 2 lines):** Sub-Gaussian tail $\Pr[\abs{\inner e u}>t/\sqrt d]\le2e^{-ct^2}$ (Vershynin Thm 3.4.6, 1-Lipschitz $u\mapsto\inner e u$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-vershynin2018.md Thm 3.4.6 (Lipschitz concentration on the sphere, proxy $O(1/d)$); substitution $r=t/\sqrt d$.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 05.03
**Location:** sections/05-lemma-orthogonality.tex:44
**Content (≤ 2 lines):** Small-ball lower bound $\Pr[\inner e u>t/\sqrt d]\ge c''e^{-C''t^2}$ from the beta density $f(r)=c_d(1-r^2)^{(d-3)/2}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-vershynin2018.md §3.4 projection density + anti-concentration-max.md (spreading estimate); $(1-t^2/d)^{(d-3)/2}\ge e^{-C''t^2}$ for large $d$. Hand-checked the density-integral bound.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 06.01
**Location:** sections/06-lemma-quadratic-variation.tex:46
**Content (≤ 2 lines):** $\sum_j e^{s_j}\ge e^{s_{t^\star}}(1+(T-1)e^{-2S})$ via $e^{s_j}\ge e^{s_{t^\star}}e^{-2S}$ termwise; hence $\max_t w_{T,t}\le1/(1+(T-1)e^{-2S})\le e^{2S}/T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 3, PASS for S∈{0.5,1,2}, 2000 trials each, both inequalities); $\abs{s_j-s_{t^\star}}\le2S$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 06.02
**Location:** sections/06-lemma-quadratic-variation.tex:71
**Content (≤ 2 lines):** $S_T=\sum_t w_{T,t}^2\le(\max_t w_{T,t})\sum_t w_{T,t}\le e^{2S}/T$ using $\sum_t w_{T,t}=1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 3 includes $S_T$ bound, PASS); $\sum w_t^2\le\max w_t\cdot\sum w_t$ is elementary (Hölder).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 07.01
**Location:** sections/07-lemma-retraction-stability.tex:50
**Content (≤ 2 lines):** Both on-sphere maps are second-order retractions with Taylor $\bar R_u(s)=u+s-\tfrac12\norm s^2 u+r(s)$, $\norm{r(s)}\le C_{\mathrm{ret}}\eta^3$ (Boumal Prop 5.44).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-boumal2023.md (Prop 5.44 second-order retraction, Ex 3.49; eq 5.30 cubic residual) and retraction-stability.md. Hypotheses (η below injectivity radius) met for large $d$.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 07.02
**Location:** sections/07-lemma-retraction-stability.tex:73
**Content (≤ 2 lines):** Difference of the two retractions' expansions: linear+quadratic cancel, residual $\le2C_{\mathrm{ret}}\eta^3$; project onto row, restore radius ⇒ $\abs{\inner{W_U^a}{x_t}-\inner{W_U^a}{\bar x_t}}\le C_{\mathrm{ret}}R_U\eta^3\sqrt d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: Cauchy--Schwarz $\abs{\inner{W_U^a}{\cdot}}\le\norm{W_U^a}\norm{\cdot}\le R_U\cdot\sqrt d\cdot2C_{\mathrm{ret}}\eta^3$. Elementary given Step 07.01.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 07.03
**Location:** sections/07-lemma-retraction-stability.tex:90
**Content (≤ 2 lines):** With $\eta=O(1/\sqrt d)$: $\eta^3\sqrt d=O(1/d)$ raw logit, $O(1/d^{1.5})$ angular; dominated by noise $\sigma_T\asymp1/\sqrt{T_{\max}d}$ for $T_{\max}\le d$ (raw) / $\le d^2$ (angular).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 4, sympy: raw=1/d, angular=d^{-3/2}, PASS); domination $1/d\le1/\sqrt{T_{\max}d}\iff T_{\max}\le d$ hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 08.01
**Location:** sections/08-lemma-incorrect-max.tex:38
**Content (≤ 2 lines):** Drift/fluctuation split of $\inner{W_U^a}{\tilde x_T}$ with $\E\tilde x_T=D\rowhat$, $D=\sum_k w_{T,k}\beta_k$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: linearity + clause (d) eq:drift_direction; $\sum_k w_{T,k}\beta_k\rowhat=(\sum w\beta)\rowhat$. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 08.02
**Location:** sections/08-lemma-incorrect-max.tex:50
**Content (≤ 2 lines):** Drift term $\inner{W_U^a}{\E\tilde x_T}=D\inner{W_U^a}{\rowhat}\le\abs D\incoh_0 R_U$; $\abs D\le M$, and $0\le D\le\snet M$ for $\snet\ge0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\abs{\inner{W_U^a}{\rowhat}}\le\incoh_0 R_U$ (incoherence); $\abs{\beta_k}\le\E[\abs{\proj_k}\mid\Fcal_{k-1}]\le M$ and net-drift identity ⇒ $\beta_k\in[\snet\driftc\rho_0,\snet M]$. Uses Step 02.01.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 08.03
**Location:** sections/08-lemma-incorrect-max.tex:66
**Content (≤ 2 lines):** Fluctuation conditional variance $\E[M_k^2\mid\Fcal_{k-1}]\le w_{T,k}^2\sigma_{\max}^2 R_U^2/d$ (isotropy upper bound), increments $\le2w_{T,k}R_U M$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\inner{W_U^a}{\Cov(\xi_k)W_U^a}\le(\sigma_{\max}^2/d)\norm{W_U^a}^2$ by eq:noise_isotropy; $\norm{\xi_k}\le2M$. Elementary quadratic form.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 08.04
**Location:** sections/08-lemma-incorrect-max.tex:82
**Content (≤ 2 lines):** Union bound over $|\Vocab|-1$ incorrect tokens at per-row budget $\delta_1/(|\Vocab|-1)$ ⇒ total $\delta_1$; threshold $2R_U M\sqrt{S_T\log(2(|\Vocab|-1)/\delta_1)/d}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: union bound is additive; $\sigma_{\max}\le2M$ fixes the displayed constant 2 (absolute Bernstein). Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 09.01
**Location:** sections/09-lemma-signal-floor.tex:55
**Content (≤ 2 lines):** Drift floor $\sum_k w_{T,k}\E[\proj_k\mid\Fcal_{k-1}]=\snet\sum_k w_{T,k}\E[\abs{\proj_k}\mid\Fcal_{k-1}]\ge\snet\driftc\rho_0$ via net-drift identity + floor + $\sum w=1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 1 = net-drift identity) + hand-check of the convex-combination step. Uses Step 02.01/02.02.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 09.02
**Location:** sections/09-lemma-signal-floor.tex:72
**Content (≤ 2 lines):** Fluctuation: $M_k=w_{T,k}\inner{\xi_k}{\rowhat}$, variance $\le w_{T,k}^2\sigma_{\max}^2/d$, increments $\le2w_{T,k}M$; lem:azuma ⇒ $\le2M\sqrt{2S_T\log(2/\delta_2)/d}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check of variance (quadratic form with $\norm{\rowhat}=1$) + lem:azuma hypotheses met ($\sigma^2\mapsto\sigma_{\max}^2$, horizon $S_T$). Cross-checked azuma-hoeffding.md.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 09.03
**Location:** sections/09-lemma-signal-floor.tex:88
**Content (≤ 2 lines):** Logit floor $\inner{W_U^{\corr}}{\tilde x_T}\ge\rho_0(\snet\driftc\rho_0-\nu)$ via $\norm{W_U^{\corr}}\ge\rho_0$; angular $\snorder_T=\inner{\rowhat}{\tilde x_T}/\norm{\tilde x_T}$, $\norm{\tilde x_T}\le M$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: multiply nonneg floor by $\norm{W_U^{\corr}}\ge\rho_0$; cosine identity $\snorder_T=\inner{\rowhat}{x_T}/\sqrt d=\inner{\rowhat}{\tilde x_T}/\norm{\tilde x_T}$ (since $x_T=\sqrt d\tilde x_T/\norm{\tilde x_T}$). Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 10.01
**Location:** sections/10-lemma-azuma.tex:30
**Content (≤ 2 lines):** Freedman tail $\Pr[\max_t\sum_s M_s\ge u]\le\exp(-u^2/(2(v+c_M u/3)))$ with $v=2\sigma^2 T/d$ predictable variation.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-freedman1975tail.md (Thm 1.6) + azuma-hoeffding.md (Bernstein-for-martingales, running-max via Ville). Hypotheses (bounded differences, predictable variation) met.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 10.02
**Location:** sections/10-lemma-azuma.tex:57
**Content (≤ 2 lines):** Variance-dominated regime $v+c_M u/3\le2v$ once $T\ge\tfrac49 d\log(2/\delta)$; exponent $-u^2 d/(8\sigma^2 T)$, two-sided $=\delta$ at $u=2\sigma\sqrt{T\log(2/\delta)/d}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 2: exponent $=\log(2/\delta)$ exactly, $2e^{-\text{exp}}=\delta$, PASS). Confirms the displayed constant 2 is the honest variance-dominated Bernstein constant.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 11.01
**Location:** sections/11-lemma-loss-to-margin.tex:22
**Content (≤ 2 lines):** $\loss(x)<\log2\iff p_{\corr}>1/2$ (since $\loss=-\log p_{\corr}$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $-\log p_{\corr}<\log2\iff p_{\corr}>1/2$. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 11.02
**Location:** sections/11-lemma-loss-to-margin.tex:26
**Content (≤ 2 lines):** $p_{\corr}>1/2\Rightarrow\max_{a\neq\corr}p_a<p_{\corr}\Rightarrow\max_{a\neq\corr}\inner{W_U^a}{x}<\inner{W_U^{\corr}}{x}$ (softmax order-preserving).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 8, 200k random logit vectors, no counterexample to $L<\log2\Rightarrow$ margin$>0$). Pigeonhole + softmax monotonicity hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

**Stage-2 revision (2026-05-29, Sudakov route).** `lem:incorrect_max_lower`
was rewritten from the second-moment / Paley--Zygmund method to the
**Sudakov minoration + Borell--TIS** route, under the isotropic-Gaussian
noise form `eq:noise_gaussian` (`ass:bounded_architecture(5)`, used by this
lemma only). The old steps 12.01--12.03 (small-ball mean, exceedance
covariance, Paley--Zygmund) are retired; the residual 🔴 (old 12.02, the
false-for-constant-$\incoh_0$ covariance bound) is **removed**, not merely
re-tagged. The new steps are 12.01 (Gaussian vector + exact correlation),
12.02 (Sudakov), 12.03 (Borell--TIS), 12.04 (shared drift, unchanged).

## Step 12.01
**Location:** sections/12-lemma-incorrect-max-lower.tex:54,86 (Steps 0--1)
**Content (≤ 2 lines):** Under `eq:noise_gaussian`, $(Z_a)_{a\neq\corr}\mid\Gcal$ is a centred Gaussian vector with $\operatorname{Cov}(Z_a,Z_{a'}\mid\Gcal)=\beta^2\inner{W_U^a}{W_U^{a'}}$, $\beta^2=\sum_k w_{T,k}^2\tau_k^2=\Theta(\sigma_T^2)$; hence $\abs{\operatorname{Corr}(Z_a,Z_{a'})}=$ Gram entry $\le\incoh_0$ exactly, giving canonical separation $\norm{Z_a-Z_{a'}}_2\ge\sqrt2\beta\rho_0\sqrt{1-\incoh_0}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: scalar covariance $\tau_k^2 I_d$ ⇒ cross terms vanish across $k$ (independent increments given $\Gcal$) and $\operatorname{Cov}\propto\inner{W_U^a}{W_U^{a'}}$, so correlation = normalised Gram entry = $\incoh(W_U)\le\incoh_0$ (`def:incoherence`) with NO Berry--Esseen term — this is exact for Gaussian, the whole point of the route. Separation $\norm{Z_a-Z_{a'}}_2^2=\operatorname{Var}Z_a+\operatorname{Var}Z_{a'}-2\operatorname{Corr}\sqrt{\cdot}\ge2\beta^2\rho_0^2(1-\incoh_0 R_U^2/\rho_0^2)$, $=2\beta^2\rho_0^2(1-\incoh_0)$ under the canonical $\rho_0=R_U$ of `rem:architecture_realism`. $\beta^2\in[\sigma_{\min}^2 S_T/d,\sigma_{\max}^2 S_T/d]=\Theta(\sigma_T^2)$ via $S_T\asymp e^{2S}/T$ (`lem:quad_variation`, Step 06.02). Elementary Gaussian algebra; replaces the retired small-ball + covariance steps.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 12.02
**Location:** sections/12-lemma-incorrect-max-lower.tex:132 (Step 2)
**Content (≤ 2 lines):** Sudakov minoration: $\delta_{\mathrm{sep}}$-separated $m=|\Vocab|-1$ points ⇒ $N(S,d_Z,\delta_{\mathrm{sep}}/2)\ge m$ ⇒ $\E[\max_{a}Z_a\mid\Gcal]\ge c\tfrac{\delta_{\mathrm{sep}}}{2}\sqrt{\log m}\ge c_1'\sigma_T\sqrt{(1-\incoh_0)\log(|\Vocab|-1)}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches sudakov-minoration.md (Vershynin Thm 7.4.1, VERIFIED verbatim against the official PDF by text extraction — see cite-vershynin2018.md). Packing/covering step: pairwise distance $\ge\delta_{\mathrm{sep}}$ ⇒ disjoint $(\delta_{\mathrm{sep}}/2)$-balls ⇒ $N\ge m$ (standard packing-vs-covering, hand-checked). Hypothesis (mean-zero Gaussian process) met by Step 12.01. $c,c_1'$ absolute.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 12.03
**Location:** sections/12-lemma-incorrect-max-lower.tex:152 (Step 3)
**Content (≤ 2 lines):** Borell--TIS: $g\mapsto\max_a(\Sigma_S^{1/2}g)_a$ is $\le\beta R_U=O(\sigma_T)$-Lipschitz ⇒ $\Pr[\max_a Z_a<\E\max_a Z_a-u\mid\Gcal]\le e^{-c_2 u^2/(C'\sigma_T)^2}$; take $u=\tfrac12$(Sudakov bound) ⇒ $\max_a Z_a\ge\sigma_T\sqrt{2\kappa(1-\incoh_0)\log(|\Vocab|-1)}$ w.p. $\ge1-(|\Vocab|-1)^{-c_3}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches borell-tis.md (Vershynin Thm 5.2.3, Gaussian concentration of Lipschitz functions; the underlying Gaussian isoperimetry Thm 5.2.2 = Tsirelson--Ibragimov--Sudakov + Borell; VERIFIED verbatim against the PDF — see cite-vershynin2018.md). Lipschitz constant of $\max$ = max coordinate std $=\max_a\sqrt{\operatorname{Var}Z_a}\le\beta R_U$ (digest's "Wrong Lipschitz constant" misuse avoided; $\abs{\max u-\max v}\le\norm{u-v}_\infty\le\norm{u-v}_2$ hand-checked). Constant identity $\kappa=(c_1'/2)^2/2$, $c_3=c_2(c_1'/(2C'))^2(1-\incoh_0)$ hand-checked; $\kappa\in(0,1)$ since $c_1'\le c_0/\sqrt2\le1/\sqrt2$. Conditional bound has $\Gcal$-free probability ⇒ unconditional by tower property (hand-checked).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 12.04
**Location:** sections/12-lemma-incorrect-max-lower.tex:194 (Step 4)
**Content (≤ 2 lines):** Incorrect drift carries shared $\abs D\le\snet M$: $\inner{W_U^{\hat a}}{\E\tilde x_T}=D\inner{W_U^{\hat a}}{\rowhat}\ge-\incoh_0 R_U\abs D$; deterministic correction $O(\critrate)$ in sub-critical regime. (Unchanged from second-moment version.)
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check identical to Step 08.02 (same $D$, sign flipped); $\abs D\le\snet M$ from net-drift identity. Consistent.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.01
**Location:** sections/13-theorem-R1-phase-transition.tex:97
**Content (≤ 2 lines):** Margin drift $\inner{W_U^{\corr}-W_U^{\hat a}}{\E\tilde x_T}=D(\inner{W_U^{\corr}}{\rowhat}-\inner{W_U^{\hat a}}{\rowhat})\ge\snet\driftc\rho_0(\rho_0-\incoh_0 R_U)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Script validation (CHECK 7: margin drift $\ge D(\norm{W_U^{\corr}}-\mu_0\max\norm{W_U})$, positive under $\mu_0<\rho_0/R_U$, 3000 random unembeddings, PASS). Uses shared $D\ge\snet\driftc\rho_0$ (Step 09.01).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.02
**Location:** sections/13-theorem-R1-phase-transition.tex:108
**Content (≤ 2 lines):** Margin fluctuation increments $\le2R_U\cdot2M w_{T,k}$, variance $\le w_{T,k}^2(2R_U)^2\sigma_{\max}^2/d$; lem:azuma + union ⇒ $\nu=4R_U M\sqrt{2S_T\log(2(|\Vocab|-1)/\delta_{\mathrm{fail}})/d}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\norm{W_U^{\corr}-W_U^{\hat a}}\le2R_U$; quadratic form + lem:azuma (Step 10.02). Elementary given lemmas.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.03
**Location:** sections/13-theorem-R1-phase-transition.tex:120
**Content (≤ 2 lines):** Success: $\Margin>0$ once $\snet\ge\sqrt2\critrate$, $c_1=2\sqrt2 e^S R_U M/(\driftc\rho_0(\rho_0-\incoh_0 R_U)/R_U)$; $\sqrt2$ slack absorbs $\log$ + lower-order corrections.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Cross-checked against the drift floor (Step 13.01) / noise $\nu$ (Step 13.02): $\snet\driftc\rho_0(\rho_0-\incoh_0 R_U)>\nu\iff\snet>\nu/[\driftc\rho_0(\rho_0-\incoh_0 R_U)]$; $\nu\le4\sqrt2 e^S R_U M\sqrt{\log(\cdots)/(T_{\max}d)}$. Constant $c_1$ assembled; $\sqrt2$/log absorption is the documented D13 slack convention (intentional).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.04
**Location:** sections/13-theorem-R1-phase-transition.tex:140
**Content (≤ 2 lines):** Failure: correct logit $\le R_U(\snet M+\nu_2)$ ($D\le\snet M$); incorrect max $\ge\sigma_T\sqrt{2(1-\incoh_0)\log(|\Vocab|-1)}-\incoh_0 R_U\snet M$; gap$>0$ under $\snet\le\critrate/\sqrt2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Cross-checked: both deterministic corrections $O(\critrate)$ (lower-order since $\snet\le\critrate/\sqrt2$); the $\sqrt2$ slack between $\sqrt2\critrate$ and $\critrate/\sqrt2$ absorbs the constant $(1-\incoh_0)$ — matching D13. The two-sided matching is the documented design.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.05
**Location:** sections/13-theorem-R1-phase-transition.tex:55
**Content (≤ 2 lines):** Union bound over exactly two events ($\Ecal_{\mathrm{sig}}$ budget $\delta_{\mathrm{fail}}$, $\Ecal_{\mathrm{inc}}$ budget $(|\Vocab|-1)^{-1}$) ⇒ good event $\ge1-\delta_{\mathrm{fail}}-(|\Vocab|-1)^{-1}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: additive union bound; matches the $1-\delta_{\mathrm{fail}}-(|\Vocab|-1)^{-1}$ in eq:R1_success. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 13.06
**Location:** sections/13-theorem-R1-phase-transition.tex:163
**Content (≤ 2 lines):** rem:min_dimension (demoted from corollary per Occam): solve $\snet\ge\sqrt2 c_1\sqrt{\log|\Vocab|/(T_{\max}d)}$ for $d$ ⇒ $d\ge2c_1^2\log|\Vocab|/(\snet^2 T_{\max})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: square both sides. Elementary.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 14.01
**Location:** sections/14-theorem-R2-critical-window.tex:75
**Content (≤ 2 lines):** Margin decomposition into drift $\mu_{T_{\max}}=\snet\driftc\rho_0(\rho_0-\incoh_0 R_U)$ + centred martingale; critical offset $=\critrate\driftc\rho_0(\rho_0-\incoh_0 R_U)$ by def of $\critrate$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Cross-checked against thm:R1 margin-drift slope (Step 13.01) and eq:critical_rate. Consistent; the offset identification uses the same $c_1$.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 14.02
**Location:** sections/14-theorem-R2-critical-window.tex:84
**Content (≤ 2 lines):** Conditional variance $V_{T_{\max}}\le S_{T_{\max}}(2R_U)^2\sigma_{\max}^2/d\le4R_U^2M^2e^{2S}/(T_{\max}d)=\sigma_{T_{\max}}^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\norm{W_U^{\corr}-W_U^{\hat a}}\le2R_U$, isotropy, $S_T\le e^{2S}/T$ (lem:quad_variation), $\sigma_{\max}\le2M$. Elementary chain.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 14.03
**Location:** sections/14-theorem-R2-critical-window.tex:88
**Content (≤ 2 lines):** Truncated conditional third moment $\rho_{T_{\max}}=O(R_U^3M^3e^{3S}d^{-3/2}T_{\max}^{-2})$ ($d^{-3/2}$ from truncated sub-Gaussian tail) ⇒ BE rate $\rho/V^{3/2}=O(e^S/\sqrt{T_{\max}})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches cite-hallheyde1980.md + berry-esseen-martingale.md ($\rho_T\le R_U^3M^3e^{4S}/(d^{3/2}T_{\max}^2)$, rate $e^S/\sqrt{T_{\max}}$). Truncation-event provenance from Step 05.02. Constant arrangement per digest.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 14.04
**Location:** sections/14-theorem-R2-critical-window.tex:96
**Content (≤ 2 lines):** Hall--Heyde Thm 3.6 ⇒ $\abs{\Pr[\sum D_t\le x\sigma]-\Phi(x)}\le C\rho/V^{3/2}$; invert at $x=-z+O(\beerr)$ ⇒ $\Pr[\Margin>0]=\Phi(z)+O(\beerr)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Matches thm:hallheyde_be (99-auxiliary) / cite-hallheyde1980.md hypotheses (square-integrable array, conditional 2nd+3rd moments). $1-\Phi(-z)=\Phi(z)$ by symmetry (hand-checked).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 14.05
**Location:** sections/14-theorem-R2-critical-window.tex:112
**Content (≤ 2 lines):** cor:R2_boundary: $\snet=\critrate\Rightarrow z=0\Rightarrow\Phi(0)=1/2$. cor:R2_width: $z\in[\pm1.28]$ ⇒ $w_{\mathrm{abs}}=\Theta(1/\sqrt{T_{\max}d})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: numerator $(\snet-\critrate)=0$ at threshold; $\sigma_{T_{\max}}=\Theta(1/\sqrt{T_{\max}d})$ ⇒ width scaling. $\Phi(0)=1/2$ standard.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 15.01
**Location:** sections/15-theorem-R3prime-cone.tex:63
**Content (≤ 2 lines):** Entry: $\E[\snorder_t\mid\Fcal_0]\ge\snet\driftc\rho_0/M=m^\star$ for $t\ge T_0$ (drift floor / $\norm{\tilde x_t}\le M$, $w_{t,0}=O(1/t)$ washout).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $m^\star=\snet\driftc\rho_0/M$ is the corrected $O(1)$ cosine (Step 09.03), drift floor from Step 09.01, washout from Step 03.03. Internally consistent.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 15.02
**Location:** sections/15-theorem-R3prime-cone.tex:73
**Content (≤ 2 lines):** Confinement: maximal inequality (lem:azuma $\max_t$) bounds running fluctuation $\le\varepsilon M/2$; $\snorder_t\ge m^\star-\varepsilon$ for all $T_0\le t\le T$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: the running-max form is already in eq:azuma_tail (Step 10.01); divide by $\norm{\tilde x_t}\le M$. No drift recurrence/ODE used.
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 15.03
**Location:** sections/15-theorem-R3prime-cone.tex:84
**Content (≤ 2 lines):** Terminal concentration: $\snorder_T$ within $O(1/\sqrt{T_{\max}d})$ of $m^\star$ (two-sided floor); invariant under rescaling, retraction adds $O(1/d^{1.5})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $\inner{\rowhat}{\tilde x_T}$ pinned in $[\snet\driftc\rho_0-\nu,\snet M+\nu]$, $\norm{\tilde x_T}\ge\inner{\rowhat}{\tilde x_T}$; cosine invariance (Step 09.03) + retraction (Step 07.03).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z

## Step 15.04
**Location:** sections/15-theorem-R3prime-cone.tex:104
**Content (≤ 2 lines):** ODE $\dot m=\snet\driftc\rho_0/M-m$ stated as INFORMAL, fixed point $m^\star$; explicitly NOT derivable from A1, requires (AS)+(L$\lambda$). No proof uses it.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: fixed point of $\dot m=K-m$ is $m=K$; the remark is flagged informal and unused. Constraint #2 honored (no forced ODE).
**Sub-agent task id:** none
**Last updated:** 2026-05-29T00:00:00Z
