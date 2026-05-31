# Joint vs. Disjoint — corrected analysis

Re-derived from the per-run data in `results/joint-vs-disjoint/results.ipynb`. FatTree *trial 1* (no optimality-gap limit) is excluded; only the 5%-gap-limited run is kept. Significance is a paired Wilcoxon signed-rank test on the 10-15 runs per point (joint vs. disjoint on the **same** chain set).

## When does joint placement matter?

The value of joint VNF+VNFM placement is **entirely conditional on VNFM management being a binding constraint**. The mechanism is feasibility, not cost: joint placement accepts ~100% of chains in every regime, whereas disjoint placement *randomly produces management-infeasible layouts* and rejects whole chains after the fact. Averaging revenue hides this — the disjoint outcomes are **bimodal** (a run either nearly succeeds or collapses), which the acceptance-rate plots and the per-point coefficient of variation (`disj_CV%`, up to ~80%) expose.

- **Management binding (FatTree default; USnet + 4-hop radius):** joint dominates — up to 100%+ more revenue and 100% vs. ~20-60% acceptance. All points significant at p<0.05 (paired Wilcoxon).
- **Management NOT binding (USnet default):** joint adds no value — and is in fact *marginally worse* (revenue uplift is slightly **negative**, e.g. -0.9% at 150 chains, and statistically significant). Accounting for management when it does not bind diverts VNF placement for no benefit.
- **Practical takeaway:** the joint formulation pays off precisely when manager radius / capacity / resources are tight. A deployment should switch it on only in that regime; otherwise the simpler disjoint pipeline is as good or marginally better.


## FatTree (k=6, default VNFM)

**Management IS binding** — joint stays at ~100% acceptance while disjoint drops to 19% on average (worst single run 0%) at N=15, with a coefficient of variation up to 79% — i.e. unstable / bimodal.

|   N |   joint% |   disj% |   disj_min% |   disj_CV% |   rev_uplift% | p(rev)   |
|----:|---------:|--------:|------------:|-----------:|--------------:|:---------|
|  10 |    100.0 |    46.0 |         0.0 |       69.6 |         132.8 | <0.001   |
|  15 |    100.0 |    18.7 |         0.0 |       62.8 |         558.7 | <0.001   |
|  20 |    100.0 |    20.3 |         5.0 |       41.6 |         457.7 | <0.001   |
|  25 |    100.0 |    31.2 |         8.0 |       78.9 |         240.8 | <0.001   |
|  30 |    100.0 |    60.2 |         6.7 |       55.3 |          68.5 | <0.001   |
|  35 |    100.0 |    85.7 |        77.1 |        7.0 |          18.3 | <0.001   |
|  40 |    100.0 |    83.2 |        62.5 |       15.4 |          22.4 | <0.001   |
|  45 |    100.0 |    87.7 |        44.4 |       19.8 |          14.8 | <0.001   |
|  50 |     99.9 |    70.5 |        36.0 |       39.3 |          43.5 | 0.001    |
|  55 |    100.0 |    61.5 |        23.6 |       47.6 |          67.3 | <0.001   |
|  60 |     99.9 |    56.4 |        28.3 |       46.8 |          83.1 | <0.001   |
|  65 |     99.9 |    65.6 |        29.2 |       47.6 |          55.2 | <0.001   |
|  70 |    100.0 |    53.2 |        25.7 |       53.9 |          93.0 | 0.001    |
|  75 |     99.8 |    53.6 |        32.0 |       51.7 |          94.4 | <0.001   |
|  80 |    100.0 |    56.0 |        33.8 |       46.2 |          85.4 | <0.001   |
|  85 |    100.0 |    50.6 |        31.8 |       48.5 |         104.1 | 0.001    |
|  90 |    100.0 |    59.6 |        27.8 |       46.6 |          73.4 | <0.001   |


## USnet (4-hop manager radius)

**Management IS binding** — joint stays at ~100% acceptance while disjoint drops to 35% on average (worst single run 0%) at N=10, with a coefficient of variation up to 81% — i.e. unstable / bimodal.

|   N |   joint% |   disj% |   disj_min% |   disj_CV% |   rev_uplift% | p(rev)   |
|----:|---------:|--------:|------------:|-----------:|--------------:|:---------|
|  10 |    100.0 |    34.7 |         0.0 |       80.8 |         215.0 | <0.001   |
|  15 |    100.0 |    41.8 |        26.7 |       24.4 |         153.4 | <0.001   |
|  20 |    100.0 |    42.3 |        25.0 |       22.8 |         153.0 | <0.001   |
|  25 |    100.0 |    45.1 |        24.0 |       45.4 |         130.3 | <0.001   |
|  30 |     99.8 |    68.7 |        40.0 |       33.0 |          47.6 | <0.001   |
|  35 |    100.0 |    94.1 |        85.7 |        4.5 |           5.4 | 0.001    |
|  40 |     99.8 |    85.3 |        72.5 |        9.8 |          16.1 | <0.001   |
|  45 |     99.9 |    87.1 |        57.8 |       12.6 |          12.7 | <0.001   |
|  50 |     99.9 |    93.6 |        88.0 |        2.7 |           5.7 | <0.001   |
|  55 |     99.6 |    89.8 |        58.2 |       10.2 |          10.3 | <0.001   |
|  60 |     99.6 |    90.3 |        81.7 |        4.3 |           8.5 | <0.001   |
|  65 |     99.3 |    88.2 |        47.7 |       12.7 |          11.9 | <0.001   |
|  70 |     99.8 |    92.1 |        87.1 |        3.6 |           6.6 | <0.001   |
|  75 |     99.4 |    87.7 |        46.7 |       12.8 |          11.7 | <0.001   |
|  80 |     99.4 |    91.4 |        86.2 |        3.1 |           7.1 | <0.001   |
|  85 |     99.2 |    90.6 |        60.0 |        9.3 |           7.5 | <0.001   |
|  90 |     99.3 |    91.7 |        88.9 |        2.1 |           6.3 | <0.001   |


## USnet (default VNFM)

**Management is NOT binding** — disjoint reaches ~100% acceptance with zero variance, so the joint formulation adds no value in this regime.

|   N |   joint% |   disj% |   disj_min% |   disj_CV% |   rev_uplift% | p(rev)   |
|----:|---------:|--------:|------------:|-----------:|--------------:|:---------|
|  50 |    100.0 |   100.0 |       100.0 |        0.0 |          -0.0 | 1.000    |
|  75 |    100.0 |   100.0 |       100.0 |        0.0 |          -0.2 | 0.008    |
| 100 |    100.0 |   100.0 |       100.0 |        0.0 |          -0.3 | 0.002    |
| 125 |    100.0 |   100.0 |       100.0 |        0.0 |          -0.3 | 0.002    |
| 150 |     99.9 |   100.0 |       100.0 |        0.0 |          -0.9 | 0.002    |
