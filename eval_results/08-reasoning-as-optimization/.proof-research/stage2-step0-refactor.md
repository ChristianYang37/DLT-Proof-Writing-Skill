# Stage-2 Step-0 framing correction — as implemented

## The logical gap (user-confirmed)
Stage-1 defined the descent indicator on LOSS descent,
$\zeta_t=\mathbf 1\{\langle\Delta x_t,-\operatorname{grad}_R L\rangle\ge0\}$,
and `lem:riem_gradient(ii)` bounded only $\langle W_U^{a^\star},-\nabla L\rangle$.
A step that lowers the LOSS need not raise the CORRECT-TOKEN logit
(inner-product alignment is not transitive). So the net correct-direction
drift $\ge\delta c\rho_0$ CANNOT be derived from the loss-descent rate $p$.
Hence $c$ cannot be derived this way.

## The correction (user-approved): two constants (p, c) on the correct direction

### Redefinition (in 01-preliminaries `def:descent_indicator`, 02 `ass:descent`)
- $\hat W_U^{a^\star}:=W_U^{a^\star}/\|W_U^{a^\star}\|$ (unit correct row).
- Per-step correct-direction projection $s_k:=\langle V_k,\hat W_U^{a^\star}\rangle$.
- Sign indicator $\zeta_k:=\operatorname{sign}(s_k)\in\{-1,+1\}$ (define
  $\operatorname{sign}(0)=+1$, measure-zero under noise non-degeneracy A2(5)).
