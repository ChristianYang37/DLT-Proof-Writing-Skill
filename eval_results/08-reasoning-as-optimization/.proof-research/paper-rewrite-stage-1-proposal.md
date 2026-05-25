# Paper rewrite — Phase A reconnaissance proposal

**Status.** Stage 1 (Phase A only). Reconnaissance for the proposed rewrite
of `08-reasoning-as-optimization/` around a per-token gradient-correctness
(GC) condition replacing the C1/C2/C3 trio. **No `.tex` file modified.**
This document is a structured proposal for user review before any LaTeX
is touched.

**Document scope (mirroring the user prompt).**
1. Verification of the gradient form of $L(x;Q) = -\log \pi(x;Q)$ on the
   constrained-softmax loss, including smoothness.
2. Examination of where (GC) can come from in a transformer's $g_j$.
3. Three candidate exact forms of (GC), ranked and recommended.
4. New dependency graph for the rewritten sections (what is new, what is
   salvaged, what is dropped).
5. Fate of the four existing strengthening / discussion sections.
6. Honest risks where the rewrite could fail to make ai-theory progress.

---

## 1. Verification of the gradient form

### 1.1 Setup and notation

Fix $Q \in F$. Let $W_U \in \R^{|\mathcal V| \times d}$ be the (fixed)
unembedding matrix, let $W_U^{(v)} \in \R^d$ denote its $v$-th row (as a
column vector), let $C \coloneqq \Correct(Q) \subseteq \mathcal V$ be the
(non-empty) set of correct answer tokens, and let
$\mathbf{1}_C \in \{0,1\}^{|\mathcal V|}$ be its indicator vector.
Define on $\R^d$:
$$
   z(x) \coloneqq W_U x \in \R^{|\mathcal V|}, \qquad
   p(x) \coloneqq \softmax(z(x)) \in \Delta^{|\mathcal V|},
$$
$$
   \pi(x) \coloneqq \sum_{v \in C} p(x)_v = \mathbf{1}_C^\top p(x), \qquad
   L(x) \coloneqq -\log \pi(x).
$$
The set-conditional posterior over correct tokens is
$$
   q_C(x)_v \coloneqq \frac{p(x)_v \cdot \mathbf 1[v \in C]}{\pi(x)}, \qquad
   q_C(x) = \frac{\mathrm{diag}(\mathbf 1_C) p(x)}{\pi(x)},
$$
so $q_C \in \Delta^{|\mathcal V|}$ is supported on $C$ and is the
*$C$-conditional posterior* under $p(x)$. Both $p$ and $q_C$ are
probability vectors on $\mathcal V$.

### 1.2 Derivation of $\nabla L$

**Step 1 (gradient of softmax).** Standard fact: for each $v$,
$$
   \partial_x p(x)_v \;=\; p(x)_v \big(W_U^{(v)} \;-\; W_U^\top p(x)\big),
$$
because $\log p_v = z_v - \log Z(x)$ with $Z(x) = \sum_w e^{z_w}$, so
$\partial_x \log p_v = W_U^{(v)} - W_U^\top p$ and
$\partial_x p_v = p_v \cdot \partial_x \log p_v$.

**Step 2 (gradient of $\pi$).** By linearity,
$$
   \nabla \pi(x)
   \;=\; \sum_{v \in C} \nabla p(x)_v
   \;=\; \sum_{v \in C} p(x)_v \big(W_U^{(v)} - W_U^\top p(x)\big)
   \;=\; W_U^\top \!\big(\mathrm{diag}(\mathbf 1_C)\, p(x)\big)
       \;-\; \pi(x)\, W_U^\top p(x).
$$

**Step 3 (gradient of $L = -\log \pi$).** Using
$\nabla L = -\nabla \pi / \pi$ and dividing the previous display by $\pi$:
$$
\boxed{\quad
   \nabla L(x;Q)
   \;=\; W_U^\top p(x) \;-\; \frac{W_U^\top\!\big(\mathrm{diag}(\mathbf 1_C) p(x)\big)}{\pi(x)}
   \;=\; W_U^\top \big( p(x) \;-\; q_C(x) \big).
\quad}
$$
This is the **log-marginal gradient form for a constrained-softmax loss**
and matches the user's claim exactly. It generalises the standard
cross-entropy gradient $W_U^\top(p - e_{v^*})$ to a set $C$ of correct
tokens — when $|C| = 1$, $q_C = e_{v^*}$ and the two coincide.

### 1.3 Smoothness of $L$ in $x$

We compute the Hessian and bound its operator norm. Set $z = z(x) = W_U x$
and view $L$ as the composition $L = \ell \circ z$ where
$\ell(z) \coloneqq -\log\!\big(\mathbf 1_C^\top \softmax(z)\big)$. By
chain rule, $\nabla^2 L(x) = W_U^\top \nabla^2 \ell(z) \, W_U$, so
$$
   \|\nabla^2 L(x)\|_{\mathrm{op}}
   \;\le\; \|W_U\|_{\mathrm{op}}^2 \cdot \|\nabla^2 \ell(z)\|_{\mathrm{op}}.
