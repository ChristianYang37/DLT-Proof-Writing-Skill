# Review iteration 1 — LSVI-UCB regret proof

## Summary

The paper proves a $\widetilde{O}(d^{3/2} \sqrt{H^3 T})$ high-probability regret bound for LSVI-UCB on linear MDPs, following the Jin et al. (2020) decomposition. The proof skeleton has five components:
(1) **Good event $\cE$** (\Cref{lem:concentration}): the empirical Bellman residual $\langle \phi, \widehat w_h^k\rangle - r_h - P_h V_{h+1}^k$ is bounded by $\beta \|\phi\|_{(\Lambda_h^k)^{-1}}$ uniformly, with $\Pr[\cE] \ge 1 - \delta$, established via self-normalised concentration + $\varepsilon$-net on the value class $\cV$.
(2) **Optimism** (\Cref{lem:optimism}): $V_h^k \ge V_h^*$ on $\cE$ by backward induction.
(3) **Per-step gap** (\Cref{lem:per-step}): on $\cE$, $Q_h^k - r_h - P_h V_{h+1}^k \le 2\beta\|\phi\|_{(\Lambda)^{-1}}$.
(4) **Decomposition** (\Cref{lem:decomposition}): $\Reg \le T_1 + T_2 + T_3$ where $T_1$ is a martingale, $T_2$ is the cumulative bonus, $T_3 = 0$.
(5) **Closing $T_1, T_2$** (\Cref{lem:azuma_mds,lem:elliptical,lem:T2_bound}): Azuma–Hoeffding closes $T_1$; elliptical-potential closes $T_2$.

The skeleton is faithful to the canonical proof. Constants are tracked through the bonus $\beta = C_\beta\, dH\sqrt\iota$ with $\iota = \log(2dKH/\delta)$.

## Strengths

- **Clean separation of concerns.** The good-event encapsulation lets the rest of the proof read deterministically. The decomposition lemma is stated as a deterministic implication on $\cE$, and the union bound is paid only once in the main proof.
- **Explicit $d^{3/2}$ origin.** \Cref{rem:T2_d_three_halves} cleanly attributes $d^{3/2}$ to $d$ (from $\beta$) plus $\sqrt d$ (from elliptical-potential), which is what readers most often miss.
- **Honest `\todo{}` flag.** Section 3 marks the bonus-constant absorption $\sqrt d + d^{3/2} \to d^{3/2}$ as needing verification — this is a constant-juggling step where AI-derived proofs commonly drop a factor.
- **Citation discipline.** All three citations (Jin 2020, Abbasi 2011, Azuma 1967) resolve in `refs.bib`.

## Weaknesses

### Weakness #1 (severity: major)
**Claim:** The proof of \Cref{lem:concentration} compresses the Bellman-residual decomposition into a chain that hides the role of $w_h^*$. Specifically, near line 79 of `03-concentration.tex`, the identity
"$\langle\phi, \widehat w_h^k\rangle - r_h - [P_h V_{h+1}^k] = \phi^\top(\Lambda)^{-1}\sum_\tau \phi_\tau \eta_\tau - \lambda\phi^\top(\Lambda)^{-1} w_h^*$"
is asserted without derivation; this step relies crucially on $r_h + P_h V_{h+1}^k$ being a linear function $\langle \phi, w_h^*\rangle$ (true by \Cref{ass:linear_mdp}), but the linear representation of $w_h^*$ is only justified parenthetically inside the proof.
**Evidence:** `03-concentration.tex:79` "$\inner{\phi(s, a)}{\wh{w}_h^k} - r_h(s, a) - [P_h V_{h+1}^k](s, a) = \phi(s, a)^\top (\Lam_h^k)^{-1} \!\!\sum_{\tau=1}^{k-1}\!\! \phi_\tau \eta_\tau^{V_{h+1}^k} - \lambda \phi(s, a)^\top (\Lam_h^k)^{-1} w_h^*$"
**Severity:** major

