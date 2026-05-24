# Runner log — cap-set-ellenberg-gijswijt

## What I built

The headline theorem (\Cref{thm:main}) proves the Ellenberg--Gijswijt cap-set upper bound: any 3-AP-free subset $A \subseteq \F_3^n$ satisfies $|A| \le 3 M_n$, where $M_n$ counts monomials $\prod_i x_i^{a_i}$ with $a_i \in \{0,1,2\}$ and $\sum_i a_i \le 2n/3$, yielding $|A| \le C \cdot (2.7558)^n$. The proof is decomposed into four lemmas:
- **\Cref{lem:slice-rank-diagonal}** — diagonal lower bound for slice rank ($\sr(T) = |V|$ when $T$ is diagonal with nonzero diagonal entries on $V$).
- **\Cref{lem:cap-set-diagonal}** — the cap-set property forces $T_A$ to be diagonal, so $\sr(T_A) = |A|$.
- **\Cref{lem:T-polynomial}** — polynomial form $T_A(x,y,z) = \prod_i (1 - (x_i+y_i+z_i)^2)$ via $\1[w=0] = 1 - w^2$ in $\F_3$.
- **\Cref{lem:slice-rank-upper-bound}** — $\sr(T_A) \le 3 M_n$ via the three-way symmetric partition by lowest-degree variable group.

The composition (Theorem \Cref{thm:main}) is a two-line chain $|A| = \sr(T_A) \le 3 M_n$.

## Patterns chosen
- Statement template: standalone formal statements (no informal/formal pair needed for a self-contained appendix-grade result)
- Derivation pattern: trailing-justification block (default for chains where each step has its own short reason)
- Organizational pattern: "theorem-as-wrapper" — the headline theorem proof is a two-line composition of two named lemmas, with the technical content pushed into the lemmas; this is the closest fit from pattern-menu.md (fine-grained complexity row's "theorem-as-wrapper")

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 20
- After sweep: 18 🟢 / 2 🟡 / 0 🔴
- Sub-agents fired: 0 (every step fell into a fast-path: textbook inequality, trivial algebra, or digest match)
- Any 🔴 with `unable-to-derive`: none
- The 2 yellow steps are Step 7 (REF-basis support-maximization argument — confirmed by direct inline argument in iteration 2's rewrite) and Step 20 (numerical entropy optimization $3\gamma < 2.7558$, cited as black box to \cite{EllenbergGijswijt2017})

## Phase D — Review loop summary
- Iterations: 3 (max 3)
- Final verdict: **accept-as-is**
- Weaknesses per iteration: 4, 2, 0
- Fixes applied per iteration: 3, 1, 0
- Termination reason: accept-as-is verdict (Gate 1)
- Iteration files: `.proof-research/review-iteration-{1,2,3}.md`

### Fixes summary
- **Iteration 1**: removed misleading "by induction on $|V|$" framing; removed false-start sentence about "$U$ killed by $f_j^{(1)}$"; removed decorative "in $\F_3$" on the $(x_i+y_i+z_i)^2$ expansion line.
- **Iteration 2**: rewrote the "generic element / row-echelon" justification into a clean direct argument via the REF basis $\phi = \sum_k \phi_k$.
- **Iteration 3**: nothing to fix; reviewer accepts the rewrite as textbook-clean.

## Where I had to make calls
- **R5 layout**: kept theorem + proof in the same file (every section file contains both a `\begin{lemma}` (or `\begin{theorem}`) and the immediate `\begin{proof}`). External cited results in `99-auxiliary.tex` use the `[\cite{...}]` form.
- **Entropy bound as black-box**: I treated $M_n^{1/n} \to 3\gamma < 2.7558$ as an explicit citation to \cite{EllenbergGijswijt2017} rather than reproducing the large-deviation calculation, because the skill prompt isolates the polynomial-method / slice-rank part as the substantive content. The asymptotic optimization is independent and standard.
- **Field choice**: stated \Cref{lem:slice-rank-diagonal} over an arbitrary field $F$ (it works over any field), and the cap-set application invokes the lemma with $F = \F_3$.
- **Convention for empty sums in slice rank**: kept the parenthetical "$\sr(T) = 0$ iff $T \equiv 0$" in \Cref{def:slice-rank} without a separate sentence (reviewer flagged as INTENTIONAL).

## Self-check results
- `lint.py` errors: 0 (0 warnings)
- `latexmk` `compile_ok`: **true**
- Every `\cite{...}` resolves in `refs.bib`: yes (3 keys — `CrootLevPach2017`, `EllenbergGijswijt2017`, `Tao2016blog` — all cross-checked against the citation digests in `.proof-research/`)
- All `\input`'d section files exist on disk: yes (6 files: 01–05 + 99)

## What's incomplete
- None of the substantive proof content has `\todo{}` markers; the proof is complete.
- The numerical estimate $3\gamma < 2.7558$ is invoked as \Cref{fac:Mn-asymp} with proof attributed to \cite{EllenbergGijswijt2017}; this is by design (not pretended-as-proved).
