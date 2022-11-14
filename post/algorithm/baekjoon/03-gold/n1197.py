import sys
import heapq
input = sys.stdin.readline

V, E = map(int, input().split())
graph = [[] for _ in range(V+1)]
visited = [False for _ in range(V+1)]
heap = [[0, 1]]
for _ in range(E):
    A, B, C = map(int, input().split())
    graph[A].append([C, B])
    graph[B].append([C, A])

total_weight = 0
node_cnt = 0
while heap:
    if node_cnt == V:
        break
    weight, node = heapq.heappop(heap)
    if not visited[node]:
        visited[node] = True
        total_weight += weight
        node_cnt += 1
        for i in graph[node]:
            heapq.heappush(heap, i)

print(total_weight)
