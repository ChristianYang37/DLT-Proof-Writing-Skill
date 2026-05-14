# Anti-patterns

Read this file once at the start of Phase C (before writing your first derivation) and again at Phase D (end-to-end review). The third section — AI-specific failure modes — is the highest-priority part; skim it whenever you notice yourself producing fluent prose around an uncertain step.

## Contents

1. [Mathematical anti-patterns](#mathematical-anti-patterns)
2. [Exposition anti-patterns](#exposition-anti-patterns)
3. [AI-specific failure modes](#ai-specific-failure-modes-highest-priority) — read carefully

---

## Mathematical anti-patterns

- **Inventing constants.** "For some constant $C > 0$" without describing what $C$ depends on. State the dependency: "$C > 0$ depending only on $d$ and $L$".
- **Silent regularity assumptions.** Slipping in "assuming $f$ is sufficiently smooth" mid-proof when no smoothness assumption is in the preliminaries.
- **Quantifier swaps.** Writing "for all $x$, there exists $C$ ..." when the proof requires "there exists $C$, for all $x$". A frequent silent bug.
- **High-probability ↔ expectation conflation.** $\E[X] \le \varepsilon$ does not imply $X \le \varepsilon$ with high probability without further argument.
- **Dropping subsidiary width/sample requirements.** Lemma A needs $m \ge n^4$, Lemma B needs $m \ge n^5$ — the theorem must require $m \ge n^5$ (the max), not just one of them.
- **"By standard concentration" without specifying.** Name the concentration inequality: Hoeffding, Bernstein, McDiarmid, Azuma, sub-Gaussian tail, matrix Bernstein. If you cannot name it, you do not know it applies.

## Exposition anti-patterns

- **Trailer / row mismatch.** Trailer says "the second step follows from the triangle inequality" but the second row is an equality, not the triangle-inequality step. Recount before submitting.
- **Bundled definitions.** One `\begin{definition}` containing four unrelated objects. Split.
- **Used-once macros.** `\newcommand{\foo}{X}` then `\foo` appears once. Inline it.
- **Over-decoration of the headline.** Cramming three different rates with `\colvec{}` annotations into a body-version statement that is supposed to be informal. Save decoration for the formal version.
- **Padding with `\poly` slack the user did not ask for.** If the user wants tight constants, do not bury them in `\poly(\cdot)`. Ask which level of precision they want.
- **Shared-counter `\newtheorem` without `aliascnt`.** Writing `\newtheorem{lemma}[theorem]{Lemma}` / `\newtheorem{assumption}[theorem]{Assumption}` / etc. compiles cleanly and numbers correctly, but makes every `\Cref{lem:foo}` / `\Cref{ass:foo}` / `\Cref{def:foo}` / `\Cref{fac:foo}` render as **"Theorem X.Y"** in the PDF, because cleveref keys its name lookup on the counter name (always `theorem` here), not the environment name. The bug is silent at compile time. **Always use the `aliascnt` template in [conventions.md](conventions.md) §Theorem-environment preamble**, and spot-check the rendered PDF (see [quality-checks.md](quality-checks.md) §LaTeX compilation gate, item 3).

## AI-specific failure modes (highest priority)

These are failure modes that human authors rarely commit but that AI-written proofs are uniquely prone to. They are also the failure modes that get past you most easily — they wear the disguise of fluent prose. Treat them as red flags whenever you notice them in your own output.

- **Fabricated references.** Inventing `\cite{authoryear}` keys, theorem numbers ("Theorem 4.2 of [Foo20]"), or `\ref` targets you have not verified.
  **Defense:** before any `\cite{...}` that names a specific theorem/lemma by number, run a **citation digest** — download the PDF, find the exact theorem number and statement, save to `.proof-research/cite-<author><year>-<slug>.md`, then cite from the digest. See [technical-research.md](technical-research.md) §Citation digests for cited prior work. If you cannot run the digest (no internet, paywalled paper without user access), leave `\todo{verify: claim X attributed to [Foo20]}` and ask the user.

- **Hallucinated lemma applications.** Citing `\Cref{lem:foo}` when Lemma foo's hypotheses are *not* met at this point in the proof.
  **Defense:** before each `\Cref{lem:foo}`, re-state Lemma foo's hypotheses in a mental check, then verify each one is established locally.

- **Confident interpolation.** Bridging two steps with a fluent English sentence that hides a missing argument: *"By a standard argument, this implies ..."*; *"It is clear that ..."*; *"A straightforward calculation gives ..."*.
  **Defense:** if you wrote any of these phrases, the next step must in fact be straightforward — otherwise expand it. "Standard" and "clear" are red flags in your own draft.

- **Plausible but wrong algebraic manipulation.** Mis-applying Cauchy-Schwarz, Jensen's inequality, or matrix-norm submultiplicativity in a direction that looks right but isn't.
  **Defense:** for any non-trivial algebraic step, write out the named inequality being used in the trailer/legend; if you cannot name a single one, the step is suspect.

- **Smoothing over a missing case.** Proof handles "Case 1: $\|x\| \ge 1$" cleanly, then writes "the other case is similar" when the other case requires materially different machinery.
  **Defense:** if the cases are genuinely symmetric, prove the symmetry. If they are not, write the second case out.

- **Notation drift.** Subscript starts as $i$, becomes $j$ midway, then $i$ again — usually a translation artifact between two derivations you mentally merged.
  **Defense:** read the proof from top to bottom looking only at indices, separately from logic.

- **Probability budget invented at the end.** Writing "with probability $1 - \delta$" in the conclusion without having explicitly union-bounded the $k$ events on which the proof depends.
  **Defense:** any high-probability conclusion must end with an explicit union-bound paragraph that names each event and its failure probability.

- **Phantom optimization.** Claiming "setting $\eta = c \lambda_0 / n^2$ minimizes the bound" without showing the derivative calculation.
  **Defense:** if you optimize a parameter, write the first-order condition or quote the elementary inequality (AM-GM, Young) that gives the optimum.

- **Memory-recalled tool statement.** Writing a derivation that invokes a concentration inequality or perturbation lemma from memory, when a digest in `.proof-research/` already covers it.
  **Defense:** before writing a step that uses a non-trivial technique, open the corresponding digest from [technical-research.md](technical-research.md). Do not write from memory if a digest exists.

- **Skipping the confidence sweep / self-marking 🟢.** Treating your own derivation as verified because it "feels right" — or skipping Phase C.5 entirely on a Standard-scope task because the proof is "short enough".
  **Defense:** run Phase C.5 ([confidence-sweep.md](confidence-sweep.md)) for any Standard or Appendix-grade proof. The only paths to 🟢 are: (a) named textbook inequality you can cite, (b) sub-agent independent re-derivation match, (c) script validation. Self-belief alone keeps the step at 🔴.

When you catch yourself producing any of these, stop, mark `\todo`, and ask the user. Do not paper over.
