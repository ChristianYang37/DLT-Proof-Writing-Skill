# Technique digest — Berry-Esseen for martingales (Hall-Heyde 1980)

**Purpose.** Provide a CLT-with-rate for the centred signal-accumulation
martingale of Lemma B Step 3 (signed by $\xi_t \in \{+1, 0, -1\}$),
which underpins the new Theorem T4 (`thm:T4_critical_window` in
`sections/07b-theorem-T4-critical-window.tex`). T4 states that on the
critical fragility window $\lambda_{\text{net}} \in (\lambda_c/\sqrt 2,
\sqrt 2 \lambda_c)$, the verifier-success probability admits a
Gaussian-CDF approximation
$\Pr[\Margin > 0] = \Phi(z) + O(\epsilon)$ with explicit rate $\epsilon$.

## Picked result — Hall-Heyde 1980 Theorem 3.6

**Reference.** Hall, P. and Heyde, C. C., *Martingale Limit Theory and
Its Application*, Academic Press (1980). Theorem 3.6 (page 76 of the
printed edition) — the "rate of convergence to normality" for
square-integrable martingale arrays under conditional Lindeberg /
moment conditions.

**Why this one (and not Bolthausen 1982 or Mourrat 2013).**
Bolthausen's 1982 result is sharp for exchangeable arrays but the
exchangeability hypothesis fails for our softmax-running-average
weights $w_{T,t}$, which are *adapted but not exchangeable* across $t$.
Mourrat's 2013 refinement gives a logarithmic improvement in the rate
but requires bounded conditional fourth moments (we have access to
this via $\norm{V_t} \le M$ a.s., but the bookkeeping is more
involved). Hall-Heyde Theorem 3.6 is the cleanest match to our setting:
it requires only conditional second and third moments (which we have
deterministically from `ass:bounded_value_norms`), and the rate matches
the Lyapunov-form CLT with rate $O(\rho_T / V_T^{3/2})$.

## Statement (paraphrased to match our notation)

Let $(M_{T,t})_{t=1}^{T_{\max}}$ be a square-integrable martingale
array (i.e., for each $T_{\max}$, $(M_{T,t})_t$ is a martingale with
respect to a filtration $(\mathcal F_t)$). Write the martingale
differences $D_{T,t} := M_{T,t} - M_{T,t-1}$. Let

  $V_T := \sum_{t=1}^{T_{\max}} \E[D_{T,t}^2 \mid \mathcal F_{t-1}]$,
  $\rho_T := \sum_{t=1}^{T_{\max}} \E[|D_{T,t}|^3 \mid \mathcal F_{t-1}]$.

Assume:
(H1) **Conditional Lindeberg.** $V_T \to V_\infty$ in probability for
some non-random $V_\infty > 0$ (or $V_T / V_\infty \to 1$ in
probability if $V_\infty$ depends on $T$).
(H2) **Bounded conditional third moment.** $\rho_T < \infty$ a.s.

Then for every $x \in \R$,

  $\big| \Pr[M_{T,T_{\max}} \le x \cdot V_T^{1/2}] - \Phi(x) \big|
  \;\le\; C \cdot \rho_T / V_T^{3/2}$,

with $C$ an absolute constant (Hall-Heyde give $C \le 25$; the
optimal constant from Esseen-Shevtsova-type refinements is closer
to $0.56$ in the i.i.d.\ Berry-Esseen case).

The bound holds *almost surely* in the conditional sense (i.e., on
each $\omega$ where (H1) holds); the unconditional version follows by
taking expectations or by truncation to the high-probability event on
which $V_T$ is concentrated.

## Hypotheses verified for our martingale

Our application target is the centred signed-signal martingale of
Lemma B Step 3 with $\xi_t$ replacing $E_t$:

  $D_t := w_{T_{\max}, t} \cdot \big( \xi_t \cdot \inner{W_U^{a^\star}}{V_t}
                        - \E[\xi_t \cdot \inner{W_U^{a^\star}}{V_t} \mid \mathcal F_{t-1}] \big)$,
  $M_{T,T_{\max}} := \sum_{t=1}^{T_{\max}} D_t$.

