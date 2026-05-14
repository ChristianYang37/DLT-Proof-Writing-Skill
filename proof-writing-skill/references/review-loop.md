# Review loop (Phase D)

Read this file at Phase D, after [quality-checks.md](quality-checks.md) §LaTeX compilation gate passes. This replaces the older single-shot end-to-end review with a peer-review-style loop: a reviewer sub-agent writes a formal review, the author agent verifies each weakness, applies minimum-change fixes, and re-submits — bounded and convergence-checked.

Do **not** run this loop for Quick-scope tasks (single inequalities, brief sketches). It is for Appendix-grade proofs only.

## The loop, at a glance

```
iteration = 0
prev_weaknesses = []
while iteration < 3:
    iteration += 1
    review = spawn_reviewer_subagent()          # Component 1
    if review.verdict == "accept-as-is": done.
    if iteration > 1 and overlap(prev, review.weaknesses) >= 0.8:
        escalate.                                # convergence failure
    decisions = [verify(w) for w in review.weaknesses]  # Component 2
    fixes = [d for d in decisions if should_fix(d)]     # Component 3
    if not fixes:
        terminate.                               # nothing actionable left
    apply_fixes(fixes)                           # minimum-change rules
    compile_check()
    prev_weaknesses = review.weaknesses
escalate.                                        # hit 3-iteration cap
```

Save the artifact of each iteration to `<project-root>/.proof-research/review-iteration-<N>.md` for traceability and rollback.

## Component 1: Reviewer sub-agent

Spawn via `Agent({subagent_type: "general-purpose", ...})`. Inputs: the source `.tex` files, the compiled PDF (`.output/main.pdf`), the compile log (`.output/main.log`), and the confidence trace (`.proof-research/confidence-trace.md` if Phase C.5 ran).

If a confidence trace is present, instruct the reviewer to **prioritize 🟡 and 🔴 steps** and to treat 🟢 steps as author-verified unless a defect is otherwise visible. This focuses reviewer attention on the parts most likely to harbor errors and saves reviewer tokens on already-checked algebra.

### Prompt template

```
You are a senior deep-learning-theory reviewer for NeurIPS / ICML / FOCS / STOC.
Read the paper at <main.tex and inputs> and the rendered PDF at .output/main.pdf,
plus the compile log at .output/main.log. Write a peer review.

YOUR GOAL: a faithful, charitable review aimed at making this proof's
contribution cleaner and more correct. Not to find fault for its own sake.
A genuinely strong proof deserves a short review.

PROCESS:
1. Read the paper top to bottom, assuming statements are correct. Build a
   mental model of the contribution.
2. Identify what the actual contribution is and verify that the proof
   skeleton supports it.
3. Only after step 2, look for defects.

RULES:
- Report AT MOST 7 weaknesses. Report ONLY as many as you actually find.
  Returning 0, 1, or 2 weaknesses is correct when the proof is strong.
  DO NOT pad to reach 7.
- Every weakness must include:
  - Claim: one sentence
  - Evidence: file:line + verbatim quote of the offending text
  - Severity: critical | major | minor | style
- "critical": proof is wrong as stated.
- "major": gap or ambiguity that blocks verification.
- "minor": notation / phrasing that confuses but does not block correctness.
- "style": pure typography or surface convention.
- DO NOT suggest restructuring, new directions, additional experiments,
  alternative techniques, or polish-level improvements unless they rise to
  major severity by your own definitions above.
- DO NOT raise weaknesses already addressed elsewhere — re-read before flagging.
- If a notation or convention is unusual but consistent and well-defined,
  do not flag it.
- Assume the author chose `\poly` slack and absorbed constants intentionally
  unless the surrounding text says otherwise.
- DO NOT propose changes that would alter the headline statement of any
  theorem. If you believe the headline is wrong, raise it as a Question, not
  a Weakness.

OUTPUT: strictly the markdown structure below, no preamble.

## Summary
[≤ 200 words. Restate the contribution and the proof skeleton. Demonstrate
you understood the paper.]

## Strengths
[3–5 specific bullets. No empty praise like "well-written". Each must name
the technique, decomposition, or move that makes the proof good.]

## Weaknesses
[0–7 bullets, each in the three-line format Claim/Evidence/Severity.
Sort by severity descending.]

## Questions for the author
[≤ 5 bullets. Softer than weaknesses — clarifications, unclear-but-not-wrong
points, or things flagged as "headline change" rather than weakness.]

## Verdict
One of: accept-as-is | accept-with-minor-revisions | major-revision-required | reject-as-flawed
```

