# Lv3. 가장 먼 노드
# https://school.programmers.co.kr/learn/courses/30/lessons/49189

from collections import defaultdict, deque

def bfs(dists, nodes):
    q = deque(nodes[1])
    dists[1] = -1
    dist = 1
    while q:
        for _ in range(len(q)):
            v = q.popleft()
            if dists[v] == 0:
                dists[v] = dist
                for w in nodes[v]:
                    q.append(w)
        dist += 1

def solution(n, vertex):
    dists = [0 for _ in range(n+1)]
    nodes = defaultdict(list)

    for v, u in vertex:
        nodes[v].append(u)
        nodes[u].append(v)

    bfs(dists, nodes)
    max_value = max(dists)

    answer = sum([1 if d == max_value else 0 for d in dists])
    return answer