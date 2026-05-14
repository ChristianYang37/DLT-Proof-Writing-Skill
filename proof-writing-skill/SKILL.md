---
name: dlt-proof-writing
description: Write rigorous, modular mathematical proofs in LaTeX for theory papers in machine learning, statistics, and deep learning theory — covering optimization, learning theory, statistical rates, fine-grained complexity, and RL. Use when the user asks you to draft, complete, or review appendix-grade proofs — typical signals include `.tex` files with `\begin{theorem}` / `\begin{lemma}`, requests like "write the proof of ...", "fill in the appendix for ...", "prove that ...", or `\input{appendix}` patterns. Enforces a structured workflow (plan → technical reconnaissance → preliminaries → per-statement review → end-to-end audit), reference honesty, Occam's razor, and one-section-per-`.tex`-file project structure. **Does not write abstracts, introductions, related work, or conclusions** — the user owns framing; this skill owns formal content. Not for main-body exposition, pedagogical write-ups, or formal-verification (Lean / Coq) tasks.
---

# Mathematical Proof Writing in LaTeX

You are writing **appendix-grade proofs**: rigorous, modular, citation-dense, designed to be read independently of the main body. The reader is a reviewer who must be able to verify each line. The goal is **auditable correctness with disciplined exposition**, not textbook polish.

This file is the workflow. Detailed templates, conventions, checklists, and anti-patterns live in [`references/`](references/) — load them at the moments specified below, not up front. Each reference is ≤ 250 lines and stands alone; loading one does not require loading others.

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

2. **A.1 Read the task.** Re-read the user's target statement until you can recite it from memory. List inputs (assumptions, prior lemmas, allowed citations) and the precise goal (equality? inequality? high-probability? asymptotic rate?).

3. **A.2 Technical reconnaissance.** List every non-trivial *tool* the proof will need — not theorems-to-prove, but tools-to-use (matrix Bernstein, Hanson-Wright, Yarotsky gadget, elliptical-potential, Gronwall, SETH, Varshamov-Gilbert + Fano, etc.). For each tool you cannot recite precisely from memory, save a digest under `<project-root>/.proof-research/<tool-slug>.md`.

   → **Read [`references/technical-research.md`](references/technical-research.md)** for the digest schema, the sub-agent prompt, and the list of techniques that warrant digests. **Skip this step at your peril** — AI memory of advanced techniques is unreliable on hypotheses and constants.

4. **A.3 Pattern selection.** Identify the type of proof you are writing (NN convergence / non-convex landscape / fine-grained complexity / statistical rate / RL regret / etc.) and pick the organizational patterns that match.

   → **Read [`references/pattern-menu.md`](references/pattern-menu.md)** to find the row matching your proof type and adopt the listed patterns.

5. **A.4 Decompose into a dependency graph.** Build a tree of named lemmas that together imply the theorem. Aim for the **shallowest tree** that fits — three lemmas at one level beats a six-deep chain.

6. **A.5 TodoWrite + Occam pass.** One todo per lemma + one per theorem-level proof + one per end-to-end review. Then sanity-check: can any lemma be merged? Any cut? Refactor before writing.

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

6. **Update todos.** Mark this lemma complete; advance the next.

If at any step you are not confident — **stop and ask the user**. See the honesty protocol below.

### Phase C.5 — Confidence sweep

When all proofs are written and before invoking Phase D, run a confidence sweep. Every derivation step starts tagged 🔴 `from-memory`; you walk the flat list and upgrade each via fast paths (textbook inequalities, digest matches, project lemma matches) or fire-and-forget sub-agent re-derivation. Steps still 🔴 at the end get `\todo{}` markers so the Phase D reviewer prioritizes them.

→ **Read [`references/confidence-sweep.md`](references/confidence-sweep.md)** for the tag taxonomy, the trace-file schema, the fast-path / sub-agent decision table, the sub-agent prompt template, and the termination conditions. Skip this phase only for Quick-scope tasks.

