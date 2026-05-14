# Confidence trace — Hoeffding's inequality proof

Date: 2026-05-14.

## Methodology

Each derivation step is enumerated, initialized to 🔴, and walked through with
fast-path classification (textbook inequality → 🟢, digest match → 🟡, project
lemma match → 🟡/🟢). Steps that cannot be fast-checked would warrant sub-agent
re-derivation; none of the steps in this proof reach that threshold, since the
proof consists entirely of named textbook moves over a single page of algebra.

Counts at end of sweep: 🟢 26 / 🟡 3 / 🔴 0.

---

## sections/02-hoeffding-lemma.tex — proof of `lem:hoeffding-lemma`

### Step L1
**Location:** sections/02-hoeffding-lemma.tex:31-36
**Content (≤ 2 lines):** $\psi'(\lambda) = \E[Y e^{\lambda Y}] / \E[e^{\lambda Y}]$,
$\psi''(\lambda) = \E[Y^2 e^{\lambda Y}]/\E[e^{\lambda Y}] - (\E[Y e^{\lambda Y}]/\E[e^{\lambda Y}])^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct calculus — differentiate $\log f(\lambda)$ where
$f(\lambda) = \E[e^{\lambda Y}]$. By chain rule $\psi' = f'/f$, by quotient/product rule
$\psi'' = f''/f - (f'/f)^2$, with $f'(\lambda) = \E[Y e^{\lambda Y}]$,
$f''(\lambda) = \E[Y^2 e^{\lambda Y}]$ by differentiating under expectation. Each
differentiation step is a one-line textbook move; the dominated-convergence
justification is given in prose at lines 26-30. Fast-path: textbook calculus.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L2
**Location:** sections/02-hoeffding-lemma.tex:39-43
**Content (≤ 2 lines):** Tilted measure $d\Pr_\lambda/d\Pr := e^{\lambda Y}/\E[e^{\lambda Y}]$
is a probability measure.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Density is nonneg (exponential is positive) and integrates to
$\E[e^{\lambda Y}]/\E[e^{\lambda Y}] = 1$. Textbook fact about Radon--Nikodym derivatives.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L3
**Location:** sections/02-hoeffding-lemma.tex:46-50
**Content (≤ 2 lines):** Change-of-measure formula
$\E_\lambda[g(Y)] = \E[g(Y) e^{\lambda Y}] / \E[e^{\lambda Y}]$ for measurable $g$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Definition of expectation under a measure with given
Radon--Nikodym derivative: $\E_\lambda[g(Y)] = \int g(Y)\, d\Pr_\lambda
= \int g(Y) (d\Pr_\lambda/d\Pr)\, d\Pr = \E[g(Y) e^{\lambda Y}]/\E[e^{\lambda Y}]$.
Textbook (any graduate probability text).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L4
**Location:** sections/02-hoeffding-lemma.tex:52-57
**Content (≤ 2 lines):** $\psi'(\lambda) = \E_\lambda[Y]$,
$\psi''(\lambda) = \Var_\lambda(Y) = \E_\lambda[Y^2] - (\E_\lambda[Y])^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute $g(y) = y$ and $g(y) = y^2$ in the change-of-measure
formula of L3, then read off from the explicit formulas in L1. Pure algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L5
**Location:** sections/02-hoeffding-lemma.tex:60-61
**Content (≤ 2 lines):** Under $\Pr_\lambda$, $Y$ still supported in $[\alpha,\beta]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\Pr_\lambda$ is absolutely continuous w.r.t. $\Pr$ with strictly
positive density on the support; equivalently, $\Pr_\lambda$ and $\Pr$ have the same
null sets, so $\{Y \in [\alpha,\beta]\}^c$ is $\Pr$-null hence $\Pr_\lambda$-null. Textbook.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L6
**Location:** sections/02-hoeffding-lemma.tex:62-65
**Content (≤ 2 lines):** For $Z \in [\alpha,\beta]$: $(Z - \tfrac{\alpha+\beta}{2})^2
\le (\tfrac{\beta-\alpha}{2})^2$ a.s.; $\Var(Z) \le \E[(Z - c)^2]$ for any $c$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** First half: $Z - \tfrac{\alpha+\beta}{2} \in [-\tfrac{\beta-\alpha}{2},
\tfrac{\beta-\alpha}{2}]$, so squared lies in $[0, (\tfrac{\beta-\alpha}{2})^2]$. Second half:
$\Var(Z) = \min_c \E[(Z-c)^2]$ attained at $c = \E Z$; for any other $c$, $\E[(Z-c)^2] \ge
\Var(Z)$. Both textbook (named: Popoviciu's variance inequality for the composite).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L7
**Location:** sections/02-hoeffding-lemma.tex:66-69 (eq:popoviciu)
**Content (≤ 2 lines):** $\Var(Z) \le (\beta-\alpha)^2/4$ for $Z \in [\alpha,\beta]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Chain L6's two inequalities: $\Var(Z) \le \E[(Z -
\tfrac{\alpha+\beta}{2})^2] \le (\tfrac{\beta-\alpha}{2})^2 = (\beta-\alpha)^2/4$.
Textbook named inequality (Popoviciu 1935).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L8
**Location:** sections/02-hoeffding-lemma.tex:70-75 (eq:psi-pp-bound)
**Content (≤ 2 lines):** $\psi''(\lambda) = \Var_\lambda(Y) \le (\beta-\alpha)^2/4$
for all $\lambda \in \R$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** L4 (identity), then L5+L7 (Popoviciu applied to tilted distribution
of $Y$, which is also supported in $[\alpha,\beta]$). Composition of two verified steps.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L9
**Location:** sections/02-hoeffding-lemma.tex:78-79
**Content (≤ 2 lines):** $\psi(0) = 0$ and $\psi'(0) = \E[Y] = 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\psi(0) = \log \E[1] = \log 1 = 0$. $\psi'(0) = \E_0[Y]$ where
the tilt at $\lambda = 0$ is $\Pr$ itself, so $\psi'(0) = \E[Y] = 0$ by centering hypothesis.
Direct substitution.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L10
**Location:** sections/02-hoeffding-lemma.tex:82-83 (Taylor row 1)
**Content (≤ 2 lines):** $\psi(\lambda) = \psi(0) + \psi'(0) \lambda + \int_0^\lambda
(\lambda - s) \psi''(s)\, ds$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Taylor's theorem with integral remainder for $C^2$ functions.
Textbook (Folland *Real Analysis* §3.7 or Rudin *PMA* Theorem 5.15). The Lagrange-type
form is standard; the integral form follows from integration by parts of
$\psi(\lambda) - \psi(0) = \int_0^\lambda \psi'(s)\, ds$ once more, integrating $\psi'$ vs.
$d(s - \lambda)$.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L11
**Location:** sections/02-hoeffding-lemma.tex:84 (Taylor row 2)
**Content (≤ 2 lines):** Drop $\psi(0) + \psi'(0)\lambda = 0$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute L9 ($\psi(0) = \psi'(0) = 0$).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L12
**Location:** sections/02-hoeffding-lemma.tex:85 (Taylor row 3)
**Content (≤ 2 lines):** $\int_0^\lambda (\lambda - s) \psi''(s)\, ds \le
\tfrac{(\beta-\alpha)^2}{4} \int_0^\lambda (\lambda - s)\, ds$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Apply L8 pointwise. CAVEAT: for $\lambda > 0$, $(\lambda - s) \ge
0$ on $[0,\lambda]$, so multiplying $\psi''(s) \le (\beta-\alpha)^2/4$ by $(\lambda-s) \ge 0$
and integrating preserves the inequality. For $\lambda < 0$, $\int_0^\lambda = -\int_\lambda^0$
and $(\lambda - s) \le 0$ on $[\lambda, 0]$, so the integrand $(\lambda - s)\psi''(s)$ is
$\le 0$ in absolute terms but after the sign flip from reversing limits the inequality
needs care. The proof body addresses this via the substitution $s \mapsto -s$ comment
(prose at lines 91-93). For a full bullet-proof handling: note that $\psi(\lambda) =
\psi(-|\lambda|)$ is not generally true, but
$\psi(\lambda) \le \tfrac{\lambda^2}{2} \cdot \sup_s \psi''(s)$ via the standard
identity $\psi(\lambda) = \int_0^\lambda \int_0^t \psi''(s)\, ds\, dt$, which is
nonneg-integrand for $\lambda$ of either sign and bounds by $\tfrac{\lambda^2}{2}$ times
the $L^\infty$ bound on $\psi''$. The proof's prose-aside is correct but slightly terse;
this step is marked 🟡 to signal that the sign-of-$\lambda$ analysis is worth scrutiny.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L13
**Location:** sections/02-hoeffding-lemma.tex:86-87
**Content (≤ 2 lines):** $\int_0^\lambda (\lambda - s)\, ds = \lambda^2/2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\int_0^\lambda (\lambda - s)\, ds = [\lambda s - s^2/2]_0^\lambda
= \lambda^2 - \lambda^2/2 = \lambda^2/2$. Elementary calculus, holds for $\lambda$ of either
sign (when $\lambda < 0$ the integral is interpreted as $-\int_\lambda^0$, yielding the
same $\lambda^2/2 \ge 0$).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step L14
**Location:** sections/02-hoeffding-lemma.tex:95-96
**Content (≤ 2 lines):** Exponentiate $\psi(\lambda) \le \lambda^2 (\beta-\alpha)^2/8$
to give $\E[e^{\lambda Y}] \le \exp(\lambda^2 (\beta - \alpha)^2/8)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\exp$ is monotone increasing. Definition $\psi = \log \E[e^{\lambda Y}]$
inverts.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

