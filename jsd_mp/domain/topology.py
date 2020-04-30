import typing
import dataclasses

from .direction import Direction


@dataclasses.dataclass(frozen=True)
class Node:
    """
    Node represents a physical node in a data-center network. Nodes may
    have computation capacity.
    """

    cores: int
    memory: int
    direction: Direction = Direction.NONE
    vnf_support: bool = True


@dataclasses.dataclass(frozen=True)
class Link:
    bandwidth: int


class Topology:
    def __init__(self):
        # stores nodes with their name
        self.nodes: typing.Map[str, Node] = {}
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
        if name not in self.nodes:
            return self.add_node(name, node)
        self.nodes[name] = node

    def update_link(self, source: str, destination: str, link: Link):
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError("source and destination must be valid nodes")
        if (source, destination) not in self.links:
            return self.add_link(source, destination, link)
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
        self, source: str, destination: str, required_bandwidth: int
    ) -> typing.Union[typing.List[typing.Tuple[str, str]], None]:
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError("source must be valid nodes")

        q: typing.List[typing.Tuple[str, typing.List[typing.Tuple[str, str]]]] = [
            (source, [])
        ]
        see: typing.Set[str] = set()

        while len(q) != 0:
            root = q.pop()
            see.add(root[0])

            if root[0] == destination:
                return root[1]

            for adj in self.connections[root[0]]:
                if (
                    adj not in see
                    and self.links[(root[0], adj)].bandwidth >= required_bandwidth
                ):
                    path = root[1].copy()
                    path.append((root[0], adj))
                    q.append((adj, path))

        return None

    def bfs(
        self, source: str, required_bandwidth: int
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
            root: typing.Tuple[str, int] = q.pop()
            see.add(root[0])
            height = root[1]

            reachability.append(root)

            for adj in self.connections[root[0]]:
                if (
                    adj not in see
                    and self.links[(root[0], adj)].bandwidth >= required_bandwidth
                ):
                    q.append((adj, height + 1))

        return reachability
