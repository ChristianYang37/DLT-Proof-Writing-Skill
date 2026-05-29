# Stage-1 decisions — numbered nontrivial choices

Every nontrivial modelling / proof-architecture choice baked into the
Stage-1 statements and stub sketches. Stage 2 must honour these or
re-open them with the user. Tagged by the honesty constraint each serves.

---

## A. Geometry and decoder

**D1. Sphere radius $\sqrt d$, track the ANGLE.** Post-LayerNorm states
live on $M_d=\{\|x\|_2=\sqrt d\}$. Because $\|x_t\|=\sqrt d$ is fixed, the
angular margin $m_t=\langle W_U^{a^\star},x_t\rangle/(\|W_U^{a^\star}\|\sqrt d)$
is a pure cosine. We track the angle, never the radius — so there is NO
radial-Ito / centrifugal calculation (the old `lem:radial_ito_expansion`
is dropped). [Constraint #3: noise comes from projection variance, not
from a radial walk.]

**D1a. $n=1$, TRUE decoder everywhere.** Answer set $\mathcal A=\{a^\star\}$,
$W_U\in\R^{|V|\times d}$ the LITERAL unembedding. $\arg\max_a\langle W_U^a,x\rangle$
IS greedy decoding, so $D_{\mathrm{true}}=D_{\mathrm{lin}}$. We DROP the
sequence-level $\mathcal V^n$ machinery and the $D_{\mathrm{lin}}/D_{\mathrm{true}}$
one-sided transfer. ALL statements (success AND failure) are about the TRUE
decoder. [Constraint #8.]

**D1b. Success $=\{M(x_T)>0\}$.** Logit margin
$M(x)=\langle W_U^{a^\star},x\rangle-\max_{a\neq a^\star}\langle W_U^a,x\rangle$.
Success $\Leftrightarrow$ argmax $=a^\star \Leftrightarrow M(x_T)>0$. The loss
is the analysis Lyapunov function; the margin is the operational quantity;
`lem:loss_to_margin` bridges them ($L<\log2\Rightarrow M>0$ for $|\mathcal A|=1$).

---

## B. The single global assumption and the derived constant

**D2. A1 is GLOBAL with NO snowball, NO basin, NO init.**
$\zeta_t=\mathbf 1\{\langle\Delta x_t,-\operatorname{grad}_R L(x_{t-1})\rangle\ge0\}$
is the per-step DESCENT indicator, and A1 asserts
$\Pr[\zeta_t=1\mid\mathcal F_{t-1}]=p$ for ALL $t$ (no region gating, no
$\Lstar$, no $\loss<\Lstar$ stratification). $\delta:=2p-1$ is the ONLY
behavioral knob. The old `ass:signed_snowball` (region-gated $\lambda_\pm$)
and `\Lstar` are RETIRED. [Constraint #1.]

**D3. The drift floor $c$ is DERIVED, not assumed.**
`lem:riem_gradient` derives, from the incoherence gap,
$\langle W_U^{a^\star},-\nabla L\rangle\ge(1-p_{a^\star})(\rho_0^2-\mu_0 R_U^2)$,
hence $c:=\rho_0^2-\mu_0 R_U^2$. This is POSITIVE iff $\mu_0<\rho_0^2/R_U^2$,
which is part of A2's explicit regime (canonical unit rows
$\rho_0=R_U=1\Rightarrow c=1-\mu_0>0$). $c$ is a LEMMA output consumed by
`lem:signal_floor` and `thm:R3prime`; it is NOT an assumption. [Constraint
#1, #5: $c$ is a first-moment statement on the UPDATE DIRECTION, not a
curvature/PL inequality.]

**D4. $\delta$ vs $p_{a^\star}$ bookkeeping (FLAGGED for Stage 2).** The
signal floor combines the A1 descent probability $p$ (giving $\delta=2p-1$
as the net signed alignment) with the per-step magnitude $c$ from D3. The
exact way $(1-p_{a^\star})$ (the softmax-gap factor inside $c$) interacts
with $\delta$ (the descent net-rate) is written as $\delta\cdot c$ at
leading order in the Stage-1 statements; pinning whether it is exactly
$\delta c$ or $\delta\cdot(1-\bar p_{a^\star})\cdot(\rho_0^2-\mu_0R_U^2)$
with an averaged gap is a Stage-2 obligation. Stage-1 statements carry the
leading-order $\delta c$ form and a `% STAGE-1 SKETCH` flag. This does NOT
introduce an init condition — it is a constant-identification task.

---

## C. The five risky derivations — tool choices

**D5. (a) GLOBAL drift floor with NO snowball.** The signal floor on the
UN-retracted iterate is a first-moment computation:
$\E[\langle W_U^{a^\star},\tilde x_T\rangle\mid\mathcal F_0]
=\sum_k w_{T,k}\E\langle W_U^{a^\star},V_k\rangle$, and each effective
(descending) step contributes $\ge c$ by D3 while A1 makes the net signed
rate $\delta$ GLOBALLY (every $k$, no gating). With $\sum_k w_{T,k}=1$ this
gives floor $\delta\cdot c$ — DERIVED, no snowball region. [Constraint #1.]

**D6. (b) Retraction-stability constant.** We use Boumal Prop. 5.44
(second-order retraction, $O(\|s\|^3)$ pullback) with the radius-$\sqrt d$
rescaling: unit-sphere step $\eta=O(1/\sqrt d)\Rightarrow$ per-step cubic
residual $O(d^{-3/2})$, accumulated/relative to the logit scale the
headline transfer error is **$O(1/d^{1.5})$**. DECISION: state the rate as
$O(1/d^{1.5})$ in `lem:retraction_stability`; the absolute constant
$C_{\mathrm{ret}}$ (third-derivative bound of the normalization map) is
named but its numeric value is a Stage-2 pin. We prove the floor on
$\tilde x_T$ FIRST, then transfer — we never apply $\sum w=1$ to the
retracted $x_T$. [Constraint #6.]

**D7. (c) Failure branch = DIRECT anti-concentration (max-LOWER bound).**
DECISION on the exact tool: the **second-moment method** (Paley–Zygmund
style) on $N_t=\sum_{a\neq a^\star}\mathbf 1\{\langle W_U^a,x_T\rangle>t\}$,
with the incoherence A2 supplying the pairwise decorrelation (off-diagonal
covariance $\le\mu_0\sigma_T^2$) and Vershynin Thm 3.4.6 supplying the
per-direction small-ball/spreading. This yields
$\max_{a\neq a^\star}\langle W_U^a,x_T\rangle\ge\sigma_T\sqrt{2(1-\mu_0)\log(|V|-1)}$
whp. It is NOT a reversed Lemma A (a union bound can only UPPER-bound a max)
and contains NO Galton–Watson. Sudakov minoration is recorded as the
fallback in `anti-concentration-max.md` if the second-moment variance term
proves loose at small $|V|$. [Constraint #7.]

**D8. (d) Noise provenance $=(1/\sqrt d)\times(1/\sqrt T)$.** The $1/\sqrt d$
is the high-dimensional projection variance of `lem:orthogonality`
($\E\langle e,u\rangle^2=1/d$, Vershynin Thm 3.4.6) — NOT sphere
concentration-of-measure / Lévy for the $\sqrt T$ factor. The $1/\sqrt T$ is
the softmax quad-variation $\sum_t w_{T,t}^2\le e^{2S}/T$ of
`lem:quad_variation`. Their product gives the martingale fluctuation scale
$\sigma_T\asymp R_U M\,e^S/\sqrt{T_{\max}d}$. Both factors are explicit in
the stub sketches. [Constraint #3.]

**D9. (e) R3' carries NO hidden ODE.** `thm:R3prime` is a FINITE-HORIZON
high-probability confinement statement: after an $O(1)$ rescaled-time
burn-in the trajectory enters and stays in the cap
$C=\{\cos\angle(W_U^{a^\star},x)\ge m^\star-\varepsilon\}$, and
$m_{T_{\max}}$ concentrates at $\delta c$ with $O(1/\sqrt{T_{\max}d})$
fluctuations. It is proved by the SAME martingale machinery (signal floor +
azuma + retraction transfer), with the entry/stay established by a
maximal-inequality argument over the horizon — NO drift ODE, NO closability
of a summary statistic, NO Foster–Lyapunov rate. The ODE $\dot m=\delta c-m$
appears ONLY in a flagged informal remark, explicitly stated as requiring
two EXTRA stylizations not implied by A1: (AS) asymptotic stationarity of
the loss-stratified indicator, and (Lλ) a Lipschitz-in-$m$ closure of the
conditional drift. The remark says the ODE is NOT derivable from A1 alone.
[Constraint #2, #4.]

---

## D. Probability-budget and degeneracy bookkeeping

**D10. Anti-pole degeneracy absorbed into the high-prob budget (NO init
condition).** On the sphere the tangential projection of the signal,
$(I-xx^\top/d)W_U^{a^\star}$, degenerates only if $x_{t-1}$ is collinear
with $W_U^{a^\star}$ (the pole — harmless, that IS success) or its antipode
(the anti-pole). DECISION: we do NOT impose any initial-angle condition.
Instead the anti-pole is handled by (i) NOISE NON-DEGENERACY — the
isotropic per-step noise component has variance $\ge\sigma_{\min}^2/d$ in
every tangent direction (`lem:orthogonality`), so the trajectory leaves any
measure-zero collinear set immediately and the time spent within angle
$\epsilon$ of the anti-pole is $O(\epsilon)$; and (ii) $x_0$-WASHOUT —
$w_{T,0}=O(1/T)\to0$ (D11), so the initial condition (including a worst-case
anti-pole start) contributes $O(1/T)$ to $\tilde x_T$ and is dominated. The
total anti-pole contribution is folded into the $\delta_{\mathrm{fail}}$
budget of R1/R2 and the burn-in failure budget of R3'. **If Stage 2 finds
this absorption requires a genuine init condition, STOP and surface as
`\todo{user-decision}`** (per Constraint #1) — do NOT silently add one.

**D11. $x_0$ washes out.** From `lem:running_average`,
$\tilde x_T=\sum_{k\ge0}w_{T,k}V_k$ with $w_{T,0}=O(1/T)$ (the SGDM decay
applied to the initial state). Stated explicitly in `def:dynamics` and
`lem:running_average`; consumed in D10 and in every floor/noise estimate as
"the $x_0$ term is $O(1/T)$ and absorbed".

**D12. Minimum-dimension corollary — KEEP as a corollary of R1.**
DECISION: keep a `cor:min_dimension` under `thm:R1` stating the smallest
$d$ for which a given $\delta>0$ is super-threshold at horizon $T_{\max}$
($d\gtrsim c_1^2\log|V|/(\delta^2 T_{\max})$). It has a downstream consumer
(empirical-prediction discussion is out of scope, but the corollary is the
clean inversion of $\delta\ge\sqrt2\delta_c$ and is cited by R3''s burn-in
length). If Stage 2 finds no consumer, OCCAM-drop it. [Occam.]

**D13. Two-sided slack factor $\sqrt2$.** Following the ported T1, the
super-threshold branch uses $\delta\ge\sqrt2\,\delta_c$ and the failure
branch $\delta\le\delta_c/\sqrt2$, with $\delta_c=c_1\sqrt{\log|V|/(T_{\max}d)}$.
The $\sqrt2$ absorbs the lower-order incoherence-drift correction
$\kappa(\mu_0)=1+\mu_0$. R2 fills the intermediate window. Constant
$c_1=2\sqrt2\,e^S R_U M\,\kappa(\mu_0)/(\rho_0\cdot\text{(normalization)})$ —
exact form pinned in Stage 2.

**D14. Berry–Esseen reference unchanged.** R2 uses Hall–Heyde (1980)
Thm 3.6 (`cite-hallheyde1980.md`, digest exists) on the centred
signed-signal martingale, with the high-probability truncation event from
`lem:orthogonality` giving the $d^{-3/2}$ third-moment that makes the rate
$e^S/\sqrt{T_{\max}}$. "Berry–Esseen" is NOT a lint-tracked technique
keyword, so no separate technique digest is required; the cite digest
suffices. [R13 satisfied.]

**D15. Width: state BOTH absolute and relative, do not conflate.** R2's
transition width is reported two ways: the HEADLINE absolute width in
$\delta$ is $\Theta(1/\sqrt{T_{\max}d})$; the RELATIVE width
(normalized by $\delta_c$) is $\Theta(1/\sqrt{\log|V|})$. These are stated
in separate clauses (headline in the theorem/`cor:width`, relative in a
remark) and never equated.

---

## E. Macros and citations

**D16. Macro repurposing.** `\snet`→$\delta$ (the net descent rate
$2p-1$); `\snorder`→$m$ (angular margin); RETIRE
`\Dlin,\Dtrue,\Eld,\equilstate,\contract,\projAset` and the $|V|^n$
notation; KEEP `\loss,\cmass,\Vocab,\norm,\inner,\incoh,\Margin,\Lstar`
(though $\Lstar$ now appears only as the decode threshold $\log2$ alias, not
a snowball cutoff — repurpose its meaning), the aliascnt block, `\crefname`.
ADD sphere $M_d$, retraction $\mathcal R$, Riemannian gradient
$\operatorname{grad}_R$, descent indicator $\zeta$.

**D17. Citation whitelist.** Only cite: vaswani2017attention (architecture),
vershynin2018 (sphere concentration + max of sub-Gaussians + small-ball),
freedman1975tail (Bernstein martingale tail), hallheyde1980 (Berry–Esseen),
saad1995online (order-parameter precedent, prose only), benarous2022highdim
(high-d SGD scaling, prose only), boumal2023 (retraction geometry). All have
cite digests. The retired RLVR/PL/DEQ references stay in `refs.bib` but are
NOT cited (lint R12/R13 fire only on USED cites).
