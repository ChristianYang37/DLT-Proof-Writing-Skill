---
name: dlt-proof-writing
description: Write rigorous, modular mathematical proofs in LaTeX for theory papers in machine learning, statistics, and deep learning theory — covering optimization, learning theory, statistical rates, fine-grained complexity, and RL. Use when the user asks you to draft, complete, or review appendix-grade proofs — typical signals include `.tex` files with `\begin{theorem}` / `\begin{lemma}`, requests like "write the proof of ...", "fill in the appendix for ...", "prove that ...", or `\input{appendix}` patterns. Enforces a structured workflow (plan → technical reconnaissance → preliminaries → per-statement review → end-to-end audit), reference honesty, Occam's razor, and one-section-per-`.tex`-file project structure. **Does not write abstracts, introductions, related work, or conclusions** — the user owns framing; this skill owns formal content. Not for main-body exposition, pedagogical write-ups, or formal-verification (Lean / Coq) tasks.
---

# Mathematical Proof Writing in LaTeX

You are writing **appendix-grade proofs**: rigorous, modular, citation-dense, designed to be read independently of the main body. The reader is a reviewer who must be able to verify each line. The goal is **auditable correctness with disciplined exposition**, not textbook polish.

This file is the workflow. Detailed templates, conventions, checklists, and anti-patterns live in [`references/`](references/) — load them at the moments specified below, not up front. Each reference is ≤ 250 lines and stands alone; loading one does not require loading others.

## Non-negotiables — read every session

These three rules are enforced by scripts, not by your judgment. If a script flips red, you stop and fix — you do not proceed.

1. **All LaTeX compile artifacts live under `<project-root>/.output/`.** The only sanctioned compile path is `python <skill>/scripts/latexmk-wrapper.py main.tex --outdir <project-root>/.output`. Parse the JSON output: `compile_ok` MUST be `true` and `overfull_violations` MUST be empty (> 50pt threshold). The script returns exit code 1 on any failure — react to it. (Belt-and-braces: copy `<skill>/settings.recommended.json` into `<project-root>/.claude/settings.json` so a PreToolUse hook blocks any PDF/AUX/LOG written outside `.output/`.)

2. **Three Phase-D gates MUST all return exit 0 before the review loop runs.** Run them in order; do not enter the review loop with a red gate.

   ```bash
   python <skill>/scripts/latexmk-wrapper.py main.tex --outdir <root>/.output  # gate (a)
   python <skill>/scripts/lint.py main.tex macros.tex sections/*.tex --bib refs.bib  # gate (b)
   python <skill>/scripts/check_confidence_tags.py <root>  # gate (c)
   ```

3. **Every claim carries its evidence.** Every `\cite{key}` must have a matching `.proof-research/cite-<key>-*.md` digest (else: lint R13 errors). Every non-trivial technique invoked in a proof must have `.proof-research/<technique>.md` (else: R14). Every derivation step in the project must appear in `.proof-research/confidence-trace.md` with a 🔴 / 🟡 / 🟢 tag (else: `check_confidence_tags.py` fails). Every `1-\delta` in a theorem statement must be discharged by an explicit union-bound paragraph in its proof (else: R17). Every bare `$C$` / `$c$` requires the universal-constant declaration somewhere in the project (else: R15).

4. **`main.tex` is the entry, not the body.** `main.tex` must contain ONLY: `\documentclass`, `\usepackage` lines, `\input{macros}`, optional `\title` / `\author` / `\date`, `\begin{document}`, an `\input{sections/NN-*}` chain, optional `\bibliographystyle` / `\bibliography`, `\end{document}`. **No theorem-like environments, no proof environments, no abstract, no inline prose.** Every statement and every proof lives in `sections/NN-<slug>.tex`. Lint R18 errors on any `\begin{theorem|lemma|proposition|corollary|claim|definition|assumption|fact|remark|proof|abstract}` inside the file containing `\documentclass`.

If you cannot satisfy a rule yet, write `\todo{verify: ...}` and surface to user. **Do not silently continue.**

## Scripts — sanctioned tooling

These scripts live at `<skill>/scripts/`. SKILL.md is the only place they are listed; if a tool is not in this table, it does not exist.

