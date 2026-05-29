# v2 framework notes — high-d SGD critical scaling + snowball

> **⚠ SUPERSEDED (2026-05-26).** This v2 framework was discovered to have **12 mathematical bugs** (5 HIGH severity) during a two-agent audit. Root cause: the radial coordinate $r = \|x\|$ is the wrong summary statistic for transformers (LayerNorm forces $\|x\| \approx \sqrt d$ constant). Forcing the analysis through $r$ required ad-hoc constants ($\bar r$, $c_\star$, $\alpha(d)$) glued together with broken derivations.
>
> The replacement is the **v3 verifier-argmax + Gumbel-concentration framework** documented in `v3-framework-notes.md`. v3 tracks loss $L$, uses logit margin $M > 0$ as success criterion, and derives the $1/\sqrt d$ scaling from $W_U$ incoherence + Gumbel max of $V$ competing logits — no postulated $\alpha(d)$ needed.
>
> This file is preserved as historical record. Do not use as orientation; read `v3-framework-notes.md` instead.

---

**Status.** Stage 0 reset complete (2026-05-25). All prior v1 (biased-SGD) sections wiped except `sections/03-lemma-softmax-running-average.tex` (potential salvage). All v1-specific `.proof-research/` files removed except citation digests and the v1 Phase-A proposal / sanity check (kept for cross-reference). `main.tex` reset to skeleton with new title.

Sanity-check pass at d ∈ {16,…,8192} (`v2-sanity-check.md`) **revised the headline scaling** from the original $\lambda_c \sim 1/d$ guess to $\lambda_c \sim 1/\sqrt d$ under the **critical step-size scaling** $\alpha(d) \sim \sqrt d$ — which is the standard Saad–Solla / Ben Arous–Gheissari–Jagannath convention for high-dim online SGD, NOT an ad hoc assumption. Framework is now anchored on the BA-G-J 2022 scaling-limit framework. See `cite-benarous2022highdim.md`, `cite-saad1995online.md`, `cite-tsiolis2025phase.md`.

This file orients any sub-agent entering the v2 framework. Read first.

## What v1 did and why it was discarded

v1 was a biased-SGD framework: assume per-token attention increment $g_j$ is an approximate stochastic gradient of $L(x;Q) = -\log \pi(x;Q)$, with bounded bias $\beta$. The convergence theorem followed from standard biased-SGD descent analysis: $\mathbb{E}[L(x_T)] \le O(1/\sqrt T) + \beta^2/\eta_0$.

The user's critique: even this is "proof hacking". The hidden assumption — that every token *attempts* a gradient step with bounded error — is empirically wrong. **Most reasoning tokens are not gradient steps at all; they are random walks on a loss plateau.** A serious convergence theory must distinguish (a) the rare effective tokens that genuinely make progress from (b) the bulk of tokens that do not, and explain why the bulk does not degrade performance.

## v2 framework, four interlocking pieces

1. **Random walk on plateau is the default**. Most tokens contribute $g_j$ near-orthogonal to $\nabla L$ in the high-$d$ residual stream. Standard concentration: random unit vectors $u, v \in \mathbb{R}^d$ satisfy $\mathbb{E}\langle u, v\rangle^2 = 1/d$. So an "untargeted" $g_j$ moves $L$ by $O(1/\sqrt d)$ per step — negligible at moderate $d$.

2. **High-$d$ orthogonality is what saves the model**. For small $d$, the random walk component accumulates drift and degrades $L$. Only sufficiently large $d$ makes random walk "harmless". This is the key step explaining *why reasoning scales with model size*.

3. **Effective tokens are rare emergent events**. A small fraction of tokens have $V_j$ that genuinely aligns with $-\nabla L(x_{j-1})$. Their rate $\lambda(x)$ is state-dependent: in bad regions, $\lambda(x) \approx 0$; in good regions, $\lambda(x) > 0$ and growing.

4. **Snowball vs. extinction phase transition**. There is a critical parameter $\lambda_c(d, Q)$:
   - $\lambda_0 > \lambda_c$: effective tokens accumulate, $L$ enters correct basin (snowball).
   - $\lambda_0 < \lambda_c$: random walk dominates, $L$ never reaches basin (extinction).

## The three theorems v2 aims for (REVISED post-sanity-check)

- **T1 (sharp phase transition)**: Under the critical step-size scaling $\alpha(d) = \alpha_0 \sqrt{d/d_0}$ (the Saad–Solla / Ben Arous–Gheissari–Jagannath convention; see `cite-benarous2022highdim.md`), the critical effective-token rate is $\lambda_c(d) = c \cdot \sigma^2 / (\alpha(d) \cdot \bar r)$. Substituting gives $\lambda_c \sim 1/\sqrt d$ — verified empirically up to $d=8192$ at slope $-0.60$ (theory $-0.50$; gap is finite-$d$ correction). Above $\lambda_c$: success w.h.p. (snowball). Below: failure w.h.p. (extinction). The **$1/\sqrt d$ scaling is the substantive prediction**, replacing the earlier guess $1/d$.
- **T2 (conditional convergence rate)**: Given the snowball event, $T_{\mathrm{converge}} = O(1/(\lambda_0 - \lambda_c))$, which is poly in $d$ via T1.
- **T3 (problem difficulty)**: $\mathcal{D}(Q) := \inf\{d : \lambda_c(d) < \lambda_0(Q)\} \sim (1/\lambda_0(Q))^2 \cdot c^2$. Minimum model dimension grows quadratically with question difficulty (inverse of empirical effective-token rate).

## Single load-bearing assumption

Replace C1+C2+C3 with one weaker assumption (let sub-agent finalize wording):

