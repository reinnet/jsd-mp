# Sensitivity sweep — when does joint placement matter?

Heuristic reproduction in this repo: **joint** = `Bari` (management-aware cost); **disjoint** = management-blind VNF placement + the same post-hoc manager step. Run on the 15-node `config_example` topology, 8 paired runs/point (usnet is ~1485s/solve, so a sweep there is infeasible — see the script header).

## 1. Toggle the management constraint (controlled A/B)

Same network, same chains; the only change is whether the per-node `notManagerNodes` management constraint is present. **The joint advantage exists if and only if the constraint binds** — with it removed, disjoint matches joint exactly. Joint acceptance is unchanged either way (it is immune, having placed VNFs management-aware). The advantage also decays as load saturates raw VNF resources, at which point management is no longer the bottleneck.

|   load |   joint% |   disj% (ON) |   gap (ON) |   disj% (OFF) |   gap (OFF) |
|-------:|---------:|-------------:|-----------:|--------------:|------------:|
|      2 |    100.0 |         87.5 |       12.5 |         100.0 |         0.0 |
|      3 |    100.0 |         83.3 |       16.7 |         100.0 |         0.0 |
|      4 |    100.0 |         81.2 |       18.8 |         100.0 |         0.0 |
|      5 |    100.0 |         82.5 |       17.5 |         100.0 |         0.0 |
|      6 |     93.8 |         77.1 |       16.7 |          93.8 |         0.0 |
|      7 |     87.5 |         75.0 |       12.5 |          87.5 |         0.0 |
|      8 |     78.1 |         73.4 |        4.7 |          78.1 |         0.0 |
|      9 |     70.8 |         69.4 |        1.4 |          70.8 |         0.0 |
|     10 |     63.8 |         63.8 |        0.0 |          63.8 |         0.0 |
|     12 |     54.2 |         54.2 |        0.0 |          54.2 |         0.0 |

## 2. Manager capacity — a non-binding lever (negative control)

Varying manager capacity over two orders of magnitude barely moves the gap: on this topology capacity does not bind, so it is not what drives the joint advantage. (Radius is likewise not a clean lever here — the network diameter is small, so radius=1 starves every manager while radius>=2 is effectively unconstrained.)

|   capacity |   joint% |   disj% |   gap(pp) |
|-----------:|---------:|--------:|----------:|
|          1 |     93.8 |    77.1 |      16.7 |
|          2 |     93.8 |    77.1 |      16.7 |
|          3 |     93.8 |    77.1 |      16.7 |
|          5 |     93.8 |    77.1 |      16.7 |
|         10 |     93.8 |    77.1 |      16.7 |
|         20 |     93.8 |    77.1 |      16.7 |
|        100 |     93.8 |    77.1 |      16.7 |

## Takeaway
The joint formulation pays off **only when a management constraint actually binds** (here `notManagerNodes`; on the full topologies, manager radius — see `SUMMARY.md`). When management is slack, or when the network is so loaded that raw VNF resources are the binding constraint, joint and disjoint converge. This is the controllable, mechanistic version of the conditional result found in the corrected joint-vs-disjoint analysis.
