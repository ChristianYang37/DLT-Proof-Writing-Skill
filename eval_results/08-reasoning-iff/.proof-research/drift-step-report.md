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
| 8 | `cor:neg.2` | `μ⟪v,∇L(x⋆)⟫>0 ↔ ⟪v,−∇L(x⋆)⟫>0` | proof (l.134–147) | μ<0 ⇒ (μc>0 ⇔ c<0); `⟪v,−g⟫=−⟪v,g⟫` rendered as "linearity in the second argument" (inner_neg_right, no Mathlib name) | faithful |

**Summary:** 8/8 faithful. 0 over-claim, 0 under-claim, 0 justification-drift. No Mathlib
declaration names leaked into prose. All symbols are notation-map macros.

**Gate status (updated 2026-06-02, post-remediation):** `lean-wrapper.py --mode build`
`integrity_ok=true` (axiom closure `{propext, Classical.choice, Quot.sound}`, no sorry/admit);
`lean_lint.py --style --lock` exit 0 (SL1 holds, signatures unchanged); `drift_check.py`
exit 0 — D1 green, **8 Lean steps ↔ 8 LaTeX steps** (4 advisory D4 warnings only,
non-blocking); `lint.py` exit 0; `latexmk-wrapper.py` `compile_ok=true`. The earlier 5 D1
id-string artifacts were resolved by a comment-only Lean edit (move each closing `-/` to its
own line; add the statement-level `@lx kind: named`; add no-op `show _ ↔ _` flush-triggers for
`thm:main.3` / `cor:neg.2`) — no signature or kernel-proof change. D1 is now green, so the 🔵
tier is **GRANTED** for all 8 steps (tags 🟢 → 🔵, machine-verified in the kernel).
