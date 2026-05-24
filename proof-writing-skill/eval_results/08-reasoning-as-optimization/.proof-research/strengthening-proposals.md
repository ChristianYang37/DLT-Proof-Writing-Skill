# Strengthening proposals (post-Lit-Survey)

*Read-only proposal phase. No `.tex` edits performed. Five lit-survey
categories appraised; six concrete strengthenings proposed; top pick
recommended.*

## Comparison to prior work by category

### Category 1 — Test-time scaling laws

**Strongest prior result**: Chen et al., *Provable Scaling Laws for the
Test-Time Compute of Large Language Models*, arXiv:2411.19477 (NeurIPS
2025). Knockout-tournament / league algorithms yield exponential or
power-law failure-probability decay in test-time compute under mild
assumptions on the verifier.

**Their gap**: The mechanism is *cross-sample aggregation* (run $N$
parallel chains, tournament them). It does not analyse within-chain
dynamics: their bound says nothing about why a single longer trajectory
gets better, only why a vote of many short ones does. They also pre-suppose
a separate verifier; we don't.

**Our current position**: **Orthogonal and complementary.** We give an
exponential-in-$T$ scaling rate for a *single* trajectory's attention
output via averaging, not voting; same headline rate $\exp(-c T)$, but
the constant $c$ in our work is $p_0^2/8$ (a within-chain anchor-frequency
parameter), where their constant is a verifier-margin / committee-size
parameter. The two results live on different axes (compute reallocation
across $N$ samples vs. within one sample), so neither subsumes the other.
*To strictly dominate*, we should (i) sharpen our constant to $p_0/2$
(closing one gap they have an apparent edge on if $p_0 < 1$), and
(ii) translate to an empirical-curve prediction Chen et al. don't make.

### Category 2 — Reasoning as optimization

**Strongest prior result**: Cheng, Mu, Bordelon, et al., *Transformers
Learn to Implement Multi-step Gradient Descent with Chain of Thought*,
arXiv:2502.21212 (ICLR 2025). A one-layer linear transformer with CoT
provably executes multi-step gradient descent on linear-regression ICL
and achieves near-exact weight recovery.

**Their gap**: Linear-attention only; ICL on synthetic regression only;
their dynamics are *training-time* (the constructed weights implementing
GD), not decode-time (post-training inference). The "reasoning = GD"
identification is at the architecture level, not at the trajectory level.

**Our current position**: **Orthogonal.** Our object is the *attention
output at `</think>`* under standard softmax (not linear) attention with
trained-frozen weights, observed at decode time. We don't pretend to
recover synthetic GT weights; we predict an exponential-in-$T$ rate for
the attention output to enter a decoding-margin ball. The two results
prove different things at different layers of abstraction.

### Category 3 — Mechanistic CoT

**Strongest prior result**: Geiping et al., *Scaling up Test-Time Compute
with Latent Reasoning: A Recurrent Depth Approach*, arXiv:2502.05171
(2025), plus Saunshi et al., *Reasoning with Latent Thoughts*,
arXiv:2502.17416 (ICLR 2025). Looped / recurrent-depth transformers show
that iterating a single block converges hidden states to a fixed-point /
orbit, and that a $k$-layer looped $L$ times nearly matches a $kL$-layer
unrolled net.

**Their gap**: They analyse *hidden-state* iteration inside a recurrent
block, with the block re-applied to the same token stream. They do *not*
analyse decode-time attention outputs as functions of an autoregressively
growing prefix, and they give no quantitative rate (only empirical
convergence-of-trajectory).

**Our current position**: **Strictly more quantitative on the
attention-output axis**: we have an exponential rate $\exp(-p_0^2 T/8)$
plus a closed-form limit ($V^*(Q)$). They have rich empirical orbit
geometry but no rate bound. Different mechanism (autoregressive prefix
vs. fixed-block iteration), so neither result subsumes the other formally,
but ours is the quantitative complement to their qualitative observation.

