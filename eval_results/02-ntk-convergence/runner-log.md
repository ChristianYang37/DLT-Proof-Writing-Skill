# Runner log — ntk-convergence-two-layer

## What I built

A complete appendix-grade proof of linear convergence of GD on a two-layer ReLU network in the over-parameterized regime, following the three-lemma NTK skeleton of Du-Zhai-Poczos-Singh 2019. The headline `\Cref{thm:main}` shows that for $m \ge C_1 n^6 / (\lambda_0^4 \delta^3)$ and $\eta = C_2 \lambda_0 / n^2$, with probability $\ge 1 - \delta$ over initialization the squared training loss contracts by $1 - \eta\lambda_0/2$ per step and every weight stays within an $R = O(\sqrt n / (\sqrt m \lambda_0)) \cdot \norm{\ub(0)-\yb}_2$-ball of init. Decomposition: `\Cref{lem:init_gram}` (Gram concentration at init), `\Cref{lem:perturbation}` (Gram stability under perturbations $\le R$), `\Cref{lem:linear_conv}` (deterministic linear convergence in a stay-in-ball regime), plus auxiliary `\Cref{lem:init_residual}` (initial-residual size). Closure via inductive fixed-point argument with explicit handoff of hypotheses between lemmas (revised in Phase D iter 1).

## Patterns chosen

- Statement template: two-tier informal vs. formal in the body; lemmas use condition-list (heavy-hypothesis case) per templates.md
- Derivation pattern: trailing-justification / inline-numbered steps; one `\paragraph{Step k}` block per major argument
- Organizational pattern: **Three-lemma NTK skeleton** (init Gram concentration + perturbation stability + stay-in-ball) + successful-event conditioning + induction on iterates, per pattern-menu.md row "Over-parameterized NN convergence"

## Phase C.5 — Confidence sweep summary

- Steps enumerated: 32
- After sweep (pre-Phase D): 27 🟢 / 3 🟡 / 2 🔴 (Steps 6, 21 with `\todo{verify}` markers)
- After Phase D iter 1 fixes: 29 🟢 / 3 🟡 / 0 🔴
- Sub-agents fired: 0 (all upgrades via fast paths: textbook inequalities, digest matches, or in-line re-derivation)
- Reports in `.proof-research/`: `confidence-trace.md`, technique digests `cite-du2019gradient.md`, `hoeffding-mcdiarmid.md`, `gaussian-anticoncentration.md`, `relu-grad-bound.md`
- Any 🔴 with `unable-to-derive`: **none**

## Phase D — Review loop summary

- Iterations: 2 (max 3)
- Final verdict: **accept-as-is** (post-fix, after iteration 2)
- Weaknesses per iteration: 5 (iter 1), 3 (iter 2)
- Fixes applied per iteration: 4 (W1, W2, W4, W5) in iter 1; 3 (W6, W7, W8) in iter 2; 1 INTENTIONAL rebuttal (W3)
- Termination reason: **accept-as-is verdict** at iter 2 (Termination Gate 1)
- Iteration files: `.proof-research/review-iteration-1.md`, `.proof-research/review-iteration-2.md`

## Where I had to make calls

- **Lemma decomposition.** Split the auxiliary `\Cref{lem:init_residual}` (initial residual size) out from `\Cref{lem:init_gram}` because both are init-time concentration but their proofs use different tools (entrywise Hoeffding + entrywise-to-op-norm vs.\ conditional Hoeffding + chi^2 tail). Combining them in one lemma would have muddied the headline.
- **Headline width.** Used $m \ge C_1 n^6 / (\lambda_0^4 \delta^3)$ (DZPS19 scaling) rather than the tighter $n^4$-type polynomials available in follow-up work, noted in `\Cref{rem:width_check}`.
- **`\Cref{lem:linear_conv}` hypothesis design.** Initially stated as a pure spectral-LB hypothesis; Phase D reviewer flagged that this hides the need for perturbation-event control inside the proof. Reworked in iter 1 to take both the perturbation bound and the flip-count bound as explicit hypotheses, with the main theorem proof Step 3 supplying them via $(\star_t)$ and $\mathcal E_2$.
- **Sub-Gaussian proxy for $\ub_i(0)$.** Initial draft compressed this into "by sub-Gaussian tail bound"; rewritten in iter 1 via explicit conditional Hoeffding + chi-squared tail on the conditioning variance, removing the `\todo{verify}` marker.
- **W3 (loose $\opnorm{\Hb_s} \le n$).** Marked INTENTIONAL — looser bound is sufficient for the absorption $\eta n \le 1$; tightening would only relax $C_2$, not change the rate.

## Self-check results

- lint.py errors: **0** errors, 0 warnings
- latexmk compile_ok: **true** (3 overfull \hbox warnings at $\le 17$pt, all in display-math wrapping — minor typesetting only)
- Cite-key check: every `\cite{...}` resolves in `refs.bib`. Single cite key used: `du2019gradient`, defined in `refs.bib`. **Yes**
- All `\input`'d section files exist on disk: **yes** (6 sections + macros)
- All `\todo{}` markers cleared: **yes** (both `verify:` markers from initial draft removed in Phase D iter 1 fixes)

## What's incomplete

- **The proof is complete relative to the eval prompt.** No `\todo{}` items remain in the .tex.
- Per `\Cref{rem:width_check}`, tighter width polynomials ($n^4$ instead of $n^6$) are available in follow-up literature but explicitly out of scope.
- The argument freezes $\ab$ at init (matching DZPS19); training both layers is a routine extension but not done here.
- `experiments-plan.md` Results section is left blank as required by theory-experiment.md; the user runs experiments and fills in numbers afterwards.
- Three style-minor weaknesses (W6, W7, W8 from Phase D iter 2) were addressed by small textual patches; if the user prefers tighter exposition, those derivations could be further compressed, but the current form is more reviewer-friendly.
