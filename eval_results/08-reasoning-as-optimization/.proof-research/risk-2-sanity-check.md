# Risk 2 numerical sanity check — bias floor vs convergence rate

**Question.** Under the proposed (GC-bounded-bias) assumption, does the
bias floor $c \beta^2 / \eta_0$ wash out the convergence rate at
realistic $(\beta, \eta_0)$, making the headline theorem vacuous at
empirically relevant $T \le 10^5$?

**Verdict.** **YELLOW** (with one **RED-leaning** caveat about the
underlying assumption itself; see §4).

**TL;DR.**

* For *untrained* random-weight transformers, the **(GC-bounded-bias)
  assumption fails at its precondition**: the empirical $\hat\eta_j$ is
  symmetric around zero (frac. negative $\approx 0.50$ across $|C| \in
  \{1,3,10\}$), so there is *no* $\eta_0 > 0$ such that
  $\E[g_j \mid \F_{j-1}] = -\eta_j \nabla L + b_j$ holds with bounded
  $b_j$. This is the strongest finding of the sanity check.
* A tiny amount of stylized "training" alignment ($\alpha \ge 0.1$ of
  the value vector pointing toward $W_U^\top \mathbf 1_C$) **flips this
  completely**: frac. negative drops to $0$ and the floor under
  $c = L_{\mathrm{sm}}/2$ at the median regime becomes $0.029 \cdot
  \log 2$ for $\alpha = 0.1$, $0.009 \cdot \log 2$ for $\alpha = 0.3$,
  $0.005 \cdot \log 2$ for $\alpha = 0.5$. The headline bound becomes
  non-vacuous under any of these.
* The **floor is not the binding constraint** at realistic $T$ — break-even
  $T$ exceeds $10^9$ in every regime that matters, so the rate term
  $L_0 / (\eta_0 \sqrt T)$ dominates at $T \le 10^5$. The headline
  reads "rate is $O(1/\sqrt T)$ down to a small floor"; this is
  qualitatively the desired story.

This implies the **(GC-bounded-bias) framing only works if it is sold
as a property of *trained* reasoning models**, not as a structural
fact. The proposal should either explicitly postulate trained-policy
behaviour or use the (GC-correlated) form as a fallback. See §5
recommendations.

---

## 1. Setup

Stylized one-layer one-head transformer with weights drawn fresh per
init from $\mathcal N(0, 1/d)$:
$V = 1000,\ d = 64,\ d_h = 16,\ T = 256$ trajectory length,
$W_U \in \R^{V \times d}$ (per-row $\sim \mathcal N(0, I/d)$, so each
row has unit-norm in expectation and $\|W_U\|_{\mathrm{op}} \approx 4.9$
in practice — see Task A), $W_Q, W_K \in \R^{d \times d_h}$,
$W_V \in \R^{d \times d}$. Random trajectory tokens
$h_t \sim \mathcal N(0, I/d)$, $t = 0, \dots, T-1$. Query at
`</think>`: $q = W_Q^\top h_{\text{eot}}$ for a fresh random
$h_{\text{eot}}$.

Hidden state along the trajectory follows the proposal's recurrence
$x_j = (s_{j-1}/s_j) x_{j-1} + g_j$, equivalent to the
softmax-weighted average of $V_i := W_V^\top h_i$ up to step $j$:
$$
   x_j \;=\; \frac{1}{s_j} \sum_{i=1}^j e^{\langle q, k_i\rangle} V_i,
   \quad s_j = \sum_{i=1}^j e^{\langle q, k_i\rangle}.
$$
Per-step "gradient signal" $g_j = (e^{\langle q,k_j\rangle}/s_j) V_j$.

For each (init, question) pair, evaluate at probe positions
$j \in \{8, 32, 128\}$:

1. $\nabla L = W_U^\top (p(x_{j-1}) - q_C(x_{j-1}))$ analytically;
2. $\E[g_j \mid \F_{j-1}]$ by Monte-Carlo over $K = 50$ fresh draws of
   the next-token hidden $h_j$ (uniform-over-vocab proxy: just
   resample $h_j \sim \mathcal N(0, I/d)$);
3. $\hat\eta_j = -\langle \E[g_j], \nabla L\rangle / \|\nabla L\|^2$;
4. $\hat b_j = \E[g_j] + \hat\eta_j \nabla L$, $\hat\beta = \|\hat b_j\|$.