$$

**Hessian of $\ell$.** From $\nabla \ell(z) = p - q_C$ (with $p, q_C$ now
viewed as functions of $z$), differentiating once more yields
$$
   \nabla^2 \ell(z)
   \;=\; \mathrm{diag}(p) - p p^\top
       \;-\; \big(\mathrm{diag}(q_C) - q_C q_C^\top\big),
$$
the difference of two centred-multinomial Hessians. Each summand is PSD
with operator norm $\le \max_i p_i (1 - p_i) \le 1/4$ (and analogously
$\le 1/4$ for $q_C$, supported on $C$). Hence
$\|\nabla^2 \ell(z)\|_{\mathrm{op}} \le 1/2$ uniformly in $z$, and
$$
\boxed{\quad
   L \text{ is } L_{\mathrm{sm}}\text{-smooth on } \R^d \text{ with }
   L_{\mathrm{sm}} \;\le\; \tfrac{1}{2}\, \|W_U\|_{\mathrm{op}}^2.
\quad}
$$
(One can tighten by a factor $2$ using a Bregman-type argument for the
log-sum-exp, but the bound $\tfrac{1}{2}\|W_U\|^2$ is sufficient and
free of constants. The constant $B_U \coloneqq \|W_U\|_{\mathrm{op}}$ is
already in the project — see `cor:entropy_decay`'s remark — so its use
here imports no new model-side observable.)

**Sanity check.** The standard cross-entropy loss $L^{\mathrm{ce}}(x) =
-\log p(x)_{v^*}$ (singleton $C = \{v^*\}$) has Hessian
$W_U^\top (\mathrm{diag}(p) - pp^\top) W_U$, which is PSD and bounded by
$\|W_U\|^2 / 4$. The set-version subtracts a non-negative PSD term
$W_U^\top (\mathrm{diag}(q_C) - q_C q_C^\top) W_U$ from the Hessian, so
$L$ is **not convex** (the Hessian can be negative definite when the
$q_C$ curvature dominates). This is expected: maximising a sum of
softmax components is a non-convex selection problem.

### 1.4 What this means for the rewrite

- The gradient form $W_U^\top(p - q_C)$ is **exact**, derivable in three
  lines, no hand-waving.
- $L$ is smooth (Lipschitz gradient) but **not convex** in general. This
  matters: the descent-lemma route works under smoothness alone, but a
  global-minimiser argument cannot rely on convexity.
- The only model-side constant the rewrite imports beyond what is
  already in the project is $B_U = \|W_U\|_{\mathrm{op}}$.

---

## 2. Examination of $g_j$ and where (GC) can come from

Recall
$$
   g_j \;=\; \frac{e^{\inner{q}{k_j}}}{s_j}\, V_j
$$
where $V_j$ is the value vector at the $j$-th emitted reasoning token,
under the policy. We examine: **under what relationship between $V_j$
and $\nabla L$ does (GC) hold?**

### 2.1 The "perfect alignment" case ($\beta = 0$)

For $\mathbb{E}[g_j \mid \mathcal F_{j-1}] = -\eta_j \nabla L(x_{j-1};Q)$,
we need
$$
   \mathbb{E}\!\left[\frac{e^{\inner{q}{k_j}}}{s_j} V_j \,\bigg|\, \mathcal F_{j-1}\right]
   \;=\; -\eta_j \cdot W_U^\top \big(p(x_{j-1}) - q_C(x_{j-1})\big).
$$
This is a **vector equation in $\R^d$ that ties the policy's
distribution over the next token's $(k_j, V_j)$ pair to the
unembedding-side residual** $p - q_C$.

The right-hand side has a clean reading:
$W_U^\top(q_C - p) = \mathbb{E}_{v \sim q_C}[W_U^{(v)}] - \mathbb{E}_{v \sim p}[W_U^{(v)}]$.
It is the difference between (a) the average unembedding row weighted
by the $C$-conditional posterior $q_C$ and (b) the average unembedding
row weighted by the full softmax posterior $p$. **Pointing toward the
correct-token unembedding direction is what reduces $L$.**

For the left-hand side, partition by the next token $a_j$:
$$
   \mathbb{E}[g_j \mid \mathcal F_{j-1}]
   \;=\; \sum_{a \in \mathcal V} \pi_j(a \mid \mathcal F_{j-1}) \cdot
         \mathbb{E}\!\left[\frac{e^{\inner{q}{k_j}}}{s_j} V_j \,\bigg|\, a_j = a, \mathcal F_{j-1}\right].
