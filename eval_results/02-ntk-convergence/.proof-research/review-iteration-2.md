# Phase D — Review iteration 2

Proof under review: **Linear convergence of gradient descent for over-parameterized two-layer
ReLU networks** (NTK analysis), `eval_results/02-ntk-convergence/`, headline
`\Cref{thm:main}` in `sections/06-main-theorem.tex`.

Five INDEPENDENT reviewers (R1 line-by-line rigor, R2 assumptions/generality, R3 ML-significance,
R4 math-taste, R5 derivation-integrity). Inputs: `sections/*.tex`, `.output/main.pdf`,
`.output/main.log`, `.proof-research/confidence-trace.md`.

## Scores

| Reviewer | Score | Blocking? |
|---|---|---|
| R1 line-by-line | 7 | no |
| R2 assumptions/generality | 7 | no |
| R3 ML-significance | 8 | no |
| R4 math-taste | 8 | no |
| R5 derivation-integrity | 7 | no |
| **mean** | **7.40** | — |

Orchestrator decision: mean 7.40 ≤ 8 (strict bar), no unresolved REAL-blocking critical → **ITERATE**.

Score history across iterations: 4.20 → 7.40.

---

## Merged + deduped weaknesses

Dedupe rule: same `file:line ± 3` OR paraphrase of the Claim = one merged weakness; keep max
severity; record how many of 5 raised it.

### Weakness #1 (severity: minor, raised by 1/5 + linked 1/5)
**Claim:** `lem:init-gram-close` states width `m ≥ Cn²log(n/δ)/λ₀²`, but the proof used only a
Frobenius second-moment + Markov bound, whose RHS is `16n²/(λ₀²m)`; at the stated log-width this
is `16/(C log(n/δ))`, which is **not** ≤ δ for a universal C (Markov needs the `1/δ` width
`m ≥ 16n²/(λ₀²δ)`). The declared `\Cref{fac:hoeffding}` — which *would* license a log-width — is
never used. (R1 minor, `02:57`; linked R5 style "phantom Hoeffding apparatus", `01:74`.)
**Verdict:** REAL-blocking (the displayed proof does not license the stated lemma width).
**Rebuttal / fix-plan:** Confirmed by substitution: `16n²/(λ₀²·Cn²log(n/δ)/λ₀²)=16/(C log(n/δ))`
does not reach δ. FIXED **without changing the lemma statement**: rewrote Steps 1–3 of `02` to use
entrywise Hoeffding (`\Cref{fac:hoeffding}`) — `Pr[|H_ij−H∞_ij|≥τ]≤2exp(−mτ²/2)` with
`τ=λ₀/(4n)` — then a union over the `n²` entries, giving `2n²exp(−mτ²/2)≤δ` whenever
`m ≥ (2/τ²)log(2n²/δ)=(32n²/λ₀²)log(2n²/δ)`, implied by `eq:width-init` with `C≥128`. The entrywise
bound feeds `‖·‖₂≤‖·‖_F≤√(n²τ²)=nτ=λ₀/4`. This genuinely delivers the stated `log(n/δ)` width
**and** consumes the previously-unused Hoeffding fact (resolving the linked W-B).

### Weakness #2 (severity: style, raised by 1/5)
**Claim:** `\Cref{fac:hoeffding}` is declared in the preliminaries but never invoked — phantom
apparatus. (R5 style, `01:74`.)
**Verdict:** REAL-nonblocking — subsumed by #1.
**Rebuttal / fix-plan:** RESOLVED by the #1 rewrite: the init-gram lemma now invokes
`\Cref{fac:hoeffding}` in Step 1. No separate patch; the fact is now load-bearing.

### Weakness #3 (severity: major, raised by 2/5)
**Claim:** `lem:main` consumes the initial-residual event (`\Cref{lem:init-residual}`,
`E_3`) in proof part (a) but lists only three events in its hypotheses, with intersection
probability `1−3δ`; its "all statements below are deterministic" claim is false on the three-event
intersection it names. Repaired only at the theorem level via the four-event union.
(R1 minor, R2 major; `05:19-22, 71-72`.)
**Verdict:** REAL-nonblocking (contract gap; the final theorem is sound because `06:66` feeds
`E_3`). Major severity per R2.
**Rebuttal / fix-plan:** Confirmed. FIXED in place: added the initial-residual event of
`\Cref{lem:init-residual}` to `lem:main`'s bulleted hypotheses, upgraded the stated intersection
budget from `1−3δ` to `1−4δ`, and changed the proof's "intersection of the three high-probability
events" to "four high-probability events". The lemma conclusion (headline) is unchanged.

