# Lyapunov drift / Foster-Lyapunov supermartingale criterion

> **Status (Round 5, 2026-05-28):** The eval-08 framework no longer
> invokes Foster-Lyapunov hitting time analysis (T2 was dropped due
> to structural incompatibility with softmax-running-average's
> convex-combination dynamics: the convex-combination structure of
> the running-average representation does not compose with
> discrete-time Foster-Lyapunov supermartingale criteria, and the
> Round-4 Path-A linear-gap rate did not survive hostile review).
> Digest retained for historical context.

## Source

- Meyn, S. P. and Tweedie, R. L. *Markov Chains and Stochastic
  Stability*, 2nd ed., Cambridge University Press 2009, Chapter 11
  ("Drift and stability").
- Williams, D. *Probability with Martingales*, Cambridge 1991,
  Chapter 11 (martingale convergence in $L^1$).
- Robbins, H. and Siegmund, D. *A convergence theorem for non-negative
  almost supermartingales and some applications*, in *Optimizing
  Methods in Statistics* (J. Rustagi ed.), Academic Press 1971,
  pp. 233-257 (the Robbins-Siegmund lemma).

## Statement (drift criterion in the form we use)

Let $(L_t)_{t \ge 0}$ be a non-negative process adapted to a filtration
$(\mathcal F_t)_{t \ge 0}$. Suppose there exist measurable $V : \R_{\ge 0}
\to \R_{\ge 0}$, constants $\eta > 0$, $b < \infty$, and a closed bounded
set $K \subset \R_{\ge 0}$ such that for every $t \ge 0$:
$$
   \E[V(L_{t+1}) - V(L_t) \mid \mathcal F_t]
   \;\le\; -\eta \cdot \1\{L_t \notin K\}
       \;+\; b \cdot \1\{L_t \in K\}.
$$
Then:
- (Recurrence / positive Harris.) The process visits $K$ infinitely
  often almost surely.
- (Hitting time.) For any $L_0 \notin K$, the expected first hitting
  time satisfies
  $$
     \E[\tau_K \mid L_0]
     \;\le\; \frac{V(L_0)}{\eta},
     \qquad \tau_K := \inf\{t \ge 0 : L_t \in K\}.
  $$
- (Convergence.) If additionally $V$ is coercive and the drift
  outside $K$ is uniformly bounded away from zero, then $L_t$ is
  positive recurrent on $K$.

## Robbins-Siegmund non-negative almost-supermartingale lemma

Let $(L_t), (a_t), (b_t), (c_t)$ be non-negative adapted processes with
$$
   \E[L_{t+1} \mid \mathcal F_t]
   \;\le\; (1 + a_t) L_t - b_t + c_t,
   \qquad \sum_t a_t < \infty \text{ a.s.}, \qquad \sum_t c_t < \infty \text{ a.s.}
$$
Then $L_t$ converges to a finite random variable a.s. and
$\sum_t b_t < \infty$ a.s.

## Why we use it

Lemma `lem:supermartingale_snowball` and Lemma `lem:hitting_time_bound`
are direct instantiations:

1. **`lem:supermartingale_snowball`**: take $V(L) = L$. On the
   snowball region $\{L < L^*\}$, the drift decomposition gives
   $\E[L_{t+1} - L_t \mid \mathcal F_t] \le -\eta := -(\lambda_0 \alpha(d)
   - c \sigma^2/\bar r)$, which is negative when
   $\lambda_0 > \lambda_c := c\sigma^2/(\alpha(d) \bar r)$. Thus $L_t$
   is a non-negative supermartingale on $\{L < L^*\}$ modulo the
   boundary-leak term. Doob's convergence theorem then gives
   $L_t \to L_\infty$ a.s. with $\E L_\infty \le L_0$.

2. **`lem:hitting_time_bound`**: directly applies the hitting-time
   inequality above with $V(L) = L$, $K = [0, \log 2]$, drift
   $\eta = \lambda_0\alpha(d)/2 - c\sigma^2/(2\bar r) > 0$ in the
   supercritical regime. Yields
   $\E[T_{\mathrm{conv}}] \le 2 L_0/(\lambda_0\alpha(d) - c\sigma^2/\bar r)$.

## Constants tracked

In our use:
- $V(L) = L$ (linear Lyapunov function; this is the simplest choice
  and is justified by the drift being already in $L$-units).
- $\eta = \lambda_0\alpha(d) - c\sigma^2/\bar r$, the gap to the
  critical threshold.
- $b = O(L_{\mathrm{sm}} M^2 / d)$, the smoothness-times-bounded-norm
  contribution from the boundary leak when $L_t \uparrow L^*$.

## Verification

The drift criterion and hitting-time inequality are standard textbook
results from Meyn-Tweedie 2009 Chapter 11. The discrete-time linear
form we use is the simplest case (constant drift, bounded Lyapunov
function), and the proofs reduce to optional-stopping on the
non-negative supermartingale $V(L_t) + \eta (t \wedge \tau_K)$. We
cross-check the constants by direct expansion in
`sections/07-theorem-T1-phase-transition.tex` and
`sections/08-theorem-T2-convergence-rate.tex`.
