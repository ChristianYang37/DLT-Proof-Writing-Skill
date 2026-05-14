# Gaussian anti-concentration / small-ball for ReLU patterns

**Source.** Standard; appears as Lemma 3.2 of Du–Zhai–Poczos–Singh 2019 (arXiv:1810.02054) and many follow-ups.

**Statement.** For $\wb \sim \mathcal N(0, \I_d)$ and any fixed unit vector $\xb \in \R^d$, and any $R \ge 0$,
\[
\Pr\!\big[ |\wb^\top \xb| \le R \big] \;\le\; \tfrac{2R}{\sqrt{2\pi}} \;\le\; \tfrac{4R}{5}.
\]
Equivalently, $\Pr[|w^\top x| \le R] \le R \sqrt{2/\pi}$ for $w \sim \mathcal N(0,1)$.

**Use in NTK perturbation.** For neuron $r$, define the "flip event"
\[
A_{i,r}(R) \;\coloneqq\; \{ \exists \wb : \|\wb - \wb_r(0)\|_2 \le R, \;\; \mathbf 1[\wb_r(0)^\top \xb_i \ge 0] \ne \mathbf 1[\wb^\top \xb_i \ge 0] \}.
\]
The event $A_{i,r}(R)$ is contained in $\{ |\wb_r(0)^\top \xb_i| \le R \}$ (since flipping sign of $\wb^\top \xb_i$ within a ball of radius $R$ requires the initial inner product be within $R$ of zero). Hence
\[
\Pr[A_{i,r}(R)] \;\le\; \Pr[ |\wb_r(0)^\top \xb_i| \le R ] \;\le\; \tfrac{2R}{\sqrt{2\pi}}.
\]
This is the key "few neurons flip" lemma in the perturbation stability step.

**Hypotheses.**
- $\wb_r(0) \sim \mathcal N(0, \I_d)$.
- $\|\xb_i\| = 1$ (else the bound scales).

**Common misuses.**
- Forgetting to condition $\xb_i$ as unit-norm.
- Treating the union $\bigcup_r A_{i,r}(R)$ as the event of one fixed $r$ — over $m$ neurons, $\sum_r \Pr[A_{i,r}(R)] = m \cdot O(R)$, which is the right scaling.

**Project citation key.** Refer to `\cite{du2019gradient}` as the source for the perturbation-stability argument; the small-ball fact itself is folklore.