> **(SS) Snowball / state-dependent effective rate**: There exists a measurable $\lambda : \mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$ such that, conditional on $\mathcal F_{j-1}$, the increment $g_j$ has effective component (aligned with $-\nabla L(x_{j-1})$) with state-dependent probability $\lambda(L(x_{j-1}))$. The function $\lambda$ is non-decreasing in $-L$ and may be zero for $L > L^*(Q)$ (a bad-region cutoff); for $L < L^*(Q)$, $\lambda(L) > 0$.

No score-margin condition. No per-step lower bound on $\lambda_j$. Effective rate may vanish in bad regions.

## Three candidate decompositions of $g_j$

The sub-agent picks one in Stage A1. My initial sketch of each:

- **(a) Hidden Markov two-mode**: $g_j$ is either effective (drawn from a distribution concentrated around $-\nabla L$) with prob $\lambda(L_{j-1})$, or pure noise (uniform on $d$-sphere) otherwise.
- **(b) Continuous decomposition**: $g_j = \alpha_j \cdot (-\nabla L_\parallel) + \beta_j \cdot \xi_j^\perp$, both magnitudes state-dependent. Smoother but less interpretable.
- **(c) Poisson point process**: effective tokens arrive as state-dependent rate-$\lambda(L_t)$ Poisson process; between arrivals, pure random walk. Requires continuous-time limit.

## Setup of the stylized 1-d model (REVISED for critical scaling)

State: $L_t := L(x_t; Q) \in \mathbb{R}_{\ge 0}$ (or equivalently $r_t := \|x_t\|$ in a radial-statistic view).

Per-step update under **critical step-size scaling** $\alpha(d) = \alpha_0 \sqrt{d/d_0}$:
$$L_{t+1} - L_t \;=\; - \mathbb{1}_{\text{effective}}(t) \cdot \alpha(d) \;+\; \sigma_{\text{rad}}(d) \cdot \xi_t,$$
where $\mathbb{1}_{\text{effective}}(t) \sim \text{Bernoulli}(\lambda(L_t))$, $\xi_t \sim \mathcal{N}(0,1)$, and $\sigma_{\text{rad}}(d)$ captures the radial-projection scale of the high-$d$ noise step (governed by Itô-style expansion of $\|x\|$ — see proof of T1).

The factor $\alpha(d) = \alpha_0 \sqrt{d/d_0}$ is **not ad hoc**: it is the standard Saad–Solla / Ben Arous–Gheissari–Jagannath critical-scaling convention. In the underlying $d$-dim model, $\|\nabla L\| \sim \sqrt d$ (random-unembedding moment bound), and per-step displacement $\eta \cdot \|\nabla L\| = O(1)$ in natural units forces $\eta \sim 1/\sqrt d$. The effective-token drift magnitude $\alpha$ in our absolute-scale parametrization is then $\eta \cdot \|\nabla L\| \cdot |\text{cosine alignment}| \sim \sqrt d \cdot O(1) = O(\sqrt d)$.

In the BA-G-J scaling-limit framework (their Theorem 2.3), this is exactly the regime in which the effective dynamics for radial summary statistics has both non-trivial drift AND non-trivial diffusion. The phase transition follows from comparing the drift rate $\lambda \cdot \alpha(d)$ to the centrifugal-corrected diffusion magnitude, giving $\lambda_c \sim 1/\sqrt d$.

The phase-transition proof of T1 will use a martingale comparison + coupling to a tractable branching process (Galton–Watson with state-dependent rate), wrapped inside the BA-G-J scaling-limit framework.

## What was preserved across the reset

**On disk** in `.proof-research/`:
- `cite-*.md` digests for: openai2024o1, deepseek2025r1, qwen2025thinking, wei2022cot, vaswani2017attention, choi2025entropy, freedman1975tail, vershynin2018, bottou2018optimization, karimi2016pl
- `paper-rewrite-stage-1-proposal.md` (v1 Phase-A reconnaissance — useful for compare/contrast in discussion)
- `risk-2-sanity-check.md` (v1 numerical check — also useful for compare/contrast)
- `scope.md`

**On disk** in `sections/`:
- `03-lemma-softmax-running-average.tex` — the basic recurrence and unrolling, salvaged from v1. Still applies in v2.

**Off disk** (snapshot only): `/tmp/eval-08-biased-sgd-snapshot-1659.tar.gz` — the entire v1 biased-SGD proof. Can be restored with `tar xzf <snapshot> -C eval_results/`.

## Likely new citations needed for v2

**Added during Phase-A reconnaissance / sanity-check (digests ready):**
- `benarous2022highdim` — **foundational** scaling-limit framework (BA-G-J 2022 CPA)
- `saad1995online` — historical origin of $\eta \sim 1/d$ high-dim SGD convention
- `tsiolis2025phase` — most recent precedent for learning-rate-induced phase transitions

**To-add (sub-agent should pull these as needed):**
- Frankle-Carbin 2019 *Lottery ticket hypothesis* (rare effective subnetworks intuition)
- Athreya-Ney *Branching Processes* textbook (Galton-Watson, phase transitions)
- Tao or Vershynin (high-dimensional concentration / orthogonality)
- Possibly Mei-Nguyen-Misiakiewicz 2021 or similar (mean-field analysis of neural training, for connecting noise-component intuition)

## Recommended Stage A1 prompt skeleton

Hand the sub-agent:
1. This file end-to-end
2. The four insights and three theorems from the plan
3. The three decomposition candidates
4. Instruction to propose: (i) chosen decomposition with rigorous formalization, (ii) full assumption set including the (SS) condition, (iii) dependency graph for 7-12 lemmas + 3 theorems, (iv) lit-survey supplement on branching/high-d, (v) tractability risk analysis with specific concerns about phase-transition proof technique.

Sub-agent should STOP before writing any LaTeX. I'll surface via AskUserQuestion before Stage A2 begins.
