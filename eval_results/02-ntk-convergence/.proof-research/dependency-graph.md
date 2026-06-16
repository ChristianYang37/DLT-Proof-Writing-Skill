# Dependency graph — NTK two-layer convergence (Du–Zhai–Poczos–Singh skeleton)

Proof type: **Over-parameterized NN convergence**. Pattern (pattern-menu.md):
three-lemma NTK skeleton + successful-event conditioning + induction on iterates,
closed by a fixed-point / contradiction argument.

Topological order (leaves first): `lem:init-gram-close` → `lem:gram-stability` →
`lem:contraction` → `lem:main` (induction) → `thm:main`.

## fac:weyl
**Statement (1-line):** For symmetric $A,B$, $|\lambda_i(A)-\lambda_i(B)|\le\|A-B\|_2$.
**Hypotheses:** $A,B$ symmetric.
**Downstream consumers:** lem:init-gram-close (Frobenius→operator→Weyl chain),
lem:gram-stability (perturbation→eigenvalue).

## fac:hoeffding
**Statement (1-line):** Bounded-RV Hoeffding tail $\Pr[|S-\E S|\ge t]\le 2e^{-2t^2/\sum(\beta-\alpha)^2}$.
**Hypotheses:** independence, a.s. boundedness.
**Downstream consumers:** lem:init-gram-close (entrywise Gram concentration).

## lem:init-gram-close
**Statement (1-line):** W.p. $\ge1-\delta$, if $m\ge C n^2\lambda_0^{-2}\log(n^2/\delta)$ then
$\|H(0)-H^\infty\|_2\le\lambda_0/4$ and $\lambda_{\min}(H(0))\ge\tfrac34\lambda_0$.
**Hypotheses:** ass:lambda0 (spectral gap), data normalization, init distribution.
**Downstream consumers:** lem:main (base case $\lambda_{\min}(H(0))\ge\tfrac34\lambda_0$),
thm:main (probability budget event $\mathcal E_1$).

## lem:gram-stability
**Statement (1-line):** If $\|w_r-w_r(0)\|\le R$ for all $r$ with $R=c\delta\lambda_0/n^2$, then
w.p. $\ge1-\delta$, $\|H(W)-H(0)\|_2\le\lambda_0/4$, hence $\lambda_{\min}(H(W))\ge\lambda_0/2$.
**Hypotheses:** ass:lambda0, init distribution (for anti-concentration), perturbation radius $R$.
**Downstream consumers:** lem:contraction (needs $\lambda_{\min}(H(k))\ge\lambda_0/2$),
lem:main (maintains Gram lower bound under the inductive stay-in-ball hypothesis).

## lem:contraction
**Statement (1-line):** On the event that $\lambda_{\min}(H(k))\ge\lambda_0/2$ and
$\eta\le\lambda_0/(2n^2)$, one GD step gives
$\|y-u(k+1)\|_2^2\le(1-\eta\lambda_0/2)\|y-u(k)\|_2^2$, and
$\|w_r(k+1)-w_r(k)\|\le\eta\sqrt{n/m}\,\|y-u(k)\|_2$.
**Hypotheses:** Gram lower bound at step $k$, step-size cap, GD update rule.
**Downstream consumers:** lem:main (inductive step: contraction + movement accumulation).

## lem:main
**Statement (1-line):** Induction/fixed-point lemma: if
$m\ge\poly(n,1/\lambda_0,1/\delta)$ and $\eta=O(\lambda_0/n^2)$, then w.p. $\ge1-\delta$,
for ALL $k\ge0$: (i) $\lambda_{\min}(H(k))\ge\lambda_0/2$, (ii)
$\|y-u(k)\|_2^2\le(1-\eta\lambda_0/2)^k\|y-u(0)\|_2^2$, (iii) $\|w_r(k)-w_r(0)\|\le R$.
**Hypotheses:** lem:init-gram-close, lem:gram-stability, lem:contraction; ass:lambda0.
**Downstream consumers:** thm:main (the headline is a 5–10 line wrapper of this lemma).

## thm:main
**Statement (1-line):** Two-tier theorem: w.p. $\ge1-\delta$, GD with $\eta=O(\lambda_0/n^2)$
and $m\gtrsim\poly(n,1/\lambda_0,1/\delta)$ attains
$\|y-u(k)\|_2^2\le(1-\eta\lambda_0/2)^k\|y-u(0)\|_2^2\to0$ (linear convergence to zero loss).
**Hypotheses:** ass:lambda0 (single spectral assumption), data + init setup.
**Downstream consumers:** (headline — terminal node; no consumers, allowed for the theorem).

## Occam check
Every lemma has ≥1 downstream consumer. No orphan lemmas. The two facts
(`fac:weyl`, `fac:hoeffding`) are external, cited, and each consumed ≥1×.
Tree depth: 3 levels (facts → 3 lemmas → main lemma → theorem). Shallowest that fits the
three-lemma skeleton requested by the prompt.
