#import "lib.typ": todo

== Joint vs. Disjoint <sec:joint-vs-disjoint>

We compare the _joint_ solution (placing VNFs and their VNFM together) against
the _disjoint_ baseline (placing VNFs first and the VNFM afterward), both solved
to optimality with CPLEX. The key effect is one of _feasibility_: a
management-blind disjoint placement can strand whole chains because no admissible
VNFM exists for the chosen VNF layout, so the joint solution accepts more chains
and earns more revenue. Crucially, this benefit is _conditional_ — it appears
only when the management constraints actually bind, as the two topologies below
make clear. We vary the number of chains; chains are generated randomly with the
configuration in @tbl:chain-config.

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

=== FatTree

Here we use a FatTree topology with $k = 6$. Each result is the average of 15
CPLEX runs under a time limit and optimality gap. The disjoint baseline
frequently fails to find a manageable layout, so the joint solution accepts
substantially more chains — and hence more revenue (@tbl:fattree,
@fig:fattree). The gap is largest at low-to-moderate load, where management is
the binding constraint.

#figure(
  caption: [Revenue of joint vs. disjoint on FatTree ($k = 6$)],
  table(
    columns: 3, align: (center, right, right), inset: 6pt,
    table.header([chains], [joint], [disjoint]),
    [10], [4453], [1913], [15], [6587], [1000], [20], [8887], [1593],
    [25], [11133], [3267], [30], [13327], [7907], [35], [15467], [13073],
    [40], [17973], [14687], [45], [20147], [17553], [50], [22440], [15633],
    [55], [24447], [14613], [60], [26940], [14713], [65], [29313], [18887],
    [70], [31487], [16313], [75], [33713], [17340], [80], [36253], [19553],
    [85], [37847], [18540], [90], [40500], [23360],
  ),
) <tbl:fattree>

#figure(
  image("plots/joint-vs-disjoint-fattree.png", height: 320pt),
  caption: [Revenue of joint vs. disjoint on FatTree ($k = 6$)],
) <fig:fattree>

=== USNet

Here we use a USNet topology with 3–4 nodes attached to each of its points. With
the _default_ (slack) management settings the joint and disjoint solutions
perform essentially identically (@tbl:usnet-slack, @fig:usnet-slack): the
topology can manage every chain, so the management constraint does not bind and
joint placement adds nothing. This null result is exactly what the conditional
view predicts.

#figure(
  caption: [Revenue of joint vs. disjoint on USNet (slack management)],
  table(
    columns: 3, align: (center, right, right), inset: 6pt,
    table.header([chains], [joint], [disjoint]),
    [50], [23000], [23010], [75], [34180], [34260], [100], [45430], [45560],
    [125], [57180], [57380], [150], [68750], [69360],
  ),
) <tbl:usnet-slack>

#figure(
  image("plots/joint-vs-disjoint-usnet-1.png", height: 320pt),
  caption: [Revenue of joint vs. disjoint on USNet (slack management)],
) <fig:usnet-slack>

When we add a management constraint — the distance between a manager and its
chain's nodes must be at most 4 hops — the constraint binds and the joint
advantage reappears (@tbl:usnet-tight, @fig:usnet-tight). The same topology thus
moves from "no difference" to a clear joint advantage by tightening a single
management parameter, which is the central message of this comparison.

#figure(
  caption: [Revenue of joint vs. disjoint on USNet (4-hop management radius)],
  table(
    columns: 3, align: (center, right, right), inset: 6pt,
    table.header([chains], [joint], [disjoint]),
    [10], [4473], [1420], [15], [6927], [2733], [20], [8940], [3533],
    [25], [11133], [4833], [30], [13313], [9020], [35], [15487], [14693],
    [40], [17913], [15433], [45], [19813], [17587], [50], [22213], [21020],
    [55], [24113], [21867], [60], [26640], [24547], [65], [28833], [25760],
    [70], [31360], [29420], [75], [33140], [29660], [80], [35687], [33320],
    [85], [37600], [34987], [90], [39840], [37473],
  ),
) <tbl:usnet-tight>

#figure(
  image("plots/joint-vs-disjoint-usnet-2.png", height: 320pt),
  caption: [Revenue of joint vs. disjoint on USNet (4-hop management radius)],
) <fig:usnet-tight>

#todo[A complementary re-analysis reports chain _acceptance rate_ (feasibility)
rather than mean revenue, with paired significance tests, and shows the disjoint
outcomes are bimodal (a run either nearly succeeds or collapses). A controlled
experiment that toggles the co-location constraint on and off confirms the joint
advantage is caused by management binding and decays as load saturates raw
compute. See the project's `analysis/` directory.]
