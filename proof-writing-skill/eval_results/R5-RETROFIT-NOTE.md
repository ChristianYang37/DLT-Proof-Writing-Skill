# R5 retrofit note (post-v1.0)

After the initial v1.0 release, a new lint rule **R5 (theorem-needs-proof-or-cite)** was added to `proof-writing-skill/scripts/lint.py`:

> Every `\begin{theorem}` / `\begin{lemma}` / `\begin{proposition}` / `\begin{corollary}` / `\begin{claim}` must satisfy **exactly one** of:
> 1. The FIRST environment after `\end{X}` (in the same file) is `\begin{proof}`.
> 2. The optional `[...]` bracket of `\begin{X}` contains a `\cite{...}` whose key resolves in `refs.bib`.

This is the "no well-known result without proof or citation" rule — the skill's strongest defense against handwaving.

## Effect on the existing v1.0 eval results

Running the new lint against the 5 eval outputs **as they were submitted under v1.0 conventions** yields:

| Eval | R5 violations | Cause |
|---|---|---|
| 01-hoeffding | 0 | theorem and proof co-located in `sections/03-main-theorem.tex` — happens to comply |
| 02-ntk-convergence | 1 | `02-main-result.tex` states the main theorem; proof is in `06-proof-of-main.tex`. Intervening env `\begin{lemma}` |
| 03-vc-generalization | 1 | `02-main-result.tex` states the main theorem; intervening `\begin{remark}` (`rem:headline-form`) before the proof file |
| 04-linear-mdp-ucb | 1 | same pattern as 02/03 |
| 05-sobolev-lower-bound | 1 | same pattern |

These are **not handwaves** — every theorem in every eval has a real, complete, immediately-following proof in the project. The violation is **structural**: under v1.0, runners followed the "one .tex per file" convention by splitting theorem statement and proof into separate files. R5 forbids this split.

## Why we keep these results unchanged

These are historical eval records under the v1.0 convention. Fixing them after the fact would:

- Misrepresent the v1.0 results (the grading.json files reflect the rules then in force)
- Make the benchmark non-reproducible (you couldn't re-derive the v1.0 numbers)

Instead, the rule change is documented here and in the updated `conventions.md` / `runner.md`. **Future runs (v1.1+) will enforce R5 from the start**, and the recommended file layout is:

```
sections/
├── 01-preliminaries.tex          # definitions / assumptions / cited facts
├── 02-lemma-A.tex                # \begin{lemma} + \begin{proof}
├── 03-lemma-B.tex                # same
├── 04-main-theorem.tex           # \begin{theorem} + \begin{proof}
└── 99-auxiliary.tex              # cited externals via [\cite{...}]
```

i.e., theorem and proof in the same file, supporting lemmas each in their own file with their own immediate proofs.

## Reproducing the R5 check

```bash
cd proof-writing-skill
for n in eval_results/0[1-5]-*/; do
  [ -f "$n/refs.bib" ] && bib="--bib $n/refs.bib" || bib=""
  ./scripts/lint.py "$n/main.tex" "$n/macros.tex" "$n"/sections/*.tex $bib | grep -E "R5|errors"
done
```
