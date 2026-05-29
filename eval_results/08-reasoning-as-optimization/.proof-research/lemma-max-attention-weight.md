# Technique digest — bounded scores → bounded max softmax weight

**Purpose.** Replace the hidden "uniform attention" assumption in T1's
threshold derivation with a derived deterministic bound. The lemma
(`lem:max_attention_weight` in `sections/04-verifier-geometry.tex`)
converts a bound on the score range $|\langle q, k_t\rangle| \le S$
into a bound on the softmax-weight quadratic variation
$S_T = \sum_t w_{T,t}^2 \le e^{2S}/T$, which is the quantity that
appears in the Azuma-Hoeffding variance accumulation in Lemma~A.

## Statement (informal)

For softmax weights $w_{T,t} = e^{s_t}/\sum_{j=1}^T e^{s_j}$ with
scores $|s_t| \le S$ deterministically, the max weight is bounded:
$$\max_{1 \le t \le T} w_{T,t} \;\le\; \frac{1}{1 + (T-1)e^{-2S}}
\;\le\; \frac{e^{2S}}{T}.$$
Consequently $S_T \le \max_t w_{T,t} \le e^{2S}/T$ since
$\sum_t w_{T,t} = 1$.

## Proof sketch

Two-line argument.

1. **Numerator–denominator ratio.** Fix
   $t^\star \in \arg\max_t w_{T,t}$. The numerator is
   $e^{s_{t^\star}} \le e^S$ trivially. For the denominator, factor
   out $e^{s_{t^\star}}$:
   $\sum_j e^{s_j} = e^{s_{t^\star}}(1 + \sum_{j \ne t^\star} e^{s_j - s_{t^\star}}) \ge e^{s_{t^\star}}(1 + (T-1)e^{-2S})$,
   using $s_j - s_{t^\star} \ge -2S$ termwise (both $s_j, s_{t^\star}$
   in $[-S, S]$). Dividing gives the first inequality.
2. **Conversion to $e^{2S}/T$.** $1 + (T-1)e^{-2S} \ge T e^{-2S}$
   since $1 \ge e^{-2S}$ for $S \ge 0$. Taking reciprocals gives the
   second inequality.

The $S_T$ bound is then $\sum w^2 \le (\max w)(\sum w) = \max w$ via
$\sum w = 1$.

## Why it works

The bound is *tight* in the uniform-attention regime
($w_{T,t} = 1/T$ for all $t$, achieving $S_T = 1/T$ exactly) with
prefactor $e^{2S} \to 1$ as $S \to 0$. It degrades gracefully: a
single concentrated weight $w_{T,1} \approx 1$ gives $S_T \to 1$
which the bound captures via $e^{2S}/T \ge 1$ when $S \gtrsim
\log(T)/2$, i.e.\ when the score spread is wide enough to admit
pathological concentration.

## Where it enters the framework

- **Lemma A** (`lem:gumbel_max_incoherent` in
  `sections/04-verifier-geometry.tex`) replaces the loose Azuma
  variance bound $\sum w^2 \le \sum w = 1$ (which would give
  $\sqrt{T \log V/d}$ in the radicand and break the headline horizon
  scaling) with the tight bound $\sum w^2 \le S_T$, kept symbolic
  in the lemma statement.
- **T1 proof Stage S2** in
  `sections/07-theorem-T1-phase-transition.tex` invokes Lemma~C to
  substitute $S_T \le e^{2S}/T$, yielding the headline
  $\sqrt{\log V/(T d)}$ form with an explicit $e^S$ prefactor in $c_1$.

## Regime of validity

The bound $S \le \text{const}$ holds deterministically under
`ass:bounded_value_norms` (extended to bound $\|W_Q\|_{\mathrm{op}},
\|W_K\|_{\mathrm{op}}$) and Cauchy–Schwarz on the residual stream
$\|x\| \le M$ (from the convex-combination representation of
`lem:softmax_running_average`). The crucial regime question is
whether $S$ is $\Theta(1)$ in $d$ (LayerNorm-bounded activations, the
modern transformer convention) or $\Theta(\sqrt d)$ (raw bounded-entry
activations, where the bound becomes vacuous). Discussed in
`rem:bounded_score_regime` of `sections/02-assumptions.tex`.

## Technique provenance

The inequality $\max_j e^{s_j}/\sum_j e^{s_j} \le 1/(1 + (n-1)e^{-2S})$
under $|s_j| \le S$ is a Cauchy–Schwarz-style softmax range bound. It
is widely used in concentration-of-measure analyses of softmax
outputs; we use the form proved in the standalone softmax-attention
sparsity literature (Cauchy–Schwarz on the denominator after pulling
out the max term). No external citation is added to the LaTeX; the
$\sim 8$-line proof is copied inline into Lemma~C's body for
self-containedness.

## Not used here, for context

The same technique extends to probabilistic refinements under
sub-Gaussian score distributions, yielding $\max_t w_{T,t} =
O((\log T)^c / T)$ in the $\sigma$-sub-Gaussian regime with score
parameter $\sigma$. We do not invoke any such probabilistic refinement
in this paper; the deterministic pigeonhole bound suffices to get the
headline scaling once $S = \Theta(1)$ is the regime of interest.