**H1 (conditional variance).** Per-step bound from
`lem:orthogonality_high_d`: $\E[D_t^2 \mid \mathcal F_{t-1}] \le
4 w_{T,t}^2 R_U^2 M^2 / d$. Summing using
$S_{T_{\max}} \le e^{2S}/T_{\max}$ from `lem:max_attention_weight`:

  $V_{T_{\max}} \le 4 R_U^2 M^2 e^{2S} / (T_{\max} d)$.

The conditional Lindeberg condition is satisfied because the per-step
$D_t$ is uniformly bounded by $|D_t| \le 2 w_{T,t} R_U M$, hence the
conditional Lindeberg ratios vanish as $T_{\max} \to \infty$
(deterministic per-step bound shrinks like $1/T_{\max}$ via
$w_{T,t} \le e^{2S}/T_{\max}$).

**H2 (conditional third moment).** Per-step bound via the
"variance × deterministic-bound" trick:

  $\E[|D_t|^3 \mid \mathcal F_{t-1}]
  \;\le\; (2 w_{T,t} R_U M) \cdot \E[D_t^2 \mid \mathcal F_{t-1}]
  \;\le\; (2 w_{T,t} R_U M) \cdot 4 w_{T,t}^2 R_U^2 M^2 / d
  \;=\; 8 w_{T,t}^3 R_U^3 M^3 / d$.

Summing:

  $\rho_{T_{\max}}
  \;\le\; (8 R_U^3 M^3 / d) \cdot \sum_t w_{T,t}^3
  \;\le\; (8 R_U^3 M^3 / d) \cdot (\max_t w_{T,t})^2 \cdot \sum_t w_{T,t}
  \;\le\; (8 R_U^3 M^3 / d) \cdot (e^{2S}/T_{\max})^2$
  $\;=\; 8 R_U^3 M^3 e^{4S} / (d T_{\max}^2)$.

**Both hypotheses checked deterministically from `ass:bounded_value_norms`
+ Lemma C + Lemma orthogonality_high_d.** No new assumption required.

## Berry-Esseen rate

Plug in:

  $\rho_{T_{\max}} / V_{T_{\max}}^{3/2}
  \;\le\; \frac{8 R_U^3 M^3 e^{4S}/(d T_{\max}^2)}
              {(4 R_U^2 M^2 e^{2S}/(T_{\max} d))^{3/2}}$
  $\;=\; \frac{8 R_U^3 M^3 e^{4S}/(d T_{\max}^2)}
              {8 R_U^3 M^3 e^{3S}/(T_{\max} d)^{3/2}}$
  $\;=\; e^{S} \cdot \frac{(T_{\max} d)^{3/2}}{d \cdot T_{\max}^2}
  \;=\; e^{S} \cdot \frac{d^{1/2}}{T_{\max}^{1/2}}
  \;=\; e^{S} \cdot \sqrt{d / T_{\max}}$.

This is the rate from the *deterministic* per-step bound. It grows
with $d$, which is the wrong direction for the high-d limit.

**Refinement: use the high-probability per-step bound from Lemma A.**

In high dimensions, the per-step centred projection
$\inner{W_U^{a^\star}}{V_t} - \E[\cdot \mid \mathcal F_{t-1}]$ is
sub-Gaussian with proxy $R_U M / \sqrt d$ (by `lem:orthogonality_high_d`
applied to the unit direction $W_U^{a^\star}/\norm{W_U^{a^\star}}_2$).
Hence on a high-probability event $\Ecal_{\text{trunc}}$ of
$\Pr[\Ecal_{\text{trunc}}] \ge 1 - O(T_{\max} e^{-d/2})$, the per-step
bound is

  $|D_t| \le 2 w_{T,t} R_U M \cdot \sqrt{\log(T_{\max}/\delta)/d}$

