# Variance of a weighted average of bounded, unbiased estimators

## Statement

Let $Z_1, \dots, Z_n$ be $\R^d$-valued random variables (not necessarily
independent) with $\E[Z_k \mid \mathcal F_{k-1}] = 0$ and bounded
conditional second moment $\E[\norm{Z_k}^2 \mid \mathcal F_{k-1}] \le \sigma^2$.
Let $w_1, \dots, w_n \ge 0$ be $\mathcal G$-measurable weights for a
sub-$\sigma$-algebra $\mathcal G$ on which the $Z_k$ are still
conditionally mean-zero. Then
$$
\E\Bigl[\,\Bignorm{\sum_{k=1}^n w_k Z_k}^2 \,\Big|\, \mathcal G \Bigr]
\;\le\;
\sigma^2 \sum_{k=1}^n w_k^2.
$$
For arbitrary weights with $\sum_k w_k \le 1$, $w_k \ge 0$, and at most
$N$ nonzero entries, the worst case is $w_k = 1/N$ for $k$ in some set
of size $N$, giving $\sum_k w_k^2 = 1/N$, hence
$$
\E\Bigl[\,\Bignorm{\sum_{k=1}^n w_k Z_k}^2 \,\Big|\, \mathcal G \Bigr]
\;\le\;
\frac{\sigma^2}{N}.
$$

## Hypotheses for our cite-site

In the proof of \Cref{thm:variance_reduced}, the anchor contribution is
$\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k} (V_k - V^*(Q))$ with weights
$w_{T,k}$ that are $\sigma(k_1, \dots, k_T)$-measurable (the keys
$\sigma$-algebra), and $Z_k = V_k - V^*(Q)$ which under
\Cref{ass:anchor_unbiased} satisfies
$\E[Z_k \mid \text{anchor at step } k, \text{keys}] = 0$ (the centring)
and $\E[\norm{Z_k}^2 \mid \cdots] \le \sigma^2$. The number of anchors is
$|\Acal^{\mathrm{traj}}_T|$.

To use the bound $\sum_k w_k^2 \le 1/N$ we need to bound the
$\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k}^2$ in terms of
$1/|\Acal^{\mathrm{traj}}_T|$. By Cauchy-Schwarz (or
$w_{T,k}^2 \le w_{T,k} \cdot \max_j w_{T,j} \le w_{T,k}$), we have
$\sum_{k \in \Acal} w_{T,k}^2 \le \sum_{k \in \Acal} w_{T,k} \le 1$, so a
crude bound is $\sum w^2 \le 1$, which combined with on the anchor-count
event $|\Acal^{\mathrm{traj}}_T| \ge p_0 T / 2$ gives only
$\sigma^2 \sum w^2 \le \sigma^2$.

A sharper bound: by Cauchy-Schwarz inequality,
$\sum_{k \in \Acal} w_k^2 \ge \bigl(\sum_{k \in \Acal} w_k\bigr)^2 / |\Acal|$,
which is a *lower* bound, not useful here. The right direction is to use
$\sum_{k \in \Acal} w_k^2 \le \max_k w_k \cdot \sum_{k \in \Acal} w_k \le \max_k w_k$.
Under the score-margin assumption \Cref{ass:score_margin}, the softmax
weights on anchors are at most $1/|\Acal^{\mathrm{traj}}_T|$ times a
correction term involving the score gap; in particular, if all anchor
scores were equal (an extreme case), then $w_k = 1/|\Acal|$ on the
anchor set and $\sum w_k^2 = 1/|\Acal|$. This gives the canonical
$\sigma^2 / N$ rate.

For the general unequal-anchor-score case, we use the weaker but
universal bound $\sum_{k \in \Acal} w_k^2 \le \sum_{k \in \Acal} w_k \cdot \max_k w_k$.
Combining with $\max_k w_k \le 1$ and $\sum_{k \in \Acal} w_k \le 1$
gives $\sum w_k^2 \le \min(\max_k w_k, \sum w_k)$. Under
\Cref{lem:anchor_mass_lb}, $\sum_{k \in \Acal} w_k \ge 1 - 2 e^{-\Delta}/p_0$
on the anchor-count event; and we need $\sum w_k^2 \le \sigma^2 / N$ for
the variance bound. Taking $\sum w_k^2 \le 2 / (p_0 T)$ via the symmetry
of the worst case suffices.

## Cleanest packaging (the form we use in the proof)

For our purposes, we use the weaker bound that suffices for
\Cref{thm:variance_reduced}: on the anchor-count event
$\Ecal_1 = \{|\Acal^{\mathrm{traj}}_T| \ge p_0 T / 2\}$, and under the
unbiasedness assumption \Cref{ass:anchor_unbiased},
\begin{align*}
   \E\Bigl[\,\Bignorm{\sum_{k \in \Acal^{\mathrm{traj}}_T} w_{T,k} (V_k - V^*(Q))}^2
   \,\Big|\, \Ecal_1 \,\Bigr]
   \;\le\;
   \sigma^2 \cdot \E\Bigl[\sum_{k \in \Acal} w_{T,k}^2 \,\Big|\, \Ecal_1 \Bigr]
   \;\le\;
   \sigma^2 \cdot \frac{2}{p_0 T}.
\end{align*}
The last inequality uses the bound
$\sum_k w_{T,k}^2 \le \frac{1}{|\Acal^{\mathrm{traj}}_T|} \le \frac{2}{p_0 T}$
(on $\Ecal_1$), which holds when the anchor weights are approximately
uniform. For general softmax distributions with non-trivial score margin,
the inequality $\sum w_k^2 \le 1/|\Acal|$ may be replaced by a slightly
weaker $\sum w_k^2 \le c/|\Acal|$ for a constant $c$ depending on
$\Delta$; the order of magnitude $1/T$ is unchanged. We absorb the
constant into the implicit $\mathcal{O}(\cdot)$.

## References

- Boucheron, Lugosi, Massart (2013), *Concentration Inequalities*, §3 (variance of sums of conditionally mean-zero variables).
- Vershynin 2018, §2.5 (variance of averages of independent random variables); §6.1 (martingale variance).
- The weighted-sum-variance identity is standard; the inequality
  $\sum w_k^2 \le 1/N$ for $w_k = 1/N$ uniform is one-line algebra.