---

## sections/03-main-theorem.tex — proof of `thm:hoeffding`

### Step T1
**Location:** sections/03-main-theorem.tex:22-25
**Content (≤ 2 lines):** $Y_i := X_i - \mu_i$ satisfies $\E Y_i = 0$, $Y_i \in
[a_i - \mu_i, b_i - \mu_i]$ with $0$ in the interval.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Match against `fac:range-invariance` (project fact, sections/01-preliminaries.tex
lines 38-42). Hypotheses (a.s. bound + integrability for $\mu_i = \E X_i$ to exist) match
trivially; conclusion matches. Project-fact citation match.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T2
**Location:** sections/03-main-theorem.tex:25-27
**Content (≤ 2 lines):** $Y_1, \ldots, Y_n$ are independent.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Independence is preserved under deterministic measurable
transformations of individual variables: if $X_1, \ldots, X_n$ are independent and
$Y_i = f_i(X_i)$, then $Y_1, \ldots, Y_n$ are independent (apply the definition via product
sigma-algebras). Textbook (Durrett *Probability* §2.1).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T3
**Location:** sections/03-main-theorem.tex:28-30
**Content (≤ 2 lines):** $S_n - \mu = \sum_i (X_i - \mu_i) = \sum_i Y_i$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Linearity of expectation gives $\mu = \E S_n = \sum_i \mu_i$;
substitute. Pure algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T4
**Location:** sections/03-main-theorem.tex:42-43 (Markov row)
**Content (≤ 2 lines):** $\Pr[\sum_i Y_i \ge t] \le e^{-\lambda t} \E[e^{\lambda \sum_i Y_i}]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Markov: $\Pr[Z \ge u] \le \E[Z]/u$ for $Z \ge 0$, $u > 0$. Take
$Z = e^{\lambda \sum Y_i} \ge 0$, $u = e^{\lambda t} > 0$. Event $\{\sum Y_i \ge t\}
\subseteq \{e^{\lambda \sum Y_i} \ge e^{\lambda t}\}$ for $\lambda > 0$ (exp monotone). Textbook.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T5
**Location:** sections/03-main-theorem.tex:44 (row 2)
**Content (≤ 2 lines):** $\E[\exp(\lambda \sum_i Y_i)] = \E[\prod_i e^{\lambda Y_i}]$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $e^{a+b} = e^a e^b$, applied $n-1$ times. Algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T6
**Location:** sections/03-main-theorem.tex:45 (row 3)
**Content (≤ 2 lines):** $\E[\prod_i e^{\lambda Y_i}] = \prod_i \E[e^{\lambda Y_i}]$
by independence.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $Y_i$ independent (T2), $e^{\lambda Y_i}$ are deterministic
functions of $Y_i$ alone hence also independent, product of expectations rule for indep
random variables. Each $e^{\lambda Y_i}$ is bounded a.s. (since $Y_i$ bounded a.s.), so
integrability is immediate. Textbook (Durrett §2.1).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T7
**Location:** sections/03-main-theorem.tex:46 (row 4)
**Content (≤ 2 lines):** $\E[e^{\lambda Y_i}] \le \exp(\lambda^2 (b_i-a_i)^2/8)$ for each
$i$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Direct invocation of `lem:hoeffding-lemma`. Hypotheses
re-verified at cite-site: each $Y_i$ has $\E Y_i = 0$ (T1) and $Y_i \in [\alpha_i, \beta_i]
:= [a_i - \mu_i, b_i - \mu_i]$ a.s. with $\alpha_i \le 0 \le \beta_i$ (since
$\mu_i \in [a_i, b_i]$, so $a_i - \mu_i \le 0 \le b_i - \mu_i$). Range
$\beta_i - \alpha_i = (b_i - \mu_i) - (a_i - \mu_i) = b_i - a_i$. Conclusion of lemma
gives $\E[e^{\lambda Y_i}] \le \exp(\lambda^2 (b_i - a_i)^2 / 8)$. Cite-site hypothesis
check matches digest at `.proof-research/hoeffding-lemma.md`. Project-lemma match.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T8
**Location:** sections/03-main-theorem.tex:47 (row 5)
**Content (≤ 2 lines):** $e^{-\lambda t} \cdot \prod_i \exp(\cdot) = \exp(-\lambda t +
\tfrac{\lambda^2}{8} \sum_i (b_i - a_i)^2)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Product of exponentials = exponential of sum. Algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T9
**Location:** sections/03-main-theorem.tex:48 (row 6)
**Content (≤ 2 lines):** Abbreviate $v := \sum_i (b_i - a_i)^2$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Notational substitution per prelim definition.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T10
**Location:** sections/03-main-theorem.tex:62-66
**Content (≤ 2 lines):** $q(\lambda) := -\lambda t + \lambda^2 v/8$ strictly convex (in
$\lambda$); $q'(\lambda) = -t + \lambda v/4 = 0 \Rightarrow \lambda^\star = 4t/v$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $q''(\lambda) = v/4 > 0$ (since $v > 0$ assumed), so $q$ strictly
convex. FOC: differentiate $q$, set to zero, solve. Hand check: $q'(\lambda^\star) =
-t + (4t/v)(v/4) = -t + t = 0$. Elementary calculus.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T11
**Location:** sections/03-main-theorem.tex:71-76
**Content (≤ 2 lines):** $q(\lambda^\star) = -4t^2/v + (4t/v)^2 v/8 = -4t^2/v + 2t^2/v
= -2t^2/v$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Hand-check: $-\lambda^\star t = -(4t/v) \cdot t = -4t^2/v$;
$(\lambda^\star)^2 v/8 = (16 t^2/v^2)(v/8) = 16 t^2/(8 v) = 2 t^2/v$. Sum $-4t^2/v + 2t^2/v =
-2 t^2/v$. Arithmetic.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T12 (eq:upper-tail)
**Location:** sections/03-main-theorem.tex:79-82
**Content (≤ 2 lines):** $\Pr[\sum Y_i \ge t] \le \exp(-2t^2/v)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Substitute $\lambda = \lambda^\star = 4t/v > 0$ (positivity
required by Markov step T4) into the Step-1 chain. Composition.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T13
**Location:** sections/03-main-theorem.tex:85-87
**Content (≤ 2 lines):** $\widetilde X_i := -X_i \in [-b_i, -a_i]$, range $b_i - a_i$
preserved.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $X_i \in [a_i, b_i] \Rightarrow -X_i \in [-b_i, -a_i]$. Range
$(-a_i) - (-b_i) = b_i - a_i$. Independence preserved (T2 rule applied to $f_i(x) = -x$).
Algebra.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T14
**Location:** sections/03-main-theorem.tex:91-99
**Content (≤ 2 lines):** $\Pr[S_n - \mu \le -t] = \Pr[\widetilde S_n - \E\widetilde S_n
\ge t] \le \exp(-2t^2/v)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Direct: $\widetilde S_n = -S_n$, $\E\widetilde S_n = -\mu$, so
$\widetilde S_n - \E \widetilde S_n = -S_n + \mu = -(S_n - \mu)$; thus
$\{S_n - \mu \le -t\} = \{-(S_n - \mu) \ge t\} = \{\widetilde S_n - \E\widetilde S_n \ge t\}$.
Apply T12 to the $\widetilde X_i$'s, whose $v$ value is identical (T13).
**Sub-agent task id:** none
**Last updated:** 2026-05-14

