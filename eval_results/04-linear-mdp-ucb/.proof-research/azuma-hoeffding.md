# Azuma–Hoeffding Inequality

**Source.** Standard textbook fact; see Boucheron–Lugosi–Massart §2.1, or Wainwright *High-Dimensional Statistics* Cor 2.20.

**Statement.** Let $\{X_t\}_{t=1}^T$ be a martingale-difference sequence with respect to $\{\mathcal{F}_t\}$ (so $\E[X_t \mid \mathcal{F}_{t-1}] = 0$), and suppose $|X_t| \le c_t$ a.s. Then for any $\epsilon > 0$,
$$\Pr\!\Bigl[\,\Bigl|\sum_{t=1}^T X_t\Bigr| \ge \epsilon\,\Bigr] \;\le\; 2 \exp\!\Bigl(-\tfrac{\epsilon^2}{2 \sum_{t=1}^T c_t^2}\Bigr).$$

**Common form used in regret proofs.** For $c_t = c$ a constant: $\Pr[|\sum X_t| \ge c \sqrt{2 T \log(2/\delta)}] \le \delta$, i.e., with probability at least $1 - \delta$,
$$\Bigl|\sum_{t=1}^T X_t\Bigr| \le c \sqrt{2 T \log(2/\delta)}.$$

**Hypotheses.**
- Martingale differences (zero conditional mean). Not just bounded — the conditional-mean-zero structure is essential.
- Uniform a.s. bound $|X_t| \le c_t$.

**Canonical use in LSVI-UCB regret bound (term $T_1$).**
```latex
The sequence $\zeta_h^k := \E[V_{h+1}^{\pi^k}(s_{h+1}^k) - V_{h+1}^{\pi^k}(s_h^k, a_h^k)] - [V_{h+1}^{\pi^k}(s_{h+1}^k) - V_{h+1}^{\pi^k}(s_h^k, a_h^k)]$
is a martingale-difference sequence with $|\zeta_h^k| \le 2H$. By Azuma--Hoeffding,
$\big|\sum_{k,h} \zeta_h^k\big| \le 2 H \sqrt{2 H T \log(1/\delta)}$ w.p. $\ge 1 - \delta$.
```

**Common misuses.**
- Not centering: forgetting to subtract conditional expectation — without centering, no martingale.
- Failing to verify $|X_t| \le c_t$ a.s. (only in expectation).

**Project citation key.** Textbook reference; we cite `\cite{azuma1967weighted}` per Jin et al. or treat as canonical (no cite needed if we cite a textbook).
