# Anti-concentration: lower bound on the maximum of |V|-1 logits

**PRIMARY ROUTE (as of 2026-05-29): Sudakov minoration + Borell--TIS.**
`lem:incorrect_max_lower` is proved by item 2 below (Sudakov minoration for
$\E\max$ + Borell--TIS Gaussian concentration to pin the max to its mean),
under the isotropic-Gaussian noise form `eq:noise_gaussian` of
`ass:bounded_architecture(5)`. The second-moment / Paley--Zygmund method
(item 1) is **NOT used** — see "Why not the second moment" below; it is
unsound for constant incoherence $\mu_0$. Digests:
`sudakov-minoration.md` (Vershynin Thm 7.4.1) and `borell-tis.md`
(Vershynin Thm 5.2.3).

**Purpose.** The FAILURE branch of R1 (Constraint #7) needs a
high-probability **lower** bound on $\max_{a\neq a^\star}\langle W_U^a,
x_T\rangle$ — i.e.\ "some incorrect logit is large". This is the
anti-concentration counterpart of the incorrect-max UPPER bound
(`lem:incorrect_max`, ported Lemma A). It is NOT a reversed Lemma A and
NOT a Galton-Watson coupling: it is a direct max-lower bound on the
$|V|-1$ incorrect logits.

**Source(s).** Roman Vershynin, *High-Dimensional Probability* (2018) —
see `cite-vershynin2018.md`. The facts the PRIMARY route uses (theorem
numbers VERIFIED verbatim against the official PDF by text extraction):
- **Theorem 7.4.1** (Sudakov minoration, §7.4): for a mean-zero Gaussian
  process $(X_t)_{t\in T}$, $\E\sup_t X_t\ge c\,\varepsilon\sqrt{\log
  N(T,d,\varepsilon)}$ with $d$ the canonical $L^2$-metric. Digest
  `sudakov-minoration.md`.
- **Theorem 5.2.3** (Gaussian concentration / Borell--TIS, §5.2.1): for
  $X\sim N(0,I_n)$ and Lipschitz $f$, $\norm{f(X)-\E f(X)}_{\psi_2}\le
  C\norm{f}_{\mathrm{Lip}}$; the underlying Gaussian isoperimetry
  (Thm 5.2.2) is Tsirelson--Ibragimov--Sudakov + Borell. Digest
  `borell-tis.md`.

Also relevant (used elsewhere / for context):
- **Theorem 3.4.6** (concentration on the sphere): $\langle e,u\rangle$
  sub-Gaussian with proxy $C/d$; underpins the $\sigma_T\sim1/\sqrt d$
  scale (used by `lem:incorrect_max`, `lem:orthogonality`).
- **Exercise 2.5.10** (max of $N$ sub-Gaussians): the UPPER bound
  $\E\max_i X_i \le C\sigma\sqrt{\log N}$ (the upper-bound counterpart,
  `lem:incorrect_max`).

**Statement (the tool we invoke).** Let $Y_1,\dots,Y_N$ be (possibly
correlated) mean-shifted sub-Gaussian random variables, $Y_a = \mu_a +
Z_a$ with $Z_a$ centred, proxy $\sigma$. Then there is a high-probability
LOWER bound on the max via either of:

1. **Gaussian-max / second-moment (Paley–Zygmund-style). [NOT USED —
   unsound for constant $\mu_0$; see "Why NOT the second moment" below.]**
   If a subset $S\subseteq[N]$ of size $|S|=m$ of the $Z_a$ are pairwise
   "sufficiently decorrelated" (covariance $\le \rho\sigma^2$ off-diagonal
   with $\rho<1$), then naively
   $\max_{a\in S} Z_a \ge \sigma\sqrt{2(1-\rho)\log m} \cdot (1-o(1))$
   with probability $\ge 1 - m^{-c}$. The variance-control step
   $\mathrm{Var}\,N_t=o((\E N_t)^2)$ FAILS for constant $\rho=\mu_0$ at the
   relevant threshold (the pair-covariance sum is $m^{\Theta(\mu_0)}(\E
   N_t)^2$); valid only for $\mu_0=O(1/\log m)$. Retired in favour of
   item 2.

2. **Sudakov minoration / Sudakov–Fernique** (cleaner when the $Z_a$ form
   a Gaussian-like process): $\E\max_{a} Z_a \ge c\,\sigma\sqrt{\log N}$
   provided the canonical metric $\E(Z_a-Z_b)^2 \gtrsim \sigma^2$ for
   $\gtrsim N$ well-separated pairs. The incoherence A2 ($\mu(W_U)\le\mu_0$)
   gives exactly this pairwise separation:
   $\E(Z_a-Z_b)^2 = \mathrm{Var}\langle W_U^a-W_U^b, \text{noise}\rangle
   \asymp \|W_U^a-W_U^b\|^2/d \ge 2\rho_0^2(1-\mu_0)/d$.

**How it closes the failure branch (Stage-2 sketch).** When the drift
$\delta$ is sub-threshold, the correct logit's expected value
$\le m^\star$ is small, while the $|V|-1$ incorrect logits each have
fluctuation scale $\sigma_T \asymp R_U M/\sqrt{T_{\max} d}$ (same noise
provenance as Lemma A). Their max therefore exceeds
$\sigma_T\sqrt{2\log(|V|-1)}$ whp by the lower bound above. Comparing to
the correct logit (upper-bounded using the SAME drift/noise machinery)
shows $M(x_{T_{\max}})<0$ whp $\Rightarrow$ $D_{\mathrm{true}}\neq a^\star$.
The residual $+1/(|V|-1)$ in R1(ii) is the favourable-noise budget where a
single incorrect direction is anomalously small.

**Constants / dimension dependence.** Same $1/\sqrt d$ projection-variance
proxy (Thm 3.4.6) and same $\sqrt{\log(|V|-1)}$ union scale as the upper
bound, so the lower and upper thresholds MATCH up to the explicit constant
$c_1$ — this matching is what makes R1 a genuine TWO-SIDED transition at
$\delta_c$.

**Why NOT the second moment (the reason this route was chosen).** The
Paley--Zygmund method (item 1) needs $\operatorname{Var} N=o((\E N)^2)$ for
$N=\sum_{a}\1\{Z_a>t\}$ at threshold $t\asymp\sigma_T\sqrt{(1-\mu_0)\log|V|}$.
The pair sum is $\sum_{a\neq a'}\operatorname{Cov}(\1\{Z_a>t\},\1\{Z_{a'}>t\})$.
For two Gaussians with correlation $\rho\le\mu_0$ at this $t$, the
exceedance ratio is $\Pr[\text{both}>t]/(\Pr\,\Pr)=|V|^{\Theta(\rho)}$
(polynomially large for CONSTANT $\mu_0$), so the pair sum is
$\gtrsim|V|^{\Theta(\mu_0)}(\E N)^2\gg(\E N)^2$ and the variance is NOT
$o((\E N)^2)$. The naive bound $\operatorname{Cov}\le\mu_0\Pr\,\Pr$ is
therefore FALSE for constant $\mu_0$; it only holds when
$\mu_0=O(1/\log|V|)$ (high-$d$). Sudakov + Borell--TIS avoid the second
moment entirely and close the failure branch **unconditionally in
$\mu_0\in[0,1)$** — at the cost of the isotropic-Gaussian noise form
`eq:noise_gaussian` (which makes the $Z_a$ exactly Gaussian, used by this
lemma only; the success branch / R2 keep general sub-Gaussian noise, see
`rem:gaussian_noise_scope`).

