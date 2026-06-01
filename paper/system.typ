In this section, after discussing the assumptions and system model, the problem
of joint SFC deployment and VNFM placement is stated and clarified by an
illustrative example.

== Assumptions <subsec:assumptions>

In the JSD-MP problem, a set of SFCs needs to be deployed in the physical
infrastructure network. The main assumption is that, in addition to
computational and network resources, a VNFM must be assigned to each SFC to
manage its VNFs. All VNFs of a chain must be managed by a single VNFM, but a VNFM
can manage multiple SFCs. The capacity of each VNFM is limited in terms of the
number of VNF instances, and each VNFM needs a license for managing a specific
number of instances. Moreover, only a subset of physical servers can host VNFMs,
and similarly each VNF type can be placed only on a subset of physical servers.
The traffic ingress and egress of each chain are conducted by special VNF types
that must be placed on ingress and egress nodes of the physical network,
respectively.

VNF instances deployed on a physical server can only be managed by VNFMs placed
on a given subset of physical servers. To maintain the timing requirement of the
management traffic, the distance (in hop count) between each VNFM and its
associated VNFs must be less than a specified threshold. JSD-MP also assumes VNFs
cannot be shared between chains.

== System Model <subsec:sysmodel>

The physical infrastructure topology is modeled as a directed graph
$G^p = (V^p, E^p)$, where $V^p$ is the set of NFVI-PoPs and $E^p$ is the set of
inter-PoP links. The computational capacity of PoP $i in V^p$ is specified by
$c_i^p$ CPU cores and $m_i^p$ gigabytes of RAM. The bandwidth of link
$(i,j) in E^p$ is $b_(i j)^p$.

The set of requested SFCs is denoted by $R$. Each request $r in R$ has revenue
$c_r$ and is represented by a directed graph $G_r^s = (V_r^s, E_r^s)$, where
$V_r^s$ is the set of VNFs and $E_r^s$ is the set of virtual links. The type of
VNF $v in V_r^s$ is $t_(v,r) in T$, where $T$ is the set of function types. Each
type $t$ determines the required number of CPU cores $c_t^s$ and the required
memory $m_t^s$ to create an instance. The required bandwidth of virtual link
$(u,v) in E_r^s$ is $b_((u,v),r)^s$.

Each VNFM requires $c^m$ CPU cores and $m^m$ gigabytes of RAM to handle at most
$kappa$ VNFs. To launch a VNFM, the service provider pays the license fee $phi$.
There is a dedicated virtual management link with bandwidth $b^m$ between every
VNF instance and its associated VNFM. We use $rho$ for the maximum hop count of
each management link, and the parameter $eta_(i,j)$ indicates whether a VNFM
mapped to physical server $i in V^p$ can manage VNFs placed on physical node
$j in V^p$. The notation is summarized in @tbl:parameters.

#figure(
  caption: [Parameters],
  table(
    columns: (auto, 1fr), align: (center + horizon, left), inset: 5pt,
    [$V^p$], [the set of NFVI-PoPs],
    [$E^p$], [the set of inter-PoP links],
    [$c_i^p$], [number of CPU cores of server $i$],
    [$m_i^p$], [amount of RAM in server $i$],
    [$b_(i j)^p$], [bandwidth of link $(i,j) in E^p$],
    [$V_r^s$], [the set of VNFs for request $r$],
    [$E_r^s$], [the set of virtual links of request $r$],
    [$m_t^s$], [required RAM (GB) of a VNF instance of type $t in T$],
    [$c_t^s$], [required CPU cores of a VNF instance of type $t in T$],
    [$m^m$], [required RAM (GB) of a VNFM],
    [$c^m$], [required CPU cores of a VNFM],
    [$kappa$], [maximum number of VNF instances a VNFM can handle],
    [$tau(v, t)$], [returns 1 if VNF instance $v$ has type $t$],
    [$b_((u,v),r)^s$], [required bandwidth for virtual link $(u,v) in E_r^s$],
    [$b^m$], [required bandwidth for each virtual management link],
    [$rho$], [maximum hop count of management links],
    [$phi$], [VNFM license fee],
    [$eta_(i,j)$], [1 if VNFs on server $i$ can be managed by VNFMs on server $j$],
  ),
) <tbl:parameters>

== Problem Statement

Under the assumptions of @subsec:assumptions, the JSD-MP problem is defined using
the notation of @subsec:sysmodel. The NFVI service provider owns the
infrastructure network $G^p$, and a set $R$ of requests is given. The provider's
goal is to accept a subset of requests that maximizes profit. To accept a request
$r$, the provider must allocate $c_(t_(v,r))^s$ CPU cores and $m_(t_(v,r))^s$
memory for all $v in r$; moreover, $b_((u,v),r)^s$ bandwidth must be allocated
for all links $(u,v) in E_r^s$, and a VNFM must be assigned to the chain. These
allocations must satisfy the requirements in @subsec:assumptions. Profit is the
revenue from accepted requests minus the license cost $phi$ paid for each VNFM.

