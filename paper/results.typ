== Joint vs. Disjoint <sec:joint-vs-disjoint>

We compare the _joint_ solution (placing VNFs and their VNFM together) against
the _disjoint_ baseline (placing VNFs first and the VNFM afterward), both solved
to optimality with CPLEX. The key effect is one of _feasibility_: a
management-blind disjoint placement can strand whole chains because no admissible
VNFM exists for the chosen VNF layout, so the joint solution accepts more chains.
Crucially, this benefit is _conditional_ — it appears only when the management
constraints actually bind, as the two topologies below make clear. We therefore
report chain _acceptance rate_ as the primary metric; the corresponding mean
revenue, which only smooths over the mechanism, is tabulated for reference in
@sec:revenue-appendix. We vary the number of chains; chains are generated
randomly with the configuration in @tbl:chain-config.

#figure(
  caption: [Chain configuration],
  table(
    columns: 2, align: (left, left), inset: 6pt,
    [Property], [Value],
    [Length], [$[4, 7)$],
    [Per-instance cost], [\$100],
    [Bandwidth], [250 bps],
  ),
) <tbl:chain-config>

We evaluate two topologies: a FatTree with $k = 6$, and a USNet topology with
3–4 nodes attached to each of its points. Each point is the average of 15 CPLEX
runs under a time limit and a 5% optimality-gap limit.

== Acceptance Rate: the Feasibility Effect <sec:acceptance>

We report chain _acceptance rate_ — the fraction of requested chains that are
admitted — and test each point with a paired Wilcoxon signed-rank test (joint
vs. disjoint on the _same_ chain set, 10–15 runs per point).

Two facts stand out. First, the joint solution accepts $approx 100%$ of chains
in _every_ regime — it is essentially feasibility-immune, because it placed the
VNFs with management in mind. Second, the disjoint baseline is _bimodal_: a run
either nearly succeeds or collapses, because the post-hoc manager step is
infeasible for the layout the VNF stage happened to choose. The per-point
coefficient of variation (`disj_CV%`, up to ~80%) and the worst single run
(`disj_min%`, as low as 0%) expose a spread that the revenue averages hide.

#[
#show figure: set block(breakable: true)
#figure(
  caption: [Chain acceptance rate, joint vs. disjoint. `disj_min%` is the
  worst single disjoint run; `disj_CV%` is the coefficient of variation across
  runs (a bimodality signal). All revenue differences are significant at
  $p < 0.05$ (paired Wilcoxon).],
  table(
    columns: 5, align: (center, right, right, right, right), inset: 5pt,
    table.header[chains][joint%][disj%][disj_min%][disj_CV%],
    table.cell(colspan: 5, align: left)[*FatTree ($k = 6$, default VNFM) —
      management binds*],
    [10], [100.0], [46.0], [0.0], [69.6],
    [15], [100.0], [18.7], [0.0], [62.8],
    [20], [100.0], [20.3], [5.0], [41.6],
    [25], [100.0], [31.2], [8.0], [78.9],
    [30], [100.0], [60.2], [6.7], [55.3],
    [35], [100.0], [85.7], [77.1], [7.0],
    [40], [100.0], [83.2], [62.5], [15.4],
    [45], [100.0], [87.7], [44.4], [19.8],
    [50], [99.9], [70.5], [36.0], [39.3],
    [55], [100.0], [61.5], [23.6], [47.6],
    [60], [99.9], [56.4], [28.3], [46.8],
    [65], [99.9], [65.6], [29.2], [47.6],
    [70], [100.0], [53.2], [25.7], [53.9],
    [75], [99.8], [53.6], [32.0], [51.7],
    [80], [100.0], [56.0], [33.8], [46.2],
    [85], [100.0], [50.6], [31.8], [48.5],
    [90], [100.0], [59.6], [27.8], [46.6],
    table.cell(colspan: 5, align: left)[*USNet (4-hop manager radius) —
      management binds*],
    [10], [100.0], [34.7], [0.0], [80.8],
    [15], [100.0], [41.8], [26.7], [24.4],
    [20], [100.0], [42.3], [25.0], [22.8],
    [25], [100.0], [45.1], [24.0], [45.4],
    [30], [99.8], [68.7], [40.0], [33.0],
    [35], [100.0], [94.1], [85.7], [4.5],
    [40], [99.8], [85.3], [72.5], [9.8],
    [45], [99.9], [87.1], [57.8], [12.6],
    [50], [99.9], [93.6], [88.0], [2.7],
    [55], [99.6], [89.8], [58.2], [10.2],
    [60], [99.6], [90.3], [81.7], [4.3],
    [65], [99.3], [88.2], [47.7], [12.7],
    [70], [99.8], [92.1], [87.1], [3.6],
    [75], [99.4], [87.7], [46.7], [12.8],
    [80], [99.4], [91.4], [86.2], [3.1],
    [85], [99.2], [90.6], [60.0], [9.3],
    [90], [99.3], [91.7], [88.9], [2.1],
    table.cell(colspan: 5, align: left)[*USNet (default VNFM) —
      management slack*],
    [50], [100.0], [100.0], [100.0], [0.0],
    [75], [100.0], [100.0], [100.0], [0.0],
    [100], [100.0], [100.0], [100.0], [0.0],
    [125], [100.0], [100.0], [100.0], [0.0],
    [150], [99.9], [100.0], [100.0], [0.0],
  ),
) <tbl:acceptance>
]