**Common misuses (to avoid).**
- Do NOT obtain the lower bound by "reversing" Lemma A's union bound — a
  union bound gives an UPPER bound on a max, never a lower bound. The
  lower bound REQUIRES Gaussian comparison (Sudakov) + decorrelation
  (incoherence) + a non-degeneracy input.
- Do NOT use the second-moment / Paley--Zygmund method for constant
  $\mu_0$ (see "Why NOT the second moment" above) — it is unsound there.
- Do NOT apply Sudakov minoration or Borell--TIS to a non-Gaussian
  process: both are Gaussian-only lower-bound tools. Make the $Z_a$
  Gaussian first (isotropic-Gaussian noise) — see the two digests.
- Borell--TIS Lipschitz constant of $\max_a$ is the MAX coordinate std
  $\max_a\sqrt{\operatorname{Var}Z_a}$, not $\norm{\Sigma^{1/2}}_{\mathrm{op}}$.
- Anti-concentration needs the noise NON-DEGENERATE in the incorrect
  directions — the lower isotropy bound $\sigma_{\min}>0$ in
  `eq:noise_gaussian` supplies the canonical-metric separation.

**Project .bib key.** \cite{vershynin2018} (Thm 7.4.1 Sudakov, Thm 5.2.3
Borell--TIS; also Thm 3.4.6, Ex. 2.5.10 for the scale/upper bound).