Sweep: $100$ inits $\times$ $100$ questions per init $\times$
$3$ probes per trajectory $= 30{,}000$ triples per $|C|$ value, for
$|C| \in \{1, 3, 10\}$. Random seeds for reproducibility (seed
$= 12345 + |C|$).

Code: `/tmp/risk-2-sanity-check.py`. Runtime $\approx 19$ s on a
laptop.

---

## 2. Task A — empirical $(\hat\eta_j, \hat\beta)$ distributions

Untrained random init. Distributions over all $30{,}000$ triples per
$|C|$.

| $|C|$ | $\|W_U\|_{\mathrm{op}}$ (med) | $L_{\mathrm{sm}}$ | $L_0$ (mean loss) | $\|\nabla L\|$ (p50) | $\hat\beta$ p10 / p50 / p90 | $\hat\eta_j$ p10 / p50 / p90 | frac. $\hat\eta_j < 0$ |
|-------|------------------------------|-------------------|-------------------|---------------------|-----------------------------|-----------------------------|--------------------------|
| 1     | 4.90                         | 12.02             | 6.91              | 0.994               | $1.01\mathrm e^{-3}$ / $4.21\mathrm e^{-3}$ / $1.65\mathrm e^{-2}$ | $-1.13\mathrm e^{-3}$ / $-2.57\mathrm e^{-6}$ / $1.13\mathrm e^{-3}$ | **0.503** |
| 3     | 4.91                         | 12.06             | 5.81              | 0.574               | $1.01\mathrm e^{-3}$ / $4.21\mathrm e^{-3}$ / $1.65\mathrm e^{-2}$ | $-1.97\mathrm e^{-3}$ / $1.33\mathrm e^{-6}$ / $1.90\mathrm e^{-3}$ | **0.499** |
| 10    | 4.90                         | 12.01             | 4.61              | 0.314               | $1.01\mathrm e^{-3}$ / $4.19\mathrm e^{-3}$ / $1.65\mathrm e^{-2}$ | $-3.59\mathrm e^{-3}$ / $-6.08\mathrm e^{-6}$ / $3.55\mathrm e^{-3}$ | **0.503** |

Notes.
* $L_0$ at random init is $\approx -\log(|C|/V) = \log(V/|C|)$ ($\log 1000 \approx 6.9$,
  $\log 333 \approx 5.8$, $\log 100 \approx 4.6$). Confirms uniform-ish
  posterior at init.
* $\hat\beta$ scales tightly with $\|x_{j-1}\|$ and the
  $e^{\langle q,k_j\rangle}/s_j$ weight, **not** with $|C|$. This is a
  property of the *attention smoothing*: $\|g_j\|$ is roughly
  $\|V_j\| / j$, independent of the loss geometry.
* **Critical:** $\hat\eta_j$ is **symmetric around zero** — the median
  $\hat\eta_j$ is within numerical noise of $0$, and $\approx 50\%$ of
  the triples have $\hat\eta_j < 0$. This means: for an *untrained*
  random model, the expected attention-weighted value vector
  $\E[g_j \mid \F_{j-1}]$ is **not even directionally aligned with**
  $-\nabla L$ on average. There is no $\eta_0 > 0$ such that
  (GC-bounded-bias) holds with bounded $b_j$ across $50\%$ of cases.

---

## 3. Task B — floor for each regime

Floor $:= c \cdot \hat\beta^2 / \hat\eta_0$, computed from quantiles
of $\hat\eta_j$ over the **positive subset only** (since the negative
subset trivially violates the assumption). Reported relative to
$\log 2 \approx 0.693$, the decoding-correctness threshold.

Break-even $T$ = value of $T$ where $L_0 / (\hat\eta_0 \sqrt T) =
\text{floor}$, i.e. $T = (L_0 / (\hat\eta_0 \cdot \text{floor}))^2$.

### 3.1 Untrained random model ($|C| = 1$, c = $L_{\mathrm{sm}}/2$ — the standard biased-SGD constant)

