# Notation, macros, labels, cross-references, voice

Read this file at Phase A.0 (project context discovery), and again whenever you set up a new appendix file or write a notation block. **Project conventions outrank everything in this file** — if `math_macros.tex` already defines `\E` or the existing chapters use `\ref` instead of `\Cref`, match what's already there.

## Project file structure

Proofs are written **one section per `.tex` file**, `\input`-ed into `main.tex`. Never write multiple proofs inline in `main.tex`; never inline a proof inside the file that imports it. The pattern:

```
project/
├── main.tex                 # short: preamble + \input chain + \end{document}
├── macros.tex               # \newcommand definitions, theorem env setup (aliascnt)
├── refs.bib
└── sections/
    ├── 01-preliminaries.tex     # notation, assumptions, definitions
    ├── 02-main-result.tex       # the headline theorem statement
    ├── 03-proof-of-thm-A.tex    # one .tex per proof
    ├── 04-proof-of-thm-B.tex
    ├── ...
    └── 99-auxiliary.tex         # auxiliary lemmas used across multiple proofs
```

`main.tex` is short and stable. Adding a new proof = create a new `sections/<NN>-proof-of-<slug>.tex` + add one `\input{sections/<NN>-proof-of-<slug>}` line in `main.tex`. This:

- Keeps git diffs scoped to the proof you're editing.
- Lets multiple proofs be drafted / reviewed / compiled-checked independently.
- Makes the dependency graph (Phase A.4) directly correspond to the file tree.
- Avoids merge conflicts when multiple proofs evolve in parallel.

**Do NOT write an abstract or introduction.** This skill writes formal content (theorems, lemmas, proofs). The user owns the paper's framing — abstract, introduction, related work, conclusion. If those sections appear in the project, treat them as read-only — match their notation but do not edit them. If the user later asks for an abstract or intro, that is a separate task with different conventions and is out of scope here.

### Theorem ↔ proof pairing (hard rule, lint R5)

Every `\begin{theorem}` / `\begin{lemma}` / `\begin{proposition}` / `\begin{corollary}` / `\begin{claim}` must satisfy **exactly one** of:

1. **Followed by `\begin{proof}` in the same file** — the FIRST environment after `\end{X}` must be `\begin{proof}` (or `\begin{proof}[Proof of \Cref{X}]`). Whitespace, comments, and `\label{}` outside any env are allowed between, **but no intervening environments** (no `\begin{remark}`, no other `\begin{lemma}`, etc.).
2. **Cited via the optional bracket** — `\begin{X}[\cite{author20...}]` for external results whose proof you do not want to reproduce. The cite key must resolve in `refs.bib`.

**Forbidden:** a theorem-like result with neither proof nor citation — the "well-known result" handwave.

**File-structure consequence.** Put a theorem and its proof **in the same `.tex` file**. The pattern `02-main-result.tex` (theorem only) + `06-proof-of-main.tex` (proof) violates R5. Use instead:

```
sections/
├── 01-preliminaries.tex          # definitions / assumptions / facts
├── 02-lemma-A.tex                # \begin{lemma} + immediate \begin{proof}
├── 03-lemma-B.tex                # same
├── 04-main-theorem.tex           # \begin{theorem} + immediate \begin{proof}
└── 99-auxiliary.tex              # cited externals via [\cite{...}] form
```

