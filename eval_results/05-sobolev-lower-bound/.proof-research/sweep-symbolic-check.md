# Phase C.5 symbolic re-derivation report

Independent symbolic check (sympy) of the load-bearing scaling and balance
arithmetic of the proof. Run during the confidence sweep; verdict for each:
**matches**, except two leading-constant slips that were **caught and fixed**
in the source (rate exponent unaffected in both).

## Change-of-variables scalings (lem:bumps, lem:kl)

- Per-bump order-$r$ derivative integral:
  $\int|\partial^\alpha(\tfrac{\omega}{m^s}g(m(x-x^{(j)})))|^2
   = \omega^2\,m^{-2(s-r)-d}\,\|\partial^\alpha g\|_{L^2}^2$.
  **matches** the proof (Step 1, sections/03). At $r=s$: $\omega^2 m^{-d}$.
- Cell $L^2$ mass ($r=0$): $c_g\,\omega^2\,m^{-2s-d}$. **matches** Eq.~(cell-mass).
- Pairwise $L^2$ separation: $\rho_H\cdot c_g\omega^2 m^{-2s-d}\ge
  \tfrac{m^d}{8}c_g\omega^2 m^{-2s-d}=\tfrac{c_g}{8}\omega^2 m^{-2s}$.
  **matches** Eq.~(sep).
- KL design sum: $\rho_H\cdot\tfrac{n}{M_0}\tfrac{\omega^2}{m^{2s}}G_\infty
  \le M_0\cdot\tfrac{n}{M_0}\tfrac{\omega^2}{m^{2s}}G_\infty
  = G_\infty\tfrac{n\omega^2}{m^{2s}}$. **matches** Eq.~(klbound).

## Balance arithmetic (thm:main)

- Ceiling two-sided bound $Bn^{1/(2s+d)}\le m\le 2Bn^{1/(2s+d)}$: **matches**
  (valid once $Bn^{1/(2s+d)}\ge1$).
- KL after $B$-substitution: with $B^{2s+d}=64G_\infty\omega_0^2/(\sigma^2\log2)$,
  $\tfrac{G_\infty\omega_0^2}{2\sigma^2}B^{-(2s+d)}m^d=\tfrac{\log2}{128}m^d$.
  **matches**.
- $\tfrac{\log2}{128}m^d\le\tfrac14\log M$: holds since
  $\tfrac14\log M\ge\tfrac14\cdot\tfrac{m^d}{8}\log2=\tfrac{\log2}{32}m^d
  \ge\tfrac{\log2}{128}m^d$. **caught**: the proof's first draft asserted the
  intermediate as an *equality* $\tfrac{\log2}{128}m^d=\tfrac14\cdot\tfrac{m^d}{8}\log2$;
  corrected to the inequality $\tfrac{1}{128}\le\tfrac14\cdot\tfrac18=\tfrac1{32}$.
- Fano: $1-\tfrac{\tfrac14\log M+\log2}{\log M}\ge1-\tfrac14-\tfrac{\log2}{\log M}\ge\tfrac12$
  for $\log M\ge4\log2$. **matches**.

## Leading-constant slip — caught and fixed

From $(2\Delta)^2=\tfrac{c_g\omega_0^2}{8\,m^{2s}}$ we get $4\Delta^2=\tfrac{c_g\omega_0^2}{8\,m^{2s}}$,
hence $\Delta^2=\tfrac{c_g\omega_0^2}{32\,m^{2s}}$ and $\tfrac{\Delta^2}{2}=\tfrac{c_g\omega_0^2}{64\,m^{2s}}$.
The first draft wrote $\Delta^2=\tfrac{c_g\omega_0^2}{128\,m^{2s}}$ and the rate
constant $\tfrac{c_g\omega_0^2}{256(2B)^{2s}}$ (both a factor $4$ too small).
**Fixed** to $32$, $64$, and $\tfrac{c_g\omega_0^2}{64(2B)^{2s}}$ respectively.
The minimax **rate exponent $-2s/(2s+d)$ is unchanged** by this; only the
absolute constant $c$ moves.

**Overall verdict: matches** (after the two cosmetic-constant fixes above);
the rate $n^{-2s/(2s+d)}$ is confirmed exact.
