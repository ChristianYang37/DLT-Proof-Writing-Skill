# Hoeffding's inequality (bounded-RV concentration) — entrywise Gram concentration

**Source.** Vershynin, *High-Dimensional Probability*, Cambridge 2018, Theorem 2.2.6
(Hoeffding for bounded independent variables).

**Statement.** Let $Z_1,\dots,Z_m$ be independent with $Z_r\in[\alpha_r,\beta_r]$ a.s.,
$S=\sum_{r=1}^m Z_r$. Then for all $t>0$,
$\Pr[|S-\E S|\ge t] \le 2\exp\!\big(-\frac{2t^2}{\sum_r(\beta_r-\alpha_r)^2}\big)$.

**Hypotheses.**
- Independence of the $Z_r$ (here: independence across neurons $r$, since the $w_r(0)$ are i.i.d.).
- Almost-sure boundedness.

**Constants / dimension dependence.** Dimension-free; the only quantity is the sum of
squared ranges $\sum_r(\beta_r-\alpha_r)^2$.

**Application in `lem:init-gram-close`.** Fix $i,j$. Write
$H_{ij}(0) = \frac1m\sum_{r=1}^m x_i^\top x_j\,\mathbf 1\{w_r(0)^\top x_i\ge0,\,w_r(0)^\top x_j\ge0\}$.
Each summand $Z_r := \frac1m x_i^\top x_j\,\mathbf 1\{\cdots\}$ is independent across $r$ and
lies in $[-1/m, 1/m]$ (since $|x_i^\top x_j|\le1$ for unit inputs), so range $\le 2/m$.
$\E H_{ij}(0) = H^\infty_{ij}$ by definition. Hoeffding with
$\sum_r(\beta_r-\alpha_r)^2 \le m\cdot(2/m)^2 = 4/m$ gives
$\Pr[|H_{ij}(0)-H^\infty_{ij}|\ge t] \le 2\exp(-m t^2/2)$.
Taking $t = \sqrt{2\log(2n^2/\delta)/m}$ and union-bounding over the $n^2$ pairs gives
$|H_{ij}(0)-H^\infty_{ij}| \le \sqrt{2\log(2n^2/\delta)/m}$ for all $i,j$ w.p. $\ge1-\delta$.

**Frobenius → operator → Weyl chain.** Then
$\|H(0)-H^\infty\|_2 \le \|H(0)-H^\infty\|_F = \big(\sum_{ij}|H_{ij}(0)-H^\infty_{ij}|^2\big)^{1/2}
\le n\sqrt{2\log(2n^2/\delta)/m}$, and Weyl gives
$\lambda_{\min}(H(0))\ge\lambda_0 - n\sqrt{2\log(2n^2/\delta)/m}\ge\tfrac34\lambda_0$
once $m \ge 32 n^2\log(2n^2/\delta)/\lambda_0^2$.

**Common misuses.**
- Forgetting the $1/m$ scaling makes the range wrong (range is $2/m$ not $2$).
- Using a single $t$ without the union bound over $n^2$ entries.
- Bounding operator norm directly without the Frobenius detour (loses the clean entrywise route).

**Project citation.** \cite{vershynin2018high}, stated as `\begin{fact}[\cite{vershynin2018high}]`.
