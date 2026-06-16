# Runner log — hoeffding-prove (eval id=1)

## What I built

A standalone appendix-grade proof of **Hoeffding's inequality**: for independent
$X_1,\dots,X_n$ with $X_i\in[a_i,b_i]$ a.s. and $S_n=\sum_i X_i$,
$\Pr[\,|S_n-\E S_n|\ge t\,]\le 2\exp\!\big(-2t^2/\sum_i(b_i-a_i)^2\big)$.
The proof follows the canonical **MGF / Chernoff** skeleton:

1. **One-sided Chernoff bound.** Apply Markov's inequality to
   $\exp(\lambda(S_n-\E S_n))$ for $\lambda>0$; independence factorizes the MGF.
2. **Hoeffding's lemma** (separate `\begin{lemma}` with proof): a bounded
   centered random variable $Y\in[a,b]$ is sub-Gaussian with
   $\E e^{\lambda Y}\le \exp(\lambda^2(b-a)^2/8)$. Proved via convexity bound +
   second-order Taylor of the log-MGF $\psi$ with $\psi''\le (b-a)^2/4$.
3. **Optimize over $\lambda$.** The exponent $-\lambda t+\lambda^2 V/8$ with
   $V=\sum_i(b_i-a_i)^2$ is minimized at $\lambda^\star=4t/V$ (explicit
   first-order condition), giving the one-sided bound $\exp(-2t^2/V)$.
4. **Two-sided bound** by applying the one-sided result to $-X_i$ and a union
   bound over the two tail events, yielding the factor $2$.

Decomposition: one auxiliary lemma (`lem:hoeffding`) + one main theorem
(`thm:hoeffding`), assembled in the theorem's proof.

## Patterns chosen
- Statement template: restated/condition-list (single clean hypothesis block).
- Derivation pattern: **trailing-justification block** (§5.1 of templates.md) —
  each chained inequality closes with a comma-list of per-step reasons.
- Organizational pattern: concentration-via-MGF (Chernoff method); the
  λ-optimization is shown with an explicit first-order condition (no phantom
  optimization), and the two-sided extension uses a small union bound.

## Phase A.1a — Socratic intake (self-Q&A; no interactive user)

