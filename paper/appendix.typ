For reference, we tabulate the mean revenue underlying the acceptance-rate
results of @sec:acceptance. Revenue tracks acceptance but smooths over the
bimodal collapse of the disjoint baseline, which is why we report acceptance as
the primary metric. Each value is the average of 15 CPLEX runs under a time and
optimality-gap limit.

#figure(
  caption: [Revenue of joint vs. disjoint on FatTree ($k = 6$, default VNFM)],
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

With the _default_ (slack) management settings the joint and disjoint solutions
earn essentially identical revenue on USNet (@tbl:usnet-slack, @fig:usnet-slack):
the topology can manage every chain, so the management constraint does not bind.

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

When the manager radius is tightened to 4 hops the constraint binds and the joint
advantage reappears in revenue as well (@tbl:usnet-tight, @fig:usnet-tight).

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
