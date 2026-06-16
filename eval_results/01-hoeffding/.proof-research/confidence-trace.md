# Confidence trace — Hoeffding's inequality (Phase C.5)

Scope = Standard ⇒ sweep MANDATORY. Every derivation step below started at
🔴 `from-memory` and was upgraded via a fast path (named textbook inequality →
🟢; digest / project-lemma match → 🟡) or hand re-derivation (🟢). No step
remained 🔴, so no `\todo{verify}` markers were required by the sweep. The three
`\todo{user-decision: ...}` markers in the source are intake decisions
(Phase A.1a), not unverified steps.

Termination: all steps ≥ 🟡; no `conclusion-differs`; no `constants-differ`.
Proceed to Phase D (handled by the independent panel).

---

## Step 1
**Location:** sections/01-hoeffding-lemma.tex:33
**Content (≤ 2 lines):** $\psi(0)=\log\E[e^0]=\log 1=0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Elementary: $e^0=1$, $\E[1]=1$, $\log 1=0$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 2
**Location:** sections/01-hoeffding-lemma.tex:34
**Content (≤ 2 lines):** $\psi'(\lambda)=\E[Ye^{\lambda Y}]/\E[e^{\lambda Y}]$ and $\psi'(0)=\E[Y]/\E[1]=0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Differentiate $\log\E[e^{\lambda Y}]$ (chain rule, differentiation under the expectation valid since $Y$ bounded); evaluate at $0$ with $\E[Y]=0$. Hand-checked; matches .proof-research/hoeffding-lemma.md §Step 1.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 3
**Location:** sections/01-hoeffding-lemma.tex:44
**Content (≤ 2 lines):** $\psi''(\lambda)=\E_{Q_\lambda}[Y^2]-(\E_{Q_\lambda}[Y])^2=\Var_{Q_\lambda}(Y)$ via the tilted law.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Quotient rule on $\psi'$; the two ratios are $\E_{Q_\lambda}[Y^2]$ and $\E_{Q_\lambda}[Y]$ under the exponential tilt $dQ_\lambda\propto e^{\lambda Y}dP$. Matches .proof-research/hoeffding-lemma.md §Step 2 (standard cumulant-generating-function identity, Boucheron–Lugosi–Massart Lemma 2.2).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 4
**Location:** sections/01-hoeffding-lemma.tex:60
**Content (≤ 2 lines):** $\Var_{Q_\lambda}(Y)=\E[(Y-\E Y)^2]\le\E[(Y-m)^2]$ with $m=(a+b)/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** The mean minimises mean-square deviation: $\E[(Y-c)^2]=\Var(Y)+(\E Y-c)^2\ge\Var(Y)$ for any constant $c$. Named textbook fact; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 5
**Location:** sections/01-hoeffding-lemma.tex:63
**Content (≤ 2 lines):** $\E[(Y-m)^2]\le((b-a)/2)^2=(b-a)^2/4$ (Popoviciu / variance-of-bounded-RV).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Pointwise $|Y-m|\le(b-a)/2$ for $Y\in[a,b]$, $m$ the midpoint ⇒ $\E[(Y-m)^2]\le(b-a)^2/4$. Hand-checked; equality at the two-point $\{a,b\}$ law confirms sharpness. Matches digest §Step 3.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 6
**Location:** sections/01-hoeffding-lemma.tex:76
**Content (≤ 2 lines):** $\psi(\lambda)=\psi(0)+\lambda\psi'(0)+\tfrac{\lambda^2}{2}\psi''(\xi)$, Taylor with Lagrange remainder, $\xi$ between $0$ and $\lambda$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Second-order Taylor with Lagrange remainder; valid as $\psi\in C^\infty(\R)$ ($Y$ bounded ⇒ MGF entire). Named textbook theorem; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 7
**Location:** sections/01-hoeffding-lemma.tex:78
**Content (≤ 2 lines):** $\psi(\lambda)=\tfrac{\lambda^2}{2}\psi''(\xi)\le\tfrac{\lambda^2}{2}\cdot\tfrac{(b-a)^2}{4}=\tfrac{\lambda^2(b-a)^2}{8}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute $\psi(0)=\psi'(0)=0$ (Steps 1–2) and the variance bound (Steps 4–5: $\psi''\le(b-a)^2/4$). Arithmetic: $\tfrac12\cdot\tfrac14=\tfrac18$. Hand-checked; this is the sharp $(b-a)^2/8$ proxy (intake Q2).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 8
**Location:** sections/02-hoeffding-theorem.tex:31
**Content (≤ 2 lines):** $\Pr[S_n-\E S_n\ge t]=\Pr[e^{\lambda(S_n-\E S_n)}\ge e^{\lambda t}]$ for $\lambda>0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $x\mapsto e^{\lambda x}$ is a strictly increasing bijection for $\lambda>0$, so the event is preserved. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 9
**Location:** sections/02-hoeffding-theorem.tex:33
**Content (≤ 2 lines):** $\le e^{-\lambda t}\E[e^{\lambda\sum_i Y_i}]$ by Markov's inequality.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Markov $\Pr[Z\ge s]\le\E[Z]/s$ on $Z=e^{\lambda(S_n-\E S_n)}\ge0$, $s=e^{\lambda t}$. Named textbook inequality; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 10
**Location:** sections/02-hoeffding-theorem.tex:34
**Content (≤ 2 lines):** $\E[e^{\lambda\sum_i Y_i}]=\prod_i\E[e^{\lambda Y_i}]$ by independence.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $e^{\lambda Y_i}$ are independent (measurable functions of independent $Y_i$); expectation of a product of independent nonnegative variables factorises. Named textbook fact; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 11
**Location:** sections/02-hoeffding-theorem.tex:50
**Content (≤ 2 lines):** $\prod_i\E[e^{\lambda Y_i}]\le\prod_i\exp(\lambda^2(b_i-a_i)^2/8)=\exp(\lambda^2 V/8)$ via Hoeffding's lemma.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Each $Y_i=X_i-\E X_i$ is centered with $Y_i\in[a_i',b_i']$, $b_i'-a_i'=b_i-a_i$; hypotheses of \Cref{lem:hoeffding} verified at the cite-site. Product of exponentials sums the exponents, $\sum_i(b_i-a_i)^2=V$. Cross-checked against lem:hoeffding (Eq.~eq:hoeffding-lemma).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 12
**Location:** sections/02-hoeffding-theorem.tex:59
**Content (≤ 2 lines):** First-order condition $g'(\lambda)=-t+\lambda V/4=0\Rightarrow\lambda^\star=4t/V$; $g''=V/4>0$ confirms global min.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $g(\lambda)=-\lambda t+\lambda^2 V/8$, $g'(\lambda)=-t+\lambda V/4$; set $=0$. Convexity ($g''=V/4>0$) ⇒ unique global minimiser. Hand-checked (explicit first-order condition; no phantom optimization).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 13
**Location:** sections/02-hoeffding-theorem.tex:67
**Content (≤ 2 lines):** $g(\lambda^\star)=-\tfrac{4t}{V}t+\tfrac18(\tfrac{4t}{V})^2V=-\tfrac{4t^2}{V}+\tfrac{2t^2}{V}=-\tfrac{2t^2}{V}$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Independent hand re-derivation: term 1 $=-4t^2/V$; term 2 $=(16t^2/V^2)(V/8)=2t^2/V$; sum $=-2t^2/V$. Matches the source exactly. This is the load-bearing arithmetic producing the leading exponent constant.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 14
**Location:** sections/02-hoeffding-theorem.tex:85
**Content (≤ 2 lines):** Lower tail: apply one-sided bound to $-X_i\in[-b_i,-a_i]$ ⇒ $\Pr[S_n-\E S_n\le-t]\le\exp(-2t^2/V)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $-X_i$ has interval width $(-a_i)-(-b_i)=b_i-a_i$, so $V$ is unchanged; centered sum negates. Symmetric application of Eq.~eq:one-sided. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z

## Step 15
**Location:** sections/02-hoeffding-theorem.tex:93
**Content (≤ 2 lines):** Union bound: $\Pr[|S_n-\E S_n|\ge t]\le\Pr[\,\ge t\,]+\Pr[\,\le-t\,]\le2\exp(-2t^2/V)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\{|S_n-\E S_n|\ge t\}=\{S_n-\E S_n\ge t\}\cup\{S_n-\E S_n\le-t\}$; subadditivity of $\Pr$ over the two events; substitute both one-sided bounds (Steps 13–14). Named textbook fact (union bound); hand-checked. Produces the leading factor $2$.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T00:00:00Z