| Regime | $\hat\eta_0$ | $\hat\beta$ | floor | floor $/\log 2$ | break-even $T$ |
|--------|-------------|-------------|-------|-----------------|----------------|
| optimistic   | $2.04\mathrm e^{-3}$ | $1.01\mathrm e^{-3}$ | $3.00\mathrm e^{-3}$ | **$4.3\mathrm e^{-3}$** | $1.27\mathrm e^{12}$ |
| **median**   | $2.95\mathrm e^{-4}$ | $4.21\mathrm e^{-3}$ | $0.360$              | **$0.520$**             | $4.22\mathrm e^{9}$  |
| pessimistic  | $3.88\mathrm e^{-5}$ | $1.65\mathrm e^{-2}$ | $42.4$               | $61.1$                  | $1.77\mathrm e^{7}$  |

### 3.2 Untrained random model ($|C| = 3$, c = $L_{\mathrm{sm}}/2$)

| Regime | $\hat\eta_0$ | $\hat\beta$ | floor | floor $/\log 2$ | break-even $T$ |
|--------|-------------|-------------|-------|-----------------|----------------|
| optimistic   | $3.42\mathrm e^{-3}$ | $1.00\mathrm e^{-3}$ | $1.77\mathrm e^{-3}$ | **$2.6\mathrm e^{-3}$** | $9.17\mathrm e^{11}$ |
| **median**   | $5.08\mathrm e^{-4}$ | $4.19\mathrm e^{-3}$ | $0.208$              | **$0.301$**             | $3.01\mathrm e^{9}$  |
| pessimistic  | $6.63\mathrm e^{-5}$ | $1.65\mathrm e^{-2}$ | $24.8$               | $35.7$                  | $1.25\mathrm e^{7}$  |

### 3.3 Untrained random model ($|C| = 10$, c = $L_{\mathrm{sm}}/2$)

| Regime | $\hat\eta_0$ | $\hat\beta$ | floor | floor $/\log 2$ | break-even $T$ |
|--------|-------------|-------------|-------|-----------------|----------------|
| optimistic   | $6.41\mathrm e^{-3}$ | $1.01\mathrm e^{-3}$ | $9.53\mathrm e^{-4}$ | **$1.4\mathrm e^{-3}$** | $5.70\mathrm e^{11}$ |
| **median**   | $9.35\mathrm e^{-4}$ | $4.21\mathrm e^{-3}$ | $0.114$              | **$0.164$**             | $1.87\mathrm e^{9}$  |
| pessimistic  | $1.25\mathrm e^{-4}$ | $1.65\mathrm e^{-2}$ | $13.1$               | $18.8$                  | $7.93\mathrm e^{6}$  |

### 3.4 Loose constant $c = 1$

For completeness, all numbers above scale by $1 / (L_{\mathrm{sm}}/2) \approx 1/6$.
The qualitative picture is unchanged:

- Optimistic floor $/\log 2 \approx 10^{-4}$ across $|C|$ — trivially non-vacuous.
- Median floor $/\log 2$: $0.087$ ($|C|=1$), $0.050$ ($|C|=3$), $0.027$ ($|C|=10$).
- Pessimistic floor $/\log 2$: $10.2$ ($|C|=1$), $5.9$ ($|C|=3$), $3.1$ ($|C|=10$).

So with the loose constant $c = 1$ the **median** is non-vacuous
($0.03$-$0.09 \times \log 2$). The standard biased-SGD constant
$c = L_{\mathrm{sm}}/2 \approx 6$ pushes the median for $|C| = 1$ to
$0.52 \times \log 2$ — **borderline**.

### 3.5 Break-even analysis

The break-even $T$ at which the rate term $L_0 / (\hat\eta_0 \sqrt T)$
matches the floor exceeds $10^9$ in every non-pessimistic regime. Since
the user's empirically relevant range is $T \le 10^5$, the **rate term
dominates the floor at all relevant $T$**. This is good for the bound's
binding constraint (the floor is **not** the actual stopping criterion
empirically), but it means the rate term itself is the bottleneck:

$$
   \frac{L_0}{\hat\eta_0 \sqrt T} \;\Big|_{T=10^5, \hat\eta_0 = 5\mathrm e^{-4}, L_0 = 5.8}
   \;\approx\; \frac{5.8}{5\mathrm e^{-4} \cdot \sqrt{10^5}} \;\approx\; 36{,}600.
$$

The rate term at $T = 10^5$ is **$\sim 10^4 \times \log 2$**, i.e. the
theorem provides no information about decoding at empirically realistic
$T$ even ignoring the floor. The bottleneck is the small $\hat\eta_0$,
not the floor.

