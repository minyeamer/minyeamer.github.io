import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


def dfs(dfs_nodes, dfs_infected, dfs_node):
    dfs_infected[dfs_node] = True

    for next_node in dfs_nodes[dfs_node]:
        if not dfs_infected[next_node]:
            dfs(dfs_nodes, dfs_infected, next_node)


com_num = int(input())
computers = [[] for _ in range(com_num+1)]
infected = [False for _ in range(com_num+1)]
count = -1

for _ in range(int(input())):
    x, y = map(int, input().split())
    computers[x].append(y)
    computers[y].append(x)

dfs(computers, infected, 1)

for virus in infected:
    if virus:
        count += 1

print(count)
