# Results

This directory holds simulation configurations and raw solver outputs.

## Authoritative

- [`joint-vs-disjoint/`](joint-vs-disjoint/) — the joint-vs-disjoint CPLEX study
  used by the paper. `results.ipynb` holds the per-run data; `runner.sh`
  reproduces it. The corrected, statistically-honest re-analysis derived from it
  lives under [`../analysis/`](../analysis/).
- [`config-fattree-k-6/`](config-fattree-k-6/), [`config-usnet/`](config-usnet/)
  — the topology / VNF-type / VNFM configurations for the two evaluated networks.

## Archival (not used by the current analysis or the paper)

- [`report/`](report/) and the loose `fattree-k-10-*.csv` files are raw outputs
  from earlier, exploratory heuristic runs (`bari`/`rari`/`oabu`). They are kept
  for provenance only; the published heuristic-vs-exact numbers come from the
  paper and [`../simulation/`](../simulation/), and the feasibility analysis comes
  from [`../analysis/`](../analysis/). Treat these files as historical, not as a
  reproducible result set.
