# Confidence trace — NTK two-layer convergence (Phase C.5)

Scope: Appendix. Every derivation step starts 🔴 `from-memory` and is upgraded via fast path
(named textbook inequality → 🟢; technique/citation/lemma digest match → 🟡) or flagged 🔴 with
a `\todo{verify}` marker if not re-derivable by fast path. Steps 1–33 cover the body, plus
Step 34 (flip-anchor) and Step 35 (init-residual Markov) added in Phase-D iter 1. Phase-D
iter 2 collapsed the former init-gram Steps 1–5 (Frobenius-second-moment + Markov route) into
the Hoeffding + union route now in Steps 1–3; downstream step numbers are unchanged.

Summary after sweep (post Phase-D iter 2): no residual 🔴.
The activation-flip remainder aggregation constant $1/8$ (formerly the single 🔴) was
re-derived in Phase-D iter 1 ($8c\lzero\le\lzero/8$ for $c\le1/64$; the `\todo` was removed),
and the remainder fold-in itself was promoted to a displayed perturbed recursion in iter 2
(W-G). The init-gram concentration is now licensed at the stated $\log(n/\delta)$ width by the
Hoeffding route (W-A), which also consumes the previously-unused \Cref{fac:hoeffding} (W-B).

---

## Step 1
**Location:** sections/02-lemma-init-gram-close.tex (eq:entry-hoeffding)
**Content (≤ 2 lines):** Entrywise Hoeffding: $\Pr[|H_{ij}(0)-\Hinf_{ij}|\ge\tau] \le 2\exp(-m\tau^2/2)$ for $\tau=\lzero/(4n)$, since $Z_r^{ij}\in[-1,1]$ and $\sum_r(\beta_r-\alpha_r)^2=4m$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** \Cref{fac:hoeffding} on $S=\sum_r Z_r^{ij}$ with threshold $m\tau$, then rescale by $1/m$; $2(m\tau)^2/(4m)=m\tau^2/2$. Hand-checked. Phase-D iter-2 rewrite (W-A): replaced the Frobenius-second-moment + Markov route, whose displayed bound $16n^2/(\lzero^2 m)$ did not reach $\delta$ at the stated $\log(n/\delta)$ width, with the Hoeffding route that genuinely licenses it. This also consumes the previously-unused \Cref{fac:hoeffding} (W-B).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T03:55:00Z

## Step 2
**Location:** sections/02-lemma-init-gram-close.tex (eq:entry-union)
**Content (≤ 2 lines):** Union over $n^2$ entries: $\Pr[\max_{ij}|H_{ij}(0)-\Hinf_{ij}|\ge\tau] \le 2n^2\exp(-m\tau^2/2)\le\delta$ when $m\ge\frac{2}{\tau^2}\log(2n^2/\delta)=\frac{32n^2}{\lzero^2}\log(2n^2/\delta)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Union bound over $n^2$ events from Step 1; solve $2n^2\exp(-m\tau^2/2)\le\delta$ for $m$. $\log(2n^2/\delta)\le4\log(n/\delta)$ for $n\ge1$, so implied by eq:width-init with $C\ge128$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T03:55:00Z

## Step 3
**Location:** sections/02-lemma-init-gram-close.tex (eq:op-from-frob)
**Content (≤ 2 lines):** On the complement, every $|H_{ij}(0)-\Hinf_{ij}|\le\tau$, so $\opnorm{H(0)-\Hinf}\le\fnorm{H(0)-\Hinf}\le\sqrt{n^2\tau^2}=n\tau=\lzero/4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\opnorm{M}\le\fnorm{M}$ (largest singular value $\le$ root-sum-of-squares); Frobenius $=\sqrt{\sum_{ij}|\cdot|^2}\le\sqrt{n^2\tau^2}$ using the entrywise bound from Step 2; $n\tau=n\cdot\lzero/(4n)=\lzero/4$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T03:55:00Z

