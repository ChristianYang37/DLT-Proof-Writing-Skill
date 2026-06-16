# Review iteration 2 — Sobolev minimax lower bound

Proof under review: `\Cref{thm:main}` (Sobolev minimax lower bound) and supporting
lemmas, `eval_results/05-sobolev-lower-bound/`.

## Reviewer scores

| Reviewer | Lens | Score | Blocking? |
|---|---|---|---|
| R1 | Correctness: line-by-line rigor | 9 | no |
| R2 | Correctness: assumptions / generality | 8 | no |
| R3 | Correctness: ML-significance | 7 | no |
| R4 | Math taste | 9 | no |
| R5 | Derivation integrity | 9 | no |
| **mean** | | **8.40** | |

(Score history: iteration 1 mean = 8.00; iteration 2 mean = 8.40.)

**Accept decision:** mean = 8.40 is strictly `> 8` AND no unresolved REAL-blocking
critical exists → **ACCEPT**. Per review-loop Component 4 gate 1, the loop
terminates in success. The proof is NOT modified this iteration (record only).

## Merged + verified weaknesses

Six raw weakness items across the five reviews merged into four distinct
weaknesses (two pairs are file:line / paraphrase duplicates). For each: how many
of 5 raised it, the verdict, and a one-line rebuttal/fix-plan. Evidence was
confirmed verbatim at each cited `file:line`.

### Weakness #1 (severity: major, raised by 3/5)
**Claim:** The headline "for all $n$ large enough" is delivered only along the
coupled subsequence where $m=\lceil B n^{1/(2s+d)}\rceil$ divides $n^{1/d}$; the
non-emptiness/density of this subsequence is never argued, so the headline
overclaims the regime relative to what is established.
(`sections/06-main-theorem.tex:38`, headline `:11`; R2 minor, R3 major, R8-style
note. Highest severity retained = major.)
**Verdict:** REAL-nonblocking — STATEMENT-CHANGE / already disclosed.
**Rebuttal / fix-plan:** Identical to iteration-1 Weakness #1. The only honest fix
restricts the theorem **headline** to the regular-grid subsequence (or adds a
nearest-grid interpolation paragraph), which is a `\begin{theorem}` conclusion
change. Per review-loop Component 3 statement-changing escalation, headline
changes are NOT applied automatically — they require explicit user approval. The
author already discloses this as user-decision Q3 (`\todo`, lines 40–42); the
bound is non-vacuous along an infinite subsequence. Non-blocking (does not block
correctness of what IS proven). Surfaced to user; no auto-fix. Accept gate is
still cleared because this is not a REAL-blocking *critical*.