### Phase D — End-to-end review

When all lemmas and the theorem proof are written:

1. **Run the LaTeX compilation gate** — fix every `Undefined control sequence`, `Reference undefined`, `Citation undefined`, `Multiply defined labels`, then open the rendered PDF and spot-check cross-reference rendering. Details in [`references/quality-checks.md`](references/quality-checks.md) §LaTeX compilation gate. A non-compiling proof is a draft, not a proof.

2. **Run the bounded review loop.** Spawn a reviewer sub-agent to produce a peer-review-style assessment (Summary / Strengths / Weaknesses / Questions / Verdict), then point-by-point verify each weakness, apply minimum-change fixes, and iterate. Loop terminates by `accept-as-is` verdict, 3-iteration cap, convergence detection, no-fixes-applied, or statement-change escalation.
   → **Read [`references/review-loop.md`](references/review-loop.md)** for the reviewer prompt, verification taxonomy (REAL-blocking / REAL-nonblocking / PHANTOM / INTENTIONAL), cost-gated fix decisions, and termination conditions.

3. **Grep your own proof against [`references/anti-patterns.md`](references/anti-patterns.md)** — especially §AI-specific failure modes. Fabricated citations, hallucinated lemma applications, and confident interpolation over missing arguments are the failure modes you will produce most often; they are also the ones that get past you most easily.

4. **Surface the final report.** Once the loop exits, deliver the structured report (what was fixed, what was rebutted, what needs user decision) per [`references/review-loop.md`](references/review-loop.md) §Final report to user.

## Honesty protocol

You will hit moments of genuine uncertainty. The correct action is **always to pause**, never to bluff.

- **Mathematical uncertainty.** If unsure that an inequality is valid, a cited lemma applies, a substitution is legal, or an asymptotic dominates — ask. Do not invent a justification.
- **Scope uncertainty.** If the user asks you to prove $X$ but you suspect $X$ is false under the stated assumptions, surface this. Offer alternative statements you can prove and let the user decide.
- **Notation uncertainty.** If the project uses an unfamiliar symbol or macro, `grep` for its definition or ask; do not assume.
- **Reference uncertainty.** If you cite a paper you have not read or a theorem number you cannot verify, write `\todo{verify: ...}` — never invent.

When asking, propose a specific path forward. Not "this seems hard, what do you want?" but: *"The constant in step (b) needs to dominate $n^{1/2}$, but the inductive hypothesis only gives $n^{1/4}$. I see two ways forward: (1) tighten the hypothesis to $n^{1/2}$ via \Cref{lem:tight}; (2) weaken the conclusion to $\Omega(n^{1/4})$. Which?"*

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

## Final-completion checklist

Before telling the user the proof is done:

- [ ] All TodoWrite items marked complete.
- [ ] End-to-end review (Phase D) ran and converged to a clean pass.
- [ ] Every `\Cref`, `\eqref`, `\cite` resolves.
- [ ] Every cited hypothesis is met at the cite-site.
- [ ] No unused definitions, assumptions, lemmas, or labels.
- [ ] Constants and parameters propagate consistently (see [`references/quality-checks.md`](references/quality-checks.md) §Constants tracking).
- [ ] Probability budgets are accounted for via explicit union bound.
- [ ] Every advanced technique used has a matching digest in `.proof-research/`, and the digest's hypotheses match the cite-site.
- [ ] Confidence sweep ran: every step in `.proof-research/confidence-trace.md` is 🟢 / 🟡, or 🔴 with a `\todo{}` marker in the .tex.
- [ ] The proof compiles (run the user's build if you can).
- [ ] AI-specific anti-patterns checked (see [`references/anti-patterns.md`](references/anti-patterns.md) §AI-specific failure modes).
- [ ] Residual uncertainties reported to the user with specific questions.

Then summarize: what was proved, which decomposition was used, which patterns were applied, and any residual items needing human judgment.