| Script | Purpose | When |
|---|---|---|
| `latexmk-wrapper.py` | Compile + structured-JSON log parse + exit 1 on errors / overfull > 50pt | Phase D gate (a); use as the only compile path |
| `lint.py` | Static rules R0a–R18 over `.tex` files (style, R0c aliascnt, R13 cite-digest, R14 technique-digest, R15 constants, R17 union-bound, R18 no-inline-in-main) | After every section write + Phase D gate (b) |
| `check_confidence_tags.py` | Validates `.proof-research/confidence-trace.md` covers ≥ 50% of estimated steps and every 🔴 has a `\todo{verify}` marker | Phase D gate (c) |
| `check_scope.py` | Validates `.proof-research/scope.md` declaration matches project size (closes the "I'll just say Quick to skip Phase D" loophole) | Phase A.0a |
| `hook_output_guard.py` | Invoked by Claude Code PreToolUse hook (auto, via `settings.recommended.json`) — blocks PDF/AUX/LOG writes outside `.output/` | Automatic |

## Core principles

These are mindset, not procedure. Re-read before every session.

1. **Occam's razor.** No definition unused, no lemma uninvoked, no assumption non-load-bearing. Every entity must justify its existence in the dependency graph. If you can delete it, delete it.
2. **Honesty over output.** If you are unsure a step is correct, a constant is tight, a lemma applies, or an assumption suffices — **stop and ask the user**. A halted proof is more useful than a wrong one.
3. **Never fabricate references.** Every `\cite{key}` must resolve in the project's `.bib`. Every "Theorem 3.1 of [Smith23]" must be verified. If you cannot verify, write `\todo{verify reference: ...}` rather than guess. This is the single highest-severity failure mode for AI-written proofs.
4. **Co-pilot, not autopilot.** The user owns the mathematics. You own structure, exposition, and bookkeeping. Surface nontrivial choices (constant tuning, hypothesis selection, citation choice) for confirmation rather than deciding silently.
5. **Audit first, polish later.** Prefer a slightly verbose, fully-justified derivation to a compact one. You can prune in review; you cannot recover correctness from missing justification.

## Workflow

Four phases. Do not skip; do not reorder.

### Phase A — Plan

1. **A.0 Read the project.** Locate `math_macros.tex` / `preamble.tex`, the `.bib`, and one or two existing chapters. Inventory existing macros and theorem environments. Note the project's `\Cref` vs. `\ref` style, label-prefix conventions, and citation-key style.

   → **Read [`references/conventions.md`](references/conventions.md)** if any of these are unclear or you are setting up new conventions for a fresh project. Project conventions outrank everything in that file.

   Then create the working directories and gitignore the build output:

   ```bash
   mkdir -p <project-root>/.proof-research <project-root>/.output
   grep -qxF .output/ <project-root>/.gitignore 2>/dev/null \
     || echo .output/ >> <project-root>/.gitignore
   ```

2. **A.0a Scope declaration.** Classify the task and write a single word to `<project-root>/.proof-research/scope.md`:

   - **Quick** — single lemma, ≤ 5 derivation steps, no probability parameter δ.
   - **Standard** — 1–3 lemmas + 1 theorem; OR a probabilistic statement; OR 5–30 derivation steps.
   - **Appendix** — ≥ 3 lemmas, paper-level proof, or > 30 steps.

   Then validate: `python <skill>/scripts/check_scope.py <project-root>` must exit 0. The validator blocks declaring **down** (calling something Quick that is actually Standard / Appendix) — this is the most common abuse path because it lets you skip Phase C.5 and Phase D. **Phase C.5 and Phase D are MANDATORY for Standard and Appendix scopes** — only Quick can skip them, and even then only after the validator agrees.

3. **A.1 Read the task.** Re-read the user's target statement until you can recite it from memory. List inputs (assumptions, prior lemmas, allowed citations) and the precise goal (equality? inequality? high-probability? asymptotic rate?).

3. **A.2 Technical reconnaissance.** List every non-trivial *tool* the proof will need — not theorems-to-prove, but tools-to-use (matrix Bernstein, Hanson-Wright, Yarotsky gadget, elliptical-potential, Gronwall, SETH, Varshamov-Gilbert + Fano, etc.). For each tool you cannot recite precisely from memory, save a digest under `<project-root>/.proof-research/<tool-slug>.md`.

   → **Read [`references/technical-research.md`](references/technical-research.md)** for the digest schema, the sub-agent prompt, and the list of techniques that warrant digests. **Skip this step at your peril** — AI memory of advanced techniques is unreliable on hypotheses and constants.

