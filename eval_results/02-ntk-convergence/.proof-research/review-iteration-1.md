# Phase D review — iteration 1

## Reviewer output

### Summary

The paper proves linear convergence of gradient descent on the squared loss for a two-layer ReLU network in the over-parameterized regime, following the three-lemma NTK skeleton of Du-Zhai-Poczos-Singh (2019). The contribution is a clean re-derivation that (i) pins down a single spectral assumption $\lambda_0 \defeq \lambda_{\min}(\Hb^\infty) > 0$, (ii) decomposes the argument into initial Gram concentration (\Cref{lem:init_gram}), Gram stability under perturbations (\Cref{lem:perturbation}), and linear convergence in a stay-in-ball regime (\Cref{lem:linear_conv}), and (iii) closes via a fixed-point / contradiction argument that maintains the spectral lower bound throughout training. The width hypothesis is $m \gtrsim n^6 / (\lambda_0^4 \delta^3)$ and the step size is $\eta = O(\lambda_0 / n^2)$, matching the headline result of the cited prior work.

### Strengths

- **Clean decomposition.** The three structural lemmas factor the proof shallowly: concentration at init, deterministic stability under small perturbations, and a deterministic inductive contraction. Each lemma is self-contained and individually verifiable.
- **Explicit probability budget.** Three failure events $\mathcal E_1, \mathcal E_2, \mathcal E_3$ each at level $\delta/3$, union-bounded to total $\delta$. The accounting is visible in \Cref{sec:proof_main} Step 1.
- **Width hypothesis traceable.** \Cref{rem:width_check} explicitly reconciles the headline $n^6$ width with the subsidiary $n^2$ requirements from \Cref{lem:init_gram,lem:perturbation}, identifying the third constraint (radius $R \le c\lambda_0/n^2$) as the binding one.
- **Uniform perturbation phrasing.** \Cref{lem:perturbation} is stated uniformly over the $R$-ball (\Cref{rem:perturbation_uniformity}), which is what enables the contradiction closure without a sequence-of-iterates union bound.

### Weaknesses

**W1.** [major / REAL-blocking?] The bound $|T_i(s)| \le |S_i| \le 2mR$ in \Cref{sec:proof_linear_conv} (line 47 of sections/05-...tex) is flagged with a `\todo{verify}` and as written conflates two different sets. $T_i(s)$ is the *single-step* flip set; $S_i$ (from \Cref{lem:perturbation}) is the set of neurons whose pattern could flip *for any* $\Wb$ within $R$ of $\Wb(0)$. The inclusion $T_i(s) \subseteq S_i$ holds *if* $\Wb(s)$ and $\Wb(s+1)$ are both within $R$ of $\Wb(0)$, which is exactly the inductive invariant — so the logic is right, but the .tex prose suggests the inclusion is automatic rather than inductively maintained. The argument should explicitly invoke the inductive hypothesis $(\star_s)$ (or some equivalent) at this point. Severity: major. Evidence: `sections/05-proof-of-lemma-linear-conv.tex:47` "$|T_i(s)| \le |S_i| \le 2 m R$".

**W2.** [major / REAL-blocking?] The sub-Gaussian proxy constant in the proof of \Cref{lem:init_residual} carries a `\todo{verify}` at line 59 of sections/03-...tex. The claim $\Pr[|\ub_i(0)| \ge t] \le 2\exp(-c_1 t^2)$ is correct in essence (since $\ub_i(0)$ is a sum-of-Rademacher times bounded-by-$|g|$ terms, and the $1/\sqrt m$ scaling balances variance), but the proof currently invokes a "standard sub-Gaussian tail bound" without specifying which one. The cleanest path is: conditionally on $\Wb(0)$, $\ub_i(0) = m^{-1/2} \sum_r a_r \sigma(\wb_r(0)^\top \xb_i)$ is a Rademacher sum of bounded vectors, so Hoeffding (\Cref{fac:hoeffding}) directly with $b = |\sigma(\wb_r(0)^\top \xb_i)|$ gives a conditional tail bound; one then bounds $\sum_r \sigma(\cdot)^2$ via Gaussian concentration. The current pass via "marginalizing" is too compressed. Severity: major. Evidence: `sections/03-proof-of-lemma-init-gram.tex:59`.

**W3.** [minor / REAL-nonblocking] The claim $\opnorm{\Hb_s} \le n$ in \Cref{sec:proof_linear_conv} Step 3 (line 62) is loose. The actual bound is $\opnorm{\Hb_s} \le n$ (since $|\Hb_s {}_{ij}| \le 1$), but the *tight* bound is $\opnorm{\Hb_s} \le \opnorm{\Hb^\infty} + \lambda_0/2 \le n$ (since the diagonal entries of $\Hb^\infty$ are exactly $1/2$ so $\opnorm{\Hb^\infty} \le n/2$). The loose bound is sufficient for the absorption $\eta n \le 1$, but a tighter constant would let $C_2$ be more permissive. Not blocking. Severity: minor.

