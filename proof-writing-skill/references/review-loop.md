# Review loop (Phase D)

Read this file at Phase D, after [quality-checks.md](quality-checks.md) §LaTeX compilation gate passes. This replaces the older single-shot end-to-end review with a peer-review-style loop: a **five-member reviewer panel** writes independent formal reviews and 0–10 scores, the author agent **merges** their weaknesses, verifies each, applies minimum-change fixes, and re-submits — bounded and convergence-checked. The proof is **accepted only when the mean panel score exceeds 8 and no unresolved critical weakness remains**.

The five role prompts live in [reviewer-roles.md](reviewer-roles.md); this file owns the orchestration.

Do **not** run this loop for Quick-scope tasks (single inequalities, brief sketches). For Standard and Appendix scope the **full five-reviewer panel runs every iteration**.

## Desk-reject gate (gate (d)) — runs BEFORE the panel

Before the scored-panel loop begins, the proof must pass a binary **desk-reject gate** — the editor's-desk screen a venue applies before a paper ever reaches reviewers. It runs once at Phase-D entry (after gates (a) compile, (b) lint, (c) confidence-tags) and contributes **no score**:

1. **Deterministic half** — `python <skill>/scripts/lint.py main.tex macros.tex sections/*.tex [--bib refs.bib] --final` → exit 0. The `--final` flag adds **R20**: no surviving `\todo{...}` invocation, and no reference to an internal research artifact (`.proof-research/*`, `runner-log`, `decisions.md`, `confidence-trace`, `sweep-step`, `grading.json`). Drafting lint *without* `--final` still tolerates `\todo{verify}`.
2. **Holistic half** — spawn the **desk-reject gate reviewer** (prompt in [reviewer-roles.md](reviewer-roles.md) §Desk-reject gate reviewer). It returns a binary `{verdict, format, anonymity, structure}`: format (editor's-eye layout lint can't see), anonymity/self-containedness (incl. author-anonymity), and complete structure (setting → theorems → insight — *within* the skill's no-standalone-intro/conclusion scope; do not demand an Introduction/Conclusion).

If either half flags a violation (`lint --final` non-zero **or** `verdict == "desk-reject"`), **fix the listed issues** (resolve/remove todos, delete internal-file references, repair format, fill a missing structural element) and **re-run gate (d)**. Only on a clean `lint --final` **and** `desk-accept` does the five-reviewer scored-panel loop below begin.

A genuinely-unresolvable `\todo{verify}` cannot pass gate (d): a desk-ready paper has no open todos, so the step must be resolved/restructured or escalated to the user as not-yet-submittable. This is stricter than the drafting honesty protocol, by design.

## The loop, at a glance

```
iteration = 0
prev_weaknesses = []
while iteration < 3:                                   # 3-iteration hard cap
    iteration += 1

    # Component 1 — five INDEPENDENT reviewers, spawned in one parallel batch.
    reviews = spawn_panel([R1, R2, R3, R4, R5])        # see reviewer-roles.md
    scores  = [r.score for r in reviews]               # five ints in 0..10
    mean    = sum(scores) / 5

    # Aggregate — merge + dedupe weaknesses across all five BEFORE verifying.
    merged    = dedupe(flatten(r.weaknesses for r in reviews))
    decisions = [verify(w) for w in merged]            # Component 2

    # ACCEPT GATE — mean > 8 (strict) AND no unresolved REAL-blocking critical.
    if mean > 8 and not has_unresolved_critical(decisions):
        accept. write final report. done.

    if iteration > 1 and overlap(prev_weaknesses, merged) >= 0.8:
        escalate.                                      # convergence failure

    fixes = [d for d in decisions if should_fix(d)]    # Component 3
    if not fixes:
        terminate.                                     # nothing actionable left
    apply_fixes(fixes)                                 # minimum-change rules
    compile_and_lint_check()                           # gate (a) + (b), incl R19
    prev_weaknesses = merged
escalate.                                              # hit 3-iteration cap
```

Save each iteration's artifact to `<project-root>/.proof-research/review-iteration-<N>.md` (all five reviews, the five scores + mean, and the merged/verified weakness set) for traceability and rollback.

## Component 1: The reviewer panel

Spawn **five** sub-agents per iteration via `Agent({subagent_type: "general-purpose", ...})`, **all in one parallel batch** (do not serialize — they are independent). Each gets the shared scaffold + its role block + the shared return block from [reviewer-roles.md](reviewer-roles.md):

- **R1 — Correctness: line-by-line rigor** — every transition licensed by a named rule.
- **R2 — Correctness: assumptions / generality / tightness** — quantifier order, hypotheses-met-at-cite-site, constant hygiene, requirements propagate by the max.
- **R3 — Correctness: ML-community significance** — does the proof deliver the claimed contribution/rate/regime under a skeptical area chair's scrutiny.
- **R4 — Math taste** — notation abuse, symbol overload, economy (the Occam lens).
- **R5 — Derivation integrity** — prose-asserted steps (review-time partner of R19), hand-waving, fabricated cites, hallucinated lemma use, invented probability budgets.

Inputs to every reviewer: the source `.tex` files, `.output/main.pdf`, `.output/main.log`, and `.proof-research/confidence-trace.md` if Phase C.5 ran (prioritize 🟡/🔴 steps; treat 🟢 as author-verified unless a defect is visible). Each returns its structured markdown (`## Summary … ## Score … ## Blocking?`). Parse the integer `## Score` and the `## Blocking?` flag from each.

### Aggregate before verifying

1. **Mean.** `mean = (s1 + s2 + s3 + s4 + s5) / 5`, equal weight. Record the five raw scores and the mean.
2. **Merge + dedupe weaknesses.** Collect all five `## Weaknesses` lists. Two weaknesses are duplicates if they cite the **same `file:line` ± 3 lines** OR their Claims are semantic paraphrases (judge liberally, the same test as the 0.8 convergence overlap below). On merge, keep the **highest severity** any reviewer assigned, concatenate distinct evidence, and record **how many of the five raised it** (3/5 is high-signal; a lone flag may be a phantom). Verify the merged set **once** — never verify the same weakness twice.

## Component 2: Verification step

The panel can be wrong. Before fixing anything, the author agent verifies each **merged** weakness point-by-point.

For each weakness `w`:

1. **Read the Evidence**: open `file:line`, confirm the quoted text exists and matches.
2. **Re-read context**: read the surrounding 10–30 lines so you understand what the proof is actually claiming at that point.
3. **Assign a verdict**:

| Verdict | Meaning | Action |
|---|---|---|
| **REAL-blocking** | weakness is correct AND it blocks verification of the proof | fix (subject to Component 3 cost rules) |
| **REAL-nonblocking** | weakness is correct BUT does not block correctness (e.g. confusing notation, missing remark) | fix only if patch cost is low (Component 3) |
| **PHANTOM** | reviewer misread, missed an assumption stated elsewhere, or used incorrect prior knowledge | do NOT fix; write one-sentence rebuttal in iteration trace |
| **INTENTIONAL** | reviewer flagged something the author chose deliberately (e.g. `\poly` slack, omitted constants, style choice consistent with project) | do NOT fix; write one-sentence rebuttal |

A weakness is an **unresolved critical** (blocks the accept gate) iff it is severity `critical` and its verdict is REAL-blocking and it has not yet been fixed this iteration. Criticals judged PHANTOM/INTENTIONAL do not block acceptance — but you must record the rebuttal.

4. **Log the decision** to `.proof-research/review-iteration-<N>.md`:

```markdown
### Weakness #<k> (severity: <level>, raised by <m>/5)
**Claim:** <merged claim>
**Verdict:** REAL-blocking / REAL-nonblocking / PHANTOM / INTENTIONAL
**Rebuttal / fix-plan:** <one to three sentences>
```

The trace is the audit log — it is what you show the user if the loop escalates.

## Component 3: Fix implementation

Apply fixes only after Component 2 verification. Two governing rules.

### Minimum-change principle

Always prefer the smallest patch that resolves the weakness. Specifically:

- Local edit > new lemma > restructured proof.
- Do not introduce a new lemma unless a Claim cannot be patched in place.
- Do not rename existing labels or macros.
- Do not reorder sections.

### Cost-gated fix decision

After verification, decide whether to fix each REAL weakness based on patch cost:

| Severity | Verdict | Patch cost ≤ ... | Action |
|---|---|---|---|
| critical | REAL-blocking | (any) | **must fix** |
| major | REAL-blocking | (any) | **must fix** |
| major | REAL-nonblocking | 10 LaTeX lines | fix |
| minor | REAL-blocking | 5 lines | fix |
| minor | REAL-nonblocking | 3 lines | fix |
| style | REAL-* | 1 line / single token | fix |
| any | PHANTOM | — | do not fix; rebut |
| any | INTENTIONAL | — | do not fix; rebut |

If a REAL weakness's required patch exceeds its cost threshold, demote it: surface in the final report to the user rather than auto-fixing. The minimum-change principle is hard — do not "make the paper better" with edits the panel did not ask for. (Exception: a REAL-blocking *critical* must be fixed regardless of cost, or the loop escalates per the statement-change rule below — it can never be silently demoted, because it blocks the accept gate.)

### Statement-changing escalation

If any verified weakness would require changing the **headline statement** of a `\begin{theorem}` / `\begin{lemma}` / `\begin{proposition}` / `\begin{corollary}` (not its proof, but its conclusion or hypotheses), **stop the loop and ask the user**. Statement changes are too consequential to apply automatically. Surface:

- The current statement (verbatim)
- The proposed statement
- The panel's reason
- Your verification verdict

Wait for explicit user approval before applying.

### Post-fix compile + lint check

After applying fixes, re-run the LaTeX compilation gate AND `lint.py` ([quality-checks.md](quality-checks.md) §LaTeX compilation gate; lint gate (b) including **R19**). A fix that converts a display derivation into prose can trip R19 — catch it here, not at the next panel. If compilation breaks or a new lint error appears, roll back the fix and demote the weakness to "needs user input".

## Component 4: Loop termination

Five gates. Any one triggers exit. Listed in priority order:

1. **Accept gate** — `mean > 8` (strict) AND no unresolved REAL-blocking critical → success. Write final report. (A unanimous-strong panel naturally clears this; the old `accept-as-is` early-exit is subsumed.)
2. **3-iteration hard cap reached** → escalate to user with all five latest reviews, the score history, and the decision log.
3. **Convergence failure** — overlap between this iteration's merged weaknesses and last iteration's ≥ 80% (by Claim similarity, judged liberally). Means previous fixes failed or the panel is stuck on the same complaint. Escalate.
4. **No fixes applied this iteration** — all merged weaknesses were judged PHANTOM/INTENTIONAL, or all REAL ones exceeded their cost threshold — AND no unresolved critical remains. Stop; write final report with rebuttals. (If an unresolved critical remains but cannot be fixed within cost, that is the statement-change escalation, not this gate.)
5. **Statement-change required** → pause loop, ask user (per Component 3).

Compute weakness overlap as: fraction of current merged weaknesses whose Claim semantically matches a Claim from the previous iteration. Threshold 0.8 is liberal — three of four overlapping is enough to signal a stall.

## Final report to user

At loop exit, generate a summary for the user:

```markdown
# Review loop complete (iterations: <N>, final mean: <mean>/10, accepted: <yes/no>)

## Reviewer scores (final iteration)
| Reviewer | Score |
|---|---|
| R1 correctness: line-by-line | <s1> |
| R2 correctness: assumptions/generality | <s2> |
| R3 correctness: ML-significance | <s3> |
| R4 math-taste | <s4> |
| R5 derivation-integrity | <s5> |
| **mean** | **<mean>** |

(Score history across iterations: <m1>, <m2>, ...)

## What was reviewed
<one sentence: the theorem(s) under review, file path>

## What was fixed
- <weakness #k> (raised by <m>/5): <one-line summary of fix> (file:line)
- ...

## What was not fixed and why
- <weakness #k> (severity, verdict): <one-line rebuttal>
- ...

## Residual weaknesses needing your decision
- <weakness #k>: <reason auto-fix declined — e.g. cost too high, statement change, mean stuck ≤ 8>
  - Panel's claim: <verbatim>
  - Proposed fix: <description>
  - Your call.

## Iteration trace
- See `.proof-research/review-iteration-1.md` ... `review-iteration-<N>.md`.
```

This report is what the user sees. It is the only audit surface for the loop. Do not hide phantom-rejected weaknesses — listing them lets the user spot panel drift or your own over-rejection.

## Safety summary

- **Infinite-loop prevention**: 3-iteration cap + convergence detection + "no fixes applied" termination. At most 3 rounds of (5 reviewers + verification).
- **Cost**: five sub-agents per iteration × ≤ 3 iterations = ≤ 15 reviewer agents. Spawn the five in one parallel batch; reviewers return only structured markdown (not file dumps), and the confidence-trace prioritization keeps each reviewer's pass bounded.
- **Quality-degradation prevention**: verification filters panel noise; merge/dedupe prevents the same weakness being fixed five ways; minimum-change limits scope; cost-gated decisions skip nit fixes; statement changes escalate to the user; the post-fix lint check (incl R19) blocks prose-regression.
- **Trace and rollback**: every iteration's five reviews + scores + decisions saved under `.proof-research/`. Compile/lint failures roll back fixes automatically.
- **Reviewer faithfulness**: the shared scaffold forbids padding to 7, restructuring suggestions, headline changes, and uncharitable reads; "0 weaknesses" with a high score is a valid output. The `> 8` mean bar means a strong proof still has to satisfy all five lenses.