4. **A.3 Pattern selection.** Identify the type of proof you are writing (NN convergence / non-convex landscape / fine-grained complexity / statistical rate / RL regret / etc.) and pick the organizational patterns that match.

   → **Read [`references/pattern-menu.md`](references/pattern-menu.md)** to find the row matching your proof type and adopt the listed patterns.

5. **A.4 Decompose into a dependency graph.** Build a tree of named lemmas that together imply the theorem. Aim for the **shallowest tree** that fits — three lemmas at one level beats a six-deep chain.

6. **A.5 TodoWrite + Occam pass with verifiable output.** Write `<project-root>/.proof-research/dependency-graph.md` listing every lemma. For each lemma, the entry MUST contain a `Downstream consumers:` field naming the cite-sites that depend on it (other lemmas / the theorem). Schema:

   ```markdown
   ## lem:gradient_lb
   **Statement (1-line):** ...
   **Hypotheses:** ass:data, ass:init
   **Downstream consumers:** thm:main (cite-site §4 step 3), lem:contraction
   ```

   If a lemma's `Downstream consumers:` is empty, the lemma MUST be deleted or merged before drafting — there is no "we'll use it later" exception. Then create one `TodoWrite` item per surviving lemma + one per theorem proof + one per end-to-end review.

7. **A.6 Surface ambiguity.** If any input is unclear (which norm, which probability space, tight constants vs. `\poly` slack), ask the user before drafting.

### Phase B — Preliminaries

Set up the proof environment before any lemma body:

1. **Notation block** — list new symbols not already in the main paper.
2. **Definitions** — `\begin{definition}[Short Name]\label{def:slug}`, one object per environment.
3. **Assumptions** — `\begin{assumption}[Short Name]\label{ass:slug}`, each followed by **one** `\begin{remark}` discussing mildness, related work, weakenability. Discussion lives in the remark, never inside the assumption.
4. **Facts and external lemmas** — lightweight `\begin{fact}` for trivial restatements; `\begin{lemma}[\cite{authoryear}]` to restate external lemmas the proof invokes repeatedly.

→ **Read [`references/templates.md`](references/templates.md)** before writing any `\begin{definition}` or `\begin{assumption}` block for the first time in this project.

Then run the per-statement review (see Phase C step 2).

### Phase C — Statements and proofs

For each node in the dependency graph, in topological order (leaves first):

1. **State the lemma.**
   → **Read [`references/templates.md`](references/templates.md) §Statement templates** if you are writing a new kind of statement (two-tier informal/formal, condition-list, decomposed-bound). Pick one template per project and apply uniformly.

2. **Run per-statement review.**
   → **Read [`references/quality-checks.md`](references/quality-checks.md) §Per-statement** the first time you do this in a session; the seven items become memorable after a few uses.

3. **If the proof invokes a technique you researched in A.2**, open the digest in `.proof-research/` first. **Do not write the derivation from memory.**

4. **Write the proof.** Pick one derivation pattern (trailing-justification block, inline tags, letter-tagged with legend, decompose-and-conquer, or successful-event conditioning) and apply uniformly within the proof.
   → **Read [`references/templates.md`](references/templates.md) §Derivation patterns** before your first non-trivial derivation in this project.

5. **Run per-proof review.**
   → **Read [`references/quality-checks.md`](references/quality-checks.md) §Per-proof** for the nine-item checklist. The most common silent bug is item 3: citing a lemma whose hypotheses are not actually met at the cite-site.

6. **Run incremental lint.** After every section write:

   ```bash
   python <skill>/scripts/lint.py <changed-file.tex> --bib <project>/refs.bib
   ```

   Fix every reported error (R0a–R17) before continuing. R13/R14 will fire as soon as you write a `\cite{}` or invoke a technique without the corresponding `.proof-research/` digest — this is the intended workflow, not nuisance noise.

7. **`\input{}` ordering rule.** When introducing a new section file: write the `.tex` file FIRST (with at least placeholder content), then add the `\input{sections/NN-foo}` line to `main.tex`. Reversed order leaves a non-compilable repo on interruption.

8. **Update todos.** Mark this lemma complete; advance the next.

If at any step you are not confident — **stop and ask the user**. See the honesty protocol below.

### Phase C.5 — Confidence sweep

When all proofs are written and before invoking Phase D, run a confidence sweep. Every derivation step starts tagged 🔴 `from-memory`; you walk the flat list and upgrade each via fast paths (textbook inequalities, digest matches, project lemma matches) or fire-and-forget sub-agent re-derivation. Steps still 🔴 at the end get `\todo{}` markers so the Phase D reviewer prioritizes them.

