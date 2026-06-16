# Sweep re-derivation — Step 13 (concentration radius / C_beta absorption)

**Step.** Show that, after the covering union bound, the fixed-$V$
self-normalized bound upgrades to the uniform bound
$\|\sum_\tau\phi_h^\tau\varepsilon_h^\tau(V_{h+1}^k)\|_{(\Lambda_h^k)^{-1}}^2
\le C^2 d^2H^2\iota$, and that $\beta=C_\beta dH\sqrt\iota$ with $C_\beta\ge C$
dominates the resulting fluctuation $C\,dH\sqrt\iota$.

**Available hypotheses.** Fixed-$V$ bound (lem:self-normalized, Step 10):
$\le 2H^2(\tfrac d2\log\tfrac{\lambda+k}{\lambda}+\log\tfrac1{\delta'})$. Covering
$\log|\mathcal V_\epsilon|\le C_1 d^2\log(1+HdK/(\epsilon\lambda))$
(cite-jin2020provably Lemma D.6). $\iota=\log(2dT/\delta)$.

**Independent derivation (rate level).**
1. Set $\delta'=\delta/(2HK|\mathcal V_\epsilon|)$. Then
   $\log(1/\delta')=\log(2HK/\delta)+\log|\mathcal V_\epsilon|
   \le \iota + C_1 d^2\log(1+HdK/(\epsilon\lambda))$.
2. With $\epsilon=dH/K$ and $\lambda=1$, $\log(1+HdK/(\epsilon\lambda))
   =\log(1+K^2)\le 2\log(2dT/\delta)=2\iota$ (loosely; the polynomial argument
   is logarithmic in $T$ and absorbed into $\iota$). So $\log(1/\delta')
   \le \iota+2C_1 d^2\iota\le C_2 d^2\iota$ for $C_2:=1+2C_1$.
3. Hence the bound is $2H^2(\tfrac d2\iota+C_2 d^2\iota)\le 2H^2(C_2+1)d^2\iota
   =:C^2 d^2H^2\iota$. The $d^2$ term dominates the $d$ term.
4. Taking square roots: radius $C\,dH\sqrt\iota$. Choosing $C_\beta\ge C$ makes
   $\beta=C_\beta dH\sqrt\iota$ at least the fluctuation radius.

**Verdict.** matches at the rate level (exponents $dH\sqrt\iota$ exact); the
exact numeric constant $C_\beta$ is NOT pinned here — jin2020provably fixes it
via $c'\sqrt{\log2+\log(c_\beta+1)}\le c_\beta\sqrt{\log2}$ (their Eq. 14), an
implicit self-consistent choice. We keep $C_\beta$ symbolic and route to human
verification: `\todo{verify: C_beta}` at sections/02-concentration.tex:113.

**Why this stays 🔴.** Only the numeric constant is unverified; this is an
honest "constant not pinned" flag, not a structural gap. The discretization
error step ($\sup_V\min_{\bar V}\|V-\bar V\|_\infty\le\epsilon$ contributes
$\le 2\epsilon\sqrt K\cdot\sqrt K=2dH$ to the sum, lower order) is standard but
the bookkeeping of $\epsilon$ vs the final constant is the kind of place AI
memory drifts — hence the conservative 🔴.
