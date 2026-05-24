# \cite{wei2022cot} — Chain-of-Thought Prompting Elicits Reasoning

**Paper.** *Chain-of-Thought Prompting Elicits Reasoning in Large Language
Models*, Wei, Wang, Schuurmans, Bosma, Ichter, Xia, Chi, Le, Zhou.
NeurIPS 2022, arxiv:2201.11903.

**Exact name in PDF.** No theorem; this is an empirical paper. Cited for
its empirical demonstration that few-shot chain-of-thought prompts improve
arithmetic, commonsense, and symbolic reasoning accuracy across model
scales. The headline result is Figure 4 (page 7 of the v6 arxiv version):
PaLM-540B with CoT prompting solves 56.9% of GSM8K problems compared to
17.9% with standard few-shot prompting.

**Statement (paraphrased).** The paper introduces *chain-of-thought*
prompting: providing $(\text{question}, \text{reasoning steps}, \text{answer})$
triples as few-shot exemplars rather than $(\text{question}, \text{answer})$
pairs. Across GSM8K, SVAMP, ASDiv, AQuA, MAWPS (arithmetic), CSQA,
StrategyQA (commonsense), date understanding, and last letter
concatenation (symbolic), CoT prompting yields large accuracy gains
that emerge at large model scale ($\ge 60$B parameters in the paper's
experiments).

**Hypotheses.** Empirical: large-scale pretrained autoregressive
transformer, in-context exemplars in CoT format, decoder sampling.

**Constants / dimension dependence.** N/A — empirical.

**Use in this paper.** Cited once in the motivation / preliminaries
(\Cref{rem:anchor_emission_prob_remark}) as empirical evidence that
modern reasoning-tuned LLMs do emit intermediate, answer-relevant tokens
during the "think" phase of inference. The convergence theorem itself
treats anchor emission as a model-policy assumption (A2'), not derived
from Wei et al.; the citation supports only the empirical plausibility
of that assumption.

**Project .bib key.** \cite{wei2022cot}