The idea behind JSD-MP is that, when placing the VNFM of a chain, the locations
of the chain's VNFs should be taken into account. By jointly conducting SFC
deployment and VNFM placement, the provider can maximize profit.

== Illustrative Example

@fig:example-chains shows two request chains where the VNF types and the required
bandwidth of the virtual links (in Mbps) are depicted; each request is worth
\$100. The provider owns the infrastructure in @fig:example-topology. VNF types
are described in @tbl:example-vnf-types, and @tbl:example-server-spec shows the
physical server specifications. There are a few constraints: instances can run
only on servers 1, 3, 5, and 7 (the rest are fully utilized); VNFs on servers 1
and 3 can be managed only by VNFMs on servers 2 and 4; VNFs on server 5 only by
VNFMs on servers 4 and 6; VNFs on server 7 only by VNFMs on servers 6 and 8. Each
VNFM handles at most 5 instances with 4 GB RAM and 2 CPU cores, and a license
costs \$10. Management links require a 10 Mbps reservation, the maximum hop count
for management is 10, and all physical links have 40 Gbps capacity.

#figure(
  image("images/example-chains.png", width: 70%),
  caption: [Chains for the illustrative example],
) <fig:example-chains>

#figure(
  image("images/example-toplogy.png", height: 150pt),
  caption: [Topology of the illustrative example],
) <fig:example-topology>

#figure(
  caption: [VNF types of the illustrative example],
  table(
    columns: 4, align: center, inset: 6pt,
    [Spec / VNF], [vFW], [vNAT], [vIDS],
    [CPU (vCore)], [2], [2], [2],
    [Memory (GB)], [2], [4], [2],
  ),
) <tbl:example-vnf-types>

#figure(
  caption: [Server specifications of the illustrative example],
  table(
    columns: 3, align: center, inset: 6pt,
    [], [Servers 1,2,7,8], [Servers 3,4,5,6],
    [Installed vCPU], [144], [72],
    [Installed Memory (GB)], [1408], [288],
    [Link (Gbps)], [40], [40],
  ),
) <tbl:example-server-spec>

The optimal solution of this instance, obtained by the MILP formulation of
@sec:formulation, accepts both chains using two VNFM instances costing \$20, for
a total revenue of \$180. Instance mappings are shown in @tbl:example-chain-1-map
and @tbl:example-chain-2-map, and the link mappings in @tbl:example-chain-1-links
and @tbl:example-chain-2-links.

#figure(
  caption: [Chain-1 instance mapping],
  table(
    columns: 5, align: center, inset: 6pt,
    [0: Source], [1: FW], [2: NAT], [3: Destination], [VNFM],
    [9], [1], [3], [9], [4],
  ),
) <tbl:example-chain-1-map>

#figure(
  caption: [Chain-2 instance mapping],
  table(
    columns: 5, align: center, inset: 6pt,
    [0: Source], [1: FW], [2: IDS], [3: Destination], [VNFM],
    [9], [3], [3], [9], [4],
  ),
) <tbl:example-chain-2-map>

#figure(
  caption: [Chain-1 link mapping],
  table(
    columns: (auto, 1fr), align: (center, left), inset: 6pt,
    [Virtual Link], [Physical Links],
    [(0, 1)], [(9, 10) (10, 12) (12, 1)],
    [(1, 2)], [(1, 12) (12, 10) (10, 13) (13, 3)],
    [(2, 3)], [(3, 13) (13, 10) (10, 9)],
    [VNF 0 Mgmt.], [(9, 10) (10, 13) (13, 4)],
    [VNF 1 Mgmt.], [(1, 12) (12, 10) (10, 13) (13, 4)],
    [VNF 2 Mgmt.], [(3, 13) (13, 4)],
    [VNF 3 Mgmt.], [(9, 10) (10, 13) (13, 4)],
  ),
) <tbl:example-chain-1-links>

#figure(
  caption: [Chain-2 link mapping],
  table(
    columns: (auto, 1fr), align: (center, left), inset: 6pt,
    [Virtual Link], [Physical Links],
    [(0, 1)], [(9, 10) (10, 13) (13, 4)],
    [(1, 2)], [---],
    [(2, 3)], [(3, 13) (13, 10) (10, 9)],
    [VNF 0 Mgmt.], [(3, 13) (13, 10) (13, 4)],
    [VNF 1 Mgmt.], [(3, 13) (13, 4)],
    [VNF 2 Mgmt.], [(3, 13) (13, 4)],
    [VNF 3 Mgmt.], [(9, 10) (10, 13) (13, 4)],
  ),
) <tbl:example-chain-2-links>
