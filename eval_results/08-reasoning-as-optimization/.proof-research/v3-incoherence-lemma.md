# Technique digest — Incoherence-based max of incorrect logits along a random trajectory

## What it is

A concentration bound for the max of $V-|C|$ inner products
$\langle W_U^v, x_T\rangle$, where $x_T = \sum_{k=1}^T w_{T,k} V_k$ is
the softmax-running-average trajectory of \Cref{def:softmax_attention}
and $W_U \in \mathbb R^{V \times d}$ has bounded row incoherence.
The bound is the foundation for Lemma~A in the v3 framework
(`sections/04-verifier-geometry.tex`) and the main source of the
$\sqrt{\log V/d}$ scaling in the v3 phase-transition formula.

**This bound is probabilistic in the trajectory $x_T$ (random over
the per-step noise in $(V_t)$), not deterministic in $W_U$.** The
randomness comes from the per-step noise in $V_t$ on noise steps
($E_t = 0$); $W_U$ is treated as deterministic with bounded
incoherence and row norms (\Cref{ass:incoherent_unembedding}).

## Setup

Let $W_U \in \mathbb R^{V \times d}$ with row norms $\|W_U^v\| \in [1, R_U]$ (bounded) and incoherence
$$\mu(W_U) := \max_{v \neq v'} \frac{|\langle W_U^v, W_U^{v'}\rangle|}{\|W_U^v\| \|W_U^{v'}\|} \;\le\; \mu_0.$$

Note: incoherence is a deterministic property of $W_U$. We do **not** assume any random-matrix model — $\mu_0$ is whatever the actual incoherence of $W_U$ is.

## Statement (Lemma A, new form post-Stage-4-fix)

Fix a horizon $T \ge 1$ and write $x_T = \sum_{k=1}^T w_{T,k} V_k$.
Let $\E[x_T]$ denote the conditional expectation over per-step noise.
For any $\delta \in (0, 1)$ and any correct-token set $C$ with
$1 \le |C| < V$:

**(i) Martingale-fluctuation bound.** With probability $\ge 1 - \delta$
over the per-step noise in $(V_t)$,
$$\max_{v \notin C} \langle W_U^v, x_T - \E[x_T]\rangle \;\le\; 2 R_U M \sqrt{\frac{T \log(2(V-|C|)/\delta)}{d}}.$$

**(ii) Drift bound (deterministic in $W_U$, via incoherence).** For every realisation,
$$\max_{v \notin C} \langle W_U^v, \E[x_T]\rangle \;\le\; R_U \cdot \|\E[x_T]\|_2 \cdot \mu_0 \;\le\; R_U \cdot M \cdot \mu_0,$$
where the tight norm bound $\|\E[x_T]\|_2 \le M$ follows from the convex-combination representation $\E[x_T] = \sum_k w_{T,k} \E[V_k]$ with $\sum_k w_{T,k} = 1$ and $\|\E[V_k]\|_2 \le M$, giving $\|\E[x_T]\|_2 \le M \sum_k w_{T,k} = M$ — \emph{independent of $T$}.

**Stage-8/Round-4 correction:** an earlier version of this digest stated the looser bound $\|\E[x_T]\|_2 \le MT$ (with an extraneous $T$ factor from a triangle-inequality relaxation on $\sum_k w_{T,k} \le T$). That relaxation drops the convex-combination structure and is unnecessarily loose; the correct bound is $\|\E[x_T]\|_2 \le M$.

Combining (i) + (ii) via triangle inequality,
$$\max_{v \notin C} \langle W_U^v, x_T\rangle \;\le\; R_U M \mu_0 + 2 R_U M \sqrt{\frac{T \log(2(V-|C|)/\delta)}{d}}.$$

## Why it works (4 steps)

**Step 1** (decomposition): Write $x_T = \E[x_T] + (x_T - \E[x_T])$ and split each $\langle W_U^v, x_T\rangle$ into the drift component and the centred fluctuation.

**Step 2** (drift via incoherence): The drift $\E[x_T]$ lies in $\mathrm{span}\{W_U^c : c \in C\}$ (by the working stylisation $V_t \propto -\nabla L = W_U^\top(q_C - p)$ on effective steps; this is now made an explicit hypothesis of Lemma A — see the alignment-condition cross-reference to Lemma B's $\eqref{eq:alignment_condition}$). For any $v \notin C$, the incoherence bound gives $|\langle W_U^v, W_U^c\rangle| \le \mu_0 R_U^2$, so $|\langle W_U^v, \E[x_T]\rangle| \le R_U \cdot \|\E[x_T]\|_2 \cdot \mu_0$ — this is the trivial incoherence-projection bound (no Gram-matrix counting needed). Combined with the tight convex-combination norm bound $\|\E[x_T]\|_2 \le M$, this gives $\max_{v \notin C} \langle W_U^v, \E[x_T]\rangle \le R_U M \mu_0$, independent of $T$.

**Step 3** (per-direction Azuma): For each fixed $v \notin C$, the sequence $M_t^{(v)} = w_{T,t}(\langle W_U^v, V_t\rangle - \E[\cdot | \mathcal F_{t-1}])$ is a martingale-difference sequence with per-step bound $\le 2 R_U M$ (Cauchy-Schwarz) and conditional variance $\le w_{T,t}^2 R_U^2 M^2/d$ (high-d orthogonality, $\sigma^2/d$ from \Cref{lem:orthogonality_high_d}). By \Cref{lem:concentration_radial_walk} (Azuma-Hoeffding), $\Pr[|\langle W_U^v, x_T - \E[x_T]\rangle| > 2 R_U M \sqrt{T \log(2/\delta')/d}] \le \delta'$.

**Step 4** (explicit union bound): For simultaneous control over all $V - |C|$ incorrect directions, set $\delta' = \delta/(V - |C|)$. The union bound over the $V - |C|$ events sums to total failure $\delta$, with the threshold absorbing the $\log(V - |C|)$ factor inside the square root: $\sqrt{T \log(2(V - |C|)/\delta)/d}$.

The full derivation goes in the proof of Lemma A in `sections/04-verifier-geometry.tex`.

## Comparison to alternatives

| Approach | Bound | Pros | Cons |
|---|---|---|---|
| Random $W_U$ (i.i.d. Gaussian rows) | $\|x\| \sqrt{2 \log V/d}(1+o(1))$ | Cleanest math | Requires probabilistic framework on $W_U$; doesn't fit trained models |
| Asymptotic Gumbel max | $\|x\| \sqrt{2 \log V/d}(1+o(1))$ | Standard reference | Asymptotic in $V$; finite-$V$ corrections lossy |
| ~~Deterministic max-of-sub-Gaussians via Gram matrix~~ | ~~$\|x\| R_U \sqrt{2 \log V/d}\kappa(\mu_0)$~~ | ~~no randomness needed~~ | **UNSOUND**: counterexample $a = e_1$ has $\|a\|_\infty = \|a\|_2 = 1$ but the claimed bound says $1 \le \sqrt{2\log N/N} \to 0$. The deterministic version simply does not exist. |
| **Martingale + union bound (this digest, Round-4-corrected)** | $R_U M \mu_0 + 2 R_U M \sqrt{T \log(V/|C|)/d}$ | Explicit constants, sound argument, deterministic in $W_U$, allows trained models, drift independent of $T$ | None significant; the factor-2 slack in T1 (Round-3) can be relaxed to $\sqrt 2$ since drift no longer scales with $T_\max$ (see T1 statement and constant tracking in Round-4 fix) |

The v3 framework uses the fourth approach: it gives explicit constants we can track through the proof, the argument is sound (no spurious deterministic max-of-sub-Gaussians bound), and it's compatible with arbitrary (trained) $W_U$ as long as $\mu_0$ is bounded.

## What we cite

- `cite-vershynin2018.md` — Ch.~2 Exercise 2.5.10 (max of $N$ sub-Gaussians, used for verification of the Step-4 union-bound budget); also \Cref{lem:concentration_radial_walk} (the Azuma-Hoeffding in Section 05 already proves the per-direction tail bound, so the Vershynin reference is supplementary, not load-bearing).
- The Gram-matrix counting argument formerly invoked from Vershynin Ch.~3 is **removed** — the new Lemma~A uses only the trivial $|\langle W_U^v, W_U^c\rangle| \le \mu_0 R_U^2$ bound directly.

No new citations needed (Vershynin already in `refs.bib`).

## What we DO NOT do (avoiding bugs #1, #5, #6, and the Stage-4 found bug)

- **Do NOT** claim "$\|W_U\| = \Theta(\sqrt d)$" from a random-matrix argument as a deus ex machina. Track the operator norm $\|W_U\|_{\mathrm{op}}$ separately when needed, and bound it via $\|W_U\|_{\mathrm{op}} \le R_U \cdot \sqrt V$ (Frobenius bound) or a sharper random-matrix bound if applicable.
- **Do NOT** introduce free constants pinned later. The $c_1$ in $\critrate = c_1 \sqrt{\log V/(Td)}$ is the explicit numerical product of constants from \Cref{lem:concentration_radial_walk} and the Step-4 union bound.
- **Do NOT** absorb $\mu_0$ into other constants — track it explicitly.
- **NEW (Stage-4):** Do NOT claim a "deterministic max-of-sub-Gaussians inequality" of the form $\|a\|_\infty \le \sqrt{2 \log n/n} \|a\|_2$. This bound is FALSE: take $a = e_1 \in \mathbb R^n$, then $\|a\|_\infty = \|a\|_2 = 1$ but the RHS is $\sqrt{2\log n/n} \to 0$. The correct $\sqrt{\log n}$ scaling requires PROBABILISTIC ingredients (either Gaussian/sub-Gaussian marginals via Markov inequality on the MGF, or martingale concentration + union bound as in our Step 3 + Step 4).

## Numerical sanity check value

At $V = 256$, $d = 4096$, $T = 3000$, $R_U = 1$, $M = 0.1$:

$$2 R_U M \sqrt{\frac{T \log(2 \cdot 255/\delta)}{d}} \;=\; 2 \cdot 0.1 \cdot \sqrt{\frac{3000 \cdot \log(510/\delta)}{4096}} \;\approx\; 0.2 \cdot \sqrt{0.73 \cdot \log(510/\delta)}.$$

At $\delta = 1/255 \approx 0.004$, $\log(510 \cdot 255) \approx \log(130000) \approx 11.78$, giving fluctuation bound $\approx 0.2 \cdot \sqrt{0.73 \cdot 11.78} \approx 0.59$.

Signal needed for argmax success: $\langle W_U^c, x_T\rangle - $ max-incorrect $> 0$. With the Round-4-corrected tight drift bound, the incoherence drift term is $R_U M \mu_0$ (independent of $T$, vs. the loose $R_U M T \mu_0$ in earlier versions).

**Round-4 numerical check at v5b parameters** ($V = 256, d = 4096, T_\max = 3000, R_U = 1, M = 0.1$, idealised $\mu_0 \approx \sqrt{\log V/d} = 0.037$ for random unit rows):
- Loose bound (old, incorrect): drift term $= 1 \cdot 0.1 \cdot 3000 \cdot 0.037 \approx 11$, dominates noise $\approx 0.59$. Predicted threshold: $\lambda_0 > 11/(0.1 \cdot 3000) = 0.037$. Off by factor 80 from observed $\lambda_c = 0.00047$.
- Tight bound (corrected, this digest): drift term $= 1 \cdot 0.1 \cdot 0.037 \approx 0.0037$, dominated by noise $\approx 0.59$. Predicted threshold: $\lambda_0 > 0.59/(\rateinit\text{-scale})$ — for the v5b stylised additive trajectory, the effective scale is $M T_{\max} = 300$, giving $\lambda_0 > 0.59/300 \approx 0.002$. Within factor 4 of observed $\lambda_c = 0.00047$.

The corrected tight bound resolves the order-of-magnitude discrepancy from the loose form.
