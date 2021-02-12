import typing
import dataclasses

from .direction import Direction


@dataclasses.dataclass(frozen=True)
class Node:
    """
    Node represents a physical node in a data-center network. Nodes may
    have computation capacity.

    not_manager_nodes contains the list of nodes that cannnot manage the
    current node.
    """

    cores: int
    memory: int
    direction: Direction = Direction.NONE
    vnf_support: bool = True
    not_manager_nodes: typing.List[str] = dataclasses.field(
        default_factory=list
    )


@dataclasses.dataclass(frozen=True)
class Link:
    bandwidth: int


class Topology:
    """
    Topology class handles the topology with some helpers
    """

    def __init__(self):
        # stores nodes with their name
        self.nodes: typing.Dict[str, Node] = {}
        # stores connections in adjacency list
        self.connections: typing.Dict[str, typing.List[str]] = {}
        # stores link information of source and destination
        self.links: typing.Dict[typing.Tuple[str, str], Link] = {}

    def add_node(self, name: str, node: Node):
        """
        Add given node with its name.
        Please note that node names must be unique.
        """
        if name in self.nodes:
            raise ValueError("node's name must be unique")
        self.nodes[name] = node
        self.connections[name] = []

    def update_node(self, name: str, node: Node):
        """
        Based on given name updates the node with the given node
        if it exists and inserts it if it doesn't
        """
        if name not in self.nodes:
            self.add_node(name, node)
            return
        self.nodes[name] = node

    def update_link(self, source: str, destination: str, link: Link):
        """
        Based on given source and destination updates the link with given link,
        if it doesn't exist inserts it.
        """
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError("source and destination must be valid nodes")
        if (source, destination) not in self.links:
            self.add_link(source, destination, link)
            return
        self.links[(source, destination)] = link

    def add_link(self, source: str, destination: str, link: Link):
        """
        Add one direction link from source node to destination node.
        """
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError("source and destination must be valid nodes")
        self.connections[source].append(destination)
        self.links[(source, destination)] = link

    def path(
        self,
        source: str,
        destination: str,
        required_bandwidth: int,
        max_height: int = -1,
    ) -> typing.Union[typing.List[typing.Tuple[str, str]], None]:
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError("source must be valid nodes")

        q: typing.List[
            typing.Tuple[str, typing.List[typing.Tuple[str, str]]]
        ] = [(source, [])]
        see: typing.Set[str] = set()

        while len(q) != 0:
            root = q.pop(0)
            see.add(root[0])

            if root[0] == destination:
                return root[1]

            if len(root[0]) == max_height:
                continue

            for adj in self.connections[root[0]]:
                if (
                    adj not in see
                    and self.links[(root[0], adj)].bandwidth
                    >= required_bandwidth
                ):
                    path = root[1].copy()
                    path.append((root[0], adj))
                    q.append((adj, path))

        return None

    def bfs(
        self,
        source: str,
        required_bandwidth: int,
        max_height: int = -1,
    ) -> typing.List[typing.Tuple[str, int]]:
        """
        Run BFS from a given source and return its reachable nodes.
        It returns reachability information in the following tuple:
        (node, height)
        """
        if source not in self.nodes:
            raise ValueError("source must be valid nodes")

        q: typing.List[typing.Tuple[str, int]] = [(source, 0)]
        reachability: typing.List[typing.Tuple[str, int]] = []
        see: typing.Set[str] = set()

        while len(q) != 0:
            root: typing.Tuple[str, int] = q.pop(0)
            see.add(root[0])
            height = root[1]

            reachability.append(root)

            if height == max_height:
                continue

            for adj in self.connections[root[0]]:
                if (
                    adj not in see
                    and self.links[(root[0], adj)].bandwidth
                    >= required_bandwidth
                ):
                    q.append((adj, height + 1))

        return reachability
