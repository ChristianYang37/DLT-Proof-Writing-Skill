# Phase A.1a — Socratic intake (self-Q&A, eval mode)

No interactive user. Per the runner protocol, each question is answered by
adopting the **stronger / tighter** default, recorded as a
`\todo{user-decision: <chosen>, alt: <alt>}` in the .tex and echoed here.

## Target statement (recited from A.1)

For a hypothesis class $\mathcal H\subset\{0,1\}^{\mathcal X}$ with
$\mathrm{VC}(\mathcal H)=d$, i.i.d. sample $S=\{(x_i,y_i)\}_{i=1}^n\sim\mathcal D^n$,
with probability $\ge 1-\delta$,
$$\sup_{h\in\mathcal H}|R(h)-\hat R_n(h)|\le C\sqrt{\tfrac{d\log(n/d)+\log(1/\delta)}{n}}.$$
Pipeline mandated by the prompt: (1) symmetrization with a ghost sample →
Rademacher complexity; (2) Sauer–Shelah to bound the growth function by
$\binom{n}{\le d}$; (3) Massart's finite-class bound on the Rademacher complexity.

## Setting questions (group A)

### Q1 [target form] — high-probability uniform bound vs. expectation bound
- **Proposed (stronger):** the full high-probability statement
  $\Pr[\sup_h|R-\hat R|\le \text{RHS}]\ge 1-\delta$, with the $\log(1/\delta)$
  term tracked explicitly. This is what the prompt asks for.
- **Alternative (weaker):** only the in-expectation bound
  $\E\sup_h|R-\hat R|\lesssim\sqrt{d\log(n/d)/n}$ (no $\delta$).
- **Chosen:** high-probability. The expectation bound is an intermediate lemma
  feeding the concentration step, not the endpoint.

### Q2 [loss / range] — 0/1 loss on $\{0,1\}$ labels
- **Proposed (stronger, and what the VC setup means):** binary $\{0,1\}$ loss
  $\ell(h,(x,y))=\mathbf 1[h(x)\ne y]$, so the loss class
  $\mathcal L=\{(x,y)\mapsto\ell(h,(x,y)):h\in\mathcal H\}$ also has VC dimension
  $\le d$ (composition with a fixed $\{0,1\}$ target preserves VC dimension).
- **Alternative:** a general bounded loss in $[0,1]$ via a contraction /
  Ledoux–Talagrand step — strictly more machinery, not needed here.
- **Chosen:** 0/1 loss. We bound the growth function of the loss class directly
  by that of $\mathcal H$.

### Q3 [constant discipline] — explicit $\sqrt{\cdot}$ rate, universal $C$, no `\poly` slack
- **Proposed (matches prompt):** deliver the explicit rate
  $C\sqrt{(d\log(n/d)+\log(1/\delta))/n}$ with a single universal constant $C$;
  no $\poly$ slack. We do **not** chase the smallest numerical $C$ (e.g. the
  constant $2$ from a careful chaining); a clean universal $C$ absorbing the
  symmetrization factor $2$, the Massart factor $\sqrt 2$, and the McDiarmid
  factor suffices.
- **Alternative:** track the exact numerical constant. Not required; the prompt
  says "for some universal constant $C$".
- **Chosen:** explicit rate, universal $C$, constant value not optimized.

### Q4 [regime / $\log(n/d)$ form] — keep the $\log(n/d)$ (not bare $\log n$)
- **Proposed (stronger / what the prompt wants):** carry the Sauer–Shelah
  bound $\Pi_{\mathcal H}(n)\le (en/d)^d$ so the rate has $d\log(n/d)$, valid in
  the regime $n\ge d$ (else the bound is vacuous — for $n<d$ the LHS is
  trivially $\le 1$ and the RHS exceeds $1$). Record $n\ge d$ as a standing
  hypothesis.
