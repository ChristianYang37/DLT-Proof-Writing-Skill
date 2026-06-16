# Socratic intake (Phase A.1a)

Read this file at Phase A.1a — after A.1 (you can recite the target statement) and **before** A.2 (technical reconnaissance). Its job is to settle, *with the user*, the two things only the user can own: the proof's **setting** (norms, probability space, regime, what counts as a win) and its **architecture** (how the result decomposes). You ask; you wait; you do not draft until the setting is pinned.

This step runs for **every scope** — only its depth scales (see §Scope-proportional depth). A halted, well-posed problem beats a fluent proof of the wrong statement.

## Why this exists

The agent is fluent enough to silently fill every gap — pick a norm, assume a regime, choose the convenient (weaker) target — and then prove *that*. The result compiles, reads well, and answers a question the user never asked. The honesty protocol catches this mid-proof; the Socratic intake catches it before a single line is written, when correction is free. The discipline is **co-pilot, not autopilot**: surface the fork, propose the principled default, let the user steer.

## The protocol

1. **Ask only what is genuinely user-owned.** A question belongs here only if *you cannot answer it from the task, the codebase, or a textbook fact*. Which norm the theorem is stated in is user-owned; which inequality bounds a sum is not — research that yourself in A.2. Do not outsource your own work as a question (violates the conciseness principle).
2. **One mathematical decision per question.** No compound "and also" questions. Each maps to exactly one downstream commitment (a symbol, a regime, a lemma boundary).
3. **Always propose a concrete default.** Never ask an open "what do you want?". Ask: *"I propose X (the stronger option) because <reason>; the alternative is Y, which buys <tradeoff>. Which?"* — the same shape as the honesty protocol's specific-paths-forward (SKILL.md §Honesty protocol).
4. **The default is the STRONGER / TIGHTER option, never the more convenient one.** If unsure whether to target a `\poly`-slack bound or a tight constant, default-propose the tight one. A blank is never license to silently choose the easier path.
5. **Batch, then block.** Collect all questions for this scope into a single numbered list, ask once, and **end your turn**. Do not draft preliminaries while waiting. Resume only when the user answers.
6. **Delegation is explicit.** If the user says "you decide" (for the whole list or one item) — or you are running autonomously with no interactive user (eval / headless mode) — adopt your proposed (stronger) default and **record each decision in `<project-root>/.proof-research/decisions.md`** (schema below) plus the Phase A report. **Do NOT write `\todo{user-decision: ...}` into the `.tex`.** Inline `\todo` is reserved for genuine *open* `\todo{verify: ...}` gaps that still need human checking; auto-resolved setting choices are not gaps, and rendering them inline only clutters the PDF. Silence is not delegation — in interactive mode keep waiting unless the user explicitly defers.

   `.proof-research/decisions.md` entry schema (one block per decision):

   ```markdown
   ## <dimension> (e.g. constant-discipline / norm / target-form)
   **Chosen:** <option adopted> — <one-line reason it is the stronger/tighter default>
   **Alternative:** <option not taken>
   **Reversible:** <yes/no — what in the proof changes if the user flips this>
   ```

## What to settle

Two groups. Skip any item the user already specified in the task — echo your reading of it back instead of re-asking ("I'm reading the norm as spectral; correct?").

### A — Setting (the formal problem)

| Dimension | The question pins down | Default to propose |
|---|---|---|
| **Target form** | equality / inequality / high-probability / asymptotic-rate / exact-constant | the strongest form the task plausibly supports |
| **Norm & space** | which norm ($\ell_2$, operator, Frobenius, $\ell_\infty$), which probability space / filtration | the norm the surrounding paper uses; else the one making the claim strongest |
| **Regime** | asymptotic vs finite-sample; which parameter $\to\infty$; overparam vs classical | finite-sample / non-asymptotic (stronger) |
| **Constant discipline** | tight constants vs `\poly`-slack vs absorbed universal $C$ | tight where the task implies a sharp result; else declare `\poly`-slack explicitly |
| **Win condition** | what counts as "done" — a rate? a phase transition? a matching lower bound? | the user's headline claim, stated at its strongest |
| **Citations** | which results are pre-approved to cite vs must be proved/researched from scratch | research-from-scratch unless the user names an allowed source |

### B — Architecture (the decomposition)

| Dimension | The question pins down | Default to propose |
|---|---|---|
| **Decomposition axis** | split along assumptions, along a lemma sequence, or warmup→main | the shallowest tree that fits (SKILL.md A.4) |
| **Lemma boundaries** | which intermediate results are named lemmas vs inline steps | name a result only if it has ≥ 1 downstream consumer (Occam) |
| **Reductions off-limits** | any technique the user wants avoided (e.g. "do not reduce to ETH") | none, but ask if the natural reduction is contentious |

For Setting, ask before A.2 so reconnaissance targets the right tools. For Architecture, you may ask a second short round *after* you sketch the dependency graph (A.4–A.5) if the graph surfaces a genuine fork — but propose the graph, don't ask the user to invent it.

## Question format

```
Phase A.1a — decisions I need before drafting:

Q1 [norm]: Should Theorem 1 be stated in the operator norm or the Frobenius norm?
  Proposed: operator norm — it gives the tighter, dimension-free bound and matches §3.
  Alternative: Frobenius — easier to prove, loses a √d factor.
  Why it matters: sets the concentration tool in A.2 (matrix Bernstein vs vector).

Q2 [regime]: Finite-sample for all n, or asymptotic n→∞?
  Proposed: finite-sample (non-asymptotic) — strictly stronger.
  Alternative: asymptotic — lets us drop lower-order terms.
  Why it matters: decides whether constants must be tracked explicitly.

(End turn. Wait for answers. Do not start Phase A.2.)
```

## Scope-proportional depth

Depth scales with `.proof-research/scope.md` (set in A.0a); the step never disappears.

- **Quick** — 1–2 questions, Setting only (typically just *target form* + *norm/space*). One short batch.
- **Standard** — full Setting group + the *decomposition axis* question.
- **Appendix** — full Setting + full Architecture, and the optional post-A.4 graph-confirmation round.

If a scope has genuinely nothing underspecified (rare — the user handed you a fully-pinned statement), say so explicitly ("Setting is fully specified by the task; no intake questions") rather than skipping silently — that record is the audit trail.

## How answers feed forward

- **A.2 reconnaissance** uses the Setting answers to pick which techniques to digest (the norm/regime decide the concentration tool, the constant discipline decides whether tightness-sensitive digests are needed).
- **A.4–A.5 decomposition** uses the Architecture answers as the skeleton; every lemma still needs a non-empty `Downstream consumers` field.
- **A.6** becomes a *residual* check: surface only ambiguity newly discovered during decomposition, not the Setting questions already answered here.
- **Phase A report** lists every decision with the option finally adopted, mirroring the entries in `.proof-research/decisions.md` (delegated/autonomous choices live there, not as inline `\todo`).

## Anti-patterns

- **Checklist dump.** Firing all 9 dimensions at a Quick single-lemma task. Match depth to scope; ask the fewest questions that pin the problem.
- **Open-ended asking.** "What probability space?" with no proposal. Every question carries a defaulted, justified recommendation or it is not ready to ask.
- **Convenient defaults.** Proposing the `\poly`-slack target because it is easier to prove. The default is the stronger claim; the user downgrades, not you.
- **Asking what you should research.** "Which inequality bounds this sum?" is an A.2 task, not an intake question. Reserve the user's attention for what only they can decide.
- **Drafting while waiting.** Writing preliminaries before the user answers. The step is blocking by design — an answer can invalidate the macros you would have written.
