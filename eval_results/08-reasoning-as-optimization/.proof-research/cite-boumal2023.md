# \cite{boumal2023} — An Introduction to Optimization on Smooth Manifolds

**Book.** Nicolas Boumal, *An Introduction to Optimization on Smooth
Manifolds*, Cambridge University Press, 2023. ISBN 978-1-009-16616-5.
Author's PDF: https://www.nicolasboumal.net/book/ . **This reference is
pre-verified by the user** (page/equation numbers supplied in the Stage-1
brief); the digest records the exact statements we invoke so the Stage-2
proofs cite the right object.

**Exact names/locations in the book (results we cite).**

- **Riemannian gradient on a Riemannian submanifold** — §2.4 (p.~20).
  For an embedded submanifold $\mathcal M \subseteq \R^d$ with the
  Euclidean metric inherited from the ambient space, the Riemannian
  gradient of $f = \bar f|_{\mathcal M}$ at $x$ is the orthogonal
  projection of the ambient gradient onto the tangent space:
  $\operatorname{grad} f(x) = \operatorname{Proj}_x \nabla \bar f(x)$.
  For the sphere $\{x : \|x\| = r\}$ the tangent space at $x$ is
  $\{v : \langle x, v\rangle = 0\}$ and the projector is
  $\operatorname{Proj}_x = I - xx^\top/\|x\|^2$, so
  $\operatorname{grad} f(x) = (I - xx^\top/\|x\|^2)\nabla\bar f(x)$.

- **Retraction (definition)** — **Definition 3.47**.
  A retraction on a manifold $\mathcal M$ is a smooth map
  $R : T\mathcal M \to \mathcal M$, $(x,s)\mapsto R_x(s)$, such that each
  curve $c(t) = R_x(ts)$ satisfies $c(0)=x$ and $c'(0)=s$ (i.e.\
  $R_x(0)=x$ and $\mathrm{D}R_x(0) = \mathrm{Id}_{T_x\mathcal M}$,
  the "local rigidity"/centering condition).

- **Sphere normalization (metric-projection) retraction** —
  **Example 3.49, eq.~(3.32)**. On the unit sphere,
  $R_x(s) = (x+s)/\|x+s\|$. (For the radius-$r$ sphere the same formula
  with the ambient norm gives a retraction onto $\{\|x\|=r\}$ after the
  rescaling described below.) This is exactly the LayerNorm-style
  normalization map $x \mapsto \sqrt d\, x/\|x\|$ used in the paper.

- **Second-order retraction on the sphere / pullback error** —
  **Proposition 5.44, eq.~(5.30)**. The normalization retraction is a
  **second-order retraction**: the pullback $\hat f = f \circ R_x$
  agrees with $f$ to second order, so for a tangent step $s$,
  $f(R_x(s)) = f(x) + \langle \operatorname{grad} f(x), s\rangle
  + \tfrac12 \langle \operatorname{Hess} f(x)[s], s\rangle + O(\|s\|^3)$.
  Equivalently $R_x(s) = x + s - \tfrac12\|s\|^2 x + O(\|s\|^3)$ on the
  unit sphere (the $-\tfrac12\|s\|^2 x$ term is the curvature correction;
  the residual after subtracting the exponential map is $O(\|s\|^3)$).

**How we use each (Stage-2 cite-sites).**

- §2.4 (p.~20): `lem:riem_gradient` — defines
  $\operatorname{grad}_R L = (I - xx^\top/\|x\|^2)\nabla L$ and, combined
  with A2 incoherence, derives the GLOBAL drift floor $c$ on the
  un-retracted update direction $\langle \Delta\tilde x_t,
  -\operatorname{grad}_R L\rangle$.
- Def.~3.47 + Example 3.49 (eq.~3.32): `def:retraction` and
  `lem:retraction_stability` — the normalization map is the sanctioned
  retraction; centering ($R_x(0)=x$, $\mathrm DR_x(0)=\mathrm{Id}$) is the
  source of the leading-order signal transfer.
- Prop.~5.44 (eq.~5.30): `lem:retraction_stability` — the $O(\|s\|^3)$
  second-order pullback error is the SOLE provenance of the
  $O(1/d^{1.5})$ retraction-stability bound. **Radius-$\sqrt d$
  rescaling**: write $x = \sqrt d\,u$ with $u$ on the UNIT sphere and a
  unit-sphere step $\sigma = s/\sqrt d$. A single SGDM step has tangent
  size $\|s\| = \alpha\|\,\cdot\,\| = O(1)$ in ambient units (since
  $\|V_t\|\le M = O(1)$ and the tangential signal magnitude scales like
  the per-step weight), so the UNIT-sphere step is
  $\|\sigma\| = \|s\|/\sqrt d = O(1/\sqrt d)$. The Prop.~5.44 cubic
  pullback error is then $O(\|\sigma\|^3) = O(d^{-3/2}) = O(1/d^{1.5})$
  per step on the unit sphere; rescaled back to the radius-$\sqrt d$
  sphere it is the stated retraction-stability bound. (Stage-2 must pin
  the constant; see `retraction-stability.md` and
  `stage1-decisions.md` item D2.)

**Constants / dimension dependence.** Prop.~5.44 gives the cubic-error
constant as a bound on the third derivative of the normalization map on a
neighbourhood of the sphere; it is an absolute constant once the step is
inside the injectivity radius (here guaranteed by $\|\sigma\| = O(1/\sqrt d)
\ll 1$ for large $d$). No probabilistic content — this is a deterministic
differential-geometric bound.

**Common misuses (to avoid in Stage 2).**
- Do NOT apply the convex-combination identity $\sum_k w_{T,k}=1$ to the
  RETRACTED iterate $x_t$; the running-average representation holds only
  for the UN-retracted $\tilde x_T$ (Constraint #6). Prove the signal
  floor on $\tilde x_T$, THEN transfer via this lemma.
- Do NOT treat the normalization map as an isometry; it is a second-order
  retraction, and the curvature term $-\tfrac12\|s\|^2 x$ is real (it
  feeds the radial/centrifugal bookkeeping, not the tangential signal).
- Do NOT invoke the exponential map / parallel transport; the
  normalization retraction is weaker and is all we need.

**Project .bib key.** \cite{boumal2023}
