# Confidence trace — Phase C.5 sweep

Initialized: all steps 🔴. Final tags after fast-path / hand-check / digest match.

---

## Lemma 3.1 (bump-norms) — sections/03-bump-family.tex

### Step 1 — chain rule for $\partial^\alpha \psi_k$
**Location:** sections/03-bump-family.tex, proof part (i), eq before align "By the change of variable".
**Content:** $\partial^\alpha \psi_k(x) = m^{|\alpha|} (\partial^\alpha \psi)(m(x - z_k))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Standard textbook chain rule for composition with linear scaling. Each $\partial_{x_\ell}$ pulls down a factor of $m$.
**Sub-agent task id:** none

### Step 2 — change of variables $\int_{R_k} (\partial^\alpha \psi_k)^2 dx = m^{2|\alpha|-d} \|\partial^\alpha \psi\|_{L^2}^2$
**Location:** sections/03-bump-family.tex.
**Content:** $\int_{R_k}(\partial^\alpha \psi_k)^2 = m^{2|\alpha|} \cdot m^{-d} \|\partial^\alpha\psi\|_{L^2}^2$.
**Current tag:** 🟢 verified
**Verification method:** Substitute $y = m(x - z_k)$, Jacobian $|\det dy/dx| = m^d$ so $dx = m^{-d} dy$. The image of $R_k$ is $[0,1)^d$ (closure $[0,1]^d$), $\psi$ supported in $(0,1)^d$ has zero boundary contribution. Combined with the $m^{2|\alpha|}$ from chain rule gives $m^{2|\alpha|-d}$. Matches digest in `bump-construction.md`.
**Sub-agent task id:** none

### Step 3 — disjoint supports collapse the cross terms in $\|f_\omega\|_{W^s_2}^2$
**Location:** sections/03-bump-family.tex, Eq.~\eqref{eq:f-omega-sob}.
**Content:** $\|f_\omega\|_{W^s_2}^2 = (c_\psi^2/m^{2s}) \sum_{|\alpha|\leq s} \sum_k \omega_k^2 \int_{R_k} (\partial^\alpha \psi_k)^2$.
**Current tag:** 🟢 verified
**Verification method:** Disjoint supports + $\omega_k \in \{0,1\}$ ⇒ pairwise products $\omega_j \omega_k \psi_j \psi_k = 0$ a.e. Hence the Sobolev seminorm of the sum equals the sum of seminorms.
**Sub-agent task id:** none

### Step 4 — bounding $m^{2|\alpha|-d} \leq m^{2s-d}$
**Location:** sections/03-bump-family.tex, just below \eqref{eq:f-omega-sob}.
**Content:** For each $|\alpha| \leq s$, $m^{2|\alpha|-d} \leq m^{2s-d}$ since $m \geq 1$.
**Current tag:** 🟢 verified
**Verification method:** Monotonicity of $m^t$ in $t$ for $m \geq 1$.
**Sub-agent task id:** none

### Step 5 — final $\|f_\omega\|_{W^s_2}^2 \leq c_\psi^2 g_\psi^2 = 1$
**Location:** sections/03-bump-family.tex.
**Content:** $\|f_\omega\|_{W^s_2}^2 \leq (c_\psi^2/m^{2s}) \cdot m^d \cdot m^{2s-d} \cdot g_\psi^2 = c_\psi^2 g_\psi^2 = 1$.
**Current tag:** 🟡 cross-checked (matches digest)
**Verification method:** Algebraic combination of steps 3, 4 with $c_\psi = 1/g_\psi$. **Note**: the bound on $\sum_{|\alpha|\leq s} m^{2|\alpha|-d} \|\partial^\alpha\psi\|_{L^2}^2 \leq m^{2s-d} \sum_{|\alpha|\leq s} \|\partial^\alpha\psi\|_{L^2}^2 = m^{2s-d} g_\psi^2$. This collapse uses upper bound, so the final bound is $\leq$ not $=$, consistent. Cross-checked against bump-construction.md.
**Sub-agent task id:** none

