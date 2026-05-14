# Eval runner — sub-agent prompt template

You are running **one** test case from this skill's eval suite. The skill (`dlt-proof-writing`) is installed locally at `~/.claude/skills/dlt-proof-writing/`.

## Inputs (filled in by the parent agent)

- `eval_id`, `eval_name`, `prompt`, `expected_output`, `output_dir`

## Your task

1. **Load the skill explicitly.** Read `~/.claude/skills/dlt-proof-writing/SKILL.md`. Follow its workflow.

2. **Run the FULL workflow** for the given `prompt`. **Do not skip phases** — this eval is testing the skill in its intended end-to-end use.

   - **Phase A** (plan, technical reconnaissance with digests, decompose, todos).
   - **Phase B** (preliminaries: macros with `aliascnt`, assumptions, definitions).
   - **Phase C** (statements and proofs with per-statement review).
   - **Phase C.5 — Confidence sweep**: produce `<output_dir>/.proof-research/confidence-trace.md` per [confidence-sweep.md](../references/confidence-sweep.md). Enumerate every derivation step, tag each 🔴 initially, then walk the list upgrading via fast-path (textbook inequalities → 🟢; digest match → 🟡) or fire-and-forget sub-agent re-derivation. Save the trace and any sub-agent reports to `.proof-research/`. **Do not skip this phase.**
   - **Phase D — Review loop**: run the bounded peer-review loop per [review-loop.md](../references/review-loop.md). Spawn a reviewer sub-agent that produces Summary / Strengths / Weaknesses / Questions / Verdict, verify each weakness, apply minimum-change fixes if the cost gate permits, iterate until verdict is `accept-as-is` OR the 3-iteration cap OR convergence detection fires. Save each iteration's review + your verification decisions to `<output_dir>/.proof-research/review-iteration-<N>.md`. **Do not skip this phase.**

3. **Experiment design (only if the eval prompt requests it).** If the eval prompt explicitly asks for an `experiments-plan.md`, produce it per [theory-experiment.md](../references/theory-experiment.md) — **design only, never fabricated numbers**. Save to `<output_dir>/experiments-plan.md`. If the eval does not request experiments, do not produce a plan; the proof PDF stays clean of empirical content per the conventions.

4. **Save outputs** to `<output_dir>/`:
   - `main.tex` — short, just preamble + `\input` chain + `\end{document}` (no abstract / intro).
   - `macros.tex` — `\newcommand`s + theorem environments with `\newaliascnt`.
   - `sections/01-preliminaries.tex`, `sections/02-...tex`, ... — one `.tex` per logical section per [conventions.md](../references/conventions.md) §Project file structure.
   - `refs.bib` — **only if your proof actually contains `\cite{...}` calls**. See "Citation discipline" below.
   - `.proof-research/` — technique / citation digests + `confidence-trace.md` + `review-iteration-<N>.md` files.
   - `experiments-plan.md` — only if the eval asks for experiments.
   - `runner-log.md` — see schema below.

5. **Self-check before declaring done**:
   - Run `python ~/.claude/skills/dlt-proof-writing/scripts/lint.py <output_dir>/main.tex <output_dir>/macros.tex <output_dir>/sections/*.tex --bib <output_dir>/refs.bib` if a .bib exists; otherwise drop `--bib`. Address every `error`.
   - Run `python ~/.claude/skills/dlt-proof-writing/scripts/latexmk-wrapper.py <output_dir>/main.tex --outdir <output_dir>/.output` and confirm `compile_ok: true`.

## Hard constraints

### Citation discipline (eval-2-v1 failure mode)

- If your proof has any `\cite{...}` call, you **must** ship a `refs.bib` file with that key resolved (via citation digest, see [technical-research.md](../references/technical-research.md)).
- If you cannot verify a citation, replace `\cite{author2020something}` with `\todo{verify: <claim attributed to author2020something>}`.
- **Never** ship a `\cite{}` to a key not in the project's `.bib`. The skill's anti-patterns explicitly forbid this; eval grading flags every unresolved cite as a critical defect.

### Incremental build (eval-2-v1 failure mode)

- **Write a section file BEFORE you add its `\input{}` line to `main.tex`.** If you list `\input{sections/06-foo}` but the file doesn't exist, the project is broken — a quota cutoff or interruption leaves an uncompileable state.
- After each new section, save main.tex and check compile.

### Theorem ↔ proof pairing (lint R5)

