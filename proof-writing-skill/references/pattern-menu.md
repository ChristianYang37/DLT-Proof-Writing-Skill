# Pattern menu by proof type

Read this file at Phase A.5, immediately before drawing the dependency graph. The table maps the *type* of proof you are writing to the **organizational patterns** that fit it. For statement templates and derivation idioms themselves, see [templates.md](templates.md).

## How to use

1. Identify which row in the table best matches your current proof.
2. Adopt the listed organizational patterns wholesale; they compose well.
3. Pick **one** decomposition pattern and **one** derivation pattern (from [templates.md](templates.md)) and apply uniformly. Mixing styles within a single proof is a tell of carelessness.

## The menu

| Proof type | Primary patterns |
|---|---|
| **Over-parameterized NN convergence** | Three-lemma NTK skeleton (init Gram concentration, perturbation stability, stay-in-ball) + successful-event conditioning + induction on iterates |
| **Non-convex landscape** (matrix completion, neural collapse) | KKT-condition decomposition + warmup-then-general layered proof + inline `\tag{}` justifications |
| **Fine-grained complexity / lower bounds** | SETH (or OVH/3SUM) as `\begin{hypothesis}` + reduction to intermediate gap problem + theorem-as-wrapper (the headline theorem proof is a 2-line citation of two named lemmas) |
| **Statistical learning rates** | Approximation + estimation triangle + bias/variance `\underbrace` annotation on the bound + minimax lower bound paired with upper bound + optimize $N$ at the very end |
| **Optimization / mean-field dynamics** | Continuous-time ODE first, discretize second + Lyapunov decomposition into named terms $A, B, C$ + Gronwall closure |
| **RL / bandit regret** | Successful-event conditioning + regret decomposition into $T_1 + T_2 + T_3$ + per-term lemma + elliptical-potential or self-normalized concentration |
| **Attention / fine-grained algorithmic** | Phase decomposition into paired (Correctness, Complexity) lemmas + `\underbrace{·}_{a \times b}` shape annotation + nano-roadmap per (sub)section |
| **Multi-stage dynamics** (edge-of-stability, CoT, ICL) | Heuristic-derivation-then-rigorous pattern + `\paragraph{Stage k}` decomposition + time horizon as sum $t = t_1 + t_2 + \ldots$ |

If your proof spans multiple rows (e.g., NN convergence with RL flavor), pick the row that dominates the dependency graph and borrow auxiliary patterns from the secondary row.

## When none of the above fit

If the proof does not match any row, fall back to the universal defaults:

- **Decomposition**: depth-graph of named lemmas, ≤ 3 levels deep.
- **Derivation**: trailing-justification block (see [templates.md](templates.md) §Derivation patterns).
- **Boundaries**: one-sentence strategy at proof start; explicit closing cue.

And ask the user whether the proof type warrants its own pattern.
