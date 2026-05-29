"""
v5b: faster version of v5 argmax verifier.

Optimizations:
- Check argmax every 50 steps (not every step)
- Sample W_U once per d, reuse across all trials and lambdas for that d
- Vectorize multiple trials at once (batch)
- Smaller V = 256 (still has log V effect; predicted slope unchanged)
- print flushing
"""
import numpy as np
import json
import time
import sys


def run_batch_trajectories(W_U, lambda_0, target_idx=0, tau=0.1,
                           T_max=3000, n_trials=50, check_every=50,
                           rng=None):
    """Vectorized: run n_trials in parallel."""
    if rng is None:
        rng = np.random.default_rng()
    V, d = W_U.shape
    target_direction = W_U[target_idx]

    # x[i] is trial i's state
    x = np.zeros((n_trials, d), dtype=np.float32)
    done = np.zeros(n_trials, dtype=bool)
    hit_time = np.full(n_trials, T_max, dtype=np.int32)

    for t in range(T_max):
        # Update only non-done trials
        # Sample effective vs noise for each trial
        effective_mask = rng.random(n_trials) < lambda_0
        # Effective: g = target_direction
        # Noise: g = random unit vector
        rand_g = rng.standard_normal((n_trials, d)).astype(np.float32)
        rand_g /= np.linalg.norm(rand_g, axis=1, keepdims=True)

        g = np.where(effective_mask[:, None], target_direction[None, :], rand_g)

        # Only update non-done
        x[~done] += tau * g[~done]

        # Check argmax every `check_every` steps
        if (t + 1) % check_every == 0 or t == T_max - 1:
            # logits[i, v] = <W_U[v], x[i]>
            logits = x @ W_U.T  # (n_trials, V)
            argmax_idx = np.argmax(logits, axis=1)
            new_success = (argmax_idx == target_idx) & (~done)
            hit_time[new_success] = t + 1
            done |= new_success
            if done.all():
                break

    return done.astype(int), hit_time


def sweep(d, V, lambdas, n_trials=50, T_max=3000, seed=42):
    rng = np.random.default_rng(seed=seed + d * 1000 + V)
    # Sample W_U once for this d
    W_U = rng.standard_normal((V, d)).astype(np.float32)
    W_U /= np.linalg.norm(W_U, axis=1, keepdims=True)
    results = []
    for lam in lambdas:
        successes, hit_times = run_batch_trajectories(
            W_U, lam, n_trials=n_trials, T_max=T_max, rng=rng,
        )
        p_succ = successes.mean()
        results.append({
            'lambda': float(lam),
            'p_succ': float(p_succ),
        })
    return results


def lambda_c_from_results(results, threshold=0.5):
    for i in range(len(results) - 1):
        l1, p1 = results[i]['lambda'], results[i]['p_succ']
        l2, p2 = results[i + 1]['lambda'], results[i + 1]['p_succ']
        if p1 < threshold <= p2:
            t = (threshold - p1) / (p2 - p1)
            return float(np.exp(np.log(l1) + t * (np.log(l2) - np.log(l1))))
    if results[0]['p_succ'] >= threshold:
        return float(results[0]['lambda']) / 2
    return float(results[-1]['lambda']) * 2


if __name__ == '__main__':
    V = 256
    d_values = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    lambdas = np.logspace(-3.5, -0.3, 14)

    print(f"=== v5b: argmax verifier (V={V}), vectorized ===", flush=True)
    pred = np.sqrt(2 * np.log(V) / 3000)
    print(f"Theory: λ_c ~ √(2 log V / (T·d)) = {pred:.4f} · d^(-0.5)", flush=True)
    print(flush=True)

    all_results = {}
    t0 = time.time()
    for d in d_values:
        n_trials = 80 if d <= 1024 else 50
        res = sweep(d, V, lambdas, n_trials=n_trials)
        all_results[d] = res
        lc = lambda_c_from_results(res)
        elapsed = time.time() - t0
        curve = ' '.join(f"{r['p_succ']:.2f}" for r in res)
        print(f"  d={d:5d} (n={n_trials}): λ_c≈{lc:.5f}  [{elapsed:6.1f}s]", flush=True)
        print(f"      curve: {curve}", flush=True)

    print(flush=True)
    print("=== Scaling fit ===", flush=True)
    ds = np.array(d_values)
    lcs = np.array([lambda_c_from_results(all_results[d]) for d in d_values])
    slope, intercept = np.polyfit(np.log(ds), np.log(lcs), 1)
    print(f"  All d:  λ_c ~ d^{{{slope:+.4f}}}, prefactor ~ {np.exp(intercept):.5f}", flush=True)
    big = ds >= 64
    if big.sum() > 1:
        slope_big, intercept_big = np.polyfit(np.log(ds[big]), np.log(lcs[big]), 1)
        print(f"  d≥64:   λ_c ~ d^{{{slope_big:+.4f}}}, prefactor ~ {np.exp(intercept_big):.5f}", flush=True)
    print(f"  Predicted slope: -0.5  (prefactor {pred:.4f})", flush=True)

    print(flush=True)
    print("=== Detailed comparison ===", flush=True)
    print(f"  {'d':<6} {'observed':<12} {'predicted':<12} {'ratio':<8}", flush=True)
    for d in d_values:
        lc_obs = lambda_c_from_results(all_results[d])
        lc_pred = pred / np.sqrt(d)
        print(f"  {d:<6} {lc_obs:<12.5f} {lc_pred:<12.5f} {lc_obs/lc_pred:<8.3f}", flush=True)

    with open('/tmp/v5b-argmax-results.json', 'w') as f:
        json.dump({str(d): res for d, res in all_results.items()}, f, indent=2)
    print(f"\nSaved to /tmp/v5b-argmax-results.json", flush=True)
