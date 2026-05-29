# Dependency graph — Reasoning as noisy Riemannian SGD (clean-slate rewrite)

Model: an LLM's chain-of-thought is **noisy Riemannian SGD with momentum
(SGDM) + normalization retraction on the cross-entropy loss over the
LayerNorm sphere** $M_d = \{x\in\R^d : \|x\|_2 = \sqrt d\}$. We
characterize when the trajectory decodes the correct single-token answer
$a^\star$ (so $n=1$, $\mathcal A=\{a^\star\}$, and the decoder is the TRUE
greedy decoder $\arg\max_a\langle W_U^a,x\rangle$).

Three results: **R1** two-sided phase transition; **R2** critical-window
Gaussian; **R3'** finite-horizon cone confinement (NOT an ODE).

Honesty constraints encoded structurally (see `stage1-decisions.md`):
NO snowball / NO loss basin / NO init condition; A1 GLOBAL; $c$ DERIVED;
NO forced ODE; noise provenance $=(1/\sqrt d)\times(1/\sqrt T)$; NO
per-step Foster–Lyapunov; NO Riemannian-PL; retraction error is real work;
failure branch = anti-concentration; all results for the TRUE decoder.

Shallow tree: a leaf layer of geometry+concentration lemmas, a middle
layer of two-sided logit bounds, and the three result-theorems on top.

---

## Preliminaries / assumptions (sections 01–02)

- `def:sphere` LayerNorm sphere $M_d$, post-LN state. **Consumers:** all.
- `def:loss` cross-entropy $L(x;Q)=\log\sum_a e^{\langle W_U^a,x\rangle}
  - \langle W_U^{a^\star},x\rangle$, convex in $x$. **Consumers:**
  `lem:riem_gradient`, `lem:loss_to_margin`, `thm:R1`, `thm:R2`.
- `def:angular_margin` $m_t = \langle W_U^{a^\star},x_t\rangle/(\|W_U^{a^\star}\|\|x_t\|)$
  (pure cosine since $\|x_t\|=\sqrt d$); logit margin $M(x)$. **Consumers:**
  `thm:R1`, `thm:R2`, `thm:R3prime`.
- `def:incoherence` $\mu(W_U)$ over the $|V|$ token rows. **Consumers:**
  `lem:riem_gradient` (derives $c$), `lem:incorrect_max`,
  `lem:incorrect_max_lower`.
- `def:filtration` $(\mathcal F_t)$; `def:descent_indicator` $\zeta_t =
  \mathbf 1\{\langle\Delta x_t, -\operatorname{grad}_R L(x_{t-1})\rangle\ge 0\}$.
  **Consumers:** A1, `lem:signal_floor`, `lem:incorrect_max_lower`.
- `def:dynamics` SGDM+retraction: $\tilde x_t=(1-\alpha)x_{t-1}+\alpha V_t$,
  $x_t=\sqrt d\,\tilde x_t/\|\tilde x_t\|$; $\tilde x_T=\sum_k w_{T,k}V_k$,
  $\sum_k w_{T,k}=1$, $\tau=1/T$, $w_{T,0}=O(1/T)$. **Consumers:**
  `lem:running_average`, `lem:quad_variation`, `lem:retraction_stability`.
- `def:retraction` normalization retraction (Boumal Def. 3.47 / Ex. 3.49).
  **Consumers:** `lem:retraction_stability`.
- `ass:A1` (GLOBAL behavioral; **Stage-2 two-constant refactor**): on the
  correct-direction projection $s_k=\langle V_k,\hat W_U^{a^\star}\rangle$,
  (a) sign rate $\Pr[\zeta_k=+1\mid\mathcal F_{k-1}]=p$ ($\delta:=2p-1$),
  (b) magnitude floor $\E[|s_k|\mid\mathcal F_{k-1}]\ge c\rho_0$,
  (c) sign/magnitude conditional independence, (d) drift direction
  $\E[V_k\mid\mathcal F_{k-1}]=\beta_k\hat W_U^{a^\star}$. Net drift
  $\E[s_k\mid\mathcal F_{k-1}]=\delta\E[|s_k|]\ge\delta c\rho_0$ is an
  IDENTITY (no transitivity). NO region, NO basin, NO init. **Consumers:**
  `lem:signal_floor`, `lem:incorrect_max`, `lem:incorrect_max_lower`,
  `thm:R1`, `thm:R2`, `thm:R3prime`.
