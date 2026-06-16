# Review iteration 2 — VC generalization bound

Proof under review: `\thm:vc-bound` (Uniform VC generalization bound) and its
supporting lemmas, in `eval_results/03-vc-generalization/`.

## Reviewer scores
| Reviewer | Lens | Score | Blocking? |
|---|---|---|---|
| R1 | correctness: line-by-line | 7 | no |
| R2 | correctness: assumptions/generality | 9 | no |
| R3 | correctness: ML-significance | 9 | no |
| R4 | math-taste | 8 | no |
| R5 | derivation-integrity | 7 | no |
| **mean** | | **8.00** | |

## Accept decision
mean = 8.00 is **not** strictly > 8, so the accept gate fails (`mean > 8` is
strict). No unresolved REAL-blocking critical exists. Decision per orchestrator:
**ITERATE** — apply minimum-change fixes to the REAL-nonblocking weaknesses.

## Merged + verified weaknesses

### Weakness #1 (severity: major, raised by 3/5)
**Claim:** Symmetrization chain step (d) is displayed as an equality
(`\overset{(d)}{=}`) but the accompanying prose at :55 explicitly invokes the
triangle inequality to split the sum, which is a strict `\le`; so the printed
relation overstates what the prose proves. (R1 major + R1 minor prose; R5-a
major; R5-b major + minor.)
**Location:** sections/03-symmetrization.tex:39 (and prose :55).
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed: from step (c) `E[sup|...|]`, the triangle
split gives `E[sup|.'|]+E[sup|.|]=2E[sup|.|]`, a genuine `\le`. The lemma's
overall conclusion `\le 2\Rad_n(\Lbar)` is unaffected. **Fixed**: changed
`\overset{(d)}{=}` to `\overset{(d)}{\le}` (one token). Prose already correct.

### Weakness #2 (severity: minor, raised by 3/5)
**Claim:** The confidence trace is stale relative to the iteration-2 .tex: trace
Steps 18/20/21/22 assert `2\Rad_n(\Lcal)` and `C=3`, whereas the audited proof
uses `2\Rad_n(\Lbar)` and `C=\sqrt{17}`; green tags do not attest to the lines
actually present (verification-coverage gap, not a math error). (R1 minor; R3
style; R5 minor.)
**Location:** .proof-research/confidence-trace.md Steps 18, 20, 21, 22.
**Verdict:** REAL-nonblocking.
**Rebuttal / fix-plan:** Confirmed bookkeeping drift; the .tex is correct.
**Fixed**: updated trace Steps 18/20 to `\Rad_n(\Lbar)` and
`2(d\log(en/d)+\log 2)/n`; Steps 21/22 to the `(d)` inflation route and
`C_0=\sqrt{17}`. Verification methods refreshed accordingly.

### Weakness #3 (severity: minor, raised by 1/5)
**Claim:** Lemma 6 (Massart) is stated "Under \Cref{ass:vc}" (bundling
`n>=d>=1`), but its first inequality needs no size constraint; only the second
(Sauer--Shelah at `m=n>=d`) does, so the stated hypothesis is mildly stronger
than the proof uses. (R2.)
**Location:** sections/04-sauer-massart.tex:69-70.
**Verdict:** INTENTIONAL.
**Rebuttal:** Stating a lemma under the project's standing assumption is a
benign, deliberate convention; the hypothesis is satisfied at every cite-site
and the conclusion is correct. Splitting `ass:vc` into per-inequality
preconditions is a restructuring the minimum-change principle forbids and the
panel did not require. No fix.

### Weakness #4 (severity: minor, raised by 1/5)
**Claim:** The headline theorem advertises arbitrary input space / every
distribution, but relies on the image-admissible-Suslin measurability convention
stated only in Preliminaries, not surfaced in the theorem hypotheses. (R2.)
**Location:** sections/01-preliminaries.tex:13-17.
**Verdict:** INTENTIONAL.
**Rebuttal:** The reviewer concedes it is "properly disclosed (so not a silent
assumption)". It is the standard empirical-process measurability convention,
declared once globally. Importing it into the theorem hypotheses would be a
statement-level edit (forbidden without user approval) and is not warranted. No
fix.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** The result carries an extra `\sqrt{\log(n/d)}` factor, not the
minimax-optimal `\sqrt{d/n}`. (R3.)
**Location:** sections/05-main-theorem.tex:86.
**Verdict:** INTENTIONAL.
**Rebuttal:** Loose-by-design and explicitly disclosed in `rem:rate`: the
optimal rate needs Dudley chaining, outside the advertised
symmetrization/Sauer--Shelah/Massart pipeline. Matches the claimed contribution.
No fix.

### Weakness #6 (severity: minor, raised by 1/5)
**Claim:** Two parallel notations (risk `R/\Rhat` vs operator `D\ell/\Dhat\ell`)
force the reader to keep the `def:loss-class` dictionary live across sections.
(R4.)
**Location:** sections/01-preliminaries.tex:37.
**Verdict:** INTENTIONAL.
**Rebuttal:** The operator notation is what makes the symmetrization section
clean; the one-line dictionary is deliberate and consistent. Collapsing one
notation would restructure §3 — disallowed by minimum-change. No fix.

### Weakness #7 (severity: minor, raised by 1/5)
**Claim:** Step (d) takes a convoluted route (inflates `\log 2` into
`d\log(en/d)`, `2\sqrt2\to4`, lands `C_0=\sqrt{17}`) where direct Cauchy--Schwarz
gives the cleaner `C_0=3`. (R4.)
**Location:** sections/05-main-theorem.tex:62.
**Verdict:** INTENTIONAL.
**Rebuttal:** The universal constant is explicitly non-optimized
(`todo` user-decision at :25; `rem:rate`); its value is immaterial to the rate.
The inflation gives a single clean `d\log(en/d)` complexity term in the headline.
Rewriting to `C_0=3` is a taste-only change the gate does not require. No fix.

### Weakness #8 (severity: style, raised by 1/5)
**Claim:** Macro `\sgn` is bound to `\sigma`, priming the reader for the signum
function rather than a sign vector. (R4.)
**Location:** macros.tex:80.
**Verdict:** INTENTIONAL/PHANTOM.
**Rebuttal:** `\sgn` for Rademacher signs is a defined, consistent shorthand
rendering as `\sigma`; renaming a macro is forbidden by minimum-change and the
reading is conventional. No fix.

## Verdict counts
- REAL-blocking: 0
- REAL-nonblocking: 2 (both fixed)
- PHANTOM: 0 (W8 borderline INTENTIONAL/PHANTOM)
- INTENTIONAL: 6

## Fixes applied this iteration
1. `sections/03-symmetrization.tex:39` — `\overset{(d)}{=}` → `\overset{(d)}{\le}`.
2. `.proof-research/confidence-trace.md` Steps 18/20/21/22 — refreshed to
   `\Rad_n(\Lbar)`, `2(d\log(en/d)+\log 2)/n`, and `C_0=\sqrt{17}`.

No theorem/lemma headline statement was changed. Post-fix lint (incl. R19) and
LaTeX compile gates re-run clean.