Every `\begin{theorem}` / `\begin{lemma}` / `\begin{proposition}` / `\begin{corollary}` / `\begin{claim}` must satisfy exactly one of:

1. **Immediate proof in same file** — the FIRST environment after `\end{X}` must be `\begin{proof}` (whitespace, comments, and `\label{}` outside an env are allowed between; **other environments are not** — no intervening `\begin{remark}` / `\begin{lemma}` / etc.).
2. **Citation in optional bracket** — `\begin{X}[\cite{authoryear}]`, key resolves in `refs.bib`.

**Practical file layout:** put theorem + proof in the SAME `.tex` file. Do NOT split into `02-main-result.tex` (theorem) + `06-proof-of-main.tex` (proof) — that violates R5. Layout:

```
sections/
├── 01-preliminaries.tex     # definitions / assumptions / cited facts
├── 02-lemma-A.tex           # \begin{lemma} + \begin{proof}
├── 03-lemma-B.tex           # same
├── 04-main-theorem.tex      # main \begin{theorem} + \begin{proof}
└── 99-auxiliary.tex         # cited externals (\begin{X}[\cite{...}])
```

See [conventions.md](../references/conventions.md) §Theorem ↔ proof pairing. Run `scripts/lint.py` after every section write — R5 violations are errors.

### Workflow phases

- Run all of A, B, C, C.5, D. The eval explicitly tests the FULL workflow. Skipping C.5 or D defeats the purpose of the test.
- If Phase D loop runs 3 iterations without converging, save the final review and stop (the loop's own termination condition). Document the residual weaknesses in `runner-log.md`.

### Other

- Apply skill conventions strictly: aliascnt theorem-env preamble, `Eq.~\eqref{...}`, no `\[ ... \]`, one section per `.tex` file, no abstract/intro.
- `\todo{verify: ...}` is encouraged over silent gaps. The grader rewards honesty.
- **Do not fabricate experimental results.** If the eval asks for experiments, produce a PLAN with `## Results` left blank.
- **Do not fabricate self-reported metrics.** The runner has no clock — do not report "minutes used" or invented timing breakdowns. See `runner-log.md` schema below.

## `runner-log.md` schema

```markdown
# Runner log — <eval_name>

## What I built
One paragraph: what the headline theorem says, how it's decomposed (which lemmas), which derivation pattern, which organizational pattern from pattern-menu.md.

## Patterns chosen
- Statement template: <two-tier / restated / condition-list / decomposed-bound>
- Derivation pattern: <one of §5.1–5.5 from templates.md>
- Organizational pattern: <from pattern-menu.md>

## Phase C.5 — Confidence sweep summary
- Steps enumerated: <N>
- After sweep: <N_green> 🟢 / <N_yellow> 🟡 / <N_red> 🔴
- Sub-agents fired: <count>; reports saved to .proof-research/sweep-step-<N>.md
- Any 🔴 with `unable-to-derive` (and corresponding `\todo{}` in .tex): <list>

## Phase D — Review loop summary
- Iterations: <N> (max 3)
- Final verdict: accept-as-is | accept-with-minor-revisions | major-revision-required | reject-as-flawed
- Weaknesses per iteration: <N_1>, <N_2>, ...
- Fixes applied per iteration: <N_1>, <N_2>, ...
- Termination reason: <accept-as-is | 3-iter cap | convergence stall | no-fixes | statement-change escalation>
- Iteration files in .proof-research/review-iteration-1.md, ..., review-iteration-<N>.md

## Where I had to make calls
Bullet list of nontrivial decisions (math judgments, convention choices, what to keep vs. push to remarks).

## Self-check results
- lint.py errors: <N> (list any remaining)
- latexmk compile_ok: <true / false>
- Cite-key check: every \cite{...} resolves in refs.bib? <yes/no/no-cites-used>
- All \input'd section files exist on disk? <yes/no>

## What's incomplete
Honest list of gaps, `\todo{}` items, deferred elaborations. The grader prefers an honest stub over a polished hallucination.
```

**Note: no "Time budget" or "minutes used" fields.** You have no clock. Do not invent timing data.

## Deliverable

The `<output_dir>/` directory with all files plus a brief summary message (≤ 300 words) describing: theorem proved, decomposition, Phase C.5 outcome (red/yellow/green counts), Phase D outcome (iterations + verdict), and residual `\todo` items. The grader will read your files directly.