### Weakness #2 (severity: major)
**Claim:** The closure of the $\varepsilon$-net residual in \Cref{lem:concentration} contains an off-by-one in the residual bound. Specifically, the bound $\|\sum_\tau (\eta_\tau^{V_{h+1}^k} - \eta_\tau^{V^\dagger}) \phi_\tau\|_{(\Lam_h^k)^{-1}} \le 2 \cdot K \cdot (1/K) \cdot \sqrt k$ uses $|\eta_\tau^{V_{h+1}^k} - \eta_\tau^{V^\dagger}| \le 2\|V_{h+1}^k - V^\dagger\|_\infty \le 2/K$ but then writes "$\le 2 \cdot K \cdot \tfrac{1}{K} \cdot \sqrt k$" which has the wrong product structure: the correct bound is $\sqrt{\sum_\tau (\eta_\tau^{V_{h+1}^k} - \eta_\tau^{V^\dagger})^2 \norm{\phi_\tau}_{(\Lambda)^{-1}}^2} \le (2/K) \sqrt{k \cdot \max_\tau \|\phi_\tau\|_{(\Lambda)^{-1}}^2} \le (2/K) \sqrt d$.
**Evidence:** `03-concentration.tex:83` "$\le C_3 d^{3/2} H \sqrt{\iota} + 2 \cdot K \cdot \tfrac{1}{K} \cdot \sqrt{k}$"
**Severity:** major

### Weakness #3 (severity: minor)
**Claim:** The headline rate in \Cref{thm:main} is $\Otil(d^{3/2}\sqrt{H^3 T})$, but the prompt and \cite{jin2020provably} use the equivalent form $\Otil(d^{3/2} H \sqrt{HK})$. The remark explains the form match, but $\Otil(d^{3/2}\sqrt{H^3 T})$ is less standard.
**Evidence:** `02-main-result.tex:10` "$\Otil(d^{3/2} \sqrt{H^3 T})$"
**Severity:** minor

### Weakness #4 (severity: minor)
**Claim:** The proof of \Cref{lem:cover} elides the Lipschitz-on-$A^{-1}$ computation, citing it to Jin et al. (Lemma D.6). This is acceptable but inverts the convention that load-bearing covering bounds should be proved in-place rather than cited.
**Evidence:** `03-concentration.tex:33` "the detailed computation appears as Lemma D.6 in \cite{jin2020provably}"
**Severity:** minor

### Weakness #5 (severity: minor)
**Claim:** \Cref{lem:weight_bound} gives $\|\widehat w_h^k\| \le H\sqrt{dk}$ but the proof step "$\norm{u}_{(\Lam)^{-1}}^2 \le \norm{u}_2^2 / \lambda \le 1$" uses both $\lambda = 1$ AND a hidden assumption that $u$ is a unit vector. The hidden bound $\norm{u}_2 \le 1$ is correct since $u$ is by construction a unit vector but should be stated.
**Evidence:** `03-concentration.tex:18` "$\norm{u}_{(\Lam_h^k)^{-1}}^2 \le \norm{u}_2^2 / \lambda \le 1$"
**Severity:** minor (style)

## Questions for the author

- Q1: The bonus coefficient $\beta = C_\beta\, d H\sqrt\iota$ is stated and used throughout, but the **value** of $C_\beta$ is left as "sufficiently large universal". For replicability (e.g., experiments-plan.md), can a numerical $C_\beta$ be given?
- Q2: \Cref{rem:T1_T3_separation} sets $T_3 = 0$ "for symmetry". Is this consistent with \cite{jin2020provably}'s three-term decomposition, or is the merger of $T_1$ and $T_3$ a notational choice?
- Q3: The bound says "$\log(4/\delta) \le \iota$ ... for $d \ge 2$". For $d = 1$, is the proof still valid without additional constants? The remark dismisses this with "absorb the constant" — is this precise?

## Verdict
accept-with-minor-revisions