$$
Note $s_j = s_{j-1} + e^{\inner{q}{k_j}}$ is **not**
$\mathcal F_{j-1}$-measurable; it depends on $k_j$ (hence on $a_j$).
This makes the "perfect alignment" equation a non-trivial coupling
between the policy $\pi_j(\cdot)$, the key/value embeddings, and the
unembedding-side residual. It is **not** a free identity.

### 2.2 Tied-embedding leverage

In modern transformers $W_E \in \R^{|\mathcal V|\times d_{\mathrm{model}}}$
is the input embedding and $W_U$ the output unembedding; many architectures
(GPT-2, LLaMA-1) set $W_U = W_E^\top$ ("tied embeddings"). Many newer
architectures (LLaMA-3, Qwen-3) do **not** tie. Even when tied, the
value-projection $W_V$ (per attention head) is **independent** of $W_U$
and $W_E$ — value vectors live in a head-internal subspace, post-LayerNorm,
and have no architectural reason to be aligned with $W_U^{(v)}$.

**Implication.** There is no architectural identity that forces
$V_j$ to be aligned with the residual direction $W_U^\top(p - q_C)$. Any
alignment is **learned**, not structural. The (GC) condition is an
**empirical regularity of trained reasoning policies**, not an algebraic
fact.

### 2.3 The training-signal argument

Why might a reasoning-tuned model (DeepSeek-R1, OpenAI o1) have learned
$V_j$ that aligns with $-\nabla L$? Heuristically:

- RL with verifiable rewards (RLVR) gives **gradient signal that
  pushes towards correct answers**. If the value projection at layer
  $i$, head $h$ contributes positively to the next-token logits of
  correct tokens through residual stream additions and downstream
  layers, then RL training reinforces $V_j$ that point in the
  $W_U^\top q_C$ direction.
