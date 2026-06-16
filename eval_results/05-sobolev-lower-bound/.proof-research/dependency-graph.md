# Dependency graph — Sobolev minimax lower bound

Headline: $\inf_{\hat f}\sup_{\|f^*\|_{W^s_2}\le1}\E_{D_n}\|\hat f-f^*\|_{L^2}^2
\gtrsim n^{-2s/(2s+d)}$, fixed design, Gaussian noise $\sigma^2$.

Depth-2 tree: four leaf lemmas + the theorem. Construction parameters: grid
side $m$, $M_0 = m^d$ cells, bump amplitude $\omega m^{-s}$ per cell (cell
measure $m^{-d}$ tracked explicitly), packing radius $M\ge 2^{m^d/8}$.

## ass:setup
**Statement (1-line):** Fixed regular grid design; Gaussian noise $\sigma^2$;
unit Sobolev ball $W^s_2([0,1]^d)$, integer $s\ge1$.
**Downstream consumers:** all lemmas + thm:main.

## fac:gauss-kl
**Statement (1-line):** $\KL(P_f\|P_g)=\frac1{2\sigma^2}\sum_i(f(x_i)-g(x_i))^2$
for common Gaussian fixed design.
**Hypotheses:** ass:setup.
**Downstream consumers:** lem:kl (cite-site, KL computation).

## lem:vg  (Varshamov–Gilbert, external, cited)
**Statement (1-line):** $\exists\,M\ge2^{m^d/8}$ codewords in $\{0,1\}^{m^d}$
pairwise Hamming-$\ge m^d/8$.
**Hypotheses:** $m^d\ge8$.
**Downstream consumers:** lem:bumps (separation), thm:main (Fano denominator $\log M$).
**Form:** `\begin{lemma}[\cite{tsybakov2009introduction}]` (R5 form 2).

## lem:bumps  (bump family: feasibility + separation)
**Statement (1-line):** With amplitude $\omega\le\omega_0$, every $u_{\tau^{(k)}}$
satisfies $\|u_{\tau^{(k)}}\|_{W^s_2}\le1$ (feasible in the ball), and for
$k\ne k'$, $\|u_{\tau^{(k)}}-u_{\tau^{(k')}}\|_{L^2}^2\ge
c_g\,\frac{\omega^2}{8}\,m^{-2s}$.
**Hypotheses:** ass:setup, lem:vg, $g\in C^\infty_c((0,1)^d)$.
**Downstream consumers:** thm:main (separation $\Delta$ and feasibility).
**Form:** own lemma + immediate proof (change of variables + disjoint supports + VG Hamming bound).

## lem:kl  (pairwise KL bound)
**Statement (1-line):** $\KL(P_{u_k}\|P_{u_{k'}})\le
\frac{C_{g}\,n}{\sigma^2}\,\omega^2\,m^{-2s}$ (using grid regularity +
fac:gauss-kl).
**Hypotheses:** ass:setup, fac:gauss-kl, bump construction.
**Downstream consumers:** thm:main (Fano numerator $I(V;Y)$).
**Form:** own lemma + immediate proof.

## lem:fano  (local Fano testing inequality, external, cited)
**Statement (1-line):** $\inf_\psi\Pr[\psi\ne V]\ge1-\frac{I(V;Y)+\log2}{\log M}$,
$I(V;Y)\le\max_{k\ne k'}\KL(P_k\|P_{k'})$.
**Hypotheses:** $M\ge2$, $V$ uniform.
**Downstream consumers:** thm:main (testing-error lower bound).
**Form:** `\begin{lemma}[\cite{tsybakov2009introduction}]` (R5 form 2).

## thm:main  (minimax lower bound)
**Statement (1-line):** $\inf_{\hat f}\sup_{\|f^*\|_{W^s_2}\le1}
\E\|\hat f-f^*\|_{L^2}^2\ge c\,n^{-2s/(2s+d)}$.
**Hypotheses:** ass:setup.
**Consumes:** lem:vg, lem:bumps, lem:kl, lem:fano.
**Balance arithmetic (the load-bearing computation):**
- Separation: $\Delta^2 \asymp \omega^2 m^{-2s}$ (from lem:bumps); take $f_k$
  $2\Delta$-apart in $L^2$.
- KL diameter: $\le \frac{C_g n}{\sigma^2}\omega^2 m^{-2s}$ (lem:kl); the Fano
  numerator must be $\le \frac1{16}\log M = \frac1{16}\frac{m^d}{8}\log2
  \asymp m^d$. So require
  $\frac{n}{\sigma^2}\omega^2 m^{-2s} \lesssim m^d
  \iff \omega^2 \lesssim \frac{\sigma^2}{n} m^{2s+d}.$
- Choose $\omega^2 \asymp \frac{\sigma^2}{n} m^{2s+d}$ (largest feasible) AND
  enforce $\omega\le\omega_0$ (ball feasibility) by picking $m$ so that
  $\frac{\sigma^2}{n}m^{2s+d}\asymp\omega_0^2=$const, i.e.
  $m \asymp (n/\sigma^2)^{1/(2s+d)} \asymp n^{1/(2s+d)}.$
- Resulting rate: $\Delta^2 \asymp \omega^2 m^{-2s}
  \asymp \omega_0^2\, m^{-2s} \asymp m^{-2s} \asymp n^{-2s/(2s+d)}.$
  Fano gives testing error $\ge1/2$, so
  $\inf_{\hat f}\sup\E\|\hat f-f^*\|_{L^2}^2 \ge \frac12\Delta^2
  \asymp n^{-2s/(2s+d)}.$
**Form:** own theorem + immediate proof (assembles the four lemmas).

All lemmas have non-empty Downstream consumers. Occam-clean.
