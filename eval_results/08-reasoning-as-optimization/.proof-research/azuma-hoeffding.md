# Azuma-Hoeffding martingale concentration

## Source

- Vershynin, *High-Dimensional Probability* (2018), Theorem 2.3.4
  (page 31 of printed edition).
- Boucheron, Lugosi, Massart, *Concentration Inequalities*, Oxford
  2013, §2.8 (one-sided bounded-difference inequality).

## Statement

Let $(M_t)_{t \ge 0}$ be a real-valued martingale with respect to a
filtration $(\mathcal F_t)$, with $M_0 = 0$ and martingale differences
$D_t := M_t - M_{t-1}$ satisfying $|D_t| \le c_t$ a.s. for each
$t \ge 1$. Then for every $T > 0$ and every $u > 0$:
$$
   \Pr\!\left[\,
      \max_{1 \le t \le T} M_t \;\ge\; u
   \,\right]
   \;\le\;
   \exp\!\left(\,
      -\frac{u^2}{2 \sum_{s=1}^{T} c_s^2}
   \,\right),
$$
and the two-sided form $\Pr[\max_t |M_t| \ge u] \le 2\exp(-u^2/(2\sum
c_s^2))$ follows by a union bound on $M_t$ and $-M_t$.

The "max over $t$" form (running maximum) is a consequence of Doob's
maximal inequality applied to the supermartingale $\exp(\lambda M_t -
\lambda^2 \sum_{s \le t} c_s^2/2)$.

## Refinement: bounded conditional variance (Bernstein form)

When the conditional variance $V_T := \sum_{t \le T} \E[D_t^2 \mid
\mathcal F_{t-1}]$ is much smaller than the bounded-difference proxy
$\sum c_t^2$, the Freedman 1975 / Bernstein-for-martingales bound
sharpens the exponent: under $|D_t| \le c$ and $V_T \le v$ a.s.,
$$
   \Pr\!\left[\, M_T \ge u,\; V_T \le v \,\right]
   \;\le\; \exp\!\left(\,
      -\frac{u^2}{2(v + c u / 3)}
   \,\right).
$$
We invoke this refinement in the proof of Theorem T1 via the
existing digest `cite-freedman1975tail.md`.

## Why we use it

Lemma `lem:concentration_radial_walk` applies Azuma-Hoeffding to the
running sum of radial-walk martingale increments. The setup:

- Per-step radial fluctuation $M_t = \Delta r_t - \E[\Delta r_t \mid \mathcal F_t]$.
- Bounded difference: $|M_t| \le 2\sigma$ a.s. (since
  $|\Delta r_t| \le \|g_t\| \le \sigma + \alpha(d) M/(\sqrt{d/d_0})$
  by triangle inequality; we use the loose bound $|M_t| \le c_M$ with
  $c_M = O(\sigma)$).
- Conditional variance: $\E[M_t^2 \mid \mathcal F_t] \le \sigma^2/d$ by
  the high-d orthogonality (lem:orthogonality_high_d).

The Bernstein form gives, for $u = R\sqrt{T \log(2/\delta)} / \sqrt d$:
$$
   \Pr\!\left[\,
      \max_{t \le T} \left|\sum_{s\le t} M_s\right| > u
   \,\right] \;\le\; \delta.
$$
This is precisely the union-bound discharge for the $(1-\delta)$
probability in the T1 snowball-branch theorem.

## Constants tracked

- $c_t \equiv c_M = O(\sigma)$ — uniform per-step bound (using $|g_t|
  \le \sigma + \alpha(d)$ in the bounded-value-norm regime).
- $v_T = \sigma^2 T / d$ — conditional variance bound from
  lem:orthogonality_high_d.
- Resulting tail: $\Pr[\max |\sum M_s| > u] \le 2\exp(-u^2 d / (2 \sigma^2 T))$
  in the Azuma form; Bernstein gives $\exp(-u^2 d / (2\sigma^2 T + c_M u/3 \cdot \sqrt d))$
  which is sharper for small $u$.

## Verification

Statement matches Vershynin Theorem 2.3.4 verbatim modulo notation.
The running-max version is standard (Doob's maximal inequality applied
to the exponential supermartingale). Constants for our use are checked
in `sections/05-random-walk-concentration.tex` proof.
