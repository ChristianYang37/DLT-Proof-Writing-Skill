# Freedman, "On Tail Probabilities for Martingales" (1975)

## Reference

David A. Freedman. *On Tail Probabilities for Martingales.* The Annals
of Probability, Vol. 3, No. 1 (Feb 1975), pp. 100–118. Institute of
Mathematical Statistics.
URL: https://www.jstor.org/stable/2959306
DOI: 10.1214/aop/1176996452

## What is cited

The conditional / martingale form of Bernstein's inequality
(Theorem 1.6 / Theorem 4.1 in the paper), which states that for a
martingale-difference sequence $(D_j)_{j=1}^n$ with $|D_j| \le c$ a.s.\
and predictable quadratic variation
$V_n \coloneqq \sum_{j=1}^n \E[D_j^2 \mid \mathcal F_{j-1}]$,
$$
\Pr\!\bigl[\, \sum_{j=1}^n D_j \ge u, \; V_n \le v \,\bigr]
\;\le\;
\exp\!\Bigl( -\frac{u^2}{2(v + c u/3)} \Bigr).
$$

This is the strict generalisation of Hoeffding/Azuma to martingales
with bounded conditional variance, and it gives the sharper $\exp(-cu^2/v)$
form rather than $\exp(-cu^2/(c^2 n))$ when $v \ll c^2 n$.

## Why we cite it

The proof of \Cref{lem:anchor_count_lb} applies a Bernstein-Chernoff
(multiplicative-Chernoff for Bernoullis, or Freedman's martingale
Bernstein) bound to the centred-indicator sequence
$D_j = \1\{a_j \in \Acal(Q)\} - p_j$. This gives the sharper exponent
$\exp(-p_0 T / 8)$ in place of Azuma's $\exp(-p_0^2 T / 8)$, because the
conditional variance of $D_j$ is $p_j (1-p_j) \le p_j$ rather than the
bounded-difference proxy $c_j^2 = 1$ used by Azuma.

## Verification

Citation verified against AMS MathSciNet record MR0380971 and JSTOR
stable URL 2959306. Pages 100–118 confirmed. The 1975 paper is the
canonical Freedman martingale tail bound reference, cited in
Boucheron–Lugosi–Massart (2013) §6.1 and Vershynin (2018) §2.4.
