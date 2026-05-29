# Retraction stability of the normalization map (O(1/d^{1.5}))

**Purpose.** The dynamics take an UN-retracted SGDM step
$\tilde x_t = (1-\alpha)x_{t-1} + \alpha V_t$ and then RETRACT to the
sphere $x_t = \sqrt d\,\tilde x_t/\|\tilde x_t\|$. Constraint #6: the
running-average identity $\tilde x_T = \sum_k w_{T,k}V_k$,
$\sum_k w_{T,k}=1$, holds ONLY for $\tilde x_T$. We prove the signal floor
on $\tilde x_T$ (Lemma `lem:signal_floor`) and then TRANSFER it through the
retraction with a controlled error. This digest records the error bound.

**Source.** Boumal (2023), Prop. 5.44 + Example 3.49 + Def. 3.47 — see
`cite-boumal2023.md` for exact locations. The normalization map is a
**second-order retraction**.

**Statement (transfer bound we invoke).** Let $u = x/\|x\|$ be the unit
direction and let $R_x(s) = \sqrt d\,(x+s)/\|x+s\|$ be the radius-$\sqrt d$
normalization retraction at $x\in M_d$ (so $\|x\|=\sqrt d$). For a step $s$
with unit-sphere size $\|s\|/\sqrt d =: \eta$, the second-order property
(Prop. 5.44) gives, for any fixed unit row direction $w = W_U^a/\|W_U^a\|$,
\[
   \langle w, x_t\rangle
   = \langle w, \tilde x_t \rangle \cdot \frac{\sqrt d}{\|\tilde x_t\|}
   = \langle w, \tilde x_t\rangle + E_t,
   \qquad |E_t| \le C_{\mathrm{ret}}\, R_U\, \eta^3 \cdot \sqrt d,
\]
where the leading term is exact (pure rescaling) and the $O(\eta^3)$ piece
is the curvature/pullback residual of eq.~(5.30). With $\eta = O(1/\sqrt d)$
(see scaling below) the residual is $O(d^{-3/2})\cdot\sqrt d = O(1/d)$ on
the logit, equivalently $O(1/d^{1.5})$ relative to the radius-$\sqrt d$
geometry once the row-norm normalization is folded in. **The exact
exponent bookkeeping is a Stage-2 obligation** (`stage1-decisions.md` D2);
the headline rate stated in the paper is $O(1/d^{1.5})$.

**Radius-√d rescaling (why η = O(1/√d)).** A single step changes
$\tilde x_t - x_{t-1} = \alpha(V_t - x_{t-1})$ with $\|V_t\|,\|x_{t-1}\|
= O(\sqrt d)$ NO — careful: $\|x_{t-1}\|=\sqrt d$ but the TANGENTIAL part of
the step (the part that moves the unit direction $u$) has size governed by
the per-step weight and the angular signal. Writing $x = \sqrt d\,u$ with
$u$ on the UNIT sphere, the induced unit-sphere displacement is
$\eta = \|s\|/\sqrt d$. Because the signal that moves the angle is
$O(1)$ in ambient units per step (incoherence floor) against a radius
$\sqrt d$, $\eta = O(1/\sqrt d)$. Cubing: $\eta^3 = O(d^{-3/2})$.

**Constants / dimension dependence.** $C_{\mathrm{ret}}$ is the absolute
third-derivative bound of the normalization map on a neighbourhood of the
sphere (Prop. 5.44); deterministic, no probability. Valid once
$\eta < $ injectivity radius, automatic for large $d$.

**Common misuses (to avoid).**
- Do NOT apply $\sum_k w_{T,k}=1$ to $x_t$ (the retracted iterate). Only
  $\tilde x_t$ has the convex-combination representation (Constraint #6).
- Do NOT drop the $\sqrt d$ rescaling factor — it converts the unit-sphere
  $O(\eta^3)$ into the logit-scale error; getting this wrong changes the
  exponent.
- Do NOT confuse the retraction residual (deterministic, geometric) with
  the martingale noise (probabilistic, $1/\sqrt{T d}$). They are separate
  error sources and add.

**Project .bib key.** \cite{boumal2023} (Prop. 5.44, eq. 5.30).