→ **Read [`references/confidence-sweep.md`](references/confidence-sweep.md)** for the tag taxonomy, the trace-file schema, the fast-path / sub-agent decision table, the sub-agent prompt template, and the termination conditions. Skipping this phase is permitted only when `.proof-research/scope.md` declares `Quick` AND `check_scope.py` exits 0 confirming that classification — see Phase A.0a. For Standard / Appendix scope this phase is MANDATORY; Phase D gate (c) (`check_confidence_tags.py`) will fail otherwise.

### Phase D — End-to-end review

When all lemmas and the theorem proof are written:

1. **Three gates — every gate MUST return exit 0 before the review loop.** Run them in order:

   ```bash
   # Gate (a) — compile + structured log
   python <skill>/scripts/latexmk-wrapper.py main.tex --outdir <root>/.output
   # → exit 0 + JSON shows compile_ok=true + overfull_violations=[]

   # Gate (b) — static rules
   python <skill>/scripts/lint.py main.tex macros.tex sections/*.tex --bib refs.bib
   # → exit 0 (R0a–R17 all pass)

   # Gate (c) — confidence sweep coverage
   python <skill>/scripts/check_confidence_tags.py <root>
   # → exit 0 (every step tagged, every 🔴 has \todo{verify})
   ```

   If any returns non-zero, fix and re-run. A non-compiling proof is a draft, not a proof; a proof with unaddressed lint errors is unreviewable; a proof without a confidence sweep is from-memory. R0c statically prevents the aliascnt counter-share bug, so visual PDF spot-checking is no longer required. See [`references/quality-checks.md`](references/quality-checks.md) §LaTeX compilation gate for the underlying rationale of each gate.

2. **Run the bounded review loop.** Spawn a reviewer sub-agent to produce a peer-review-style assessment (Summary / Strengths / Weaknesses / Questions / Verdict), then point-by-point verify each weakness, apply minimum-change fixes, and iterate. Loop terminates by `accept-as-is` verdict, 3-iteration cap, convergence detection, no-fixes-applied, or statement-change escalation.
   → **Read [`references/review-loop.md`](references/review-loop.md)** for the reviewer prompt, verification taxonomy (REAL-blocking / REAL-nonblocking / PHANTOM / INTENTIONAL), cost-gated fix decisions, and termination conditions.

3. **Grep your own proof against [`references/anti-patterns.md`](references/anti-patterns.md)** — especially §AI-specific failure modes. Fabricated citations, hallucinated lemma applications, and confident interpolation over missing arguments are the failure modes you will produce most often; they are also the ones that get past you most easily.

4. **Surface the final report.** Once the loop exits, deliver the structured report (what was fixed, what was rebutted, what needs user decision) per [`references/review-loop.md`](references/review-loop.md) §Final report to user.

## Honesty protocol — objective triggers

"If unsure" is too vague — LLMs almost never feel unsure. This protocol uses **mechanical triggers** instead. When ANY of these is true, you MUST `\todo{verify: ...}` the offending step AND surface to the user (do not silently continue):

- Writing `\cite{key}` without a matching `.proof-research/cite-<key>-*.md` digest on disk (lint R13 will catch this — but the protocol comes first).
- Invoking a technique listed in [`references/technical-research.md`](references/technical-research.md) §Examples without a corresponding `.proof-research/<slug>.md` digest (R14).
- Introducing a constant `$C$` / `$c$` / `$C_n$` without either (a) the universal-constant declaration earlier in the project (R15), or (b) explicit dependency notation like `$C_{\lambda_0, L, d}$`.
- A `1-\delta` appears in a theorem conclusion before a union-bound paragraph has been written (R17).
- You cannot **name** the specific inequality, lemma, or arithmetic fact justifying a step (e.g. "by some algebra" / "it follows easily" / "by standard concentration" without specifying which).
- A case-split says "the other case is similar" but the cases actually use different machinery (R16).
- A scope assumption you suspect is unsatisfied at the cite-site of a `\Cref{lem:X}`.
- The user asked you to prove $X$ but you suspect $X$ is false / not provable under the stated assumptions.
- Project notation uses a macro you cannot `grep` to a definition.

When pausing to ask, propose a specific path forward. Not "this seems hard, what do you want?" but: *"The constant in step (b) needs to dominate $n^{1/2}$, but the inductive hypothesis only gives $n^{1/4}$. I see two ways forward: (1) tighten the hypothesis to $n^{1/2}$ via \Cref{lem:tight}; (2) weaken the conclusion to $\Omega(n^{1/4})$. Which?"*

