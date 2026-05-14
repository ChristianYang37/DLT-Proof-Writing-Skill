# \cite{du2019gradient} — Du, Zhai, Poczos, Singh 2019 ("Gradient Descent Provably Optimizes Over-parameterized Neural Networks")

**Paper.** Simon S. Du, Xiyu Zhai, Barnabas Poczos, Aarti Singh. *Gradient Descent Provably Optimizes Over-parameterized Neural Networks*. ICLR 2019. arXiv:1810.02054.

**Status.** This is the primary reference for the three-lemma NTK skeleton used in the proof (linear convergence of two-layer ReLU networks via NTK Gram analysis). The paper proves exactly the theorem this proof restates and follows.

**Key result (Theorem 4.1 of arXiv v3).** For a two-layer ReLU network
\[
f(\Wb, \ab, \xb) = \tfrac{1}{\sqrt m} \sum_{r=1}^m a_r \sigma(\wb_r^\top \xb),
\]
with $\wb_r(0) \sim \mathcal N(0, \I)$, $a_r \sim \mathrm{Unif}\{\pm 1\}$, $\|x_i\|_2 = 1$, $|y_i| \le C$, suppose $\lambda_0 := \lambda_{\min}(\Hb^\infty) > 0$ and $m \ge \poly(n, 1/\lambda_0, 1/\delta)$. Then with probability $\ge 1 - \delta$, gradient descent with step size $\eta = O(\lambda_0 / n^2)$ achieves
\[
\|\ub(k) - \yb\|_2^2 \le (1 - \eta \lambda_0 / 2)^k \|\ub(0) - \yb\|_2^2.
\]

**Three-lemma skeleton.**
1. *Initialization Gram concentration* (Lemma 3.1 of arXiv v3): $\|\Hb(0) - \Hb^\infty\|_2 \le \lambda_0/4$ w.p. $\ge 1 - \delta$ if $m \ge \Omega(n^2 \log(n/\delta) / \lambda_0^2)$.
2. *Perturbation stability* (Lemma 3.2 of arXiv v3): if $\|\wb_r - \wb_r(0)\|_2 \le R$ for all $r$ with $R \le c \lambda_0/n^2$, then $\|\Hb(\Wb) - \Hb(0)\|_2 \le \lambda_0/4$ w.h.p.
3. *Linear convergence given Gram bound* (Lemma 3.3 / Theorem 4.1): if $\lambda_{\min}(\Hb(t)) \ge \lambda_0/2$ for all $t \le T$, then loss decays as $(1 - \eta\lambda_0/2)^t$ and $\|\wb_r(t) - \wb_r(0)\|_2 \le 4\sqrt{n}\|\ub(0) - \yb\|_2 / (\sqrt m \lambda_0)$.

**Closure argument.** The fixed-point / contradiction step shows the perturbation bound never breaches, so the linear-convergence regime holds for all $t$. Specifically: if $T'$ is the first time the perturbation breaches $R$, then before $T'$ Lemma 3.3 gives a smaller perturbation than $R$, contradiction.

**Width requirement (as printed).** $m = \Omega\!\left( \frac{n^6}{\lambda_0^4 \delta^3} \right)$ in v3 of the arXiv paper (improved from a worse polynomial in earlier versions). The simpler statement in the body is $m = \poly(n, 1/\lambda_0, 1/\delta)$.

**Project .bib key.** `du2019gradient`. Standard key used across the literature; matches author-year style.

**Note.** I have not re-downloaded the PDF in this session and so cannot verify the exact arXiv-version theorem numbers above against the printed text. I will cite this as `\cite{du2019gradient}` for the headline result and use `\todo{verify: ...}` for any specific theorem-number invocation. The qualitative skeleton (three lemmas + contradiction closure) is robust across versions.
