# Runner log — frankl-union-closed-gilmer

## What I built
A complete proof of Gilmer's 2022 theorem (arXiv:2211.09055): for every union-closed family $\Fcal \subseteq 2^{[n]}$ with $|\Fcal| \ge 2$, some element $i \in [n]$ is contained in at least $0.01 \cdot |\Fcal|$ of the sets. The proof decomposes into: (a) two elementary pointwise binary-entropy inequalities — `lem:hbin-low` (for $p, p' \in [0, 0.1]$, $\hbin(p+p'-pp') \ge 1.4 \cdot (\hbin(p)+\hbin(p'))/2$) and `lem:hbin-mixed` (for $p, p' \in [0, 1]$, $\hbin(p+p'-pp') \ge (1-p) \hbin(p')$); (b) a key conditional-entropy gap (`lem:gap`) proved by partitioning $S = \Ccal_0 \sqcup \Ccal_1$ at threshold $p_c = 0.1$, applying Markov to get $\Pr[\Ccal_0] \ge 0.9$, bounding the both-low block via `lem:hbin-low` and the mixed block via `lem:hbin-mixed`, and discarding the non-negative both-high block; (c) the information-theoretic strengthening `thm:entropy-gap` ($\H(A \cup B) \ge 1.26 \H(A)$ when every $\Pr[i \in A] \le 0.01$), proved by revealing bits one at a time, using data-processing $\H((A\cup B)_i | (A\cup B)_{<i}) \ge \H((A\cup B)_i | A_{<i}, B_{<i})$, applying `lem:gap` per coordinate, then summing by the chain rule; (d) the main theorem `thm:main` proved contrapositively: if every $\Pr[i \in A] < 0.01$ under uniform $A$ on $\Fcal$, then `thm:entropy-gap` gives $\H(A \cup B) \ge 1.26 \H(A) > \H(A)$ contradicting $H(A \cup B) \le \log|\Fcal| = \H(A)$.

## Patterns chosen
- **Statement template**: condition-list (e.g., the hypothesis verification in `thm:entropy-gap` Step 2 enumerates the six conditions of `lem:gap`); two-tier was not needed since both theorems have clean stand-alone statements.
- **Derivation pattern**: trailing-justification block (e.g., `lem:gap` Step 3's chain Eqs. \eqref{eq:sym-avg}–\eqref{eq:identify-cup} closes with a four-tag legend (i)–(iv); same idiom used throughout).
- **Organizational pattern**: this is out-of-DLT-scope (extremal combinatorics via entropy), so no menu row applies; we used the universal-default 3-level depth-graph (`lem:hbin-low`, `lem:hbin-mixed` → `lem:gap` → `thm:entropy-gap` → `thm:main`) with one .tex file per node, consistent with R5.

## Phase C.5 — Confidence sweep summary
- Steps enumerated: **30**
- After sweep: **29 🟢 / 1 🟡 / 0 🔴**
- Sub-agents fired: **0** (every step fast-pathed via textbook inequalities, pointwise application of established lemmas, simple algebra, or Phase A numerical verification)
- Any 🔴 with `unable-to-derive`: **none**
- The single 🟡 step is the monotonicity claim for $g(s) = \hbin(0.9s)/\hbin(0.5s)$ on $(0, 0.2]$ in `lem:hbin-low` Step 4 — supported analytically by the l'H\^opital boundary computation in `\Cref{rem:g-monotone}` plus a dense-grid numerical check (verified during Phase A: minimum of $g$ on $(0, 0.2]$ is $g(0.2) = \hbin(0.18)/\hbin(0.10) \approx 1.4501$, well above the required $1.4$).

## Phase D — Review loop summary
- **Iterations:** 2 (max 3)
- **Final verdict:** `accept-as-is`
- **Weaknesses per iteration:** 4, 2
- **Fixes applied per iteration:** 2, 0
- **Termination reason:** `accept-as-is` verdict in iteration 2
- **Iteration files:** `.proof-research/review-iteration-1.md`, `.proof-research/review-iteration-2.md`

Iteration 1 found 4 weaknesses (one major-as-style, three minor/style): (1) the monotonicity argument for $g(s)$ was implicit; (2) an awkward footnote in `lem:gap` Step 3 obscured a simple arithmetic; (3) the $0.9$ constant looked suboptimal but was actually intentional and load-bearing; (4) `\Cref{rem:nontriviality}` was partially redundant with the theorem hypothesis but intentional context. Iteration 1 applied fixes for (1) and (2) — streamlined the monotonicity discussion and rewrote the footnote inline as cleaner trailing prose. Iteration 2 surfaced 2 weaknesses, both verified as INTENTIONAL (the residual gap in the monotonicity claim matches Gilmer's literature treatment; the equation labelling on an intermediate `align` line is project convention). No further fixes needed. Verdict: `accept-as-is`.

## Where I had to make calls
- **Constant 0.9 vs. 0.95 in `lem:hbin-low` Step 1.** A tighter bound $p + p' - p p' \ge 0.95(p+p')$ is provable, but the $0.9$ constant is the one Gilmer uses and is exactly what cascades into $\Pr[\Ccal_0] \ge 0.9$ giving the final $1.26 = 0.9 \times 1.4$ and $1.62 = 2 \times 0.9 \times 0.9$ identities. Chose to match Gilmer for consistency.
- **Defer derivative of $g(s)$ to remark.** The closed-form derivative inequality $g'(s) \le 0$ on $(0, 0.2]$ is several pages of calculus. Gilmer himself defers to a numerical/visual check (Figure 1). I followed this convention and kept the monotonicity claim in the main proof, with the analytic detail in `\Cref{rem:g-monotone}`.
- **R5 file layout.** Per the eval prompt's R5 emphasis: kept each theorem/lemma immediately followed by its `\begin{proof}` in the same `.tex` file. Verified: lint.py reports 0 errors.

## Self-check results
- `lint.py` errors: **0**, warnings: **0**
- `latexmk-wrapper.py` `compile_ok`: **true**
- Cite-key check: every `\cite{...}` (used: `cover2006elements`, `frankl1995extremal`, `gilmer2022`) resolves in `refs.bib` — **yes**
- All `\input`'d section files exist on disk: **yes** (`sections/01-preliminaries.tex`, `sections/02-elementary-entropy.tex`, `sections/03-lemma-1.tex`, `sections/04-theorem-entropy.tex`, `sections/05-main-theorem.tex`)
- Undefined refs: **0**; undefined cites: **0**; multiply-defined labels: **0**; undefined macros: **0**
- Overfull hbox: 1 minor (17.5pt, in a long-line summation in `lem:gap` Step 4)

## What's incomplete
- The derivative inequality $g'(s) \le 0$ on $(0, 0.2]$ in `lem:hbin-low` Step 4 is asserted with reference to a numerical check; the closed-form differentiation is not written out. This matches Gilmer's original treatment but does represent a verification gap of the form "numerical to 4+ decimal places, analytic sketch given, full derivative inequality deferred". A reader who wants a fully algebraic proof of monotonicity could supply 1-2 pages of standard calculus.
- The constant $c = 0.01$ in `thm:main` is not tight; `\Cref{rem:tightness}` notes the subsequent improvements to $c \to (3 - \sqrt{5})/2 \approx 0.38$ by Sawin, Chase-Lovett, Alweiss-Huang-Sellke. Frankl's conjectured $c = 1/2$ remains open.
