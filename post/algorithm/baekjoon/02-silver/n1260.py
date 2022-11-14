import heapq
import sys
from collections import deque

sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


def dfs(nodes, visited, node):
    visited[node] = True

    next_nodes = nodes[node]
    while next_nodes:
        next_node = heapq.heappop(next_nodes)
        if not visited[next_node]:
            print(next_node, end=' ')
            dfs(nodes, visited, next_node)


def bfs(nodes, visited, root):
    queue = deque()
    visited[root] = True
    queue.append(root)

    while queue:
        node = queue.popleft()
        visited[node] = True
        print(node, end=' ')

        next_nodes = nodes[node]
        while next_nodes:
            next_node = heapq.heappop(next_nodes)
            if not visited[next_node]:
                visited[next_node] = True
                queue.append(next_node)


N, M, V = map(int, input().split())
dfs_nodes = [[] for _ in range(N+1)]
bfs_nodes = [[] for _ in range(N+1)]
dfs_visited = [False for _ in range(N+1)]
bfs_visited = [False for _ in range(N+1)]

for _ in range(M):
    u, v = map(int, input().split())
    heapq.heappush(dfs_nodes[u], v)
    heapq.heappush(dfs_nodes[v], u)
    heapq.heappush(bfs_nodes[u], v)
    heapq.heappush(bfs_nodes[v], u)

print(V, end=' ')
dfs(dfs_nodes, dfs_visited, V)
print()
bfs(bfs_nodes, bfs_visited, V)
print()