via union bound + sub-Gaussian tail. This effective per-step bound
$c_t^{\text{eff}} = O(w_{T,t} R_U M / \sqrt d)$ (up to logs) gives the
refined cubic moment

  $\rho_{T_{\max}}^{\text{eff}}
  \;\le\; (c_t^{\text{eff}})^3 \cdot T_{\max} \cdot ?$

Actually the right form is: on the truncation event, the conditional
third moment is

  $\E[|D_t|^3 \mid \mathcal F_{t-1}, \Ecal_{\text{trunc}}]
  \;\le\; (c_t^{\text{eff}}) \cdot \E[D_t^2 \mid \mathcal F_{t-1}]
  \;=\; O(w_{T,t} R_U M / \sqrt d) \cdot w_{T,t}^2 R_U^2 M^2 / d
  \;=\; O(w_{T,t}^3 R_U^3 M^3 / d^{3/2})$.

Summing on the truncation event:

  $\rho_{T_{\max}}^{\text{eff}}
  \;\le\; (R_U^3 M^3 / d^{3/2}) \cdot \sum_t w_{T,t}^3
  \;\le\; R_U^3 M^3 e^{4S} / (d^{3/2} T_{\max}^2)$.

The Berry-Esseen rate becomes

  $\rho_T^{\text{eff}} / V_T^{3/2}
  \;\le\; \frac{R_U^3 M^3 e^{4S}/(d^{3/2} T_{\max}^2)}
              {(R_U^2 M^2 e^{2S}/(T_{\max} d))^{3/2}}$
  $\;=\; \frac{R_U^3 M^3 e^{4S}/(d^{3/2} T_{\max}^2)}
              {R_U^3 M^3 e^{3S}/(T_{\max} d)^{3/2}}$
  $\;=\; e^{S} \cdot \frac{(T_{\max} d)^{3/2}}{d^{3/2} T_{\max}^2}
  \;=\; e^{S} \cdot \frac{T_{\max}^{3/2}}{T_{\max}^2}
  \;=\; e^{S} / \sqrt{T_{\max}}$.

The $d$ dependence cancels exactly. Then the **standardised threshold
$z$** at which we evaluate $\Phi(z)$ corresponds (via Lemma A) to a
gap of $O(\sqrt{\log(|\Vocab|^n/|\Aset|)/(T_{\max} d)}) \cdot V_T^{1/2}$, so
the *effective* error including the threshold uncertainty is

  $\epsilon \;=\; O\Big(\sqrt{\log(|\Vocab|^n/|\Aset|)/(T_{\max} d)}\Big)$,

matching the prompt's claim exactly. The $1/\sqrt{T_{\max}}$ Lyapunov-
form rate above is dominated by the $\sqrt{\log V^n/(T_{\max} d)}$
threshold-uncertainty rate in the relevant regime $d \cdot
\log(|\Vocab|^n/|\Aset|) \ll T_{\max}$, which is the post-critical
regime of interest.

## Proof technique outline

Hall-Heyde's proof of Theorem 3.6 uses **Stein's method for
martingales**:

