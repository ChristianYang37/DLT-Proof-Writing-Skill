"""
Phase C.5 numeric/symbolic verification of the load-bearing algebra chains
in the Stage-2 proof bodies. Script-validation path to 🟢.

Run: python sweep-numeric-checks.py
"""
import numpy as np
import sympy as sp

rng = np.random.default_rng(0)
results = {}

# ---------------------------------------------------------------------------
# CHECK 1 (02 / 09): net-drift identity  E[s_k | F] = delta * E[|s_k|]
# under conditional independence of sign zeta=sign(s) and magnitude |s|,
# with Pr[zeta=+1]=p, delta=2p-1.  Monte-Carlo over a sign-mixture model.
# ---------------------------------------------------------------------------
def check_net_drift():
    ok = True
    for p in [0.5, 0.62, 0.8, 0.95]:
        delta = 2*p - 1
        N = 4_000_000
        # magnitude law: independent of sign (here Gamma), floored implicitly
        mag = rng.gamma(shape=2.0, scale=0.7, size=N)        # |s_k|
        sign = np.where(rng.random(N) < p, 1.0, -1.0)        # zeta, indep of mag
        s = sign * mag
        lhs = s.mean()                 # E[s_k]
        rhs = delta * mag.mean()       # delta * E[|s_k|]
        if abs(lhs - rhs) > 5e-3 * max(1.0, abs(rhs)):
            ok = False
        results.setdefault("net_drift_detail", []).append(
            (p, round(lhs,4), round(rhs,4)))
    return ok
results["1_net_drift_identity"] = check_net_drift()

# ---------------------------------------------------------------------------
# CHECK 2 (10): Azuma/Bernstein constant. Variance-dominated Freedman:
# Pr[max_t sum M_s >= u] <= exp(-u^2 / (2(v + c u/3))).  With v=2 sigma^2 T/d,
# and the regime v + c u/3 <= 2v, the two-sided bound = delta at
# u = 2 sigma sqrt(T log(2/delta)/d).  Verify the exponent arithmetic.
# ---------------------------------------------------------------------------
def check_azuma_constant():
    sigma, T, d, delta = 1.3, 5000, 400, 0.05
    v = 2*sigma**2*T/d
    u = 2*sigma*np.sqrt(T*np.log(2/delta)/d)
    # variance-dominated: denominator 2*(2v)=4 sigma^2 T/d
    exponent = u**2 / (4*sigma**2*T/d)         # = u^2 d/(4 sigma^2 T)
    two_sided = 2*np.exp(-exponent)
    # claim: exponent == log(2/delta), so 2 exp(-exponent) == delta
    results["azuma_exponent_vs_log"] = (round(exponent,5),
                                        round(np.log(2/delta),5))
    return abs(two_sided - delta) < 1e-9
results["2_azuma_constant"] = check_azuma_constant()

# ---------------------------------------------------------------------------
# CHECK 3 (06): quadratic variation. softmax weights with |s_j|<=S satisfy
# max_t w_t <= 1/(1+(T-1)e^{-2S}) <= e^{2S}/T, and S_T = sum w^2 <= e^{2S}/T.
# Random scores in [-S,S]; verify both inequalities hold.
# ---------------------------------------------------------------------------
def check_quad_variation():
    ok = True
    for S in [0.5, 1.0, 2.0]:
        for _ in range(2000):
            T = rng.integers(5, 400)
            s = rng.uniform(-S, S, size=T)
            w = np.exp(s); w /= w.sum()
            maxw = w.max()
            if not (maxw <= 1/(1+(T-1)*np.exp(-2*S)) + 1e-12):  # first bound
                ok = False
            if not (maxw <= np.exp(2*S)/T + 1e-12):             # second bound
                ok = False
            if not (np.sum(w**2) <= np.exp(2*S)/T + 1e-12):     # S_T bound
                ok = False
    return ok
results["3_quad_variation"] = check_quad_variation()

# ---------------------------------------------------------------------------
# CHECK 4 (07): retraction exponent. eta = O(1/sqrt d), residual eta^3 * sqrt d
# on the raw logit = O(1/d); divided by row-norm scale sqrt d = O(1/d^{1.5}).
# Symbolic check of the exponent bookkeeping.
# ---------------------------------------------------------------------------
def check_retraction_exponent():
    d = sp.symbols('d', positive=True)
    eta = 1/sp.sqrt(d)                 # eta = O(1/sqrt d)
    raw_logit_err = eta**3 * sp.sqrt(d)        # C_ret R_U eta^3 sqrt d  (R_U const)
    raw_simpl = sp.simplify(raw_logit_err)     # expect d^{-1}
    angular_err = raw_logit_err / sp.sqrt(d)   # divide by row-norm scale sqrt d
    ang_simpl = sp.simplify(angular_err)       # expect d^{-3/2}
    results["retraction_raw"] = str(raw_simpl)
    results["retraction_angular"] = str(ang_simpl)
    return (raw_simpl == 1/d) and (ang_simpl == d**sp.Rational(-3,2))
