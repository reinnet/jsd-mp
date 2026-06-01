"""
Sensitivity sweep: when does JOINT VNF+VNFM placement beat DISJOINT?

The thesis' joint-vs-disjoint comparison ran in the CPLEX solver under
`simulation/` (which needs a CPLEX licence), so it is not reproduced here
directly. Instead we reproduce the *same distinction* inside this repo's
heuristic:

  - JOINT    = the existing `Bari` solver. Its `get_cost` is management-aware
               (it penalises nodes that cannot host a VNFM and accounts for
               not-manager-node conflicts), so VNF placement is steered toward
               management-feasible layouts.
  - DISJOINT = `Bari` with a management-BLIND `get_cost` (path length only).
               VNFs are placed ignoring management, then the *same*
               `place_manager` step tries to add managers afterward.

Feasibility of a chain is identical in both (same `is_resource_available`);
only the cost ordering during VNF placement differs. So any acceptance-rate gap
is attributable purely to "did we consider management while placing VNFs".

Topology: the repo's 15-node `config_example`. We use it (not usnet) because
Bari is O(functions x nodes^2) per chain with a BFS in the inner loop -- ~1485s
for 20 chains on the 120-node usnet, which makes a sweep infeasible. On the
15-node net a solve is ~0.2s. The trade-off is that the *binding* management
constraint here is the per-node `notManagerNodes` restriction (radius has too
small a diameter to be a clean lever, and manager capacity turns out not to
bind -- see the capacity experiment). The qualitative result -- joint helps iff
management binds, and the benefit decays under load -- matches the corrected
joint-vs-disjoint analysis on the full topologies (see SUMMARY.md).

Experiments
  1. CONSTRAINT TOGGLE across offered load: run with the management constraint
     present vs. stripped. The controlled A/B isolates the effect.
  2. CAPACITY sweep: vary manager capacity to show it is *not* a binding lever
     on this topology (a deliberately negative control).

Outputs (next to this file): sweep_constraint.{csv,png},
sweep_capacity.{csv,png}, SWEEP.md
"""
import os
import copy
import random
import argparse

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
# jsd_mp is installed as a package (uv sync); run via `uv run python ...`.
from jsd_mp.config import load, Config
from jsd_mp.domain import Chain, Link, VNFM
from jsd_mp.bari import Bari

MANAGEABLE = ["vFW", "vNAT", "vIDS", "vDPI"]
CHAIN_FEE = 100
CHAIN_BW = 250


class Disjoint(Bari):
    """Management-blind VNF placement (cost = path length only), then the
    unchanged Bari manager-placement step. This is the 'disjoint' baseline."""

    def get_cost(self, topology, previous, current, fn, link):
        if previous == "" or link is None:
            return 0
        path = topology.path(previous, current, 0)
        return int(float("inf")) if path is None else len(path)


def make_chains(n, types, rng):
    """n random chains, chainer style: length in [4,6], ingress + manageable
    middles + egress, fee=100, link bandwidth=250."""
    chains = []
    for i in range(n):
        length = rng.randint(4, 6)
        chain = Chain(name=f"ch-{i}", fee=CHAIN_FEE)
        chain.add_function(types["ingress"])
        for _ in range(length - 2):
            chain.add_function(types[rng.choice(MANAGEABLE)])
        chain.add_function(types["egress"])
        for s in range(len(chain.functions) - 1):
            chain.add_link(s, s + 1, Link(CHAIN_BW))
        chains.append(chain)
    return chains


def build_cfg(base, chains, *, radius=None, capacity=None, strip_management=False):
    """Fresh Config with given chains, optional vnfm overrides, and an option to
    remove the notManagerNodes management constraint (negative control)."""
    v = base.vnfm
    vnfm = VNFM(
        cores=v.cores, memory=v.memory,
        capacity=capacity if capacity is not None else v.capacity,
        radius=radius if radius is not None else v.radius,
        bandwidth=v.bandwidth, license_cost=v.license_cost,
    )
    topo = copy.deepcopy(base.topology)
    if strip_management:
        for node in topo.nodes.values():
            object.__setattr__(node, "not_manager_nodes", [])  # Node is frozen
    return Config(base.types, chains, vnfm, topo)


