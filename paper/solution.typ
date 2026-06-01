We have formulated the JSD-MP problem as an ILP, and its optimal solution is
NP-hard, so it takes a long time to solve, whereas data centers need a faster way
to place chains. In this section we present a near-optimal, polynomial-time
solution for quickly deciding on SFC requests with management resources; it can
be used at large data centers with many nodes and requests.

== Maximizing the Accepted SFC Requests with Management Constraints (MASMAN)

As mentioned, the JSD-MP problem places chains, and each placement has two parts:
VNF placement (placing the chain's VNFs) and VNFM placement (placing the chain's
VNFM), which we formulate together. For each chain we divide the placement into
two phases, solved by different algorithms; to account for managers, we reserve
at least one VNFM's resources on each physical node before the placement phase.

The first phase is VNF placement, which we solve with the Bari algorithm
@Bari2015. This is an efficient dynamic-programming algorithm based on the
Viterbi algorithm for SFC placement; it does not consider management resources,
so we tweak it. For each chain it solves a dynamic program that finds the
minimum-cost path in a multi-stage graph, deciding each node's location together
with its predecessor to minimize cost (a minimum-cost path consists of
minimum-cost sub-paths). Each stage in the graph is one network function that
needs placement, and the graph nodes are the candidates; edges between stages
represent the links.

Finally, we use Tabu search to improve VNFM placement — by _merging_ VNFMs to
reduce the license cost. In Tabu search we randomly select two physical nodes to
merge, update the tabu table so they are not re-checked, and, if the merge is
feasible, update the minimum cost and continue.

#figure(
  caption: [MASMAN — VNF placement phase],
  kind: "algorithm", supplement: [Algorithm],
  block(width: 100%, stroke: 0.6pt, inset: 8pt, align(left, raw(
"function masman_placement(chains, topology):
  for chain in chains:
    for i in 0 .. len(chain):        # len(chain) = number of VNFs
      if i == 0:                     # ingress: no predecessor
        for n in topology.nodes:
          if hasEnoughResource(n):
            cost[(0, n)] = cost(n)
      else:
        for n in topology.nodes:
          min = +inf
          for k in topology.nodes:   # choose best predecessor k
            if hasEnoughResourceOnState(i-1, k, n):
              c = costOnState(i-1, k, n)
              if c <= min: min = c
          cost[(i, n)] = min",
    lang: none))),
) <alg:masman>

#figure(
  caption: [MASMAN — manager placement and consolidation (Tabu search)],
  kind: "algorithm", supplement: [Algorithm],
  block(width: 100%, stroke: 0.6pt, inset: 8pt, align(left, raw(
"function masman_manager_placement(chains, topology):
  for chain in chains:
    for n in topology.nodes:
      if canBeManager(chain, n):     # reachable + enough resources
        chain.manager = n
        reserveManagementResources(n)
  for i in 0 .. maxIterations:
    n1 = randomNode(topology)
    n2 = randomNode(topology)
    updateTabuTable(n1, n2)
    if isMergePossible(n1, n2):
      for chain in chains:
        if chain.manager == n1:
          chain.manager = n2
          freeManagementResources(n1)
          reserveManagementResources(n2)
          updateMinCost()",
    lang: none))),
) <alg:masman-mgr>

#figure(
  image("images/bari.png", width: 100%),
  caption: [Transitions of the Bari @Bari2015 algorithm to create the
  multi-stage graph],
) <fig:bari>

Another way to place the chains is to use the Bari @Bari2015 algorithm but add a
new stage at the end for VNFM placement; we use this as a second algorithm in the
next section to compare with @alg:masman.
