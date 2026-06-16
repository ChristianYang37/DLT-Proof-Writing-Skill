# Confidence trace — Sobolev minimax lower bound (Phase C.5)

Every derivation step starts 🔴 `from-memory`. The sweep upgrades each via a
fast path (named textbook fact / hand-check → 🟢; technique- or
citation-digest match → 🟡) or independent re-derivation. The load-bearing
scaling and balance arithmetic were re-derived symbolically (sympy); the
report is `.proof-research/sweep-symbolic-check.md`. No step remains 🔴.

Sweep summary: **27 steps tagged — 🟢 23 / 🟡 4 / 🔴 0.**

---

## Step 1
**Location:** sections/01-preliminaries.tex:60
**Content (≤ 2 lines):** $\KL(P_f\|P_g)=\sum_i\KL(\mathcal N(f(x_i),\sigma^2)\|\mathcal N(g(x_i),\sigma^2))$ (tensorization over independent coordinates).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named fact — KL of a product measure is the sum of coordinate KLs (independence); hand-checked against `.proof-research/gaussian-kl.md`.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 2
**Location:** sections/01-preliminaries.tex:62
**Content (≤ 2 lines):** $\sum_i\KL(\cdots)=\frac{1}{2\sigma^2}\sum_i(f(x_i)-g(x_i))^2$ (common-variance Gaussian KL).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook identity $\KL(\mathcal N(\mu_1,\sigma^2)\|\mathcal N(\mu_2,\sigma^2))=(\mu_1-\mu_2)^2/(2\sigma^2)$; variances match so the log/ratio terms vanish. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 3
**Location:** sections/03-bump-family.tex:36
**Content (≤ 2 lines):** $\partial^\alpha[g(m(x-x^{(j)}))]=m^{r}(\partial^\alpha g)(m(x-x^{(j)}))$ then $\int|\cdot|^2=\frac{\omega^2}{m^{2s}}m^{2r}\int|\partial^\alpha g(m(x-x^{(j)}))|^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Chain rule pulls a factor $m$ per derivative order ($r=|\alpha|$); pull out the constant. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 4
**Location:** sections/03-bump-family.tex:37
**Content (≤ 2 lines):** Change of variables $y=m(x-x^{(j)})$: $\int_{[0,1]^d}|\partial^\alpha g(m(x-x^{(j)}))|^2dx=m^{-d}\int_{(0,1)^d}|\partial^\alpha g(y)|^2dy$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Jacobian of $y=m(x-x^{(j)})$ is $m^{d}$, so $dx=m^{-d}dy$; $\operatorname{supp}g\subseteq(0,1)^d$ keeps the integral on one cell. Sympy-confirmed (sweep-symbolic-check.md).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 5
**Location:** sections/03-bump-family.tex:38
**Content (≤ 2 lines):** $=\frac{\omega^2}{m^{2(s-r)}}m^{-d}\|\partial^\alpha g\|_{L^2}^2$ (collect powers of $m$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Exponent arithmetic $-2s+2r=-2(s-r)$. Sympy-confirmed: per-bump integral $=\omega^2 m^{-2(s-r)-d}$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 6
**Location:** sections/03-bump-family.tex:39
**Content (≤ 2 lines):** $\le\omega^2 m^{-d}\|\partial^\alpha g\|_{L^2}^2$ since $r\le s\Rightarrow m^{-2(s-r)}\le1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $m\ge1$, $s-r\ge0$, so $m^{-2(s-r)}\le1$. Trivial monotonicity; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 7
**Location:** sections/03-bump-family.tex:51
**Content (≤ 2 lines):** $\|u_{\tau^{(k)}}\|_{W^s_2}^2=\sum_{|\alpha|\le s}\sum_j\tau_j^{(k)}\int|\partial^\alpha(\cdots)|^2$ (disjoint-support orthogonality).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Bumps have pairwise disjoint supports, so cross terms in $\|\sum_j\cdot\|^2$ vanish and squared norms add; definition of $\|\cdot\|_{W^s_2}^2$ from Eq.~(1). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 8
**Location:** sections/03-bump-family.tex:53
**Content (≤ 2 lines):** $\le\sum_{|\alpha|\le s}\|\tau^{(k)}\|_0\,\omega^2 m^{-d}\|\partial^\alpha g\|_{L^2}^2$ (insert Step 6).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute the per-bump bound of Steps 3–6; $\sum_j\tau_j^{(k)}=\|\tau^{(k)}\|_0$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 9
**Location:** sections/03-bump-family.tex:54
**Content (≤ 2 lines):** $\le\omega^2 m^{-d}M_0\sum_{|\alpha|\le s}\|\partial^\alpha g\|_{L^2}^2=\omega^2 C_g$ (since $\|\tau\|_0\le M_0=m^d$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\|\tau^{(k)}\|_0\le M_0$, $m^{-d}M_0=1$, and $C_g:=\sum_{|\alpha|\le s}\|\partial^\alpha g\|_{L^2}^2$ by definition. This gives feasibility Eq.~(3). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 10
**Location:** sections/03-bump-family.tex:69
**Content (≤ 2 lines):** $\int|\frac{\omega}{m^s}g(m(x-x^{(j)}))|^2dx=\frac{\omega^2}{m^{2s}}m^{-d}\|g\|_{L^2}^2=\frac{c_g\omega^2}{m^{2s+d}}$ (Step 4 with $r=0$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Specialize Steps 3–5 to $r=0$; $c_g:=\|g\|_{L^2}^2$. Sympy-confirmed cell mass $=c_g\omega^2 m^{-2s-d}$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 11
**Location:** sections/03-bump-family.tex:78
**Content (≤ 2 lines):** $\|u_{\tau^{(k)}}-u_{\tau^{(k')}}\|_{L^2}^2=\sum_j\1\{\tau_j^{(k)}\ne\tau_j^{(k')}\}\int|\frac{\omega}{m^s}g(m(x-x^{(j)}))|^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Difference supported only on differing cells, equals $\pm$ one bump there; disjoint-support additivity. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 12
**Location:** sections/03-bump-family.tex:80
**Content (≤ 2 lines):** $=\rho_H(\tau^{(k)},\tau^{(k')})\cdot\frac{c_g\omega^2}{m^{2s+d}}$ (count differing cells = Hamming distance; insert Step 10).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Number of indicators equal to 1 is $\rho_H$; per-cell mass from Step 10. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 13
**Location:** sections/03-bump-family.tex:81
**Content (≤ 2 lines):** $\ge\frac{M_0}{8}\cdot\frac{c_g\omega^2}{m^{2s+d}}=\frac{c_g}{8}\frac{\omega^2}{m^{2s}}$ (Varshamov–Gilbert separation $\rho_H\ge M_0/8$, $M_0=m^d$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Hamming lower bound $\rho_H\ge M_0/8$ from `\Cref{lem:vg}` Eq.~(2), matched against `.proof-research/cite-tsybakov2009introduction-vg-fano.md` (Lemma 2.9); the $m^d$ cancellation is sympy-confirmed.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 14
**Location:** sections/04-kl-bound.tex:23
**Content (≤ 2 lines):** $\KL(P_{u_k}\|P_{u_{k'}})=\frac{1}{2\sigma^2}\sum_i(\Delta u(x_i))^2$ (apply `\Cref{fac:gauss-kl}`).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct application of `\Cref{fac:gauss-kl}` (Steps 1–2, already verified); hypotheses (common fixed design, common $\sigma^2$) hold here.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 15
**Location:** sections/04-kl-bound.tex:30
**Content (≤ 2 lines):** $\sum_i(\Delta u(x_i))^2=\sum_{j:\tau_j^{(k)}\ne\tau_j^{(k')}}\sum_{i:x_i\in\text{cell }j}(\frac{\omega}{m^s}g(m(x_i-x^{(j)})))^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\Delta u$ supported on differing cells, equals $\pm$ one bump there; partition the design sum over cells. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 16
**Location:** sections/04-kl-bound.tex:32
**Content (≤ 2 lines):** $\le\sum_{j:\,\ne}\frac{n}{M_0}\cdot\frac{\omega^2}{m^{2s}}G_\infty$ (each cell holds $n/M_0$ points; bound each by max $\frac{\omega^2}{m^{2s}}\|g\|_\infty^2$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Grid-regularity (each cell has exactly $n/M_0$ design points) is the stated hypothesis of `\Cref{lem:kl}`; pointwise bound $g(\cdot)^2\le\|g\|_\infty^2=G_\infty$. Matched to `.proof-research/gaussian-kl.md` §canonical use.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 17
**Location:** sections/04-kl-bound.tex:34
**Content (≤ 2 lines):** $=\rho_H\cdot\frac{n}{M_0}\frac{\omega^2}{m^{2s}}G_\infty\le M_0\cdot\frac{n}{M_0}\frac{\omega^2}{m^{2s}}G_\infty=G_\infty\frac{n\omega^2}{m^{2s}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\rho_H\le M_0$ (whole cube), $M_0$ cancels. Sympy-confirmed design-sum bound $=n\omega^2/m^{2s}$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 18
**Location:** sections/06-main-theorem.tex:43
**Content (≤ 2 lines):** $B n^{1/(2s+d)}\le m=\lceil Bn^{1/(2s+d)}\rceil\le 2Bn^{1/(2s+d)}$ for $n$ large.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Ceiling satisfies $x\le\lceil x\rceil\le x+1\le 2x$ once $x\ge1$, i.e. $n$ large enough that $Bn^{1/(2s+d)}\ge1$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 19
**Location:** sections/06-main-theorem.tex:54
**Content (≤ 2 lines):** $\|f_k-f_{k'}\|_{L^2}^2\ge\frac{c_g}{8}\frac{\omega_0^2}{m^{2s}}=:(2\Delta)^2$, so $\Delta^2=\frac{c_g\omega_0^2}{32 m^{2s}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Apply `\Cref{lem:bumps}` Eq.~(4) (Step 13) with $\omega=\omega_0$; $(2\Delta)^2=4\Delta^2=\frac{c_g\omega_0^2}{8 m^{2s}}\Rightarrow\Delta^2=\frac{c_g\omega_0^2}{32 m^{2s}}$. Sympy-confirmed (sweep-symbolic-check.md). NOTE: the first draft wrote $128$ here — a $4\times$ constant slip, caught by this sweep and corrected to $32$; rate exponent unaffected.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 20
**Location:** sections/06-main-theorem.tex:62
**Content (≤ 2 lines):** $\log M\ge\frac{m^d}{8}\log2$ (Varshamov–Gilbert cardinality $M\ge2^{m^d/8}$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** $\log M\ge\log 2^{m^d/8}=\frac{m^d}{8}\log2$ from `\Cref{lem:vg}` Eq.~(2); matched to citation digest (Lemma 2.9).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 21
**Location:** sections/06-main-theorem.tex:71
**Content (≤ 2 lines):** $\max_{k\ne k'}\KL\le\frac{G_\infty}{2\sigma^2}\frac{n\omega_0^2}{m^{2s}}=\frac{G_\infty\omega_0^2}{2\sigma^2}\frac{n}{m^{2s+d}}m^d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** `\Cref{lem:kl}` (Step 17) at $\omega=\omega_0$; multiply and divide by $m^d$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 22
**Location:** sections/06-main-theorem.tex:73
**Content (≤ 2 lines):** $\le\frac{G_\infty\omega_0^2}{2\sigma^2}\frac{1}{B^{2s+d}}m^d$ using $m^{2s+d}\ge B^{2s+d}n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** From Step 18, $m\ge Bn^{1/(2s+d)}\Rightarrow m^{2s+d}\ge B^{2s+d}n\Rightarrow n/m^{2s+d}\le B^{-(2s+d)}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 23
**Location:** sections/06-main-theorem.tex:74
**Content (≤ 2 lines):** $=\frac{\log2}{128}m^d\le\frac14\log M$ (insert $B^{2s+d}=64G_\infty\omega_0^2/(\sigma^2\log2)$; then $\frac1{128}\le\frac14\cdot\frac18$ and Eq.~(8)).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Sympy-confirmed (sweep-symbolic-check.md): after substituting $B$, the bound equals $\frac{\log2}{128}m^d$; and $\frac{\log2}{128}m^d\le\frac14\cdot\frac{m^d}{8}\log2=\frac{\log2}{32}m^d\le\frac14\log M$ via Step 20. The first draft wrote this transition as an equality; corrected to the inequality $\frac1{128}\le\frac1{32}$ during the sweep.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 24
**Location:** sections/06-main-theorem.tex:90
**Content (≤ 2 lines):** $\inf_\psi\Pr[\psi\ne V]\ge1-\frac{I(V;Y)+\log2}{\log M}\ge1-\frac{\frac14\log M+\log2}{\log M}\ge\frac12$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Fano inequality + mutual-information bound from `\Cref{lem:fano}` Eq.~(9), matched to `.proof-research/local-fano.md` and citation digest (Thm 2.5/Cor 2.6); $\log2/\log M\le1/4$ for $n$ large via Step 20. Arithmetic $1-1/4-1/4=1/2$ hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 25
**Location:** sections/06-main-theorem.tex:109
**Content (≤ 2 lines):** $2\|\hat f-f_k\|\ge\|\hat f-f_k\|+\|\hat f-f_\psi\|\ge\|f_k-f_\psi\|\ge2\Delta$ on $\{\psi\ne k\}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\psi$ minimizes distance to $\hat f$ ($\|\hat f-f_\psi\|\le\|\hat f-f_k\|$); triangle inequality; separation Eq.~(7). Named textbook (triangle) + minimality. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 26
**Location:** sections/06-main-theorem.tex:120
**Content (≤ 2 lines):** $\sup_{f^*}\E\|\hat f-f^*\|^2\ge\frac1M\sum_k\E\|\hat f-f_k\|^2\ge\Delta^2\Pr[\psi\ne V]\ge\Delta^2/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** sup over $\mathcal W\supseteq\{f_k\}$ $\ge$ max $\ge$ average; $\|\hat f-f_k\|^2\ge\Delta^2\1\{\psi\ne k\}$ from Step 25; uniform-prior average $=\Pr[\psi\ne V]$; Fano (Step 24). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 27
**Location:** sections/06-main-theorem.tex:142
**Content (≤ 2 lines):** $\inf_{\hat f}\sup_{f^*}\E\|\hat f-f^*\|^2\ge\frac{\Delta^2}{2}=\frac{c_g\omega_0^2}{64 m^{2s}}\ge\frac{c_g\omega_0^2}{64(2B)^{2s}}n^{-2s/(2s+d)}=c\,n^{-2s/(2s+d)}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\Delta^2/2=\frac12\cdot\frac{c_g\omega_0^2}{32 m^{2s}}=\frac{c_g\omega_0^2}{64 m^{2s}}$ (using the corrected $\Delta^2$ from Step 19); $m\le2Bn^{1/(2s+d)}\Rightarrow m^{-2s}\ge(2B)^{-2s}n^{-2s/(2s+d)}$; collect constants into $c=\frac{c_g\omega_0^2}{64(2B)^{2s}}$. Sympy-confirmed (sweep-symbolic-check.md); the final rate exponent $-2s/(2s+d)$ is exact and invariant to the leading constant.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z