### Weakness #4 (severity: minor, raised by 4/5)
**Claim:** The initial-residual constant carries two values across §05/§06: `√(2n/δ)` in
`lem:init-residual` and the stay-in-ball computation (`05:72`), but `√(8n/δ)` in `E_3` / the
iteration count (`06:42,71`); the `δ→δ/4` rescaling that reconciles them is left implicit at the
cite-site. (R2 minor, R3 minor, R4 minor, R5 minor; `05:72 vs 06:42`.)
**Verdict:** REAL-nonblocking (the two values are mutually consistent — `√(2n/(δ/4))=√(8n/δ)` —
the factor 4 is absorbed into `C`; only the cite-site annotation was missing).
**Rebuttal / fix-plan:** Confirmed. FIXED: at `05:72` the cite now reads "when the theorem invokes
this lemma at level `δ/4` the bound reads `√(8n/δ)`, which only enlarges the constant `C` below and
is absorbed into it". The `32→128` factor in the width constant lands in the same universal `C`.

### Weakness #5 (severity: minor, raised by 1/5)
**Claim:** The initial-residual constant is recorded at a **third**, mutually inconsistent value in
the confidence trace (`6n/δ` at Steps 33/35) vs `8n/δ` in the theorem and `2n/δ` in the lemma —
evidence the iter-1 constant fix was not propagated to the trace. (R3 minor;
`06:71 vs confidence-trace.md:305,308`.)
**Verdict:** REAL-nonblocking (trace-only; the `.tex` is internally consistent).
**Rebuttal / fix-plan:** Confirmed: the trace still showed the obsolete `δ/3` value `6n/δ`. FIXED:
synced trace Steps 33 to `8n/δ` and annotated `E_3` as `\Cref{lem:init-residual}` at level `δ/4`.
No proof change.

