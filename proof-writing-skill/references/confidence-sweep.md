# Confidence sweep (Phase C.5)

Read this file at Phase C.5, after all proofs are written and before the Phase D review loop fires. The sweep adds a metacognitive layer: every derivation step starts unverified, and the sweep upgrades each step's confidence through deliberate work — fast paths for trivial steps, fire-and-forget sub-agents for steps that need independent re-derivation.

Skip the sweep for Quick-scope tasks. Run it for any Standard or Appendix-grade proof.

## Why this exists

AI memory of derivations looks fluent but routinely contains drift — a misplaced factor, a wrong direction in Jensen, a swapped quantifier. The Phase D reviewer catches some of these, but reviewer attention is finite and spreads thin across the whole proof. The confidence sweep is cheap defense in depth: every step gets at least a one-line classification, and any step that survives at 🔴 from-memory after the sweep gets reviewer priority (or a `\todo{}` flag for human attention).

## Tag taxonomy

| Tag | Meaning | Upgrade trigger |
|---|---|---|
| 🔴 `from-memory` | Written from LLM memory, not yet verified. **Default initial state for every step.** | (initial) |
| 🟡 `cross-checked` | Step has been matched against an external reference (technique digest, project lemma, citation digest), but not independently re-derived | Digest match, lemma-hypothesis match, citation digest match |
| 🟢 `verified` | Step has been independently re-derived, hand-computed, script-checked, or follows from a textbook fact you can name | Hand-check passed, sub-agent re-derivation matched, script validation succeeded, or named textbook inequality (Cauchy-Schwarz, AM-GM, Jensen for convex, Young's, triangle) |

## Trace file

Confidence state lives in `<project-root>/.proof-research/confidence-trace.md`. Schema for each step:

```markdown
## Step <N>
**Location:** <file>:<line>
**Content (≤ 2 lines):** <verbatim or short paraphrase>
**Initial tag:** 🔴 from-memory
**Current tag:** 🔴 | 🟡 | 🟢
**Verification method:** <one sentence>
**Sub-agent task id:** <id if delegated, else `none`>
**Last updated:** <ISO timestamp>
```

## Phase C.5 workflow

### Step 1 — Enumerate

Parse every `\begin{proof} ... \end{proof}` in the project. Each of the following counts as one step:

- One row of an `\begin{align}` / `\begin{align*}` block (a single `=` / `\leq` / `\geq` line)
- A standalone `\begin{equation}` or single-display statement
- A prose claim of the form "by <X>, we have <Y>"
- A case-split branch ("Case 1:", "Case 2:")

Skip:
- Pure assignments without inference (*"Let $x = \dots$"*)
- The opening strategy paragraph
- The closing cue (*"This completes the proof."*)

Initialize all enumerated steps to 🔴 `from-memory` in `confidence-trace.md`.

### Step 2 — Flatten to a TodoWrite list

Convert the trace into a TodoWrite list — one todo per step, content like `Verify step N: <one-line summary>`. This makes the sweep visible to the user — they see exactly which steps are being checked, and progress streams as items flip to completed.

### Step 3 — Iterate with fast-path / sub-agent dispatch

For each step still at 🔴, run a fast classification:

| Step kind | Fast path | Sub-agent? |
|---|---|---|
| Textbook inequality (Cauchy-Schwarz, AM-GM, triangle, Jensen for convex $f$, Young's) | Hand-check, upgrade 🟢 | No |
| Cites a project lemma | Re-read the lemma's hypotheses, verify they hold here, upgrade 🟡 (or 🟢 if the hypothesis check is trivial) | No |
| Cites a digest in `.proof-research/<technique>.md` | Open the digest, match this step's hypotheses against the digest's, upgrade 🟡 | No |
| Cites a citation digest in `.proof-research/cite-<author>.md` | Match the cited theorem against this step, upgrade 🟡 | No |
| Algebra chain ≥ 3 lines collapsed into one step ("by some algebra, ...") | Cannot fast-check | **Yes — fire-and-forget sub-agent** |
| Numerical claim / explicit constant | Cannot fast-check | **Yes — sub-agent** |
| Anything you wrote from memory and are not certain of | Cannot fast-check | **Yes — sub-agent** |

For sub-agent dispatch, use `Agent({..., run_in_background: true})` so the main agent keeps moving through the list. The sub-agent prompt template:

```
Re-derive the following step independently. Do NOT look at the original
derivation. Use only the listed hypotheses.

Step: <verbatim step from confidence-trace.md>
Location: <file:line>
Available hypotheses: <list of project lemmas + assumptions in scope at this point>

Report (≤ 200 words):
- your derivation (≤ 10 LaTeX lines)
- verdict ∈ {matches, constants-differ, conclusion-differs, unable-to-derive}
- if verdict ≠ matches: where the divergence is

Save report to .proof-research/sweep-step-<N>.md.
```

### Step 4 — Update tags as sub-agents return

You will be auto-notified when each sub-agent finishes. On each notification:

1. Read the sub-agent's report at `.proof-research/sweep-step-<N>.md`.
2. Update `confidence-trace.md`:
   - `matches` → upgrade to 🟢; `verification_method = "independent re-derivation matched"`
   - `constants-differ` → keep 🔴; flag as defect; surface to user with both versions
   - `conclusion-differs` → keep 🔴; flag as **critical defect**; STOP the sweep; ask user
   - `unable-to-derive` → keep 🔴; leave a `\todo{verify: step N}` in the .tex source; will route to Phase D reviewer for human attention
3. Mark the corresponding todo complete.

### Step 5 — Join and proceed

When all sub-agents have returned (you've received notifications for every dispatched task), the sweep is done. Final states:

- **All steps ≥ 🟡**: proceed to Phase D. Reviewer will scrutinize only 🟡 steps as still-suspect.
- **Some steps 🔴 with `unable-to-derive`**: proceed to Phase D, but those steps must carry a `\todo{}` marker in the .tex so the reviewer pays attention.
- **Any step `conclusion-differs`**: do NOT proceed to Phase D. Surface to user with both derivations side-by-side. Wait for instruction.

## Integration with Phase D review

The Phase D reviewer sub-agent (see [review-loop.md](review-loop.md)) takes `confidence-trace.md` as an additional input. Effects:

- Reviewer skips 🟢 steps (author-verified).
- Reviewer prioritizes 🟡 (verified-via-reference only) and 🔴 (unverifiable) steps.
- Reviewer's weakness list naturally aligns with sweep gaps, saving reviewer tokens.

## Termination conditions

- **Success**: every step is at ≥ 🟡, or 🔴-with-`unable-to-derive` is acceptable for Phase D handoff (with `\todo{}` marker).
- **Halt on defect**: any sub-agent returns `conclusion-differs` → stop, ask user.
- **Halt on suspicion**: if more than 30% of steps fail to upgrade past 🔴 in a single sweep pass, something is structurally off — surface to user before continuing to Phase D.

## Anti-patterns

- **Skipping the sweep for Standard tasks.** *"It's just one lemma, I don't need to sweep"* — wrong. The reviewer expects a clean proof; from-memory steps are exactly what makes proofs subtly incorrect.
- **Marking your own work 🟢 without independent verification.** Self-belief is not verification. The only paths to 🟢 are: named textbook inequality, sub-agent re-derivation match, or script validation.
- **Letting 🔴 steps slip into Phase D unmarked.** If a step is 🔴 after the sweep, it must have a corresponding `\todo{}` in the .tex source or an explicit user notification — never silent.
- **Treating sub-agent dispatch as serial.** The point of `run_in_background: true` is that the main agent keeps moving. If you dispatch one sub-agent and wait before dispatching the next, you waste the concurrency.