**W4.** [minor / REAL-nonblocking] In \Cref{lem:perturbation}'s proof Step 2 (line at sections/04, "stronger concentration"), the deviation argument applies Hoeffding to centered Bernoullis with $\Pr[A_{i,r}] \le R$, but the centering subtracts $\Pr[A_{i,r}]$ which is at most $R$. The chain "$\Pr[\sum_r \one[A_{i,r}]/m \ge 2R] = \Pr[\sum_r \one[A_{i,r}]/m - \Pr[A_{i,r}] \ge R]$" implicitly uses $\Pr[A_{i,r}] \le R$. This is correct but worth a one-line justification rather than an implicit step. Severity: minor.

**W5.** [minor / REAL-nonblocking] The first-order Taylor expansion in \Cref{sec:proof_linear_conv} Step 1 invokes a "first-order expansion" of a piecewise-linear function (ReLU). For ReLU, this is exact between activations of the same sign and the remainder vanishes there; the remainder $e_i(s)$ captures only the sign-flip contributions. The .tex prose calls this a "first-order expansion" which is technically correct only because the second derivative of ReLU is zero except at the kink. Worth one sentence clarifying that the "remainder" is a sign-flip-only term, not a quadratic-error term. Severity: minor.

### Questions for the author

- Q1. The argument freezes the second layer $\ab$ at initialization. The DZPS19 paper does the same, but downstream improvements (Arora-Du-Hu-Li-Wang, Allen-Zhu-Li-Song) train both layers. Is this a deliberate scope decision, and would a remark indicate so?
- Q2. The width polynomial $n^6 / (\lambda_0^4 \delta^3)$ is presented as matching DZPS19 but the exact polynomial in DZPS19 varies across arXiv versions. Worth a one-line note in \Cref{rem:width_check} explicitly disclaiming that $C_1$ absorbs the version dependence.

### Verdict

**accept-with-minor-revisions.** The proof skeleton is sound and individually each lemma is correct. The two `\todo{verify}` markers (W1, W2) point to real exposition gaps that should be tightened to make the chain fully airtight; the other three weaknesses are minor stylistic improvements.

---

## Author verification + decisions

### Weakness #W1 (severity: major)
**Claim:** $T_i(s) \subseteq S_i$ requires the inductive invariant; .tex prose hides this.
**Verdict:** REAL-blocking
**Rebuttal / fix-plan:** Fix. The inductive invariant $(\star_s)$ from \Cref{sec:proof_main} establishes that $\wb_r(s)$ and $\wb_r(s+1)$ are both within $R$ of $\wb_r(0)$ on the event $(\star_s) \cap \mathcal E_2$. Once this is in scope, $T_i(s) \subseteq S_i$ follows because a flip between $\wb_r(s)$ and $\wb_r(s+1)$ — both within $R$ of $\wb_r(0)$ — implies a flip somewhere in the $R$-ball, i.e., $A_{i,r}(R)$ from Eq.~\eqref{eq:flip_event}. However, \Cref{lem:linear_conv} is *stated* as a deterministic implication on an event that already includes the perturbation bound; the current proof of the lemma should not bake in $(\star_s)$ but rather assume that the iterates are in the ball as an additional hypothesis OR route the flip-count differently. The cleanest minimum-change fix: add an explicit hypothesis to \Cref{lem:linear_conv} that on the event in question, the perturbation bound holds for all $s' \le s$. **Fix cost:** ~4 lines (one line in the lemma statement, one line in the proof).

### Weakness #W2 (severity: major)
**Claim:** Sub-Gaussian tail derivation in \Cref{lem:init_residual} is too compressed; the proxy constant needs to be derived explicitly.
**Verdict:** REAL-nonblocking — the tail bound is correct, just under-justified.
**Rebuttal / fix-plan:** Fix. The cleanest path is: condition on $\Wb(0)$, apply Hoeffding (\Cref{fac:hoeffding}) to $\ub_i(0) = m^{-1/2} \sum_r a_r \sigma(\wb_r(0)^\top \xb_i)$ with $b_r = |\sigma(\wb_r(0)^\top \xb_i)| \le |\wb_r(0)^\top \xb_i|$, then take expectation over $\wb_r(0)$ to bound $\sum_r b_r^2$. **Fix cost:** ~8 lines.

### Weakness #W3 (severity: minor)
**Claim:** $\opnorm{\Hb_s} \le n$ is loose; tighter $\opnorm{\Hb_s} \le n/2 + \lambda_0/2$.
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Do not fix. The looser bound $\opnorm{\Hb_s} \le n$ is sufficient for the absorption $\eta n \le 1$ (which is what we need for $\opnorm{\I - \eta\Hb_s} \le 1 - \eta\lambda_0/2$). Tightening would not change the headline rate; it would only relax the constant $C_2$. Not worth the patch.

### Weakness #W4 (severity: minor)
**Claim:** Centering step in \Cref{lem:perturbation} Step 2 implicit.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Fix. Add one line ("using $\Pr[A_{i,r}(R)] \le R$ from Eq.~\eqref{eq:flip_prob} to absorb the centering"). **Fix cost:** 1 line.

### Weakness #W5 (severity: minor)
**Claim:** "First-order expansion" of ReLU under-explained.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Fix. Add one sentence noting that for piecewise-linear $\sigma$ the "remainder" $e_i(s)$ captures sign-flip contributions only, not a quadratic-order Taylor error. **Fix cost:** 1 line.

---

## Iteration outcome

Applying fixes for W1, W2, W4, W5; rebutting W3.
