# Confidence trace — VC generalization bound (Phase C.5)

Tag taxonomy: 🔴 from-memory · 🟡 cross-checked (digest / lemma match) ·
🟢 verified (textbook inequality hand-checked, or independent re-derivation).
All steps initialized 🔴, then upgraded. Final summary at the bottom.

Sweep date: 2026-06-08T20:56:06Z.

---

## Step 1
**Location:** sections/01-preliminaries.tex:88
**Content (≤ 2 lines):** The coordinatewise map $\psi$ is a bijection of
$\{0,1\}^m$ (identity if $y_i=0$, bit-flip if $y_i=1$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-checked: $b\mapsto 1-b$ and $b\mapsto b$ are both
bijections of $\{0,1\}$; a product of coordinatewise bijections is a bijection.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 2
**Location:** sections/01-preliminaries.tex:96
**Content (≤ 2 lines):** $\abs{\Lcal_{|(z_i)}}=\abs{\Hcal_{|(x_i)}}\le
\Growth_\Hcal(m)$, hence $\Growth_\Lcal(m)\le\Growth_\Hcal(m)$ and
$\VC(\Lcal)\le d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** A bijection preserves cardinality of images; max over
$z$ gives the growth-function inequality; a shattered $\Lcal$-set pulls back to a
shattered $\Hcal$-set of equal size. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 3
**Location:** sections/02-mcdiarmid-deviation.tex:30
**Content (≤ 2 lines):** Changing one example changes $\Riskhat_n(h)$ by
$\le 1/n$ (indicators in $\{0,1\}$, normalization $1/n$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\frac1n|\1\{\cdot\}-\1\{\cdot\}|\le\frac1n$ since each
indicator $\in\{0,1\}$; population risk is $S$-independent. Hand-checked;
matches `mcdiarmid.md` ($c_i=1/n$).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 4
**Location:** sections/02-mcdiarmid-deviation.tex:39
**Content (≤ 2 lines):** $|\Phi(S)-\Phi(S')|\le\sup_h|a(h)-b(h)|\le 1/n$, i.e.
bounded differences with $c_i=1/n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook fact $|\sup f-\sup g|\le\sup|f-g|$, then
reverse triangle inequality $|a(h)-b(h)|\le|\Riskhat_S-\Riskhat_{S'}|\le1/n$.
Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 5
**Location:** sections/02-mcdiarmid-deviation.tex:51
**Content (≤ 2 lines):** McDiarmid tail
$\Pr[\Phi-\E\Phi\ge t]\le\exp(-2t^2/\sum_i c_i^2)=\exp(-2nt^2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Hypotheses (independence, bounded differences $c_i=1/n$,
$\sum c_i^2=1/n$) match `mcdiarmid.md` / `cite-boucheron2013concentration-ci.md`
Thm 6.2 and `cite-wainwright2019high-hds.md` Cor 2.21. Constant $2$ in exponent
verified against digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 6
**Location:** sections/02-mcdiarmid-deviation.tex:57
**Content (≤ 2 lines):** Invert tail: set $e^{-2nt^2}=\delta\Rightarrow
t=\sqrt{\log(1/\delta)/(2n)}$; gives the $1-\delta$ bound.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebra: $-2nt^2=\log\delta\Rightarrow
t^2=\log(1/\delta)/(2n)$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 7
**Location:** sections/03-symmetrization.tex:24
**Content (≤ 2 lines):** (a) $\Dcal\ell=\E_{S'}\widehat\Dcal_n'\ell$ and
$\widehat\Dcal_n\ell=\E_{S'}\widehat\Dcal_n\ell$, rewriting the deviation.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Ghost sample i.i.d.\ $\sim\Dcal$ so its empirical mean
is unbiased for $\Dcal\ell$; $\widehat\Dcal_n\ell$ is $S'$-free so equals its own
$\E_{S'}$. Hand-checked; matches `symmetrization.md` step (i).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 8
**Location:** sections/03-symmetrization.tex:29
**Content (≤ 2 lines):** (b) Jensen: $|\E_{S'}(\cdot)|\le\E_{S'}|\cdot|$ and
$\sup\E_{S'}\le\E_{S'}\sup$, pulling $\E_{S'}$ out.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Convexity of $|\cdot|$ and of $\sup$ (pointwise max of
affine) ⇒ Jensen. Textbook. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 9
**Location:** sections/03-symmetrization.tex:34
**Content (≤ 2 lines):** (c) Insert Rademacher signs: $\ell(z_i')-\ell(z_i)$ is
symmetric, so $\sigma_i(\cdot)$ has the same law; expectation unchanged.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Symmetrization identity; the swap
$z_i\leftrightarrow z_i'$ is a measure-preserving involution and $\sigma_i$ is
independent. Matches `symmetrization.md` step (ii) /
`cite-mohri2018foundations-foml.md` Lemma 3.4.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 10
**Location:** sections/03-symmetrization.tex:38
**Content (≤ 2 lines):** (d) Triangle-split the sign sum into two Rademacher
averages, each $=\Rad_n(\Lcal)$; total $\le 2\Rad_n(\Lcal)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $|\sum\sigma_i(\ell(z_i')-\ell(z_i))|\le
|\sum\sigma_i\ell(z_i')|+|\sum\sigma_i\ell(z_i)|$; $-\sigma_i\overset d=\sigma_i$;
$S'$ indep copy of $S$ ⇒ both averages equal $\Rad_n(\Lcal)$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 11
**Location:** sections/04-sauer-massart.tex:27
**Content (≤ 2 lines):** Pajor claim $|\Hcal_{|C}|\le|\{B\subseteq C:\Hcal
\text{ shatters }B\}|$ (statement of the strengthened induction target).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** This is the standard Pajor strengthening used by the
shifting proof; matches `sauer-shelah.md` and `cite-shalev2014understanding-uml.md`
Lemma 6.10.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 12
**Location:** sections/04-sauer-massart.tex:30
**Content (≤ 2 lines):** No $B$ with $|B|>d$ shattered ⇒ RHS of Pajor
$\le\sum_{i\le d}\binom mi$ ⇒ Eq.(sauer).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Counting: number of subsets of an $m$-set of size $\le d$
is $\sum_{i=0}^d\binom mi$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 13
**Location:** sections/04-sauer-massart.tex:35
**Content (≤ 2 lines):** Shifting induction: $T_x$ injective (cardinality
preserved); partition by restriction to $C'$; both groups counted by shattered
subsets; base case $m=0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Downward-shifting argument; hypotheses and bookkeeping
match `sauer-shelah.md` (Pajor/shifting) and `cite-shalev2014understanding-uml.md`
Lemma 6.10 proof. Combinatorial step (R19-ignored proof).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 14
**Location:** sections/04-sauer-massart.tex:57
**Content (≤ 2 lines):** $(d/m)^d\sum_{i\le d}\binom mi\le\sum_{i\le d}\binom mi
(d/m)^i\le(1+d/m)^m\le e^d$, valid for $m\ge d$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $(d/m)^d\le(d/m)^i$ for $i\le d$ since $d/m\le1$;
binomial theorem $\sum_{i\le m}\binom mi t^i=(1+t)^m$ with $t=d/m$; $1+t\le e^t$.
Hand-checked; gives $\sum_{i\le d}\binom mi\le(em/d)^d$.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 15
**Location:** sections/04-sauer-massart.tex:82
**Content (≤ 2 lines):** $|A|=|\Lcal_{|S}|\le\Growth_\Lcal(n)\le\Growth_\Hcal(n)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of growth function (max over samples) +
Fact (loss-vc, Step 2). Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 16
**Location:** sections/04-sauer-massart.tex:89
**Content (≤ 2 lines):** Massart core:
$\E_\sigma\max_{a\in A}\sum_i\sigma_i a_i\le r\sqrt{2\log|A|}$, $r=\max\|a\|_2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Hypotheses (finite $A$, radius $r$, Rademacher signs)
and constant $\sqrt2$ match `massart.md` / `cite-mohri2018foundations-foml.md`
Thm 3.7 and `cite-shalev2014understanding-uml.md` Lemma 26.8.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 17
**Location:** sections/04-sauer-massart.tex:94
**Content (≤ 2 lines):** $\Radhat_S(\Lcal)=\frac1n\E_\sigma\max\ldots
\le\frac{r\sqrt{2\log|A|}}{n}\le\sqrt{2\log\Growth_\Hcal(n)/n}$ using
$r\le\sqrt n$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** (a) Massart core (Step 16); (b) $a\in\{0,1\}^n\Rightarrow
\|a\|_2=\sqrt{\#\text{ones}}\le\sqrt n$, and $|A|\le\Growth_\Hcal(n)$.
$\frac{\sqrt n\sqrt{2\log N}}{n}=\sqrt{2\log N/n}$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 18
**Location:** sections/04-sauer-massart.tex:103
**Content (≤ 2 lines):** Take $\E_S$ (bound holds per-sample) ⇒
$\Rad_n(\Lbar)\le\sqrt{2\log(2\Growth_\Hcal(n))/n}$; Sauer–Shelah $\Rightarrow
\le\sqrt{2(d\log(en/d)+\log 2)/n}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Per-sample inequality + monotonicity of $\E_S$;
$\log\Growth_\Hcal(n)\le d\log(en/d)$ from Step 14 with $m=n\ge d$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 19
**Location:** sections/05-main-theorem.tex:30
**Content (≤ 2 lines):** Event $\Ecal$ with $\Pr[\Ecal]\ge1-\delta$ (McDiarmid);
single stochastic step ⇒ union bound over $\Ecal$ alone covers budget $\delta$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct from Lemma mcdiarmid-dev (Steps 5–6); the other
three lemmas are deterministic, so no additional union terms. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 20
**Location:** sections/05-main-theorem.tex:46
**Content (≤ 2 lines):** (a)$\to$(c): $\Phi\le\E\Phi+\sqrt{\log(1/\delta)/2n}
\le2\Rad_n(\Lbar)+\ldots\le2\sqrt{2(d\log(en/d)+\log 2)/n}+\ldots$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** (a) def of $\Ecal$ (Step 19); (b) Lemma symmetrization
(Step 10); (c) Lemma massart-rademacher (Step 18). All three are prior project
lemmas whose hypotheses hold at this cite-site. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 21
**Location:** sections/05-main-theorem.tex:53
**Content (≤ 2 lines):** (d) collect $1/\sqrt n$, inflate $\log 2$ into
$d\log(en/d)$ ($2\sqrt2\to4$); (e) $4\sqrt u+\sqrt v\le\sqrt{17}\sqrt{u+v}$
(Cauchy–Schwarz in $\R^2$, $C_0=\sqrt{17}$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** (d) $d\log(en/d)+\log 2\le2d\log(en/d)$ since
$d\log(en/d)\ge d\ge1>\log 2$. (e) Cauchy–Schwarz $\alpha\sqrt u+\beta\sqrt v\le
\sqrt{\alpha^2+\beta^2}\sqrt{u+v}$; $\sqrt{4^2+1^2}=\sqrt{17}$.
Hand-checked (named textbook inequality).
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

## Step 22
**Location:** sections/05-main-theorem.tex:69
**Content (≤ 2 lines):** Final: $\Phi\le C\sqrt{(d\log(en/d)+\log(1/\delta))/n}
=C\sqrt{(d\log(n/d)+d+\log(1/\delta))/n}$ w.p. $\ge1-\delta$, $C=\sqrt{17}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\log(en/d)=\log(n/d)+\log e=\log(n/d)+1$; substitution
exact. Probability transfer from Step 19. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-08T20:56:06Z

---

## Sweep summary
- **Steps enumerated:** 22
- **After sweep:** 🟢 16 / 🟡 6 / 🔴 0
- **Sub-agents fired:** 0 — every step closed by a named textbook inequality
  (hand-checked → 🟢) or a digest/lemma-hypothesis match (→ 🟡). No algebra chain
  collapsed >3 lines into one step, and no unverifiable numerical constant
  remained, so no fire-and-forget re-derivation was warranted.
- **🟡 (cross-checked, reviewer-priority) steps:** 5 (McDiarmid tail),
  9 (Rademacher symmetrization identity), 11 & 13 (Pajor/shifting),
  16 (Massart core) — all external classical results matched to citation digests
  rather than re-derived from first principles here.
- **🔴 remaining:** 0. No `\todo{verify}` markers required for unverified steps.
  (The two `\todo{}` markers in the .tex are `user-decision` records from the
  Socratic intake, not confidence-sweep failures.)
- **Termination:** success — every step at ≥ 🟡; no `conclusion-differs`,
  no >30% stall. Proceed to Phase D (independent panel).
