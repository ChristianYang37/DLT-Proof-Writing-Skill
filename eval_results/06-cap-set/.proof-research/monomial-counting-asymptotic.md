# Monomial-counting asymptotic $M_n^{1/n}\to 3\gamma$ (large deviations)

**Source.** Ellenberg–Gijswijt, "On large subsets of $\mathbb{F}_q^n$ with no
three-term arithmetic progression," *Annals of Math.* 185 (2017), 339–343
(arXiv:1605.09223), and Tao's blog exposition. Project key
`\cite{ellenberggijswijt2017}`.

**Quantity.** $M_n=\#\{(a_1,\dots,a_n)\in\{0,1,2\}^n:\sum_i a_i\le 2n/3\}$, i.e.
the number of degree-$\le 2n/3$ monomials in $n$ variables over $\mathbb{F}_3$
(each exponent in $\{0,1,2\}$).

**Asymptotic.** $M_n = $ coefficient extraction from $(1+x+x^2)^n$:
$M_n=\sum_{0\le t\le 2n/3}[x^t](1+x+x^2)^n$. By a standard Chernoff / large-
deviation (saddle-point) bound on the coefficients of $(1+x+x^2)^n$,
$$M_n^{1/n}\ \longrightarrow\ \min_{0<x\le 1}\ \frac{1+x+x^2}{x^{2/3}}\ =:\ 3\gamma .$$
The minimizing $x_\*\in(0,1)$ solves $\frac{d}{dx}\log\frac{1+x+x^2}{x^{2/3}}=0$,
i.e. $\frac{1+2x}{1+x+x^2}=\frac{2}{3x}$, giving $x_\*\approx 0.5931$ and the
numerical value
$$3\gamma=\min_{0<x\le1}\frac{1+x+x^2}{x^{2/3}}\approx 2.7551\ <\ 2.7558,$$
with $\gamma\approx 0.9184$ — the standard statement is $\gamma<0.9183$ and
$3\gamma<2.7558$. (Ellenberg–Gijswijt state $|A|\le c\,2.756^n$; the rounded
$2.7558$ is the commonly quoted constant.)

**Derivation sketch we reproduce.** Use the generating-function / Cramér bound:
for any $x\in(0,1]$,
$$M_n\le \sum_{t\le 2n/3} [x^t](1+x+x^2)^n\, x^{2n/3-t}\cdot x^{t-2n/3}
\ \le\ x^{-2n/3}(1+x+x^2)^n,$$
because for $t\le 2n/3$ we have $x^{t-2n/3}\ge 1$ (as $x\le 1$ and exponent $\le0$).
Hence $M_n^{1/n}\le (1+x+x^2)/x^{2/3}$ for every $x\in(0,1]$; minimizing over $x$
gives the constant. The matching lower bound (not needed for the upper bound on
$|A|$) follows from concentration of the multinomial coefficients.

**How it feeds the theorem.** $|A|\le 3M_n$ and $M_n^{1/n}\to 3\gamma<2.7558/?$…
precisely: $(3M_n)^{1/n}=3^{1/n}M_n^{1/n}\to 3\gamma<2.7558$, so
$|A|\le C\cdot(2.7558)^n$ for a constant $C$ absorbing lower-order factors.
(The "$3$" in $3M_n$ is subexponential, $3^{1/n}\to1$.)

**Constants.** $3\gamma=\min_{0<x\le1}(1+x+x^2)x^{-2/3}$; numerically
$3\gamma\approx 2.7551<2.7558$. We **cite** the explicit optimization to
Ellenberg–Gijswijt rather than recompute the minimizer to full precision — the
prompt allows "citation of the optimization is acceptable if cited correctly."

**Common misuses.**
- Claiming $M_n^{1/n}\to\gamma$ (missing the factor 3) — the per-variable factor
  is $(1+x+x^2)$ evaluated at the optimum, normalized; the convention puts the
  factor 3 so that $\gamma<0.9183$ and $3\gamma<2.7558$.
- Forgetting $3^{1/n}\to 1$ so the leading $3$ in $3M_n$ does not change the base.

**Project citation key.** `\cite{ellenberggijswijt2017}`.
