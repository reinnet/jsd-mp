# Joint-vs-disjoint analysis

Two parts:

1. **Corrected re-analysis** of `results/joint-vs-disjoint/results.ipynb` —
   reports **chain acceptance rate** (feasibility) with **paired significance
   tests** instead of mean-revenue line plots, and drops the FatTree *trial 1*
   data (CPLEX run with no optimality-gap limit).
   → `joint_vs_disjoint_corrected.py`, `SUMMARY.md`
2. **Sensitivity sweep** (`sensitivity_sweep.py`, `SWEEP.md`) — a live heuristic
   reproduction in this repo that pins down *when* joint placement matters, by
   toggling a management constraint and sweeping load/capacity.

## Reproduce

```sh
python3 -m venv .analysis-venv
.analysis-venv/bin/pip install numpy pandas matplotlib scipy tabulate pyyaml click
.analysis-venv/bin/python analysis/joint_vs_disjoint_corrected.py   # part 1 (instant)
.analysis-venv/bin/python analysis/sensitivity_sweep.py             # part 2 (~80s)
```

## Outputs

Part 1 (corrected re-analysis):
- `SUMMARY.md` — writeup ("when does joint placement matter") + per-regime tables
- `summary.csv` — full per-(experiment, N) statistics
- `acceptance_*.png` — acceptance-rate plots (joint vs disjoint, worst-run + significance markers)
- `revenue_*.png` — mean-revenue plots, for reference

Part 2 (sensitivity sweep):
- `SWEEP.md` — the controlled experiments + takeaway
- `sweep_constraint.{csv,png}` — toggle the management constraint across load
- `sweep_capacity.{csv,png}` — capacity as a non-binding lever (negative control)

## Headline

Joint VNF+VNFM placement reaches ~100% acceptance in every regime. Its value is
**conditional on management being a binding constraint**:

| Regime | Joint vs disjoint |
|---|---|
| FatTree (default VNFM) | joint dominates (100% vs ~20-60% accept) |
| USnet + 4-hop radius | joint dominates (100% vs ~35-94% accept) |
| USnet (default VNFM) | no benefit — joint marginally *worse* (−0.2 to −0.9% revenue, p<0.01) |

The sweep confirms the mechanism causally: with the management constraint
removed, disjoint **equals** joint at every load (gap 0); with it present, joint
leads by up to ~18pp acceptance, decaying to 0 as load saturates raw VNF
resources. Manager capacity is *not* the lever (gap ~constant from cap 1→100).
