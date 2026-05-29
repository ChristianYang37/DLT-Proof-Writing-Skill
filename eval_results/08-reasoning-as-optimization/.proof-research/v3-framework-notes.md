# v3 framework notes — verifier-argmax + Gumbel concentration

**Status.** v3 rewrite (2026-05-26). Replaces the v2 framework after a comprehensive bug audit found 12 mathematical errors, of which 5 were HIGH severity. The single root cause: v2 tracked the radial coordinate $r = \|x\|$ as its main summary statistic, which is the wrong choice (real transformers have $\|x\| \approx \sqrt d$ constant due to LayerNorm). Forcing the analysis through $r$ required ad-hoc constants ($\bar r$, $c_\star$, $\alpha(d)$) to glue together inconsistent pieces.

v3 fixes this by:
- Tracking the **loss** $L_t = -\log\pi(x_t; Q)$ (gives the clean v1-style gradient form $\nabla L = W_U^\top(p - q_C)$).
- Defining the **success criterion** as logit-margin $M_t > 0$ (matches what the verifier actually checks: argmax-decode in $C$).
- Deriving the $1/\sqrt d$ scaling from $W_U$'s incoherence + Gumbel max of $V$ competing logits, with no postulated $\alpha(d)$.

This file is the orientation document for any sub-agent entering v3. Read first.

## What v2 broke (12-bug taxonomy — **DO NOT REINTRODUCE**)

The sub-agent writing this paper MUST avoid recreating these patterns:

| # | Pattern | How to avoid |
|---|---|---|
| 1 | "i.i.d. $W_U$ with var $\Theta(1/d)$ gives $\|\nabla L\| = \Theta(\sqrt d)$" | All moment bounds derived independently in proof body, no hand-waved scalings |
| 2 | Quantity `conf(Q)` referenced in `def:equilibrium_radius` but never defined | Every symbol in a definition must itself be defined elsewhere in project; no implicit "inherited from..." |
| 3 | Constant $c_\star$ declared "to be pinned by proof of T1" but proof "absorbs $c_\star$ into definition" | Constants either explicit numerical values or chosen as "any $c$ satisfying [inequality]" |
| 4 | $\sqrt 2$ error in Freedman bound | Every concentration-bound invocation independently verified for constant |
| 5 | T1 proof uses $a_{t-1} \ge c_\star$ without justifying | Every step's claimed lower bound must reference a specific lemma |
| 6 | Unexplained $c_\star \bar r/\bar r$ factor in centrifugal drift | No magical factor without source-lemma reference |
| 7 | Conditional variance $C_V$ depends on $\lambda_i$ without justification | Variance bounds traced to specific lemma |
| 8 | Union bound over geometric intervals not fully discharged | Every $1-\delta$ has explicit union bound paragraph |
| 9 | T2 polynomial rate assumes $\lambda_i$ is $d$-independent without verifying | Every monotonicity/independence claim numerically tested |
| 10 | T3 monotonicity of $\lambda_c(d)$ assumes $\bar r$ d-independent without verifying | Same as #9 |
| 11 | $r_t = 0$ boundary behavior never addressed | Every proof has explicit domain analysis |
| 12 | `\norm{W_U}` ambiguous (op vs Frobenius) | Every `\norm{}` specifies the norm |

## The v3 framework

### Setup

**State:** $x_t \in \mathbb R^d$ — attention output at the `</think>` position after $t$ reasoning tokens. Dynamics inherited from the softmax-running-average recurrence in `sections/01-preliminaries.tex` and `sections/03-lemma-softmax-running-average.tex` (salvaged unchanged from v1).

**Unembedding:** $W_U \in \mathbb R^{V \times d}$, with rows $W_U^v \in \mathbb R^d$ representing each vocabulary token. We assume bounded incoherence:
$$\mu(W_U) := \max_{v \neq v'} \, |\langle W_U^v, W_U^{v'}\rangle| \;\le\; \mu_0,$$
for some $\mu_0 \in [0, 1)$. (Typical magnitude: $\mu_0 = O(\sqrt{\log V/d})$ for typical $W_U$.)

**Loss:** $L(x; Q) = -\log \pi(x; Q)$, where $\pi(x; Q) = \sum_{v \in C(Q)} \mathrm{softmax}(W_U x)_v$. Standard v1 definition.

