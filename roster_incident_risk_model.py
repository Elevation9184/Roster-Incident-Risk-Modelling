import numpy as np
import random
import matplotlib.pyplot as plt
from numba import njit

# 1) Define or import sample_binary_matrix_via_swaps here
@njit
def sample_binary_matrix_via_swaps_jit(row_sums, col_sums, n_swaps=100_000):
    n_rows, n_cols = len(row_sums), len(col_sums)
    M = np.zeros((n_rows, n_cols), dtype=np.int8)
    quotas = row_sums.copy()

    # 1) Greedy fill
    for j in range(n_cols):
        # simple selection sort to find top col_sums[j] quotas
        # (replace argsort)
        for _ in range(col_sums[j]):
            # find index of the current max quota
            max_i = 0
            for i in range(1, n_rows):
                if quotas[i] > quotas[max_i]:
                    max_i = i
            M[max_i, j] = 1
            quotas[max_i] -= 1

    # 2) Swap phase using np.random
    for _ in range(n_swaps):
        i = np.random.randint(0, n_rows)
        k = np.random.randint(0, n_rows)
        if k == i:
            k = (k + 1) % n_rows
        j = np.random.randint(0, n_cols)
        l = np.random.randint(0, n_cols)
        if M[i, j] and M[k, l] and not M[i, l] and not M[k, j]:
            M[i, j] = 0
            M[k, l] = 0
            M[i, l] = 1
            M[k, j] = 1

    return M

# 2) Generate realistic margins

TIER_SPECS = {
    'A': {'hrs_m': 36, 'hrs_sd': 3, 'count': 15},   # 3     shifts per week
    'B': {'hrs_m': 24, 'hrs_sd': 4, 'count': 10},   # 2     shifts per week
    'C': {'hrs_m': 18, 'hrs_sd': 3, 'count':  9},   # 1     shift  per week
    'D': {'hrs_m':  9, 'hrs_sd': 2, 'count':  3},   # 0.75  shifts per week
    'E': {'hrs_m': 48, 'hrs_sd': 2, 'count':  1},   # 4     shifts per week
}

# print("Tier  Avg Hours/wk   ≈ Shifts/wk")
# print("----  -------------  -------------")

# for tier, spec in TIER_SPECS.items():
#     hrs = spec['hrs_m']
#     shifts = hrs / 12  # Assuming 12-hour shifts
#     print(f" {tier}     {hrs:>5} hrs/wk       ≈ {shifts:>4.2f} shifts/wk")

def generate_realistic_row_sums(rng, n_shifts, specs=TIER_SPECS):
    """
    rng       : np.random.Generator
    n_shifts  : total number of shifts in the period
    specs     : dict of tier → {hrs_m, hrs_sd, count}
    """
    # build and shuffle tier list
    tiers = sum(([t] * specs[t]['count'] for t in specs), [])
    rng.shuffle(tiers)

    row_sums = []
    for t in tiers:
        # convert to fill‐rate and its SD
        μ_rate = specs[t]['hrs_m'] / 168      # Hours per week
        σ_rate = specs[t]['hrs_sd'] / 168

        # sample a rate, clip to [0,1], then convert to shifts
        rate = rng.normal(μ_rate, σ_rate)
        rate = np.clip(rate, 0.0, 1.0)
        shifts = int(round(rate * n_shifts))
        row_sums.append(shifts)

    return row_sums

def generate_realistic_col_sums(n_shifts, rng):
    col_sums = []
    for s in range(n_shifts):
        if s % 2 == 0:
            staff = rng.normal(8.78, 2.39)  # Day shift cover estimated from CEH/16
        else:
            staff = rng.normal(5.63, 0.81)  # Night shift cover estimated from CEH/16
        col_sums.append(int(round(np.clip(staff, 3, 12))))
    return col_sums

# 4) Monte Carlo simulation of max incidents
def simulate_max_incidents(row_sums, col_sums, rng, n_runs=1000, n_swaps=20_000, incident_count=61):
    maxima = []
    for _ in range(n_runs):
        roster = sample_binary_matrix_via_swaps_jit(row_sums, col_sums, n_swaps)
        # use the same NumPy RNG for incident sampling
        incident_shifts = rng.choice(len(col_sums), size=incident_count, replace=False)
        counts = roster[:, incident_shifts].sum(axis=1)
        maxima.append(int(counts.max()))
    return maxima

# 5) Plot and summary
def plot_histogram(maxima, incident_count, n_shifts):
    min_m, max_m = min(maxima), max(maxima)
    bins = np.arange(min_m - 0.5, max_m + 1.5, 1)

    plt.figure()
    plt.hist(maxima, bins=bins, edgecolor='black')
    plt.xticks(np.arange(min_m, max_m + 1, 1))
    plt.xlim(min_m - 0.5, max_m + 0.5)
    plt.xlabel('Max Incidents per Nurse')
    plt.ylabel('Frequency')
    plt.title(
        f'Highest Nurse Incident Count Given {incident_count} Incidents\n'
        f'Distributed Across {n_shifts} shifts (Avg {len(maxima)} Simulations)'
    )
    plt.tight_layout()
    plt.show()

def run(seed=123,
        n_days=384,
        incident_count=20,
        n_runs=1000,
        n_swaps=20_000):
    # 1) Central seed point
    np.random.seed(seed)
    random.seed(seed)
    rng = np.random.default_rng(seed)

    # 2) Generate margins
    n_shifts = n_days * 2
    row_sums = generate_realistic_row_sums(rng, n_shifts)
    col_sums = generate_realistic_col_sums(n_shifts, rng)

    # 3) Balance totals exactly as before
    total_needed = sum(col_sums)
    raw = np.array(row_sums, float)
    scaled = np.round(raw / raw.sum() * total_needed).astype(int)
    scaled[0] += (total_needed - scaled.sum())
    row_sums = scaled.tolist()

    # 4) Monte Carlo
    maxima = simulate_max_incidents(row_sums, col_sums, rng,
                                   n_runs=n_runs,
                                   n_swaps=n_swaps,
                                   incident_count=incident_count)

    # 5) Plot & report
    plot_histogram(maxima, incident_count, n_shifts)
    # observed_max = 25
    # p_empirical = sum(m >= observed_max for m in maxima)/len(maxima)
    # print(f"Empirical P(max ≥ {observed_max}) ≈ {p_empirical:.3f}")

if __name__ == "__main__":
    run(seed=2025, incident_count=50, n_runs=1000, n_swaps=20_000)
