// Joint Service Chain Deployment and Manager Placement in NFV
// Migrated from LaTeX (elsarticle) to Typst.

#set document(
  title: "Joint Service Chain Deployment and Manager Placement in NFV",
  author: ("Parham Alvani", "Bahador Bakhshi"),
)
#set page(paper: "a4", numbering: "1", margin: (x: 2.4cm, y: 2.6cm))
#set text(size: 11pt, lang: "en")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.2em, below: 0.7em)
#set math.equation(numbering: "(1)")

// ---- Title block ----
#align(center)[
  #text(17pt, weight: "bold")[Joint Service Chain Deployment and Manager
  Placement in NFV]
  #v(0.6em)
  #text(11pt)[Parham Alvani#super[a] #h(1.5em) Bahador Bakhshi#super[a,\u{2217}]]
  #v(0.3em)
  #text(9pt, style: "italic")[#super[a]Amirkabir University of Technology,
  Tehran, Iran]
  #v(0.2em)
  #text(9pt)[`parham.alvani@aut.ac.ir`, `bbakhshi@aut.ac.ir` #h(0.5em)
  (#super[\u{2217}]corresponding author)]
]
#v(1.2em)

// ---- Abstract ----
#block(inset: (left: 1.2em, right: 1.2em))[
  #align(center)[*Abstract*]
  #v(0.4em)
  Network operators deploying service function chains (SFCs) with Network
  Function Virtualization (NFV) must also provide each chain with a VNF Manager
  (VNFM) under capacity, latency-radius, and co-location constraints. Most prior
  work optimizes VNF placement first and assigns managers afterward. We show
  that this _disjoint_ approach is not merely suboptimal but frequently
  _infeasible_: management-blind VNF layouts strand whole chains because no
  admissible manager exists for the chosen placement. We formulate the joint SFC
  deployment and VNFM placement problem (JSD-MP) as an Integer Linear Program,
  show it is NP-hard, and propose MASMAN, a polynomial-time heuristic that makes
  VNF placement management-aware (a Viterbi-style dynamic program) and then
  consolidates managers with Tabu search. Against an exact CPLEX solver the
  heuristic produces near-optimal results far faster. Finally, we characterize
  _when_ joint placement matters: its benefit is a feasibility effect that
  appears precisely when management constraints bind, and is negligible under
  slack management or when raw compute saturates the network.
]
#v(1em)

// = Introduction =
= Introduction <sec:introduction>
#include "introduction.typ"

= Related Work <sec:related-works>
#include "related-works.typ"

= System Model and Problem Statement <sec:system-model>
#include "system.typ"

= Problem Formulation <sec:formulation>
#include "formulation.typ"

= Proposed Solution <sec:solution>
#include "solution.typ"

= Evaluation and Numerical Results <sec:results>
#include "results.typ"

= Conclusion and Future Work <sec:conclusion>
We considered, for the first time, the joint deployment of service function
chains and the placement of their VNF Managers (JSD-MP). We formulated the
problem as an ILP, showed its NP-hardness, and proposed MASMAN, a
polynomial-time heuristic that is management-aware during VNF placement and
consolidates managers with Tabu search. Our evaluation shows the heuristic is
near-optimal, and that the value of joint placement is a feasibility effect that
is large exactly when management constraints bind. Future work includes an
online variant in which requests arrive over time, reliability-aware manager
placement with backup managers, and tighter approximation guarantees for the
manager-placement subproblem (which is a capacitated facility-location problem
with a coverage radius).

// ---- Appendix ----
#counter(heading).update(0)
#set heading(numbering: "A.1")

= Revenue Tables <sec:revenue-appendix>
#include "appendix.typ"

#bibliography("references.bib", style: "ieee")
