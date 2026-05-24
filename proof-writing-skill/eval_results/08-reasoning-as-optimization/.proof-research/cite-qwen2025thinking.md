# \cite{qwen2025thinking} — Qwen3 / Qwen-Thinking technical report

**Paper.** *Qwen3 Technical Report*, Qwen Team (Alibaba Group), 2025.
arxiv:2505.09388.

**Exact name in PDF.** No theorem. Cited for empirical setting motivation:
the Qwen3 family includes "thinking" model variants (e.g. Qwen3-235B-A22B
Thinking, Qwen3-32B Thinking) that operate in a two-mode inference
protocol — a "thinking" mode that emits long-form reasoning traces and a
"non-thinking" mode that responds directly. The report (§3 of the v1
arxiv version) describes the thinking-mode inference as wrapping the
reasoning in `<think>` ... `</think>` delimiters, identical in form to
DeepSeek-R1's protocol. The report includes results on AIME 2025,
LiveCodeBench, GPQA-diamond.

**Statement (paraphrased).** Qwen3 thinking variants implement a two-mode
inference protocol with explicit `<think>`/`</think>` delimitation of the
reasoning trace, trained by a combination of large-scale RL on
verifiable rewards and a final mode-merging SFT step. Reasoning traces
emitted in thinking mode contain natural-language intermediate steps,
self-checks, and explicit verification.

**Hypotheses.** N/A — system-level description.

**Constants / dimension dependence.** N/A.

**Use in this paper.** Cited as empirical evidence (alongside
\cite{openai2024o1, deepseek2025r1, wei2022cot}) that the
`<think>...</think>` protocol with vocabulary-defined anchor tokens is
ecologically valid — Qwen3 thinking, DeepSeek-R1, and OpenAI o1 all share
this surface protocol. The convergence theorem does not depend on
Qwen-specific implementation details.

**Project .bib key.** \cite{qwen2025thinking}