### Step 6 — $L^2$ separation: $\|f_\omega - f_{\omega'}\|_{L^2}^2 = (c_\psi^2/m^{2s}) m^{-d} \|\psi\|_{L^2}^2 \rho_H(\omega,\omega')$
**Location:** sections/03-bump-family.tex, part (ii).
**Content:** Direct computation via disjoint supports.
**Current tag:** 🟢 verified
**Verification method:** Disjoint supports give $\|h\|_{L^2}^2 = \sum_k (\omega_k - \omega_k')^2 \int (\psi_k)^2 = \sum_k (\omega_k - \omega_k')^2 \cdot m^{-d} \|\psi\|_{L^2}^2$. $\sum_k (\omega_k - \omega'_k)^2 = \rho_H$ for $\{0,1\}$ entries. Matches bump-construction.md.
**Sub-agent task id:** none

### Step 7 — $L^\infty$ bound
**Location:** sections/03-bump-family.tex, part (iii).
**Content:** $\|f_\omega - f_{\omega'}\|_\infty \leq (c_\psi/m^s) \|\psi\|_\infty$.
**Current tag:** 🟢 verified
**Verification method:** Each point lies in at most one $R_k$, so at most one summand is nonzero, bounded by $\|\psi\|_\infty$.
**Sub-agent task id:** none

---

## Lemma 4.1 (KL-bound) — sections/04-kl-bound.tex

### Step 8 — invoking Fact 1.4 (Gaussian KL) with $g \equiv 0$
**Location:** sections/04-kl-bound.tex, Eq.~\eqref{eq:kl-step1}.
**Content:** $KL(P_{f_\omega} \| P_{f_0}) = \frac{1}{2\sigma^2} \sum_i f_\omega(x_i)^2$.
**Current tag:** 🟡 cross-checked
**Verification method:** Direct substitution into Fact 1.4 (gaussian-kl-fixed-design.md digest). $g \equiv 0$ ⇒ $f - g = f_\omega$.
**Sub-agent task id:** none

### Step 9 — disjoint-support claim: $f_\omega(x_i) = (c_\psi/m^s) \omega_{k(i)} \psi_{k(i)}(x_i)$
**Location:** sections/04-kl-bound.tex.
**Content:** For each $i$, only the $\psi_{k(i)}$ with $x_i \in R_{k(i)}$ is nonzero.
**Current tag:** 🟢 verified
**Verification method:** Cells partition $[0,1]^d$; each $x_i$ in exactly one cell; bump supports are disjoint.
**Sub-agent task id:** none

### Step 10 — partition sum $\sum_i f_\omega(x_i)^2 = (c_\psi^2/m^{2s}) \sum_k \omega_k^2 \sum_{i: x_i \in R_k} \psi_k(x_i)^2$
**Location:** sections/04-kl-bound.tex.
**Content:** Partition of sum by cell index.
**Current tag:** 🟢 verified
**Verification method:** Direct from Step 9 by grouping the indices $i$ by their cell $k(i)$.
**Sub-agent task id:** none

### Step 11 — Balance bound: $|\{i: x_i \in R_k\}| \leq C_{\msf{bal}} n/m^d$ and combination
**Location:** sections/04-kl-bound.tex, Eq.~\eqref{eq:kl-step2}.
**Content:** Substituting balance into the previous bound: $\leq (c_\psi^2 \|\psi\|_\infty^2 / m^{2s}) m^d (C_{\msf{bal}} n / m^d) = C_{\msf{bal}} c_\psi^2 \|\psi\|_\infty^2 n / m^{2s}$.
**Current tag:** 🟢 verified
**Verification method:** Direct algebraic. $m^d \cdot (n/m^d) = n$. The $\sum_k \omega_k^2 \leq m^d$ uses $\omega_k \leq 1$, and the $|\{i: x_i\in R_k\}| \leq C_{\msf{bal}} n/m^d$ comes from balance.
**Sub-agent task id:** none

### Step 12 — Final KL bound assembly
**Location:** sections/04-kl-bound.tex, Eq.~\eqref{eq:kl-bound} & Step 3 of proof.
**Content:** $KL \leq C_{\msf{KL}} n / (\sigma^2 m^{2s})$ with $C_{\msf{KL}} = \tfrac{1}{2} c_\psi^2 \|\psi\|_\infty^2 C_{\msf{bal}}$.
**Current tag:** 🟢 verified
**Verification method:** Plug step 11 into step 8 and simplify.
**Sub-agent task id:** none

---

## Lemma 5.2 (probability lower bound) — sections/05-fano-application.tex

### Step 13 — $M \geq 2^{m^d/8} - 1$ from Fact 1.3 (VG)
**Location:** sections/05-fano-application.tex, Eq.~\eqref{eq:M-lb}.
**Content:** Direct from VG with $K = m^d \geq 8$. $|\Hpack| = M + 1 \geq 2^{m^d/8}$ so $M \geq 2^{m^d/8} - 1$.
**Current tag:** 🟡 cross-checked
**Verification method:** Match to varshamov-gilbert.md digest. $K = m^d$, hypothesis $K \geq 8$ ensured by precondition.
**Sub-agent task id:** none

### Step 14 — $\log M \geq (m^d/16) \log 2$ when $m^d \geq 16/\log 2$
**Location:** sections/05-fano-application.tex.
**Content:** From $M \geq 2^{m^d/8} - 1$, $\log M \geq (m^d/8)\log 2 - O(1)$, and we collapse the $O(1)$ into the constant by demanding $m^d \geq 16/\log 2 \approx 23$.
**Current tag:** 🔴 from-memory ⇒ 🟢 verified (hand-check below)
**Verification method:** **Hand-check.** $M \geq 2^{m^d/8} - 1$ ⇒ $\log M \geq \log(2^{m^d/8} - 1)$. For $m^d \geq 16/\log 2$, $2^{m^d/8} \geq e^2 \approx 7.39$, so $2^{m^d/8} - 1 \geq (1/2) \cdot 2^{m^d/8}$ (since $1 \leq 2^{m^d/8}/2$ when $2^{m^d/8} \geq 2$, true for $m^d \geq 8$). Hence $\log M \geq (m^d/8) \log 2 - \log 2 = (m^d/8) \log 2 (1 - 8/m^d) \geq (m^d/8) \log 2 \cdot (1/2) = (m^d/16) \log 2$ for $m^d \geq 16$. ✓
**Sub-agent task id:** none

### Step 15 — Separation $\|f_{\omega^{(j)}} - f_{\omega^{(k)}}\|_{L^2}^2 \geq (c_\psi^2 \|\psi\|_{L^2}^2 / 8) m^{-2s}$
**Location:** sections/05-fano-application.tex, Eq.~\eqref{eq:sep-direct}.
**Content:** Apply Lemma 3.1(ii) with $\rho_H \geq m^d/8$ from VG.
**Current tag:** 🟢 verified
**Verification method:** Direct substitution. $c_\psi^2 \|\psi\|_{L^2}^2 m^{-(2s+d)} \cdot (m^d/8) = c_\psi^2 \|\psi\|_{L^2}^2 m^{-2s} / 8$. Hypotheses of Lemma 3.1(ii) (no extra) trivially satisfied.
**Sub-agent task id:** none

### Step 16 — Definition of $\rho = c_\rho m^{-s}$ with $c_\rho = c_\psi \|\psi\|_{L^2}/(2\sqrt{8})$
**Location:** sections/05-fano-application.tex, Eq.~\eqref{eq:rho-def}.
**Content:** $\rho := \frac{1}{2} \cdot \sqrt{c_\psi^2 \|\psi\|_{L^2}^2 / 8} \cdot m^{-s}$, so $2\rho = \sqrt{c_\psi^2 \|\psi\|_{L^2}^2 / 8} m^{-s}$. Hence $\|f_j - f_k\|_{L^2} \geq 2\rho$.
**Current tag:** 🟢 verified
**Verification method:** Direct: $\|f_j - f_k\|_{L^2}^2 \geq (c_\psi \|\psi\|_{L^2})^2 m^{-2s}/8$ gives $\|f_j - f_k\|_{L^2} \geq (c_\psi \|\psi\|_{L^2})/\sqrt{8} \cdot m^{-s} = 2\rho$ with $\rho = c_\psi\|\psi\|_{L^2}/(2\sqrt 8) m^{-s}$. ✓
**Sub-agent task id:** none

### Step 17 — KL inequality with hypothesis Eq.~\eqref{eq:m-condition}
**Location:** sections/05-fano-application.tex.
**Content:** $KL \leq (C_{\msf{KL}} n)/(\sigma^2 m^{2s}) = C_{\msf{KL}} m^d \cdot n/(\sigma^2 m^{2s+d}) \leq \alpha_\star C_{\msf{KL}} m^d$.
**Current tag:** 🟢 verified
**Verification method:** Trivial algebra: multiply and divide by $m^d$.
**Sub-agent task id:** none

### Step 18 — Averaged KL $\leq (1/8) \log M$
**Location:** sections/05-fano-application.tex, Eq.~\eqref{eq:kl-alpha}.
**Content:** Avg KL $\leq \alpha_\star C_{\msf{KL}} m^d \leq \alpha_\star C_{\msf{KL}} (16/\log 2) \log M$.
**Current tag:** 🟡 cross-checked (then 🟢 by hand-check)
**Verification method:** Using Step 14 ($\log M \geq (m^d/16)\log 2$ ⇒ $m^d \leq 16\log M / \log 2$). Plugging $\alpha_\star = \log 2 / (128 C_{\msf{KL}})$: $\alpha_\star C_{\msf{KL}} \cdot 16/\log 2 = 16/128 = 1/8$. ✓ Note the text revises $\alpha_\star$ to $\log 2/(256 C_{\msf{KL}})$ which gives $1/16$. Both work.
**Sub-agent task id:** none

### Step 19 — Numerical Fano constants: $1 - 2\alpha - \sqrt{2\alpha/\log M} \geq 0.45$ for $\alpha = 1/16$, $\log M \geq \log 2$
**Location:** sections/05-fano-application.tex, Eq.~\eqref{eq:fano-numerical}.
**Content:** Plug $\alpha = 1/16$: $1 - 1/8 = 7/8 = 0.875$. $\sqrt{2 \cdot (1/16)/\log M} = \sqrt{1/(8 \log M)} \leq \sqrt{1/(8 \log 2)} \approx \sqrt{0.180} \approx 0.425$. Difference $\approx 0.45$. Halved by $\sqrt M/(1+\sqrt M) \geq 1/2$ ⇒ final $\geq 0.225$.
**Current tag:** 🟢 verified
**Verification method:** Hand-check arithmetic. $1/(8 \log 2) = 1/(8 \cdot 0.693) \approx 0.180$, $\sqrt{0.180} \approx 0.4250$. $7/8 - 0.425 = 0.45$. Half is $0.225$. Set $c_{\msf{prob}} = 0.22$. ✓
**Sub-agent task id:** none

---

## Theorem 2.1 (main) — sections/06-proof-of-thm.tex

### Step 20 — Markov gives $\E\|\hat f - f_\omega\|^2 \geq \rho^2 P(\|\hat f - f_\omega\| \geq \rho)$
**Location:** sections/06-proof-of-thm.tex, Eq.~\eqref{eq:markov}.
**Content:** For $Z = \|\hat f - f_\omega\|^2 \geq 0$ and event $\{Z \geq \rho^2\}$: $\E Z \geq \rho^2 P(Z \geq \rho^2)$.
**Current tag:** 🟢 verified
**Verification method:** Textbook Markov for non-negative RVs.
**Sub-agent task id:** none

### Step 21 — Inclusion $\Hpack \subseteq \Sobball$
**Location:** sections/06-proof-of-thm.tex, first inequality in Eq.~\eqref{eq:risk-to-prob}.
**Content:** Each $f_\omega$ for $\omega \in \Hpack$ has $\|f_\omega\|_{W^s_2} \leq 1$.
**Current tag:** 🟢 verified
**Verification method:** Direct from Lemma 3.1(i).
**Sub-agent task id:** none

### Step 22 — Scalar pull-out: $\inf \sup [c \cdot a_\omega] = c \inf \sup a_\omega$ for $c \geq 0$
**Location:** sections/06-proof-of-thm.tex.
**Content:** Elementary identity.
**Current tag:** 🟢 verified
**Verification method:** $c$ is a function of $m, n$ only, independent of $\fhat$ and $\omega$.
**Sub-agent task id:** none

### Step 23 — Choice of $m = \lfloor (\alpha_\star \sigma^2 n)^{1/(2s+d)} \rfloor$ satisfies hypothesis
**Location:** sections/06-proof-of-thm.tex, Eq.~\eqref{eq:m-choice}.
**Content:** From $m \leq (\alpha_\star \sigma^2 n)^{1/(2s+d)}$, $m^{2s+d} \leq \alpha_\star \sigma^2 n$, so $n/(\sigma^2 m^{2s+d}) \leq \alpha_\star$ if $\sigma^2 > 0$ (which holds).
**Current tag:** 🟢 verified
**Verification method:** Rearrange algebra.
**Sub-agent task id:** none

### Step 24 — Rate assembly: $m^{-2s} \geq (\alpha_\star \sigma^2 n)^{-2s/(2s+d)} = c_n n^{-2s/(2s+d)}$
**Location:** sections/06-proof-of-thm.tex, Eq.~\eqref{eq:m-lower}.
**Content:** $m \leq (\alpha_\star \sigma^2 n)^{1/(2s+d)}$ ⇒ $m^{-2s} \geq (\alpha_\star \sigma^2 n)^{-2s/(2s+d)}$.
**Current tag:** 🟢 verified
**Verification method:** Monotonicity: $m \leq x$ ⇒ $m^{-2s} \geq x^{-2s}$ for $m, x > 0$.
**Sub-agent task id:** none

### Step 25 — Final constant assembly
**Location:** sections/06-proof-of-thm.tex.
**Content:** $\mathfrak{M}_n \geq c_\rho^2 c_{\msf{prob}} (\alpha_\star \sigma^2)^{-2s/(2s+d)} n^{-2s/(2s+d)} = c_{\msf{lb}} n^{-2s/(2s+d)}$.
**Current tag:** 🟢 verified
**Verification method:** Direct algebraic combination of steps 20, 21, 22, 24 and Lemma 5.2 (which provided $c_{\msf{prob}}$).
**Sub-agent task id:** none

---

## Summary

| Tag | Count |
|---|---|
| 🟢 verified | 21 |
| 🟡 cross-checked | 4 |
| 🔴 from-memory | 0 |

All 25 enumerated derivation steps reached at least 🟡; 21 are 🟢. No 🔴 remain. No `\todo{}` markers needed in `.tex`. No sub-agents fired (every step was fast-path verifiable via hand-check, digest match, or project lemma match).

Sweep complete. Proceeding to Phase D.
