# ReLU indicator-pattern perturbation (DZPS Gram-stability core)

**Source.** Du–Zhai–Poczos–Singh (ICLR 2019, arXiv:1810.02054), proof of their Lemma 3.2;
the anti-concentration ingredient is small-ball for Gaussian projections.

**Goal.** Bound $\E[\|H(W)-H(0)\|]$ when each neuron moves $\|w_r-w_r(0)\|\le R$, then
convert to a high-probability operator-norm bound via Markov.

**Key facts.**
1. **Entrywise identity.** With $\sigma$ = ReLU, $\sigma'(z)=\mathbf 1\{z\ge0\}$,
   $H_{ij}(W) = \frac1m\sum_r x_i^\top x_j\,\mathbf 1\{w_r^\top x_i\ge0\}\mathbf 1\{w_r^\top x_j\ge0\}$.
   So $H_{ij}(W)-H_{ij}(0) = \frac1m\sum_r x_i^\top x_j\,(\mathbf 1_{r,ij}(W)-\mathbf 1_{r,ij}(0))$,
   where $\mathbf 1_{r,ij}(\cdot)=\mathbf 1\{w_r^\top x_i\ge0\}\mathbf 1\{w_r^\top x_j\ge0\}$.

2. **Sign-flip event.** $\mathbf 1_{r,ij}(W)\ne\mathbf 1_{r,ij}(0)$ requires neuron $r$ to flip
   its activation on $x_i$ or $x_j$, i.e. the event
   $A_{r,i} := \{ |w_r(0)^\top x_i| \le R\|x_i\| = R \}$ (a sign change after moving $\le R$
   forces $w_r(0)^\top x_i$ within $R$ of $0$, using $\|x_i\|=1$ and Cauchy–Schwarz
   $|(w_r-w_r(0))^\top x_i|\le R$).

3. **Gaussian anti-concentration (small-ball).** $w_r(0)^\top x_i\sim\mathcal N(0,1)$ (unit input),
   so $\Pr[A_{r,i}] = \Pr[|\mathcal N(0,1)|\le R] \le \frac{2R}{\sqrt{2\pi}} \le R$ (the standard
   normal density is $\le 1/\sqrt{2\pi}\le 1/2$, integrated over an interval of length $2R$).
   Hence $\E[\mathbf 1_{A_{r,i}}]\le R$.

4. **Expected perturbation.** $\E|H_{ij}(W)-H_{ij}(0)| \le \frac1m\sum_r |x_i^\top x_j|\,
   \Pr[A_{r,i}\cup A_{r,j}] \le \frac1m\sum_r 2R = 2R$. Summing over the $n^2$ entries and
   using $\|\cdot\|_2\le\|\cdot\|_F$ (conservatively),
   $\E\|H(W)-H(0)\|_2 \le \E\|H(W)-H(0)\|_F \le \E\sum_{ij}|H_{ij}(W)-H_{ij}(0)| \le 2n^2 R$.

5. **Markov → high-probability.** $\Pr[\|H(W)-H(0)\|_2 \ge \tfrac14\lambda_0] \le
   \frac{\E\|H(W)-H(0)\|_2}{\lambda_0/4} \le \frac{8n^2 R}{\lambda_0}$. Choosing
   $R = c\,\frac{\delta\lambda_0}{n^2}$ makes this $\le\delta$. Hence w.p. $\ge1-\delta$,
   $\|H(W)-H(0)\|_2<\tfrac14\lambda_0$, so by Weyl $\lambda_{\min}(H(W))\ge\tfrac12\lambda_0$.

**Constants / dimension dependence.** Perturbation radius scales as
$R=\Theta(\delta\lambda_0/n^2)$ for the stability event; this same radius is what the
contraction lemma's weight-movement bound must stay under (with $m$ large enough).

**Common misuses.**
- Forgetting the half-density bound (anti-concentration constant) → wrong $\Pr[A]$.
- Treating the sign-flip event as deterministic; it is random over $w_r(0)$ and we take
  expectation, then Markov.
- Bounding operator norm directly without the Frobenius detour.

**Project citation.** Anti-concentration is elementary Gaussian; the structure follows
\cite{du2019gradient} Lemma 3.2 (attribution only, proof reproduced).
