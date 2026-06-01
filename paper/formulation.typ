In this section, the JSD-MP problem is formulated as a MILP model. First the
variables of the model are introduced, then the constraints are discussed, and
finally the objective is presented.

The variables are listed in @tbl:variables. $x_r$ is a binary variable for the
acceptance of demand $r in R$. The integer variable $y_(i t)$ is the number of
VNFs of type $t in T$ on server $i$. The binary variable $z_(v i)^t$ indicates
whether an instance of VNF type $t$ serves node $v$ on server $i$. The integer
variable $overline(y)_i$ is the number of VNFMs placed on server $i$, and the
binary variable $overline(z)_(r i)$ represents the VNFM assignment of a chain.
Finally, $pi_(i j)^((u,v))$ and $overline(pi)_(i j)^v$ are binary variables
indicating that virtual link $(u,v)$ is mapped on physical link $(i,j)$ and that
link $(i,j)$ is used to manage VNF $v$, respectively.

#figure(
  caption: [Variables],
  table(
    columns: (auto, 1fr), align: (center + horizon, left), inset: 5pt,
    [$x_r$], [1 if the SFC request $r$ is accepted; otherwise 0],
    [$y_(i t)$], [number of VNF instances of type $t in T$ set up on server $i in V^p$],
    [$z_(v i)^t$], [1 if VNF node $v in union.big_(r=1)^R V_r^s$ is served by a VNF
      instance of type $t in T$ on server $i in V^p$],
    [$overline(y)_i$], [number of VNFMs set up on server $i in V^p$
      (each with its capacity and license fee)],
    [$overline(z)_(r i)$], [1 if SFC $r$ is assigned to a VNFM on server $i in V^p$],
    [$pi_(i j)^((u,v))$], [1 if virtual link $(u,v)$ is routed on physical link $(i,j)$],
    [$overline(pi)_(i j)^v$], [1 if the management of VNF node $v$ is routed on
      physical link $(i,j)$],
  ),
) <tbl:variables>

Each node has limited installed memory; each VNF instance (by its type) and each
VNFM uses a specific amount. @eq:node-memory limits the used memory of each node
by its installed memory.

$ sum_(t in T) y_(i t) m_t^s + overline(y)_i m^m <= m_i^p quad forall i in V^p $ <eq:node-memory>

Each node has limited processing power in CPU cores. @eq:node-cpu limits the used
processing power of each node by its installed CPUs.

$ sum_(t in T) y_(i t) c_t^s + overline(y)_i c^m <= c_i^p quad forall i in V^p $ <eq:node-cpu>

If a chain's node is served on a physical node, a VNF instance must be set up on
it. @eq:service-place controls this relationship.

$ sum_(v in union.big_(r=1)^R V_r^s) z_(v i)^t <= y_(i t) quad forall i in V^p, forall t in T $ <eq:service-place>

@eq:service and @eq:manager accept a chain only if all of its nodes are placed on
physical servers and it has an assigned VNFM.

$ x_r = sum_(t in T) sum_(i in V^p) z_(v i)^t quad forall v in V_r^s, forall r in R $ <eq:service>

$ x_r = sum_(i in V^p) overline(z)_(r i) quad forall r in R $ <eq:manager>

@eq:manager-capacity limits manager capacity.

$ sum_(r in R) overline(z)_(r i) dot |V_r^s| <= kappa dot overline(y)_i quad forall i in V^p $ <eq:manager-capacity>

@eq:type assures each chain's node is served by a VNF of its type.

$ z_(v i)^t <= tau(v, t) quad forall i in V^p, forall t in T, forall v in union.big_(r in R) V_r^s $ <eq:type>

Each physical server has a set of servers that cannot manage it.
@eq:mgmt-relationship represents this.

$ & 1 - z_(v i)^t + overline(z)_(r j) = 0, \
  & forall i, j in V^p "with" eta_(i,j) = 1, quad forall r in R, forall v in V_r^s, forall t in T $ <eq:mgmt-relationship>

@eq:flow and @eq:mgmt-flow express flow conservation on service and management
links, respectively.

$ sum_((i,j) in E^p) pi_(i j)^((u,v)) - sum_((j,i) in E^p) pi_(j i)^((u,v)) = sum_(t in T) z_(u i)^t - sum_(t in T) z_(v i)^t, \
  forall i in V^p, (u,v) in E_r^s, r in R $ <eq:flow>

$ sum_((i,j) in E^p) overline(pi)_(i j)^v - sum_((j,i) in E^p) overline(pi)_(j i)^v = sum_(t in T) z_(v i)^t - overline(z)_(r i), \
  forall i in V^p, v in V_r^s, r in R $ <eq:mgmt-flow>

@eq:link-bw limits the consumed bandwidth of each link by its capacity.

$ sum_(v in union.big_(r in R) V_r^s) overline(pi)_(i j)^v dot b^m + sum_(r in R) sum_((u,v) in E_r^s) pi_(i j)^((u,v)) dot b_((u,v),r)^s <= b_(i j)^p, \
  forall (i,j) in E^p $ <eq:link-bw>

@eq:radius controls the management radius.

$ sum_((i,j) in E^p) overline(pi)_(i j)^v <= rho quad forall v in union.big_(r in R) V_r^s $ <eq:radius>

The objective is to maximize the profit from placing chains:

$ max sum_(r in R) c_r x_r - sum_(i in V^p) phi dot overline(y)_i $ <eq:objective>

The problem is an ILP and can be reduced to bin packing, so it is NP-hard.
