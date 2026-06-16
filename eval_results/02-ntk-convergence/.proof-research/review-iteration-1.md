# Phase D — Review iteration 1

Proof under review: **Linear convergence of gradient descent for over-parameterized two-layer
ReLU networks** (NTK analysis), `eval_results/02-ntk-convergence/`, headline
`\Cref{thm:main}` in `sections/06-main-theorem.tex`.

Five INDEPENDENT reviewers (R1 line-by-line rigor, R2 assumptions/generality, R3 ML-significance,
R4 math-taste, R5 derivation-integrity). Inputs: `sections/*.tex`, `.output/main.pdf`,
`.output/main.log`, `.proof-research/confidence-trace.md`.

## Scores

| Reviewer | Score | Blocking? |
|---|---|---|
| R1 line-by-line | 2 | no |
| R2 assumptions/generality | 5 | no |
| R3 ML-significance | 3 | yes |
| R4 math-taste | 8 | no |
| R5 derivation-integrity | 3 | yes |
| **mean** | **4.20** | — |

Orchestrator decision: mean 4.20 ≤ 8 (and unresolved REAL-blocking criticals present) → **ITERATE**.

---

## Merged + deduped weaknesses

Dedupe rule: same `file:line ± 3` OR paraphrase of the Claim = one merged weakness; keep max
severity; record how many of 5 raised it.