- **A1 (global):** $\Pr[\zeta_k=+1\mid\mathcal F_{k-1}]=p$ for all $k$; $\delta:=2p-1$.
- **Magnitude floor (part of the assumption):** $\mathbb E[\,|s_k|\mid\mathcal F_{k-1}]\ge c\rho_0$
  with $c\in(0,1]$ (conditional-mean floor; honors the user's "a.s. or in
  conditional mean"). Also $|s_k|\le\|V_k\|\le M$ a.s. (A2(2)).
- **Anti-aligned-tail control (the clean way):** conditional independence of
  the sign $\zeta_k$ and the magnitude $|s_k|$ given $\mathcal F_{k-1}$.

### The rigorous net drift (derived explicitly in 02 remark + consumed in 09)
Under conditional independence of $\zeta_k$ and $|s_k|$ given $\mathcal F_{k-1}$:
$$\mathbb E[s_k\mid\mathcal F_{k-1}]
 =\mathbb E[\zeta_k|s_k|\mid\mathcal F_{k-1}]
 =\mathbb E[\zeta_k\mid\mathcal F_{k-1}]\,\mathbb E[|s_k|\mid\mathcal F_{k-1}]
 =\delta\,\mathbb E[|s_k|\mid\mathcal F_{k-1}].$$
This is an **identity** (no sign on $\delta$ needed). Then:
- If $\delta\ge0$: $\mathbb E[s_k\mid\mathcal F_{k-1}]\ge\delta c\rho_0$ (uses floor).
- If $\delta<0$: $\mathbb E[s_k\mid\mathcal F_{k-1}]\le\delta c\rho_0\le0$
  and in all cases $|\mathbb E[s_k\mid\mathcal F_{k-1}]|=|\delta|\,\mathbb E[|s_k|]\le|\delta|M$.
The two-sided handle $\mathbb E[s_k\mid\mathcal F_{k-1}]=\delta\,\mathbb E[|s_k|]$,
$\mathbb E[|s_k|]\in[c\rho_0,M]$, is what the success branch (floor, $\delta>0$),
the failure branch (ceiling on correct logit), and R2 (drift term) all use.
NO transitivity through $-\operatorname{grad}_R L$. NO extra assumption needed
beyond the conditional independence (which is part of A1).

### Added clause A1(d) (drift direction) — NOT a strengthening of the net-drift derivation
The incorrect-max UPPER bound (lem:incorrect_max) needs the DRIFT term
$\langle W_U^a, \E\tilde x_T\rangle\le\mu_0 R_U M$ for $a\neq a^\star$. This
requires knowing the conditional MEAN of $V_k$ has no large incorrect-direction
component. The Stage-1 skeleton implicitly assumed this ("$\E\tilde x_T$ supported
in the correct-row direction up to mean-zero noise") but never stated it.
Honest fix: **A1 clause (d)** states $\E[V_k\mid\F_{k-1}]=\beta_k\hat W_U^{a^\star}$,
$\beta_k=\E[s_k\mid\F_{k-1}]$ — the systematic part of each step points at the
answer, everything else is mean-zero noise (consistent with A2(5)). Then for
$a\neq a^\star$: $|\langle W_U^a,\E[V_k\mid\F_{k-1}]\rangle|=|\beta_k||\langle W_U^a,\hat W_U^{a^\star}\rangle|\le M\mu_0 R_U$.
This is GLOBAL (every k), NO basin/region/init. It is a structural modelling
clause for the incorrect-max bound, NOT part of the correct-direction net-drift
derivation (which needs only (a)+(b)+(c)). The net drift $\delta c\rho_0$ remains
rigorous from (sign p + magnitude c + cond. indep.) alone, as the user required;
clause (d) is surfaced explicitly here and in rem:descent_globality, not smuggled.

## Conversion to logit / angular margin
$\langle W_U^{a^\star},V_k\rangle=\|W_U^{a^\star}\|\,s_k$, $\|W_U^{a^\star}\|\in[\rho_0,R_U]$.
Floor on the logit drift ($\delta\ge0$): $\ge\rho_0\cdot\delta c\rho_0=\delta c\rho_0^2$.
Angular-margin target level $m^\star=\delta c\rho_0/(\sqrt d\,R_U)$ (worst-case
$\|W_U^{a^\star}\|=R_U$ in the denominator of the cosine; using the unit-projection
floor $\delta c\rho_0$ in the numerator). Consistent with the Stage-1 statements
once $\driftc$ is reinterpreted as the assumed $c$.

## Fate of `lem:riem_gradient` under Occam (user-instructed)
After the redefinition $\zeta_k=\operatorname{sign}(s_k)$, the loss-descent
direction $\operatorname{grad}_R L$ has NO load-bearing downstream consumer:
- the indicator no longer uses it,
- $c$ is now assumed (not derived),
- R3' confinement uses the signal floor + martingale, not the gradient,
- the incoherence GAP $\mu_0<\rho_0^2/R_U^2$ is no longer needed for $c>0$.
Per Occam (user: "demote the whole lemma to a remark"): **`lem:riem_gradient`
is deleted as a lemma**; section 04 becomes a MOTIVATION remark
(`rem:descent_naming`) explaining why raising $\langle W_U^{a^\star},x\rangle$
tends to lower the cross-entropy loss (so the dynamics deserve the name
"descent / SGD on cross-entropy"), explicitly NOT feeding the drift and NOT
deriving $c$. The Riemannian-gradient FORMULA stays in `def:riem_gradient_obj`
(preliminaries) as part of the SGD reading; the gradient computation
$\langle W_U^{a^\star},-\nabla L\rangle=(1-p_{a^\star})(\rho_0^2-\mu_0R_U^2)$ is
shown inside the motivation remark (it is correct; it just is not load-bearing).

## Incoherence $\mu_0$: where it is still consumed
- `lem:incorrect_max` drift term $\mu_0 R_U M$ (orthogonality of $\E\tilde x_T$
  to incorrect rows).
- `lem:incorrect_max_lower` pairwise decorrelation (covariance $\le\mu_0\sigma_T^2$).
The GAP $\mu_0<\rho_0^2/R_U^2$ is DROPPED as a load-bearing condition (mentioned
in the A2 remark as a sufficient condition under which the motivating gradient
computation is positive, but not required for any result).

## CRITICAL Stage-2 correctness finding: margin-drift-sharing (deviation from skeleton, resolved honestly)
The skeleton's incorrect-max drift term $\mu_0 R_U M$ is $\Theta(1)$, which
would DOMINATE the critical-rate signal $\delta_c\cdot c\rho_0^2\sim\sqrt{\log|V|/(T_{\max}d)}\to0$
and BREAK the headline $\delta_c\propto1/\sqrt{T_{\max}d}$ scaling unless $\mu_0$
is itself $O(\sqrt{\log|V|/(T_{\max}d)})$ (a very strong incoherence assumption).
RESOLUTION (honest, not a todo): the correct AND incorrect drifts SHARE the
same systematic-update magnitude $D=\langle\hat W_U^{a^\star},\E\tilde x_T\rangle=\sum_k w_{T,k}\beta_k$.
For $\delta\ge0$, $D\in[\delta c\rho_0,\delta M]$. So:
- correct-logit drift $=\|W_U^{a^\star}\|D\ge\rho_0 D$;
- incorrect-logit drift $=D\langle W_U^a,\hat W_U^{a^\star}\rangle\le|D|\mu_0 R_U\le\delta M\mu_0 R_U$ (SMALL).
R1 SUCCESS compares the MARGIN $\langle W_U^{a^\star}-W_U^{\hat a},\tilde x_T\rangle$
whose drift $=D(\|W_U^{a^\star}\|-\langle W_U^{\hat a},\hat W\rangle)\ge\delta c\rho_0(\rho_0-\mu_0 R_U)$,
beating the margin noise $O(R_U M e^S\sqrt{\log|V|/(T_{\max}d)})$. NO $\Theta(1)$
$\mu_0 R_U M$ term survives; the $\mu_0 R_U M$ appears only as the LOOSE upper
bound in lem:incorrect_max (kept for R2), with the SHARP $\mu_0 R_U|D|$ exposed.
This gives the headline $\delta_c\propto1/\sqrt{T_{\max}d}$ cleanly.
**Cost:** R1/R3' acquire a MILD incoherence condition $\mu_0<\rho_0/R_U$ (so the
margin drift is positive; canonically $\rho_0=R_U=1\Rightarrow\mu_0<1$, automatic),
NOT the old gap $\mu_0<\rho_0^2/R_U^2$. This is the natural minimal incoherence for
incorrect tokens to be separable from the correct one — a genuine, mild, GLOBAL
architectural condition, NOT a basin/init condition. Surfaced in rem and final report.
Honest $c_1=2\sqrt2\,e^S R_U M/(c\rho_0(\rho_0-\mu_0 R_U))\cdot\kappa$ (κ = log-factor
absorption), structurally matching the user's template with $(1-\mu_0 R_U/\rho_0)$
in place of $(1+\mu_0)$ (sign flips because incoherence now HELPS separation and
appears as a denominator factor under the condition $\mu_0<\rho_0/R_U$).

## Macro
`\driftc` keeps rendering as $c_\star$ but is now the ASSUMED magnitude constant
$c$ (a.k.a. $c_\star$), not a derived quantity. No clash with the universal $c$.
Documented in macros.tex.

## Constants propagated (driftc rename: derived -> assumed, same symbol $c_\star$)
- `eq:critical_rate` $c_1=2\sqrt2\,e^S R_U M(1+\mu_0)/(\driftc\,\rho_0/R_U)$ unchanged
  in form; $\driftc$ now assumed.
- $m^\star=\snet\driftc\rho_0/(\sqrt d R_U)$ unchanged in form (R3').
- R2 standardised threshold $z$ unchanged in form.