- **Alternative:** $\Pi_{\mathcal H}(n)\le n^d+1$ giving the looser $d\log n$.
- **Chosen:** $(en/d)^d$ form ⇒ $d\log(n/d)$.

### Q5 [symmetrization route] — two-sided sup via ghost sample + Rademacher
- **Proposed:** the textbook route the prompt names — bounded-differences
  (McDiarmid) to concentrate $\sup_h|R-\hat R|$ around its mean, then
  ghost-sample symmetrization of the mean to $2\,\mathfrak R_n(\mathcal L\circ S)$,
  then Massart over the projection $\mathcal L_{|S\cup S'}$ whose cardinality is
  controlled by Sauer–Shelah.
- **Alternative:** a direct two-sided union bound over an $\varepsilon$-net /
  the VC "double-sample" trick à la Vapnik–Chervonenkis with the factor-$2$
  symmetrization on the probability directly. Equivalent rate, more bookkeeping.
- **Chosen:** McDiarmid + ghost-sample Rademacher symmetrization + Massart.

### Q6 [citations] — research from scratch, digest the named classical results
- **Proposed:** prove the load-bearing lemmas locally (symmetrization,
  Sauer–Shelah, Massart, McDiarmid), but back each with a digest of its
  canonical textbook source (Wainwright HDS 2019, Mohri–Rostamizadeh–Talwalkar
  FoML 2018, Shalev-Shwartz–Ben-David UML 2014, Boucheron–Lugosi–Massart 2013)
  so every `\cite` is digest-backed and resolves in `refs.bib`.
- **Chosen:** prove locally; cite textbook sources with digests.

## Architecture questions (group B)

### Q7 [decomposition axis] — flat lemma sequence (shallowest tree)
- **Proposed:** a depth-2 tree: four leaf lemmas (McDiarmid concentration,
  ghost-sample symmetrization, Sauer–Shelah, Massart) feeding directly into the
  main theorem. No intermediate aggregation lemma — the theorem's proof chains
  the four in ~10 lines.
- **Alternative:** a "uniform-deviation" intermediate lemma combining
  symmetrization + Massart + Sauer–Shelah into one expected-sup bound, then the
  theorem adds only McDiarmid. Slightly deeper; obscures the named pipeline.
- **Chosen:** flat four-leaf sequence; the prompt explicitly wants each
  ingredient as its own `\begin{lemma}`.

### Q8 [Sauer–Shelah proof] — full shifting proof or cite?
- **Proposed (stronger):** prove Sauer–Shelah in full via the
  downward-shifting / polynomial argument, since it is the combinatorial heart
  and the prompt lists it as a stated-and-proved ingredient. The shifting
  argument is genuinely combinatorial (counting shattered subsets), so its
  proof is the one place a `% lint: ignore R19` is justified.
- **Alternative:** cite Sauer–Shelah from a textbook via `\begin{lemma}[\cite{}]`.
- **Chosen:** prove in full (shifting), annotate that proof `% lint: ignore R19`.

## Summary of adopted decisions (all stronger/tighter defaults)

| Q | Decision adopted | Alternative not taken |
|---|---|---|
| Q1 | high-probability $1-\delta$ bound | in-expectation only |
| Q2 | 0/1 loss, VC of loss class $\le d$ | general $[0,1]$ loss + contraction |
| Q3 | explicit rate, universal $C$ (value not optimized) | track exact constant |
| Q4 | $(en/d)^d$ ⇒ $d\log(n/d)$, regime $n\ge d$ | $d\log n$ |
| Q5 | McDiarmid + ghost Rademacher + Massart | VC double-sample direct |
| Q6 | prove locally, digest textbook cites | cite as black boxes |
| Q7 | flat four-leaf decomposition | nested uniform-deviation lemma |
| Q8 | full Sauer–Shelah shifting proof | cite Sauer–Shelah |

Each appears as a `\todo{user-decision: ...}` at the relevant point in the .tex.
