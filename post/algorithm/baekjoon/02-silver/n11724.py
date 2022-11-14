import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


def dfs(dfs_nodes, dfs_visited, dfs_node):
    dfs_visited[dfs_node] = True

    for next_node in dfs_nodes[dfs_node]:
        if not dfs_visited[next_node]:
            dfs(dfs_nodes, dfs_visited, next_node)


N, M = map(int, input().split())
nodes = [[] for _ in range(N+1)]
visited = [False for _ in range(N+1)]
parents = set()
count = 0

for _ in range(M):
    u, v = map(int, input().split())
    parents.add(u)
    nodes[u].append(v)
    nodes[v].append(u)

others = set([i for i in range(1, N+1)]) - parents

for node in parents:
    if not visited[node]:
        dfs(nodes, visited, node)
        count += 1

for node in others:
    if not visited[node]:
        dfs(nodes, visited, node)
        count += 1

print(count)