**Logit margin (success quantity):**
$$M(x; Q) := \max_{c \in C} (W_U x)_c - \max_{v' \notin C} (W_U x)_{v'}.$$
Decode correct $\Leftrightarrow M > 0$. The verifier checks $\arg\max_v (W_U x)_v \in C$, equivalent to $M > 0$.

### Step dynamics

Per step (Hidden Markov two-mode, same structure as v2's snowball but applied to $L$):
- **Effective** ($E_t = 1$, prob $\lambda(L_{t-1})$): $V_j$ points along $-\nabla L(x_{t-1})/\|\nabla L\|$. Increment $g_t = \tau \cdot V_j$.
- **Noise** ($E_t = 0$): $V_j$ is a random unit vector independent of $\mathcal F_{t-1}$. Increment $g_t = \tau \cdot V_j$.

Result: per-step $\Delta L$ has drift $-\tau \|\nabla L\|$ when effective, mean 0 with std $\tau \|\nabla L\|/\sqrt d$ when noise (high-d concentration).

### The behavioral assumption (single load-bearing)

**(SS) State-dependent effective rate.** There exists $\lambda: \mathbb R_{\ge 0} \to [0,1]$ and a question-dependent threshold $L^*(Q)$ such that:
$$\Pr[E_t = 1 \mid \mathcal F_{t-1}] = \lambda(L_{t-1}; Q), \qquad \lambda(L) \ge \rateinit(Q) \cdot \mathbb 1\{L < L^*(Q)\}.$$

Same as v2's snowball assumption. The only behavioral postulate.

### The three regularity assumptions

1. (W) Bounded incoherence: $\mu(W_U) \le \mu_0$. (Replaces v2's `ass:critical_scaling` — geometric, not dynamical.)
2. (Sm) Smoothness: $L_{\mathrm{sm}} \le \|W_U\|_{\mathrm{op}}^2/2$. (Same as v2, automatic from architecture.)
3. (B) Bounded value norms: $\|V_j\| \le M$ a.s. (Same as v2.)

### Critical analytic objects

#### Lemma A — Gumbel max of incoherent logits

For any $x \in \mathbb R^d$ and $W_U$ with incoherence $\mu_0 \le 1/2$:
$$\max_{v \notin C} (W_U x)_v \;\le\; \|x\| \cdot \sqrt{\frac{2 \log V}{d}} \cdot (1 + o(1)),$$
with probability $\ge 1 - V^{-c}$ (over the randomness in $x$, if $x$ comes from a martingale, or over the random construction of $W_U$ in the natural-language argument).

Use Vershynin Ch.~2 max-of-sub-Gaussians (explicit constants) rather than asymptotic Gumbel.

#### Lemma B — Signal accumulation

Under the (SS) snowball assumption restricted to $L < L^*(Q)$, with effective rate $\ge \rateinit$:
$$\max_{c \in C}(W_U x_t)_c \;\ge\; \rateinit \cdot t \cdot \tau \cdot \cos\theta \;-\; O(\text{noise std}),$$
where $\cos\theta \ge 1/2$ is the alignment of $V_j$ (on effective steps) with the closest $W_U^c$.

#### Theorem T1 (Phase transition)

There exists a critical rate
$$\boxed{\critrate(d, V, |C|, T) \;=\; c_1 \cdot \sqrt{\frac{\log(V/|C|)}{T \cdot d}}}$$
with $c_1$ an explicit absolute constant (no $c_\star$ pinning, no `conf(Q)`), such that:
- $\rateinit > \critrate$: $\Pr[\arg\max W_U x_T \in C] \ge 1 - \delta_+$, with $\delta_+$ decaying exponentially in $d(\rateinit - \critrate)^2$.
- $\rateinit < \critrate$: $\Pr[\arg\max W_U x_T \in C] \le \delta_-$, with $\delta_-$ via Galton-Watson extinction.

**Proof structure:**
1. Track $L_t$ under the (SS) snowball assumption.
2. Lemma B: cumulative correct-logit signal $\max_c z_c$ grows as $\rateinit T \tau$ + noise.
3. Lemma A: max non-correct logit bounded by $\|x_t\| \sqrt{2 \log V/d}$.
4. Combine: $M_t > 0$ when $\rateinit T \tau > \tau \sqrt T \cdot \sqrt{2 \log V/d}$, i.e., $\rateinit > c_1 \sqrt{\log V/(Td)}$.
5. Concentration: Freedman martingale tail (with **CORRECTED $\sqrt 2$ constant** — bug #4) bounds the fluctuations.
6. Union bound over $V$ competing tokens (discharged explicitly — bug #8).

#### Theorem T2 (Convergence rate)

Conditional on $\{M_T > 0\}$:
$$\E[T_\text{decode}] \;=\; O\!\left(\frac{\log V}{d (\rateinit - \critrate)^2}\right).$$

#### Theorem T3 (Problem difficulty)

$$\Difficulty(Q) \;:=\; \inf\{d : \critrate(d, V, T_\max) < \rateinit(Q)\} \;=\; \Theta\!\left(\frac{\log V}{T_\max \cdot \rateinit(Q)^2}\right).$$

Direct corollary of T1.

## Empirical anchor

The v5b experiment (`/tmp/v5b-verifier-argmax-fast.py`) tested exactly the verifier-argmax model with $V = 256$, $d \in [16, 4096]$, $T_\max = 3000$. Result:
- Log-log fit: $\critrate \sim d^{-0.549}$ (theory: $-0.500$)
- Prefactor ratio observed/predicted: $0.5$–$0.7$ stable across $d$
- Slope gap (0.05) within finite-$V$ correction expected from Vershynin Ch.~2 max-of-sub-Gaussians (vs asymptotic Gumbel).

See `v5b-empirical-validation.md` for full data.

## What sub-agents salvage from v2

**Sections kept untouched:**
- `01-preliminaries.tex` (gradient form, smoothness fact, attention recurrence — all correct).
- `03-lemma-softmax-running-average.tex` (salvaged from v1, still applies).
- `05-random-walk-concentration.tex` (high-d orthogonality + Azuma; FIX the $\sqrt 2$ bug in `lem:concentration_radial_walk`).

**Sections rewritten:**
- `02-assumptions.tex` partial: delete `ass:critical_scaling`, `def:equilibrium_radius`, `def:critical_rate`. Add `ass:incoherent_unembedding`. Keep `ass:snowball`, `ass:bounded_smoothness`, `ass:bounded_value_norms`.
- `04-verifier-geometry.tex` (NEW): logit margin def, incoherence-based Gumbel max bound (Lemma A), loss-to-margin bridge.
- `06-snowball-coupling.tex`: Galton-Watson on loss process (replaces v2's radial GW).
- `07-theorem-T1-phase-transition.tex`: T1 proof in $L$-space.
- `08-theorem-T2-convergence-rate.tex`: T2 with corrected scaling.
- `09-theorem-T3-problem-difficulty.tex`: T3 direct corollary.
- `10-discussion-empirical-implications.tex` partial: update quantitative claims.

**Citation digests (all kept; no new citations needed):**
- `cite-vershynin2018.md` — Ch.~2 max-of-sub-Gaussians for Lemma A
- `cite-freedman1975tail.md` — martingale tail bound (now with corrected $\sqrt 2$)
- `cite-benarous2022highdim.md` — high-dim SGD scaling-limit context
- `cite-saad1995online.md`, `cite-tsiolis2025phase.md` — historical precedent
- `cite-karimi2016pl.md` — PL-style convergence for T2
- `cite-bottou2018optimization.md` — biased-SGD context
- All other cites unchanged.

## Macro changes

- DELETE from `macros.tex`: `\rbar` (was equilibrium radius), `\critrate` (will redefine)
- ADD: `\Margin` (logit margin $M$), `\incoh` (incoherence parameter $\mu$), `\Ldecode` (decode threshold loss)
- KEEP: `\loss, \cmass, \qcond, \Cset, \Snowball, \Extinction, \rateinit, \Lstar, \Difficulty`

## "DO NOT" reminders for sub-agent

1. **NO** circular constants. Every constant $c$ is either an explicit numerical value or stated as "any $c$ satisfying [explicit inequality]".
2. **NO** undefined symbols. If you write `conf(Q)`, `c_\star`, or similar, define it RIGHT THERE.
3. **NO** "by standard concentration" hand-waves. Cite the specific lemma + verify the constants in the proof body.
4. **NO** "we choose $\eta$ such that ..." followed by "absorbing this into the definition". Just write the explicit value.
5. **NO** norm without specifying op vs Frobenius — every `\norm{matrix}` must clarify.
6. **NO** silent assumptions about $r_t = 0$ — explicit domain analysis required.
7. **NO** "$d$-independent" claims without numerical verification.
8. Track every union bound discharge as a separate paragraph.

## Snapshot

Pre-rewrite snapshot at `/tmp/eval-08-v2-pre-v3-rewrite-1779734779.tar.gz` (852KB).