### Weakness #6 (severity: minor, raised by 3/5)
**Claim:** The flipping set `S_k` is declared `⊆[m]` (neurons) but then treated as a set of
`(r,i)` pairs (`⊆N`, counted by `Σ_r Σ_i`, `E|S_k|≤2nmR`) — one symbol, two types.
(R1 minor, R4 minor, R5 minor; `05:93,108,117`.)
**Verdict:** REAL-nonblocking (the realized bound is unaffected; `N` and the count are pair-typed,
so the over-estimate is safe — but the declaration is genuinely inconsistent).
**Rebuttal / fix-plan:** Confirmed. FIXED: declared `S_k ⊆ [m]×[n]` as "the set of flipping pairs"
at the point of definition, and made the surrounding prose ("every flipping pair", "each flipping
pair `(r,i)` perturbs the `i`-th coordinate", the `Σ_r Σ_i` count justification) type-consistent.
`N := {(r,i):…}` is now genuinely a superset of `S_k`.

### Weakness #7 (severity: major, raised by 3/5)
**Claim:** The load-bearing remainder fold-in (Step 27) is asserted in prose — "it shifts the
factor by at most `ηλ₀/4`, absorbed by the slack in `(1−x)²≤1−x`" — without displaying the
perturbed recursion `y−u(k+1)=(I−ηH)(y−u(k))+ε(k)` or the squared-norm absorption; moreover the
named licensing rule (`(1−x)²≤1−x`) is not the operative one (the actual step is
`(1−3ηλ₀/8)²≤1−ηλ₀/2`). (R1 minor, R2 minor, R5 major; `05:143`.)
**Verdict:** REAL-nonblocking (conclusion `eq:contract-kp1` is correct; the prose mechanism and the
missing display are the defect). Major severity per R5.
**Rebuttal / fix-plan:** Confirmed by re-derivation. FIXED: replaced the prose parenthetical with a
displayed perturbed recursion `y−u(k+1)=(I−ηH(k))(y−u(k))+ε(k)`, then a triangle-inequality
display `‖y−u(k+1)‖ ≤ (1−ηλ₀/2)‖y−u(k)‖ + (ηλ₀/8)‖y−u(k)‖ = (1−3ηλ₀/8)‖y−u(k)‖`, and an explicit
squaring step `(1−3ηλ₀/8)² ≤ 1−ηλ₀/2` (valid since `9/64·(ηλ₀)² ≤ ¼ηλ₀` for `ηλ₀≤16/9`, which
holds as `ηλ₀≤κλ₀²/n²≤1/2`). The headline rate `(1−ηλ₀/2)^k` is unchanged.

### Weakness #8 (severity: style, raised by 1/5)
**Claim:** Constant-tracking prose drops the `η` of the flip-remainder prefactor: line 140 says
"prefactor `8cλ₀ ≤ λ₀/8`" but the display at 134 is `(ηλ₀/8)‖·‖`, so the prefactor is `8cηλ₀`.
(R2 style; `05:140`.)
**Verdict:** REAL-nonblocking (the display is correct; the prose dropped a factor `η`).
**Rebuttal / fix-plan:** Confirmed. FIXED (single token): prose now reads
"prefactor `8cηλ₀ ≤ ηλ₀/8` for `c ≤ 1/64`".

### Weakness #9 (severity: minor, raised by 1/5)
**Claim:** The per-neuron per-coordinate perturbation magnitude `(1/√m)R_step` is asserted in prose
with no derivation; the underlying 1-Lipschitz / Cauchy–Schwarz bound on
`|σ(w(k+1)^⊤x_i)−linearization|` is omitted (true only up to a factor of 2). (R5 minor; `05:127`.)
**Verdict:** REAL-nonblocking — DECLINED per cost gate.
**Rebuttal / fix-plan:** The one-clause magnitude `(1/√m)R_step` feeds the display `eq:remainder`
and is dominated by it; a fully rigorous 1-Lipschitz derivation (with its factor-of-2 slack, itself
absorbed by `c ≤ 1/64`) would add well beyond the 3-line budget for a minor non-blocking item, for
marginal rigor gain — R19 already passes and the realized bound is on the safe over-estimating
side. Surfaced here rather than auto-fixed. (Minimum-change / cost-gate decline.)

---

## Accept decision

Mean **7.40** ≤ 8 (strict bar). No reviewer set Blocking? = yes, and no merged weakness is a
REAL-blocking **critical** — so no unresolved critical blocks the gate, but the mean bar is not
met. Per Component 4 gate 1, the accept gate is **NOT** met → **ITERATE**.

Fixes applied this iteration (all minimum-change, no headline statement altered):

- **#1 (REAL-blocking minor, 1/5):** init-gram lemma rewritten to the Hoeffding + union route that
  genuinely licenses the stated `log(n/δ)` width (`02`, Steps 1–3 + R17-ignore comment).
- **#2 (style, subsumed):** Hoeffding fact now load-bearing — no separate patch.
- **#3 (major, 2/5):** init-residual event added to `lem:main` hypotheses; budget `1−3δ → 1−4δ`
  (`05:19-22, 38-40`).
- **#4 (minor, 4/5):** `δ/4` rescaling annotated at the stay-in-ball cite-site (`05:72`).
- **#5 (minor, 1/5):** confidence-trace residual constant synced `6n/δ → 8n/δ` (`trace:305,308`).
- **#6 (minor, 3/5):** `S_k` re-typed as `⊆[m]×[n]` (pairs) consistently (`05:93,108,122,133,142`).
- **#7 (major, 3/5):** remainder fold-in promoted to a displayed perturbed recursion + explicit
  squaring `(1−3ηλ₀/8)²≤1−ηλ₀/2` (`05:136-160`, new `eq:contract-kp1-sq`).
- **#8 (style, 1/5):** prose prefactor corrected to `8cηλ₀ ≤ ηλ₀/8` (`05:146`).

Declined (surfaced, not fixed):

- **#9 (minor non-blocking, 1/5):** prose-only per-coordinate magnitude — cost > 3-line budget for
  marginal gain; bound is on the safe side and R19 passes.

No PHANTOM and no INTENTIONAL verdicts this iteration. No headline theorem/lemma **statement** was
changed (the init-gram width string `Cn²log(n/δ)/λ₀²` is preserved; only its proof changed) — no
statement-change escalation triggered.

Post-fix gates: `lint.py` 0 errors / 0 warnings (incl. R19); `latexmk-wrapper.py`
compile_ok=true, no undef-ref / undef-cite / mult-label / overfull violations; `pdf/main.pdf`
refreshed.

Convergence check vs iteration 1: iter-1 merged weaknesses (#1–#3 the exponent-1/2,
random-count, from-memory-constant in the flip remainder; #5 gram-stability uniformity) do **not**
recur — overlap with iter-2's set is 0 (the iter-2 set is a fresh, lower-severity layer). No
convergence stall.
