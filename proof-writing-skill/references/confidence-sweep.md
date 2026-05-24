# Confidence sweep (Phase C.5)

Read this file at Phase C.5, after all proofs are written and before the Phase D review loop fires. The sweep adds a metacognitive layer: every derivation step starts unverified, and the sweep upgrades each step's confidence through deliberate work — fast paths for trivial steps, fire-and-forget sub-agents for steps that need independent re-derivation.

Skipping is permitted only when `.proof-research/scope.md` declares `Quick` AND `check_scope.py` agrees with that classification (see SKILL.md §Phase A.0a). For Standard / Appendix scopes the sweep is MANDATORY — Phase D gate (c), `check_confidence_tags.py`, fails closed without `confidence-trace.md`.

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

## Examples

The four entries below show every realistic upgrade path. Use them as templates when populating your own `confidence-trace.md`. Copy the structure; replace content; keep the field names verbatim — `check_confidence_tags.py` parses them.

### Example 1 — textbook inequality → 🟢 by fast path

```markdown
## Step 3
**Location:** sections/04-main-theorem.tex:128
**Content (≤ 2 lines):** $\|x + y\|^2 \le 2\|x\|^2 + 2\|y\|^2$ (Cauchy-Schwarz + AM-GM applied to $\|x+y\|^2$).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Named textbook inequality (Cauchy-Schwarz then AM-GM); hand-checked.
**Sub-agent task id:** none
**Last updated:** 2026-05-18T14:02:11Z
```

### Example 2 — citation digest matched → 🟡 by fast path

```markdown
## Step 7
**Location:** sections/03-gram-concentration.tex:54
**Content (≤ 2 lines):** $\|\hat\Sigma - \Sigma\|_{\mathrm{op}} \le \sqrt{n \log n / m}$ with prob $\ge 1 - \delta$, by matrix Bernstein (Tropp 2015, Thm 1.6).
**Initial tag:** 🔴 from-memory
**Current tag:** 🟡 cross-checked
**Verification method:** Hypotheses (mean-zero, bounded operator norm, second-moment bound) match those in .proof-research/cite-tropp2015-matrix-conc.md §Theorem 1.6; constants line up with our $R = O(1)$, $\sigma^2 = O(n)$.
**Sub-agent task id:** none
**Last updated:** 2026-05-18T14:05:42Z
```

### Example 3 — sub-agent independent re-derivation → 🟢

```markdown
## Step 12
**Location:** sections/04-main-theorem.tex:201
**Content (≤ 2 lines):** Algebra chain reducing $\|W^{(t+1)} - W^*\|_F^2 \le (1 - \eta\mu/2) \|W^{(t)} - W^*\|_F^2$, given gradient bound from Lemma 3.2.
**Initial tag:** 🔴 from-memory
**Current tag:** 🟢 verified
**Verification method:** Sub-agent re-derivation reported matches at .proof-research/sweep-step-12.md (verdict: matches). Used only the gradient bound from \Cref{lem:gradient_lb}.
**Sub-agent task id:** sweep-12-d4f3
**Last updated:** 2026-05-18T14:18:30Z
```

### Example 4 — unable-to-derive → stays 🔴 with `\todo{}` in source

```markdown
## Step 18
**Location:** sections/05-perturbation.tex:77
**Content (≤ 2 lines):** Bound on $\| \nabla L(W^{(t)}) \|_F$ via local PL inequality with constant $\mu_{\text{loc}}(\lambda_0)$.
**Initial tag:** 🔴 from-memory
**Current tag:** 🔴 from-memory
**Verification method:** Sub-agent attempted independent re-derivation; report at .proof-research/sweep-step-18.md (verdict: unable-to-derive). \todo{verify: step 18 — local PL constant} marker added at sections/05-perturbation.tex:78.
**Sub-agent task id:** sweep-18-9a21
**Last updated:** 2026-05-18T14:31:07Z
```

Note: the `\todo{verify: ...}` marker in Example 4 is what `check_confidence_tags.py` looks for when validating that every 🔴 step has been surfaced for human attention. No `\todo` → gate (c) fails.

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
