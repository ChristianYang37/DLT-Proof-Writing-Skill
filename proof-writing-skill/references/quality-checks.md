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

- **Union-bound budget.** If you prove $k$ high-probability events each at failure $\delta/k$, the theorem statement must use $\delta$ (not $\delta/k$). When in doubt, write out the union bound explicitly: *"By a union bound over \Cref{lem:A,lem:B,lem:C}, all three events hold with probability at least $1 - 3 \cdot \delta/3 = 1 - \delta$."*

---

## LaTeX compilation gate

A proof that does not compile is not a proof — it is a draft. Before declaring any phase complete:

1. **Run the project's build, with output redirected to `<project-root>/.output/`.** Keep build artifacts (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.pdf`) out of the project root so the source tree stays clean and gitignorable. Prefer:

   ```bash
   mkdir -p .output
   latexmk -pdf -outdir=.output main.tex
   ```

   If `latexmk` is unavailable, fall back to `pdflatex -output-directory=.output main.tex` twice (so `\ref` resolves), then `bibtex .output/main` if there is a `.bib`, then `pdflatex -output-directory=.output main.tex` twice more. The rendered PDF will be at `.output/main.pdf`.

   If the project has its own Makefile or `build.sh`, use that. Add `.output/` to `.gitignore` if it isn't already.

2. **Read the log.** Treat all of the following as failures, not warnings:
   - `Undefined control sequence` — a macro is used before it is defined.
   - `Reference ... undefined` — a `\ref`/`\eqref`/`\Cref` points at a nonexistent label.
   - `Citation ... undefined` — a `\cite` key is not in the `.bib`. **This may indicate a fabricated citation — verify immediately.**
   - `Multiply defined labels` — two `\label{}` with the same slug. Pick unique slugs.
   - `Overfull/Underfull \hbox` over ~50pt — fix display sizing, not just typesetting.

3. **Open the rendered PDF (`.output/main.pdf`) and spot-check cross-references.** This catches a class of bugs that compile cleanly but render wrong. In particular:
   - **Type-name correctness.** For each kind of label, verify the rendered prose: `\Cref{lem:foo}` must say "Lemma X.Y", `\Cref{ass:foo}` must say "Assumption X.Y", `\Cref{def:foo}` must say "Definition X.Y", `\Cref{fac:foo}` must say "Fact X.Y". **If everything renders as "Theorem X.Y" regardless of label type, the preamble is using shared `\newtheorem{X}[theorem]{X}` counters without `aliascnt`** — fix per [conventions.md](conventions.md) §Theorem-environment preamble. This is a silent-at-compile-time, loud-at-review-time bug; the log gives no warning.
   - **Equation references.** `\eqref{eq:foo}` must render as "(X.Y)" with parentheses.
   - **Multi-reference rendering.** `\Cref{lem:a,lem:b,lem:c}` must render as "Lemmas X, Y and Z" (or whatever the cleveref configuration prescribes), not as three separate "Lemma X" copies.
   - **Capitalization at sentence start.** Use `\Cref` (capital C) at sentence start, `\cref` (lowercase) mid-sentence — verify the rendered case matches sentence position.

4. **If the build is broken**, fix it before continuing. Do not move on with a non-compiling file; downstream edits compound the breakage.

5. **If you cannot run the build** (sandbox, no LaTeX installed), say so to the user explicitly and ask them to run it; do not pretend the file compiles. Also flag any cross-reference rendering you cannot verify without the PDF.

---

## End-to-end review

Triggered when all lemmas and the theorem proof are complete (Phase D), after the LaTeX compilation gate above has passed.

The end-to-end review is a **bounded peer-review loop**, not a single-shot check. A reviewer sub-agent writes a structured review (Summary / Strengths / Weaknesses / Questions / Verdict); the author agent verifies each weakness point-by-point, applies minimum-change fixes, and resubmits. The loop terminates by `accept-as-is` verdict, a 3-iteration hard cap, convergence detection (weakness overlap ≥ 80%), no-fixes-applied, or statement-change escalation.

→ **Read [review-loop.md](review-loop.md)** for the reviewer prompt template, the verification taxonomy (REAL-blocking / REAL-nonblocking / PHANTOM / INTENTIONAL), the cost-gated fix decision table, and the final-report format.

Before invoking the loop, re-read [anti-patterns.md](anti-patterns.md) — especially the AI-specific failure modes — and grep your own proof for any of them. Catching your own mistakes pre-review is cheaper than relying on the reviewer to find them.