Scope = Standard → full Setting group + decomposition-axis question. The task
prompt already pins the target inequality, the proof route (MGF/Chernoff →
Markov → Hoeffding's lemma → optimize λ), and the output file. The genuinely
user-owned forks below were resolved by adopting the **stronger/tighter**
default in each case and recording a `\todo{user-decision: ...}` in the source.

**Q1 [target form / constant tightness].** State the bound with the exact
constant $2\exp(-2t^2/\sum_i(b_i-a_i)^2)$, or allow a `\poly`/looser universal
constant in the exponent?
  - Proposed (STRONGER): the exact textbook constant — exponent $-2t^2/V$ with
    the leading $2$, no slack. This is the sharp Hoeffding constant and matches
    the prompt's displayed inequality verbatim.
  - Alternative: absorb into a universal $C$ (e.g. $\exp(-ct^2/V)$) — easier to
    prove via a cruder sub-Gaussian bound, but loses the textbook sharpness.
  - Adopted: STRONGER. `\todo{user-decision: exact constant 2 exp(-2t^2/V),
    alt: looser universal-C exponent}`.

**Q2 [Hoeffding's-lemma constant].** Prove Hoeffding's lemma with the sharp
sub-Gaussian variance proxy $(b-a)^2/8$ (i.e. $\psi''\le(b-a)^2/4$), or a
weaker proxy?
  - Proposed (STRONGER/TIGHTER): the sharp $(b-a)^2/8$ proxy via the
    $\psi''(s)=\mathrm{Var}_{Q_s}(Y)\le (b-a)^2/4$ variance-of-bounded-RV bound.
    This is exactly what yields the leading constant $2$ in the exponent.
  - Alternative: a convexity-only proxy giving $(b-a)^2/2$ — shorter but
    doubles the constant and fails to reproduce the target.
  - Adopted: STRONGER. `\todo{user-decision: sharp (b-a)^2/8 proxy via
    psi'' <= (b-a)^2/4, alt: loose (b-a)^2/2 convexity proxy}`.

**Q3 [two-sided route].** Obtain the two-sided $2\exp(\cdots)$ via a union
bound over the upper and lower tails (applying the one-sided result to $-X_i$),
or only prove the one-sided bound?
  - Proposed (STRONGER): full two-sided bound with the explicit factor-$2$
    union bound — this is the stated theorem.
  - Alternative: one-sided only — strictly weaker than the prompt's claim.
  - Adopted: STRONGER. `\todo{user-decision: two-sided via union over both
    tails, alt: one-sided only}`.

**Q4 [decomposition axis].** Lemma boundary: factor Hoeffding's lemma out as a
named `\begin{lemma}` with its own proof (Occam: it has ≥1 downstream consumer,
the main theorem), versus inlining it.
  - Proposed: named lemma `lem:hoeffding` — the eval explicitly requires it as a
    separate environment, and it is the single reusable sub-result.
  - Adopted: named lemma. No `\todo` needed (this matches the prompt).

No residual ambiguity surfaced during decomposition (A.6 clean). No citations
are required: both the lemma and the theorem are proved from first principles,
so `refs.bib` is omitted (no `\cite{}` calls).

## Phase A.2 — Technical reconnaissance
Tools the proof uses, with digest status:
- **Markov's inequality** — textbook, no digest needed (R14 does not list it).
- **Chernoff method (MGF + Markov on $e^{\lambda S}$)** — textbook; no R14 keyword.
- **Hoeffding's lemma** — proved in-file from convexity + the log-MGF second
  derivative bound; digest `.proof-research/hoeffding-lemma.md` written for the
  sharp $\psi''\le(b-a)^2/4$ step (the one non-obvious inequality).
- **Sub-Gaussian / variance-of-bounded-RV bound** $\mathrm{Var}(Y)\le(b-a)^2/4$
  (Popoviciu) — digest folded into hoeffding-lemma.md.
None of the R14-tracked advanced-technique keywords (matrix Bernstein,
Hanson–Wright, etc.) appear, so no R14 digests are triggered.

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 15 (check_confidence_tags estimate: 18 → 83.3% coverage).
- After sweep: 13 🟢 / 2 🟡 / 0 🔴.
- The 2 🟡 are cross-checked-via-reference: Step 3 (CGF second-derivative =
  $\Var_{Q_\lambda}$ identity, matched to hoeffding-lemma.md / BLM Lemma 2.2)
  and Step 11 (Hoeffding's-lemma application — hypotheses verified at the
  cite-site, matched to lem:hoeffding).
- The load-bearing arithmetic (Step 13: $g(\lambda^\star)=-2t^2/V$ from
  $\lambda^\star=4t/V$) and the sharp variance proxy (Steps 4–5,7) were
  independently hand re-derived → 🟢.
- Sub-agents fired: 0 (every step resolved by a fast path — named textbook
  inequality or digest/lemma match — so no fire-and-forget re-derivation
  needed; the two non-obvious steps were hand-checked directly).
- Any 🔴 with `unable-to-derive`: none. No `\todo{verify}` markers required by
  the sweep. (The three `\todo{user-decision: ...}` in runner-log are Phase
  A.1a intake choices, not unverified steps.)
- Trace: .proof-research/confidence-trace.md (gate (c) exit 0).

## Where I had to make calls
- Adopted the sharp $(b-a)^2/8$ sub-Gaussian proxy (Q2) so the leading exponent
  constant is exactly $2$ as the prompt demands; the cruder convexity proxy
  would have failed the assertion on the exact rate.
- Proved Hoeffding's lemma fully (including the $\psi''$ variance bound) rather
  than citing it, per the eval's requirement that it not be a black box.
- No `refs.bib`: everything is self-contained, so shipping a `.bib` would add an
  unused file. (Citation discipline: zero `\cite{}` → zero unresolved keys.)

## Self-check results
- lint.py errors: 0 (R0a–R19 all pass; exit 0). R19 clean — every proof is
  display-dominated; no `% lint: ignore` escape hatch needed.
- latexmk compile_ok: true; overfull_violations: []; undef_refs/undef_cites: [];
  exit 0. PDF at pdf/main.pdf (copied from .output/main.pdf).
- check_confidence_tags.py: exit 0 (15 tagged entries, 83.3% coverage,
  0 red_issues).
- Cite-key check: no `\cite{...}` used → no refs.bib shipped → no unresolved
  keys (vacuously clean).
- All `\input`'d section files exist on disk: yes
  (sections/01-hoeffding-lemma.tex, sections/02-hoeffding-theorem.tex).
- aliascnt rendering: main.aux anchors lem:hoeffding → lemma.1.1 and
  thm:hoeffding → theorem.2.1, confirming cleveref renders "Lemma 1.1" /
  "Theorem 2.1" correctly (R0c also passes statically).

## Phase D — review loop (five-reviewer panel)
- Iterations run: 1 (of 3-iteration cap).
- Per-iteration mean history: [9.00].
- Final mean: 9.00.
- Accepted: yes (accept gate: mean 9.00 > 8 strict AND no unresolved
  REAL-blocking critical → ACCEPT on iteration 1; no edits applied).
- Final five scores (R1 line-by-line, R2 assumptions/generality,
  R3 ML-significance, R4 math-taste, R5 derivation-integrity): 9, 9, 9, 9, 9.
- Merged weaknesses: 11 raw → 7 distinct. Severities: 0 critical, 0 major,
  5 minor, 2 style. Verdicts: 0 REAL-blocking, 5 REAL-nonblocking, 0 PHANTOM,
  2 INTENTIONAL. No unresolved critical.
- Highest-signal item (3/5): vestigial universal-constant convention paragraph
  (INTENTIONAL, standard boilerplate). The three surviving `\todo{user-decision}`
  markers are intake records surfaced for the user, not unverified steps.
- Iteration artifact: .proof-research/review-iteration-1.md (all scores, mean,
  merged/verified weaknesses, verdicts, rebuttals).

## What's incomplete
- Phase D residual: nothing blocking. The seven recorded weaknesses are all
  minor/style and were left unfixed per the ACCEPT gate (no edits on accept);
  the two INTENTIONAL items (user-decision \todo markers, constant convention)
  are user-owned calls, not defects.
- Residual `\todo{}` markers: three `\todo{user-decision: ...}` from the
  Phase A.1a self-Q&A (intake decisions Q1–Q3, all adopting the
  stronger/tighter option). No `\todo{verify}` markers — the sweep left no
  step at 🔴.
- No experiments-plan.md: the eval prompt does not request experiments
  (design-only plans are produced only when asked).

v1.2 retrofit: +hyperref, user-decision todos -> decisions.md (3 moved, 0 verify kept)

v1.2 finalize: completed 0 todos, geometry margin=1in
