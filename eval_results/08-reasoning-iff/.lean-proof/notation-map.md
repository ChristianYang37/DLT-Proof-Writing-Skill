# Notation map (Lean ident ↔ LaTeX macro)

Seeded in Phase B from the user-approved notation; grown in Phase D for any new `set`/`let`.
Every `@lx latex` symbol in the Lean proof and every symbol in the generated `.tex` draws
from this table. LaTeX column uses the project macros defined in `macros.tex`.

| role | lean ident | latex | macro / def site | notes |
|---|---|---|---|---|
| carrier (inner product space) | `E` | `E` | — | real `InnerProductSpace ℝ E`, `[CompleteSpace E]` |
| vocabulary | `V` | `\Vocab` | `\newcommand{\Vocab}{\mathcal{V}}` | finite, `Nontrivial` (≥ 2 tokens) |
| unembedding | `W` | `W` | — | `W : V → E`; row of token `a` is `W a` |
| token row of `a` | `W a` | `W_{a}` | — | `W` applied to token `a` |
| inner product | `⟪x, y⟫` | `\inner{x}{y}` | `\newcommand{\inner}[2]{\left\langle #1, #2 \right\rangle}` | real inner product `⟪·,·⟫_ℝ` |
| norm | `‖x‖` | `\norm{x}` | `\newcommand{\norm}[1]{\left\| #1 \right\|}` | |
| sphere radius | `r` | `r` | — | `0 < r` |
| LayerNorm sphere | `{x : ‖x‖ = r}` | `\Sphere` | `\newcommand{\Sphere}{\mathcal{S}_r}` | membership `x ∈ \Sphere ⟺ \norm{x}=r` |
| implicit loss | `L` | `\loss` | `\newcommand{\loss}{L}` | differentiable (setting remark) |
| gradient at `x⋆` | `gradient L x_star` | `\grad \loss(\xstar)` | `\newcommand{\grad}{\nabla}` | Mathlib `gradient`; ambient ∇L |
| stationary point | `x_star` | `\xstar` | `\newcommand{\xstar}{x^{\star}}` | on the sphere |
| designated token | `a_star` | `\astar` | `\newcommand{\astar}{a^{\star}}` | the answer token a⋆ |
| competitor token | `b` | `b` | — | ranges over `b ≠ a⋆` |
| Lagrange multiplier | `μ` | `\mu` | — | `μ ≠ 0`; sign(μ) carries the orientation |
| decoder predicate | `Generated W a x` | `\Generated(a, x)` | `\newcommand{\Generated}{\mathsf{Gen}}` | `∀ b ≠ a, \inner{W_a}{x} > \inner{W_b}{x}` |
| competitor gap vector | `W a_star - W b` | `W_{\astar} - W_b` | — | the difference row |
| descent direction | `-gradient L x_star` | `-\grad\loss(\xstar)` | — | `−∇L(x⋆)`, the steepest-descent direction |

## Statement-level renderings (for Phase E)

- Main iff:
  `\Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \mu\,\inner{W_{\astar} - W_b}{\grad\loss(\xstar)} > 0`
- Corollary (μ<0):
  `\Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \inner{W_{\astar} - W_b}{-\grad\loss(\xstar)} > 0`
- Stationarity hypothesis: `\grad\loss(\xstar) = \mu\,\xstar`.
- Sphere hypothesis: `\norm{\xstar} = r`.