### Category 4 — Empirical "why thinking helps"

**Strongest prior result**: *Let Me Think! A Long Chain-of-Thought Can Be
Worth Exponentially Many Short Ones*, arXiv:2505.21825 (NeurIPS 2025).
On graph-connectivity tasks, sequential CoT scaling is exponentially more
powerful than parallel majority-vote of many short chains. This is a
sequential-vs-parallel separation theorem.

**Their gap**: The result is task-specific (graph reachability /
connectivity); the mechanism is a counting/expressivity argument about
state space, not a dynamics argument about how a single thinking
trajectory converges. They explain *that* sequential thinking is better,
not *how fast* a given sequential trajectory converges.

**Our current position**: **Complementary.** Our exponential-in-$T$ rate
gives an explicit mechanistic story for *why* sequential thinking yields
exponential gains within a single chain (each anchor emission cuts the
within-chain failure rate). This is consistent with their separation
theorem and gives a candidate quantitative explanation, but is not a
strict generalisation of their result.

### Category 5 — Closest neighbors

Three contenders. I'll appraise each.

**(a) Kim et al., Certified Self-Consistency**, arXiv:2510.17472 (2025).
Strongest prior martingale-flavoured result. Builds a Martingale Majority
Certificate over parallel samples; proves answer distribution gets
exponentially tilted toward its mode under TTRL. *Their gap*: parallel
samples, not within-chain; the martingale is over sampled chains, not
over the within-chain attention dynamics. *Our position*: **Orthogonal**
on the parallel/within-chain axis; we explicitly handle within-chain.
*To dominate*: deliver a within-chain analogue of their exponential tilt
with a tighter rate constant.

**(b) Santilli et al., Statistical Physics of Reasoning**,
arXiv:2506.04374 (2025). Continuous-time SDE/drift-diffusion picture with
four regimes. *Their gap*: phenomenological / non-rigorous on the
quantitative rate; no closed-form limit. *Our position*: **Strictly more
quantitative** — we give an explicit limit ($V^*$), an explicit decoding
ball ($\gamma(Q)/2 + \varepsilon_{\mathrm{anc}}$), and an explicit
exponential rate. They give a richer-regime descriptive model.

**(c) Choi et al., Entropy After `</think>`**, arXiv:2509.26522 (2025).
**Strongest direct neighbor.** Empirically: append `</think>` and watch
next-token entropy; it decreases and stabilises in tandem with pass@1
plateau. They use EMA-variance as a stopping rule. *Their gap*: purely
empirical; no theoretical model of *why* the entropy plateaus or *how
fast*. *Our position*: we are a candidate mechanistic explanation for
the plateau but currently we do not produce an entropy prediction —
we only bound $\|x_T - V^*\|$. **This is a strict gap we can close**.

---

## Proposed strengthenings

### Proposal A — Bernstein–Chernoff sharpening of the anchor-count rate

**The strengthening**: Replace the Azuma bound in `lem:anchor_count_lb`
with a Bernstein–Chernoff (multiplicative-Chernoff) bound for sums of
$\mathcal F_{j-1}$-conditional Bernoullis with conditional mean
$p_j \ge p_0$. The standard multiplicative Chernoff gives
$$
\Pr\!\bigl[\, |\mathcal A^{\mathrm{traj}}_T| \le p_0 T/2 \,\bigr]
\;\le\;
\exp(- p_0 T / 8),
$$
and the *one-sided lower-tail Chernoff* (Boucheron–Lugosi–Massart, §2.2,
Thm 2.3, with $\delta = 1/2$) tightens this to $\exp(-p_0 T / 8)$ — a
factor of $1/p_0$ better in the exponent than the current $p_0^2 T / 8$.
With a Bernstein refinement using the conditional variance
$\sigma_j^2 = p_j(1-p_j) \le p_j$, we further get
$\exp(-p_0 T / (2(1 + 1/3))) = \exp(-3 p_0 T / 8)$ in the small-deviation
regime (Freedman 1975 / Boucheron–Lugosi–Massart, Thm 2.11).

