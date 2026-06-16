# \cite{ellenberggijswijt2017} — Ellenberg–Gijswijt cap-set bound

**Paper.** "On large subsets of $\mathbb{F}_q^n$ with no three-term arithmetic
progression," Jordan S. Ellenberg and Dion Gijswijt, *Annals of Mathematics*
185 (2017), no. 1, 339–343. arXiv:1605.09223. Published version pp. 339–343.

**Exact name in PDF.** "Theorem 1" (the $q=3$ cap-set statement) and the general
"Theorem 4" for $\mathbb{F}_q^n$. The monomial-counting constant is in the proof
of Theorem 1 and the displayed optimization $\min_{0<x\le1}(1+x+x^2)x^{-2/3}$.

**Statement (faithfully paraphrased).** If $A\subseteq\mathbb{F}_3^n$ contains no
three distinct elements $x,y,z$ in arithmetic progression (equivalently, no
$x,y,z\in A$ with $x+y+z=0$ other than $x=y=z$), then $|A|\le 3M_n$ where
$M_n=\#\{a\in\{0,1,2\}^n:\sum_i a_i\le 2n/3\}$, and consequently
$|A|\le c\cdot(2.756)^n$ for an absolute constant $c$. More precisely
$M_n^{1/n}\to 3\gamma=\min_{0<x\le1}(1+x+x^2)/x^{2/3}\approx 2.7551$, i.e.
$\gamma<0.9183$.

**Hypotheses.** $A\subseteq\mathbb{F}_3^n$ is 3-AP-free (a cap set). Field is
$\mathbb{F}_3$; method generalizes to $\mathbb{F}_q$.

**Constants / dimension dependence.** $3M_n$ exact; base $3\gamma<2.7558$ from the
displayed one-variable minimization. Leading factor $3$ is subexponential.

**Project .bib key.** `\cite{ellenberggijswijt2017}`.