- `ass:A2` (architecture): $\mu(W_U)\le\mu_0$, row norms in $[\rho_0,R_U]$,
  $\|V_t\|\le M$, $\|W_Q\|,\|W_K\|\le W_{QK}$; explicit bounded-score
  regime $|\langle q,k_t\rangle|\le S$, $S=O(1)$. **Consumers:** every
  lemma.

---

## Leaf lemmas (sections 03–07, 10) — geometry + concentration

### lem:running_average  (03; REUSE current sec 03)
**Statement (1-line):** the softmax recurrence for the UN-retracted iterate
is a running convex average $\tilde x_T=\sum_k w_{T,k}V_k$, $w\ge0$,
$\sum w=1$, $w_{T,0}=O(1/T)$.
**Hypotheses:** def:dynamics.
**Downstream consumers:** `lem:signal_floor` (cite-site step 1),
`lem:incorrect_max` (representation of $\tilde x_T$), `lem:quad_variation`.

### ~~lem:riem_gradient~~ → rem:descent_naming  (04; **Stage-2: DEMOTED to a remark per Occam**)
**Was:** a lemma DERIVING $c:=\rho_0^2-\mu_0 R_U^2$ from the incoherence gap.
**Now:** a MOTIVATION remark (`rem:descent_naming`) only. The Step-0 framing
correction redefines $\zeta_k=\operatorname{sign}(s_k)$ on the
correct-direction projection (not loss descent), so $\operatorname{grad}_R L$
has NO load-bearing consumer: $c$ is now ASSUMED in A1(b), R3' uses the
signal floor directly, and the incoherence GAP is no longer needed for $c>0$.
The remark keeps the gradient computation
$\langle W_U^{a^\star},-\nabla L\rangle\ge(1-p_{a^\star})(\rho_0^2-\mu_0R_U^2)$
purely to motivate the "descent / SGD on cross-entropy" naming; it is
explicitly NOT used in any proof. The Riemannian-gradient FORMULA stays in
`def:riem_gradient_obj` (preliminaries). **Downstream consumers (of the
remark):** none load-bearing (motivation only).

### lem:incorrect_max  (08; ADAPT current sec 04 Lemma A, union over |V|-1)
**Statement (1-line):** whp $\max_{a\neq a^\star}\langle W_U^a,\tilde x_T\rangle
\le \mu_0 R_U M + 2R_U M\sqrt{S_T\log(2(|V|-1)/\delta_1)/d}$.
**Hypotheses:** ass:A2, lem:running_average, lem:orthogonality, lem:azuma,
lem:quad_variation.
**Downstream consumers:** `thm:R1`(i) (upper bounds incorrect side),
`thm:R2` (max-incorrect term in margin decomposition).

### lem:orthogonality  (05; REUSE current sec 05 lem:orthogonality_high_d)
**Statement (1-line):** for fixed unit $e$ and $u$ uniform on $S^{d-1}$,
$\E\langle e,u\rangle^2=1/d$ and sub-Gaussian tail with proxy $C/d$
(Vershynin Thm 3.4.6).
**Hypotheses:** none (cited external, geometry).
**Downstream consumers:** `lem:incorrect_max`, `lem:signal_floor`,
`lem:azuma` (variance proxy), `lem:incorrect_max_lower`, `thm:R2`.

### lem:quad_variation  (06; REUSE current sec 04 lem:max_attention_weight)
**Statement (1-line):** under bounded scores $|\langle q,k_t\rangle|\le S$,
$S_T=\sum_t w_{T,t}^2\le e^{2S}/T$.
**Hypotheses:** ass:A2 (bounded-score regime), lem:running_average.
**Downstream consumers:** `lem:incorrect_max`, `lem:signal_floor`,
`thm:R2` (variance scale), `thm:R1` (the $1/\sqrt T$ factor — RISKY (d)).

