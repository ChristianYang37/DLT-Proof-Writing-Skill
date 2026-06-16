# Dependency graph — VC generalization bound

Proof type (pattern-menu): **Statistical learning rates** → symmetrization +
finite-class discretization + concentration. Organizational pattern: flat
four-leaf sequence feeding a wrapper theorem. Derivation pattern: **letter-tagged
with shared legend** for the chained inequalities; **decompose-and-conquer** is
not needed (single chain).

Regime: $n\ge d\ge1$ standing hypothesis (`ass:vc`). 0/1 loss class
$\mathcal L=\{(x,y)\mapsto\mathbf 1[h(x)\ne y]:h\in\mathcal H\}$,
$\mathrm{VC}(\mathcal L)\le d$ (`fac:loss-vc`).

## lem:mcdiarmid-dev  (McDiarmid concentration of the uniform deviation)
**Statement (1-line):** With prob $\ge1-\delta$,
$\sup_h|R(h)-\hat R_n(h)|\le\E\sup_h|R(h)-\hat R_n(h)|+\sqrt{\log(1/\delta)/(2n)}$.
**Hypotheses:** i.i.d. sample; 0/1 loss bounded in $[0,1]$ (so $c_i=1/n$).
**Technique digest:** `mcdiarmid.md`. **Downstream consumers:** thm:vc-bound
(cite-site: concentration step, §05 step 1).

## lem:symmetrization  (ghost-sample Rademacher symmetrization)
**Statement (1-line):**
$\E\sup_h|R(h)-\hat R_n(h)|\le 2\,\E_{S,\sigma}\,\widehat{\mathfrak R}_S(\mathcal L)
= 2\,\mathfrak R_n(\mathcal L)$, and the ghost sample $S'$ is introduced
explicitly.
**Hypotheses:** i.i.d. sample + independent ghost sample $S'$; fixed class.
**Technique digest:** `symmetrization.md`. **Downstream consumers:** thm:vc-bound
(§05 step 2).

## lem:sauer-shelah  (growth function bound; proved by shifting)
**Statement (1-line):** $\mathrm{VC}(\mathcal H)=d\Rightarrow
\Pi_{\mathcal H}(m)\le\sum_{i\le d}\binom mi\le(em/d)^d$ for $m\ge d$.
**Hypotheses:** $\mathrm{VC}(\mathcal H)\le d$. **Proof:** downward shifting
(combinatorial → `% lint: ignore R19`). **Technique digest:** `sauer-shelah.md`.
**Downstream consumers:** thm:vc-bound (§05 step 3, applied at $2n$);
lem:massart-rademacher (provides $|\mathcal L_{|S\cup S'}|\le\Pi_{\mathcal H}(2n)$).

## lem:massart-rademacher  (Massart finite-class Rademacher bound)
**Statement (1-line):**
$\mathfrak R_n(\mathcal L)\le\sqrt{2\log\Pi_{\mathcal H}(2n)/(2n)}$ via Massart on
the projection $\mathcal L_{|S\cup S'}$ (cardinality $\le\Pi_{\mathcal H}(2n)$,
$\{0,1\}^{2n}$ radius $\le\sqrt{2n}$).
**Hypotheses:** finite projection (Sauer–Shelah controls it); Rademacher signs.
**Technique digest:** `massart.md`; uses lem:sauer-shelah.
**Downstream consumers:** thm:vc-bound (§05 step 3).

## thm:vc-bound  (main theorem)
**Statement (1-line):** With prob $\ge1-\delta$,
$\sup_h|R(h)-\hat R_n(h)|\le C\sqrt{(d\log(n/d)+\log(1/\delta))/n}$.
**Hypotheses:** ass:iid, ass:vc ($n\ge d$). **Proof:** chain
lem:mcdiarmid-dev → lem:symmetrization → lem:massart-rademacher → lem:sauer-shelah,
then absorb constants into $C$; union-bound paragraph discharges the single
$\delta$ (one application of McDiarmid → no union needed across lemmas, but the
failure-budget paragraph is written to satisfy R17 and make the $1-\delta$
explicit). **Downstream consumers:** (top of graph — the deliverable).

## Occam check
Every node has a non-empty Downstream-consumers field. No node is removable:
- drop McDiarmid ⇒ no high-probability (only expectation);
- drop symmetrization ⇒ cannot pass to a data-dependent finite class;
- drop Massart ⇒ no $\sqrt{\log N/n}$;
- drop Sauer–Shelah ⇒ $\log N$ is $\log\Pi(2n)$ uncontrolled (could be $2^{2n}$).
Tree depth 2 (leaves → theorem). Shallowest that fits the named pipeline.

## File layout (one section per file; theorem+proof co-located, R5)
- `sections/01-preliminaries.tex` — notation, ass:iid, ass:vc, def of $R,\hat R,
  \mathfrak R_n$, growth function $\Pi_{\mathcal H}$, fac:loss-vc, universal-$C$
  declaration.
- `sections/02-mcdiarmid-deviation.tex` — lem:mcdiarmid-dev + proof.
- `sections/03-symmetrization.tex` — lem:symmetrization + proof.
- `sections/04-sauer-shelah.tex` — lem:sauer-shelah + proof (shifting), then
  lem:massart-rademacher + proof.
- `sections/05-main-theorem.tex` — thm:vc-bound + proof (assembly + union budget).
