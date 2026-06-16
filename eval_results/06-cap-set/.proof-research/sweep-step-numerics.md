# Sweep verification — numerical/identity steps (script-checked)

Independent re-derivation by a standalone Python script (not looking at the proof's
asserted constants). Verdict: **matches**, with one constant corrected.

## (i) $\F_3$ identity $1-u^2=\one[u=0]$
For $u\in\{0,1,2\}$: $u=0\Rightarrow u^2=0\Rightarrow 1-u^2=1$; $u\in\{1,2\}\Rightarrow
u^2=1\Rightarrow 1-u^2=0$. Script confirms `(1-(u*u)%3)%3 == [u==0]` for all $u$.
Verdict: matches.

## (ii) Monomial count $M_n=\sum_{s\le 2n/3}[u^s](1+u+u^2)^n$
Brute-force polynomial expansion of $(1+u+u^2)^n$ and summation of coefficients up to
$s=\lfloor 2n/3\rfloor$:
- $n=3$: $M_n=10$, $M_n^{1/n}=2.154$
- $n=12$: $M_n=57720$, $M_n^{1/n}=2.493$
- $n=30$: $M_n^{1/n}=2.616$
- $n=60$: $M_n^{1/n}=2.671$ (increasing toward $\approx 2.755$, consistent with the
  $\limsup$ bound).
Verdict: matches the generating-function encoding in \Cref{lem:monomial-count}.

## (iii) Chernoff optimum $3\gamma=\min_{0<t\le1}(1+t+t^2)t^{-2/3}$
Grid search + Brent root of the first-order condition
$\frac{1+2t}{1+t+t^2}=\frac{2}{3t}$:
- minimizer $t_\ast\approx 0.5931$ (NOT $0.5085$ — original draft had a wrong root;
  **corrected** in sections/05-monomial-count.tex:65 and the digest).
- minimum value $3\gamma\approx 2.75510 < 2.7558$. Verdict: matches (value correct,
  minimizer corrected).

Net effect on the proof: none on the bound $|A|\le 3M_n$ or on $3\gamma<2.7558$; only
the reported value of the minimizer $t_\ast$ was fixed. This is the confidence sweep
catching a transcription error in a non-load-bearing constant.
