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
| softmax probability vector | `p` | `p` | — | `p : V → ℝ`; `p_c` is the model probability of token `c` |
| softmax probability of `c` | `p c` | `p_c` | — | entry of `p` at token `c` |
| vocabulary token (summed) | `c` | `c` | — | ranges over all of `\Vocab` in the gradient sum |
| one-hot target indicator | `if c = a_star then 1 else 0` | `\indicator{c = \astar}` | `\newcommand{\indicator}[1]{\mathbf{1}\!\left[#1\right]}` | the one-hot answer vector `e_{a⋆}` entry; `= 1` iff `c = a⋆` |
| softmax residual at `c` | `p c - (if c = a_star then 1 else 0)` | `p_c - \indicator{c = \astar}` | — | entry of the residual `p − e_{a⋆}` |
| per-token Gram gap | `⟪W a_star, W c⟫ - ⟪W b, W c⟫` | `\inner{W_{\astar}}{W_c} - \inner{W_b}{W_c}` | — | `(W a⋆ − W b)` paired with row `W c` |
| softmax-residual separation score | `∑ c, (p c - (if c = a_star then 1 else 0)) * (⟪W a_star, W c⟫ - ⟪W b, W c⟫)` | `\sum_{c}\bigl(p_c - \indicator{c = \astar}\bigr)\bigl(\inner{W_{\astar}}{W_c} - \inner{W_b}{W_c}\bigr)` | — | the cross-entropy separation functional for competitor `b` |
| cross-entropy gradient (vocab sum) | `∑ c, (p c - (if c = a_star then 1 else 0)) • W c` | `\sum_{c}\bigl(p_c - \indicator{c = \astar}\bigr) W_c` | — | `∇L = Wᵀ(p − e_{a⋆})` as a sum over `\Vocab` |

### 2nd layer — bridge (verified) + dynamics (cited), `sections/04-bridge-and-dynamics.tex`

| role | lean ident | latex | macro / def site | notes |
|---|---|---|---|---|
| single-token cross-entropy loss | `lossCE W a_star x` | `\loss(x)` | `\newcommand{\loss}{L}` | `= \log(\sum_c \exp\inner{W_c}{x}) - \inner{W_{\astar}}{x}` = `−log p_{a⋆}(x)` |
| logit of token `c` | `⟪W c, x⟫` (`ℓ c`) | `\logit{c}` = `\ell_c` | `\newcommand{\logit}[1]{\ell_{#1}}` | `ℓ_c := \inner{W_c}{x}`; abbreviation `set ℓ` in `Bridge.lean` |
| softmax partition | `Z = ∑ c, Real.exp (ℓ c)` | `\Zpart` = `Z` | `\newcommand{\Zpart}{Z}` | `Z := \sum_c \exp(\ell_c)`; abbreviation `set Z` in `Bridge.lean` |
| log-2 decode threshold | `Real.log 2` | `\log 2` | — | bridge fires when `\loss(x) < \log 2` (i.e. `p_{a⋆} > 1/2`) |
| competitor sum (erase a⋆) | `∑ c ∈ Finset.univ.erase a_star, Real.exp (ℓ c)` | `\sum_{c \ne \astar} \exp(\ell_c)` | — | combined softmax mass of all competitors |
| suboptimality margin (B2, cited) | — | `\optgap` = `\Delta` | `\newcommand{\optgap}{\Delta}` | `\Delta := \log 2 - \lossopt > 0`; NOT a Lean symbol (classical part) |
| optimal loss value (B2, cited) | — | `\lossopt` = `L^{\star}` | `\newcommand{\lossopt}{\loss^{\star}}` | `\lossopt := \inf_x \loss(x)`; classical part |
| decode-time threshold (B2, cited) | — | `\tstar` = `t^{\star}` | `\newcommand{\tstar}{t^{\star}}` | `\tstar := \smooth\norm{x_0-x^\star}^2/(2\optgap)`; classical part |
| success rate over problems (B2) | — | `\passat{T}` = `\mathrm{pass}@T` | `\newcommand{\passat}[1]{\mathrm{pass}@#1}` | `\passat{T} := \Pr_Q[\optgap(Q)>0 \wedge \tstar(Q)\le T]`; classical part |
| smoothness constant (B2, cited) | — | `\smooth` = `\beta` | `\newcommand{\smooth}{\beta}` | `\loss` is `\smooth`-smooth on the sphere; classical part |
| GD step size (B2, cited) | — | `\stepsize` = `\eta` | `\newcommand{\stepsize}{\eta}` | `\stepsize = 1/\smooth`; classical part |
| logical implication | — | `\implies` | amsmath builtin (`\Longrightarrow`) | standard connective in `lem:bridge` statement; not an invented symbol |

## Statement-level renderings (for Phase E)

- Main iff:
  `\Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \mu\,\inner{W_{\astar} - W_b}{\grad\loss(\xstar)} > 0`
- Corollary (μ<0):
  `\Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \inner{W_{\astar} - W_b}{-\grad\loss(\xstar)} > 0`
- Corollary (failure characterization):
  `\neg\,\Generated(\astar, \xstar) \iff \exists b \ne \astar,\ \mu\,\inner{W_{\astar} - W_b}{\grad\loss(\xstar)} \le 0`
- Corollary (cross-entropy instantiation):
  `\Generated(\astar, \xstar) \iff \forall b \ne \astar,\ \mu \sum_{c}\bigl(p_c - \indicator{c = \astar}\bigr)\bigl(\inner{W_{\astar}}{W_c} - \inner{W_b}{W_c}\bigr) > 0`
- Stationarity hypothesis: `\grad\loss(\xstar) = \mu\,\xstar`.
- Cross-entropy gradient hypothesis: `\grad\loss(\xstar) = \sum_{c}\bigl(p_c - \indicator{c = \astar}\bigr) W_c`.
- Sphere hypothesis: `\norm{\xstar} = r`.
