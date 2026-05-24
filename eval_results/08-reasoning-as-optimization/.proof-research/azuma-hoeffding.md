# Azuma–Hoeffding inequality (technique digest)

**Source.** Vershynin, *High-Dimensional Probability* (CUP, 2018),
Theorem 2.3.4, page 31; also Boucheron–Lugosi–Massart,
*Concentration Inequalities* (OUP, 2013), §2.4 and §3.6;
Durrett, *Probability: Theory and Examples* (5th ed., 2019),
Theorem 5.2.6.

**Statement (scalar form, sufficient for this paper).** Let $(M_t)_{t \ge 0}$
be a real-valued martingale with respect to a filtration
$(\mathcal F_t)_{t \ge 0}$, with $M_0 = 0$ and bounded differences
$|M_t - M_{t-1}| \le c_t$ almost surely for each $t \ge 1$. Then for
every $t \ge 1$ and every $u > 0$,
$$
   \Pr\!\big[\, M_t \ge u \,\big]
   \;\le\;
   \exp\!\left(\,
      -\frac{u^2}{2 \sum_{s=1}^{t} c_s^2}
   \,\right),
   \qquad
   \Pr\!\big[\, |M_t| \ge u \,\big]
   \;\le\;
   2 \exp\!\left(\,
      -\frac{u^2}{2 \sum_{s=1}^{t} c_s^2}
   \,\right).
$$
The two-sided form follows by a union bound on $M_t$ and $-M_t$.

**Hypotheses (verbatim).**
- $(M_t)$ is an $(\mathcal F_t)$-martingale: $\E[M_t \mid \mathcal F_{t-1}] = M_{t-1}$ a.s.
- Bounded differences: $|M_t - M_{t-1}| \le c_t$ almost surely, with $c_t$
  deterministic (or, at minimum, $\mathcal F_{t-1}$-measurable).
- $M_0$ is deterministic (commonly $M_0 = 0$).

**Constants and dimension dependence.** None — Azuma–Hoeffding is scalar
and the exponent constant $1/2$ is tight for sub-Gaussian bounded
differences. The right-tail bound becomes $\exp(-u^2 / (2 t))$ when
$c_t \equiv 1$ for all $t$.

**Canonical use pattern.** Suppose $X_1, X_2, \ldots$ is a sequence of
$[0,1]$-valued random variables with $\E[X_j \mid \mathcal F_{j-1}] \ge p_0$
for all $j$. Define
$M_t \coloneqq \sum_{s \le t} \bigl( X_s - \E[X_s \mid \mathcal F_{s-1}] \bigr)$,
which is a martingale with $|M_t - M_{t-1}| \le 1$. Apply Azuma:
$$
   \Pr\!\bigg[\, \sum_{s \le t} X_s \,<\, p_0 t - u \,\bigg]
   \;\le\;
   \Pr\!\bigg[\, M_t \,<\, -u \,\bigg]
   \;\le\;
   \exp(- u^2 / (2 t)).
$$
Choosing $u = p_0 t / 2$ gives
$\Pr[\sum X_s < p_0 t / 2] \le \exp(-p_0^2 t / 8)$.

**Common misuses.**
- Applying Azuma to a partial sum that is not a martingale (e.g. summing
  $X_j$ rather than the centred differences).
- Forgetting the bounded-difference hypothesis (Azuma fails for unbounded
  $M_t - M_{t-1}$ without a sub-Gaussian assumption — that is McDiarmid /
  Freedman territory).
- Using $c_t = 1$ when the actual differences can be as large as $2$
  (e.g. indicators of an event minus its probability can lie in $[-1, 1]$,
  so the difference is in $[-1, 1]$ and $c_t = 1$ is correct; but
  $[-1, 1]$-valued martingale differences have range $2$, so a careless
  reader can be off by $4$ in the exponent).
- Cherry-picking a stopping time $T$ and applying Azuma at $t = T$
  without justifying the optional-stopping conditions.

**Project citation key.** \cite{vershynin2018} (Theorem 2.3.4).

**Use in this paper.** Applied once in the proof of
\Cref{lem:anchor_count_lb} to lower-bound the number of anchor emissions
in $T$ steps. The martingale is the centred indicator
$M_t = \sum_{s \le t} (\1\{s \in \mathcal A^{\mathrm{traj}}\} - p_s)$
with $p_s \coloneqq \Pr[s \in \mathcal A^{\mathrm{traj}} \mid \mathcal F_{s-1}] \ge p_0$
by \Cref{ass:anchor_emission_prob}. Bounded differences hold with
$c_s = 1$. Choosing $u = p_0 T / 2$ yields
$\Pr[|\mathcal A^{\mathrm{traj}} \cap [T]| < p_0 T / 2] \le \exp(-p_0^2 T / 8)$.
We use the failure budget $\exp(-p_0^2 T / 8) \le \delta / 2$ in the
union bound for \Cref{thm:main_convergence_hp}.
