import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# Settings — single-token LLM decoding on the LayerNorm sphere

A deterministic, finite-dimensional characterization of single-token decoding under
implicit-loss optimization on the LayerNorm sphere. **No probability, no asymptotics** —
pure inner-product geometry plus a first-order optimality hypothesis.

All objects below are the user-approved encodings (frozen in `statement.lock`).

## Carrier and vocabulary
* `E` — a real inner product space (e.g. `EuclideanSpace ℝ (Fin d)`); `[CompleteSpace E]`
  is required only so that Mathlib's `gradient` is well-defined (it is the Riesz
  representative of the Fréchet derivative). `EuclideanSpace ℝ (Fin d)` and every real
  Hilbert space satisfy it, so generality is preserved.
* `V` — a finite vocabulary with at least two tokens (`Fintype V`, `Nontrivial V`).
* `W : V → E` — the unembedding; `W a` is the row of token `a`.

## Sphere
* `r : ℝ`, `0 < r`. The LayerNorm sphere is `{x : ‖x‖ = r}`. Only `‖x⋆‖ = r` is ever used
  as a hypothesis (and, in fact, the proof needs only `μ ≠ 0`); see `.proof-research/decisions.md`.

## Loss
* `L : E → ℝ` is the implicit loss. It is intended to be **differentiable**; this is a
  *setting remark*, not a load-bearing hypothesis — the proof never differentiates `L`, it
  only uses the value `gradient L x⋆` through the stationarity hypothesis. Keeping
  `Differentiable ℝ L` out of the theorem hypotheses is the Occam-faithful choice
  (see `.proof-research/decisions.md`, D2). `gradient L x⋆` is Mathlib's `gradient`.

## Decoder
Single-token (`n = 1`), so the greedy argmax **is** the true decoder. Token `a` is
generated at `x` iff `x` lies in the open decoding cone of `a`:
`∀ b ≠ a, ⟪W a, x⟫ > ⟪W b, x⟫`.

## Stationarity
"Reasoning settled (even inefficiently) at a constrained stationary point `x⋆` on the
sphere" is encoded **only** as the first-order (Lagrange) condition
`∃ μ, gradient L x⋆ = μ • x⋆` (ambient gradient normal to the sphere ⟺ Riemannian gradient
zero). In the theorems the multiplier `μ` and the witness equation are taken as hypotheses;
no convexity, global minimality, or convergence rate is assumed.
-/

open RealInnerProductSpace

namespace Decode

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable {V : Type*}

/-- **Decoder (greedy argmax = true decoder, single-token).**
Token `a` is *generated at* `x` iff `x` lies in the open decoding cone of `a`: the row
`W a` has strictly larger inner product with `x` than every other row `W b`, `b ≠ a`. -/
def Generated (W : V → E) (a : V) (x : E) : Prop :=
  ∀ b, b ≠ a → ⟪W a, x⟫ > ⟪W b, x⟫

/-- **Single-token cross-entropy loss (`L`).**
The negative log-likelihood the model assigns to the answer token `a⋆` at hidden state `x`,
i.e. `−log` of the softmax probability of `a⋆`:
`L(x) = log (∑_c exp ⟪W c, x⟫) − ⟪W a⋆, x⟫`.
The first term is the log-partition (`log Z`) of the logits `⟪W c, x⟫`; subtracting the
answer logit `⟪W a⋆, x⟫` gives exactly `−log p_{a⋆}(x)`. Requires `[Fintype V]` so the
partition sum is finite. (Convexity — log-sum-exp minus a linear term — is a classical
property recorded in `sections/04-bridge-and-dynamics.tex`; it is *not* used in the
machine-verified bridge below.) -/
noncomputable def lossCE [Fintype V] (W : V → E) (a_star : V) (x : E) : ℝ :=
  Real.log (∑ c, Real.exp ⟪W c, x⟫) - ⟪W a_star, x⟫

end Decode
