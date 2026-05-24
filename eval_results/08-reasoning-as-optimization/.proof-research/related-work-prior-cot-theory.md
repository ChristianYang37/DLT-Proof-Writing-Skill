# Related work — prior CoT / reasoning theory

**Purpose.** Survey what has already been proven about chain-of-thought
reasoning, in-context learning convergence, and "transformer dynamics as
optimization." Establish what THIS proof would add.

## Key prior works

### Schuurmans–Liu–Schwarzer–Liu–Bahdanau–Wang (NeurIPS 2024) — *Autoregressive LLMs are Computationally Universal*
- **Claim:** an autoregressive LLM with an external prompt loop can simulate
  any Turing machine.
- **Mechanism:** prompting strategy + tape encoding in the generated text.
- **Relation to our project:** orthogonal. Their result is about
  *expressivity* (what can be computed in principle), not about *convergence
  dynamics* (whether the latent representation stabilises during reasoning).

### Feng–Zhang–Zhang–Ye–Wang–He (NeurIPS 2024) — *Towards Revealing the Mystery behind Chain-of-Thought*
- **Claim:** with $T$ chain-of-thought tokens, a fixed-depth transformer can
  solve problems requiring depth $\Theta(T)$ in the underlying circuit.
- **Mechanism:** simulating sequential computation via the token stream.
- **Relation to our project:** complementary. Establishes a depth-extension
  argument; says nothing about whether the *attention output* at any layer
  converges to a meaningful point.

### von Oswald–Niklasson–Randazzo–Sacramento–Mordvintsev–Zhmoginov–Vladymyrov (ICML 2023) — *Transformers learn in-context by gradient descent*
- **Claim:** a linear self-attention layer can implement exactly one step of
  GD on a constructed in-context regression loss.
- **Mechanism:** explicit weight construction; the gradient is over the
  constructed loss, not a "reasoning objective."
- **Relation to our project:** their gradient is over a known in-context loss
  with given features; ours would need to be over a reasoning objective whose
  loss is unspecified. Methodology is reusable; the result does not transfer.

### Akyürek–Schuurmans–Andreas–Ma–Zhou (ICLR 2023) — *What learning algorithm is in-context learning?*
- **Claim:** for linear-regression in-context tasks, the transformer's
  forward pass approximates least-squares regression on the in-context data.
- **Mechanism:** empirical + theoretical analysis of attention as
  preconditioned GD.
- **Relation to our project:** same family as von Oswald; identifies an
  implicit algorithm for a specific synthetic task.

### Wei–Tay–Bommasani–Raffel–Zoph–Borgeaud–Yogatama–Bosma–Zhou–Metzler–Chi–Hashimoto–Vinyals–Liang–Dean–Fedus (NeurIPS 2022) — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*
- **Empirical, not theoretical.** Demonstrates CoT improves reasoning;
  no convergence claim.

### OpenAI (2024) — o1 system card; DeepSeek-AI (2025) — DeepSeek-R1 technical report; Qwen team (2025) — Qwen-3-Thinking
- **Empirical.** Demonstrate "thinking models" with explicit reasoning
  anchors; provide architectural details and training recipes. Cite for
  setting motivation only.

### Tian et al. (2023, *Joma*); Ahn et al. (NeurIPS 2023, *Transformers learn higher-order optimization*)
- Analyse transformer training dynamics or in-context optimization. None
  prove convergence of an *inference-time* trajectory to a "correct answer"
  embedding.

## Gap this proof fills

To the best of my reconnaissance, **no published result** proves that the
inference-time latent attention output at a fixed layer/head converges in
$T = \poly$ steps to a point whose decoding is correct, for a general
reasoning task, under inference-time-observable assumptions.

The contribution must therefore be framed as:
1. A *clean reframing*: the attention output is exactly a softmax-weighted
   running average of value vectors along the trajectory.
2. A *convergence theorem*: under explicit assumptions on the trained value
   projection and the reasoning policy, the weighted average converges to
   a target $V^*$.
3. A *decoding bridge*: assuming $\mathrm{decode}: \R^d \to \mathrm{vocab}^*$
   has a margin around $V^*$, the decoded answer is correct.

## Risks the proof must acknowledge

- **The "SGD with weight decay" framing in the problem statement is
  rhetorical, not load-bearing.** Be explicit in the paper that the
  identification is algebraic, but the proof rests on Toeplitz, not on a
  postulated potential.
- **The Anchored-Attention assumption is empirical.** A reviewer will ask
  for evidence; the proof should cite Wei et al. (2022) and the o1/R1/Qwen
  reports as empirical motivation, and explicitly say the assumption is not
  derived from a more primitive condition.
- **The result is qualitative.** With \poly-slack and a generic anchor-set
  hypothesis, the constants are huge and the rate is loose. Be honest about
  this; do not oversell.

## Project citation keys to register

`\cite{vaswani2017attention}`, `\cite{wei2022chain}`, `\cite{openai2024o1}`,
`\cite{deepseek2025r1}`, `\cite{qwen2025thinking}`, `\cite{vonoswald2023}`,
`\cite{akyurek2023learning}`, `\cite{feng2024cot}`,
`\cite{schuurmans2024universal}`, `\cite{karimi2016pl}` (only if PL used),
`\cite{robbins1971convergence}` (only if Robbins–Siegmund used),
`\cite{hardy1949divergent}` (folklore for Toeplitz; optional).