### lem:retraction_stability  (07; NEW; Boumal Prop 5.44)
**Statement (1-line):** the normalization retraction transfers any fixed-row
logit from $\tilde x_T$ to $x_T$ with additive error $O(1/d^{1.5})$ (cubic
second-order pullback residual, radius-$\sqrt d$ rescaling).
**Hypotheses:** def:retraction, def:dynamics, ass:A2.
**Downstream consumers:** `lem:signal_floor` (transfer the floor to $x_T$ —
RISKY (b)), `thm:R1`, `thm:R3prime`.

### lem:azuma  (10; REUSE current sec 05 lem:concentration_radial_walk)
**Statement (1-line):** Freedman/Azuma tail for a martingale-difference
sum with conditional variance $\le 2\sigma^2/d$ and bounded differences.
**Hypotheses:** lem:orthogonality (variance proxy), ass:A2 (bound).
**Downstream consumers:** `lem:incorrect_max`, `lem:signal_floor`,
`lem:incorrect_max_lower`.

---

## Middle layer (sections 09, 11, 12)

### lem:signal_floor  (09; ADAPT current sec 04 Lemma B; on $\tilde x_T$ then transfer)
**Statement (1-line):** under A1+A2, whp the correct logit on the
UN-retracted iterate satisfies $\langle W_U^{a^\star},\tilde x_T\rangle\ge
\delta\,c\,\rho_0/\text{(norm)} - \text{noise}$; transfer to $x_T$ via
`lem:retraction_stability`. ($c$ from `lem:riem_gradient`.)
**Hypotheses:** ass:A1, ass:A2, lem:running_average, lem:riem_gradient,
lem:azuma, lem:quad_variation, lem:retraction_stability.
**Downstream consumers:** `thm:R1`(i) (lower bounds correct side),
`thm:R2` (drift term), `thm:R3prime` (signal level $\delta c$). RISKY (a),(b),(d).

### lem:loss_to_margin  (11; ADAPT current sec 04 loss-to-margin, |A|=1 ⇒ log2)
**Statement (1-line):** if $L(x;Q)<\log 2$ then $M(x;Q)>0$ (singleton
answer set pigeonhole).
**Hypotheses:** def:loss, def:angular_margin.
**Downstream consumers:** `thm:R1`(i) (loss→margin→TRUE-decoder success),
`thm:R3prime` (cap membership ⇒ positive margin).

### lem:incorrect_max_lower  (12; NEW; anti-concentration max-LOWER bound)
**Statement (1-line):** when $\delta$ is sub-threshold, whp
$\max_{a\neq a^\star}\langle W_U^a,x_T\rangle \ge \sigma_T\sqrt{2\kappa(1-\mu_0)\log(|V|-1)}-\mu_0 R_U|D|$
(**Sudakov minoration + Borell--TIS**, PRIMARY as of 2026-05-29, under the
isotropic-Gaussian noise form `eq:noise_gaussian` of `ass:A2`(5) used by this
lemma only; Vershynin Thm 7.4.1 + Thm 5.2.3, $\kappa\in(0,1)$ absolute Sudakov
constant). The second-moment / Paley--Zygmund route is RETIRED (unsound for
constant $\mu_0$ — see anti-concentration-max.md "Why NOT the second moment").
NOT a reversed Lemma A (a union bound only UPPER-bounds a max); NO GW.
**Hypotheses:** ass:A1 (sub-threshold), ass:A2 incl. the Gaussian noise clause
`eq:noise_gaussian`, lem:incorrect_max (scale $\sigma_T$ and the shared drift
$|D|\le\delta M$), lem:quad_variation ($S_T\le e^{2S}/T$).
**Downstream consumers:** `thm:R1`(ii) (the FAILURE branch, cite-site §13
lines ~138–151), `thm:R2` (Step 1 threshold pinning, §14 lines ~57, ~90).

---

## Result theorems (sections 13–15)

