# Statement and derivation templates

Read this file before writing any new `\begin{theorem}` / `\begin{lemma}` / `\begin{proof}` block, and again whenever you start a new derivation chain. Pick **one** statement template and **one** derivation pattern per proof, and apply uniformly.

## Contents

- [Statement templates](#statement-templates) — pick by result type
  - Two-tier (informal + formal)
  - Restated lemma at top of appendix proof
  - Condition-list (heavy-hypothesis case)
  - Decomposed bound with annotated terms
- [Derivation patterns](#derivation-patterns) — pick by chain structure
  - Trailing-justification block (default)
  - Inline per-step tags
  - Letter-tagged step markers with shared legend (+ circled-number variant)
  - Decompose-and-conquer with named pieces
  - Successful-event conditioning
- [Proof boundaries](#proof-boundaries) — opening and closing conventions

---

## Statement templates

Hypotheses go first, conclusion last; every named object referenced by `\Cref` rather than restated from scratch.

### Two-tier (informal in body, formal in appendix)

The near-universal pattern. Body version uses `\lesssim`, `\poly(\cdot)`, asymptotic horizons; appendix version pins every constant.

**Informal (main body):**

```latex
\begin{theorem}[Convergence, informal]\label{thm:main_informal}
Under \Cref{ass:data,ass:init}, if $m \gtrsim \poly(n, 1/\lambda_0, 1/\delta)$ and
$\eta \lesssim \lambda_0 / n^2$, then with high probability gradient descent achieves
$\|f(\Wb^{(T)}) - y\|_2^2 \le \varepsilon$ after $T = O(\log(1/\varepsilon)/(\eta\lambda_0))$ steps.
\end{theorem}
```

**Formal (appendix), restating with constants pinned:**

```latex
\begin{theorem}[Convergence, formal version of \Cref{thm:main_informal}]\label{thm:main_formal}
For any $\varepsilon, \delta \in (0, 1)$, suppose \Cref{ass:data} and \Cref{ass:init} hold and
\begin{align*}
m &\ge C_1 \cdot \frac{n^7}{\lambda_0^4 \delta^4 \varepsilon^2}, &
\eta &= C_2 \cdot \frac{\lambda_0}{n^2}, &
T &= C_3 \cdot \frac{\log(1/\varepsilon)}{\eta \lambda_0},
\end{align*}
for universal constants $C_1, C_2, C_3 > 0$. Then with probability at least $1 - \delta$
over the random initialization,
\begin{align*}
\| f(\Wb^{(T)}) - y \|_2^2 \;\le\; \varepsilon.
\end{align*}
\end{theorem}
```

The optional bracket `[formal version of \Cref{thm:main_informal}]` makes the appendix proof self-reference the body teaser.

### Restated lemma at top of appendix proof

When a lemma was stated in the body and re-stated where its proof lives:

```latex
\begin{lemma}[Coupling, \Cref{lem:coupling_main} restated]\label{lem:coupling}
Under \Cref{ass:data}, with probability at least $1 - \delta$, for every $\tau > 0$
and every $t \le T_0(\tau)$, at least a $(1 - \kappa \tau)$-fraction of neurons
$r \in [m]$ satisfy
\begin{align*}
\frac{\partial L(\Wb^{(t)})}{\partial w_r} = \frac{\widetilde{\partial} L(\Wb^{(t)})}{\partial w_r}.
\end{align*}
\end{lemma}
```

### Condition-list (heavy-hypothesis case)

When more than three hypotheses are needed, prefer `itemize` over a paragraph:

```latex
\begin{lemma}[Induction step]\label{lem:induction_step}
If the following conditions hold:
\begin{itemize}
    \item $\lambda := \lambda_{\min}(H^*) > 0$;
    \item $m \ge \lambda^{-2} \poly(n, d, \exp(B))$;
    \item $\eta = \lambda / \bigl( m \poly(n, d, \exp(B)) \bigr)$;
    \item the inductive hypothesis at time $t$ in \Cref{def:induction_properties} holds,
\end{itemize}
then at time $t+1$:
\begin{align*}
\|\Wb^{(t+1)} - \Wb^{(0)}\|_F &\le D, \\
\|f(\Wb^{(t+1)}) - Y\|_F^2 &\le (1 - m\eta\lambda/2) \, \|f(\Wb^{(t)}) - Y\|_F^2.
\end{align*}
\end{lemma}
```

### Decomposed bound with annotated terms

For statements whose conclusion is a sum of named error terms (approximation + estimation + optimization, or bias + variance):

```latex
\begin{theorem}[Excess-risk decomposition]\label{thm:risk_decomp}
Under \Cref{ass:smoothness}, if $n \gtrsim N \log N$ and $T \gtrsim n^{(2\alpha+2d)/(2\alpha+d)}$,
\begin{align*}
\bar{R}(\widehat{\theta})
\;\lesssim\;
\underbrace{N^{-2\alpha/d}}_{\text{approximation}}
\;+\;
\underbrace{\frac{N \log N}{n}}_{\text{estimation}}
\;+\;
\underbrace{\frac{N^2 \log N}{T}}_{\text{pretraining}}.
\end{align*}
Setting $N \asymp n^{d/(2\alpha + d)}$ yields the minimax rate $n^{-2\alpha/(2\alpha + d)}$
up to logarithmic factors.
\end{theorem}
```

---

## Derivation patterns

Pick by chain structure:

| Pattern | When | Best for |
|---|---|---|
| Trailing-justification block | each step has one short reason | long chains where reasons differ row by row |
| Inline per-step tags (`\tag{}`) | each row carries one short cite | short chains, one named result per row |
| Letter-tagged with shared legend | many steps share a justification family | mid-length chains, dense citations |
| Decompose-and-conquer | target splits into pieces needing different machinery | NN perturbation analysis, multi-source error |
| Successful-event conditioning | proof is probabilistic / RL-flavored | concentration-heavy proofs |

Do not mix patterns within a single proof.

### Trailing-justification block

Write the chain with `& ~` after each relation symbol; close with one comma-list of reasons:

```latex
\begin{align*}
\| \widetilde{D}^{-1} \widetilde{A} V - D^{-1} \widetilde{A} V \|_\infty
\;\le\; & ~ \sum_{l=1}^{n} \big| (\widetilde{D}_{i,i}^{-1} - D_{i,i}^{-1}) \widetilde{A}_{i,l} \big| \cdot \|V\|_\infty \\
\;=\; & ~ \sum_{l=1}^{n} \Big| \tfrac{D_{i,i} - \widetilde{D}_{i,i}}{D_{i,i} \widetilde{D}_{i,i}} \widetilde{A}_{i,l} \Big| \cdot \|V\|_\infty \\
\;\le\; & ~ \varepsilon_D \cdot \sum_{l=1}^{n} \big| \widetilde{D}_{i,i}^{-1} \widetilde{A}_{i,l} \big| \cdot \|V\|_\infty \\
\;\le\; & ~ \varepsilon_D \cdot B,
\end{align*}
where the first step follows from the triangle inequality, the second step follows from
algebraic simplification of the difference of reciprocals, the third step follows from
$|(D_{i,i} - \widetilde{D}_{i,i})/D_{i,i}| \le \varepsilon_D$ (\Cref{lem:d_close}),
and the last step follows from $\sum_l \widetilde{D}_{i,i}^{-1} \widetilde{A}_{i,l} \le B$
(\Cref{ass:bounded_attention}).
```

Conventions:
- `& ~` after each relation symbol gives a uniform single-space indent.
- Ordinals (`first / second / ... / last`) map exactly to visible relation rows. **Count carefully** — off-by-one between trailer and rows is the most common silent bug.
- One reason per step. If a step is "simple algebra", say so — do not skip it.

### Inline per-step tags

For chains where each row carries one short cite:

```latex
\begin{align*}
\big\| (P_\Omega(XX^\top) X)_{i^*} + (\lambda \nabla R(X))_{i^*} \big\|
&\;\ge\; \big\| (\lambda \nabla R(X))_{i^*} \big\| \tag{by \Cref{eq:gradient_split}} \\
&\;=\; \tfrac{4\lambda(\|X_{i^*}\| - \alpha)^3}{\|X_{i^*}\|} \cdot \|X_{i^*}\| \tag{by \Cref{prop:gradient}} \\
&\;\ge\; \tfrac{\lambda}{2} \|X_{i^*}\|^3 \tag{since $\|X_{i^*}\| \ge 2\alpha$}
\end{align*}
```

Use `\tag{by \Cref{...}}` for forward references and `\tag{since <inline fact>}` for arithmetic conditions.

### Letter-tagged with shared legend

When several lines depend on the same family of facts:

```latex
\begin{align*}
L_{\text{un}}(f)
&\;\stackrel{(a)}{=}\; \E_{c^+, c^- \sim \rho^2} \E_{x \sim D_{c^+}, x^+ \sim D_{c^+}, x^- \sim D_{c^-}} \bigl[ \ell(f(x)^\top (f(x^+) - f(x^-))) \bigr] \\
&\;\stackrel{(b)}{\ge}\; \E_{c^+, c^- \sim \rho^2} \E_{x \sim D_{c^+}} \bigl[ \ell(f(x)^\top (\mu_{c^+} - \mu_{c^-})) \bigr] \\
&\;\stackrel{(c)}{=}\; (1 - \tau) \E_{c^+ \ne c^-} L_{\sup}^\mu(\{c^+, c^-\}, f) + \tau
\end{align*}
where (a) follows from the definitions in \Cref{eq:sim_def} and \Cref{eq:neg_def};
(b) follows from convexity of $\ell$ and Jensen's inequality, taking the expectation
over $x^+, x^-$ inside the loss; (c) follows by splitting the expectation into the cases
$c^+ = c^-$ and $c^+ \ne c^-$ and using symmetry.
```

**Circled-number visual variant.** Same pattern, with `\overset{\text{\ding{172}}}{\leq}`, `\overset{\text{\ding{173}}}{=}`, etc. Pick letters or circles per project convention; do not mix within one proof.

### Decompose-and-conquer with named pieces

When the target quantity splits into pieces that need different machinery, name them with `\triangleq` and bound each separately:

```latex
We decompose the difference as
\begin{align*}
\big| G_{ij}^{(H)}(k) - G_{ij}^{(H)}(0) \big|
&\;\le\;
\underbrace{\big| x_i^{(H-1)}(k)^\top x_j^{(H-1)}(k) - x_i^{(H-1)}(0)^\top x_j^{(H-1)}(0) \big| \cdot \tfrac{c_\sigma}{m} \sum_r a_r(0)^2 \sigma'_{i,r}(k) \sigma'_{j,r}(k)}_{\triangleq\, I_1} \\
&\quad +\;
\underbrace{\big| x_i^{(H-1)}(0)^\top x_j^{(H-1)}(0) \big| \cdot \tfrac{c_\sigma}{m} \big| \textstyle\sum_r a_r(0)^2 \big( \sigma'_{i,r}(k) \sigma'_{j,r}(k) - \sigma'_{i,r}(0) \sigma'_{j,r}(0) \big) \big|}_{\triangleq\, I_2} \\
&\quad +\;
\underbrace{\big| x_i^{(H-1)}(k)^\top x_j^{(H-1)}(k) \big| \cdot \tfrac{c_\sigma}{m} \big| \textstyle\sum_r (a_r(k)^2 - a_r(0)^2) \sigma'_{i,r}(k) \sigma'_{j,r}(k) \big|}_{\triangleq\, I_3}.
\end{align*}
We bound each piece in turn.

\smallskip\noindent
\textbf{Bound on $I_1$.} By \Cref{lem:perturbation_of_neuron}, $\| x^{(H-1)}(k) - x^{(H-1)}(0) \|_2 \le \ldots$, so
\begin{align*}
I_1 \;\le\; 3 c_\sigma a_{2,0}^2 c_{x,0}^2 \sqrt{c_\sigma} L^3 g_{c_x}(H) R.
\end{align*}

\smallskip\noindent
\textbf{Bound on $I_2$.} \ldots
```

### Successful-event conditioning (probabilistic / RL proofs)

Define a high-probability event up front, then proceed deterministically on it:

```latex
\begin{proof}
Define the events
\begin{align*}
\mathcal{E}_1 &:= \{ \forall k \in [K], \, \widehat{\theta}_k \in \mathcal{C}_k \}, \\
\mathcal{E}_2 &:= \{ \forall k, h, \, |\widehat{r}_{k,h} - r_h| \le \beta_k \|\phi(s,a)\|_{\Sigma_k^{-1}} \}, \\
\mathcal{E}   &:= \mathcal{E}_1 \cap \mathcal{E}_2.
\end{align*}
By \Cref{lem:concentration_theta} and \Cref{lem:concentration_r} together with a union
bound, $\Pr[\mathcal{E}] \ge 1 - \delta$. In the rest of the proof, we condition on $\mathcal{E}$.

\medskip
On $\mathcal{E}$, we prove the claim by induction on $h$, downward from $h = H+1$ to $h = 1$.
\ldots
\end{proof}
```

This pattern lets all subsequent algebra read as deterministic. The cost is paid once, at the top.

---

## Proof boundaries

### Opening

Begin every proof with a one-sentence strategy statement. Example:
*"The proof proceeds in three stages. We first show the Gram matrix is well-conditioned at initialization, then that small perturbations preserve this conditioning, and finally that the iterates stay within the perturbation region."*

If the proof needs an inductive hypothesis or notation fixed up-front, state it before the first display.

### Closing

Close every proof with an explicit cue. Choose **one** of the following and use it uniformly across the paper:

- "This completes the proof."
- "Rearranging terms completes the proof."
- "as desired."
- "This gives the assertion."
- `\qed`

Then `\end{proof}`. Never end a proof with a dangling `align*` and no closing prose.
