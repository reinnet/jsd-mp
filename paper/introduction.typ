Telecommunications industry has traditionally been responsible for setting up
and deploying services. Moreover, network operators deploy proprietary and
custom-built hardware and equipment for each function in their infrastructure.
Stability and high-quality results can earn the trust of service providers in
regards to proprietary hardware.

However, we are facing increased users' demand for a variety of short-lived and
high traffic services. Therefore, service providers should constantly upgrade
themselves in terms of purchase, store, and deployment of new physical
equipment. These implementations in turn increase the overall expenditure of
service providers. In addition, with the increase in total number of equipment,
the amount of available space for deploying new equipment shrinks. Finally,
increased expenditure for retraining staff to gain the knowledge of working with
new equipment should also be considered. The worst-case scenario is that, with
the acceleration of innovation in services and technology, the hardware life
cycle becomes shorter, which prevents innovation in network services.

In the traditional method of deploying a network service, user traffic must pass
through a number of network functions in a certain order to create a traffic
processing route. At present, these functions are connected to each other in the
form of hardware, and traffic is forwarded to them using routing tables. The
main challenge of this method is that it is difficult to establish and change
the order of functions. For example, over time, as network conditions change, we
need to change the connectivity and location of functions to better serve users,
which requires moving functions and changing routing tables. In the traditional
way, this was a difficult and costly task that can lead to many errors. On the
other hand, the rapid change of services desired by users requires a rapid
change in the order of functions, which is difficult to make in the current
method. Therefore, network operators have found the need for programmable
networks and dynamic service chaining.

In recent years, software-based networks and network virtualization have
received much attention. Service providers have begun to move towards
virtualized and software-networked functions, so they can provide innovative
services to users. This process creates an option for service providers in
regards to proprietary hardware and reduces the cost of setting up and
maintaining the service.

The main idea of network function virtualization is to separate the physical
equipment of the network from its function. A network function such as a
firewall can be deployed on standard servers as simple software. Therefore, a
service can be deployed using virtual network functions, which can themselves be
implemented as software and run on one or more physical standard hosts. Virtual
network functions can be relocated or instantiated in different locations
without the need to purchase and install new equipment.

It is worth mentioning that SDN concerns forwarding tables and their centralized
updates. This can take place alongside NFV, as NFV operates at the service layer
and does not address how to update forwarding tables. Therefore, what is stated
in this study is related to NFV networks, but it can also be used in networks
that have an SDN infrastructure.

The problem of deploying virtual network functions is one of the major
challenges in allocating resources to service function chaining and has received
great attention in the past few years. The problem of embedding virtual network
functions is divided into two sub-problems — mapping of virtual nodes and
virtual links — which must be considered simultaneously. There are many mapping
limitations that need to be considered: the physical resources selected from the
infrastructure network must meet the functional requirements of the virtual
network (for example, the processing power of a virtual function must be less
than or equal to the processing power of the physical node on which it is
mapped), and the need for a specific physical node for a function must also be
considered.

In addition, there is a set of restrictions that apply to service function
chaining. One is the existence of a VNFM for managing the life cycle of
functions; due to the importance of the connection delay between the virtual
network function and its VNFM, the VNFM must be located in a suitable place.
Therefore, a new sub-problem is added to the main issue.

The present study discusses this issue for the first time. Nowadays, due to the
importance of monitoring, a huge amount of expense is spent on monitoring data
centers, and in many cases adding monitoring as a second thought brings its own
drawbacks. This study intends to consider the need for management at the time of
mapping to prevent future losses.

One of the main innovations of this research is the definition of the problem
together with attention to management needs, which allows the system
administrator to implement and adjust all the required policies. The present
study examines the placement of service function chains together with the
limitations of management resources and formulates it as an admission-control
problem in a linear manner. Another innovation is a heuristic method based on
@Bari2015 and @AbuLebdeh2017 that improves both implementation time and final
output.

In the NFV ecosystem, each chain must be monitored and managed by a VNFM.
Similar to other virtual functions, VNFMs need computing and network resources
and can manage a limited number of chains. Our work considers the Service Chain
Placement Problem and the Manager Placement Problem _jointly_ and places chains
and their corresponding VNFMs at the same time. We believe this work has not been
done in the literature before. By considering the joint problem, the placement avoids
committing VNFs to a layout that no admissible manager can serve, so chains a
management-blind pipeline would strand stay feasible. The benefit is therefore a
_feasibility_ effect that is _conditional_ on the management constraints binding,
and the results in @sec:joint-vs-disjoint, @sec:acceptance, and @sec:sweep
confirm it.

The paper is structured as follows. In @sec:related-works we review the
literature; we then describe the problem in @sec:system-model and formulate it in
@sec:formulation as an ILP. In @sec:solution we propose a polynomial-time
solution and evaluate its results in @sec:results. We conclude the paper in
@sec:conclusion.
