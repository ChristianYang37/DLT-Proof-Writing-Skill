# Review iteration 1 — frankl-union-closed-gilmer (eval id=7)

## Reviewer scores

| Reviewer | Role | Score | Blocking? |
|---|---|---|---|
| R1 | Correctness: line-by-line rigor | 9 | no |
| R2 | Correctness: assumptions / generality / tightness | 9 | no |
| R3 | Correctness: ML-community significance | 8 | no |
| R4 | Math taste (Occam) | 8 | no |
| R5 | Derivation integrity | 7 | no |
| **mean** | | **8.20** | |

## Accept decision

**ACCEPT.** Gate: `mean > 8` (8.20 > 8, strict) **AND** no unresolved REAL-blocking
critical weakness. No reviewer flagged `blocking:true`; no weakness is severity
`critical`. Highest severity raised is one `major` (REAL-nonblocking). All five
reviewers independently re-derived the load-bearing constants (g_min = 1.4500 > 1.4,
1.26/1.4 = 0.9, 1.8·0.9 = 1.62, Markov 0.01/0.1 = 0.1) and Monte-Carlo-verified the
end-to-end 1.26 amplification (worst observed ratio ≈ 1.74) with zero violations.
Per review-loop.md Component 4 gate 1, the proof is accepted as-is; **no fixes applied**.

## Merged + verified weaknesses

### Weakness #1 (severity: minor, raised by 4/5)
**Claim:** Two unresolved `\todo{user-decision: ...}` markers render as visible bold
`[TODO: ...]` text in the compiled PDF body — one in the single-variable section
(03-single-variable-bounds.tex:14, choice of Gilmer's Lemmas 2–3 vs. the heuristic
placeholder) and one immediately before the headline corollary
(07-frankl-corollary.tex:8, explicit c ≥ 0.01 vs. abstract c > 0). Both decisions are
already resolved and correctly implemented in the math; the markers read as residual
scaffolding that should not survive into a submitted manuscript.
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Confirmed both markers exist and render via the eval-mode
`\todo` macro (`macros.tex:67`, `\textbf{[TODO: #1]}`). They are the deliberate record
of the Phase-A.1a Socratic self-Q&A delegations (runner-log.md "What's incomplete":
eval mode has no interactive user, so each user-decision is logged at its cite-site
with the stronger/faithful branch adopted). They are author-intentional, decision-
neutral to soundness, and meant to be confirmed by the user. Not removed under the
review loop; surfaced to the user for a one-token deletion if a clean PDF is wanted.

### Weakness #2 (severity: major, raised by 2/5)
**Claim:** The load-bearing minimization that pins the constant 1.4 is asserted with
prose ("A direct calculation shows g is minimized on (0, 0.2] at u = 0.2") without a
displayed monotonicity argument licensing that the minimum is attained at the right
endpoint rather than an interior critical point (03-single-variable-bounds.tex:46).
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed the prose at line 46; it is load-bearing (it fixes
g(0.2) = h(0.18)/h(0.10) = 1.450… > 1.4). Both flagging reviewers independently
verified the claim is **correct** — g is strictly decreasing on (0, 0.2], so the
endpoint u = 0.2 is genuinely the minimizer and the resulting 1.4 bound is sound. The
step does not block verification of the proof (the conclusion is true and
numerically reconfirmed by all five panelists). Under the accept gate no fix is
applied; were the loop to continue, the minimum-change fix is a one-line displayed
note that g'(u) < 0 on (0, 0.2] (a local edit, well within cost). Recorded for the
user; not auto-applied since the gate is met and the proof is already accepted.

### Weakness #3 (severity: style, raised by 1/5)
**Claim:** The chain `0.9(p+p') \le \tfrac{p+p'}{2}\cdot 1.8 \le 0.18` writes an exact
identity (the middle term equals 0.9(p+p')) as a non-strict inequality, momentarily
reading as a genuine bound when the only content is p+p' ≤ 0.2
(03-single-variable-bounds.tex:37).
**Verdict:** REAL-nonblocking (style).
**Rebuttal / fix-plan:** Confirmed at line 37. Logically valid (identity is a special
case of ≤); purely presentational. The chain serves to record p+p' ≤ 0.2 ⇒
0.9(p+p') ≤ 0.18 ≤ 1/2, which is exactly what licenses the "h increasing on [0,1/2]"
step that follows. Single lone style flag; no soundness impact. Not fixed under the
accept gate.

### Weakness #4 (severity: minor, raised by 1/5)
**Claim:** Lemma 3.1's ratio lower bound silently relies on the denominator
½(h(p)+h(p')) being strictly positive (well-definedness of the divided inequality)
for (p,p') ≠ (0,0); the positivity is true but never stated
(03-single-variable-bounds.tex:41).
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed. The proof (line 25) explicitly dispatches the
(p,p') = (0,0) case separately, then "assume (p,p') ≠ (0,0)"; for such (p,p') in
[0,0.1]² at least one of p, p' is in (0,0.1], so h(·) > 0 and the denominator is
strictly positive, making the ratio well-defined. The gap is a one-clause omission,
not an error. Near-PHANTOM (the case split already implies positivity); recorded, not
fixed under the accept gate.

### Weakness #5 (severity: style, raised by 1/5)
**Claim:** Region lemmas 4.2 (`lem:region-low`) and 4.3 (`lem:region-mix`) are stated
"Under Eq. (marginal-cap)" (E[X] ≤ 0.01), but their proofs invoke only the strictly
weaker consequence Pr[C0] ≥ 0.9; the stated hypothesis is over-strong — a benign
hypothesis-tightness mismatch (04-region-bounds.tex:28).
**Verdict:** INTENTIONAL.
**Rebuttal / fix-plan:** Confirmed: both region-lemma proofs use only
`Pr[Cz] ≥ 0.9` (derived from the cap via Markov at Eq. markov-region, line 22–23).
Stating the lemmas under the same single hypothesis Eq. (marginal-cap) that governs
the whole section (declared at line 9) is a deliberate uniformity/readability choice —
every region statement keys off one named assumption rather than each restating the
derived Pr[Cz] ≥ 0.9. The hypothesis is satisfied at every cite-site, so no
correctness or generality is lost. Not fixed.

### Weakness #6 (severity: style, raised by 1/5)
**Claim:** The macro `\R` (`\mathbb{R}`) is defined in macros.tex but never used in the
body — a dead, defined-once macro (macros.tex:55).
**Verdict:** REAL-nonblocking (style).
**Rebuttal / fix-plan:** Confirmed: `grep` over all `.tex` body files finds zero uses
of `\R` outside its definition at macros.tex:55. A harmless unused-macro; no soundness
or rendering impact. A one-line deletion would resolve it; not applied under the
accept gate (the proof is accepted as-is and minimum-change forbids cosmetic edits the
gate does not require). Surfaced to the user.

## Verdict counts
- INTENTIONAL: 2 (#1, #5)
- REAL-nonblocking: 3 (#2, #3, #6)  [#4 near-PHANTOM, recorded as REAL-nonblocking]
- REAL-blocking: 0
- PHANTOM: 0 (#4 borderline; the (0,0) case split already implies the positivity)
- Unresolved critical: 0

## Outcome
Accepted at iteration 1. Mean 8.20 > 8, no blocking/critical weakness. Proof
unmodified per the accept gate. Residual style/prose items (#1, #2, #6 in particular)
surfaced to the user as optional one-line cleanups, none required for correctness.