To reach $\E[L(x_T)] \lesssim \log 2$ via the rate term alone (median
$\hat\eta_0 \approx 5\mathrm e^{-4}$, $L_0 \approx 5.8$):
$$
   T_{\text{rate, to log 2}} \;\gtrsim\; (L_0 / (\hat\eta_0 \log 2))^2
   \;\approx\; (5.8 / (5\mathrm e^{-4} \cdot 0.69))^2 \;\approx\; 3 \times 10^8.
$$

So $T \approx 3 \times 10^8$ steps are needed just for the rate term to
drop below $\log 2$. **This is the binding constraint, not the floor.**
The floor is comfortably $< \log 2$ in the median regime under $c=1$ and
borderline under $c = L_{\mathrm{sm}}/2$.

---

## 4. Task C — realistic-training improvement factor

Stylized "training" makes each value vector partially align with the
correct-token direction $W_U^\top \mathbf 1_C$. Operationalisation: for
fraction $\alpha \in \{0.1, 0.3, 0.5\}$, rotate the value vector so that
its expected inner product with the unit vector
$\widehat{W_U^\top \mathbf 1_C}$ equals $\alpha \cdot \|V_j\|$
(preserving $\|V_j\|$ otherwise). All other settings as Task A,
$|C| = 3$, $50$ inits $\times$ $100$ questions.

| $\alpha$ | frac. $\hat\eta_j < 0$ | $\hat\eta_j$ p10 / p50 / p90 | $\hat\beta$ p10 / p50 / p90 | floor (median, $c=L_{\mathrm{sm}}/2$) | floor $/\log 2$ | break-even $T$ |
|----------|------------------------|-----------------------------|------------------------------|---------------------------------------|------------------|----------------|
| 0 (Task A) | 0.499 (degenerate) | $-2.0\mathrm e^{-3}$ / $\sim 0$ / $1.9\mathrm e^{-3}$ | $1.0\mathrm e^{-3}$ / $4.2\mathrm e^{-3}$ / $1.6\mathrm e^{-2}$ | $0.208$ | $0.301$ | $3.0\mathrm e^{9}$ |
| 0.1 | **0.000** | $1.29\mathrm e^{-3}$ / $5.27\mathrm e^{-3}$ / $2.02\mathrm e^{-2}$ | $1.01\mathrm e^{-3}$ / $4.22\mathrm e^{-3}$ / $1.65\mathrm e^{-2}$ | $0.0203$ | **$0.0293$** | $2.9\mathrm e^{9}$ |
| 0.3 | **0.000** | $3.86\mathrm e^{-3}$ / $1.58\mathrm e^{-2}$ / $6.07\mathrm e^{-2}$ | $9.73\mathrm e^{-4}$ / $4.08\mathrm e^{-3}$ / $1.59\mathrm e^{-2}$ | $0.00631$ | **$0.00910$** | $3.2\mathrm e^{9}$ |
| 0.5 | **0.000** | $6.48\mathrm e^{-3}$ / $2.65\mathrm e^{-2}$ / $1.02\mathrm e^{-1}$ | $9.21\mathrm e^{-4}$ / $3.84\mathrm e^{-3}$ / $1.52\mathrm e^{-2}$ | $0.00335$ | **$0.00483$** | $3.9\mathrm e^{9}$ |

Key takeaways.

* **The assumption's precondition holds under any nonzero alignment.**
  Frac. negative drops from $\approx 0.5$ at $\alpha = 0$ to $0.000$
  at $\alpha \ge 0.1$. This is the single most important quantity.
* **$\hat\beta$ barely changes** across $\alpha$ values: $\alpha = 0.5$
  reduces median $\hat\beta$ by $\sim 9\%$ vs. random init
  ($4.21 \to 3.84\mathrm e^{-3}$). The bias norm is dominated by the
  *perpendicular component* of $V_j$, which alignment leaves untouched.
* **$\hat\eta_j$ scales linearly with $\alpha$** (median: $5.3\mathrm e^{-3}, 1.6\mathrm e^{-2}, 2.7\mathrm e^{-2}$
  for $\alpha = 0.1, 0.3, 0.5$). This is the standard "trained policy
  pushes attention-weighted values along $\nabla L$ direction" effect.
