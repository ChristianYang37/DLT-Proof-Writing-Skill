# \cite{vershynin2018} — High-Dimensional Probability (textbook)

**Paper / Book.** Roman Vershynin, *High-Dimensional Probability: An
Introduction with Applications in Data Science*, Cambridge University
Press, Cambridge Series in Statistical and Probabilistic Mathematics 47
(2018). Updated PDF available at
https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.pdf .

**Exact names in PDF (results we cite).**
- Theorem 2.3.1 — Hoeffding's inequality (bounded case).
- Theorem 2.8.1 — Hoeffding's inequality for sub-Gaussian distributions.
- Theorem 2.3.4 — Hoeffding-Azuma martingale inequality (page 31).
- Exercise 2.5.10 — Maximum of $N$ sub-Gaussian random variables
  ($\E\max_{i \le N} X_i \le C \sigma \sqrt{\log N}$ for $X_i$
  centred sub-Gaussian with proxy $\sigma$, plus the corresponding
  high-probability form $\max_{i \le N} X_i \le \sigma\sqrt{2\log(N/\delta)}$
  with probability $\ge 1 - \delta$).
- Theorem 3.4.6 — Concentration on the sphere
  ($\inner{e}{u}$ sub-Gaussian with proxy $C/d$ for $u$ uniform on
  $S^{d-1}$ and fixed unit $e$).
- Theorem 5.2.3 — Gaussian concentration (§5.2.1, p. 146): for
  $X\sim N(0,I_n)$ and Lipschitz $f$, $\norm{f(X)-\E f(X)}_{\psi_2}\le
  C\norm{f}_{\mathrm{Lip}}$; the high-probability tail
  $\Pr[\abs{f(X)-\E f(X)}\ge u]\le2e^{-cu^2/\norm{f}_{\mathrm{Lip}}^2}$
  follows. The underlying Gaussian isoperimetric inequality is
  **Theorem 5.2.2**, attributed in the book to Tsirelson–Ibragimov–Sudakov
  and Borell (hence ``Borell--TIS''). Digested in `borell-tis.md`.
  (Verified by direct PDF text extraction.)
- Theorem 7.4.1 — Sudakov inequality (§7.4, p. 207): for a mean-zero
  Gaussian process $(X_t)_{t\in T}$ and any $\varepsilon\ge0$,
  $\E\sup_t X_t\ge c\,\varepsilon\sqrt{\log N(T,d,\varepsilon)}$ with $d$
  the canonical $L^2$-metric (eq. 7.13). Proved from Sudakov--Fernique
  (Theorem 7.2.8, §7.2). Digested in `sudakov-minoration.md`. (Verified by
  direct PDF text extraction.)

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

**Statement (Max of sub-Gaussian RVs, Exercise 2.5.10 of \cite{vershynin2018},
paraphrased to match our notation).** Let $X_1, \dots, X_N$ be centred
sub-Gaussian random variables with sub-Gaussian proxy $\sigma$ (no
independence required). Then
$$\E\max_{i \le N} X_i \;\le\; C\,\sigma\,\sqrt{\log N}$$
for an absolute constant $C$, and for every $\delta \in (0, 1)$,
$$\Pr\!\Big[\max_{i \le N} X_i > \sigma\sqrt{2\log(N/\delta)}\Big] \;\le\; \delta,$$
the latter following directly from a union bound applied to the per-$X_i$
sub-Gaussian tail $\Pr[X_i > t] \le \exp(-t^2/(2\sigma^2))$ at
$t = \sigma\sqrt{2\log(N/\delta)}$.

**Hypotheses (Azuma–Hoeffding).**
- $(M_t)$ is an $(\mathcal F_t)$-martingale: $\E[M_t \mid \mathcal F_{t-1}] = M_{t-1}$.
- Bounded differences: $|M_t - M_{t-1}| \le c_t$ a.s. for each $t$.
- $M_0$ deterministic (typically $0$).

**Hypotheses (Ex. 2.5.10).**
- Each $X_i$ is centred sub-Gaussian with proxy $\sigma$
  ($\E\exp(\lambda X_i) \le \exp(\lambda^2 \sigma^2/2)$ for all $\lambda$).
- $N$ finite. No independence required.

**Constants / dimension dependence.** Azuma is scalar (no $d$ factor). Ex.\
2.5.10 has the standard $\sqrt{\log N}$ scaling; the $1/\sqrt d$ factor
in our paper enters via the sub-Gaussian proxy $\sigma = C/\sqrt d$ from
Theorem 3.4.6 (sphere-concentration).

**Use in this paper.**
- Theorem 3.4.6 underpins \Cref{lem:orthogonality_high_d}'s
  $\Theta(1/d)$ projection variance.
- Theorem 2.3.4 (Azuma) is invoked via
  \Cref{lem:concentration_radial_walk} for cumulative martingale-difference
  tails. We use the Bernstein-refined form (variance-aware) following
  Freedman 1975 in our actual proofs.
- Exercise 2.5.10 (max of sub-Gaussians) is the standard reference for
  the union-bound budget used in Step~4 of \Cref{lem:gumbel_max_incoherent}.
  Note: our actual proof does NOT invoke Ex.~2.5.10 directly — we apply
  \Cref{lem:concentration_radial_walk} per direction and union-bound by
  hand. Ex.~2.5.10 is the textbook statement of the same content.

**Project .bib key.** \cite{vershynin2018}
