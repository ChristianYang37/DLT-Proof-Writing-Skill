# \cite{du2019gradient} — Du–Zhai–Poczos–Singh, two-layer NTK convergence

**Paper.** "Gradient Descent Provably Optimizes Over-parameterized Neural Networks",
Simon S. Du, Xiyu Zhai, Barnabas Poczos, Aarti Singh, ICLR 2019, arXiv:1810.02054.

**Exact names in PDF (v3).**
- Definition of $H^\infty$ (their Eq. for the Gram limit):
  $H^\infty_{ij} = \E_{w\sim\mathcal N(0,I)}[x_i^\top x_j \,\mathbf 1\{w^\top x_i\ge 0, w^\top x_j\ge 0\}]$.
- Their Lemma 3.1: with prob $1-\delta$, $\|H(0)-H^\infty\|_2$ is small and
  $\lambda_{\min}(H(0))\ge\tfrac34\lambda_0$ for $m=\Omega(n^2\lambda_0^{-2}\log(n/\delta))$.
- Their Lemma 3.2: if $\|w_r-w_r(0)\|\le R$ for all $r$ with $R = c\delta\lambda_0/n^2$, then
  $\|H(W)-H(0)\|_2 < \tfrac14\lambda_0$, hence $\lambda_{\min}(H(W))\ge\tfrac12\lambda_0$.
- Their Theorem 3.1 (gradient flow) and Theorem 4.1 (discrete GD): with
  $m = \Omega(n^6\lambda_0^{-4}\delta^{-3})$ and $\eta = O(\lambda_0/n^2)$,
  $\|y - u(k)\|_2^2 \le (1-\tfrac{\eta\lambda_0}{2})^k \|y-u(0)\|_2^2$ w.p. $\ge 1-\delta$.

**Statement (faithfully paraphrased), discrete GD (their Thm 4.1).**
For $f(x)=\frac1{\sqrt m}\sum_r a_r\sigma(w_r^\top x)$, $w_r(0)\sim\mathcal N(0,I)$,
$a_r\sim\text{Unif}\{\pm1\}$ fixed, training $W$ only by GD on $\tfrac12\|y-u\|_2^2$:
if $\lambda_0=\lambda_{\min}(H^\infty)>0$, $m=\Omega(n^6/(\lambda_0^4\delta^3))$,
$\eta=O(\lambda_0/n^2)$, then w.p. $\ge1-\delta$ over init,
$\|y-u(k)\|_2^2\le(1-\eta\lambda_0/2)^k\|y-u(0)\|_2^2$ for all $k\ge0$.

**Hypotheses.**
- Data normalized $\|x_i\|_2=1$; no two parallel inputs ($x_i\not\parallel x_j$ for $i\ne j$),
  which guarantees $\lambda_0>0$.
- $a_r$ fixed at init (only first layer trained).
- $\lambda_0:=\lambda_{\min}(H^\infty)>0$ the single spectral assumption.

**Constants / dimension dependence.**
- Width polynomial $m=\Omega(n^6\lambda_0^{-4}\delta^{-3})$; step $\eta=O(\lambda_0/n^2)$;
  contraction factor $1-\eta\lambda_0/2$.
- Perturbation radius $R=O(\delta\lambda_0/n^2)$ keeps $\lambda_{\min}(H(W))\ge\lambda_0/2$.

**Project .bib key.** \cite{du2019gradient}

**Note on usage in this proof.** We reproduce the *structure* (three lemmas + fixed-point
induction) and prove each lemma ourselves; the only `\cite{du2019gradient}` is an
attribution of the overall NTK skeleton and the $H^\infty$ definition, used in Remarks,
not as a black-box theorem substitute. No theorem is invoked as `\begin{X}[\cite{...}]`.
