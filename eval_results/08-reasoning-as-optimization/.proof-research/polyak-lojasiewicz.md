# Polyak-Lojasiewicz drift for conditional rate

> **Status (Round 5, 2026-05-28):** The eval-08 framework no longer
> invokes the PL amplification step. T2 (convergence rate) was
> dropped entirely in Round 5: the Round-4 Path-A linear-gap
> alternative to the PL-quadratic amplification was itself dropped
> when hostile review identified a structural incompatibility
> between the Foster-Lyapunov hitting-time framing and the
> convex-combination dynamics of the softmax-running-average
> representation (\Cref{lem:softmax_running_average}); see
> `lyapunov.md` Round-5 header.
>
> **Round-4 historical note (superseded):** In Round 4 the framework
> attempted to replace the PL amplification with a Path-A linear-gap
> drift, producing a T2 rate linear in $(\rateinit - \critrate)$
> rather than quadratic; the supporting `lem:expected_drift` and
> `rem:expected_drift_no_PL` blocks (Round 4 additions in
> `sections/04-verifier-geometry.tex`) and the `T2` chapter
> (`sections/08-theorem-T2-convergence-rate.tex`) were deleted in
> Round 5.
>
> Digest retained for historical context and for possible future use
> if the framework is extended to recover a convergence-rate theorem
> via a different (non-Foster-Lyapunov) approach.

## Source

- Karimi, Nutini, Schmidt, *Linear Convergence of Gradient and
  Proximal-Gradient Methods Under the Polyak-Lojasiewicz Condition*,
  ECML PKDD 2016, LNCS 9851, pp. 795-811.
- Polyak, B. T., *Gradient methods for the minimization of functionals*,
  USSR Comput. Math. Math. Phys. 3 (1963), 643-653 (original PL paper).

## Statement (PL inequality)

A differentiable function $L : \R^d \to \R$ with global minimum
$L^*$ satisfies the Polyak-Lojasiewicz inequality with constant
$\mu > 0$ if for every $x$:
$$
   \tfrac{1}{2} \norm{\nabla L(x)}^2
   \;\ge\; \mu \cdot (L(x) - L^*).
$$

## Karimi et al. Theorem 1 (deterministic GD rate)

If $L$ is $L_{\mathrm{sm}}$-smooth and PL-$\mu$, then gradient descent
with step size $\eta = 1/L_{\mathrm{sm}}$ achieves
$$
   L(x_t) - L^*
   \;\le\; \bigl(1 - \mu/L_{\mathrm{sm}}\bigr)^t \, (L(x_0) - L^*),
$$
i.e. linear (geometric) convergence to the global minimum **without**
convexity.

## Karimi et al. Theorem 4 (biased SGD extension)

For biased stochastic gradients $g_t$ with bias $\|\E[g_t \mid \mathcal F_t]
- \nabla L(x_t)\| \le \beta$ and second-moment bound
$\E\|g_t\|^2 \le G^2$, constant-step-size SGD with $\eta = \eta_0$ satisfies
$$
   \E[L(x_T) - L^*]
   \;\le\; (1 - c_3 \eta_0 \mu)^T (L(x_0) - L^*)
       + \frac{c_4 \beta^2}{\eta_0 \mu}
$$
for constants $c_3, c_4 > 0$ depending only on $L_{\mathrm{sm}}$.

## How we use it (Theorem T2 conditional convergence)

Conditional on the snowball event, the loss process $L_t$ satisfies a
**PL-like Lyapunov drift** in expectation:
$$
   \E[L_{t+1} - L_t \mid \mathcal F_t, \mathrm{snowball}]
   \;\le\; -\eta \cdot (L_t - L^*),
   \qquad
   \eta := \lambda_0 \alpha(d) - c \sigma^2/\bar r > 0.
$$
This is the *same structural inequality* as PL gradient descent: a
multiplicative contraction of the loss gap per step, with rate
$\eta = \lambda_0\alpha(d) - \lambda_c\alpha(d) = (\lambda_0 - \lambda_c)\alpha(d)$.
Unrolling gives
$\E[L_T \mid \mathrm{snowball}] \le (1 - \eta)^T L_0$, and the hitting
time to $L \le \log 2$ satisfies
$\E[T_{\mathrm{conv}}] \le \log(L_0/\log 2) / \eta = O(1/(\lambda_0 - \lambda_c))$.

**Key adaptation.** Our drift is *additive in the gap*
($\eta(L_t - L^*)$) rather than multiplicative in $L_t$. We use the
linear version: $\E[L_{t+1} - L_t \mid \mathcal F_t] \le -\eta_0$ for
$L_t > L^*$, giving the **arithmetic** hitting-time bound
$\E[T_{\mathrm{conv}}] \le L_0/\eta_0$ instead of the
**geometric** Karimi bound. This is sufficient for the T2 polynomial-rate
statement and avoids requiring the multiplicative (PL) form.

## Constants tracked

- $\eta = \lambda_0\alpha(d) - \lambda_c \alpha(d) = (\lambda_0 - \lambda_c) \alpha(d)$
  — the drift gap to criticality.
- $L_0$ — initial loss (bounded by $L^*(Q)$ by snowball event).
- $\E[T_{\mathrm{conv}}] \le L_0 / \eta = O(L_0 / ((\lambda_0-\lambda_c)\alpha(d)))$.

In our absolute-scale parametrization with $\alpha(d) = \alpha_0\sqrt{d/d_0}$,
this gives $T_{\mathrm{conv}} = O(1/((\lambda_0-\lambda_c)\sqrt d))$
in absolute time units, which polynomial-time in $d$ (in fact decreasing
with $d$).

## Verification

Karimi et al. 2016 Theorem 1 and Theorem 4 statements verified against
the arXiv version (1608.04636). Our application uses the linear
(additive-drift) form, which is a direct specialization of the
Foster-Lyapunov criterion (see `.proof-research/lyapunov.md`). The
multiplicative (PL) form is invoked only by analogy in the T2 proof
exposition.