- Empirical "logit-lens" observations
  (\cite{wei2022cot, deepseek2025r1, qwen2025thinking}-style chain-of-thought
  analysis, also nostalgebraist's logit lens) suggest middle-late layer
  value vectors do correlate with eventual-output token directions.
- But middle layers (i in the deeper half) are the candidates; early
  layers' $V_j$ are tokenisation / syntactic, not semantic, so the
  (GC) condition should be **layer/head-dependent**.

**Bottom line for the assumption.** (GC) cannot be derived from
architecture; it must be **postulated as a condition the proof
diagnoses for**, with $\beta$ measurable in principle from a
"directional anchor probe" applied to a held-out trajectory set. This
is the *honest* sellability story; it parallels how the project
currently sells $p_0, \Delta, \varepsilon_{\mathrm{anc}}$ as
inference-time observables.

### 2.4 Caveat: the $1/s_j$ factor and "decreasing learning rate"

A subtlety the user prompt should be aware of: $g_j$ has a built-in
**decreasing scale** $\mathbb{E}[e^{\inner{q}{k_j}}/s_j \mid \mathcal F_{j-1}] = \mathcal{O}(1/j)$
on average (after many steps, $s_j$ grows linearly in $j$ if anchor
emissions are frequent), so the effective step size $\eta_j$ in (GC)
naturally has a $1/j$-like shape. This **does not** automatically yield
SGD convergence — biased SGD with $\eta_j = 1/j$ and bias $\beta$
gives an $L^2$ floor of $\beta^2 / \eta_0$-style. But it **does**
suggest the natural setting of $\eta_j$ is $j$-dependent, and the rate
analysis will resemble decreasing-step-size SGD rather than constant
step.

---

## 3. Three candidate exact forms of (GC), ranked

I propose **three** formulations of GC, evaluate each against
provability / novelty / empirical interpretability, and **recommend
one**.

### 3.1 (GC-strong): Unbiased per-token gradient

**Statement.** For every $j \ge 1$ and every $Q \in F$, almost surely:
$$
   \mathbb{E}[g_j \mid \mathcal F_{j-1}] \;=\; -\eta_j \nabla L(x_{j-1}; Q),
   \qquad
   \eta_j \ge \eta_0 > 0.
$$
Possibly augment with a conditional variance bound
$\mathbb{E}[\|g_j + \eta_j \nabla L\|^2 \mid \mathcal F_{j-1}] \le \sigma^2$.

**Empirical interpretation.** A practitioner would estimate $\beta = 0$
by checking that the empirical conditional mean of $g_j$ aligns with
the analytical $-\nabla L(x_{j-1})$ direction across a held-out set.
This is the **classic "implicit SGD" sellability test** for
RL-trained reasoning models.

**Provability.** Cleanest. Allows unbiased SGD analysis: descent lemma
+ either PL-type condition (for linear rate) or non-convex SGD (for
sublinear rate to a stationary point). The convergence rate for $L$
becomes $\mathcal O(1/T)$ to a global minimiser if PL holds, or
$\mathcal O(1/\sqrt T)$ to a stationary point otherwise. The rest of
the proof goes through cleanly; PL-vs-non-convex is the main fork.

**Honest bias estimate.** $\beta = 0$ is **unrealistic** for real
reasoning models. RLVR-tuned policies have learned to produce
informative $V_j$, but **not** unbiased gradient estimators of any
explicit loss — there's no training-time signal that says "match
$\nabla L$ on this constrained-softmax loss". $\beta = 0$ is the kind
of assumption that wins a theorem but loses a reviewer.

**Score.** Provability: 5/5. Novelty: 3/5 (the unbiased-SGD analysis
exists; only the loss is new). Strength (= empirical implausibility):
5/5 — the strongest assumption, requires the most leap of faith.
**Verdict: too strong to sell honestly.**

### 3.2 (GC-bounded-bias): Constant-bias per-token gradient

**Statement.** For every $j \ge 1$ and every $Q \in F$, almost surely:
$$
   \mathbb{E}[g_j \mid \mathcal F_{j-1}] \;=\; -\eta_j \nabla L(x_{j-1}; Q) + b_j,
   \qquad
   \eta_j \ge \eta_0 > 0, \qquad \|b_j\| \le \beta.
$$

**Empirical interpretation.** Estimate
$\hat b_j = \mathbb{E}[g_j \mid \mathcal F_{j-1}] + \hat\eta_j \nabla L(x_{j-1})$
on a held-out set; report the sup-norm or 95-percentile. The constant
$\beta$ is the **measurable bias floor of the policy's per-token
gradient estimate**. This is a *clean, single-number diagnostic*
practitioners can produce.

**Provability.** Standard biased-SGD analysis. The descent inequality is
$\mathbb{E}[L(x_j) \mid \mathcal F_{j-1}] \le L(x_{j-1}) - c_1 \eta_j \|\nabla L\|^2 + c_2 \beta \cdot \|\nabla L\| + c_3 \eta_j^2 L_{\mathrm{sm}} \cdot \|g_j\|_{\mathrm{rms}}^2$,
which after Young's inequality + sum-over-$j$ gives
$\min_j \mathbb{E}\|\nabla L(x_j)\|^2 \lesssim L(x_0)/(\eta_0 T) + \beta^2 / \eta_0$.
The floor $\beta^2/\eta_0$ is **inherent** to biased SGD — it is the
mathematical signature of bias. Connecting expected-$\|\nabla L\|^2$ to
expected-$L$ requires either PL ($\mathcal{O}(\beta^2)$ floor on
$\mathbb{E}[L - L_*]$) or further structure.

**Honest bias estimate.** For DeepSeek-R1 / o1, a reasonable guess is
$\beta = \mathcal{O}(B_U)$, i.e. the bias is on the same order as the
gradient norm itself for non-reasoning-tuned baselines, and a factor
$2$-$5$ smaller for reasoning-tuned models. The empirically meaningful
quantity is the *relative* bias $\beta / \mathbb{E}\|\nabla L\|$; if
this is below $0.5$, biased SGD converges to a meaningful
floor — if above $1$, the gradient direction is dominated by bias
(failure mode). Concrete numbers require an experiment.

**Score.** Provability: 4/5. Novelty: 4/5 (the biased-SGD framing
applied to the constrained-softmax reasoning loss is new in the LLM
theory literature). Strength: 3/5 (still requires postulating $\beta$,
but the postulation is testable).
**Verdict: the user's stated framework. A defensible main result if
the floor $\beta^2/\eta_0$ is reported honestly as the binding
constraint.**

### 3.3 (GC-correlated): Expected-descent only

**Statement.** For every $j \ge 1$ and every $Q \in F$, almost surely:
$$
   \mathbb{E}[\langle g_j, \nabla L(x_{j-1}; Q) \rangle \mid \mathcal F_{j-1}]
   \;\le\; -\eta_0 \, \|\nabla L(x_{j-1}; Q)\|^2,
$$
together with a second-moment bound
$\mathbb{E}[\|g_j\|^2 \mid \mathcal F_{j-1}] \le G^2$.

**Empirical interpretation.** Estimate the conditional cosine
similarity $\mathbb{E}[\cos\angle(g_j, -\nabla L) \mid \mathcal F_{j-1}]$
or the inner-product-to-norm ratio; (GC-correlated) holds if this is
**bounded away from zero** uniformly. This is the *minimal*
inference-time-testable signal that "the model is gradient-descending
$L$ on average".

**Provability.** Allows non-convex SGD analysis without unbiasedness
or constant bias: the descent inequality is
$\mathbb{E}[L(x_j)] \le \mathbb{E}[L(x_{j-1})] - \eta_0 \mathbb{E}\|\nabla L(x_{j-1})\|^2 + (L_{\mathrm{sm}}/2) \cdot G^2$,
giving $\min_j \mathbb{E}\|\nabla L(x_j)\|^2 = \mathcal O(L_{\mathrm{sm}} G^2/(\eta_0 T))$
to a stationary point. **No floor in $\beta^2$**, but also **no
information about the value of $L$ at the stationary point** without
further structure (PL or strict descent).

**Honest bias estimate.** Easiest to verify empirically (cosine
positive) but weakest mathematically (does not guarantee descent in
$L$ itself, only in $\|\nabla L\|^2$). For real models, **this is
almost certainly true** for reasoning-tuned policies on verifiable
tasks — it just says "the model's emissions help on average".

**Score.** Provability: 3/5 (rate analysis goes through but the
conclusion is weaker — stationary point, not minimum). Novelty: 4/5.
Strength: 1/5 (weakest condition, most realistic).
**Verdict: cleanest empirically, but the conclusion ("converges to a
stationary point of $L$") is weaker than what the framing promises
("converges to a correct-answer region"). Would need a separate PL or
basin-of-attraction argument to upgrade.**

### 3.4 Ranking and recommendation

Ranking by **(novelty + provability) / strength** — higher is better,
meaning more impact per unit of assumption strength:

| Form | Provability | Novelty | Strength (lower=better) | Score |
|------|-------------|---------|-------------------------|-------|
| GC-strong | 5 | 3 | 5 | (5+3)/5 = 1.6 |
| GC-bounded-bias | 4 | 4 | 3 | (4+4)/3 = 2.67 |
| GC-correlated | 3 | 4 | 1 | (3+4)/1 = 7.0 |

**Pure ratio favors GC-correlated.** But: GC-correlated does not yield
a "decode correctly with probability $1 - \delta$" conclusion — only
stationarity. This breaks the headline that the user wants ("more
thinking → correct answer").

**My recommendation: GC-bounded-bias (GC-2), as the user proposed.**
Reasoning:

1. It is the **only** form that yields a headline result
   $\mathbb{E}[L(x_T)] \le \text{(decreasing in T)} + \text{floor}(\beta)$
   that connects directly to decoding correctness via the logit-margin
   route.
2. The bias floor $\beta^2/\eta_0$ is **honest** — it pre-empts the
   reviewer's "but this is just postulating SGD" objection by
   quantifying the gap between the policy and a true gradient.
3. Empirical sellability is *better* than C2 + C3: $\beta$ is one
   number, not two qualitative conditions, and it is directly
   estimable from $g_j$ samples without designating an anchor set.
4. The PL question (does $L$ satisfy a PL-type condition along the
   trajectory?) can be **avoided** by stating the headline as
   $\mathbb{E}[L(x_T)] \le \text{floor}$ rather than
   $\mathbb{E}[L(x_T) - L^*] \le \text{floor}$. A $L \le \log 2$
   threshold implies $\pi \ge 1/2$ implies decode-correct via the
   logit-margin route — no PL needed.

**Optional belt-and-braces:** present GC-correlated as a *weaker
sufficient condition* under which one obtains stationarity (a remark
or appendix); the main result is under GC-bounded-bias. This mirrors
the project's current pattern of presenting Theorem-main + Lower-bound
+ Variance-reduced strengthening.

---

## 4. New dependency graph

Below: each new lemma, its statement (one-line), and what it replaces
or salvages from the current proof. **Status legend:** NEW = no
counterpart in current proof; SALVAGE = adapt an existing lemma;
DROP = obsolete.

### 4.1 New chain of lemmas

#### lem:gradient_form (NEW)
**Statement.** $\nabla L(x; Q) = W_U^\top (p(x) - q_C(x))$ with $p, q_C$
as in §1.1 above.
**Hypotheses.** Definitions only; no probability.
**Downstream consumers.** lem:smoothness, lem:descent_inequality.
**Proof.** §1.2 above, 5 lines.

#### lem:smoothness (NEW)
**Statement.** $L$ is $L_{\mathrm{sm}}$-smooth with
$L_{\mathrm{sm}} \le \tfrac{1}{2}\|W_U\|_{\mathrm{op}}^2$.
**Hypotheses.** Existence of $W_U$ (already in `cor:entropy_decay`'s
remark).
**Downstream consumers.** lem:descent_inequality, thm:main_convergence.
**Proof.** §1.3 above.

#### ass:gradient_correctness (NEW — replaces ass:anchor_emission_prob + ass:score_margin)
**Statement.** GC-bounded-bias (§3.2).
**Hypotheses.** Policy $\pi$, fixed model weights.
**Remark.** One paragraph on how $\eta_0, \beta$ are empirically
estimated. Cite \cite{deepseek2025r1, openai2024o1} for evidence that
trained reasoning policies do produce informative $g_j$.

#### lem:descent_inequality (NEW — biased-SGD descent)
**Statement.** Under lem:smoothness + ass:gradient_correctness, for
every $j$:
$\mathbb{E}[L(x_j) \mid \mathcal F_{j-1}] \le L(x_{j-1}) - \tfrac{\eta_j}{2}\|\nabla L(x_{j-1})\|^2 + \tfrac{\eta_j \beta^2}{2 \eta_0} + L_{\mathrm{sm}} \eta_j^2 G^2$,
where $G^2$ is the second-moment bound on $g_j$ (implied by bounded
value norms + bounded $e^{\inner{q}{k_j}}/s_j \le 1$).
**Hypotheses.** lem:smoothness, ass:gradient_correctness,
ass:bounded_value_norms (salvaged).
**Downstream consumers.** lem:telescoping, thm:main_convergence.
**Proof.** Standard biased-SGD descent lemma. Reference: classical
non-convex SGD analysis (e.g. Ghadimi-Lan 2013, or Bottou-Curtis-Nocedal
SIAM 2018, §4); **DO NOT cite without adding a citation digest.**

#### lem:telescoping (NEW)
**Statement.** Telescoping lem:descent_inequality over $j = 1, \dots, T$
yields:
$\mathbb{E}[L(x_T)] \le L(x_0) - \tfrac{1}{2}\sum_{j=1}^T \eta_j \mathbb{E}\|\nabla L(x_{j-1})\|^2 + T \cdot \tfrac{\beta^2}{2\eta_0} + L_{\mathrm{sm}} G^2 \sum_j \eta_j^2$.
With $\eta_j = \eta_0/\sqrt{j}$ or $\eta_j = \eta_0/j$ (matching the
$1/j$ shape suggested by §2.4), this gives
$\min_{j \le T} \mathbb{E}\|\nabla L(x_{j-1})\|^2 = \mathcal O(1/\sqrt T) + \mathcal O(\beta^2/\eta_0^2)$.
**Hypotheses.** lem:descent_inequality.
**Downstream consumers.** thm:main_convergence.

#### lem:logit_margin_decoding (NEW — replaces lem:decoding_correctness)
**Statement.** If $L(x; Q) \le \log 2$ then $\pi(x; Q) \ge 1/2$, and if
in addition $\max_{v \notin C} p(x)_v < \min_{v \in C} p(x)_v$ (which
holds when $\pi(x) > 1/2$ and at least one $v \in C$ has
$p(x)_v > 1/(|C|+1)$), then $\dec(x)$ outputs a token in $C$.
**Hypotheses.** Definition of $L, \pi$; argmax-decoding (or temperature-1
sampling with high-probability success).
**Downstream consumers.** thm:main_convergence.
**Remark.** This is the **polyhedral-cone decoding region** the user
flagged: the correct decoding region is
$\{x : (W_U x)_{v^*} \ge (W_U x)_v \, \forall v\}$ for argmax-decoding
with singleton $C$, generalised to "max over $C$ exceeds max outside
$C$" for set $C$. The level set $\{L \le \log 2\}$ is a sufficient
condition for this cone, captured analytically by the loss value.

#### lem:expectation_to_failure_probability (NEW — Markov-style)
**Statement.** $\Pr[\dec(x_T) \notin C(Q)] \le \Pr[L(x_T) > \log 2] \le \mathbb{E}[L(x_T)] / \log 2$
(Markov on the non-negative random variable $L(x_T)$).
**Hypotheses.** lem:logit_margin_decoding.
**Downstream consumers.** thm:main_convergence (failure-probability
form of the headline).

#### thm:main_convergence (NEW — replaces thm:main_convergence_hp)
**Statement.** Under ass:gradient_correctness with parameters
$(\eta_0, \beta)$ and ass:bounded_value_norms, for every $Q \in F$ and
every $T \ge 1$ with step-size schedule $\eta_j = \eta_0/\sqrt j$
(or $\eta_0/j$):
$$
   \mathbb{E}[L(x_T; Q)] \;\le\; \frac{L(x_0; Q)}{c_1 \sqrt T} + \frac{c_2 \beta^2}{\eta_0},
$$
for explicit constants $c_1, c_2$ depending on $L_{\mathrm{sm}}, \eta_0, G$.
Combining with lem:expectation_to_failure_probability:
$\Pr[\dec(x_T) \notin C(Q)] \le \mathcal O(1/\sqrt T) + \mathcal O(\beta^2)$.
**Hypotheses.** lem:smoothness, ass:gradient_correctness,
ass:bounded_value_norms, lem:descent_inequality, lem:telescoping,
lem:expectation_to_failure_probability.

### 4.2 Salvageable lemmas from the current proof

#### lem:softmax_running_average (SALVAGE, unchanged)
The recurrence $x_j = (s_{j-1}/s_j)x_{j-1} + g_j$ is still the
substrate for everything. Keep as-is.

#### ass:bounded_value_norms (SALVAGE, unchanged)
Still needed for $\|g_j\| \le M$ and hence for the $G$ in the
second-moment bound. Identical statement.

#### lem:anchor_decomposition (DROP)
No longer needed. The new proof routes through $L$, not through
geometric decomposition of $x_j - V^*$.

#### lem:anchor_accuracy_bound (DROP)
Obsolete — no anchor set in the new framework.

#### lem:anchor_count_lb (DROP)
Obsolete — the (GC) assumption directly gives the expected-descent
inequality without going through anchor-count concentration.

#### lem:anchor_mass_lb (DROP)
Obsolete.

#### lem:T_polynomial (DROP — replaced by lem:telescoping)

#### lem:decoding_correctness (REPLACE with lem:logit_margin_decoding)
The new version is more general and removes the Euclidean-ball
artefact.

### 4.3 Tree depth and Occam check

New dependency graph has depth 2 (leaves → headline) like the old
one, with 7 surviving / new lemmas (vs. 7 in the old graph). The
substitution is one-for-one in count, but the **gradient-form** and
**descent-inequality** lemmas are *load-bearing in a way the old ones
were not*: they directly justify the "reasoning = (biased) optimization"
framing.

---

## 5. Strengthening-result fate

For each existing supplementary result, my recommendation:

### `sections/11-lower-bound.tex` — KEEP, ADAPT
The current matching lower bound shows the rate is tight via a
hard-instance construction (all non-anchor emissions). Under the new
framework, an analogous lower bound is **natural**: construct a
policy where $b_j = \beta \cdot u$ for some fixed unit $u \perp \nabla L$,
showing the $\beta^2/\eta_0$ floor cannot be improved without
strengthening (GC). One paragraph adaptation. Status: KEEP with
re-statement.

### `cor:entropy_decay` (within sections/10) — KEEP, RESTATE
Under the new framework, this becomes: $H_T = H(\softmax(W_U x_T))$
decays at the rate of $\mathbb{E}[L(x_T)]$ via the Lipschitz composition
already in `softmax-lipschitz.md`. The link to \citet{choi2025entropy}
becomes **cleaner**: their entropy plateau is a direct empirical
signature of $L$ converging to its floor.
Status: KEEP — empirically valuable and now better motivated.

### `sections/12-variance-reduced.tex` — DROP (or RESTATE optionally)
The current variance-reduced theorem relies on unbiasedness of anchor
emissions — a strictly stronger hypothesis than the main one. Under
the new framework, the analogous strengthening would be (GC-strong) =
unbiased $g_j$, yielding either $\mathcal O(1/T)$ to a stationary
point (no PL) or $\mathcal O(1/T)$ to global min (with PL).
**Recommendation: drop in v1 of the rewrite, optionally re-add in a
revision if reviewers ask for the variance-reduced regime.** The
result is "second-paper material" once the main framing is settled.
Status: DROP for now; revisit in revision.

### `sections/13-discussion.tex` — KEEP, RESTATE
The empirical-scope discussion is **more relevant** under the new
framework, not less. The three falsifiable predictions need updating:

- (i) Pass@1 vs. $T$: now becomes a prediction about $L(x_T)$ vs.
  $T$, with floor $\beta^2/\eta_0$. **Stronger prediction**, because
  it pins down the floor value, not just its existence.
- (ii) Entropy plateau: unchanged, via cor:entropy_decay.
- (iii) Per-question heterogeneity: replace with "per-$\beta$
  heterogeneity" — different policies have different $\beta$ at the
  same task.

Future directions: keep momentum-style acceleration, sharpness-aware
reasoning, compounding within/across-sample scaling. Drop the SAM
discussion (now off-message; the framework doesn't naturally give a
basin-flatness story).
Status: KEEP with substantive rewrite of (i) and (iii).

### `sections/99-sgd-aside.tex` — DELETE
The whole point of the rewrite is that "reasoning as SGD" is now
**a theorem, not an aside**. This file is obsolete and would be
embarrassing to keep.
Status: DELETE.

---

## 6. Risks and unknowns

Honest enumeration of where the rewrite could **fail to make
ai-theory progress**.

### Risk 1 — $\beta$ is empirically intractable to measure
The (GC-bounded-bias) condition requires estimating
$\mathbb{E}[g_j \mid \mathcal F_{j-1}]$ — but this conditional
expectation is over the policy's stochastic sampling, requiring
multiple resamples from the same prefix to estimate. For a single
trajectory of length $T = 1000$ this means $T \times K$ forward
passes where $K$ is the resample budget. **For practitioners with
inference budgets**, $K \le 10$, which yields high-variance estimates
of $\mathbb{E}[g_j]$. Whether $\beta$ can be **diagnostically reported**
the way $p_0, \Delta$ currently are is unclear.
**Mitigation:** state $\beta$ as a *postulated* parameter and offer a
worst-case bound $\beta \le 2 \cdot \mathbb{E}\|g_j\|$ from
$\|b_j\| \le \|\mathbb{E}[g_j]\| + \eta_j \|\nabla L\| \le \|g_j\|_{\mathrm{rms}} + \eta_j L_{\mathrm{sm}} \|x - x^*\|$.
This gives an *upper bound* on $\beta$ from observables.

### Risk 2 — The bias floor washes out the rate
For realistic $\beta$ values, the floor $\beta^2/\eta_0$ might
dominate the rate $\mathcal{O}(1/\sqrt T)$ at all empirically-relevant
$T$ ($T \le 10^5$). If so, the theorem says "you converge to a noisy
floor", which is qualitatively the same as the current result
($\gamma(Q)/2 + \varepsilon_{\mathrm{anc}}$ floor) and adds little.
**Mitigation:** numerically check on a stylised model that the
floor is non-vacuous, i.e. $\beta^2/\eta_0 \ll \log 2$ for plausible
$(\beta, \eta_0)$. If this check fails, the user should reconsider
whether (GC-bounded-bias) is the right framing or whether
(GC-correlated) + a basin-of-attraction argument is more honest.
**Estimated probability of this risk firing:** moderate (40%).
This is the single biggest theoretical risk.

### Risk 3 — Connection between $V_j$ and $\nabla L$ is pure postulate
The proof would have the structure "if a trained reasoning policy
satisfies (GC), then it converges". The reviewer's question — "**why
does a trained policy satisfy (GC)?**" — is then unanswered. The current
proof has the same issue (why does the model satisfy C1-C5?), but the
new framework makes the question sharper because the postulate is now
the *gradient* of an explicit loss, not a geometric condition.
**Mitigation:** add a short "training-signal" subsection in the
discussion arguing heuristically that RLVR training produces $V_j$
with bounded $\beta$. Cite logit-lens / interpretability work
(if a suitable citation exists in `.proof-research/`; otherwise add a
`\todo{verify reference}` per the SKILL's honesty protocol).

### Risk 4 — Loss of accumulated proof work
The current 13-section, ~800-step proof has substantial proof
machinery (Chernoff-Freedman, anchor decompositions, Toeplitz). The
new framework discards lemmas 04-08 wholesale (sections 4-8), keeping
only 03 (running average). This is **~60% of the proof body**, a
non-trivial sunk cost.
**Mitigation:** explicitly approve the discard before writing.
Salvage opportunities: lem:anchor_decomposition could be kept as a
*Bregman-divergence* style decomposition lemma if it lands cleanly
in the descent-inequality proof; otherwise drop.
**Estimated probability:** 100%, this is a known cost not a risk.

### Risk 5 — The polyhedral cone is still hand-waved
The user critiqued the Euclidean ball; the fix is the logit-margin
decoding region. But the level set $\{L \le \log 2\}$ is still a
*sufficient* condition for landing in the correct decoding region.
The actual decoding region is the polyhedral cone
$\{x : (W_U x)_{v^*} \ge (W_U x)_v \, \forall v\}$, and
$\{L \le \log 2\}$ is a smooth interior subset.
Whether this is "principled enough" depends on how the result is
sold. **Mitigation:** explicitly state in the proof that
$\{L \le \log 2\}$ is a sufficient condition for argmax-decoding
correctness via the elementary inequality $\pi \ge 1/2 \Rightarrow
\max_{v \in C} p_v \ge 1/(2|C|) > \max_{v \notin C} p_v$ under mild
conditions on $|C|$ and the non-$C$ posterior. The proof remains
honest if this sufficient-condition status is foregrounded.

---

## 7. Summary of recommendations

1. **Adopt (GC-bounded-bias) as the new central assumption** (the
   user's proposed framework). Reject (GC-strong) as too strong;
   reject (GC-correlated) as too weak for the headline.
2. **Confirm the gradient form $\nabla L = W_U^\top(p - q_C)$ and
   smoothness $L_{\mathrm{sm}} \le \|W_U\|^2/2$** — both verified
   above, derivable in 5 lines each.
3. **New dependency graph:** 7 lemmas (gradient_form, smoothness,
   descent_inequality, telescoping, logit_margin_decoding,
   expectation_to_failure_probability, softmax_running_average).
   ~60% of the current proof body is dropped.
4. **Strengthening fate:** KEEP lower-bound and discussion (adapt
   substantively); KEEP entropy-decay corollary (now better
   motivated); DROP variance-reduced theorem (revisit in revision);
   DELETE SGD aside file.
5. **Top risk:** the floor $\beta^2/\eta_0$ may dominate the rate at
   realistic $\beta$, washing out the convergence claim. **Numerical
   sanity check before writing LaTeX** is recommended.

**Estimated effort for Phase B-D rewrite:** 4-6 days of LaTeX work,
plus 1 day for the numerical sanity check on Risk 2.

**Recommendation to the user:** approve GC-bounded-bias and the
dependency graph, then proceed to Phase B; do the numerical sanity
check in parallel with Phase B drafting.
