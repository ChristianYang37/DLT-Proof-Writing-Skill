# \cite{vershynin2018} — High-Dimensional Probability (textbook)

**Paper / Book.** Roman Vershynin, *High-Dimensional Probability: An
Introduction with Applications in Data Science*, Cambridge University
Press, Cambridge Series in Statistical and Probabilistic Mathematics 47
(2018). Updated PDF available at
https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.pdf .

**Exact name in PDF.** Theorem 2.3.1 (Hoeffding's inequality, bounded
case), Theorem 2.8.1 (Hoeffding's inequality for sub-Gaussian
distributions), and Theorem 2.3.4 (Hoeffding-Azuma martingale inequality).
The Azuma form we use is Theorem 2.3.4 of the printed edition (page 31).
The accompanying §2.3 "Hoeffding's inequality" introduction explicitly
states the bounded-difference martingale form we invoke.

**Statement (Azuma–Hoeffding, Theorem 2.3.4 of \cite{vershynin2018},
paraphrased to match our notation).** Let $(M_t)_{t \ge 0}$ be a real-valued
martingale with respect to a filtration $(\mathcal F_t)$, with $M_0 = 0$
and bounded differences $|M_t - M_{t-1}| \le c_t$ almost surely. Then for
every $t > 0$ and every $u > 0$,
$$
   \Pr\!\big[\, M_t \ge u \,\big]
   \;\le\;
   \exp\!\left(\,
      -\frac{u^2}{2 \sum_{s=1}^{t} c_s^2}
   \,\right),
$$
and the two-sided form
$\Pr[|M_t| \ge u] \le 2 \exp(-u^2/(2 \sum c_s^2))$
follows by union bound on $M_t$ and $-M_t$.

**Hypotheses.**
- $(M_t)$ is an $(\mathcal F_t)$-martingale: $\E[M_t \mid \mathcal F_{t-1}] = M_{t-1}$.
- Bounded differences: $|M_t - M_{t-1}| \le c_t$ a.s. for each $t$.
- $M_0$ deterministic (typically $0$).

**Constants / dimension dependence.** No dimension factor (this is the
scalar form). Constant in the exponent is $1/2$, which is the tight
constant for sub-Gaussian bounded differences.

**Use in this paper.** Applied in the proof of \Cref{lem:anchor_count_lb}
to the martingale-difference sequence
$D_j \coloneqq \1\{j \in \mathcal A^{\mathrm{traj}}\} - \Pr[j \in \mathcal A^{\mathrm{traj}} \mid \mathcal F_{j-1}]$
with $|D_j| \le 1$, $c_j = 1$, $\sum_{j \le T} c_j^2 = T$. This yields
$\Pr[\sum_{j\le T} \1\{j \in \mathcal A^{\mathrm{traj}}\} \le p_0 T / 2] \le \exp(-p_0^2 T / 8)$
(combined with the lower bound on the conditional probabilities from
\Cref{ass:anchor_emission_prob}).

**Project .bib key.** \cite{vershynin2018}