The headline theorem becomes
$$
\Pr\!\bigl[\,\text{success}\,\bigr]
\;\ge\; 1 - 2 \exp(-c\, p_0 T)
$$
for an explicit constant $c \in [1/8, 1/2]$, with $c = 1/8$ from a clean
Chernoff and $c = 1/2$ from a sharper Bernstein–Freedman bound under the
additional observation that $p_j \le 1$.

**Why it's non-trivial**: When $p_0$ is small (the empirically realistic
regime $p_0 \in [0.05, 0.2]$), the improvement from rate $p_0^2 T /8$ to
$p_0 T /8$ is a factor of $20$–$1/p_0$ in the test-time horizon needed
to reach a given accuracy. This is the dominant practical lever and is
flagged in our own `rem:anchor_count_lb_remark` as a known slack.
Bernstein further beats Azuma because the conditional variance
$p_j(1 - p_j) \le p_j$ shrinks when $p_0$ is small, whereas Azuma's
bounded-difference $c_j = 1$ does not.

**Which prior work it dominates**: 
- Kim et al. **arXiv:2510.17472** (MMC certificate) achieves
  $\exp(-cT)$ for the parallel-sample tilt with a model-dependent $c$;
  our sharpened constant gives an explicit inference-time-observable
  $c = p_0 / 8$ or $p_0 / 2$, on axis (a) (tighter constants) for the
  within-chain comparison.
- Chen et al. **arXiv:2411.19477** has rate $\exp(-\Omega(T))$ but with
  an implicit verifier-quality constant; ours is an explicit
  $p_0$-parameterised constant we can read off attention patterns. On
  axis (d) (explicit empirical prediction).

**Proof effort**:
- Rewrite `sections/06-lemma-anchor-count.tex` to apply Chernoff or
  Bernstein–Freedman in place of Azuma. The martingale construction
  carries over; only the concentration step changes.
- Add a new digest file
  `.proof-research/bernstein-chernoff-bernoulli.md` (≈ 60 lines)
  summarising the multiplicative-Chernoff bound and the Bernstein–Freedman
  form for $\mathcal F_{j-1}$-conditional Bernoullis. Cite Boucheron–
  Lugosi–Massart Thm 2.3 (Chernoff) or Thm 2.11 (Freedman), already
  standard.
- Update the rate constant in `sections/08-lemma-T-polynomial.tex` and
  `sections/10-main-theorem.tex` (one symbol change per file, plus
  the corollary update).
- Update `rem:anchor_count_lb_remark` to remove the disclaimer "we keep
  the Azuma form for transparency" since we no longer keep it.

**Risk**: 
- Bernstein–Freedman needs the conditional variance to be summed; here
  $\sum_j p_j(1-p_j) \le T$ trivially, but using the sharper $\sum p_j \ge p_0 T$
  needs care: the bound $\sum \mathrm{Var}_j \le \sum p_j \le T$ is one
  thing; getting a *lower* bound on $\sum p_j$ inside the exponent requires
  the right form of Freedman's inequality (the *one-sided* version
  with variance proxy $\sum p_j (1-p_j)$). This is standard but the
  constants need to be tracked carefully.
- $\gamma_{\min}$ in `eq:thm_main_Delta_condition` is unchanged; the
  score-margin floor condition does not need to be revisited.
- Score-margin assumption stays inference-observable.

**Sellability**: **High**. The rate improvement from $p_0^2$ to $p_0$
(or $3 p_0$ with Bernstein) is the single most visible quantitative
strengthening; it changes a curve that's flat-then-cliff into a curve
with $20\times$ steeper slope at empirically realistic $p_0$. Reviewers
will recognise this immediately as the standard Chernoff-vs-Azuma
sharpening — the proof's own remark already concedes it's tighter, so
there is no novelty risk.

---

### Proposal B — Matching lower bound on the rate

