# \cite{deepseek2025r1} — DeepSeek-R1 technical report

**Paper.** *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
Reinforcement Learning*, DeepSeek-AI, 2025. arxiv:2501.12948.

**Exact name in PDF.** No theorem. Cited for empirical setting motivation:
DeepSeek-R1 is a reasoning model trained by large-scale RL on top of
DeepSeek-V3-Base. The report describes (§2.3) an explicit "thinking"
phase delimited by `<think>` and `</think>` tags during inference, and
reports headline numbers including 79.8% on AIME 2024 (pass@1) and 97.3%
on MATH-500 (pass@1). The report's central observation is that pure RL
on verifiable rewards (no SFT, no human-curated reasoning traces) suffices
to elicit long-form reasoning behaviour.

**Statement (paraphrased).** Section 2.3 of the report formalises the
two-phase generation protocol: the model first emits a sequence of
reasoning tokens between `<think>` and `</think>` delimiters, then emits
an answer. Both phases are sampled from the same autoregressive decoder.
The report reports that the average reasoning trace length grows
significantly during RL training, correlated with the accuracy gain.

**Hypotheses.** N/A — system-level description.

**Constants / dimension dependence.** N/A.

**Use in this paper.** Cited as empirical evidence (alongside
\cite{openai2024o1, qwen2025thinking, wei2022cot}) that real reasoning
models emit intermediate tokens between explicit `<think>`/`</think>`
markers during inference, supporting our modelling of the latent
trajectory as the layer-$i$ / head-$h$ attention output at the
`</think>` position. The convergence theorem does not depend on
DeepSeek-R1-specific details.

**Project .bib key.** \cite{deepseek2025r1}
