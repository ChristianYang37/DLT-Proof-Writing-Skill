# Phase-E drift review — per-step faithfulness report

Reviewer role: semantic drift reviewer (Lean is ground truth). For each rendered LaTeX
step we compare the Lean `@lx latex` proposition + the tactic body + `@lx cite` against the
generated LaTeX step. Verdict ∈ {faithful, over-claim, under-claim, justification-drift}.

Deterministic `drift_check.py` D1 was RED due to an annotation-formatting artifact (mangled
step ids in the frozen Lean — see `confidence-trace.md` Phase-E status); that was orthogonal
to the *semantic* verdicts below, which assess content faithfulness. The comment-only
remediation has since been applied — `drift_check.py` now exits 0 (D1 green, 8 Lean ↔ 8
LaTeX) — so the 🔵 tier is GRANTED for all steps (see the updated **Gate status** below).

Notation map: `.lean-proof/notation-map.md` (every symbol drawn from it; D5 clean).

| # | step id | Lean proposition (source of truth) | LaTeX rendering site | justification check (INV-3) | verdict |
|---|---|---|---|---|---|
| 1 | `lem:sign_equiv` | `μ⁻¹*c > 0 ↔ μ*c > 0` (μ≠0, c:ℝ) | `02-theorem-decode-iff.tex` Lemma + proof (l.16–31) | factor `μ²>0` + identity `(μ⁻¹c)μ²=μc`; no Mathlib names (internal `hsq`,`hid` absorbed) | faithful |
| 2 | `thm:main` (statement) | hyps `0<r`, `‖x⋆‖=r`, `∇L(x⋆)=μ•x⋆`, `μ≠0`; concl `Generated ↔ ∀ b≠a⋆, μ⟪W_{a⋆}−W_b,∇L(x⋆)⟫>0` | Theorem env (l.37–52) | statement-level; sphere hyps retained, sign `μ⟪·⟫>0` NOT flipped | faithful |
| 3 | `thm:main.1` | `x⋆ = μ⁻¹ • ∇L(x⋆)` | proof (l.59–64) | rearrange stationarity using μ≠0 (smul_smul/inv_mul_cancel₀/one_smul → "rearranges") | faithful |
| 4 | `thm:main.2` | `⟪W_{a⋆},x⋆⟫>⟪W_b,x⋆⟫ ↔ μ⟪W_{a⋆}−W_b,∇L(x⋆)⟫>0` | proof (l.66–81) | bilinearity (inner_sub_left/sub_pos = internal h1), substitute + scalar pull (real_inner_smul_right = internal h2), then `\Cref{lem:sign_equiv}`; cites lem:sign_equiv ✔ | faithful |
| 5 | `thm:main.3` | unfold `Generated`; push per-competitor equiv under `∀ b≠a⋆` | proof (l.83–93) | unfold `\Cref{def:decoder}` + quantify thm:main.2; cites thm:main.2 ✔ | faithful |
| 6 | `cor:neg` (statement) | hyp `μ<0`; concl `∀ b≠a⋆, ⟪W_{a⋆}−W_b,−∇L(x⋆)⟫>0` | Corollary env (l.111–122) | statement-level; descent-direction reading | faithful |
| 7 | `cor:neg.1` | instantiate main thm at this x⋆,μ (μ≠0 from μ<0) | proof (l.125–132) | "applies with this x⋆ and μ"; cites thm:main ✔ | faithful |
| 8 | `cor:neg.2` | `μ⟪v,∇L(x⋆)⟫>0 ↔ ⟪v,−∇L(x⋆)⟫>0` | `03-corollaries.tex` proof (cor:neg.2) | μ<0 ⇒ (μc>0 ⇔ c<0); `⟪v,−g⟫=−⟪v,g⟫` rendered as "linearity in the second argument" (inner_neg_right, no Mathlib name) | faithful |
| 9 | `cor:fail` (statement) | same hyps as MAIN; concl `¬Generated ↔ ∃ b≠a⋆, μ⟪W_{a⋆}−W_b,∇L(x⋆)⟫≤0` | `03-corollaries.tex` Corollary env (cor:fail) | statement-level; De Morgan dual; `≤0` is the exact negation of `>0`; sign preserved | faithful |
| 10 | `cor:fail.1` | `¬Generated ↔ ∃ b≠a⋆, μ⟪…⟫≤0` (via negating main iff) | `03-corollaries.tex` proof (cor:fail.1) | negate main iff; push ¬ through ∀ and strict ineq (push_neg) → ∃ + ≤0; cites thm:main ✔ | faithful |
| 11 | `cor:ce` (statement) | extra hyp `∇L=∑_c (p_c−[c=a⋆])•W_c`; concl `Generated ↔ ∀ b≠a⋆, μ∑_c (p_c−[c=a⋆])(⟪W_{a⋆},W_c⟫−⟪W_b,W_c⟫)>0` | `03-corollaries.tex` Corollary env (cor:ce) | statement-level; cross-entropy specialization; strict `>0` preserved | faithful |
| 12 | `cor:ce.1` | `⟪W_{a⋆}−W_b,∇L⟫ = ∑_c (p_c−[c=a⋆])(⟪W_{a⋆},W_c⟫−⟪W_b,W_c⟫)` | `03-corollaries.tex` proof (cor:ce.1) | substitute hgrad; distribute inner over sum (inner_sum), pull scalar (real_inner_smul_right), expand gap (inner_sub_left), termwise (Finset.sum_congr) — all rendered as "distributing/pulling/expanding", no Mathlib names; cites hgrad ✔ | faithful |
| 13 | `cor:ce.2` | rewrite each per-b alignment in main iff by the cor:ce.1 identity under `∀ b≠a⋆` | `03-corollaries.tex` proof (cor:ce.2) | apply thm:main + rewrite by identity under ∀; cites thm:main, cor:ce.1 ✔ | faithful |

**Summary:** 13/13 faithful. 0 over-claim, 0 under-claim, 0 justification-drift. No Mathlib
declaration names leaked into prose. All symbols are notation-map macros.

**Gate status (this paper, 4 results):** `lean-wrapper.py --mode build` `integrity_ok=true`
(axiom closure `{propext, Classical.choice, Quot.sound}` for ALL FOUR theorems, no
sorry/admit); `lean_lint.py --style --lock` exit 0 (SL1 holds for all 4 frozen signatures —
the 2 carried-over byte-for-byte, the 2 new ones added); `drift_check.py` exit 0 — D1 green,
**13 Lean steps ↔ 13 LaTeX steps** (9 advisory D4 warnings only — all are prose
`\Cref`-references to definitions/remarks/sections or cross-theorem references, not lemma
citations the tactic used; non-blocking by design); `lint.py` exit 0; `latexmk-wrapper.py`
`compile_ok=true` (1 overfull hbox of 20.3pt, well under the 50pt threshold). The new steps
use the same annotation conventions (closing `-/` on its own line + `show _ ↔ _`
flush-triggers for `cor:fail.1` / `cor:ce.2`). D1 green ⇒ the 🔵 tier is GRANTED for all 13
steps (machine-verified in the kernel).
