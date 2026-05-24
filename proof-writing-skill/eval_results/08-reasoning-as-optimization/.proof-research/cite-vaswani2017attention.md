# \cite{vaswani2017attention} — Attention Is All You Need

**Paper.** *Attention Is All You Need*, Vaswani, Shazeer, Parmar, Uszkoreit,
Jones, Gomez, Kaiser, Polosukhin. NeurIPS 2017, arxiv:1706.03762.

**Exact name in PDF.** Section 3.2, equation labeled "Attention" (no
explicit equation number in the PDF; presented in §3.2.1
"Scaled Dot-Product Attention" on page 4).

**Statement (verbatim).** The scaled dot-product attention used in the
Transformer architecture is defined as
$$
   \mathrm{Attention}(Q, K, V) \;=\; \mathrm{softmax}\!\left( \frac{Q K^\top}{\sqrt{d_k}} \right) V,
$$
where $Q \in \R^{n_q \times d_k}$, $K \in \R^{n_k \times d_k}$,
$V \in \R^{n_k \times d_v}$ are queries, keys, and values, and $d_k$ is the
key dimension. Multi-head attention runs $h$ scaled dot-product attentions
in parallel on linear projections of $Q, K, V$ and concatenates the outputs.

**Hypotheses.** None (this is a definition of an architectural primitive,
not a theorem).

**Constants / dimension dependence.** The $\sqrt{d_k}$ scale factor in the
exponent is a normalisation choice motivated heuristically in §3.2.1 of the
paper ("pushed into a region where the softmax has extremely small
gradients" without the scaling). For our purposes the scale factor is
absorbed into the inner-product notation; we write
$\langle q, k \rangle$ for $q^\top k / \sqrt{d_k}$ throughout.

**Use in this paper.** Cited once when defining single-head softmax
attention in the preliminaries (\Cref{def:softmax_attention}). The
algebraic identity $x_j = (s_{j-1}/s_j) x_{j-1} + (e^{\langle q,k_j\rangle}/s_j) V_j$
follows immediately by writing the cumulative softmax denominator
$s_j \coloneqq \sum_{i\le j} e^{\langle q, k_i\rangle}$ and noting
$s_j x_j = s_{j-1} x_{j-1} + e^{\langle q,k_j\rangle} V_j$.

**Project .bib key.** \cite{vaswani2017attention}
