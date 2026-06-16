# \cite{bubeck2015} — gradient-descent rate for smooth convex functions

**Paper.** *Convex Optimization: Algorithms and Complexity*, Sébastien Bubeck,
Foundations and Trends in Machine Learning, Vol. 8, No. 3–4 (2015), pp. 231–358.
arXiv:1405.4980v2 [math.OC], 16 Nov 2015. DOI 10.1561/2200000050. Page 267
(Section 3.2, "Gradient descent for smooth functions").

**Exact name in PDF.** "Theorem 3.3".

**Statement (verbatim).**
> Theorem 3.3. Let $f$ be convex and $\beta$-smooth on $\mathbb{R}^n$. Then gradient
> descent with $\eta = \tfrac{1}{\beta}$ satisfies
> $$ f(x_t) - f(x^*) \le \frac{2\beta\,\lVert x_1 - x^*\rVert^2}{t-1}. $$

Here gradient descent is the iteration $x_{t+1} = x_t - \eta\,\nabla f(x_t)$
(stated on p. 267 just above the theorem), $x_1$ is the initial point (Bubeck
indexes iterates from $1$), and $x^*$ is a minimizer.

**Hypotheses.**
- $f : \mathbb{R}^n \to \mathbb{R}$ is **convex**.
- $f$ is **$\beta$-smooth**: $\nabla f$ is $\beta$-Lipschitz,
  $\lVert\nabla f(x)-\nabla f(y)\rVert \le \beta\lVert x-y\rVert$ (equivalently, twice-diff.
  with Hessian eigenvalues $\le \beta$). This is Bubeck's definition opening §3.2, p. 266–267.
- **Unconstrained** ($X = \mathbb{R}^n$); the constrained projected-GD version is the
  separate Theorem 3.7 (p. ~272), same $O(1/t)$ rate.
- Fixed step size $\eta = 1/\beta$.
- A minimizer $x^*$ exists (the bound is relative to $f(x^*)$).

**Constants / dimension dependence.** The bound is **dimension-free**: the only constants
are $\beta$ (smoothness) and $\lVert x_1 - x^*\rVert$ (initial distance). Asymptotically
$f(x_t) - f(x^*) = O(1/t)$ with the explicit constant $2\beta\lVert x_1-x^*\rVert^2$.
NOTE on constant convention: Bubeck's exact constant is $2\beta$ with denominator $t-1$ and
initial index $x_1$. The looser textbook form $\beta\lVert x_0-x^*\rVert^2/(2t)$ (e.g.
under a 0-indexed start and a sharper one-step analysis) is the *same* $O(1/t)$ rate but a
different constant; **we cite and reproduce Bubeck's exact constant** $2\beta\lVert x_1-x^*\rVert^2/(t-1)$
to keep the citation honest (R13). The downstream decode-time corollary needs only the
$O(1/t)$ shape, so it is constant-agnostic.

**Monotone descent (companion fact, same source).** Bubeck's proof of Theorem 3.3 (p. 267,
Eq. (3.5)) establishes the one-step decrease
$f\!\left(x - \tfrac1\beta\nabla f(x)\right) - f(x) \le -\tfrac{1}{2\beta}\lVert\nabla f(x)\rVert^2 \le 0$,
i.e. the loss is **non-increasing** along the iterates. This justifies the "stays correct"
(monotone) clause of the decode-time corollary in §4.

**Why this is the right citation for our §4 B2.** Our model is "reasoning = gradient descent
on the single-token cross-entropy $L$". $L(x) = \log\sum_c e^{\langle W_c,x\rangle} - \langle W_{a^\star},x\rangle$
is log-sum-exp minus a linear term, hence **convex** (log-sum-exp is convex; a linear term is
affine). On any bounded region (the LayerNorm sphere is compact) its gradient is Lipschitz, so
$L$ is $\beta$-smooth for some finite $\beta$. Theorem 3.3 then gives $L(x_t) - L^\star = O(1/t)$,
which combined with our Lean-verified bridge ($L(x) < \log 2 \Rightarrow$ decode $a^\star$)
yields polynomial-time decode-correctness. The bridge is machine-verified; this rate is the
classical, cited input.

**Project .bib key.** \cite{bubeck2015} (digest filename body `bubeck2015-gd-smooth-convex-rate`
starts with `bubeck2015-`, so lint R13 matches it).
