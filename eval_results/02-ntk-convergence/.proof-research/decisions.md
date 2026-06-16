# Phase A.1a — Socratic-intake decisions (autonomous / eval mode)

These setting choices were adopted autonomously (headless eval, no interactive user)
per `references/socratic-intake.md` §6: each is the stronger/tighter proposed default.
They are recorded here rather than as inline `\todo{user-decision}` markers in the `.tex`.

## training-mode / target-norm
**Chosen:** $\ell_2$ residual loss with first-layer GD, output weights $a_r$ fixed — the standard DZPS over-parameterized NTK setting, isolating the first-layer feature dynamics that drive the spectral-gap argument and keeping the analysis tight in the operator norm. — implemented in `sections/01-preliminaries.tex` (loss Eq.~(loss); "Only the first layer is trained: the $a_r$ are fixed").
**Alternative:** joint two-layer training (both $W$ and $a$ updated).
**Reversible:** no — flipping to joint training changes the gradient, the Gram matrix definition, and the stability lemmas; it is a different proof, not a constant tweak.

## target-form (convergence rate)
**Chosen:** explicit geometric rate $\norm{y-u(k)}^2 \le (1-\eta\lzero/2)^k \norm{y-u(0)}^2$ — strictly stronger than a bare limit: it pins the per-step contraction factor and yields the explicit iteration complexity $k = O((n^2/\lzero^2)\log(n/\delta\varepsilon))$. — implemented in `sections/06-main-theorem.tex` Eq.~(thm-conv).
**Alternative:** asymptotic loss $\to 0$ (qualitative convergence only).
**Reversible:** yes — the asymptotic statement is an immediate corollary ($0 < 1-\eta\lzero/2 < 1 \Rightarrow$ RHS $\to 0$); downgrading drops the rate display and the complexity sentence but touches no lemma.

## regime (width)
**Chosen:** finite-width non-asymptotic, explicit $m \ge C\,n^6/(\lzero^4\delta^3)$ with conclusion holding w.p. $\ge 1-\delta$ — strictly stronger than an infinite-width kernel limit: it gives a usable, checkable width threshold at finite $m$. — implemented in `sections/06-main-theorem.tex` Eq.~(thm-conditions).
**Alternative:** asymptotic $m\to\infty$ kernel limit (qualitative NTK regime).
**Reversible:** yes — taking $m\to\infty$ recovers the kernel limit as a special case; the finite-$m$ statement subsumes it. Flipping would remove the explicit polynomial and the union-bound width-budget bookkeeping.

## constant-discipline (contraction vs width)
**Chosen:** tight contraction factor $1-\eta\lzero/2$ (pinned exactly, with $\eta=\kappa\lzero/n^2$) while the width carries `\poly`-slack ($n^6/(\lzero^4\delta^3)$) — concentrates sharpness where the headline lives (the rate the reader quotes) and declares the slack explicitly where it is harmless (a width sufficiency threshold). — implemented in `sections/06-main-theorem.tex` (rate pinned; width polynomial; `\poly`-slack noted in rem:decisions).
**Alternative:** tight width exponent (optimize the power of $n$ in $m$ at the cost of a looser/implicit rate constant).
**Reversible:** yes — the width polynomial can be sharpened independently of the rate; flipping re-optimizes the constant $C$ and exponents in Eq.~(thm-conditions) without changing Eq.~(thm-conv) or any lemma statement.