**The strengthening**: Construct a hard instance — a question $Q^*$ and
a fixed-weight model satisfying the five assumptions — for which
$$
\Pr\!\bigl[\,\text{success}\,\bigr]
\;\le\; 1 - c \cdot \exp(- p_0 T)
$$
for some constant $c > 0$ independent of $T$. The instance is a coin-flip
construction: a model that emits an anchor token with probability exactly
$p_0$ at each step (saturating `ass:anchor_emission_prob`), where
$V(\text{anchor}) = V^*(Q^*)$ and $V(\text{non-anchor}) = V^*(Q^*) + v_{\perp}$
for some $v_\perp$ with $\|v_\perp\| > \gamma(Q^*)$. Under this
construction, the failure event "no anchor in $T$ steps" has probability
exactly $(1 - p_0)^T \ge \exp(-2 p_0 T)$ for $p_0 \le 1/2$, and on that
event $x_T = V^*(Q^*) + v_\perp$, which falls outside the decoding ball.

**Why it's non-trivial**: A matching lower bound proves the upper-bound
rate is tight up to constants, which is a strict strengthening (axis (c):
stronger conclusion). The literature (Chen et al. 2411.19477; Kim et al.
2510.17472) gives only upper bounds without matching lower bounds for
the within-chain rate. This makes our analysis *minimax-rate-optimal* for
the within-chain regime.

**Which prior work it dominates**:
- Chen et al. **arXiv:2411.19477**: their tournament bound has no
  matching lower bound (axis (c)).
- Kim et al. **arXiv:2510.17472**: same — upper bound only.
- Saunshi et al. **arXiv:2502.17416** and Geiping et al.
  **arXiv:2502.05171**: empirical convergence only, no rate either
  way.

**Proof effort**:
- New section `sections/11-lower-bound.tex` (≈ 50 lines): construct the
  hard instance explicitly, verify all five assumptions hold for it,
  compute $\Pr[\text{failure}] \ge (1-p_0)^T$.
- Update `sec:main_theorem` to add a "matching lower bound" remark with
  one-line reference to the new section.
- No new technique digest needed (this is a direct construction).
- No changes to existing lemmas.

**Risk**:
- We must verify the score-margin assumption can be satisfied while
  keeping $p_0$ at exactly the threshold; for the lower bound to be
  tight, we need a construction where the policy *chooses* to emit
  non-anchors with probability $1 - p_0$ despite the score margin (which
  is fine: the score margin is about the softmax weights, the
  anchor-emission probability is about the model's stochastic decoding —
  these are *separate* mechanisms with no contradictions).
- A subtle point: the lower-bound failure event must produce $x_T$
  outside the decoding ball, which requires the *attention output* (not
  just the failure event) to land far from $V^*$. The construction with
  $V(\text{non-anchor}) = V^* + v_\perp$ does give this, but care is
  needed if the softmax mass on non-anchors is small (per
  `ass:score_margin`). The construction probably wants $p_0$ small *and*
  $\Delta$ moderate so non-anchors still grab nontrivial mass.

**Sellability**: **Medium-high**. Lower bounds are the gold-standard
strengthening from a theory perspective; the worry is that constructing
a tight instance is a bit fiddly and may need 1-2 iterations to get
right. Less polished than Proposal A but more theoretically deep.

---

### Proposal C — Entropy-decay corollary matching Choi et al. empirical curve

**The strengthening**: Prove a quantitative bound on the **next-token
entropy at the `</think>` position**, $H(p_{\text{next}\mid x_T})$, that
decays at the same exponential rate as $\|x_T - V^*(Q)\|$, matching the
empirical curve of Choi et al. (2509.26522).