### Weakness #1 (severity: critical, raised by 3/5)
**Claim:** The first inequality of the flip-remainder bound Eq.~(remainder) carries the factor
$\abs{\mathcal S_k}^{1/2}$, but the stated prose mechanism (each flipping neuron perturbs each
coordinate of $u$ by at most $\tfrac{1}{\sqrt m}R_{\mathrm{step}}$), aggregated over
$\abs{\mathcal S_k}$ flips by the triangle inequality, yields exponent $1$, not $1/2$. No
Cauchy–Schwarz / sign-cancellation / Khintchine rule licenses $1/2$.
(R1 critical, R3 major, R5 major; `05-lemma-main-induction.tex:112-117`.)
**Verdict:** REAL-blocking.
**Rebuttal / fix-plan:** Confirmed by re-derivation: honest $\ell_1$-over-neurons +
$\ell_2$-over-$n$-coords gives $\norm{\varepsilon(k)}\le\frac{\eta n}{m}\abs{\mathcal S_k}\norm{y-u(k)}$
(exponent 1). FIXED: rewrote Eq.~(remainder) with exponent 1; the bound still closes (see #2/#3).

### Weakness #2 (severity: critical, raised by 5/5)
**Claim:** Eq.~(remainder) substitutes the expectation $\E\abs{\mathcal S_k}\le2nmR$ for the
realized random count $\abs{\mathcal S_k}$ inside a per-step deterministic recursion declared to
hold on a conditioning event, with no high-probability bound on $\abs{\mathcal S_k}$ and no union
over the (infinitely many) iterations $k$; the budget covers only the init events.
(R1 major, R2 major, R3 critical, R5 critical; `05-lemma-main-induction.tex:118`.)
**Verdict:** REAL-blocking.
**Rebuttal / fix-plan:** Confirmed. FIXED by the key observation that every flip satisfies the
anchor Eq.~(flip-anchor), so $\mathcal S_k\subseteq\mathcal N:=\{(r,i):\abs{w_r(0)^\top x_i}\le2R\}$
for ALL $k$, where $\mathcal N$ is a function of $W(0)$ ALONE. One Markov bound on $\abs{\mathcal N}$
(new event $\mathcal E_4$, Eq.~flip-event-budget, at level $\delta/4$) covers every $k$
simultaneously — no per-$k$ union needed. $\mathcal E_4$ added to the lemma conditions and the
theorem's union budget (now $4\times\delta/4=\delta$).

### Weakness #3 (severity: critical, raised by 5/5)
**Claim:** The aggregation constant $1/8$ in Eq.~(remainder) is, by the author's own admission,
carried from memory (DZPS Lemma 3.3), not re-derived; it carries a live `\todo{verify}` marker, so
numerical closure of the contraction rests on an unverified constant.
(R1 major, R2 minor, R3 critical, R5 critical; `05-lemma-main-induction.tex:122`.)
**Verdict:** REAL-blocking.
**Rebuttal / fix-plan:** Confirmed. FIXED: re-derived explicitly. Substituting $R=c\delta\lzero/n^2$
and $\abs{\mathcal S_k}\le8nmR/\delta$ gives prefactor $8c\lzero\le\lzero/8$ for $c\le1/64$, with
$n$, $m$, $\delta$ all cancelling (the bound is width-free, driven by $c$). `\todo` deleted;
trace Step 27 re-tagged 🟢.

### Weakness #4 (severity: major, raised by 1/5)
**Claim:** The prose justification "$m\ge Cn^6/(\lzero^4\delta^3)$ drives the remainder prefactor
below $\eta\lzero/8$" is a non-sequitur: substituting $\E\abs{\mathcal S_k}=2nmR$ into the
displayed line needs only $m=O(n/\lzero)$, so the stated justification does not match its display.
(R5 major; `05-lemma-main-induction.tex:119`.)
**Verdict:** REAL-nonblocking (symptom of #1–#3).
**Rebuttal / fix-plan:** Correct — the width was never what closed this step. RESOLVED by the #1–#3
rewrite: the new derivation closes via the constant $c$ alone and explicitly states "$n$, $m$ and
$\delta$ all cancelling ... driven by the constant $c$ alone, not the width." No separate patch.

### Weakness #5 (severity: major, raised by 1/5)
**Claim:** `lem:gram-stability` is used as a uniform-over-$W$ event ($\mathcal E_2$ quantifies
"whenever $\norm{w_r-w_r(0)}\le R$"), but its Step-4 Markov is applied to the $W$-dependent
$\opnorm{H(W)-H(0)}$ for a single fixed $W$, establishing only the per-fixed-$W$ statement; the
data-dependent $W(k+1)$ downstream needs the uniform event. The $W$-independent dominating bound is
derived (Eq.~entry-diff) then discarded.
(R2 major; `03-lemma-gram-stability.tex:80`.)
**Verdict:** REAL-blocking (low-cost reroute).
**Rebuttal / fix-plan:** Confirmed: Eq.~(entry-diff) RHS depends on $W(0)$ only and dominates
$\opnorm{H(W)-H(0)}$ for all $W$ in the ball, but the written Markov acted on the $W$-dependent
quantity. FIXED: introduced the $W$-independent random variable $D$ (Eq.~dom-quantity), proved
$\sup_W\opnorm{H(W)-H(0)}\le D$ (Eq.~dom-sup), and applied Markov to $D$; the event $\{D\le\lzero/4\}$
(a function of $W(0)$ alone) now holds uniformly over all admissible $W$ including the iterates.

### Weakness #6 (severity: minor, raised by 1/5)
**Claim:** The geometric-series transition writes the intermediate $\tfrac{2}{1-\sqrt{1-\eta\lzero/2}}$
and cites $1-\sqrt{1-x}\ge x/2$, which together give $8/(\eta\lzero)$, not the written $4/(\eta\lzero)$.
The endpoint $4/(\eta\lzero)$ is correct via the tight identity $\sum=\frac{1}{1-\sqrt{1-X}}\le 2/X$,
but the written chain (factor-2 numerator + cited bound) does not produce it.
(R1 minor; `05-lemma-main-induction.tex:63-66`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed (verified numerically). FIXED: replaced the spurious-factor-2
intermediate with the exact geometric-series identity $\sum_{s\ge0}(1-X)^{s/2}=\frac{1}{1-\sqrt{1-X}}\le\frac{2}{X}=\frac{4}{\eta\lzero}$,
and spelled the chain out so the endpoint follows from the cited bound. Endpoint unchanged.

### Weakness #7 (severity: minor, raised by 1/5)
**Claim:** The initial-residual constant is inconsistent: $\mathcal E_3$ uses $\sqrt{6n/\delta}$ but
`lem:init-residual` and the stay-in-ball use $\sqrt{2n/\delta}$; the $\delta/3$ rescaling
reconciling them is never written.
(R3 minor; `06-main-theorem.tex:42`.)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed. FIXED in the course of the #2 budget change: with the budget now
$4\times\delta/4$, $\mathcal E_3$ is `lem:init-residual` at level $\delta/4$, giving
$\sqrt{2n/(\delta/4)}=\sqrt{8n/\delta}$; updated $\mathcal E_3$ and the iteration-count display to
$8n/\delta$, and the theorem now explicitly states the $\delta/4$ rescaling is absorbed into $C$.

### Weakness #8 (severity: minor, raised by 1/5)
**Claim:** The confidence trace records a different stay-in-ball width exponent than the proof:
Step 26 says $m\ge64n^6/(c^2\delta^2\lzero^4)$ ($\delta^2$) whereas `.tex:69` derives
$m\ge32n^6/(c^2\delta^3\lzero^4)$ ($\delta^3$); the $\delta^3$ value is internally consistent
(matches eq:width-main), so the trace entry is stale.
(R2 minor; `.proof-research/confidence-trace.md:242`.)
**Verdict:** REAL-nonblocking (trace-only; the .tex is correct).
**Rebuttal / fix-plan:** Confirmed: the trace used the no-$\delta$ residual $2\sqrt n$ while the .tex
uses $\sqrt{2n/\delta}$. FIXED: synced trace Step 26 to $\sqrt{2n/\delta}$ /
$m\ge32n^6/(c^2\delta^3\lzero^4)$ ($\delta^3$). No proof change.

---

## Accept decision

Mean **4.20** ≤ 8 (strict bar), and the panel raised REAL-blocking criticals (#1, #2, #3).
Per Component 4 gate 1, the accept gate is **NOT** met → **ITERATE**.

All REAL-blocking criticals (#1, #2, #3) and the REAL-blocking major (#5) are fixed this iteration
within the minimum-change principle (no headline statement changed; the rewrite is local to the
remainder block of `05`, the union budget of `06`, and Steps 3–4 of `03`). REAL-nonblocking items
#4, #6, #7, #8 fixed within their line budgets. No PHANTOM or INTENTIONAL verdicts this iteration.
Post-fix gates: `lint.py` 0 errors / 0 warnings (incl. R19); `latexmk-wrapper.py` compile_ok=true,
no overfull / undef-ref / undef-cite / mult-label violations; `pdf/main.pdf` refreshed.

No headline theorem/lemma statement was changed; no statement-change escalation triggered.
