import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


class Node:
    def __init__(self, index):
        self.index = index
        self.data = 0
        self.root = self
        self.parent = self
        self.active = None
        self.passive = []

    def get_branch(self):
        if self.active:
            return self.passive + [self.active]
        else:
            return []

    def set_branch(self, node, data):
        if self.root == node.root:
            if data < node.data:
                node.parent = self
                node.data = data
        else:
            node.root = self.root
            node.parent = self
            node.data += data
        if not self.active:
            self.active = node
            self.data += node.data
            node.data = self.data
        else:
            self.passive.append(node)
        self.update_data()

    def update_data(self):
        branch = self.get_branch()
        branch.sort(key=lambda n: n.data, reverse=True)
        active = branch.pop()
        if active != self.active:
            self.active = active
            self.passive = branch
        self.data = self.active.data


def union_root(source: Node, target: Node, data: int) -> None:
    root = source.root
    if target.root in [source, source.root, target]:
        source.set_branch(target, data)
        while source != root:
            source = source.parent
            source.update_data()


V, E = map(int, input().split())

if V > 1:
    graph = [Node(i) for i in range(V + 1)]
    edge_dict = {}

    for _ in range(E):
        A, B, C = map(int, input().split())
        edge_dict[(A, B)] = C

    edge_list = sorted(edge_dict.items(), key=lambda x: [x[1], x[0]])

    for (a, b), c in edge_list:
        node_a, node_b = graph[a], graph[b]
        if node_a.parent != node_b.parent:
            union_root(node_a, node_b, c)

    weight = 2147483647

    for edge_node in graph:
        if (edge_node.root == edge_node) and edge_node.get_branch():
            if edge_node.data < weight:
                weight = edge_node.data

    print(weight)
else:
    print(0)
