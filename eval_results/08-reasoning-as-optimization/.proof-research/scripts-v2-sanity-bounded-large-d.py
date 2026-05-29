"""
v2 sanity check — bounded box (Revision A), extended to d=3072

Per user request: "有边界的直觉是对的，但是我怀疑你采样的结果也太少了，
或许你跑到d=3072继续看看效果"

Setup (Revision A): Constrain ||x|| <= X_max via projection.
This mimics layer normalization — kills the centrifugal drift.

Compare against the unbounded v3 model (which showed wrong-signed lambda_c ~ d^{+0.14}).

Sweep: d in {16, 32, 64, 128, 256, 512, 1024, 2048, 3072}.
"""
import numpy as np
import json
import time


def sample_unit_vector(d, rng):
    v = rng.standard_normal(d)
    v /= np.linalg.norm(v)
    return v


def run_trajectory(d, lambda_0, bounded=True, alpha=0.05, sigma=0.05,
                   r_star=3.0, X_max=3.0, R_0=1.5, basin=0.3, T_max=3000, rng=None):
    """One trial. Returns (success_bool, hit_time)."""
    if rng is None:
        rng = np.random.default_rng()
    # Initialize on sphere of radius R_0
    x = sample_unit_vector(d, rng) * R_0
    for t in range(T_max):
        r = np.linalg.norm(x)
        if r < basin:
            return 1, t
        # Sample step
        u = sample_unit_vector(d, rng)
        # Effective rate (zero outside r_star)
        if r < r_star:
            effective = rng.random() < lambda_0
        else:
            effective = False
        if effective:
            g = alpha * (-x / r) + sigma * u
        else:
            g = sigma * u
        x = x + g
        # Boundary: project to ball of radius X_max
        if bounded:
            r_new = np.linalg.norm(x)
            if r_new > X_max:
                x = x * (X_max / r_new)
    return 0, T_max


def sweep(d, lambdas, bounded=True, n_trials=50, seed_base=42):
    rng = np.random.default_rng(seed=seed_base + d)
    results = []
    for lam in lambdas:
        successes = 0
        times = []
        for _ in range(n_trials):
            succ, t = run_trajectory(d, lam, bounded=bounded, rng=rng)
            successes += succ
            if succ:
                times.append(t)
        mean_time = np.mean(times) if times else -1
        results.append({
            'lambda': float(lam),
            'p_succ': successes / n_trials,
            'mean_hit_time': float(mean_time),
        })
    return results


def lambda_c_from_results(results, threshold=0.5):
    """Find lambda where success rate crosses threshold (log-linear interp)."""
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
    d_values = [16, 32, 64, 128, 256, 512, 1024, 2048, 3072]

    # Dense grid covering the expected transition region across all d
    # (theory predicts somewhere in 0.001..0.1)
    lambdas = np.logspace(-3.0, -0.5, 14)  # 0.001 to 0.316

    all_results = {'bounded': {}, 'unbounded': {}}

    for case_name, bounded in [('bounded', True), ('unbounded', False)]:
        print(f"=== {case_name.upper()} (X_max = {3.0 if bounded else 'inf'}) ===")
        t0 = time.time()
        for d in d_values:
            n_trials = 50 if d <= 1024 else 30
            res = sweep(d, lambdas, bounded=bounded, n_trials=n_trials)
            all_results[case_name][d] = res
            lc = lambda_c_from_results(res)
            elapsed = time.time() - t0
            # Show success curve compactly
            curve = ' '.join(f"{r['p_succ']:.2f}" for r in res)
            print(f"  d={d:5d} (n={n_trials}): λ_c≈{lc:.5f}  [{elapsed:5.1f}s]  curve: {curve}")
        print()

    print("=== Scaling fits (log-log linear regression) ===")
    for case in ['bounded', 'unbounded']:
        ds = np.array(d_values)
        lcs = np.array([lambda_c_from_results(all_results[case][d]) for d in d_values])
        slope, intercept = np.polyfit(np.log(ds), np.log(lcs), 1)
        print(f"  {case:10s}: λ_c ~ d^{{{slope:+.3f}}}, prefactor ~ {np.exp(intercept):.4f}")

    # Save raw
    out_path = '/tmp/v2-sanity-bounded-large-d-results.json'
    with open(out_path, 'w') as f:
        json.dump({k: {str(d): res for d, res in v.items()}
                  for k, v in all_results.items()}, f, indent=2)
    print(f"\nRaw results saved to {out_path}")