Most of these triggers are also lint-enforced (R13–R17), so the protocol is the rule and lint is the safety net. Lint catching them after the fact is a lagging signal — the honesty protocol means you do not write them in the first place.

## References — when to load each

| File | When to load | Why |
|---|---|---|
| [`references/conventions.md`](references/conventions.md) | Phase A.0 (first contact with project) | macros, label slugs, `\Cref` vs `\ref`, asymptotic notation, voice |
| [`references/technical-research.md`](references/technical-research.md) | Phase A.2 (technical reconnaissance) | digest schema, sub-agent prompt, list of digest-worthy techniques |
| [`references/pattern-menu.md`](references/pattern-menu.md) | Phase A.3 (pattern selection) | proof-type → recommended organizational patterns |
| [`references/templates.md`](references/templates.md) | Phase B (preliminaries) and Phase C (each new statement / derivation) | LaTeX templates for statements, derivation patterns, proof boundaries |
| [`references/quality-checks.md`](references/quality-checks.md) | Phase C (per-statement / per-proof review) and Phase D (end-to-end) | the three checklists, constants tracking, compilation gate, end-to-end review |
| [`references/confidence-sweep.md`](references/confidence-sweep.md) | Phase C.5 (after all proofs written, before Phase D) | tag taxonomy, trace schema, sub-agent dispatch, fast-path / re-derivation decisions |
| [`references/anti-patterns.md`](references/anti-patterns.md) | Phase C (after writing a derivation) and Phase D (final pass) | math anti-patterns, exposition anti-patterns, AI-specific failure modes |
| [`references/review-loop.md`](references/review-loop.md) | Phase D (after compilation gate passes) | reviewer sub-agent prompt, verification taxonomy, fix-cost decisions, loop termination |
| [`references/theory-experiment.md`](references/theory-experiment.md) | only if the user explicitly asks for experiments | how to design ICML/NeurIPS/ICLR-grade empirical validation as a separate `experiments-plan.md`; **never fabricate results, never pollute `main.tex` with experiment sections** |

Load on demand. Do not load up front.

## Final-completion checklist — MUST paste into your final message

Before declaring the proof done, paste this block verbatim into your final message to the user and replace each `[ ]` with `[✅]` / `[❌]` plus a one-line evidence string (file:line, command output, `n/a — reason`, or `\todo{}` location). A bare "all done" is not an acceptable completion message.

```markdown
- [ ] Phase D gate (a): `latexmk-wrapper.py` exit 0, `compile_ok=true`, `overfull_violations=[]`
  Evidence: <command output excerpt>
- [ ] Phase D gate (b): `lint.py` exit 0 across all `.tex` files
  Evidence: <command output excerpt>
- [ ] Phase D gate (c): `check_confidence_tags.py` exit 0
  Evidence: <command output excerpt>
- [ ] `.proof-research/scope.md` declared; `check_scope.py` exit 0
  Evidence: <declared scope> matches <suggested>
- [ ] `.proof-research/dependency-graph.md` lists every surviving lemma with non-empty `Downstream consumers`
  Evidence: <count of lemmas, count of consumers>
- [ ] Every `\cite{key}` has `.proof-research/cite-<key>-*.md` (auto: R13)
  Evidence: R13 violations = 0
- [ ] Every non-trivial technique used has `.proof-research/<technique>.md` (auto: R14)
  Evidence: R14 violations = 0
- [ ] Bare-constant convention satisfied (auto: R15) OR explicit `% lint: ignore R15` annotations listed
  Evidence: R15 violations = 0
- [ ] Every `1-\delta` discharged by an explicit union-bound paragraph (auto: R17)
  Evidence: R17 violations = 0
- [ ] All `\input{}` targets exist on disk
  Evidence: list of \input targets
- [ ] Review loop converged
  Evidence: <iteration count> · <final verdict>
- [ ] Residual `\todo{}` markers enumerated with one-line context each
  Evidence: <count> markers; locations: <list>
- [ ] AI-specific anti-patterns swept ([`references/anti-patterns.md`](references/anti-patterns.md) §AI-specific failure modes)
  Evidence: which patterns checked, what was found
```

After the checklist, summarize: what was proved, which decomposition was used, which patterns were applied, and any residual items needing human judgment.