Specifically: under the assumptions of the main theorem plus a mild
Lipschitz assumption on the unembedding (softmax) map (which can be made
inference-observable: bound the Jacobian of the next-token softmax by
$L_{\text{unemb}}$ on the relevant ball — this is computable from the
model's unembedding matrix norm and the softmax saturation level), the
KL-divergence between the realised next-token distribution and the
limiting distribution $p^*(Q) \coloneqq \text{softmax}(W_{\text{unemb}} V^*(Q))$
satisfies
$$
\E\bigl[\, \mathrm{KL}(p_{\text{next}\mid x_T} \,\Vert\, p^*(Q)) \,\bigr]
\;\le\; L_{\text{unemb}}^2 \cdot
\Bigl(\tfrac{\gamma(Q)}{2} + \varepsilon_{\mathrm{anc}}\Bigr)^2
+ \mathcal O\bigl(\exp(-c\, p_0 T)\bigr),
$$
via Pinsker's inequality + the Corollary 1.2 ($L^2$-Lipschitz of
$\mathrm{softmax}$) bound. Taking expectations of $H(p_{\text{next}\mid x_T})$
on both sides, the entropy converges to $H(p^*(Q))$ at the same
exponential rate, with an irreducible floor governed by the *same*
trained-model constants $(\gamma, \varepsilon_{\mathrm{anc}})$.

**Why it's non-trivial**: This converts our raw $\|x_T - V^*\|$ bound
into the *exact observable quantity* (entropy of the post-`</think>`
distribution) that Choi et al. measure empirically. It is the kind of
direct empirical-prediction-from-theory bridge that no prior paper in
the lit survey makes. It also closes the lit-survey's "this is the
mechanistic explanation for the empirical phenomenon" framing into an
actual quantitative prediction.

**Which prior work it dominates**:
- Choi et al. **arXiv:2509.26522**: they observe the curve empirically;
  we predict it from first principles, on axis (d) (explicit empirical
  prediction connecting to documented data). This is unique in the
  lit-survey — no other paper produces a predicted entropy curve.
- Santilli et al. **arXiv:2506.04374**: their SDE picture predicts
  qualitative regime transitions but not a quantitative entropy curve.

**Proof effort**:
- New section `sections/12-entropy-corollary.tex` (≈ 80 lines).
- New assumption `ass:unembed_lipschitz` (one extra inference-observable
  assumption — the Lipschitz constant of the unembedding map on the ball
  around $V^*(Q)$). This is fine: still inference-observable (compute
  $\|W_{\text{unemb}}\|_{\mathrm{op}}$ once at inference time and bound
  the softmax Jacobian via a standard inequality).
- New digest `.proof-research/softmax-lipschitz.md` (≈ 40 lines) on the
  $L^2$-Lipschitz constant of the softmax (standard, Gao–Pavel
  arXiv:1704.00805, Prop 4).
- Update `main.tex` to include the new section.
- Update intro of `sec:main_theorem` (one paragraph noting the corollary).

**Risk**:
- Adds an *extra* assumption (`ass:unembed_lipschitz`), which complicates
  the "5 inference-observable assumptions" pitch. Mitigation: this 6th
  assumption can be relegated to the corollary only, leaving the main
  theorem at 5.
- Risk that empirical Choi-et-al curve doesn't quantitatively match the
  predicted rate at the constant level (we can't verify this without
  empirical work). Mitigation: state the prediction as "the rate
  $\exp(-c p_0 T)$ matches the qualitative empirical decay; constants
  depend on the trained-model-specific Lipschitz of the unembedding."
  This is honest and still novel.

**Sellability**: **High**. This is the differentiator that maps our
result onto a specific empirical paper's data. Reviewers will see the
direct bridge and recognise it as the kind of "theory predicts
experiment" deliverable that journal-style reviews care about. Pairs
particularly well with Proposal A: the sharper rate makes the predicted
curve match the empirical curve at a more useful $T$ range.

---

### Proposal D — Variance-reduced anchor-accuracy via unbiased estimator

