# Borell–TIS / Gaussian concentration of Lipschitz functions

**Source.** Roman Vershynin, *High-Dimensional Probability* (2018),
**Theorem 5.2.3 (Gaussian concentration)**, §5.2.1 "Gaussian
concentration" (p. 146). \cite{vershynin2018}. The underlying Gaussian
isoperimetric inequality is **Theorem 5.2.2**, which Vershynin attributes
to B. Tsirelson, I. Ibragimov and V. Sudakov [87] and C. Borell [50] —
hence the name **Borell–TIS**. (Verified verbatim against the official PDF
by direct text extraction — see `cite-vershynin2018.md`.)

**Statement (verbatim, Theorem 5.2.3).** Consider a random vector
$X\sim N(0,I_n)$ and a Lipschitz function $f:\R^n\to\R$ (with respect to
the Euclidean metric). Then
$$
   \norm{f(X)-\E f(X)}_{\psi_2} \;\le\; C\,\norm{f}_{\mathrm{Lip}}.
$$
Equivalently (sub-Gaussian-norm $\Rightarrow$ tail), there is an absolute
$c>0$ such that for every $u\ge0$,
$$
   \Pr\bigl[\,\abs{f(X)-\E f(X)}\ge u\,\bigr]
   \;\le\; 2\exp\!\Bigl(-\frac{c\,u^2}{\norm{f}_{\mathrm{Lip}}^2}\Bigr),
$$
and in particular $f(X)\ge\E f(X)-\norm{f}_{\mathrm{Lip}}\sqrt{C'\log(1/\varepsilon)}$
with probability $\ge1-\varepsilon$. The constant does **not** depend on
the dimension $n$.

**Hypotheses.**
- $X\sim N(0,I_n)$ standard Gaussian (the result is Gaussian-only; the
  same statement on the sphere is Theorem 5.1.4/5.1.3, on other product
  spaces it needs separate hypotheses).
- $f$ Lipschitz in Euclidean norm with constant $\norm{f}_{\mathrm{Lip}}$.
  No convexity, no smoothness, no boundedness required.

**Constants / dimension dependence.** Dimension-free: only
$\norm{f}_{\mathrm{Lip}}$ enters, not $n$. $C,c,C'$ absolute. Centering is
at $\E f(X)$ (the median form differs by an absolute constant).

**Canonical use pattern (max of a Gaussian vector).** Let
$G=(G_a)_{a\in S}\in\R^m$ be a centred Gaussian vector with a covariance
factorisation $G=A\,X$, $X\sim N(0,I_n)$, and let $f(x)=\max_{a\in S}(Ax)_a$.
Then $f$ is Lipschitz with $\norm{f}_{\mathrm{Lip}}=\max_a\norm{A^\top
e_a}_2=\max_a\sqrt{\Var G_a}=:\sigma$ (the max coordinate standard
deviation, since $\abs{\max_a u_a-\max_a v_a}\le\max_a\abs{u_a-v_a}\le
\norm{u-v}_2$ pointwise and each coordinate map $x\mapsto(Ax)_a$ is
$\norm{A^\top e_a}_2$-Lipschitz). Hence
$$
   \max_{a\in S}G_a \;\ge\; \E\max_{a\in S}G_a-\sigma\sqrt{2\log(1/\varepsilon)}
   \qquad\text{w.p. }\ge1-\varepsilon.
$$
Combined with a Sudakov lower bound on $\E\max_a G_a$
(`sudakov-minoration.md`) this yields a high-probability lower bound on
the max.

**Common misuses.**
- **Non-Gaussian $X$.** The theorem is for Gaussian $X$; for general
  Lipschitz concentration one needs a log-Sobolev / transport hypothesis
  (Boucheron–Lugosi–Massart Ch. 3) or sub-Gaussian-with-bounded-difference
  (McDiarmid). On a finite-$T$ sub-Gaussian (non-Gaussian) vector the
  concentration of $\max$ around its mean still holds (bounded-difference /
  convex-Lipschitz Talagrand), but pairing it with a *Sudakov lower bound*
  on $\E\max$ requires the process to be Gaussian (see
  `sudakov-minoration.md` misuses).
- **Wrong Lipschitz constant for the max.** The Lipschitz constant of
  $x\mapsto\max_a(Ax)_a$ is the **max** coordinate standard deviation
  $\max_a\norm{A^\top e_a}_2$, NOT $\norm{A}_{\mathrm{op}}$ and not the sum.
  Using $\norm{A}_{\mathrm{op}}$ over-counts.
- **Forgetting it is two-sided.** The tail bounds $\abs{f(X)-\E f(X)}$;
  for a lower bound on the max use only the lower half (no factor 2 needed
  if a one-sided statement suffices, but the factor 2 is harmless).

**Project citation key.** \cite{vershynin2018} (Theorem 5.2.3, §5.2.1;
Gaussian isoperimetry Theorem 5.2.2 = Borell–TIS).
