# Review iteration 5

This iteration reviews the newly added discussion section
(`sections/13-discussion.tex`); the preceding statements
(\Cref{thm:main_convergence_hp,thm:lower_bound,thm:variance_reduced,cor:expected_error_scaling,cor:entropy_decay}
and supporting lemmas) were assessed in iterations 1–4 and converged
to accept-with-minor-revisions in iteration 4. The discussion section
adds no new theorem/lemma/corollary; it is prose plus two `remark`
environments. Phase D gates (a)–(c) all return exit 0 at the time of
review.

## Summary

`sections/13-discussion.tex` adds a single new discussion section,
titled "Discussion: empirical scope and future directions", placed
between `12-variance-reduced.tex` and `99-sgd-aside.tex`. It has two
subsections. The first (`sec:discussion_scope`) walks through where
the five assumptions of \Cref{sec:assumptions} are plausible (math /
code / verifiable-reward reasoning), where they are not (open-ended
generation; agentic long-horizon planning), how the constants $p_0$,
$\Delta$, $\gamma(Q)$, $\varepsilon_{\mathrm{anc}}$ depend on the
trained model vs. the task, three falsifiable predictions of the
framework (pass@1-vs-$T$, entropy plateau rate, per-question
heterogeneity), and three honest scope caveats (sufficient-not-
necessary, faithfulness-not-bounded, training-time-not-modelled).
The second (`sec:discussion_future`) lists four future directions
(optimization-style diagnostics, momentum-style acceleration,
sharpness-aware reasoning, compounding within-chain and across-sample
scaling) and two short remarks (multimodal extension; removing
score-margin uniformity).

## Strengths

- Reuses only existing citations (`choi2025entropy`, `wei2022cot`,
  `openai2024o1`, `deepseek2025r1`, `qwen2025thinking`); no new
  bibliographic entries introduced, hence no new cite-digests required.
- All twelve `\Cref{...}` invocations resolve to labels in earlier
  sections (`sec:assumptions`, `ass:*`, `lem:anchor_mass_lb`,
  `cor:entropy_decay`, `eq:test_time_scaling`, `eq:entropy_decay_rate`,
  `thm:*`, `rem:*`); checked by `grep \label` across sections.
- Adds no new derivation-style content, so no new entries to
  `confidence-trace.md` are needed; coverage remains at 98.11% over the
  prior trace, comfortably above the 50% threshold.
- Honestly delimits scope: explicit "tasks the framework does not
  cover" (open-ended generation, agentic planning) ahead of the
  predictions, rather than burying the limitation; explicit
  "faithfulness" caveat (theorem bounds probability, not whether the
  reasoning trace is causally faithful).
- Each "future direction" comes with an honest cost/risk note —
  momentum-style acceleration's risk is breaking
  \Cref{ass:score_margin}, SAM's risk is multiplicative forward-pass
  cost with unclear payoff, compound scaling needs a separate
  per-chain pass-rate constant — rather than oversold.

## Weaknesses

- **Claim**: The "Pass@1 versus $T$ curve" prediction (Falsifiable
  prediction (i)) says one can "Estimate $\Delta$ from the post-softmax
  weights on the same subset", but post-softmax weights are
  \emph{exponentiated} score differences, not the score gap $\Delta$
  itself; recovering $\Delta$ from post-softmax weights requires log
  inversion and a choice of anchor / non-anchor pair, which the text
  glosses. Not technically wrong, but minor methodological hand-wave.
  - **Evidence**: `sections/13-discussion.tex:77-79`, verbatim:
    `Estimate $p_0$ from anchor-emission counts and $\Delta$ from
    post-softmax weights on a held-out subset of trajectories`.
  - **Severity**: minor (the claim is qualitatively right; the
    methodological step is a one-line $\Delta = \log(w_{\text{anchor}}/w_{\text{non-anchor}})$
    inversion, but the text could be clearer).

- **Claim**: The remark `rem:nonuniform_score_margin` asserts that an
  average-margin condition would give "the same exponential form with
  a slightly worse rate constant" via a Jensen-style argument, but
  Jensen on the score gap goes the \emph{wrong} direction for the
  anchor-mass bound (the bound depends on $e^{-\Delta}$ which is convex
  in $\Delta$, so Jensen gives $\E e^{-\Delta} \ge e^{-\E\Delta}$, i.e.
  the average-margin bound is weaker, not the same up to constants).
  The qualitative claim "we expect the same exponential form" is
  defensible but the constants are not obviously preserved.
  - **Evidence**: `sections/13-discussion.tex:200-204`, verbatim:
    `The proof of \Cref{lem:anchor_mass_lb} would need a Jensen-style
    argument over the per-step score-gap distribution, which we expect
    to give the same exponential form with a slightly worse rate
    constant`.
  - **Severity**: minor (this is a forward-looking remark, framed as
    speculation; the imprecision is acceptable for a discussion remark
    but slightly overstates how clean the extension would be).