Return the review as a markdown string. The author agent saves it to `.proof-research/review-iteration-<N>.md`.

## Component 2: Verification step

The reviewer can be wrong. Before fixing anything, the author agent verifies each weakness point-by-point.

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

4. **Log the decision** to `.proof-research/review-iteration-<N>.md` with the format:

```markdown
### Weakness #<k> (severity: <level>)
**Claim:** <reviewer's claim>
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

If a REAL weakness's required patch exceeds its cost threshold, demote it: surface in the final report to the user rather than auto-fixing. The minimum-change principle is hard — do not "make the paper better" with edits the reviewer did not ask for.

### Statement-changing escalation

If any verified weakness would require changing the **headline statement** of a `\begin{theorem}` / `\begin{lemma}` / `\begin{proposition}` / `\begin{corollary}` (not its proof, but its conclusion or hypotheses), **stop the loop and ask the user**. Statement changes are too consequential to apply automatically. Surface:

- The current statement (verbatim)
- The proposed statement
- The reviewer's reason
- Your verification verdict

Wait for explicit user approval before applying.

### Post-fix compile check

After applying fixes, re-run the LaTeX compilation gate ([quality-checks.md](quality-checks.md) §LaTeX compilation gate). If compilation breaks, roll back the fix and demote the weakness to "needs user input".

## Component 4: Loop termination

Five gates. Any one triggers exit. Listed in priority order:

1. **`verdict == "accept-as-is"`** → success. Write final report.
2. **3-iteration hard cap reached** → escalate to user with the latest review and decision log.
3. **Convergence failure** — overlap between this iteration's weaknesses and last iteration's ≥ 80% (by Claim similarity, judged liberally). Means previous fixes failed or reviewer is stuck on the same complaint. Escalate.
4. **No fixes applied this iteration** — all weaknesses were judged PHANTOM/INTENTIONAL, or all REAL ones exceeded their cost threshold. Stop; write final report with rebuttals.
5. **Statement-change required** — pause loop, ask user (per Component 3).

Compute weakness overlap as: fraction of current weaknesses whose Claim semantically matches a Claim from the previous iteration. Threshold 0.8 is liberal — three of four overlapping is enough to signal a stall.

## Final report to user

At loop exit, generate a summary for the user:

```markdown
# Review loop complete (iterations: <N>, verdict: <final>)

## What was reviewed
<one sentence: the theorem(s) under review, file path>

## What was fixed
- <weakness #k>: <one-line summary of fix> (file:line)
- ...

## What was not fixed and why
- <weakness #k> (severity, verdict): <one-line rebuttal>
- ...

## Residual weaknesses needing your decision
- <weakness #k>: <reason auto-fix declined — e.g. cost too high, statement change>
  - Reviewer's claim: <verbatim>
  - Proposed fix: <description>
  - Your call.

## Iteration trace
- See `.proof-research/review-iteration-1.md` ... `review-iteration-<N>.md`.
```

This report is what the user sees. It is the only audit surface for the loop. Do not hide phantom-rejected weaknesses — listing them lets the user spot reviewer drift or your own over-rejection.

## Safety summary

- **Infinite loop prevention**: 3-iteration cap + convergence detection + "no fixes applied" termination. At most 3 reviewer + 3 verification rounds.
- **Quality-degradation prevention**: verification step filters reviewer noise; minimum-change principle limits scope; cost-gated decisions skip nit fixes; statement changes escalate to user.
- **Trace and rollback**: every iteration's review + decisions saved under `.proof-research/`. Compile failures roll back fixes automatically.
- **Reviewer faithfulness**: prompt explicitly forbids padding to 7, restructuring suggestions, headline changes, and uncharitable reads. "0 weaknesses" is a valid output.
