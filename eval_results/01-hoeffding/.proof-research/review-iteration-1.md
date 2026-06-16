# Review iteration 1 — 01-hoeffding

Proof under review: Hoeffding's inequality (`sections/02-hoeffding-theorem.tex`)
and its preliminary `sections/01-hoeffding-lemma.tex`. Five-member independent
panel, full run.

## Reviewer scores

| Reviewer | Lens | Score | Blocking |
|---|---|---|---|
| R1 | Correctness: line-by-line rigor | 9 | no |
| R2 | Correctness: assumptions / generality / tightness | 9 | no |
| R3 | Correctness: ML-community significance | 9 | no |
| R4 | Math taste | 9 | no |
| R5 | Derivation integrity | 9 | no |
| **mean** | | **9.00** | |

Score history: [9.00].

## Accept gate

`mean = 9.00 > 8` (strict) AND no unresolved REAL-blocking critical weakness.
**Decision: ACCEPT.** Per the review-loop accept gate (Component 4, gate 1), the
proof is accepted as-is; no edits are applied. All merged weaknesses below are
minor/style and are recorded with verdicts and rebuttals only.

## Merged + verified weaknesses

Eleven raw weaknesses across five reviews merged to seven distinct items
(same `file:line ± 3` or paraphrase = one; max severity kept; raise-count noted).

### Weakness #1 (severity: minor, raised by 1/5)
**Claim:** Step 4 bounds $\psi''(\xi)$ by the variance bound but does not explicitly
note that the bound was proved for *every* $\lambda$ (hence valid at the Lagrange
point $\xi$); the reader must supply the connection.
(`sections/01-hoeffding-lemma.tex:78`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The text at lines 54–69 establishes
$\Var_{Q_\lambda}(Y)\le(b-a)^2/4$ "for each fixed $\lambda$" with $Q_\lambda$
indexed by an arbitrary $\lambda$, so the bound is uniform and applies at
$\xi$. Correct as written; the connection is implicit but licensed. Patch
would be one clause but is not load-bearing and the accept gate is already met
— not fixed (no edits on ACCEPT).

### Weakness #2 (severity: style, raised by 2/5)
**Claim:** The quotient-rule second derivative ($\psi''$) is asserted in two
equalities without showing the intermediate differentiation of
$\E[Ye^{\lambda Y}]/\E[e^{\lambda Y}]$; the single most non-elementary algebraic
step is compressed. (`sections/01-hoeffding-lemma.tex:50`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Lines 50–52 name the licensing rule (quotient rule on
Eq.~\eqref{eq:psi-prime}, then rewrite ratios as $Q_\lambda$-expectations). The
result is correct and the rule is named; expanding the cancellation is a
presentation nicety, not a rigor gap. Not fixed.

### Weakness #3 (severity: minor, raised by 2/5)
**Claim:** The optimizer $\lambda^\star=4t/V$ and exponent $-2t^2/V$ require
$V>0$; this well-definedness step is never stated, though it holds because the
headline assumes $a_i<b_i$ for every $i$. (`sections/02-hoeffding-theorem.tex:61`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The theorem hypothesis "$a_i<b_i$" (line 12) forces
$(b_i-a_i)^2>0$, so $V=\sum_i(b_i-a_i)^2>0$ for $n\ge1$ — division by $V$ is
well-defined. Headline-guaranteed; an explicit remark is optional. Not fixed.

### Weakness #4 (severity: minor, raised by 1/5)
**Claim:** $g$ is minimized over all of $\R$, but the Chernoff/Markov step is
only valid for $\lambda>0$; the proof never explicitly notes the unconstrained
minimizer $\lambda^\star=4t/V$ is feasible in the restricted domain
$\lambda>0$. (`sections/02-hoeffding-theorem.tex:57`)
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** The text already records "$\lambda^\star=4t/V\;>\;0$"
(line 61), and since $t>0,V>0$ the minimizer lies in $\lambda>0$ — feasibility
is shown by the displayed inequality. The verbal gloss "feasible in the
restricted domain" is missing but the inequality is on the page. Not fixed.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** Three user-decision `\todo` markers survive into the final PDF,
rendering as bold red [TODO: …] blocks inside the closing Remark — visible
clutter. (`sections/02-hoeffding-theorem.tex:107`)
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** The three `\todo{user-decision: …}` markers (lines
107–113) are deliberate Phase A.1a intake records of the stronger/tighter
option chosen at each fork (exact constant, sharp $(b-a)^2/8$ proxy, two-sided
union bound); they are surfaced for the user's confirmation by design, per the
runner-log. They are user-decision flags, not unverified `\todo{verify}` steps.
Resolving them is the user's call, not an auto-fix. Not fixed.

### Weakness #6 (severity: minor→style, raised by 3/5)
**Claim:** The opening universal-constant convention paragraph
($c, C, C_1,\ldots$ "may change from line to line") is vestigial: this proof
produces the exact constant $2\exp(-2t^2/V)$ with no universal-constant slack,
so the convention is never exercised. (`sections/01-hoeffding-lemma.tex:4`)
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Confirmed: no abstract $c/C$ appears in either body
(grep clean). The convention is standard appendix boilerplate; it is harmless
and does no damage to verifiability. Keeping a stock convention paragraph is a
consistent project style choice. Style-only; not fixed.

### Weakness #7 (severity: style, raised by 1/5)
**Claim:** Five preamble macros are defined but never used in the body
(`\poly`, `\eps`, `\norm`, `\inner`, `\1`) — dead boilerplate. (`macros.tex:56`)
**Verdict:** REAL-nonblocking (style).
**Rebuttal / fix-plan:** Verified by grep over `sections/` + `main.tex`: none of
`\poly,\eps,\norm,\inner,\1` is referenced (exit 1, no matches). They are
shared-template macro definitions; unused defs are inert and touch nothing in
the compiled output or verifiability. Cosmetic only. Not fixed (no edits on
ACCEPT).

## Also-flagged (folded into the above)

- "Differentiation under the expectation asserted as fact rather than shown via
  a dominating function" (`01-hoeffding-lemma.tex:27`, R5) — REAL-nonblocking;
  correctly licensed by boundedness of $Y$ ($Y\in[a,b]\Rightarrow|Ye^{\lambda Y}|$
  bounded, dominated convergence applies). Same compression family as #2; the
  rule is named ("differentiating under the expectation"). Not fixed.
- "$\psi'(\lambda)$ asserted in one display without intermediate chain-rule"
  (`01-hoeffding-lemma.tex:34`, R5) — REAL-nonblocking; merged with #2 as the
  same $\psi'/\psi''$ compression. Result correct, prose-annotated. Not fixed.

## Summary

Unanimous 9/5 panel, mean 9.00. Seven distinct weaknesses: 0 critical, 0 major,
5 minor, 2 style. Verdicts: 0 REAL-blocking, 5 REAL-nonblocking, 0 PHANTOM,
2 INTENTIONAL. No unresolved critical. Accept gate cleared on iteration 1 →
**ACCEPTED, no changes.**
