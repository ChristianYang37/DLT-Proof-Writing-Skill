# Local Fano method for minimax lower bounds

**Source.** Tsybakov, *Introduction to Nonparametric Estimation*, Springer
2009, §2.2 (reduction to hypothesis testing) and the Fano-type bound around
Theorem 2.5 / Corollary 2.6. Equivalent modern statement in Wainwright,
*High-Dimensional Statistics*, 2019, Ch. 15 (Fano method). Cite key
`tsybakov2009introduction`.

**Statement (Fano testing inequality, faithfully paraphrased).** Let
$V$ be uniform on $\{1,\dots,M\}$, $M\ge 2$, and let $Y$ be an observation
with conditional law $P_k$ when $V=k$. For any (possibly randomized) test
$\psi(Y)\in\{1,\dots,M\}$,
$$\inf_{\psi}\Pr[\psi(Y)\ne V]
\;\ge\; 1 - \frac{I(V;Y) + \log 2}{\log M},$$
and the mutual information is bounded by the pairwise-KL diameter
$$I(V;Y) \;\le\; \frac{1}{M^2}\sum_{k,k'}\KL(P_k\,\|\,P_{k'})
\;\le\; \max_{k\ne k'}\KL(P_k\,\|\,P_{k'}).$$

**Reduction to estimation (separation step).** If the parameters
$f_1,\dots,f_M$ are $2\Delta$-separated in the (pseudo)metric $\rho$
(i.e. $\rho(f_k,f_{k'})\ge 2\Delta$ for $k\ne k'$), then any estimator
$\hat f$ induces a test (map $\hat f$ to its nearest $f_k$) whose error
lower-bounds the estimation error:
$$\inf_{\hat f}\max_k \E_{P_k}[\rho^2(\hat f,f_k)]
\;\ge\; \Delta^2 \cdot \inf_\psi \Pr[\psi\ne V].$$

**Hypotheses.**
- $M\ge 2$ hypotheses, $V$ uniform.
- A valid separation $\rho(f_k,f_{k'})\ge 2\Delta$ for all $k\ne k'$.
- A finite pairwise-KL bound $\KL(P_k\|P_{k'})\le \alpha\log M$ with $\alpha$
  a small constant (here we drive $\alpha\le 1/16$ so the Fano RHS is
  $\ge$ const $>0$).

**Constants and dimension dependence.** The clean sufficient condition: if
$\max_{k\ne k'}\KL(P_k\|P_{k'}) \le \frac{1}{16}\log M$ and $M\ge 16$, then
$1 - (I+\log2)/\log M \ge 1 - (\tfrac{1}{16}\log M + \log 2)/\log M
\ge 1 - 1/16 - \log2/\log M \ge 1/2$ for $M$ large. So the testing error is
$\ge 1/2$, giving $\inf_{\hat f}\max_k \E\,\rho^2 \ge \Delta^2/2$.

**Canonical use pattern.** Choose the perturbation magnitude $\omega$ so that
(i) the separation $\Delta \asymp$ rate and (ii) the KL diameter $\le
\frac1{16}\log M$. The two constraints both scale with $\omega^2$ and with
$m$, and balancing $m\asymp n^{1/(2s+d)}$ makes them compatible at the
minimax rate.

**Common misuses.**
- Bounding $I(V;Y)$ by the wrong (un-averaged) KL — must use the convexity
  bound $I\le \max_{k,k'}\KL$, valid because $I(V;Y)\le \frac1{M}\sum_k
  \KL(P_k\|\bar P)\le \frac1{M^2}\sum_{k,k'}\KL(P_k\|P_{k'})$.
- Dropping the $+\log 2$ in the numerator (it is what forces $M$ not too small).
- Forgetting the factor $2$ in the separation ($2\Delta$ apart $\Rightarrow$
  $\Delta$-radius balls disjoint).

**Project citation key.** `\cite{tsybakov2009introduction}`.