* **Floor under $c = L_{\mathrm{sm}}/2$ becomes comfortably
  non-vacuous**: $0.029, 0.0091, 0.0048$ of $\log 2$ for
  $\alpha = 0.1, 0.3, 0.5$. The improvement factor relative to the
  untrained median ($0.301 \times \log 2$) is roughly $10\times$ at
  $\alpha = 0.1$ and $60\times$ at $\alpha = 0.5$, driven entirely by
  the $\hat\eta_0$ in the denominator (since $\hat\beta$ barely
  changes).

**Implication for the (GC-bounded-bias) sellability.** The honest
characterisation is:

> "(GC-bounded-bias) does not hold for untrained random models — the
> condition is *vacuous-or-violated* at $\alpha = 0$. For trained
> reasoning policies with even modest alignment ($\alpha \ge 0.1$), the
> condition holds and the bias floor stays non-vacuous."

This matches §2.2 of the proposal ("The (GC) condition is an
**empirical regularity of trained reasoning policies**, not an
algebraic fact").

---

## 5. Bottom-line verdict and recommendation

### 5.1 Strict scoring per the user's rubric

* **GREEN** (floor $\ll \log 2$ in median + optimistic regimes,
  *untrained* model): No.
  * Median $c=1$: $\{0.087, 0.050, 0.027\} \times \log 2$ for $|C|=1,3,10$ — borderline green.
  * Median $c=L_{\mathrm{sm}}/2$: $\{0.520, 0.301, 0.164\} \times \log 2$ — yellow to red.
  * Pessimistic $c=L_{\mathrm{sm}}/2$: $\{61, 36, 19\} \times \log 2$ — fully vacuous.

* **YELLOW** (borderline floor $[0.1, 1] \times \log 2$ in median):
  Yes, this is where the *untrained* model lands at standard biased-SGD
  constant for $|C| = 1, 3$.

* **RED** (floor $\gg \log 2$ in median): Only in the
  *pessimistic* untrained regime. The median is yellow.

### 5.2 Actual verdict: YELLOW with a structural caveat

The official verdict is **YELLOW**, but with a caveat that is more
important than the floor analysis itself:

> **The deeper finding is that the untrained random-weight model
> already *violates the precondition* of (GC-bounded-bias).** Half the
> $(j, \text{init}, \text{question})$ triples have $\hat\eta_j < 0$,
> so there is no global $\eta_0 > 0$ for which the condition holds.

This is **not** a flaw of the theorem — it is the theorem behaving as
designed. The condition is asserted *of* trained policies, not as a
universal fact. But the proposal should be explicit:

1. **Restate (GC-bounded-bias) as a condition on trained reasoning
   policies**, not as a universal property of transformers. The
   $\eta_0 > 0$ requirement is a *training-induced* property.

2. **Quote the empirical improvement factor**: alignment fraction
   $\alpha \ge 0.1$ (a modest amount) is sufficient to make the
   condition hold cleanly and yield a non-vacuous floor:
   floor $/\log 2 \approx 0.03$ at $\alpha = 0.1$ under
   $c = L_{\mathrm{sm}}/2$.

3. **Highlight that the rate term, not the floor, is the binding
   constraint** at empirically relevant $T \le 10^5$. The break-even
   $T$ exceeds $10^9$ even in the trained-ish regime. This means:
   * Reporting "you converge at rate $1/\sqrt T$ down to a floor" is
     fine because the floor is genuinely small.
   * But the **constant in front** matters: at $\hat\eta_0 \approx
     5\mathrm e^{-3}$ (alpha=0.1 median) and $L_0 \approx 6$, you need
     $T \gtrsim 3 \times 10^6$ steps for the rate term to drop below
     $\log 2$. This is **outside** the $T \le 10^5$ horizon by 1-2
     decades.
   * For empirically relevant $T \le 10^5$ in the trained-ish median
     regime, the rate term is $\approx (6) / (5\mathrm e^{-3} \cdot
     316) \approx 3.8$, which is $5.5 \times \log 2$ — still vacuous
     for Markov.

4. **Consider strengthening to PL** (Polyakov-Lojasiewicz) for the
   exponential-rate variant of the theorem. The proposal §3.4 already
   discusses this. Under PL with parameter $\mu_{\mathrm{PL}}$, the
   rate becomes $\E[L(x_T)] \le L_0 e^{-\eta_0 \mu_{\mathrm{PL}} T} +
   c\beta^2 / (\eta_0 \mu_{\mathrm{PL}})$, which buys exponential
   decrease in $T$ rather than $\sqrt T$. For $\hat\eta_0 = 5\mathrm e^{-3}$,
   even small $\mu_{\mathrm{PL}}$ (say $0.1$) would make $T = 10^4$
   sufficient. This is **the right move if the user wants to claim
   $T \le 10^5$ regime non-vacuity**.

### 5.3 Recommended path forward

* **Do not abandon the framework**: median floor under $c = 1$ is
  $\approx 0.05 \times \log 2$ for $|C| \ge 3$ in *untrained* models
  and $\approx 0.03$-$0.005$ in trained-ish models. The floor is not
  the problem.

* **Strengthen the framing**: state the assumption explicitly as a
  property of *trained* policies, and quote $\alpha$ as a parameter of
  practical importance.

* **Adopt the PL variant for the main rate**, with the non-PL variant
  as a remark. The non-PL rate is too slow ($\sqrt T$) to be
  non-vacuous at empirically realistic $T \le 10^5$ given the small
  $\hat\eta_0$ values observed; PL fixes this and is plausible for a
  basin of attraction around correct-answer regions.

* **Optional: empirically estimate or upper-bound $L_0$ more
  carefully.** At the proposal's framing $L_0 = -\log \pi(x_0; Q)$,
  with $x_0$ being the post-prompt hidden state. For trained models
  starting from a well-formed prompt, $L_0$ could be much smaller than
  $\log V \approx 6.9$ (which is the random-init worst case). Even a
  modest improvement to $L_0 = 2$ shrinks the break-even threshold
  ten-fold.

### 5.4 Risk taxonomy update for the proposal

The proposal §6 "Risk 2: bias floor washes out the rate" should be
updated:

* **Old assessment**: probability 40%, the floor dominates the rate.
* **New assessment**: probability **10%** that the *floor* dominates
  (it's non-vacuous in median across all settings with $c = 1$, and
  under $c = L_{\mathrm{sm}}/2$ for trained-ish models). But
  probability **70%** that the *rate term* itself is too slow at
  empirically realistic $T \le 10^5$ — meaning the theorem is
  technically non-vacuous but won't predict empirical behaviour
  meaningfully unless the PL variant is invoked.

* **New mitigation**: adopt the PL-rate variant of the headline (which
  is exponential rather than $\sqrt T$). Already proposed as an
  optional variant in §3.4 — make it the default.

---

## 6. Reproducibility

* Script: `/tmp/risk-2-sanity-check.py`
* Seeds: `12345 + |C|` for Task A/B; `54321 + int(100 * alpha)` for
  Task C.
* Runtime: $\approx 19$ s, NumPy only.
* No PyTorch dependency.
* Output: full JSON in `/tmp/risk2-full.json` (re-runnable via
  `python3 /tmp/risk-2-sanity-check.py`).

---

## 7. Numerical summary cheat-sheet

| Question | Answer (single number) |
|----------|------------------------|
| Does (GC-bounded-bias) hold for untrained random transformers? | **No** (50% of cases have $\hat\eta_j < 0$). |
| Does it hold under modest $\alpha \ge 0.1$ alignment? | **Yes** (100% of cases have $\hat\eta_j > 0$). |
| Median floor for untrained model, $c = 1$, $|C| = 3$? | $0.05 \times \log 2$ — green. |
| Median floor for untrained model, $c = L_{\mathrm{sm}}/2$, $|C| = 1$? | $0.52 \times \log 2$ — yellow. |
| Median floor for trained-ish model ($\alpha = 0.1$), $c = L_{\mathrm{sm}}/2$, $|C| = 3$? | $0.029 \times \log 2$ — green. |
| Break-even $T$ in median trained-ish regime? | $\approx 3 \times 10^9$ — floor is not the binding constraint at $T \le 10^5$. |
| Number of steps needed for rate term $L_0/(\eta_0 \sqrt T)$ to drop below $\log 2$ in median trained-ish regime? | $\approx 3 \times 10^6$ — **outside** the $T \le 10^5$ horizon. |
| Verdict | **YELLOW**: floor is non-vacuous, but the $\sqrt T$ rate is too slow at empirical $T$. PL variant recommended. |