#figure(
  grid(
    columns: 3, gutter: 4pt,
    image("plots/acceptance-fattree.png"),
    image("plots/acceptance-usnet-radius.png"),
    image("plots/acceptance-usnet-slack.png"),
  ),
  caption: [Acceptance rate vs. number of chains. Left: FatTree (default VNFM).
  Middle: USNet (4-hop radius). Right: USNet (slack management). Joint stays at
  $approx 100%$; disjoint collapses precisely where management binds and matches
  joint where it does not.],
) <fig:acceptance>

On FatTree with the default VNFM, and on USNet once a 4-hop manager radius is
imposed, the management constraint binds and joint placement dominates. In the
slack regime (USNet, default VNFM) disjoint reaches 100% acceptance with zero
variance, so the joint formulation adds nothing — and, accounting for management
that never binds, it diverts VNF placement enough to be _marginally worse_ on
revenue (−0.2% to −0.9%, paired Wilcoxon $p < 0.01$; see @sec:revenue-appendix).
We keep this null result in deliberately: it delimits the regime in which joint
placement is worth the extra coupling. Note that the same USNet topology moves
from "no difference" to a clear joint advantage by tightening a single management
parameter — the manager radius — which is the central message of this comparison.

== When Joint Placement Matters: a Controlled Sweep <sec:sweep>

The comparisons above show _that_ the advantage is conditional; a controlled
sweep on the 15-node example topology isolates _why_. Here the joint method is
the management-aware heuristic (Bari) and the disjoint method is the same
pipeline with management-blind VNF placement, with 8 paired runs per point.

*The management constraint is the cause.* Holding the network and chains fixed,
we toggle the per-node co-location (`notManagerNodes`) management constraint on
and off (@tbl:sweep-constraint, @fig:sweep-constraint). With it _on_, the joint
method leads disjoint by 12–19 percentage points of acceptance at low load; with
it _off_, disjoint matches joint exactly (gap 0) at every load. Joint acceptance
is identical in both columns — it is immune by construction. The gap also decays
to 0 as load rises and raw VNF resources, not management, become the bottleneck.

#figure(
  caption: [Toggling the management constraint (controlled A/B). The joint
  advantage exists if and only if the constraint binds, and decays under load.],
  table(
    columns: 6, align: (right, right, right, right, right, right), inset: 5pt,
    table.header(
      [load], [joint%], [disj% (on)], [gap (on)], [disj% (off)], [gap (off)]),
    [2], [100.0], [87.5], [12.5], [100.0], [0.0],
    [3], [100.0], [83.3], [16.7], [100.0], [0.0],
    [4], [100.0], [81.2], [18.8], [100.0], [0.0],
    [5], [100.0], [82.5], [17.5], [100.0], [0.0],
    [6], [93.8], [77.1], [16.7], [93.8], [0.0],
    [7], [87.5], [75.0], [12.5], [87.5], [0.0],
    [8], [78.1], [73.4], [4.7], [78.1], [0.0],
    [9], [70.8], [69.4], [1.4], [70.8], [0.0],
    [10], [63.8], [62.5], [1.2], [63.8], [0.0],
    [12], [54.2], [54.2], [0.0], [54.2], [0.0],
  ),
) <tbl:sweep-constraint>

#figure(
  image("plots/sweep-constraint.png", height: 300pt),
  caption: [Acceptance vs. load with the management constraint on vs. off. The
  joint–disjoint gap appears only when the constraint is present.],
) <fig:sweep-constraint>

*Manager capacity is not the lever (negative control).* Sweeping manager
capacity over two orders of magnitude barely moves the gap (@tbl:sweep-capacity):
on this topology capacity does not bind, so it is not what drives the joint
advantage. The binding lever here is the co-location constraint; on the full
topologies it is the manager radius (@sec:acceptance).

#figure(
  caption: [Manager capacity as a non-binding lever (negative control). The gap
  is essentially constant from capacity 1 to 100.],
  table(
    columns: 4, align: (right, right, right, right), inset: 5pt,
    table.header([capacity], [joint%], [disj%], [gap (pp)]),
    [1], [93.8], [77.1], [16.7],
    [2], [93.8], [81.2], [12.5],
    [3], [93.8], [77.1], [16.7],
    [5], [93.8], [81.2], [12.5],
    [10], [93.8], [77.1], [16.7],
    [20], [93.8], [77.1], [16.7],
    [100], [93.8], [79.2], [14.6],
  ),
) <tbl:sweep-capacity>

Together these results turn a soft comparison into a characterization: joint
placement does not make good layouts better; it makes infeasible layouts
feasible — exactly when a management constraint binds, and not otherwise.
