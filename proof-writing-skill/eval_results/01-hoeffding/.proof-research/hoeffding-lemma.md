# Hoeffding's lemma — MGF bound for bounded centered RVs

**Source.** Boucheron, Lugosi, Massart, *Concentration Inequalities* (2013), Lemma 2.2; also Vershynin, *High-Dimensional Probability* (2018), Lemma 2.6.1. Original: W. Hoeffding (1963), *Probability inequalities for sums of bounded random variables*, JASA.

**Statement.** Let $X$ be a real-valued random variable with $\E X = 0$ and $X \in [a, b]$ almost surely, where $a \le 0 \le b$. Then for every $\lambda \in \R$,
$$
\E\bigl[e^{\lambda X}\bigr] \;\le\; \exp\!\Bigl(\tfrac{\lambda^2 (b - a)^2}{8}\Bigr).
$$

**Hypotheses.**
- $X$ is a real random variable (no independence yet required at this lemma level).
- $X \in [a, b]$ almost surely, with $a \le b$ real numbers.
- $\E X = 0$ (centered). Equivalently: for an uncentered $Y \in [a', b']$, apply to $X = Y - \E Y$, which lies in $[a' - \E Y, b' - \E Y]$, an interval of the same length $b' - a'$.
- $\lambda \in \R$ arbitrary (both signs allowed; the bound is symmetric in $\lambda$).

**Constants.** The factor $1/8$ in the exponent is sharp for this lemma; it cannot be improved without additional structure (e.g., a variance bound would replace $(b-a)^2/4$ by $\Var X$ via Bennett/Bernstein). The MGF inequality is therefore sub-Gaussian with proxy $\sigma^2 = (b-a)^2/4$.

**Proof sketch (standard).** Define $\psi(\lambda) := \log \E[e^{\lambda X}]$. Then
$\psi'(\lambda) = \E_\lambda[X]$ and $\psi''(\lambda) = \Var_\lambda(X)$, where the
expectation/variance is under the tilted measure with density proportional to
$e^{\lambda x}$. Since $X \in [a, b]$ under the tilt, $\Var_\lambda(X) \le (b-a)^2/4$ by
Popoviciu's inequality on variance for bounded random variables (the maximum of $\Var X$
over distributions on $[a,b]$ is $(b-a)^2/4$, attained at the two-point distribution with
mass $1/2$ each on $a$ and $b$). With $\psi(0) = 0$ and $\psi'(0) = \E X = 0$, Taylor's
theorem with integral remainder gives
$\psi(\lambda) = \int_0^\lambda (\lambda - s) \psi''(s)\,ds \le (b-a)^2/4 \cdot \lambda^2/2
= \lambda^2 (b-a)^2 / 8$. Exponentiating gives the claim.

**Canonical use pattern (Chernoff + Hoeffding's lemma).**

```latex
By Markov applied to $e^{\lambda S_n}$ for $\lambda > 0$,
\begin{align*}
\Pr[S_n \ge t]
&\;\le\; e^{-\lambda t}\, \E\!\bigl[e^{\lambda S_n}\bigr] \\
&\;=\; e^{-\lambda t}\, \prod_{i=1}^n \E\!\bigl[e^{\lambda X_i}\bigr]
       \tag{independence} \\
&\;\le\; e^{-\lambda t}\, \prod_{i=1}^n \exp\!\Bigl(\tfrac{\lambda^2 (b_i - a_i)^2}{8}\Bigr)
       \tag{Hoeffding's lemma} \\
&\;=\; \exp\!\Bigl(-\lambda t + \tfrac{\lambda^2}{8} \textstyle\sum_i (b_i - a_i)^2\Bigr).
\end{align*}
Optimize: the right side is minimized at $\lambda^\star = 4t / \sum_i (b_i - a_i)^2$,
giving $\exp(-2t^2 / \sum_i (b_i - a_i)^2)$.
```

**Common misuses.**
- Forgetting to center: $X \in [a, b]$ with $\E X \ne 0$ does not give $\E e^{\lambda X} \le e^{\lambda^2 (b-a)^2 / 8}$ — it gives $\E e^{\lambda(X - \E X)} \le \ldots$, with an extra factor $e^{\lambda \E X}$ that must be tracked.
- Off-by-factor: writing $\lambda^2 (b-a)^2 / 2$ instead of $/8$ (the variance-proxy version of sub-Gaussianity uses $\sigma^2 = (b-a)^2 / 4$, which appears as $\sigma^2/2$ in the standard form $e^{\lambda^2 \sigma^2 / 2}$, hence $/8$).
- Applying with $\lambda < 0$ to bound the upper tail (works, but yields a trivial bound — use $\lambda > 0$ for upper, $\lambda < 0$ for lower).
- Confusing Popoviciu (variance on bounded support: $\Var X \le (b-a)^2/4$) with the deterministic identity $\max_{p} p(1-p)(b-a)^2 = (b-a)^2/4$. Same number, but Popoviciu states it as a variance inequality over all distributions on $[a,b]$.

**Project citation key.** Not cited (the proof writes Hoeffding's lemma out in
full as a standalone lemma in the appendix). If the project wanted an external
cite, the standard choices are `\cite{boucheron2013concentration}` or
`\cite{vershynin2018high}`.
