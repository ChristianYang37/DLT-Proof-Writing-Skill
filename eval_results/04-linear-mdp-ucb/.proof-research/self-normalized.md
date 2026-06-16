# Self-normalized concentration for adapted vector sequences

**Source.** Abbasi-Yadkori, Pal, Szepesvari 2011 (Theorem 1, self-normalized
bound for vector-valued martingales). Applied in Jin-Yang-Wang-Jordan 2020 via
their Lemmas D.4 + D.6 to obtain the LSVI fixed-point concentration Lemma B.3.
Project .bib key: \cite{abbasi2011improved}.

**Statement (self-normalized tail, AY-P-S Thm 1).** Let $\{\varepsilon_t\}$ be a
real-valued $\{\mathcal F_t\}$-adapted, conditionally $\sigma$-sub-Gaussian
noise: $\E[e^{\lambda\varepsilon_t}\mid\mathcal F_{t-1}]\le e^{\lambda^2\sigma^2/2}$.
Let $\{\phi_t\}$ be $\mathcal F_{t-1}$-measurable in $\mathbb R^d$,
$V_t=\lambda I+\sum_{s\le t}\phi_s\phi_s^\top$. Then for any $\delta\in(0,1)$,
with probability $\ge 1-\delta$, for all $t\ge0$ simultaneously,
$$\Big\|\sum_{s=1}^t \phi_s\varepsilon_s\Big\|_{V_t^{-1}}^2
\le 2\sigma^2\log\!\Big(\frac{\det(V_t)^{1/2}\det(\lambda I)^{-1/2}}{\delta}\Big).$$

**Use in JYWJ (Lemma B.3).** Setting $\varepsilon_\tau=V_{h+1}^k(x_{h+1}^\tau)-
(P_h V_{h+1}^k)(x_h^\tau,a_h^\tau)$ (a martingale-difference w.r.t. the episode
filtration, $|\varepsilon_\tau|\le H$ so $H$-sub-Gaussian), and union-bounding
over an $\varepsilon$-net of the value-function class $\mathcal V$ (covering
number $\log\mathcal N_\varepsilon \lesssim d^2\log(\dots)$ from Lemma D.6),
gives: there is an absolute constant $C$ with, on event $\mathcal E$,
$$\Big\|\sum_{\tau=1}^{k-1}\phi_h^\tau\big[V_{h+1}^k(x_{h+1}^\tau)
-(P_h V_{h+1}^k)(x_h^\tau,a_h^\tau)\big]\Big\|_{(\Lambda_h^k)^{-1}}
\le C\,dH\sqrt{\chi},\quad \chi=\log[2(c_\beta+1)dT/\delta],$$
and $\Pr[\mathcal E]\ge 1-\delta/2$.

**Hypotheses.**
- Conditionally sub-Gaussian noise w.r.t. the filtration ($|\varepsilon_\tau|\le H$).
- $\phi_\tau$ predictable ($\mathcal F_{\tau-1}$-measurable).
- Uniform covering of the function class $V_{h+1}^k$ ranges over (so the bound
  holds simultaneously for the data-dependent $V_{h+1}^k$). This is the
  $d^2$-vs-$d$ subtlety: the covering of $\{w,\beta,\Lambda\}$-parametrised
  value functions contributes the extra $d$ that makes $\beta=\Theta(dH)$ not
  $\Theta(\sqrt d H)$.

**Constants / dimension dependence.** $\beta=c_\beta\, dH\sqrt\iota$,
$\iota=\log(2dT/\delta)$. The first $d$ is the self-normalized
$\sqrt{\log\det}$ factor; the covering argument keeps it $O(dH\sqrt\iota)$ after
absorbing the $d^2\log$ covering term into $\sqrt{\chi}=O(\sqrt{\iota})$.

**Common misuses.**
- Forgetting the covering union bound and claiming $\beta=\Theta(\sqrt d H)$ —
  this is the single most common error; the value function is data-dependent so
  a naive self-normalized bound does not apply pointwise.
- Treating $V_{h+1}^k$ as fixed/independent of the data $\{x_{h+1}^\tau\}$.

**Project citation key.** \cite{abbasi2011improved}
