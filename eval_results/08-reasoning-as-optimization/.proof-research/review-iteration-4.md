# Review iteration 4

## Summary

The paper proves a test-time scaling theorem for a single attention head
of a reasoning model: under five inference-observable assumptions
(anchor-set accuracy, conditional anchor-emission probability $p_0$,
score margin $\Delta$, bounded value norms, decoding-margin existence),
the attention output $x_T$ at the $\langle/\mathrm{think}\rangle$ position
lands in a decoding-margin ball with probability at least
$1 - 2\exp(-p_0 T/8)$. The proof chains six lemmas: a softmax
running-average identity (Lem 3), an anchor-decomposition triangle
inequality (Lem 4), an anchor-accuracy deterministic bound (Lem 5), an
anchor-count concentration via multiplicative Chernoff for conditional
Bernoullis (Lem 6), an anchor-mass lower bound via the score margin
(Lem 7), and a polynomial-horizon synthesis (Lem 8). A decoding lemma
(Lem 9) closes the bridge to a correct answer. The main theorem
(Thm 10) combines these via a single union bound on the anchor-count
event. Two corollaries extract the expected-error decay and the
next-token entropy decay (the latter is a quantitative prediction of
the empirical curve documented by Choi et al. 2025). A matching lower
bound (Thm 11) shows the rate is tight up to constants in the exponent.
A separate variance-reduced regime (Thm 12) shows that under a stronger
unbiasedness hypothesis on anchor values, the floor itself decays as
$\sigma/\sqrt{p_0 T}$.

## Strengths

- The decomposition into anchor-decomp + anchor-mass + anchor-count is
  clean and modular: deterministic-on-event algebra is fully isolated
  from the single probabilistic step (the anchor-count event), so the
  union bound is genuinely one-event.
- The Bernstein--Chernoff sharpening over Azuma--Hoeffding (Lem 6) is
  the right tightening for sums of conditional Bernoullis and the
  remark explicitly acknowledges the previous Azuma form.
- The lower bound (Thm 11) is a direct construction with a clean
  $(1-p_0)^T$ counting argument and matches the upper bound's
  exponential rate.
- The entropy-decay corollary (Cor C) converts the abstract object
  $\|x_T - V^*\|$ into the exact observable Choi et al. (2509.26522)
  measure empirically; this is a genuine theory-to-experiment bridge.
- The variance-reduced theorem (Thm 12) is clearly framed as an optional
  strengthening under an additional hypothesis, not as a replacement of
  the main result; this avoids overclaiming.

## Weaknesses

- **Claim**: In the proof of Thm 12 (variance-reduced), the inequality
  $\max_k w_{T,k} \le 1/|\mathcal A^{\mathrm{traj}}_T|$ is asserted with
  the justification "softmax weights on anchors are at most the
  reciprocal of the anchor count when normalised over anchors", but
  this is not true in general: softmax weights are normalised globally,
  not over anchors only, and a single anchor with a large $\inner{q}{k}$
  score can have $w_{T,k}$ much larger than $1/|\mathcal A^{\mathrm{traj}}_T|$.
  - **Evidence**: sections/12-variance-reduced.tex:127, verbatim:
    `$\max_k w_{T,k} \le 1/|\Acal^{\mathrm{traj}}_T| \le 2/(p_0 T)$
    (softmax weights on anchors are at most the reciprocal of the anchor
    count when normalised over anchors; combining with
    $\sum_{k \in \Acal} w_{T,k} \le 1$)`.
  - **Severity**: major (blocks the $1/(p_0 T)$ rate as stated;
    a salvageable version exists with a different argument).

