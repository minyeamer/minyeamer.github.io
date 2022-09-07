import operator
from collections import defaultdict
from heapdict import heapdict
import heapq
import sys
input = sys.stdin.readline

def prim(nodes: dict, start: int) -> int or float:
    mst, keys, pi = [], heapdict(), dict()
    depth, total_weight = -1, 0

    for n in nodes.keys():
        keys[n] = float('inf')
        pi[n] = None
    keys[start], pi[start] = 0, start

    while keys:
        current_node, current_key = keys.popitem()
        current_depth = get_depth(pi, start, current_node, 0)
        if current_depth <= depth:
            if pi[current_node] == start:
                return float('inf')
            break
        depth = current_depth
        mst.append([pi[current_node], current_node, current_key])
        total_weight += current_key

        for adjacent, weight in nodes[current_node].items():
            if adjacent in keys and weight < keys[adjacent]:
                keys[adjacent] = weight
                pi[adjacent] = current_node

    return total_weight

def get_depth(nodes: dict, root: int, start: int, data: int) -> int:
    if start == root:
        return data
    if nodes[start] == root:
        return data+1
    return get_depth(nodes, root, nodes[start], data+1)


V, E = map(int, input().split())
graph = defaultdict(dict)

if V > 1:
    for _ in range(E):
        A, B, C = map(int, input().split())
        graph[A][B] = C
        graph[B][A] = C

    weight_list = []
    for node in graph.keys():
        heapq.heappush(weight_list, prim(graph, node))

    print(heapq.heappop(weight_list))
else:
    print(0)
