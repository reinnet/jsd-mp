# Joint Service Deployment - Manager Placement

[![CI](https://github.com/reinnet/jsd-mp/actions/workflows/ci.yml/badge.svg)](https://github.com/reinnet/jsd-mp/actions/workflows/ci.yml)


## Introduction

JSD-MP solves the **joint** placement of Virtual Network Functions (VNFs) and the
VNF Managers (VNFMs) that manage them. Most placement work optimizes VNFs first
and places managers afterward; we instead place both together, so VNF placement is
steered toward layouts a manager can actually serve — subject to manager capacity,
a latency *radius*, and co-location (`notManagerNodes`) constraints. The problem is
NP-hard, so we provide heuristics and compare them against an exact CPLEX solver.

**Central finding.** Joint placement is best understood as a *feasibility-
preservation* mechanism, not a revenue tweak: a management-blind (disjoint)
pipeline frequently strands whole chains because no admissible manager exists for
the layout it chose. Its benefit is therefore **conditional** — large exactly when
management constraints bind, and negligible (even slightly negative) when they do
not. See [Key findings](#key-findings) and [`analysis/FRAMING.md`](analysis/FRAMING.md).

Methods implemented here:

- `bari` — the joint VNF+VNFM heuristic (management-aware DP / Viterbi); the core method
- `rari` — MASMAN, a randomized variant
- `abu` — Abu-Lebdeh's tabu-search baseline, unmodified
- `oabu` — Abu-Lebdeh adapted to our constraints for a fair comparison
- Optimal with CPLEX, implemented under [`simulation/`](simulation/) (a Java/Gradle
  project, formerly the standalone [jsd-mp.simulation](https://github.com/reinnet/jsd-mp.simulation) repo)

In the jsd-mp problem some functions can be managened and there are the functions that need VNFM,
so the following code snippet find these functions in a chain.

```python
itertools.compress(
        placement.nodes, chain.manageable_functions
)
```

Also we have the following configuration for our VNFM constraints as default:

```yaml
ram: 4
cores: 2
capacity: 10
radius: 100
bandwidth: 10
licenseFee: 100
```

## Abu Method

Abu-Lebdeh describe a method based on tabu-search to improve VNFM placement on datacenter that already has VNF placement.
In our work we are considering the VNF placement jointly with VNFM placement so we are going to change it to consider the placement and after that compare it with our method.
In Abu-Lebdeh method there is no way to discard a chain so it can generate infeasible results so we are reserving resources for VNFM to prevent the infeasible situation.

The following variables are available in the `src/jsd_mp/abu` solution to configure it so you need to change them by hand (with `--options`) and report them into results.

```python
n_iter
reserve_percentage
```

## Optimized Abu Method

Abu-Lebdeh uses tabu-search to improve its VNFM placement but at this method it doesn't use consider our problem constraints,
so here we are going to optimize it based on our constraints.

## Key findings

From the re-analysis in [`analysis/`](analysis/), which reports chain
**acceptance rate** (feasibility) with paired significance tests plus a controlled
sensitivity sweep. Full detail in [`analysis/SUMMARY.md`](analysis/SUMMARY.md) and
[`analysis/SWEEP.md`](analysis/SWEEP.md).

- **Joint placement preserves feasibility.** It accepts ~100% of chains across
  regimes, whereas disjoint placement is *bimodal* — a run either nearly succeeds
  or collapses (often to ~30–50% acceptance) because the post-hoc manager step is
  infeasible. Mean-revenue plots hide this; acceptance rate exposes it.
- **The advantage is conditional on management binding:**

  | Regime | Joint accept | Disjoint accept | Reading |
  |---|---|---|---|
  | USnet, default (slack) management | ~100% | ~100% | joint adds nothing; revenue −0.2…−0.9% (p<0.01) |
  | FatTree, default VNFM | ~100% | ~20–87% (bimodal) | joint preserves feasibility |
  | USnet + 4-hop radius | ~100% | ~35–94% | tightening one constraint flips the regime |

- **The constraint is the cause.** Toggling the `notManagerNodes` co-location
  constraint on/off makes the joint advantage appear (+12–19 pp acceptance) and
  disappear (0 pp), and the gap decays as load saturates raw compute. On the
  tested topology, manager capacity is *not* a binding lever.

## Results

Running a solver writes a `report.csv` that the Jupyter notebooks under
[`results/`](results/) load. The corrected, statistically-honest re-analysis and
the sensitivity study live under [`analysis/`](analysis/) and are regenerable with
`uv run --group notebook python analysis/<script>.py`.

## Paper

The manuscript lives under [`paper/`](paper/), written in LaTeX using the
**MDPI _Future Internet_** class (vendored in `paper/Definitions/`). Build the
PDF with `make -C paper` (or `latexmk -pdf -bibtex paper/main.tex`); CI also
typesets it on every change and uploads the PDF as an artifact. See
[`paper/README.md`](paper/README.md) for details.

## [Topologies](https://github.com/reinnet/topology)

There are two topology that are considering here, fattree and usnet. There is another project that generate networks with these two topology.
The generated configuration that must be copied and used with this project as follow:

```sh
topology fattree -k 4
cp topology.yaml ../jsd-mp/config/topology.yml
```

Please note that you must also consider to store these configuration for future re-runs.

## [Chains](https://github.com/reinnet/chainer)

We are going to place SFCs on our network and there is project that generate chains.
The generated chains chains can be copied and used with this project as follow:

```sh
chainer -n 100
cp chains.yaml ../jsd-mp/config/chains.yml
```

## How to Run

This project is managed with [uv](https://docs.astral.sh/uv/). Install the
dependencies (and the `jsd-mp` package itself) with:

```sh
uv sync
```

Then run a solver via the `jsd-mp` console entry point:

```sh
uv run jsd-mp -ss rari -c config/ -r 10
```

Run the test suite and type checker with:

```sh
uv run pytest
uv run mypy
```

The Jupyter notebooks and the `analysis/` scripts need the extra `notebook`
dependency group:

```sh
uv sync --group notebook
uv run --group notebook python -m ipykernel install --user --name=jsd-mp-krnl
```

In your notebook, Kernel -> Change Kernel. Your kernel should now be an option.
