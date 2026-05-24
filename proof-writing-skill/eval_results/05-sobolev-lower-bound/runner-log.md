# Runner log — sobolev-minimax-lower-bound

## What I built
A four-lemma decomposition of the canonical Tsybakov-style minimax lower bound: $\mathfrak M_n \gtrsim n^{-2s/(2s+d)}$ for fixed-design Gaussian regression over the Sobolev unit ball $W^s_2([0,1]^d)$. The decomposition is (1) bump-norm lemma giving $\Wnorm{f_\omega} \leq 1$ and $L^2$ separation, (2) restated Varshamov--Gilbert packing as a \fact, (3) KL bound for the bump family using balanced design, (4) restated Tsybakov Fano-type bound plus an instantiated probability lower bound (\Cref{lem:prob-lb}); the headline theorem is assembled via Markov-to-expectation and the choice $m \asymp (n/(\alpha_\star\sigma^2))^{1/(2s+d)}$. Derivation pattern: trailing-justification + step-decomposed proof boundaries; organizational pattern: statistical-rates row (minimax lower bound paired with optimization-of-$m$ at the end).

## Patterns chosen
- Statement template: two-tier informal/formal via \Cref{thm:main} body + remark on tightness
- Derivation pattern: \paragraph{Step k} decomposition + trailing-justification (e.g. \Cref{lem:bump-norms} (i))
- Organizational pattern: Statistical learning rates row (Tsybakov minimax recipe — VG + bump + Fano + Markov + balance $m$)

## Phase C.5 — Confidence sweep summary
- Steps enumerated: 25
- After sweep: 21 🟢 / 4 🟡 / 0 🔴
- Sub-agents fired: 0 (every step was fast-path verifiable via hand-check, digest match, or project lemma match)
- Any 🔴 with `unable-to-derive` (and corresponding `\todo{}` in .tex): none

## Phase D — Review loop summary
- Iterations: 3 (max 3)
- Final verdict: accept-as-is
- Weaknesses per iteration: 4, 2, 0
- Fixes applied per iteration: 4 (3 critical + 1 minor stylistic refinement), 1 (minor), 0
- Termination reason: accept-as-is
- Iteration files: .proof-research/review-iteration-1.md, review-iteration-2.md, review-iteration-3.md

## Where I had to make calls
- Chose balanced fixed design (\Cref{def:balanced-design}) rather than restricting to the regular grid, because the problem prompt says "fixed-design" without specifying; balance is the textbook hypothesis under which the closed-form KL gives the right rate.
- Restated Fano-type theorem as a "restated \lemma" rather than a Fact, because it has hypotheses to verify whereas Facts in this project are used for purely algebraic restatements.
- Chose Tsybakov 2009 throughout (one citation digest) rather than mixing in Yu's Lemma / Birgé--Massart; flagged in \Cref{rem:alt-fano}.
- Selected $\alpha_\star = (\log 2)/(256 C_{\msf{KL}})$ to give $\alpha = 1/16$ comfortably below $1/8$; this was a halving from the initial $1/128 C_{\msf{KL}}$ after iteration-1 review.

## Self-check results
- lint.py errors: 0
- latexmk compile_ok: true
- Cite-key check: only \cite{tsybakov2009introduction}; resolves in refs.bib. ✓
- All \input'd section files exist on disk: yes (six files: 01-preliminaries through 06-proof-of-thm)

## What's incomplete
- The constant $C_{\msf{bal}}$ in \Cref{def:balanced-design} is treated as a problem datum; the theorem's $n_0$ implicitly depends on it. This is standard but I did not push the dependence into the theorem statement explicitly.
- The $L^\infty$ bound from \Cref{lem:bump-norms}\ref{lem:bump-norms:linf} is proved but never used downstream. Could be deleted in a tighter pass; left in because it's the natural companion to the $L^2$ bound and aids reader understanding.
- The Fano-type bound (\Cref{lem:fano-tsybakov}) is restated as a Lemma rather than proved; this is the standard appendix practice for cited external results.