def run_once(solver_cls, cfg, seed):
    random.seed(seed)
    solver = solver_cls(cfg)
    solver.solve()
    return len(solver.solution) / len(cfg.chains) * 100


def paired(base, n_chains, runs, *, strip_management, **vnfm_kw):
    """`runs` paired (joint, disjoint) trials on the SAME chain set."""
    j, d = [], []
    for r in range(runs):
        rng = random.Random(1000 + r)
        chains = make_chains(n_chains, base.types, rng)
        cfg = build_cfg(base, chains, strip_management=strip_management, **vnfm_kw)
        j.append(run_once(Bari, cfg, seed=r))
        d.append(run_once(Disjoint, cfg, seed=r))
    return np.array(j), np.array(d)


def exp_constraint(base, loads, runs):
    rows = []
    for n in loads:
        for strip, cond in ((False, "with"), (True, "without")):
            j, d = paired(base, n, runs, strip_management=strip)
            rows.append(dict(
                load=n, constraint=cond,
                joint=j.mean(), disjoint=d.mean(),
                disjoint_std=d.std(), gap=j.mean() - d.mean(),
            ))
            print(f"  n={n:2d} {cond:7s}: joint={j.mean():5.1f}%  "
                  f"disjoint={d.mean():5.1f}%  gap={j.mean()-d.mean():+5.1f}pp")
    return pd.DataFrame(rows)


def exp_capacity(base, caps, n_chains, runs):
    rows = []
    for cap in caps:
        j, d = paired(base, n_chains, runs, strip_management=False, capacity=cap)
        rows.append(dict(
            capacity=cap, joint=j.mean(), disjoint=d.mean(),
            disjoint_std=d.std(), gap=j.mean() - d.mean(),
        ))
        print(f"  cap={cap:3d}: joint={j.mean():5.1f}%  "
              f"disjoint={d.mean():5.1f}%  gap={j.mean()-d.mean():+5.1f}pp")
    return pd.DataFrame(rows)