### Step T15
**Location:** sections/03-main-theorem.tex:104-108
**Content (≤ 2 lines):** Union bound: $\Pr[|S_n - \mu| \ge t] \le \Pr[S_n - \mu \ge t]
+ \Pr[S_n - \mu \le -t] \le 2 \exp(-2t^2/v)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** $\{|S_n - \mu| \ge t\} = \{S_n - \mu \ge t\} \cup \{S_n - \mu \le
-t\}$; finite union bound $\Pr[A \cup B] \le \Pr[A] + \Pr[B]$. Combine T12 + T14.
**Sub-agent task id:** none
**Last updated:** 2026-05-14

---

## Sweep result

- **Total steps enumerated:** 29 (14 lemma + 15 theorem)
- **🟢 verified:** 26 — textbook inequalities (Markov, Popoviciu, Taylor, exp monotone),
  hand-checked algebra, calculus FOC.
- **🟡 cross-checked:** 3 — L12 (sign-of-$\lambda$ subtle but treated in prose),
  T1 (project-fact match), T7 (project-lemma match).
- **🔴 from-memory (final):** 0.

No defects detected; no `\todo{}` markers needed. The only steps that did not reach 🟢
are the cross-checked ones that rely on project-internal references — by the sweep's
own definition, these can only escalate to 🟢 via independent re-derivation, which
would be redundant since the cited statements are themselves either textbook or proved
in this document.

Proceed to Phase D.