results["4_retraction_exponent"] = check_retraction_exponent()

# ---------------------------------------------------------------------------
# CHECK 5 (09): orthogonality variance E<e,u>^2 = 1/d for u uniform on S^{d-1}.
# ---------------------------------------------------------------------------
def check_orthogonality():
    ok = True
    for d in [10, 50, 200]:
        N = 200000
        U = rng.standard_normal((N, d)); U /= np.linalg.norm(U, axis=1, keepdims=True)
        e = np.zeros(d); e[0] = 1.0
        emp = np.mean((U @ e)**2)
        if abs(emp - 1/d) > 0.1/d:
            ok = False
    return ok
results["5_orthogonality_variance"] = check_orthogonality()

# ---------------------------------------------------------------------------
# CHECK 6 (12): second-moment / Paley-Zygmund. With pairwise correlation <= mu0,
# Var(N) <= E N + mu0 (E N)^2, so Pr[N>0] >= (E N)^2/((1+mu0)(E N)^2 + E N)
# >= (1-1/EN)/(1+mu0).  Verify the algebraic lower bound.
# ---------------------------------------------------------------------------
def check_paley_zygmund():
    ok = True
    for EN in [3.0, 10.0, 100.0]:
        for mu0 in [0.0, 0.2, 0.5]:
            VarN = EN + mu0*EN**2            # the bound (extremal)
            EN2 = EN**2 + VarN
            pz = EN**2 / EN2
            lb = (1 - 1/EN)/(1+mu0)
            if pz + 1e-9 < lb:               # claimed: pz >= lb
                ok = False
    return ok
results["6_paley_zygmund"] = check_paley_zygmund()

# ---------------------------------------------------------------------------
# CHECK 7 (13): margin-drift sharing. correct & incorrect drifts share D.
# margin drift = D(||W*|| - <W_a, hatW*>) >= D(rho0 - mu0 R_U) when mu0<rho0/R_U.
# Verify numerically over random unembeddings that the margin drift has the
# claimed lower bound and is positive under mu0 < rho0/R_U.
# ---------------------------------------------------------------------------
def check_margin_drift_sharing():
    ok = True
    d, V = 64, 400
    for _ in range(3000):
        W = rng.standard_normal((V, d))
        # normalize rows to norms in [rho0, R_U]
        norms = np.linalg.norm(W, axis=1, keepdims=True)
        W = W / norms
        rho0, R_U = 0.9, 1.1
        scales = rng.uniform(rho0, R_U, size=(V,1))
        W = W * scales
        astar = 0
        hatW = W[astar]/np.linalg.norm(W[astar])
        # incoherence mu0 = max off-diagonal normalized gram
        G = (W @ W.T) / (np.linalg.norm(W,axis=1)[:,None]*np.linalg.norm(W,axis=1)[None,:])
        np.fill_diagonal(G, 0.0)
        mu0 = np.abs(G[astar, 1:]).max()
        D = rng.uniform(0.0, 0.5)   # shared drift magnitude >=0
        # margin drift for worst incorrect a
        proj_inc = (W[1:] @ hatW)            # <W_a, hatW*>
        worst = proj_inc.max()
        margin_drift = D*(np.dot(W[astar], hatW) - worst)
        # claimed lower bound
        lb = D*(np.linalg.norm(W[astar]) - mu0*np.linalg.norm(W,axis=1).max())
        if margin_drift + 1e-9 < lb - 1e-6:  # margin_drift >= D(||W*|| - mu0 max||W||)
            ok = False
    return ok
results["7_margin_drift_sharing"] = check_margin_drift_sharing()

# ---------------------------------------------------------------------------
# CHECK 8 (11): loss-to-margin. L<log2 => p_correct>1/2 => max incorrect logit
# < correct logit. Verify p_correct>1/2 forces margin>0 over random logits.
# ---------------------------------------------------------------------------
def check_loss_to_margin():
    ok = True
    for _ in range(200000):
        d = 20
        z = rng.standard_normal(d)*2.0
        p = np.exp(z - z.max()); p /= p.sum()
        astar = int(np.argmax(rng.random(d)))   # arbitrary "correct" index
        L = -np.log(p[astar])
        if L < np.log(2):                        # hypothesis
            margin = z[astar] - np.max(np.delete(z, astar))
            if margin <= 0:                      # conclusion must hold
                ok = False
    return ok
results["8_loss_to_margin"] = check_loss_to_margin()

# ---------------------------------------------------------------------------
print("="*64)
for k in sorted(results):
    if k.startswith(tuple("12345678")):
        print(f"  {k}: {'PASS' if results[k] else 'FAIL'}")
print("-"*64)
print("  details:")
for k in results:
    if not k.startswith(tuple("12345678")):
        print(f"    {k}: {results[k]}")
print("="*64)
allpass = all(v for k,v in results.items() if k.startswith(tuple("12345678")))
print("ALL CHECKS PASS" if allpass else "SOME CHECKS FAILED")
