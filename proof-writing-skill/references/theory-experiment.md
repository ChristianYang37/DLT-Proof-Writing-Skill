# Experiment design (separate from the proof)

Read this file only when the user explicitly asks for experiments alongside the theory. Otherwise skip — experiments are optional artifacts, not part of the proof workflow.

## Hard rules

1. **Design only — never fabricate results.** Your output is a **plan**: datasets, models, baselines, metrics, expected behavior tied to specific theorems. You do not invent numerical values, fitted slopes, accuracy numbers, or experimental conclusions. The user runs the experiments and fills in actual results afterward. If you find yourself writing "Figure 1 shows that our method achieves X% improvement", you have crossed the line — delete it.

2. **Output to a separate markdown file, never into the `.tex`.** The proof PDF stays clean of empirical content. Write the experiment plan to `<project-root>/experiments-plan.md` (or `experiments-plan-<theorem-slug>.md` if the project has multiple theorems with distinct empirical claims). The user reads this file when running experiments; it is **never** `\input{}`-ed into `main.tex` and never appears in the compiled PDF.

3. **Target ICML / NeurIPS / ICLR theory-track empirical rigor.** This is not "run on one dataset, plot a curve, ship." Minimum bar:
   - **≥ 5 random seeds**; report mean ± std (or 95% CI) over seeds. Never single-run numbers.
   - **At least one baseline** (random init / kernel-regression closed-form / prior method).
   - **At least one ablation** if the theory has multiple components.
   - **Multiple settings** (data sizes, dimensions, hyperparameters) sweeping the regime the theory predicts.
   - **Hyperparameter protocol** stated up front (grid / random / principled-from-theory; with budget).
   - **Compute reporting** (rough GPU-hours, hardware class).
   - **Reproducibility**: seeds, config file paths, code references, library versions.

4. **Experiments verify theorems, not benchmark unrelated tasks.** Every plot or table must correspond to a specific theoretical claim or assumption. Caption pattern: *"This figure verifies \Cref{lem:gradient_lb} by measuring ..."*. If a proposed experiment doesn't map to a specific claim, drop it. Generic CIFAR-10 accuracy when the theorem makes no statement about CIFAR-10 is not relevant.

5. **Pre-register success criteria before running.** State in the plan what empirical outcome *confirms* the theory and what *refutes* it. This protects against post-hoc adjustment of success thresholds.

## experiments-plan.md schema

```markdown
# Experiments plan: <theorem / paper name>

## Theoretical claim
One paragraph restatement of the claim, with `\Cref{thm:foo}` reference.
What quantity does the theory predict? In what regime? What rate or behavior
is expected as $n, d, \varepsilon, \ldots$ vary?

## Empirical hypothesis
The specific empirical prediction derived from the claim. E.g.:
- "Training loss decays as $(1 - \eta \lambda_0 / 2)^k$ → log-loss vs.
  iteration should be linear with slope $\log(1 - \eta \lambda_0 / 2)$."
- "Distance from init $\|W^{(t)} - W^{(0)}\|_F = O(1/\sqrt{m})$ at fixed $t$."

## Setup

### Data
- Generation process or dataset name (with reference / formula).
- Sample sizes to sweep: $n \in \{ \ldots \}$.
- Input dimension: $d \in \{ \ldots \}$.

### Model
- Architecture (if applicable).
- Width / depth sweep ranges.
- Initialization scheme (named + cited).

### Training
- Optimizer (GD / SGD / Adam ...) with reason (theory uses which?).
- Step size formula (often `η = c · λ_0 / n^2` computed from data).
- Iterations / epochs.
- Loss function (matching the proof's loss).

### Random seeds
List 5–10 seeds explicitly. E.g. `[1, 2, 3, 4, 5]`.

### Compute estimate
GPU-hours / CPU-hours; hardware class.

## Metrics

| Metric | What it measures | Verifies |
|---|---|---|
| <metric 1> | <description> | `\Cref{thm:main}` |
| <metric 2> | <description> | `\Cref{lem:stay_in_ball}` |

Every metric must point at one theoretical claim. Drop any that don't.

## Baselines
- **B1:** <name> — <why included; what comparison this enables>
- **B2:** ...

## Ablations
- **A1:** vary <param> over <range> — predicted effect: <effect>
- **A2:** ...

## Plots and tables to produce

- **Figure 1**: <what it shows>. X-axis: <…>. Y-axis: <…>. Lines: <…>.
  Error bars: ±1 std over <N> seeds. **Predicts**: slope / value matches
  <quantity from theorem>. **Verifies**: `\Cref{thm:foo}`.
- **Figure 2**: ...
- **Table 1**: ...

## Pre-registered success criteria

- **Confirms theory**: <specific quantitative outcome — slopes within ±X%,
  rates within constant factor, etc.>
- **Refutes theory**: <specific outcome that would falsify>

## Reproducibility statement
- Code path / repo: <path or "to be released">
- Seeds: `[1, 2, 3, 4, 5]`
- Configs: <list of config files>
- Library versions: <e.g., `torch 2.3.0`, `numpy 1.26.0`>
- Hardware: <CPU/GPU model>

---

## Results

**Leave this section blank.** The user fills it in after running experiments.
Do NOT populate with imagined numbers, predicted-as-actual values, or
placeholder rows like "TODO: 0.95".
```

## Anti-patterns

- **Fabricating numbers.** "Figure 1 confirms the theory with R²=0.97" using invented data. Never. The Results section stays blank until the user runs.
- **Generating fake plots.** Writing code that emits dummy data and treating that as experimental output. Code that *would* run on real data is fine — pretending the output is real is not.
- **Polluting the .tex.** No `\section{Experiments}` in `main.tex`. The PDF is the proof. The experiment design is a separate `.md` file.
- **Generic benchmarks unrelated to theory.** "We test on CIFAR-10" when the theorem makes no CIFAR-10 prediction. Empirical claims must be implied by the theorem.
- **Single-seed claims.** "We observe linear convergence" from one run. Re-run with ≥ 5 seeds; report mean ± std.
- **Cherry-picked baselines.** Compare against the strongest relevant prior method, not a weak strawman.
- **Adjusting success criteria after seeing data.** Pre-register what counts as confirmation before running; do not relax the threshold post-hoc.
- **Writing a Discussion / Limitations section without data.** Discussion belongs after results. If there are no results yet, there is nothing to discuss.