If a result is genuinely external (e.g., Hoeffding's lemma cited from Vershynin 2018), use form 2. If it is yours, prove it immediately. There is no third option.

## Macros — typical project header

Place at top of `math_macros.tex` (or whatever the project calls its macros file). Do not add macros that already exist in the project.

```latex
% Asymptotics and rates
\DeclareMathOperator{\poly}{poly}
\DeclareMathOperator{\polylog}{polylog}
\newcommand{\Otil}{\widetilde{O}}
\newcommand{\Omegatil}{\widetilde{\Omega}}
\newcommand{\Thetatil}{\widetilde{\Theta}}

% Common shortcuts
\newcommand{\wt}{\widetilde}
\newcommand{\wh}{\widehat}
\newcommand{\R}{\mathbb{R}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\Pr}{\mathbb{P}}
\newcommand{\1}{\mathbf{1}}

% Norm and inner product
\newcommand{\norm}[1]{\left\| #1 \right\|}
\newcommand{\inner}[2]{\left\langle #1, #2 \right\rangle}

% Vectors / matrices — pick one convention and stay with it
\renewcommand{\vec}[1]{\mathbf{#1}}
\newcommand{\mat}[1]{\mathbf{#1}}
```

Use `\triangleq` to define a shorthand mid-derivation; `\coloneqq` or `\stackrel{\mathrm{def}}{=}` for a top-level definition. Use `\mathsf{}` for fine-grained / problem names (`\mathsf{SETH}`, `\mathsf{AAttC}`).

## Theorem-environment preamble (cleveref-safe setup)

**The trap.** The textbook `amsthm` pattern with shared numbering is

```latex
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}            % shares the theorem counter
\newtheorem{assumption}[theorem]{Assumption}  % shares the theorem counter
\newtheorem{fact}[theorem]{Fact}              % shares the theorem counter
% ...
\crefname{assumption}{Assumption}{Assumptions}  % this line will NOT take effect
```

This compiles, numbers cleanly (Theorem 1.1, Lemma 1.2, Assumption 1.3, ...), and looks correct. **But cleveref keys its name lookup on the *counter name*, not the environment name.** Because every environment shares the `theorem` counter, every `\Cref{lem:...}` / `\Cref{ass:...}` / `\Cref{fac:...}` renders as **"Theorem X.Y"** — the `\crefname{lemma}{...}`, `\crefname{assumption}{...}` registrations never fire. The bug is silent at compile time and visible only in the PDF.

**The fix.** Use the `aliascnt` package, which creates *aliased counters* that share numbering with `theorem` but are distinct counter names from cleveref's perspective. Canonical template:

```latex
\usepackage{amsthm}
\usepackage{aliascnt}
\usepackage[capitalize]{cleveref}

% Master counter
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]

% Aliased plain-style environments.
% IMPORTANT: the [lemma] / [proposition] / ... after the env name tells
% \newtheorem to use the aliascnt-created counter. Omitting it makes
% \newtheorem define a fresh counter and the subsequent \aliascntresetthe
% errors with "Command \c@<name> already defined."
\newaliascnt{lemma}{theorem}
\newtheorem{lemma}[lemma]{Lemma}
\aliascntresetthe{lemma}

\newaliascnt{proposition}{theorem}
\newtheorem{proposition}[proposition]{Proposition}
\aliascntresetthe{proposition}

\newaliascnt{corollary}{theorem}
\newtheorem{corollary}[corollary]{Corollary}
\aliascntresetthe{corollary}

% Aliased definition-style environments
\theoremstyle{definition}
\newaliascnt{definition}{theorem}
\newtheorem{definition}[definition]{Definition}
\aliascntresetthe{definition}

\newaliascnt{assumption}{theorem}
\newtheorem{assumption}[assumption]{Assumption}
\aliascntresetthe{assumption}

\newaliascnt{fact}{theorem}
\newtheorem{fact}[fact]{Fact}
\aliascntresetthe{fact}

% Aliased remark-style environment
\theoremstyle{remark}
\newaliascnt{remark}{theorem}
\newtheorem{remark}[remark]{Remark}
\aliascntresetthe{remark}

% Cleveref names — now correctly keyed
\crefname{theorem}{Theorem}{Theorems}
\crefname{lemma}{Lemma}{Lemmas}
\crefname{proposition}{Proposition}{Propositions}
\crefname{corollary}{Corollary}{Corollaries}
\crefname{definition}{Definition}{Definitions}
\crefname{assumption}{Assumption}{Assumptions}
\crefname{fact}{Fact}{Facts}
\crefname{remark}{Remark}{Remarks}
\crefname{equation}{Eq.}{Eqs.}
```

Verify by spot-checking the rendered PDF: `\Cref{lem:foo}` should render "Lemma X.Y", `\Cref{ass:foo}` should render "Assumption X.Y", etc. — never all as "Theorem X.Y".

## Itemize / enumerate / step-labeling — hard rules

These choices are surface-level but inconsistency across a paper is one of the most visible AI tells. Pick the right tool per use case and **never substitute**:

| Use case | Environment | Example |
|---|---|---|
| Hypothesis list in a statement (≥ 3 hypotheses) | `\begin{itemize}` | `\item Let $\lambda > 0$.` |
| Multi-conclusion statement (each conclusion may be referenced later) | `\begin{enumerate}[label=(\roman*)]` or `\begin{enumerate}[label=(\alph*), ref=\ref*{lem:foo}\alph*]` | `\item $\norm{\Wb^{(t)}} \le C$.` |
| Section / appendix roadmap | `\begin{itemize}` with one item per (sub)section | `\item Section \ref{sec:init} establishes ...` |
| Step decomposition inside a proof | `\paragraph{Step 1.}` or `\noindent\textbf{Step 1.}` | not bullets |
| Case decomposition inside a proof | `\noindent\textbf{Case 1.}` / `\paragraph{Case 1.}` | not bullets |
| Branch cases inside a *formula* | `\begin{cases}` or `\left\{\begin{array}{ll} ... \end{array}\right.` | not bullets |
| Per-step justification of an `align*` | **comma-chained run-on sentence** ("where the first step ..., the second step ..., ..., and the last step ...") | **never** bullets |

**Spacing.** When using `enumitem`, prefer compact list-spacing in appendix-grade proofs:

```latex
\usepackage{enumitem}
% ... and in itemize/enumerate calls:
\begin{itemize}[leftmargin=2em, itemsep=0.2em]
\item ...
\end{itemize}
```

**`ref=` is mandatory for multi-part lemmas.** If parts of a lemma will be cited individually downstream (e.g. *"By part (ii) of \Cref{lem:foo} ..."*), use:

```latex
\begin{lemma}\label{lem:foo}
The following hold.
\begin{enumerate}[label=(\alph*), ref=\ref*{lem:foo}\alph*]
\item \label{lem:foo:a} $A = B$.
\item \label{lem:foo:b} $C = D$.
\end{enumerate}
\end{lemma}
```

Then `\Cref{lem:foo:a}` renders correctly as "Lemma X.Y(a)".

**Justifications in derivations are never bulleted.** Pick the trailing-justification idiom or the letter-tagged idiom from [templates.md](templates.md) §Derivation patterns. A bulleted list of "the first step uses Cauchy-Schwarz" / "the second step uses Lemma 3.2" is wrong style for any of the conventions in the corpus.

## Math display syntax

**Never use `\[ ... \]` for display math.** Always use one of:

- `\begin{align*} ... \end{align*}` — the default. Use for any displayed equation or chain, even a single line.
- `\begin{align} ... \end{align}` — only when the display needs an equation number (i.e., when you will `\eqref` or `\Cref` to a specific line). Add `\label{eq:...}` on the line you intend to reference.

Why: `align`/`align*` is the right tool even for single-line displays — it composes uniformly with multi-line chains, supports `\notag` / `\label` on a per-line basis, and aligns at `&` for derivations. `\[ ... \]` forces a switch of environment as soon as the display grows by one line, and breaks the convention that every reference-able equation lives inside an `align`.

```latex
% Single-line display, no number
\begin{align*}
\| f(\Wb^{(T)}) - y \|_2^2 \;\le\; \varepsilon.
\end{align*}

% Single-line display, will be referenced
\begin{align}\label{eq:gd_update}
\Wb^{(t+1)} = \Wb^{(t)} - \eta \nabla L(\Wb^{(t)}).
\end{align}

% Multi-line chain, intermediate lines unnumbered, last line referenced
\begin{align}
\|\Wb^{(t+1)} - \Wb^*\|_F^2
&\le (1 - \eta \mu) \|\Wb^{(t)} - \Wb^*\|_F^2 \notag \\
&\le (1 - \eta \mu)^{t+1} \|\Wb^{(0)} - \Wb^*\|_F^2 \label{eq:contraction}.
\end{align}
```

Inline math stays in `$...$` as usual.

## Label conventions

Use a slug prefix matching the environment:

| Environment | Prefix | Example |
|---|---|---|
| Theorem | `thm:` | `\label{thm:main}` |
| Lemma | `lem:` | `\label{lem:gradient_lb}` |
| Proposition | `prop:` | `\label{prop:smoothness}` |
| Corollary | `cor:` | `\label{cor:main_corollary}` |
| Definition | `def:` | `\label{def:properties}` |
| Assumption | `ass:` | `\label{ass:data_separation}` |
| Fact | `fac:` | `\label{fac:transpose}` |
| Equation | `eq:` | `\label{eq:gd_update}` |
| Algorithm | `alg:` | `\label{alg:training}` |
| Section | `sec:` | `\label{sec:proof_main}` |

For informal/formal pairs, suffix `:informal` / `:formal`. For appendix restatements, the appendix label can be the bare slug and the body teaser carries `:informal`.

## Cross-references

- **Default to `\Cref` (cleveref)** for typed references: `\Cref{lem:gradient_lb}` renders "Lemma 3.2" automatically. This is the modern convention.
- **Equation citations: always prefix `Eq.~` before `\eqref`.** Write `Eq.~\eqref{eq:gd_update}` (renders "Eq.~(3.7)"), **not** bare `\eqref{eq:gd_update}`. The bare form drops the type name and reads as a parenthetical number in mid-sentence, which is ambiguous when the surrounding prose already contains parenthetical asides. The `Eq.~` prefix makes the reference type explicit and the non-breaking space `~` prevents the line break between "Eq." and the number. Apply this rule whenever you cite an equation in prose; the only exception is inside an `align`/`align*` `\tag{...}` argument where the tag itself already labels the line. Examples:

  ```latex
  Combining Eq.~\eqref{eq:gd_update} and Eq.~\eqref{eq:smoothness}, we obtain ...
  By Eq.~\eqref{eq:contraction}, the iterates converge linearly.
  ```

  Multi-equation cites in a single sentence: write `Eq.~\eqref{eq:a} and Eq.~\eqref{eq:b}` (repeat the prefix), not `Eq.~(\eqref{eq:a}, \eqref{eq:b})`.

- **Match existing project style.** If the project uses `Lemma~\ref{lem:foo}`, do not switch to `\Cref` mid-paper. Similarly, if the project already uses bare `\eqref` consistently, match it — but flag the inconsistency to the user.
- **Multi-references**: `\Cref{lem:a,lem:b,lem:c}` for a comma list. Do not chain three separate `\Cref` calls.

## Asymptotic notation rules

- **Informal statements / prose**: `\lesssim`, `\gtrsim`, `\asymp` (constants absorbed silently).
- **Formal statements**: explicit `O(\cdot)`, `\Omega(\cdot)`, `\Theta(\cdot)`, `\widetilde{O}(\cdot)`.
- **Polynomial dependence**: `\poly(n, 1/\lambda_0, d)`. If the exact polynomial degree matters, pin it in a `Hidden:` remark beneath the theorem or in a footnote.
- **Universal-constant convention** (state once in the notation block):
  *"Throughout, $c, C, C_1, C_2, \ldots$ denote universal positive constants whose values may change from line to line and depend only on quantities specified in each lemma's hypothesis."*
  After this is stated, use $c, C$ freely. Do not use $c$ or $C$ until this is stated.
- **Problem-dependent constants must show their dependency at the symbol level.** If a constant depends on $\lambda_0, L, d$, write `$C_{\lambda_0, L, d}$` or `$c(\lambda_0, L, d)$`, never bare `$C$`. See [quality-checks.md](quality-checks.md) for the full constants-tracking discipline.

## Voice and connectives

- **First-person plural** ("we have", "we show", "we condition on") is the default. Avoid passive ("it is shown that") except for brief asides.
- **Sentence starters** that appear pervasively: *We have*, *Thus*, *Now*, *Recall*, *Note that*, *It follows that*, *Combining the above*, *By <Lemma X>*, *Plugging into*, *Substituting*. Use these as connective tissue between displays.
- **Avoid hedges in formal statements** ("we believe", "essentially", "roughly"). Hedging is permitted only in informal proof-sketch paragraphs.
- **Sentence length**: short and tightly bound to a single equation. Two-clause prose between displays is the norm.