def plot_constraint(df, path):
    fig, ax = plt.subplots(figsize=(9, 6))
    w = df[df.constraint == "with"].sort_values("load")
    wo = df[df.constraint == "without"].sort_values("load")
    ax.plot(w.load, w.joint, "o-", color="#c0392b", label="joint")
    ax.plot(w.load, w.disjoint, "s--", color="#2980b9",
            label="disjoint (management constraint ON)")
    ax.plot(wo.load, wo.disjoint, "^:", color="#16a085",
            label="disjoint (constraint OFF — negative control)")
    ax.fill_between(w.load, w.disjoint, w.joint, color="#c0392b", alpha=0.10,
                    label="joint advantage")
    ax.set_title("Joint vs disjoint acceptance — management constraint toggled\n"
                 "(config_example, 15 nodes)")
    ax.set_xlabel("offered chains (load)")
    ax.set_ylabel("accepted chains (%)")
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def plot_capacity(df, path):
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.errorbar(df.capacity, df.joint, fmt="o-", color="#c0392b", label="joint")
    ax.errorbar(df.capacity, df.disjoint, yerr=df.disjoint_std, fmt="s--",
                color="#2980b9", capsize=3, label="disjoint")
    ax.set_xscale("log")
    ax.set_title("Acceptance vs manager capacity — a non-binding lever\n"
                 "(config_example, gap ~constant)")
    ax.set_xlabel("manager capacity (log)")
    ax.set_ylabel("accepted chains (%)")
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def write_md(dfc, dfcap, args):
    L = ["# Sensitivity sweep — when does joint placement matter?\n"]
    L.append(
        "Heuristic reproduction in this repo: **joint** = `Bari` "
        "(management-aware cost); **disjoint** = management-blind VNF placement "
        "+ the same post-hoc manager step. Run on the 15-node `config_example` "
        f"topology, {args.runs} paired runs/point (usnet is ~1485s/solve, so a "
        "sweep there is infeasible — see the script header).\n"
    )
    L.append("## 1. Toggle the management constraint (controlled A/B)\n")
    L.append(
        "Same network, same chains; the only change is whether the per-node "
        "`notManagerNodes` management constraint is present. **The joint "
        "advantage exists if and only if the constraint binds** — with it "
        "removed, disjoint matches joint exactly. Joint acceptance is "
        "unchanged either way (it is immune, having placed VNFs "
        "management-aware). The advantage also decays as load saturates raw VNF "
        "resources, at which point management is no longer the bottleneck.\n"
    )
    piv = dfc.pivot(index="load", columns="constraint",
                    values=["joint", "disjoint", "gap"])
    tbl = pd.DataFrame({
        "load": dfc.load.unique().astype(int).astype(str),
        "joint%": piv["joint"]["with"].values,
        "disj% (ON)": piv["disjoint"]["with"].values,
        "gap (ON)": piv["gap"]["with"].values,
        "disj% (OFF)": piv["disjoint"]["without"].values,
        "gap (OFF)": piv["gap"]["without"].values,
    })
    L.append(tbl.to_markdown(index=False, floatfmt=".1f"))
    L.append("\n## 2. Manager capacity — a non-binding lever (negative control)\n")
    L.append(
        "Varying manager capacity over two orders of magnitude barely moves the "
        "gap: on this topology capacity does not bind, so it is not what drives "
        "the joint advantage. (Radius is likewise not a clean lever here — the "
        "network diameter is small, so radius=1 starves every manager while "
        "radius>=2 is effectively unconstrained.)\n"
    )
    t2 = dfcap[["capacity", "joint", "disjoint", "gap"]].copy()
    t2["capacity"] = t2["capacity"].astype(int).astype(str)
    t2.columns = ["capacity", "joint%", "disj%", "gap(pp)"]
    L.append(t2.to_markdown(index=False, floatfmt=".1f"))
    L.append(
        "\n## Takeaway\n"
        "The joint formulation pays off **only when a management constraint "
        "actually binds** (here `notManagerNodes`; on the full topologies, "
        "manager radius — see `SUMMARY.md`). When management is slack, or when "
        "the network is so loaded that raw VNF resources are the binding "
        "constraint, joint and disjoint converge. This is the controllable, "
        "mechanistic version of the conditional result found in the corrected "
        "joint-vs-disjoint analysis.\n"
    )
    open(os.path.join(HERE, "SWEEP.md"), "w").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(HERE, "..", "config_example"))
    ap.add_argument("--runs", type=int, default=8)
    ap.add_argument("--loads", type=int, nargs="+",
                    default=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    ap.add_argument("--caps", type=int, nargs="+", default=[1, 2, 3, 5, 10, 20, 100])
    ap.add_argument("--cap-load", type=int, default=6,
                    help="offered load used for the capacity experiment")
    args = ap.parse_args()

    base = load(args.config)
    print(f"loaded {args.config}: {len(base.topology.nodes)} nodes, "
          f"radius={base.vnfm.radius} capacity={base.vnfm.capacity}\n")

    print(f"== experiment 1: constraint toggle across load ({args.runs} runs) ==")
    dfc = exp_constraint(base, args.loads, args.runs)
    dfc.to_csv(os.path.join(HERE, "sweep_constraint.csv"), index=False)
    plot_constraint(dfc, os.path.join(HERE, "sweep_constraint.png"))

    print(f"\n== experiment 2: capacity sweep (load={args.cap_load}) ==")
    dfcap = exp_capacity(base, args.caps, args.cap_load, args.runs)
    dfcap.to_csv(os.path.join(HERE, "sweep_capacity.csv"), index=False)
    plot_capacity(dfcap, os.path.join(HERE, "sweep_capacity.png"))

    write_md(dfc, dfcap, args)
    print("\nwrote sweep_constraint.*, sweep_capacity.*, SWEEP.md")


if __name__ == "__main__":
    main()