**The strengthening**: Replace the deterministic anchor-accuracy bound
$\|V(a) - V^*(Q)\| \le \varepsilon_{\mathrm{anc}}$ with a *centred*
condition: assume that anchor value vectors are *unbiased estimators* of
$V^*(Q)$ with variance $\sigma_{\mathrm{anc}}^2$, i.e.
$\E_{a \sim \pi(\cdot \mid \mathcal F_{j-1})}[V(a) \1\{a \in \Acal(Q)\}]
= p_j \cdot V^*(Q)$ and
$\mathrm{Var}(\dots) \le p_j \sigma_{\mathrm{anc}}^2$.

Under this stronger but still inference-observable assumption, the
anchor contribution
$\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k}\, V_k$ averages anchor
values and the variance-reduction gives a $T$-decaying error:
$$
\Bigl\|\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k}\, V_k
       - \Bigl(\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k}\Bigr) V^*\Bigr\|
\;\le\; \frac{\sigma_{\mathrm{anc}}}{\sqrt{|\Acal^{\mathrm{traj}}_T|}}
\;\le\; \frac{\sigma_{\mathrm{anc}}}{\sqrt{p_0 T / 2}}
\quad \text{w.h.p.},
$$
which produces a *genuinely $T$-decaying* total error (not just a
constant floor). The corollary becomes
$$
\E\|x_T - V^*(Q)\|
\;\le\; \frac{\gamma(Q)}{2}
       + \frac{\sigma_{\mathrm{anc}}}{\sqrt{p_0 T / 2}}
       + 2 G \exp(-c p_0 T),
$$
i.e.\ the floor is replaced by a $T^{-1/2}$ term and we get *accuracy*
scaling in $T$, not just confidence scaling.

**Why it's non-trivial**: The current Corollary is a *confidence-scaling*
result: with probability $\to 1$, the error is below a fixed floor
$\gamma/2 + \varepsilon_{\mathrm{anc}}$. The strengthened version is a
*both confidence and accuracy* scaling: expected error itself shrinks
to $0$ at $T^{-1/2}$ rate plus exponential confidence tail. This is the
"real" interpretation of test-time scaling — that the *limit* of the
trajectory improves, not just our certainty about it.

**Which prior work it dominates**:
- Chen et al. **arXiv:2411.19477** still scales accuracy with $N$
  (number of parallel samples), but each sample is a separate full chain;
  our $T$-scaling within a chain is a different axis. On axis (c)
  (stronger conclusion).
- Sequential-vs-parallel paper **arXiv:2505.21825**: gives an
  exponential separation but no quantitative within-chain accuracy
  scaling. We close that gap quantitatively on axis (c).

**Proof effort**:
- Replace `ass:anchor_set_accuracy` with a centred version
  `ass:anchor_set_unbiased` (or keep the deterministic version as an
  alternative and add the centred one as a stronger variant).
- Rewrite `sections/05-lemma-anchor-accuracy.tex` to apply a martingale
  variance bound (Doob $L^2$-maximal inequality or Freedman) over
  $\sum_{k \in \Acal^{\mathrm{traj}}} (V_k - V^*)$ weighted by $w_{T,k}$.
- This is *not* a one-symbol-change; this is a real new lemma
  (≈ 100 lines).
- New digest `.proof-research/martingale-variance-vector.md` (≈ 60 lines)
  on Freedman / Pinelis for $\R^d$-valued martingales.
- Update `sections/08-lemma-T-polynomial.tex` (the combination step)
  and `sections/10-main-theorem.tex` (the corollary; main theorem rate
  is unchanged because confidence still relies on the anchor-count
  event).

**Risk**:
- The unbiasedness assumption is stronger than the current
  $\varepsilon_{\mathrm{anc}}$-cluster assumption. Whether it is
  empirically defensible is a separate question (centred clustering is
  plausible but not free); we should pitch this as an *optional
  strengthening* under stronger conditions, not a replacement of the
  main theorem.
- The weighted-martingale variance bound requires the weights $w_{T,k}$
  to be predictable or at minimum bounded; since they are softmax of
  generated-so-far keys, they are random but bounded in $[0, 1]$. A
  careful argument is needed (condition on the keys $\sigma$-algebra,
  then apply variance bound; see `martingale-lln.md`, Caveats section,
  which already flags this).

