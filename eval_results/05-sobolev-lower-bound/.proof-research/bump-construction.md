# Bump function construction for Sobolev minimax lower bounds

**Source.** Standard; see Tsybakov 2009 Chapter 2 (specifically the construction in §2.6.1 for Hölder; the Sobolev analogue is the same scaling argument).

**Construction.** Fix a non-zero function $\psi \in C^\infty_c(\R^d)$ supported in $(0,1)^d$ (e.g. a tensor product of a $C^\infty$ bump of one variable). Define
\[
\psi_k(x) \;:=\; \psi\bigl(m(x - x_k)\bigr) \quad \text{for } x_k = k/m,\ k \in \{0,1,\ldots,m-1\}^d.
\]
Each $\psi_k$ is supported in the grid cell $R_k := x_k + [0,1/m]^d \subset [0,1]^d$, and the cells $R_k$ are pairwise disjoint.

**Key norm identities.** By change of variables $y = m(x - x_k)$:
- $L^2$ norm: $\|\psi_k\|_{L^2}^2 = m^{-d} \|\psi\|_{L^2}^2$.
- $W^s_2$ norm (for integer $s$): each derivative of order $|\alpha| \leq s$ scales as $\|\partial^\alpha \psi_k\|_{L^2}^2 = m^{2|\alpha|} \cdot m^{-d} \|\partial^\alpha \psi\|_{L^2}^2$. Hence
\[
\|\psi_k\|_{W^s_2}^2 \;\leq\; m^{2s - d} \cdot \|\psi\|_{W^s_2}^2.
\]
(For fractional $s$, the same scaling holds via the Slobodeckij/Fourier definition.)

**Standard bump family.** For each $\omega \in \{0,1\}^{m^d}$ (indexed by $k$), define
\[
f_\omega(x) \;:=\; \frac{c_0}{m^s} \sum_{k} \omega_k\, \psi_k(x),
\]
where $c_0$ is chosen below.

**Sobolev norm of $f_\omega$.** Because the $\psi_k$ have disjoint supports, all derivatives are orthogonal across $k$, so
\[
\|f_\omega\|_{W^s_2}^2
\;=\; \frac{c_0^2}{m^{2s}} \sum_k \omega_k^2 \, \|\psi_k\|_{W^s_2}^2
\;\leq\; \frac{c_0^2}{m^{2s}} \cdot m^d \cdot m^{2s - d} \|\psi\|_{W^s_2}^2
\;=\; c_0^2 \|\psi\|_{W^s_2}^2.
\]
Choosing $c_0 := 1/\|\psi\|_{W^s_2}$ ensures $\|f_\omega\|_{W^s_2} \leq 1$, so $f_\omega \in W^s_2([0,1]^d)$ with norm $\leq 1$.

**$L^2$ separation.** For $\omega \neq \omega'$ with Hamming distance $\rho_H(\omega,\omega') \geq m^d/8$,
\[
\|f_\omega - f_{\omega'}\|_{L^2}^2
\;=\; \frac{c_0^2}{m^{2s}} \sum_k (\omega_k - \omega'_k)^2 \|\psi_k\|_{L^2}^2
\;=\; \frac{c_0^2}{m^{2s}} \cdot \rho_H(\omega,\omega') \cdot m^{-d} \|\psi\|_{L^2}^2
\;\geq\; \frac{c_0^2 \|\psi\|_{L^2}^2}{8} \cdot m^{-(2s + d)}.
\]
So pairwise $L^2$-distance is $\geq c_1 m^{-(s + d/2)}$ where $c_1 := c_0 \|\psi\|_{L^2} / (2\sqrt{2})$.

**$L^\infty$ bound.** Each $\psi_k$ has $\|\psi_k\|_\infty = \|\psi\|_\infty$, and supports are disjoint, so $\|f_\omega - f_{\omega'}\|_\infty \leq \frac{c_0}{m^s} \|\psi\|_\infty$.

**Common misuses.**
- Using $\psi$ that is only $C^k$ for $k < s$ — then $\|f_\omega\|_{W^s_2}$ might not be finite. The fix: take $\psi \in C^\infty_c$, which works for all $s$.
- Forgetting the $c_0 = 1/\|\psi\|_{W^s_2}$ normalization, leaving the constant in the radius constraint.

**Project citation key.** \cite{tsybakov2009introduction}
