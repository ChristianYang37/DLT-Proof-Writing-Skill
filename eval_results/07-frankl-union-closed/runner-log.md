# Runner log — frankl-union-closed-gilmer (eval id=7)

## What I built
A faithful, appendix-grade reconstruction of **Gilmer's entropy proof** of a
constant lower bound for the union-closed sets conjecture (arXiv:2211.09055).
Headline result (`thm:gilmer-frankl`, = Gilmer's Theorem 2): every union-closed
family $\mathcal F$ with $|\mathcal F|\ge 2$ has an element in $\ge 0.01\,|\mathcal F|$
of its sets. This is the corollary of the information-theoretic strengthening
(`thm:gilmer-entropy`, = Gilmer's Theorem 1): for i.i.d. $A,B$ with
$\Pr[i\in A]\le 0.01$, $H(A\cup B)\ge 1.26\,H(A)$. Decomposition (7 section
files): an entropy-monotonicity lemma (data processing), two single-variable
concavity bounds (Gilmer's Lemmas 2–3), two region bounds (Lemmas 4–5), the key
per-coordinate technical lemma (Lemma 1), the entropy theorem (chain rule), and
the combinatorial corollary (max-entropy + union-closure contradiction).
Derivation pattern: **letter-tagged with shared legend** (the entropy chains)
and trailing-justification for the region sums. Organizational pattern:
depth-graph of named lemmas, leaves-first (universal default from pattern-menu).

## Patterns chosen
- Statement template: restated-lemma / condition-list (no two-tier — pure-math,
  no informal/formal split needed).
- Derivation pattern: letter-tagged with shared legend ($\overset{(a)}{=}$ …)
  for the multi-step entropy chains; trailing-justification for region sums.
- Organizational pattern: universal default (named-lemma depth graph, ≤ 3 deep,
  leaves first) — pattern-menu has no "extremal combinatorics / entropy" row;
  this is an out-of-DLT generalization probe.

## Phase A.1a — Socratic intake (self-Q&A, eval mode: no interactive user)
Eval mode has no user to block on, so I ran A.1a as a self-Q&A, adopting the
**stronger/tighter** default for each and recording a `\todo{user-decision}` at
the relevant point.

- **Q1 [target form / constant].** Prove the explicit constant $c\ge 0.01$
  (Gilmer's stated value) vs. a weaker "some universal $c>0$"?
  *Default (stronger): the explicit $c\ge 0.01$, reproducing Gilmer's $1.26$
  amplification.* Alt: abstract $c>0$. → `\todo{user-decision}` in 07-frankl-corollary.tex.
- **Q2 [log base].** State entropy in bits ($\log_2$) vs. nats?
  *Default: base 2*, so $H(\text{uniform on }\mathcal F)=\log_2|\mathcal F|$ is clean
  and matches Gilmer. Alt: natural log (rescales, no math change). → recorded in 01-preliminaries.tex.
- **Q3 [single-variable inequality form].** The prompt suggests "$f(p)=h(p^2)-2h(p)$
  or its analog". Gilmer's *actual* load-bearing single-variable facts are
  $h(p+p'-pp')\ge 1.4\cdot\frac{h(p)+h(p')}{2}$ (Lemma 2) and
  $h(p+p'-pp')\ge(1-p)h(p')$ (Lemma 3). Reproduce Gilmer's true lemmas vs. the
  prompt's heuristic placeholder? *Default (faithful/stronger): Gilmer's actual
  Lemmas 2–3* — the placeholder $h(p^2)-2h(p)$ is the i.i.d.-marginal special
  case and does not by itself yield the conditional bound. → `\todo{user-decision}`
  in 03-single-variable-bounds.tex.
- **Q4 [generality of Theorem 1].** State Theorem 1 for an arbitrary
  distribution on $2^{[n]}$ (Gilmer's general form) vs. only the uniform case
  needed for the corollary? *Default (stronger/more general): arbitrary
  distribution* — it is what makes the per-coordinate conditioning work and is
  strictly stronger. → recorded in 06-main-theorem.tex.
- **Q5 [decomposition axis].** Sequence-of-lemmas (region split inside Lemma 1)
  vs. a flatter single-pass argument? *Default: Gilmer's lemma sequence* — the
  region split is mathematically necessary (the naive Jensen route is non-convex,
  Gilmer §4). Shallowest tree that fits.

No residual A.6 ambiguity surfaced during decomposition.

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 31 (trace) over an estimated 40 (script estimate; 77.5% coverage).
- After sweep: 25 🟢 / 6 🟡 / 0 🔴.
  - The 6 🟡 are the cross-lemma / cross-digest invocations (Steps 14, 18, 22,
    24, 26, 28): region bounds via Lemmas 2–3, the Lemma-1 region assembly, and
    the coarsening + key-lemma steps — each digest-matched against Gilmer's
    verbatim Lemmas 1–5 / Eqs. (1)–(3).
  - The 25 🟢 are named textbook facts (concavity/Jensen, Markov, data-processing,
    max-entropy, chain rule) and arithmetic constants ($0.01/0.1$, $g$-min $=1.45$,
    $1.26/1.4=0.9$, $1.8\cdot0.9=1.62$, $\log_2 2=1$), all independently
    script-verified.
- Sub-agents fired: 0 — every step upgraded by fast path (textbook inequality,
  digest match, or direct numeric script check). No step needed fire-and-forget
  re-derivation; none remained 🔴, so no `\todo{verify}` markers were required.
- Any 🔴 with `unable-to-derive`: none.

## Phase D — Review loop summary
RUN by the independent five-reviewer panel (Phase-D author agent, iteration 1).

- **Iterations:** 1 (of 3-iteration cap).
- **Per-iteration mean history:** [8.20].
- **Final mean:** 8.20 / 10.
- **Accepted:** yes — gate cleared at iteration 1 (`mean > 8` strict, 8.20 > 8,
  AND no unresolved REAL-blocking critical; no reviewer set `blocking:true`).
- **Final five scores:** R1 line-by-line = 9, R2 assumptions/generality = 9,
  R3 ML-significance = 8, R4 math-taste = 8, R5 derivation-integrity = 7.
- **Merged weaknesses (6, deduped from 12):** all non-blocking. Verdicts —
  INTENTIONAL ×2 (visible `\todo` user-decision markers 4/5; over-strong
  region-lemma hypothesis 1/5), REAL-nonblocking ×3 (prose-asserted g-minimization
  "direct calculation" major, 2/5; identity-as-≤ chain style 1/5; dead `\R` macro
  style 1/5), 0 REAL-blocking, 0 PHANTOM (one near-phantom denominator-positivity
  minor 1/5, logged REAL-nonblocking since the (0,0) case split implies positivity).
- **Fixes applied:** none. Per review-loop.md Component 4 gate 1, an accepted proof
  is recorded, not modified. Residual style/prose items surfaced to the user as
  optional one-line cleanups; none required for correctness.
- **Artifact:** `.proof-research/review-iteration-1.md` (all five scores + mean,
  each merged weakness with verdict and rebuttal/fix-plan, accept decision).

## Where I had to make calls
- Used $h(\cdot)$ for the scalar binary-entropy function and $H(\cdot)$ for
  Shannon entropy to avoid Gilmer's overload of the symbol $H$.
- Reproduced Gilmer's actual single-variable Lemmas 2–3 rather than the prompt's
  heuristic $h(p^2)-2h(p)$ placeholder (see Q3); noted the relationship in a remark.
- Kept the constant $0.01$ unoptimized exactly as Gilmer does; flagged that the
  sharp threshold $\frac{3-\sqrt5}{2}$ is follow-up work, cited not reproduced.

## Self-check results
- lint.py errors: 0 (R0a–R19 all clean; one `% lint: ignore R19` on the
  prose-bound corollary proof, and one `% lint: ignore R15` on the single named
  threshold $c=0.01$ — both annotated with reasons).
- latexmk compile_ok: true; overfull_violations: []; undef_refs/undef_cites: [].
- Cite-key check: every `\cite{...}` resolves in refs.bib (gilmer2022unionclosed,
  coverthomas2006), each with a `.proof-research/cite-*.md` digest (R13 clean). yes.
- All `\input`'d section files exist on disk? yes (01–07).
- check_confidence_tags.py exit 0 (31 tagged, 0 untagged, 0 red issues).
- check_scope.py exit 0 (declared Appendix).

## What's incomplete
- Two `\todo{user-decision: ...}` markers record the Socratic self-Q&A
  delegations (eval mode, no interactive user): (1) reproduce Gilmer's actual
  single-variable Lemmas 2–3 vs. the prompt's heuristic $\hb(p^2)-2\hb(p)$
  placeholder — adopted the faithful/stronger Gilmer lemmas; (2) prove the
  explicit constant $c\ge0.01$ vs. an abstract $c>0$ — adopted the explicit
  constant. Both should be confirmed by the user.
- The constant $0.01$ is Gilmer's deliberately unoptimized value; the sharp
  threshold $\frac{3-\sqrt5}{2}\approx0.38$ (follow-up work) is cited in
  \Cref{rem:constant} but not reproduced, as the eval asks only for $c\ge0.01$.
- Phase D (five-reviewer panel) is handled by an independent panel, not here.

v1.2 retrofit: +hyperref, user-decision todos -> decisions.md (2 moved, 0 verify kept)
v1.2 finalize: completed 0 todos, geometry margin=1in
