# Quality checks

Read this file twice during writing: once after every new statement (per-statement checklist), once after every proof body (per-proof checklist + constants tracking). Read it again at Phase D for the end-to-end review.

## Contents

1. [Per-statement review checklist](#per-statement-review-checklist) — run after each `\begin{theorem}/\begin{lemma}/...`
2. [Per-proof review checklist](#per-proof-review-checklist) — run after each `\begin{proof} ... \end{proof}`
3. [Constants and parameter dependency tracking](#constants-and-parameter-dependency-tracking) — applies throughout
4. [LaTeX compilation gate](#latex-compilation-gate) — before declaring any phase complete
5. [End-to-end review](#end-to-end-review) — Phase D

---

## Per-statement review checklist

After writing each `\begin{definition} / \begin{assumption} / \begin{lemma} / \begin{theorem} / \begin{proposition} / \begin{corollary}` — before its proof — check:

1. **Necessity.** Does the dependency graph require this statement? If you cannot point to a downstream consumer, delete it.
2. **Self-containment.** Can a reader who lands on this environment alone understand what is being claimed? Are all symbols either defined inline or referenced by `\Cref` to their definition?
3. **Quantifier order.** Are existential and universal quantifiers in the right order? Read the statement aloud to check.
4. **Probability budget.** If the statement is high-probability, is the failure probability explicit ("with probability at least $1 - \delta$")? Is it consistent with the union bounds you will pay downstream?
5. **Hypothesis tightness.** Are the hypotheses the *minimum* needed for the conclusion? Strengthening assumptions to shorten a proof is a refactor, not progress.
6. **Short-title quality.** The optional `[Short Title]` should be a noun phrase ≤ 5 words naming the *thing being claimed*, not the technique used.
7. **Label sanity.** Label matches the slug convention (see [conventions.md](conventions.md)). Label is unique in the project.

If anything fails, fix before proceeding. If anything is uncertain, ask the user.

## Per-proof review checklist

After writing each `\begin{proof} ... \end{proof}`, check:

1. **Opening.** First sentence states the strategy in one line.
2. **Every cited object resolves.** Every `\Cref` / `\eqref` / `\cite` points at something that exists in the project.
3. **Every cited hypothesis is satisfied.** When you invoke `\Cref{lem:X}`, are the hypotheses of Lemma X actually met at this point in the proof? **This is the most common silent bug.**
4. **Every derivation step has a justification.** No display equation is allowed to dangle without prose or tag.
5. **Step count matches trailer count.** If the trailer says "the first ... the second ... the last", ordinals correspond one-to-one with visible relation rows. Recount manually.
6. **No used-but-undefined symbols.** Every symbol on the right-hand side of any display was defined upstream.
7. **No unused intermediate result.** If you proved a sub-claim and never used it, delete or move to a separate lemma.
8. **Probabilistic statements remain coherent.** High-probability events compose; expectations and almost-sure statements are not silently substituted.
9. **Closure.** Final sentence is a closing cue ("This completes the proof.", "as desired.", `\qed`). The proof exits via `\end{proof}`.

If anything fails, fix. If uncertain, ask.

---

## Constants and parameter dependency tracking

NN-convergence and statistical-rate proofs frequently fail silently because a constant changes its dependency mid-proof — e.g., a lemma proves `$\|W^{(t)}\| \le C$` where $C$ depends on $\lambda_0$, but the theorem then treats $C$ as a universal constant. Every reviewer hits this. Defend against it:

- **State the universal-constant convention exactly once** in the notation block:
  *"Throughout, $c, C, C_1, C_2, \ldots$ denote universal positive constants whose values may change from line to line and depend only on quantities specified in each lemma's hypothesis."*
  Then *use* this convention — do not introduce additional unnamed constants downstream.

- **Name every problem-dependent constant.** If a constant depends on $\lambda_0, L, d$, write it `$C_{\lambda_0, L, d}$` or `$c(\lambda_0, L, d)$`, never just `$C$`. Make the dependency visible at the symbol level.

- **Track the dependency chain.** When Lemma A produces `$C_A = C_A(\lambda_0)$` and Lemma B uses it, Lemma B's conclusion is implicitly `$C_B = C_B(\lambda_0)$` even if you wrote just `$C_B$`. Walk the chain explicitly when you assemble.

- **Width / sample / step-size requirements compose multiplicatively.** If Lemma A requires `$m \ge n^4/\lambda_0^2$`, Lemma B requires `$m \ge n^5 \log m$`, Lemma C requires `$m \ge d^3/\delta$`, the theorem must require the *maximum* — write `$m \ge \max\{ n^4/\lambda_0^2,\, n^5 \log m,\, d^3/\delta \}$` or merge into a single dominating `\poly` expression. Do not silently drop subsidiary requirements.

- **Union-bound budget.** If you prove $k$ high-probability events each at failure $\delta/k$, the theorem statement must use $\delta$ (not $\delta/k$). When in doubt, write out the union bound explicitly: *"By a union bound over \Cref{lem:A,lem:B,lem:C}, all three events hold with probability at least $1 - 3 \cdot \delta/3 = 1 - \delta$."* **Lint R17 enforces this**: a theorem statement containing `1-\delta` whose proof body lacks any union-bound paragraph triggers a hard error. Suppress with `% lint: ignore R17 — <reason>` only when the bound is established in a separate file.

> **Lint R15 enforces the bare-constant discipline.** If no file in the project declares the universal-constant convention (the *"Throughout, $c, C, C_1, \ldots$ denote universal positive constants ..."* sentence), any bare `$C$` / `$c$` / `$C_n$` triggers R15. Either add the declaration to the notation block, annotate the constant with explicit dependency (e.g. `$C_{\lambda_0, L, d}$`), or suppress per-line via `% lint: ignore R15 — <reason>`. Do not bypass the rule without a written reason — bare constants drifting into problem-dependent meaning is the #1 silent bug in NN-convergence proofs.

---

## LaTeX compilation gate

A proof that does not compile is not a proof — it is a draft. The compile is enforced through **Phase D gate (a)** in SKILL.md, which is now the only sanctioned compile path:

```bash
python <skill>/scripts/latexmk-wrapper.py main.tex --outdir <project-root>/.output
```

The wrapper:

1. **Runs `latexmk` (preferred) or falls back to `pdflatex`**, with output redirected to `.output/`. Build artifacts (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.pdf`) stay out of the project root — they belong in `.output/` and `.gitignore` (the gitignore step is handled by SKILL.md Phase A.0).

2. **Parses the log into structured JSON** with fields `compile_ok`, `undef_refs`, `undef_cites`, `mult_labels`, `undef_macros`, `errors`, `overfull_hbox_pts`, `overfull_violations` (boxes exceeding `--overfull-threshold`, default 50pt). All of the following flip `compile_ok` to `false`:
   - `Undefined control sequence` — macro used before it is defined.
   - `Reference ... undefined` — `\ref`/`\eqref`/`\Cref` points at a nonexistent label (caught here AND statically by R5).
   - `Citation ... undefined` — `\cite` key not in `.bib` (caught here AND by R12 / R13).
   - `Multiply defined labels` — two `\label{}` with the same slug (caught here AND by R4).
   - `Overfull/Underfull \hbox` exceeding 50pt — fix display sizing.

3. **Returns exit code 1** when `compile_ok=false`. The non-zero exit IS the signal — react to it. Phase D gate (a) requires exit 0.

The previous version of this gate told you to *"open the rendered PDF and spot-check cross-reference rendering"* to catch the silent aliascnt counter-share bug (everything renders as "Theorem X.Y" regardless of label type). That step is no longer required: **lint R0c statically checks the macros preamble** and errors if `\newtheorem{lemma}[theorem]{...}` lacks a matching `\newaliascnt{lemma}{theorem}`. R0c is stronger than visual spot-checking because it catches the bug at the source rather than via inspection. Run `lint.py` and ensure R0c passes.

**If you cannot run the build** (sandbox, no LaTeX installed), `latexmk-wrapper.py` returns JSON with `log_missing: true` and exits 1 — surface this to the user explicitly and ask them to run the build locally. Do not pretend the file compiles.

---

## End-to-end review

Triggered when all lemmas and the theorem proof are complete (Phase D), after the LaTeX compilation gate above has passed.

The end-to-end review is a **bounded peer-review loop**, not a single-shot check. A reviewer sub-agent writes a structured review (Summary / Strengths / Weaknesses / Questions / Verdict); the author agent verifies each weakness point-by-point, applies minimum-change fixes, and resubmits. The loop terminates by `accept-as-is` verdict, a 3-iteration hard cap, convergence detection (weakness overlap ≥ 80%), no-fixes-applied, or statement-change escalation.

→ **Read [review-loop.md](review-loop.md)** for the reviewer prompt template, the verification taxonomy (REAL-blocking / REAL-nonblocking / PHANTOM / INTENTIONAL), the cost-gated fix decision table, and the final-report format.

Before invoking the loop, re-read [anti-patterns.md](anti-patterns.md) — especially the AI-specific failure modes — and grep your own proof for any of them. Catching your own mistakes pre-review is cheaper than relying on the reviewer to find them.
