# Confidence trace — frankl-union-closed-gilmer (Phase C.5)

Every derivation step is enumerated and tagged. Upgrade paths used:
- 🟢 **verified** — named textbook inequality (concavity/Jensen, Markov,
  data-processing, max-entropy) hand-checked, OR independent numeric
  re-derivation matched (script `/tmp` run logged in runner-log; constants
  re-checked: OR-identity, Jensen, $0.9$-bound, $g$-min $=1.45$, Lemma 3,
  Markov $0.01/0.1$, $1.26/1.4=0.9$, $1.8\cdot0.9=1.62$, $\log_2 2 =1$).
- 🟡 **cross-checked** — matched against the Gilmer source digest
  `.proof-research/gilmer-entropy-method.md` (verbatim Lemmas 1–5 / Theorems
  1–2) or the Cover–Thomas digest.

No step remains 🔴: every step is either a named textbook fact (🟢) or a
verbatim digest match against Gilmer's published lemmas (🟡). Numerical
constants were independently script-verified (🟢).

---

## Step 1
**Location:** sections/03-single-variable-bounds.tex:7
**Content (≤ 2 lines):** $\Pr[\text{bit}\cupbit\text{bit}'=1]=1-(1-p)(1-p')=p+p'-pp'$ (OR of two independent bits).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Elementary inclusion–exclusion; independent numeric identity check passed.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 2
**Location:** sections/02-cond-entropy-monotone.tex:17
**Content (≤ 2 lines):** $I(X;f(Y))\le I(X;Y)$ by data processing on Markov chain $X\to Y\to f(Y)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (data-processing, \Cref{fac:data-processing}); Cover–Thomas digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 3
**Location:** sections/02-cond-entropy-monotone.tex:19
**Content (≤ 2 lines):** $H(X)-H(X\mid f(Y))\le H(X)-H(X\mid Y)$ via $I(X;W)=H(X)-H(X\mid W)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Textbook mutual-information identity; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 4
**Location:** sections/02-cond-entropy-monotone.tex:21
**Content (≤ 2 lines):** Cancel $H(X)$, rearrange to $H(X\mid Y)\le H(X\mid f(Y))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Elementary algebra; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 5
**Location:** sections/03-single-variable-bounds.tex:24
**Content (≤ 2 lines):** $\frac{\hb(p)+\hb(p')}{2}\le \hb(\frac{p+p'}{2})$ (concavity of $\hb$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Jensen / concavity (\Cref{fac:concavity}); numeric check over $[0,0.5]^2$ passed (0 violations).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 6
**Location:** sections/03-single-variable-bounds.tex:30
**Content (≤ 2 lines):** $p+p'-pp'=p+p'(1-p)\ge 0.9(p+p')$ on $[0,0.1]^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $1-p'\ge0.9$ on $[0,0.1]$; independent numeric check over $[0,0.1]^2$ passed (0 violations).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 7
**Location:** sections/03-single-variable-bounds.tex:39
**Content (≤ 2 lines):** $\frac{\hb(p+p'-pp')}{\frac12(\hb(p)+\hb(p'))}\ge \frac{\hb(0.9u)}{\hb(0.5u)}=g(u)$, $u=p+p'$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Combines Steps 5–6 with monotonicity of $\hb$ on $[0,1/2]$; matches Gilmer Lemma 2 digest.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 8
**Location:** sections/03-single-variable-bounds.tex:44
**Content (≤ 2 lines):** $\min_{u\in(0,0.2]} g(u)=g(0.2)=\hb(0.18)/\hb(0.10)=1.450\ldots>1.4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Independent numeric minimization: $g$-min $=1.4501$ at $u=0.2$ (matches Gilmer Figure-1 caption $1.496$ for the 2D function); script-verified.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 9
**Location:** sections/03-single-variable-bounds.tex:60
**Content (≤ 2 lines):** $p+p'-pp'=p\cdot1+(1-p)p'$ (convex combination of endpoints $1$ and $p'$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Algebraic identity; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 10
**Location:** sections/03-single-variable-bounds.tex:62
**Content (≤ 2 lines):** $\hb(p\cdot1+(1-p)p')\ge p\,\hb(1)+(1-p)\hb(p')=(1-p)\hb(p')$, using $\hb(1)=0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Concavity of $\hb$ + $\hb(1)=0$; Gilmer Lemma 3; numeric check over $[0,1]^2$ passed (0 violations).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 11
**Location:** sections/04-region-bounds.tex:27
**Content (≤ 2 lines):** Markov: $\Pr[p_C>0.1]\le \E[p_c]/0.1\le 0.01/0.1=0.1$, so $\Pr[\Cz]\ge0.9$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Markov's inequality (named); arithmetic $0.01/0.1=0.1$ script-verified.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 12
**Location:** sections/04-region-bounds.tex:41
**Content (≤ 2 lines):** $\Pr[\Cz]H(X\mid\Cz)=\Pr[\Cz]\E_{c\sim q_0}[\hb(p_c)]$ (conditional Bernoulli identity).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of conditional entropy of a Bernoulli; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 13
**Location:** sections/04-region-bounds.tex:42
**Content (≤ 2 lines):** Symmetrize: $\E_{c\sim q_0}[\hb(p_c)]=\E_{c,c'\sim q_0}[\tfrac12(\hb(p_c)+\hb(p_{c'}))]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** i.i.d. copies have equal expectation; elementary, hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 14
**Location:** sections/04-region-bounds.tex:43
**Content (≤ 2 lines):** Apply Lemma 2 pointwise: $\le \frac{\Pr[\Cz]}{1.4}\E_{c,c'\sim q_0}[\hb(p_c+p_{c'}-p_cp_{c'})]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:concavity-half} (proved here, Steps 5–8); hypotheses $p_c,p_{c'}\le0.1$ hold on $\Cz$. Matches Gilmer Lemma 4 chain.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 15
**Location:** sections/04-region-bounds.tex:44
**Content (≤ 2 lines):** $\E_{c,c'\sim q_0}[\hb(p_c+p_{c'}-p_cp_{c'})]=H(X\cupbit X'\mid\Cz,\Cz')$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Conditional independence given $\Cz,\Cz'$ makes the OR Bernoulli$(p_c+p_{c'}-p_cp_{c'})$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 16
**Location:** sections/04-region-bounds.tex:45
**Content (≤ 2 lines):** $\frac{\Pr[\Cz]}{1.4}\le \frac{\Pr[\Cz]^2}{1.26}$ since $\Pr[\Cz]\ge0.9=1.26/1.4$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $1.26/1.4=0.9$ script-verified; inequality $1/1.4\le\Pr[\Cz]/1.26$ follows.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 17
**Location:** sections/04-region-bounds.tex:73
**Content (≤ 2 lines):** Expand $2\Pr[\Cz,\Co']H(\cdots)=2\sum_{c\in\Cz,c'\in\Co}q(c)q(c')\hb(p_c+p_{c'}-p_cp_{c'})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Conditional-entropy expansion over product law; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 18
**Location:** sections/04-region-bounds.tex:75
**Content (≤ 2 lines):** $\ge 2\sum q(c)q(c')(1-p_c)\hb(p_{c'})$ by Lemma 3.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:concavity-mix} (Step 10) with $(p,p')=(p_c,p_{c'})$. Matches Gilmer Lemma 5 chain.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 19
**Location:** sections/04-region-bounds.tex:77
**Content (≤ 2 lines):** Factor the double sum into $(\sum_{c\in\Cz}q(c)(1-p_c))(\sum_{c'\in\Co}q(c')\hb(p_{c'}))$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Distributivity of the product sum; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 20
**Location:** sections/04-region-bounds.tex:79
**Content (≤ 2 lines):** $\ge 2(\sum_{c\in\Cz}q(c)\cdot0.9)\Pr[\Co]H(X\mid\Co)$ using $1-p_c\ge0.9$ and identifying the $\Co$-sum.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $p_c\le0.1\Rightarrow1-p_c\ge0.9$; conditional-entropy identity; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 21
**Location:** sections/04-region-bounds.tex:81
**Content (≤ 2 lines):** $=1.8\Pr[\Cz]\Pr[\Co]H(X\mid\Co)$, then $\ge1.62\Pr[\Co]H(X\mid\Co)$ via $\Pr[\Cz]\ge0.9$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\sum_{c\in\Cz}q(c)=\Pr[\Cz]$; $1.8\cdot0.9=1.62$ script-verified.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 22
**Location:** sections/05-key-lemma.tex:30
**Content (≤ 2 lines):** Region decomposition $H(X\cupbit X'\mid C,C')=T_1+T_2+T_3$ over $\Cz\sqcup\Co$ partition.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Law of total conditional entropy across the 4 region pairs; matches Gilmer Lemma 1 assembly (digest).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 23
**Location:** sections/05-key-lemma.tex:36
**Content (≤ 2 lines):** $T_2$ collects both mixed events (factor 2) by i.i.d. symmetry; $\Pr[\Cz,\Co']=\Pr[\Cz]\Pr[\Co]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Independence of the two copies + symmetry of OR; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 24
**Location:** sections/05-key-lemma.tex:45
**Content (≤ 2 lines):** $T_1\ge1.26\Pr[\Cz]H(X\mid\Cz)$, $T_2\ge1.62\Pr[\Co]H(X\mid\Co)$, $T_3\ge0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:region-low,lem:region-mix} (Steps 12–21); non-negativity of entropy. Matches Gilmer Lemma 1.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 25
**Location:** sections/05-key-lemma.tex:56
**Content (≤ 2 lines):** Sum + $1.62\ge1.26$ + total conditional entropy law $\Rightarrow H(X\cupbit X'\mid C,C')\ge1.26H(X\mid C)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $1.62\ge1.26$; $H(X\mid C)=\Pr[\Cz]H(X\mid\Cz)+\Pr[\Co]H(X\mid\Co)$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 26
**Location:** sections/06-main-theorem.tex:30
**Content (≤ 2 lines):** $H((A\cup B)_i\mid(A\cup B)_{<i})\ge H((A\cup B)_i\mid A_{<i},B_{<i})$ since $(A\cup B)_{<i}=f(A_{<i},B_{<i})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:cond-mono} (Steps 2–4). The crucial Eq. (2) of Gilmer; digest-matched.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 27
**Location:** sections/06-main-theorem.tex:32
**Content (≤ 2 lines):** $H((A\cup B)_i\mid A_{<i},B_{<i})=H(A_i\cupbit B_i\mid A_{<i},B_{<i})$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $(A\cup B)_i=A_i\cupbit B_i$ by definition; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 28
**Location:** sections/06-main-theorem.tex:33
**Content (≤ 2 lines):** $\ge1.26H(A_i\mid A_{<i})$ by the key lemma with $C=A_{<i},C'=B_{<i}$, marginal $\E[A_i]=\Pr[i\in A]\le0.01$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** \Cref{lem:single-var}; hypotheses checked ($A_{<i},B_{<i}$ i.i.d., conditional Bernoulli, marginal cap). Gilmer Eq. (3).
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 29
**Location:** sections/06-main-theorem.tex:42
**Content (≤ 2 lines):** Chain rule on both sides: $H(A\cup B)=\sum_i H((A\cup B)_i\mid\cdot)\ge1.26\sum_i H(A_i\mid\cdot)=1.26H(A)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Chain rule \Cref{fac:chain-rule} (textbook); summation of Step 28 over $i$; hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 30
**Location:** sections/07-frankl-corollary.tex:42
**Content (≤ 2 lines):** $H(A\cup B)\le\log|\F|=H(A)$: max-entropy on $\F$-support + $A$ uniform.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Maximum-entropy fact \Cref{fac:max-entropy} (Cover–Thomas Thm 2.6.4); union-closure gives $A\cup B\in\F$. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z

## Step 31
**Location:** sections/07-frankl-corollary.tex:55
**Content (≤ 2 lines):** Contradiction $H(A)\ge H(A\cup B)\ge1.26H(A)>H(A)$ since $H(A)=\log|\F|\ge\log2=1>0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\log_2 2=1>0$ script-verified; $1.26>1$; chain of Steps 28/30. Hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-06-09T05:00:00Z