### Weakness #2 (severity: minor, raised by 2/5)
**Claim:** `lem:kl` is stated with the exact-count hypothesis "each cell contains
exactly $n/M_0$ design points", which is strictly the $m\mid n^{1/d}$ subsequence
condition; in mild tension with `rem:setup`'s comparable-count claim, and the
divisibility hypothesis is introduced only inside the lemma rather than promoted
into `ass:setup`. (`sections/04-kl-bound.tex:8–9`.)
**Verdict:** REAL-nonblocking — entangled with Weakness #1.
**Rebuttal / fix-plan:** Confirmed verbatim at `04-kl-bound.tex:8–9`. The "exactly
$n/M_0$" count is the honest consequence of the $m\mid n^{1/d}$ hypothesis that is
the subject of user-decision Q3 (Weakness #1); it is not a standalone overclaim.
Promoting the divisibility into `ass:setup` or relaxing to comparability is part
of the same Q3 decision — folding it in now would pre-empt that user choice.
Deferred to Weakness #1's escalation. No standalone fix.

### Weakness #3 (severity: minor, raised by 1/5)
**Claim:** The "In particular" clause of `lem:fano` bounds the $M^2$-average KL by
the maximum, but the displayed average over $M^2$ pairs includes the $M$ diagonal
($k=k'$) terms which are zero; the one-line "average by the maximum" justification
glosses the diagonal-zero accounting. (`sections/05-fano.tex:18–19`.)
**Verdict:** REAL-nonblocking (narration gloss; inequality correct).
**Rebuttal / fix-plan:** Confirmed at `05-fano.tex:18–19`. The inequality
$\tfrac1{M^2}\sum_{k,k'}\KL\le\max_{k\ne k'}\KL$ holds exactly: the $M$ diagonal
terms are $0$, the remaining $M(M-1)$ off-diagonal terms are each $\le\max_{k\ne
k'}\KL$, and dividing by the larger $M^2$ only shrinks the average — so average
$\le\frac{M(M-1)}{M^2}\max\le\max$. The displayed bound is valid as written; only
the prose is terse. Patch would be a clarifying sub-clause (style, ≤1 line), but
the math is already licensed and downstream Step 2 uses the (correct) max bound;
no correctness fix required. Cosmetic only — not fixed under minimum-change.

### Weakness #4 (severity: style/minor, raised by 2/5)
**Claim (merged):** (a) Step 16 of the KL bound bounds each summand "by its
maximum $\tfrac{\omega^2}{m^{2s}}G_\infty$" without naming the licensing pointwise
sup-norm fact $g(\cdot)^2\le\|g\|_\infty^2=G_\infty$
(`sections/04-kl-bound.tex:38`); and (b) the abstract Fano observation $Y$ is
never explicitly identified with the data $D_n$ at the application site, so
$\psi(Y)$ and $\Pr_{P_{f_k}}$ coexist without binding $Y=D_n$
(`sections/06-main-theorem.tex:106`). Plus the seven rendered `\todo`
user-decision markers cluttering statement bodies.
**Verdict:** (a) INTENTIONAL/style; (b) PHANTOM; `\todo` clutter INTENTIONAL.
**Rebuttal / fix-plan:**
(a) Confirmed at `04-kl-bound.tex:38–39`. $G_\infty:=\|g\|_\infty^2$ is *defined*
in the lemma statement (`:10`); the per-cell summand is exactly
$(\tfrac{\omega}{m^s}g(\cdot))^2=\tfrac{\omega^2}{m^{2s}}g(\cdot)^2\le
\tfrac{\omega^2}{m^{2s}}G_\infty$, so the licensing fact is implicit-but-named
(via the $G_\infty$ symbol). Correct, non-blocking, style only — not fixed.
(b) PHANTOM: `ass:setup` defines the data $D_n=(x_i,y_i)_{i\le n}$ and $P_{f_k}$
is the law of $D_n$ under $f^*=f_k$; in Step 4 the test $\psi$ is a function of
the observations and $Y$ is the same data object. The $Y\!\leftrightarrow\!D_n$
binding is unambiguous in context (the same measure $\Pr_{P_{f_k}}$ governs
both). No defect — rebut, no fix.
`\todo` markers: INTENTIONAL — they are the five Socratic user-decision markers
(Q1/Q3×2/Q4/Q6) deliberately retained pending human confirmation, documented in
the runner log. Not a math defect.

## Convergence check

Iteration-1 merged set: {#1 headline-subsequence (major), #2 $M\ge M_0\ge8$
(fixed), #3 digest-$\alpha$ (rebutted), #4 lem:kl exact-count (deferred), #5 $g$
double-duty (fixed), #6 dead macros (fixed), #7 `\argmin` single-use (rebutted),
#8 Fano averaged-vs-max attribution (fixed)}.

Iteration-2 merged set maps to: #1 ≡ iter-1 #1 (still open, statement-change);
#2 ≡ iter-1 #4 (still deferred to Q3); #3, #4 are NEW minor/style/phantom seams.
The four iter-1 items that were *fixed* (#2,#5,#6,#8) did not recur — the fixes
held. Overlap of currently-open weaknesses with iter-1 is ~50% (#1, #2 recur; #3,
#4 are new), below the 0.8 convergence-failure threshold; and the mean rose
8.00 → 8.40. No stall. The accept gate fires before any convergence concern.

## Fixes applied this iteration

**None.** The accept gate (mean 8.40 > 8, no unresolved REAL-blocking critical)
fired. Per the task directive (ACCEPTED — do NOT modify the proof; record only),
the source is left untouched. The two open REAL-nonblocking weaknesses (#1, #2)
are statement-change / user-decision items already escalated in iteration 1 and
re-surfaced to the user; #3, #4 are cosmetic/phantom and not actionable under
minimum-change.

## Not fixed (surfaced to user)

- #1 (major, REAL-nonblocking, STATEMENT-CHANGE): "for all $n$" headline vs
  $m\mid n^{1/d}$ subsequence. Requires theorem-headline change → user decision
  (Q3 already flagged in source).
- #2 (minor, REAL-nonblocking): `lem:kl` exact-count hypothesis — entangled with
  #1's Q3; deferred to the same decision.
- #3 (minor, REAL-nonblocking): Fano diagonal-zero narration gloss — math valid,
  cosmetic; left as-is.
- #4 (style/phantom): Step-16 sup-norm narration (style, $G_\infty$ already
  named) and $Y=D_n$ binding (phantom, unambiguous in context); `\todo` markers
  intentional scaffolding.

## Accept decision

**mean = 8.40 > 8 (strict) AND no unresolved REAL-blocking critical → ACCEPT.**
Loop terminates in success at iteration 2 (Component 4, gate 1). Proof recorded as
accepted; no source modification.