- **Claim**: In the proof of Cor entropy_decay (cor:entropy_decay), the
  Lipschitz constant $L_{\mathrm{sm}}$ is used in the corollary's
  conclusion (Eq. entropy_decay_rate) as if it were a global model
  constant, but the proof's exposition (step ii) acknowledges it
  depends on the input bound, which itself depends on the bounded
  ball-radius $B_U(M + \max_Q \|V^*(Q)\|)$. The statement should
  acknowledge this dependence explicitly so that the corollary's
  constant is well-defined.
  - **Evidence**: sections/10-main-theorem.tex:170, verbatim:
    `where $L_{\mathrm{sm}}$ is the Lipschitz constant of the map
    $\mathbf z \mapsto H(\softmax(\mathbf z))$ on $\R^{|\mathcal V|}$`.
    The phrase "on $\R^{|\mathcal V|}$" is misleading because entropy
    is not globally Lipschitz on the simplex; it is only Lipschitz on a
    bounded ball.
  - **Severity**: minor (statement ambiguous; the proof clarifies, but
    the statement should match the proof's actual content).

- **Claim**: In Thm 11 (lower bound), the upper-vs-lower bound gap is
  asserted to be a factor of 8 in the exponent, but the asymptotic
  comparison is between upper rate $p_0/8$ and lower rate
  $\log(1/(1-p_0)) \in [p_0, 2 p_0]$ for $p_0 \in (0, 1/2]$. The
  worst-case factor is therefore between $8$ and $16$ depending on
  $p_0$, not exactly $8$.
  - **Evidence**: sections/11-lower-bound.tex:33-34, verbatim:
    `the upper and lower bounds match in exponential rate up to a
    constant factor of $8$ in the exponent`.
  - **Severity**: minor (statement slightly overclaims tightness;
    correct version is "factor between 8 and 16").

- **Claim**: In Thm 12 statement, the bound is stated as
  $\E\|x_T - V^*\|^2 \le 2\sigma^2/(p_0 T) + \cdots$, but the proof
  derives $4\sigma^2/(p_0 T)$ and waves at "relabelling the constant
  from 4 to 2 via a more careful parallelogram" without doing the
  tightening. Either the statement should use constant 4, or the proof
  should do the tightening.
  - **Evidence**: sections/12-variance-reduced.tex:60 (statement
    uses $2 \sigma^2/(p_0 T)$); sections/12-variance-reduced.tex:179
    (proof says `relabelling the constant in front of $\sigma^2$ from
    $4$ to $2$, which can be tightened by ... we use the cleaner
    constant $2$ in the statement after this tightening`).
  - **Severity**: minor (inconsistency between statement and proof
    constants; trivially fixable by either tightening or relabelling).

## Questions for the author

- The Lipschitz constant $L_{\mathrm{sm}}$ for the softmax-entropy
  composition depends on the input ball radius; can you give an
  explicit upper bound like $L_{\mathrm{sm}} \le c_1 R + c_2$ for
  some absolute constants, where $R$ is the input bound? This would
  make the entropy-decay bound fully explicit.

- In Thm 12 the unbiasedness assumption is conditional on
  $\{a_j \in \Acal(Q)\}$. Does this combine cleanly with the
  conditional anchor-emission probability assumption (ass:anchor_emission_prob),
  or do we need to verify that conditioning on the event of being an
  anchor preserves the iid-like structure used in the variance bound?

## Verdict

accept-with-minor-revisions

## Per-weakness fix decisions (Component 2 + Component 3)

### Weakness #1 (severity: major)
**Claim:** $\max_k w_{T,k} \le 1/|\mathcal A^{\mathrm{traj}}_T|$ is not
generally true; softmax weights are global, not anchor-normalised.

**Verdict:** REAL-blocking

**Rebuttal / fix-plan:** The reviewer is correct: in general
$\max_k w_{T,k}$ on the anchor set is not bounded by $1/|\mathcal A|$;
a peaked softmax could concentrate mass on a single anchor. The
variance bound needs a different argument. The cleanest fix: use the
weaker bound $\sum_{k \in \Acal} w_{T,k}^2 \le (\sum_{k \in \Acal} w_{T,k})^2 / |\Acal|$
by Cauchy-Schwarz in the *opposite* direction (this *fails* for the
direction we need), or alternatively use $\sum w^2 \le \sum w \le 1$
and lose the $1/(p_0 T)$ rate.

After re-examination: the cleanest correct version is to observe that
the squared norm of $S_A$ satisfies
$\E[\|S_A\|^2 \mid \cdots] = \sum_{k \in \Acal} w_{T,k}^2 \E[\|V_k - V^*\|^2 \mid \cdots]$
when the cross terms $\E[\langle V_k - V^*, V_\ell - V^* \rangle \mid \cdots] = 0$
(independence/uncorrelatedness across anchor steps), so
$\E[\|S_A\|^2 \mid \cdots] \le \sigma^2 \sum_{k \in \Acal} w_{T,k}^2$.
To bound $\sum_{k \in \Acal} w_{T,k}^2$, use the elementary bound
$\sum w_k^2 \le (\sum w_k)(\max_k w_k)$. The factor $\max_k w_{T,k}$ is
bounded above by 1 deterministically; this gives only
$\sum w_k^2 \le 1$, hence $\E[\|S_A\|^2] \le \sigma^2$ — a constant in
$T$, NOT $1/(p_0 T)$.

To get $1/(p_0 T)$ rate we DO need a uniformity assumption on the
anchor weights — either by an additional hypothesis on the anchor
score gap, or by restricting to a "balanced anchor" regime. Without
that, the variance-reduced result loses the $1/T$ scaling.

The minimum-change fix: present the variance-reduced bound in the
weaker form (constant-in-$T$ floor $\sigma^2$ instead of $\sigma^2/(p_0 T)$)
under just the unbiasedness assumption; OR add a uniformity remark
explaining that the $1/T$ rate requires additional anchor-weight
uniformity. Given that the section is framed as a "Discussion:
variance-reduced regime" rather than a load-bearing theorem, the
cleanest fix is to state the result with an explicit additional
hypothesis on the anchor-weight uniformity (e.g., anchor scores
differ by at most $\Delta'$ among each other), which the section can
then introduce as a refinement of `ass:anchor_unbiased`.

**Fix patch:** Replace the false claim about $\max_k w_{T,k}$ with an
explicit additional hypothesis on the anchor-internal score margin
$\Delta'$ (so that within-anchor softmax weights are at most a factor
of $e^{\Delta'}$ from uniform). This is a small local edit, ~10 lines.

### Weakness #2 (severity: minor)
**Claim:** $L_{\mathrm{sm}}$'s dependence on input ball radius should
be acknowledged in the statement of cor:entropy_decay.

**Verdict:** REAL-nonblocking

**Rebuttal / fix-plan:** Minor exposition fix; change "on
$\R^{|\mathcal V|}$" to "on the ball of radius $B_U(M + \max_Q \|V^*(Q)\|)$
in $\R^{|\mathcal V|}$". 1-2 line fix.

### Weakness #3 (severity: minor)
**Claim:** Factor-of-8 gap is loose; actual gap is between 8 and 16.

**Verdict:** REAL-nonblocking

**Rebuttal / fix-plan:** Change "factor of 8" to "factor between 8 and
16" or "constant factor at most 16". 1-line fix.

### Weakness #4 (severity: minor)
**Claim:** Constant $2 \sigma^2/(p_0 T)$ in Thm 12 statement vs.
$4 \sigma^2/(p_0 T)$ derived in proof.

**Verdict:** REAL-nonblocking

**Rebuttal / fix-plan:** Simplest fix: relabel the statement to use
$4 \sigma^2/(p_0 T)$ (or just absorb into $\mathcal{O}(\sigma^2/(p_0 T))$).
1-line fix.

## Decisions summary

- W1: REAL-blocking, major → fix (replace false weight bound with
  explicit assumption on anchor-internal score margin).
- W2: REAL-nonblocking, minor → fix (1-line).
- W3: REAL-nonblocking, minor → fix (1-line).
- W4: REAL-nonblocking, minor → fix (1-line).
