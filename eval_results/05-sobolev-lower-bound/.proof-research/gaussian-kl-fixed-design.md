# KL divergence for Gaussian fixed-design regression

**Source.** Standard; appears as Lemma 1.6 / Section 2.5 of Tsybakov 2009 in this form.

**Statement.** Let $(x_1,\ldots,x_n)$ be a fixed design. For each $f: [0,1]^d \to \R$, let $P_f$ denote the law of $(Y_1,\ldots,Y_n)$ with $Y_i = f(x_i) + \epsilon_i$, $\epsilon_i \overset{\mathrm{i.i.d.}}{\sim} N(0,\sigma^2)$. Then for any two regression functions $f, g$,
\[
\mathrm{KL}(P_f \| P_g) \;=\; \frac{1}{2\sigma^2} \sum_{i=1}^n \bigl(f(x_i) - g(x_i)\bigr)^2
\;=\; \frac{n}{2\sigma^2} \|f - g\|_n^2,
\]
where $\|h\|_n^2 := \frac{1}{n} \sum_{i=1}^n h(x_i)^2$ is the empirical (design) norm.

**Hypotheses.** None beyond Gaussian noise with known variance $\sigma^2$ and independence of $\epsilon_i$.

**Constants and dimension dependence.** Exact equality, no hidden constants.

**Canonical use pattern.** In a fixed-design minimax lower bound, one bounds $\|f_j - f_0\|_n^2$ by a multiple of $\|f_j - f_0\|_{L^2}^2$ (using e.g. the regular grid design $\{x_i\}$ being well-distributed, or via direct computation when bumps are supported on grid cells). Then KL is bounded by a multiple of the $L^2$-norm-squared and is straightforward to control.

For bumps supported in a single grid cell of width $1/m$ on a regular grid with $n/m^d$ design points per cell, one has
\[
\frac{n}{2\sigma^2} \|f_j - f_0\|_n^2 \;=\; \frac{n}{2\sigma^2} \cdot \frac{1}{n} \sum_i (f_j - f_0)^2(x_i)
\;\leq\; \frac{1}{2\sigma^2} \cdot n \cdot \|f_j - f_0\|_{L^\infty}^2,
\]
which often suffices.

**Common misuses.**
- Using the random-design KL (which is an expectation under $X$) when the problem is fixed-design.
- Conflating $\|\cdot\|_n^2$ with $\|\cdot\|_{L^2}^2$ without justification.
- Forgetting the $1/(2\sigma^2)$ factor (writing $1/\sigma^2$ as if for total variation).

**Project citation key.** \cite{tsybakov2009introduction}
