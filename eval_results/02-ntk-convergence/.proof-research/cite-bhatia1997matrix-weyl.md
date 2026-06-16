# \cite{bhatia1997matrix} — Weyl's eigenvalue perturbation inequality

**Paper.** Rajendra Bhatia, *Matrix Analysis*, Graduate Texts in Mathematics 169, Springer,
1997.

**Exact name in book.** Corollary III.2.6 (consequence of the Weyl monotonicity / Lidskii
results in §III.2); equivalently Horn & Johnson, *Matrix Analysis* 2nd ed., Theorem 4.3.1.

**Statement (faithful).** For Hermitian $A,B\in\mathbb C^{n\times n}$ with eigenvalues sorted
decreasingly $\lambda_1\ge\cdots\ge\lambda_n$,
$\max_i|\lambda_i(A)-\lambda_i(B)|\le\|A-B\|_{\mathrm{op}}$.
In particular $\lambda_{\min}(A)\ge\lambda_{\min}(B)-\|A-B\|_{\mathrm{op}}$.

**Hypotheses.** $A,B$ Hermitian/symmetric (we apply only to symmetric PSD Gram matrices).
Eigenvalues sorted in the same order.

**Constants / dimension dependence.** None; the bound is tight and dimension-free.

**Use in this proof.** Cited as `\begin{fact}[\cite{bhatia1997matrix}]` (`fac:weyl`); invoked
in `lem:init-gram-close` (Step 4), `lem:gram-stability` (Step 5), and `lem:main` (Gram floor at
$k+1$). The `\begin{fact}[\cite{...}]` form satisfies R5 without a local proof.

**Project .bib key.** \cite{bhatia1997matrix}
