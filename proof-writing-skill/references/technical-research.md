# Technical reconnaissance

Read this file in Phase A, immediately after listing the goal and before drawing the dependency graph. The purpose is to **pre-load the precise statement of every non-trivial tool the proof will use**, because AI memory is unreliable on the hypothesis, constants, and tail behaviour of these tools.

## Why this exists

Failure mode: you remember a high-level statement of a tool (e.g., "matrix Bernstein gives operator-norm concentration") and write a derivation that *looks* right. The reviewer then catches that you used the sub-Gaussian variant with a sub-exponential payload, or you forgot the dimension factor, or you assumed centered when the lemma needs symmetric. AI proofs fail at this level routinely. Pre-loading the precise statement defuses this.

Skip for pure-algebra steps (Cauchy-Schwarz, AM-GM, triangle inequality). Do not skip for anything advanced or recent.

## Workflow

1. **Enumerate techniques at a granular level.** Not "concentration" but
   *"matrix Bernstein for $\sum_i X_i$ with $X_i \in \R^{n \times d}$, $\E X_i = 0$, $\|X_i\|_{\mathrm{op}} \le R$ a.s., $\|\sum_i \E X_i X_i^\top\|_{\mathrm{op}} \le \sigma^2$"*.

2. **Search the project bibliography first.** If the project already cites a textbook (Vershynin's *High-Dimensional Probability*, Wainwright's *High-Dimensional Statistics*, Boucheron-Lugosi-Massart, Tropp's *Introduction to Matrix Concentration*) or a survey, use that as the canonical source — match the project's existing citation key.

3. **Spawn a research sub-agent** for any technique whose precise statement you are not certain of. Brief it:

   > Find and digest the canonical statement of **<technique>** as used in **<subfield>**. Pull the relevant arxiv source (or textbook chapter) and extract:
   > - (i) the precise statement with all hypotheses,
   > - (ii) constants and dimension dependence,
   > - (iii) the common usage pattern as a 5–15 line LaTeX excerpt from a paper that uses it well,
   > - (iv) failure modes when hypotheses are weakened.
   >
   > Save to `<project-root>/.proof-research/<technique-slug>.md`, 200–500 words, under 5 minutes.

4. **Save digests** under `<project-root>/.proof-research/` (create the directory if needed). One markdown file per technique. Schema:

   ```markdown
   # <technique name>

   **Source.** <book / paper, with \cite key as it appears in project .bib>

   **Statement.** <verbatim from canonical source>

   **Hypotheses.** <bulleted list — every condition, every quantifier order>

   **Constants and dimension dependence.** <what's hidden in O(·), what's explicit>

   **Canonical use pattern.** <LaTeX excerpt, 5–15 lines, from a paper that applies it well>

   **Common misuses.**
   - <misuse 1, e.g. using sub-Gaussian form on sub-exponential data>
   - <misuse 2, e.g. forgetting the dimension factor>
   - ...

   **Project citation key.** \cite{...}
   ```

5. **Re-read the digest at the moment of use.** When Phase C reaches the derivation step that invokes the technique, open the digest first, then write the step. Do not write from memory.

## Examples of "non-trivial techniques" that benefit from a digest

Probability / concentration:

- matrix Bernstein (different variants for symmetric vs. rectangular)
- matrix Chernoff
- Hanson–Wright (sub-Gaussian quadratic forms)
- Bernstein for sub-exponential variables
- McDiarmid's inequality and its extensions
- Azuma–Hoeffding for martingales
- Self-normalized concentration (de la Peña / Pinelis)
- Gaussian / sub-Gaussian anti-concentration

Empirical-process / chaining:

- Dudley's chaining
- Talagrand's generic chaining
- Local Rademacher / local Fano
- Covering / packing-number bounds (Varshamov–Gilbert + Fano for lower bounds)

Optimization / dynamics:

- Semi-smoothness inequalities for ReLU networks
- Gronwall and integral-form Gronwall
- Lyapunov decomposition (proximal-Gibbs, mean-field free energy)
- Polyak–Łojasiewicz, Kurdyka–Łojasiewicz
- Elliptical-potential lemma (RL / bandits)

Linear algebra / numerical:

- Weyl's perturbation inequality
- Davis–Kahan
- Matrix-determinant lemma, Sherman–Morrison, Woodbury
- Hoffman–Wielandt for singular values

Approximation theory:

- Yarotsky multiplication gadget for ReLU networks
- B-spline / wavelet expansions for Besov classes
- Local-polynomial approximation rates

Fine-grained complexity:

- SETH and its strong variants
- Orthogonal Vectors Hypothesis (OVH)
- 3SUM-Hardness
- Polynomial method (Aggarwal–Alman style)

Optimal transport:

- Wasserstein contraction
- Talagrand's transportation inequality
- Sinkhorn convergence

This list is not exhaustive — anything not in your fluent toolkit deserves a digest.

## Citation digests for cited prior results

The technique digest covers *tools* (concentration inequalities, approximation gadgets). The **citation digest** covers *specific prior results* the proof cites by theorem/lemma number: *"By Theorem 3.2 of \cite{smith2023}, ..."*. AI memory of these is even less reliable than of techniques — you may remember a result exists in Smith 2023 but be off by a section, a theorem number, or a hypothesis. Citing the wrong number lands you in fabricated-reference territory.

### When to run citation reconnaissance

Run it before any `\cite{...}` that:

- Names a specific result by number (Theorem X.Y of [author]).
- Is the load-bearing reference for an inequality, reduction, or known bound used in your derivation.
- Has not appeared in the project's existing chapters / `.bib` already.

Skip it for:

- Background references in the introduction (no theorem-level claim depends on them).
- Results already cited correctly elsewhere in the project (just match the existing cite key).
- Textbook material where the project already cites a textbook (Vershynin, Wainwright, etc.) and the result is widely known.

### How to run citation reconnaissance

1. **Identify the result.** You know roughly what you want: *"the matrix-Bernstein bound in some Tropp paper"*, *"the elliptical-potential lemma in Abbasi-Yadkori et al."*, etc.

2. **Find the PDF** — arxiv abstract page (e.g. `https://arxiv.org/abs/2310.12345`) usually links the PDF. If only a publisher version exists and is paywalled, ask the user whether they have access.

3. **Spawn a sub-agent** (preferred for non-trivial searches):

   > Find Theorem **<rough description>** in the paper **<title, arxiv id or DOI>**. Download the PDF (`curl -L -o /tmp/<slug>.pdf "https://arxiv.org/pdf/<id>"`) and read it. Report:
   > - The **exact theorem/lemma/proposition number** as printed in the PDF (e.g. "Theorem 3.2", not "Theorem 3.2 in Section 3.1").
   > - The **page number** where it appears.
   > - The **precise statement**, verbatim if short or paraphrased faithfully if long, with all hypotheses.
   > - Any **constants or dimension dependence** the statement carries.
   > - The **citation key** as it should appear in the project's `.bib` (match the project's existing key style — e.g. `smith2023sometitle` vs. `s23` vs. `[42]`).
   >
   > Save to `<project-root>/.proof-research/cite-<author><year>-<slug>.md` with this schema:
   >
   > ```markdown
   > # \cite{<key>} — <short description>
   > **Paper.** <full title>, <authors>, <venue/year>, arxiv:<id>, page <P>.
   > **Exact name in PDF.** "Theorem 3.2"
   > **Statement (verbatim or faithfully paraphrased).** ...
   > **Hypotheses.** ...
   > **Constants / dimension dependence.** ...
   > **Project .bib key.** \cite{<key>}
   > ```

4. **Or do it yourself** for a single quick check: `curl` the PDF, then `pdftotext -layout` it, then `grep` for the theorem statement. Save the digest as above.

5. **At the cite-site in the proof**, use the digest's exact theorem number and citation key. Do not re-guess from memory.

### Failure modes the citation digest defuses

- Citing "Theorem 3.2" when the paper's Theorem 3.2 says something else (the result you want is Theorem 3.4).
- Citing a result that was *removed* in a published version (arxiv v1 vs JMLR final).
- Citing a result with weaker hypotheses than your derivation needs (and thus invalid at the cite-site).
- Using a `\cite{key}` that doesn't exist in the project's `.bib`.

## When you finish

After Phase A.4, you should have:

- `<project-root>/.proof-research/<technique-slug>.md` for each non-trivial technique;
- `<project-root>/.proof-research/cite-<author><year>-<slug>.md` for each load-bearing cited prior result.

The dependency graph in Phase A.5 and the citations at every cite-site in Phase C will then be built on tools and references whose exact statements you have verified, not remembered.
