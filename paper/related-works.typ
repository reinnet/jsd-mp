In this section, we review the work that has been done on service chain
deployment and resource assignment in NFV, mainly focusing on work that
considers the management requirements of chains.

== Resource Allocation in NFV

The service chain deployment problem, especially for virtual mobile core network
functions, has recently received substantial attention in the literature
@GilHerrera2016 @Laghrissi2019 @Bhamare2016. This problem is composed of two main
steps: allocating computing and memory resources for the virtual machines that
run the chains' virtual network functions, and assigning network resources to
the chains' virtual links @Laghrissi2019. Various versions of this problem, with
different objective functions and a wide range of constraints, have been
investigated @Laghrissi2019. The placement problem has many variations; we
concentrate on VNF placement with VNF chain placement. There are many different
objectives, such as minimizing the deployment cost, increasing profit, and
minimizing resource usage @Laghrissi2019 @Bhamare2016, and many variations such
as online, dynamic, and scheduled placement #cite(label("1608.00095")).

From the objective-function standpoint, deployment of service chains can be
optimized for different goals. One common category uses SFC deployment to
maximize the business profit of the infrastructure provider @Eramo2016
@Eramo2017 @TahmasbiNejad2018 @Huang2019: the objective is to maximize the
revenue gained by accepting SFC requests while minimizing the cost of physical
servers and links @Bouet2015 @Pham2020 @Huang2019 and the cost of VNF images and
licenses @Bouet2015. Energy-awareness is another objective @Eramo2017 @Eramo20172
@Farkiani2019, aiming to minimize the power footprint by turning off unused
servers and links via green-networking techniques such as traffic consolidation
@Zheng2020. While QoS requirements are typically constraints, some work optimizes
QoS metrics such as delay and congestion as the objective @Huang2019 @Yu2017
@Chen2017. Finally, there is plenty of work that optimizes multiple objectives
simultaneously, e.g., load balancing and reconfiguration overheads @Qu2020.

The constraints of the SFC deployment problem are a second differentiating
factor. The required computing resources for virtual functions, the bandwidth
for virtual links, and the limited capacity of the infrastructure are the most
basic constraints @TahmasbiNejad2018 @Eramo2016 @Huang2019. Beyond these, more
realistic assumptions and QoS requirements have been considered. Since VNFs are
software images, their processing capacity is typically limited by software and
license issues beside the underlying hardware capacity; these limitations were
considered in @Luo2020. Authors also took into account different QoS
requirements, such as end-to-end delay @Yu2017 @Yaghoubpour2019 and reliability
@Yu2017 @Torkamandi2019 @Khezri2019. Finally, the management requirements of
service chains are another important category of constraints that has received
little attention @AbuLebdeh2017 @AbuLebdeh20172 @Chiang2019; we elaborate on it
below.

Several solution methods have been used. Mainly, the problem is formulated as a
Mixed Integer Linear Program (MILP); since it is NP-hard @Eramo2016 @Ma2017,
various approaches tackle its complexity. Optimization-theory techniques such as
decomposition and Lagrangian relaxation were proposed @Liu2017 @Farkiani2019
#cite(label("1709.04772")). Another category is meta-heuristic algorithms, e.g.,
Tabu search and genetic algorithms @AbuLebdeh2017. Problem-specific heuristics
are also common @Ghaznavi2017 @Bari2015 @Eramo2016. Available information about
demands is another important issue: in off-line approaches whole demands are
known at the beginning, while in on-line solutions demands arrive one-by-one
@Alhussein2020.

In comparison to previous works, here we consider profit maximization as the
objective, formulate the problem as a MILP model, and use Tabu search to solve
it. However, in addition to computation and bandwidth requirements, we consider
the management requirement, which has not been investigated in the literature
except for the very few studies discussed next.

== Management Resources in NFV

To the best of our knowledge, @AbuLebdeh2017, its follow-up @AbuLebdeh20172, and
@Chiang2019 are the only works that consider VNFM and other management resources
in SFC deployment.

In @AbuLebdeh2017, the authors study VNFM placement in a distributed NFV
infrastructure under the assumption that chains have already been deployed, so
the locations of VNFs are known. The objective is to minimize operational cost
(life-cycle management, compute resources, migration, and reassignment), subject
to a delay constraint on management links. They use Tabu search, starting from a
feasible placement and improving it via reassignment, relocation, bulk
reassignment, and deactivation. While this is the first work on management
resource assignment in NFV, it does not _jointly_ deploy SFCs and VNFMs.

In @AbuLebdeh20172, the authors extend their previous work to the VNFO placement
problem, with the same system model, aiming to place VNFO and VNFM jointly to
minimize operational cost. They propose a two-step algorithm that first places
VNFOs and then VNFMs using Tabu search. That paper also assumes the SFCs have
already been deployed.

In @Chiang2019, the authors give VNFMs autonomy so they select their managed
VNFs dynamically, using game theory for a distributed solution to the VNFM
placement problem of @AbuLebdeh2017. Again, the VNF locations are given and only
VNFM placement is solved.

To conclude, prior work on management resources in NFV is based on the system
model of @AbuLebdeh2017, in which service chains are deployed beforehand. Here,
we instead _jointly_ optimize SFC deployment and VNFM placement. Moreover, we
consider a license cost for VNFM instances, and in our model each physical node
has its own list of nodes that may run its VNFM, which provides great flexibility
for implementing management policies.
