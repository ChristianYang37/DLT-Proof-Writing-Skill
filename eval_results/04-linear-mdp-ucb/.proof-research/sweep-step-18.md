# Sweep re-derivation — Step 18 (q_3 resolvent identity)

**Step.** Show $\langle\phi(x,a),q_3\rangle = P_h(V_{h+1}^k-V_{h+1}^\pi)(x,a)
- \lambda\langle\phi(x,a),(\Lambda_h^k)^{-1}\int(V_{h+1}^k-V_{h+1}^\pi)\,d\mu_h\rangle$,
where $q_3=(\Lambda_h^k)^{-1}\sum_\tau\phi_h^\tau[(P_hV_{h+1}^k-P_hV_{h+1}^\pi)
(x_h^\tau,a_h^\tau)]$.

**Available hypotheses.** Linear MDP ($P_hg(x,a)=\langle\phi(x,a),\int g\,d\mu_h
\rangle$); $\Lambda_h^k=\sum_\tau\phi_h^\tau(\phi_h^\tau)^\top+\lambda I$.

**Independent derivation.**
1. $(P_hV_{h+1}^k-P_hV_{h+1}^\pi)(x_h^\tau,a_h^\tau)=(\phi_h^\tau)^\top\int
   (V_{h+1}^k-V_{h+1}^\pi)\,d\mu_h$ (linear MDP). Let $g:=\int(V_{h+1}^k-
   V_{h+1}^\pi)\,d\mu_h\in\R^d$.
2. $q_3=(\Lambda_h^k)^{-1}\sum_\tau\phi_h^\tau(\phi_h^\tau)^\top g
   =(\Lambda_h^k)^{-1}(\Lambda_h^k-\lambda I)g=(I-\lambda(\Lambda_h^k)^{-1})g$,
   using $\sum_\tau\phi_h^\tau(\phi_h^\tau)^\top=\Lambda_h^k-\lambda I$.
3. $\langle\phi(x,a),q_3\rangle=\langle\phi(x,a),g\rangle-\lambda\langle\phi(x,a),
   (\Lambda_h^k)^{-1}g\rangle$.
4. $\langle\phi(x,a),g\rangle=\langle\phi(x,a),\int(V_{h+1}^k-V_{h+1}^\pi)d\mu_h
   \rangle=P_h(V_{h+1}^k-V_{h+1}^\pi)(x,a)$ (linear MDP again).

**Verdict.** matches.

**Notes.** The resolvent identity $(\Lambda)^{-1}(\Lambda-\lambda I)=I-\lambda
\Lambda^{-1}$ is the only non-obvious move; it is exact. No constant drift.