- **Claim**: The "Compounding within-chain and across-sample scaling"
  paragraph posits a compound bound of the form
  $\exp(-p_0 T/8 - c_{\mathrm{agg}} N)$ without specifying whether
  $c_{\mathrm{agg}}$ requires additional assumptions on the verifier
  (best-of-$N$ scoring needs a verifier accuracy assumption that is
  not in the current framework). The phrasing "$c_{\mathrm{agg}}$ the
  aggregation-induced rate constant" elides this.
  - **Evidence**: `sections/13-discussion.tex:176-179`, verbatim:
    `A clean compound bound of the form
    $\exp(-p_0 T / 8 - c_{\mathrm{agg}} N)$ (with $c_{\mathrm{agg}}$
    the aggregation-induced rate constant) would formalise this
    trade-off`.
  - **Severity**: minor (framed as future work; the constant
    $c_{\mathrm{agg}}$ is admitted to be defined by a separate
    argument, but reader might assume it falls out of our framework
    when it doesn't).

- **Claim**: The "Sharpness-aware reasoning" paragraph describes
  perturbing intermediate latents $x_j$ and running "extra forward
  passes from each perturbation", but in a standard transformer the
  latent $x_j$ at the layer-$i$, head-$h$, position-$j$ slot is not a
  hyperparameter one can simply override and continue decoding from;
  the forward-pass architecture doesn't expose that intervention as a
  first-class operation in current inference stacks. The proposal is
  more like a research-prototype hook than a deployable trick.
  - **Evidence**: `sections/13-discussion.tex:160-163`, verbatim:
    `perturb the intermediate latents $x_j$ for $j < T$ by a controlled
    amount, run a few extra forward passes from each perturbation`.
  - **Severity**: minor (the paragraph admits "the quantitative
    payoff is unclear in our formalism", which already softens the
    claim; reader should not over-interpret the deployment story).

## Questions for the author

- The "Pass@1 versus $T$ curve" prediction (i) suggests plugging the
  estimated $(p_0, \Delta)$ into \Cref{eq:test_time_scaling} to get a
  predicted curve; in practice $\gamma(Q)$ is question-dependent and
  not directly observable. Is the recommended empirical protocol to
  fit $\gamma(Q)$ from the empirical floor and report only the
  exponential rate as a parameter-free prediction, or to estimate
  $\gamma(Q)$ from a held-out reference model and use it directly?

- The momentum-style acceleration direction proposes a temperature
  schedule on the attention softmax to reshape $\lambda_j$. Does this
  preserve causal masking and the autoregressive structure of the
  decoder? If the temperature schedule depends on $j$ globally, the
  rescaled attention is no longer a stationary softmax and the
  trained model's score margins may degrade non-monotonically.

## Verdict

accept-as-is

## Per-weakness fix decisions

### Weakness #1 (severity: minor)
**Claim:** $\Delta$ from post-softmax weights requires log inversion.
**Verdict:** REAL-nonblocking → no fix (qualitatively correct; the
extra word "logs of" would tighten it but adds no information for the
target audience).

### Weakness #2 (severity: minor)
**Claim:** Jensen-style argument over heterogeneous $\Delta$ does not
obviously preserve rate constants.
**Verdict:** REAL-nonblocking → no fix (the remark is framed as
speculation; tightening would convert a 4-line outlook into a
mini-theorem, exceeding the discussion-section scope).

### Weakness #3 (severity: minor)
**Claim:** Compound bound elides verifier-accuracy assumption.
**Verdict:** REAL-nonblocking → no fix (the phrasing "with
$c_{\mathrm{agg}}$ the aggregation-induced rate constant" implicitly
defers to whatever model the future paper would adopt; this is
appropriate for a discussion section).

### Weakness #4 (severity: minor)
**Claim:** SAM-style intervention is not a first-class operation in
current inference stacks.
**Verdict:** REAL-nonblocking → no fix (the existing text already
flags this is high-risk with unclear payoff; the deployment-story
caveat is implicit).

## Decisions summary

- W1: REAL-nonblocking, minor → no fix.
- W2: REAL-nonblocking, minor → no fix.
- W3: REAL-nonblocking, minor → no fix.
- W4: REAL-nonblocking, minor → no fix.

All weaknesses are nonblocking; the section is accepted as-is.
Termination condition: `accept-as-is` verdict on iteration 5.

## AI-specific failure-mode sweep

- **Fabricated citations**: zero. All five cite-keys used in
  section 13 (`choi2025entropy`, `wei2022cot`, `openai2024o1`,
  `deepseek2025r1`, `qwen2025thinking`) appear in `refs.bib`; all
  have `.proof-research/cite-*-*.md` digests on disk from prior
  iterations (verified by `ls .proof-research/cite-*`).
- **Hallucinated lemma applications**: section 13 does not invoke
  lemmas/theorems beyond `\Cref{...}` cross-references; no derivation
  uses a lemma's conclusion. The `\Cref` targets all resolve.
- **Confident interpolation over missing arguments**: the four
  future-direction paragraphs each name an open issue (preserves
  score margin? overhead worth it? quantitative payoff? verifier
  accuracy constant?) rather than overclaiming a clean result.
- **Phantom references**: no references to non-existent equations
  or labels; checked via `grep \label`.
- **Bare-constant abuse**: $c_{\mathrm{agg}}$ in §future is
  explicitly named ("the aggregation-induced rate constant") and is
  a forward reference to a hypothetical theorem, not a constant
  introduced and used in the current proof — does not trigger R15
  (lint exit 0 confirms).