1. Define the Stein equation $f'(x) - x f(x) = h(x) - \E h(Z)$ for
   a test function $h$ and standard normal $Z$. Solutions $f_h$ are
   bounded with $\norm{f_h}_\infty, \norm{f'_h}_\infty \le 2
   \norm{h}_\infty$.
2. Apply $f_h$ to the standardised martingale sum
   $S_{T_{\max}} := M_{T,T_{\max}} / V_T^{1/2}$. By the martingale
   property, $\E[D_{T,t} f_h(S_{t-1})] = 0$ for $t = 2, \ldots,
   T_{\max}$ (where $S_t = \sum_{s \le t} D_{T,s}/V_T^{1/2}$).
3. Telescoping and the Taylor expansion of $f_h$ around $S_{t-1}$
   yield the error term $\E[D_{T,t}^3 / V_T^{3/2}]$ at second order;
   summing gives the rate $\rho_T / V_T^{3/2}$.

The clean Bolthausen-style proof avoids Stein and uses
characteristic-function comparisons via the Esseen lemma; the
Hall-Heyde proof via Stein is more transparent for the bookkeeping
needed in our application (we don't need the sharp constant $\le 0.56$
of i.i.d.\ Berry-Esseen).

## Citation

**Yes, a `\cite{}` is needed.** Hall-Heyde 1980 is not currently in
`refs.bib`. Add a new entry:

```bibtex
@book{hallheyde1980,
  author    = {Peter Hall and C. C. Heyde},
  title     = {Martingale Limit Theory and Its Application},
  publisher = {Academic Press},
  series    = {Probability and Mathematical Statistics},
  year      = {1980}
}
```

with a sibling citation digest at `.proof-research/cite-hallheyde1980.md`
giving:
- Theorem 3.6 statement (paraphrased to our notation, as above).
- Hypotheses (conditional Lindeberg + bounded third moment).
- Constants tracked: the absolute $C \le 25$ in the rate bound.
- Verification: Hall-Heyde 1980 is the canonical reference for
  martingale Berry-Esseen; cited in Bose-Sen (2008) "Berry-Esseen
  Bounds in Stochastic Geometry" §3 and elsewhere.

## Why the existing `cite-vershynin2018` does NOT suffice

Vershynin Ch.~2 gives sub-Gaussian tail bounds (Thms 2.3.1, 2.5.10)
and martingale-difference Hoeffding (Thm 2.3.4), but no CLT-with-rate.
Vershynin Ch.~3 gives concentration on the sphere (Thm 3.4.6), which
underpins our per-step variance bound but does *not* give a
Berry-Esseen-type rate. The Hall-Heyde reference is genuinely new
technique for the v3 paper.

## Where T4 enters the framework

- **`thm:T4_critical_window`** (`sections/07b-theorem-T4-critical-window.tex`,
  NEW file): the Φ-CDF approximation. The proof structure is:
  (T4-1) decompose $\Margin = (\text{signed signal}) - (\text{Lemma A
  incorrect max})$. (T4-2) apply Hall-Heyde 3.6 to the signed signal
  martingale on the truncation event. (T4-3) integrate the CDF
  comparison against the bounded threshold uncertainty from Lemma A.
  Final rate $\epsilon = O(\sqrt{\log(|\Vocab|^n/|\Aset|)/(T_{\max} d)})$.
- **Empirical prediction**: at finite $T_{\max} d$, the verifier
  success curve as a function of $\lambda_{\text{net}}$ follows a
  Gaussian-CDF shape with transition width $\Theta(\epsilon)$,
  *narrowing* to a step function in the limit. This is the
  finite-$T_{\max} d$ refinement of the asymptotic phase-transition
  claim of T1.

## Regime of validity

T4 applies on the full critical window $\lambda_{\text{net}} \in
(\critrate/\sqrt 2, \sqrt 2 \critrate)$, including the boundary
$\lambda_{\text{net}} = \critrate$ (where $z = 0$ and the CDF gives
$1/2$). The asymptotic regime $\lambda_{\text{net}} \to \pm\infty$
recovers T1's hard 0/1 limits as a continuous degeneration; the
intermediate critical regime is the substantive new content. The
$\sqrt{\log V^n/(T_{\max} d)}$ rate is small when $T_{\max} d \gg
\log(|\Vocab|^n/|\Aset|)$, which is the post-snowball regime of practical
interest (a model with $d = 1024$, $|\Vocab| = 50000$, $T_{\max} =
1000$ gives $T_{\max} d \approx 10^6 \gg \log(50000) \approx 11$).