### thm:R1  (13; ADAPT current sec 07) — two-sided phase transition, TRUE decoder
**Statement (1-line):** with $\delta_c:=c_1\sqrt{\log|V|/(T_{\max}d)}$:
(i) $\delta\ge\sqrt2\,\delta_c \Rightarrow \Pr[D_{\mathrm{true}}(x_{T_{\max}})=a^\star]
\ge 1-\delta_{\mathrm{fail}}-1/(|V|-1)$;
(ii) $\delta$ below threshold $\Rightarrow \Pr[D_{\mathrm{true}}=a^\star]
\le \text{small}+1/(|V|-1)$ via anti-concentration.
**Hypotheses:** ass:A1, ass:A2; uses lem:signal_floor, lem:incorrect_max,
lem:loss_to_margin (branch i); lem:incorrect_max_lower (branch ii).
**Downstream consumers:** headline; `thm:R2` refines its window.

### thm:R2  (14; ADAPT current sec 07b) — critical-window Gaussian
**Statement (1-line):** $\Pr[D_{\mathrm{true}}=a^\star]=\Phi(z)+O(\varepsilon_{BE})$,
$z\propto(\delta-\delta_c)\sqrt{T_{\max}d}$, $\Phi(0)=1/2$ at threshold;
$\varepsilon_{BE}=O(e^S/\sqrt{T_{\max}}+\sqrt{\log|V|/(T_{\max}d)})$. Width:
ABSOLUTE $\Theta(1/\sqrt{T_{\max}d})$ (headline) vs RELATIVE
$\Theta(1/\sqrt{\log|V|})$ (remark).
**Hypotheses:** ass:A1, ass:A2; uses lem:signal_floor (centred martingale),
lem:incorrect_max, lem:quad_variation, lem:orthogonality;
\cite{hallheyde1980} Berry–Esseen.
**Downstream consumers:** terminal (with two corollaries: width, boundary).

### thm:R3prime  (15; NEW) — finite-horizon cone confinement (NOT an ODE)
**Statement (1-line):** whp, after $O(1)$ rescaled-time burn-in the
trajectory enters and stays in the cap $C=\{\cos\angle(W_U^{a^\star},x)\ge
m^\star-\varepsilon\}$; $m_{T_{\max}}$ concentrates at $\delta\cdot c$ with
$O(1/\sqrt{T_{\max}d})$ fluctuations. The ODE $\dot m=\delta c - m$ appears
ONLY as a flagged informal remark citing extra stylizations (AS)+(Lλ),
stated NOT derivable from A1. RISKY (e).
**Hypotheses:** ass:A1, ass:A2; uses lem:signal_floor, lem:riem_gradient,
lem:loss_to_margin, lem:retraction_stability, lem:azuma.
**Downstream consumers:** terminal.

---

## 99-auxiliary (cited externals)
`lem:orthogonality` and the Berry–Esseen statement may be restated as
`\begin{lemma}[\cite{vershynin2018}]` / `\begin{lemma}[\cite{hallheyde1980}]`
in 99-auxiliary if invoked in multiple proofs. (Currently kept inline in
05 and inside thm:R2; revisit in Stage 2.)

## DROPPED from current 08 (do NOT port)
- sec 06 Galton–Watson / snowball-coupling (`lem:branching_extinction`) —
  replaced by `lem:incorrect_max_lower` anti-concentration.
- sec 09 T3 problem-difficulty, sec 10 discussion, sec 11 DEQ contraction
  (T6), sec 12 ODE limit (T5) — out of scope; R3' replaces T5 as a
  finite-horizon confinement statement with the ODE demoted to a remark.
- radial Ito expansion (`lem:radial_ito_expansion`) — not needed; angle is
  tracked directly, radius is fixed at $\sqrt d$ on the sphere.
- sequence-level $\mathcal V^n$ machinery, `def:linear_surrogate_decoder`
  ($D_{\mathrm{lin}}$/$D_{\mathrm{true}}$ split) — $n=1$ honesty upgrade:
  argmax IS greedy decoding, so $D_{\mathrm{true}}=D_{\mathrm{lin}}$ and all
  statements are about the TRUE decoder directly.