## Step 6
**Location:** sections/02-lemma-init-gram-close.tex:66 (eq:weyl-init)
**Content (≤ 2 lines):** $\lmin(H(0)) \ge \lmin(\Hinf) - \opnorm{H(0)-\Hinf} \ge \lzero - \lzero/4 = \tfrac34\lzero$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Weyl's inequality (\Cref{fac:weyl}); hypotheses (symmetric $H(0)$, $\Hinf$) match .proof-research/cite-bhatia1997matrix-weyl.md.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 7
**Location:** sections/03-lemma-gram-stability.tex:24 (eq:entry-diff)
**Content (≤ 2 lines):** $|H_{ij}(W)-H_{ij}(0)| \le \frac1m\sum_r |x_i^\top x_j||S_{r,ij}(W)-S_{r,ij}(0)| \le \frac1m\sum_r \indic{E_{r,i}\cup E_{r,j}}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Triangle inequality termwise + sign-flip event identification; matches .proof-research/relu-indicator-perturbation.md §Key facts 1–2.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 8
**Location:** sections/03-lemma-gram-stability.tex:35–37 (E_{r,i} inclusion)
**Content (≤ 2 lines):** Sign flip of $w_r^\top x_i$ forces $|w_r(0)^\top x_i|\le R$, via Cauchy–Schwarz $|(w_r-w_r(0))^\top x_i|\le R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Cauchy–Schwarz with $\norm{x_i}=1$ and $\norm{w_r-w_r(0)}\le R$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 9
**Location:** sections/03-lemma-gram-stability.tex:43 (eq:anti-conc)
**Content (≤ 2 lines):** $\Pr[|\N(0,1)|\le R] = \int_{-R}^R \frac1{\sqrt{2\pi}}e^{-t^2/2}dt \le 2R/\sqrt{2\pi} \le R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Gaussian density $\le 1/\sqrt{2\pi}\le1/2$ on interval of length $2R$; $2/\sqrt{2\pi}\le1$. Named anti-concentration fact, hand-checked; matches relu-indicator-perturbation.md §3.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 10
**Location:** sections/03-lemma-gram-stability.tex:53 (eq:exp-entry)
**Content (≤ 2 lines):** $\E|H_{ij}(W)-H_{ij}(0)| \le \frac1m\sum_r \Pr[E_{r,i}\cup E_{r,j}] \le 2R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Take expectation of Step 7; union bound $\Pr[A\cup B]\le\Pr A+\Pr B\le2R$ via Step 9. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 11
**Location:** sections/03-lemma-gram-stability.tex:60 (eq:exp-op)
**Content (≤ 2 lines):** $\E\opnorm{H(W)-H(0)} \le \sum_{ij}\E|H_{ij}(W)-H_{ij}(0)| \le 2n^2 R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\opnorm{M}\le\fnorm{M}\le\sum_{ij}|M_{ij}|$ (chain of norm inequalities); apply Step 10 to each of $n^2$ entries. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 12
**Location:** sections/03-lemma-gram-stability.tex:71 (eq:markov-stab)
**Content (≤ 2 lines):** Markov: $\Pr[\opnorm{\cdot}\ge\lzero/4] \le \frac4\lzero\E\opnorm{\cdot} \le 8n^2R/\lzero = 8c\delta \le \delta$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Markov on nonnegative r.v.; substitute Step 11 then $R=c\delta\lzero/n^2$; $c\le1/8$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 13
**Location:** sections/03-lemma-gram-stability.tex:80 (eq:weyl-stab)
**Content (≤ 2 lines):** $\lmin(H(W)) \ge \lmin(H(0)) - \opnorm{H(W)-H(0)} \ge \tfrac34\lzero - \tfrac14\lzero = \tfrac12\lzero$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Weyl (\Cref{fac:weyl}) + intersection with \Cref{lem:init-gram-close} event; matches cite-bhatia1997matrix-weyl.md.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 14
**Location:** sections/04-lemma-contraction.tex:24 (eq:grad-r)
**Content (≤ 2 lines):** $\partial L/\partial w_r = \sum_i(u_i-y_i)\partial u_i/\partial w_r = \frac1{\sqrt m}\sum_i(u_i-y_i)a_r\indic{w_r^\top x_i\ge0}x_i$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Chain rule on $L=\tfrac12\norm{y-u}^2$; $\partial u_i/\partial w_r = \tfrac1{\sqrt m}a_r\sigma'(w_r^\top x_i)x_i$ with $\sigma'=\indic{\ge0}$. Hand-checked derivative.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 15
**Location:** sections/04-lemma-contraction.tex:32 (eq:grad-norm, line 1)
**Content (≤ 2 lines):** $\norm{\partial L/\partial w_r} \le \frac1{\sqrt m}\sum_i|u_i-y_i||a_r|\indic{\cdot}\norm{x_i}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Triangle inequality on the sum of vectors. Named textbook inequality.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 16
**Location:** sections/04-lemma-contraction.tex:34 (eq:grad-norm, line 2)
**Content (≤ 2 lines):** $\le \frac1{\sqrt m}\sum_i|u_i-y_i| \le \frac{\sqrt n}{\sqrt m}\norm{y-u}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $|a_r|=1,\indic{\cdot}\le1,\norm{x_i}=1$; then Cauchy–Schwarz $\sum_i|u_i-y_i|\le\sqrt n\norm{y-u}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 17
**Location:** sections/04-lemma-contraction.tex:48–51 (eq:u-step)
**Content (≤ 2 lines):** $u_i(k+1)-u_i(k) = \inner{\partial u_i/\partial W}{W(k+1)-W(k)} = -\eta\sum_j(u_j-y_j)H_{ij}(k)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Local linearity under fixed activation pattern + GD update + Gram identity (Step 18); matches dzps-contraction-algebra.md §One-step residual identity (with $\varepsilon(k)=0$ under fixed patterns).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 18
**Location:** sections/04-lemma-contraction.tex:55 (eq:gram-identity)
**Content (≤ 2 lines):** $\inner{\partial u_i/\partial W}{\partial u_j/\partial W} = \frac1m\sum_r a_r^2 x_i^\top x_j\indic{}\indic{} = H_{ij}(k)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute the per-neuron Jacobian from Step 14, $a_r^2=1$, match \Cref{def:gram} Eq.~(emp-gram). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 19
**Location:** sections/04-lemma-contraction.tex:62 (eq:resid-vec)
**Content (≤ 2 lines):** $y-u(k+1) = (I-\eta H(k))(y-u(k))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Vectorize Step 17 ($u(k+1)-u(k)=-\eta H(k)(u(k)-y)$) and subtract from $y$. Hand-checked algebra.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 20
**Location:** sections/04-lemma-contraction.tex:69 (eq:contract-chain, lines 1–2)
**Content (≤ 2 lines):** $\norm{y-u(k+1)}^2 = (y-u(k))^\top(I-\eta H)^2(y-u(k)) \le \norm{I-\eta H}_2^2\norm{y-u(k)}^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Expand quadratic form; Rayleigh bound $v^\top M^2 v\le\norm{M}_2^2\norm v^2$. Named textbook fact.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 21
**Location:** sections/04-lemma-contraction.tex:71 (eq:contract-chain, line 3)
**Content (≤ 2 lines):** $\norm{I-\eta H(k)}_2 \le 1-\eta\lmin(H(k))$, using $\eta\lambda_{\max}(H)\le\eta n\le1$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Eigenvalues of $I-\eta H$ are $1-\eta\lambda_\ell\in[1-\eta\lambda_{\max},1-\eta\lmin]\subseteq[0,1-\eta\lmin]$; $\lambda_{\max}(H)\le\opnorm H\le n$ and $\eta\le\lzero/(2n^2)$ give nonnegativity. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 22
**Location:** sections/04-lemma-contraction.tex:72 (eq:contract-chain, lines 4–5)
**Content (≤ 2 lines):** $\le(1-\tfrac{\eta\lzero}2)^2\norm{y-u(k)}^2 \le (1-\tfrac{\eta\lzero}2)\norm{y-u(k)}^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute $\lmin(H(k))\ge\tfrac12\lzero$; then $(1-x)^2\le1-x$ for $x\in[0,1]$ with $x=\eta\lzero/2$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 23
**Location:** sections/05-lemma-main-induction.tex (base case)
**Content (≤ 2 lines):** Base case $k=0$: conv. equality; stay-in-ball trivial; $\lmin(H(0))\ge\tfrac34\lzero\ge\tfrac12\lzero$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Directly from \Cref{lem:init-gram-close} (base of induction); hypothesis check trivial.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 24
**Location:** sections/05-lemma-main-induction.tex (eq:move-sum, lines 1–2)
**Content (≤ 2 lines):** $\norm{w_r(k+1)-w_r(0)} \le \sum_{s\le k}\norm{w_r(s+1)-w_r(s)} \le \sum_s \frac{\eta\sqrt n}{\sqrt m}\norm{y-u(s)}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Triangle inequality over telescoping path + \Cref{lem:contraction} Eq.~(move) at each $s$; matches dzps-contraction-algebra.md §Weight-movement bound.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 25
**Location:** sections/05-lemma-main-induction.tex (eq:move-sum, lines 3–5)
**Content (≤ 2 lines):** $\le \frac{\eta\sqrt n}{\sqrt m}\norm{y-u(0)}\sum_{s\ge0}(1-\tfrac{\eta\lzero}2)^{s/2} \le \frac{4\sqrt n\norm{y-u(0)}}{\sqrt m\lzero}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Insert geometric residual decay; geometric series $\sum(1-x/2)^{s/2}\le\frac{2}{1-\sqrt{1-x}}\le\frac4x$ using $1-\sqrt{1-x}\ge x/2$ for $x\in[0,1]$; $\eta$ cancels. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 26
**Location:** sections/05-lemma-main-induction.tex (width threshold for stay-in-ball)
**Content (≤ 2 lines):** With $\norm{y-u(0)}\le\sqrt{2n/\delta}$, RHS $\le 4\sqrt2\,n/(\sqrt{m\delta}\lzero)\le R$ iff $m\ge 32n^6/(c^2\delta^3\lzero^4)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute \Cref{lem:init-residual} bound $\sqrt{2n/\delta}$ (matching .tex line 67); solve $4\sqrt2\,n/(\sqrt{m\delta}\lzero)\le c\delta\lzero/n^2$ for $m$, giving $m\ge32n^6/(c^2\delta^3\lzero^4)$ ($\delta^3$, consistent with eq:width-main). Hand-checked arithmetic; Phase-D iter-1 sync.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 27
**Location:** sections/05-lemma-main-induction.tex:122
**Content (≤ 2 lines):** Activation-flip remainder $\norm{\varepsilon(k)} \le \frac{\eta\lzero}8\norm{y-u(k)}$ via honest $\abs{\mathcal S_k}^1$ aggregation + whp ball-count event $\mathcal E_4$ (Eq.~flip-event-budget).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Phase-D iter-1 rewrite. (i) Exponent: triangle over $\abs{\mathcal S_k}$ flips + Cauchy–Schwarz over $n$ coords gives $\norm{\varepsilon(k)}\le\frac{\eta n}m\abs{\mathcal S_k}\norm{y-u(k)}$ (exponent $1$, not $1/2$; the prose mechanism licenses exactly this). (ii) Randomness: $\mathcal S_k\subseteq\mathcal N=\{(r,i):\abs{w_r(0)^\top x_i}\le2R\}$, a $W(0)$-only set; Markov at $\delta/4$ gives event $\mathcal E_4=\{\abs{\mathcal N}\le8nmR/\delta\}$ added to the union budget (now $4\times\delta/4$), so $\abs{\mathcal S_k}\le8nmR/\delta$ holds deterministically for ALL $k$ at once — no per-$k$ union needed. (iii) Constant: substituting $R=c\delta\lzero/n^2$ gives prefactor $8c\lzero\le\lzero/8$ for $c\le1/64$; $n,m,\delta$ cancel, so the bound is width-free. `\todo` removed. Hand-checked via sympy.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 28
**Location:** sections/05-lemma-main-induction.tex (eq:gram-floor-kp1)
**Content (≤ 2 lines):** $\lmin(H(k+1)) \ge \lmin(H(0)) - \opnorm{H(k+1)-H(0)} \ge \tfrac34\lzero-\tfrac14\lzero = \tfrac12\lzero$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:gram-stability} applies (stay-in-ball at $k+1$) + Weyl (\Cref{fac:weyl}); hypotheses verified at cite-site (every neuron within $R$). Matches cite-bhatia1997matrix-weyl.md.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 29
**Location:** sections/05-lemma-main-induction.tex (eq:contract-kp1)
**Content (≤ 2 lines):** $\norm{y-u(k+1)}^2 \le (1-\tfrac{\eta\lzero}2)\norm{y-u(k)}^2 \le (1-\tfrac{\eta\lzero}2)^{k+1}\norm{y-u(0)}^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:contraction} (with Step 27 remainder absorbed) + inductive hypothesis Eq.~(main-conv) at $k$. Conditional on Step 27.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 30
**Location:** sections/05-lemma-main-induction.tex (eq:init-second-moment, lines 1–2)
**Content (≤ 2 lines):** $\E\norm{y-u(0)}^2 = \sum_i(y_i^2+\E u_i(0)^2) = \sum_i(y_i^2+\frac1m\sum_r\E\sigma(w_r(0)^\top x_i)^2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Expand $\norm{y-u(0)}^2$; $\E u_i(0)=0$ kills cross term ($a_r$ mean-zero, independent); $\E[a_ra_{r'}]=\indic{r=r'}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 31
**Location:** sections/05-lemma-main-induction.tex (eq:init-second-moment, lines 3–4)
**Content (≤ 2 lines):** $\le \sum_i(1+\frac1m\sum_r\E[(w_r(0)^\top x_i)^2]) = \sum_i(1+1) = 2n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $|y_i|\le1$, $\sigma(z)^2\le z^2$, $w_r(0)^\top x_i\sim\N(0,1)$ so $\E[(\cdot)^2]=1$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 32
**Location:** sections/06-main-theorem.tex (eq:union)
**Content (≤ 2 lines):** $\Pr[\mathcal E_1\cap\mathcal E_2\cap\mathcal E_3] \ge 1-\sum_i\Pr[\mathcal E_i^c] \ge 1-3\cdot\delta/3 = 1-\delta$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Union bound $\Pr[\cap\mathcal E_i]=1-\Pr[\cup\mathcal E_i^c]\ge1-\sum\Pr[\mathcal E_i^c]$; each lemma at $\delta/3$. Named textbook fact.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 33
**Location:** sections/06-main-theorem.tex (iteration count)
**Content (≤ 2 lines):** Solving $(1-\tfrac{\eta\lzero}2)^k\cdot(8n/\delta)\le\varepsilon$ gives $k=O(\tfrac1{\eta\lzero}\log\tfrac{n}{\delta\varepsilon})=O(\tfrac{n^2}{\lzero^2}\log\tfrac{n}{\delta\varepsilon})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $-\log(1-x)\ge x$ so $k\ge\frac{\log(8n/(\delta\varepsilon))}{\eta\lzero/2}$; substitute $\eta=\kappa\lzero/n^2$. Initial residual $\|y-u(0)\|^2\le8n/\delta$ on $\mathcal E_3$ ($\mathcal E_3$ invokes \Cref{lem:init-residual} at level $\delta/4$, giving $\sqrt{8n/\delta}$; Step 35). Hand-checked. Phase-D iter-2 sync ($6n/\delta\to8n/\delta$).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 34
**Location:** sections/05-lemma-main-induction.tex (eq:flip-anchor)
**Content (≤ 2 lines):** $|w_r(0)^\top x_i| \le \norm{w_r(k)-w_r(0)}+\norm{w_r(k+1)-w_r(k)} \le R+R_{\mathrm{step}} \le 2R$ (flip event anchored at init).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Cauchy–Schwarz + inductive stay-in-ball Eq.~(main-stay) + movement Eq.~(move) + $R_{\mathrm{step}}\le R$ for the stated width. Added in Phase-D iter 1 to fix the non-Gaussian anti-concentration application. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z

## Step 35
**Location:** sections/05-lemma-main-induction.tex (eq:init-markov)
**Content (≤ 2 lines):** Markov at threshold $2n/\delta$: $\Pr[\norm{y-u(0)}^2\ge2n/\delta]\le\frac\delta{2n}\cdot2n=\delta$, so $\norm{y-u(0)}\le\sqrt{2n/\delta}$ w.p. $\ge1-\delta$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Markov on nonnegative $\norm{y-u(0)}^2$ vs threshold $2n/\delta$; substitute $\E[\cdot]\le2n$ (Step 31). Added in Phase-D iter 1 to show the $1-\delta$ upgrade explicitly. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T17:44:25Z
