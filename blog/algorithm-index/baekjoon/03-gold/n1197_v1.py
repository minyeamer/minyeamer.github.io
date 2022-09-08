import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


class Node:
    def __init__(self, index):
        self.index = index
        self.data = 2147483647
        self.parent = []
        self.child = []

    def print_node(self):
        print(self.index, self.data, self.parent, self.child)


def spanning_tree(nodes, check, root, parent, data):
    for child in parent.child:
        weight = data + child[1]
        child = nodes[child[0]]
        if child.child:
            if not check[child.index]:
                spanning_tree(nodes, check, root, child, weight)
        else:
            check[parent.index] = True
            if weight < root.data:
                root.data = weight


V, E = map(int, input().split())
graph = [Node(i) for i in range(V+1)]
visited = [False for _ in range(V+1)]

for _ in range(E):
    A, B, C = map(int, input().split())
    graph[A].child.append((B,C))
    graph[B].parent.append((A,C))

min_weight = 2147483647

for node in graph:
    if node.child and not node.parent:
        spanning_tree(graph, visited, node, node, 0)
        if node.data < min_weight:
            min_weight = node.data

print(min_weight)