**Sellability**: **Medium**. The result is theoretically stronger but
needs a stronger assumption. A reviewer might prefer the original
deterministic form to keep the assumption count low. Best presented as
"under the stronger condition X, our floor is replaced by $T^{-1/2}$"
rather than as a replacement of the main result.

---

### Proposal E — Average-margin relaxation of `ass:score_margin`

**The strengthening**: Replace the uniform score-margin assumption
$$
\forall j, \forall a \in \Acal(Q), a' \notin \Acal(Q):
\inner{q}{k(a)} - \inner{q}{k(a')} \ge \Delta
$$
with an *average* score-margin assumption: over the trajectory,
$$
\frac{1}{T} \sum_{j=1}^T \inner{q}{k(a_{j^*})} - \inner{q}{k(a_j)}
\ge \Delta_{\mathrm{avg}}
\quad \text{a.s.}
$$
where $a_{j^*}$ is an arbitrary fixed anchor token. Translating through
the existing anchor-mass argument: with the average-margin assumption,
the softmax mass on non-anchors satisfies a Jensen-type bound, and the
non-anchor leakage is replaced by an empirical average of exponentials,
which can still be controlled via a one-step concentration argument.

**Why it's non-trivial**: The uniform-margin assumption is the strongest
assumption in the proof; empirical attention weights are *not* uniformly
larger on anchors at every step (they fluctuate). Replacing it with an
average-margin condition that admits per-step margin violations brings
the assumption much closer to empirical reality (a weaker, more
defensible assumption is axis (b)).

**Which prior work it dominates**:
- Cheng et al. **arXiv:2502.21212** assumes a *linear* attention regime,
  which is far stronger than even our uniform-margin assumption;
  weakening on axis (b).
- Multi-head 2508.08222: needs a constructive head-specialisation
  hypothesis; we don't.
- Geiping / Saunshi (2502.05171, 2502.17416): they don't make explicit
  margin assumptions but do require architectural recurrence; we replace
  that with a strictly weaker average-margin condition. Axis (b).

**Proof effort**:
- Rewrite `sections/02-assumptions.tex`'s `ass:score_margin` to the
  average form.
- Rewrite `sections/07-lemma-anchor-mass.tex` to apply a Jensen-type
  bound; the proof becomes longer (≈ 30 extra lines).
- Update `sections/08-lemma-T-polynomial.tex` (the combination step
  changes form: the leakage bound becomes $\exp(-\Delta_{\mathrm{avg}})$
  by Jensen, with the same downstream consequences).
- No new technique digest needed (Jensen's inequality is canonical).

**Risk**:
- A Jensen bound goes the *wrong way* if applied naively (the score is
  in the exponent of a softmax denominator, where Jensen gives an upper
  bound on $e^{-\bar x}$, not on $\overline{e^{-x}}$). This means the
  average-margin condition will *not* directly imply the per-step
  anchor-mass bound; instead, it will imply a bound on the
  *time-averaged* anchor mass $(1/T)\sum_j (1 - \sum_{k \in \Acal} w_{j,k})$.
  This may suffice for the convergence theorem (which only uses the
  anchor mass at the final step $T$, in the polynomial-horizon proof),
  but the argument needs to be threaded through carefully.
- An alternative is to weaken `ass:score_margin` to a "with high
  probability over the trajectory" form, which is easier to plumb
  through but loses some of the headline novelty.

**Sellability**: **Medium**. The strengthening is real and addresses
the most-likely reviewer complaint ("uniform-across-trajectory is
unrealistic"), but the Jensen direction issue means the proof is more
fiddly. Worth doing eventually; not the highest-bang-for-buck pick for
a single revision pass.

---

### Proposal F — Quantitative prediction for thought-anchor head specialisation

**The strengthening**: Add a corollary that converts our theorem's
constants into a *quantitative ranking* of attention heads by their
likely contribution to reasoning. Specifically: the proof shows that the
test-time scaling rate of head $(i, h)$ is $\exp(-c \, p_0^{(i,h)} T)$
with $c = 1/8$ (or improved per Proposal A). Heads with the highest
*product* $p_0^{(i,h)} \cdot \Delta^{(i,h)}$ (after sharpening) will
dominate the anchored-attention dynamics. This makes a quantitative
prediction matching Bogdan et al. (2506.19143)'s empirical
identification of "thought-anchor heads": those should be precisely the
heads with high $p_0 \cdot \Delta$ on a calibration set.

**Why it's non-trivial**: This converts a single-head theorem into a
multi-head selection rule. It's testable: rank all heads by $p_0 \cdot
\Delta$ on a held-out trajectory sample, and check whether the top-ranked
heads coincide with Bogdan et al.'s empirically identified thought-anchor
heads.

**Which prior work it dominates**:
- Bogdan et al. **arXiv:2506.19143**: empirical identification only;
  we provide a theory-derived predictor and a falsifiable test
  (axis (d)).
- Attention-anchor 2510.13554 paper: similar — they have an empirical
  "preplan-and-anchor rhythm" metric; we have a theory-derived
  $p_0 \cdot \Delta$ metric that should rank-correlate with theirs.
  Axis (d).

**Proof effort**:
- New corollary in `sections/10-main-theorem.tex` (≈ 30 lines): take
  the per-layer-head extension `rem:per_layer_extension` and observe
  that the head with the best rate dominates; formalise.
- No new lemmas, no new digests.
- Add a paragraph in `99-sgd-aside.tex` (or a new
  `sections/13-head-selection.tex` for cleanliness) framing the
  prediction.

**Risk**:
- Low. This is a corollary-level extraction from existing theorem
  content. The risk is that the prediction is too qualitative to
  count as a "strengthening" — we should phrase it as a quantitative
  ranking rule with explicit constants, not a fuzzy intuition.

**Sellability**: **Medium-high**. Low effort, real empirical hook,
direct engagement with the thought-anchors literature. Pairs with
Proposal C.

---

## Recommendation

**Top pick: Proposal A (Bernstein–Chernoff sharpening) + Proposal C
(entropy-decay corollary) as a combined revision pass.**

Rationale: Proposal A is the lowest-risk single-largest-quantitative-win
strengthening — it is already conceded by our own remark
`rem:anchor_count_lb_remark`, requires changing one lemma and propagating
the constant, and converts the rate from $p_0^2 T / 8$ to $p_0 T / 8$
(or sharper), a factor of $1/p_0 \approx 20\times$ at empirical $p_0$.
This single change strictly dominates Kim et al. (2510.17472) on axis
(a) (rate constant, within-chain) and matches/sharpens the empirical
slope predicted versus Snell (2408.03314) and s1 (2501.19393).

Proposal C is the lowest-risk single-largest-positioning-win
strengthening — it converts our object ($\|x_T - V^*\|$) into the
quantity that Choi et al. (2509.26522) actually measure (post-`</think>`
entropy), turning the lit survey's "we are the mechanistic explanation
for their empirical curve" framing into a literal quantitative
prediction. This is unique in the entire lit-survey: no other paper
predicts a rate-of-entropy-decay curve from first principles.

Together, A and C dominate:
- **Cat 1**: Snell, Chen et al. (rate constant + empirical curve match).
- **Cat 4**: sequential-vs-parallel paper (explicit within-chain rate).
- **Cat 5**: Kim et al. (rate constant), Choi et al. (predict their
  empirical curve), Santilli et al. (quantitative not qualitative).

Proof effort: one rewritten lemma + one new digest + one new section +
one new digest + one new optional assumption. All within a single
revision pass (Phase B–D scoped to two new sections).

If only one can be picked: **Proposal A alone**. It is the highest-yield
per unit effort, requires no new assumption, and turns the
"$p_0^2 T / 8$ should really be $p_0 T / 8$" admission in our own
remarks into the actual theorem statement.
