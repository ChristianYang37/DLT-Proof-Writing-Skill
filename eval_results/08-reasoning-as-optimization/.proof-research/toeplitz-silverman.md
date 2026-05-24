# Toeplitz / Silverman–Toeplitz lemma — weighted-mean convergence

**Source.** Hardy, *Divergent Series* (1949), §3.2; Boos, *Classical and Modern
Methods in Summability* (2000), Ch. 2. Standard textbook material, often cited
without source. The form used here is the "row-stochastic regular matrix"
version (Silverman 1913, Toeplitz 1911).

**Statement (Toeplitz / Silverman regularity).** Let $(w_{j,k})_{j,k \ge 1}$
be a triangular array of non-negative weights with $w_{j,k} = 0$ for $k > j$
and $\sum_{k=1}^j w_{j,k} = 1$ for every $j$. Suppose furthermore that for every
fixed $k$, $w_{j,k} \to 0$ as $j \to \infty$. Then for any sequence $(v_k)$ with
$v_k \to v^*$ in a normed space, the weighted average
$$
  \bar v_j \;\coloneqq\; \sum_{k=1}^j w_{j,k}\, v_k
$$
also converges to $v^*$.

**Quantitative form.** If $\|v_k - v^*\| \le \varepsilon_k$ with $\varepsilon_k \to 0$,
then $\|\bar v_j - v^*\| \le \sum_{k=1}^j w_{j,k}\, \varepsilon_k$. Splitting at any
$N$ and bounding the head by $\max_{k \le N} w_{j,k} \cdot \sum_{k \le N}\varepsilon_k$
and the tail by $\max_{k > N}\varepsilon_k$ gives the standard $\varepsilon/2$
argument. This is the **rate** Toeplitz delivers — it does not by itself give
an explicit $T = \poly$ bound; the rate is inherited from $\varepsilon_k$ and
from the *concentration rate* of the weights.

**Hypotheses (verbatim).**
- Row sums equal one: $\sum_{k=1}^j w_{j,k} = 1$.
- Non-negativity: $w_{j,k} \ge 0$.
- Vanishing-head: $\lim_{j\to\infty} w_{j,k} = 0$ for each fixed $k$.

(The classical statement allows complex weights with row-norm bounded uniformly
and $\sum_k w_{j,k} \to 1$; the simplified non-negative version above is what we
will use.)

**Direct relevance to the softmax recurrence.** With keys $k_1,\dots,k_j$ along
a reasoning trajectory and a fixed query $q$ at the `</think>` position,
$$
  x_j \;=\; \frac{1}{s_j} \sum_{k=1}^j e^{q^\top k_k}\, V_k \;=\; \sum_{k=1}^j w_{j,k} V_k,
  \qquad w_{j,k} \coloneqq \frac{e^{q^\top k_k}}{s_j}.
$$
The Toeplitz hypotheses translate to:
1. **Row sums:** automatic, by softmax normalisation.
2. **Non-negativity:** automatic, since $e^{q^\top k_k} > 0$.
3. **Vanishing-head:** $w_{j,k} \to 0$ as $j \to \infty$ for fixed $k$ iff
   $s_j \to \infty$, i.e. the cumulative softmax denominator diverges. This is
   the *only* non-trivial hypothesis on the LLM. It is implied by either
   (a) the per-step exponents being lower-bounded ($q^\top k_k \ge -B$ uniformly)
   so $s_j \ge j e^{-B}$, or (b) the trajectory containing infinitely many keys
   with $q^\top k_k \ge -B$ (a non-vanishing-attention condition).

**Quantitative rate via the weights.** If $\max_{k \le N} w_{j,k} \le \alpha_j$
with $\alpha_j \to 0$, splitting at $N = \lceil j/2\rceil$ gives
$\|x_j - V^*\| \le \alpha_j \cdot \|V\|_\infty \cdot N + \max_{k > N}\|V_k - V^*\|$.
With $q^\top k_k$ bounded in $[-B,B]$, $w_{j,k} \le e^{2B}/j$ so $\alpha_j = e^{2B}/j$
and the rate is $\mathcal O(1/j + \max_{k > j/2}\|V_k - V^*\|)$.

**Common misuses.**
- **Forgetting non-negativity:** the general (signed) Toeplitz needs $\sup_j \sum_k |w_{j,k}| < \infty$. For softmax weights this is automatic but worth stating.
- **Conflating $v_k \to v^*$ with `$V_k$ are good values':** Toeplitz needs convergence of the un-weighted sequence; if $V_k$ oscillates and only a *subsequence* converges, one needs a more refined argument (e.g. the dominant-weight subsequence).
- **Assuming $s_j \to \infty$ without justification:** if attention scores are uniformly $-\infty$ (e.g. the query embedding is orthogonal to all key embeddings), $s_j$ can converge and Toeplitz fails. The vanishing-head condition must be checked.
- **Confusing Toeplitz with Cesàro:** Cesàro is the special case $w_{j,k} = 1/j$. Softmax weights are *non-uniform*; one cannot apply Cesàro directly.

**Project citation key.** No direct citation needed — Toeplitz/Silverman is
folklore in summability theory; reference Hardy 1949 (`\cite{hardy1949divergent}`)
if a citation is needed at all. Most analysis textbooks prove it (Rudin's
*Principles of Mathematical Analysis*, Exercise 3.14).

**Critical caveat for THIS proof.** Toeplitz delivers *convergence of $x_j$ to
$V^*$* under the assumption that *$V_k \to V^*$*. The "g_j is a gradient" SGD
framing is therefore NOT load-bearing for convergence of $x_j$ — what is load-
bearing is that the value vectors along the trajectory have a limit, or
equivalently, that the model's *value projection* eventually agrees with a
target value. This is the cleanest sellable assumption.
