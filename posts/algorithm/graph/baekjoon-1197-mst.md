---
title: "[Python] 백준 1197 - 최소 스패닝 트리 (Gold 4)"
date: "2022-03-20T16:18:29+09:00"
layout: "post"
description: >
  백준 1197 최소 스패닝 트리(MST) 문제를 DFS, 크루스칼, 프림 알고리즘으로 차례대로 접근하며 시행착오를 겪은 과정을 상세히 기록했습니다.
  각 알고리즘의 한계와 개선 방향, 그리고 최종 해결까지의 여정을 코드와 함께 공유합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/urp006mklessb60476rk9/baekjoon-cover.webp?rlkey=l2rycs6gxicqd29c4xr0e8ogd&dl=0"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/tg1jfh6uc53wykiuden0x/baekjoon-cover-og.webp?rlkey=ptw8l3wroyh530mzhhx7mi5tf&dl=0"
categories: ["Algorithm", "Graph"]
tags: ["백준", "최소 스패닝 트리", "MST", "DFS", "크루스칼 알고리즘", "프림 알고리즘", "Python", "알고리즘", "Union-Find", "Heap", "백준 Gold 4"]
---

{{< bookmark
  url="https://www.acmicpc.net/problem/1197"
  title="1197번: 최소 스패닝 트리"
  description="그래프가 주어졌을 때, 그 그래프의 최소 스패닝 트리를 구하는 프로그램을 작성하시오. 최소 스패닝 트리는, 주어진 그래프의 모든 정점들을 연결하는 부분 그래프 중에서 그 가중치의 합이 최소인 트리를 말한다."
  image="https://dl.dropboxusercontent.com/scl/fi/tg1jfh6uc53wykiuden0x/baekjoon-00-cover-og.webp?rlkey=ptw8l3wroyh530mzhhx7mi5tf&dl=0"
  fetch="false" >}}

해당 문제는 n개의 정점들에 대한 간선들 중에서 가장 가중치가 작은 경로의 가중치를 찾는 것이다.  

정답 풀이보다는 여러가지 방식으로 시도하면서 알고리즘을 발전시키는 과정을 서술한다.

## DFS

처음엔 노드하면 DFS와 BFS 밖에 몰랐기 때문에 당연하게 DFS로 접근했다.

먼저 부모, 자식, 가중치, 인덱스를 변수로 가지는 Node 클래스를 선언하여
간선의 정보를 노드 내 인스턴스 변수에 저장하게 한다.

전체 노드 중 자식 노드를 가진 노드에 한해 가중치 최솟값을 구하는 함수를 실행한다.

1. 해당 함수는 root에서부터 end-point까지 순회하면서 가중치 합의 최솟값을 구하는 동작을 수행한다.
2. 함수의 결과는 따로 반환되지 않고 root 노드의 인스턴스 변수에 저장된다.

이러한 논리를 가지고 작성한 알고리즘이 글 밑에 있는 첫 번째 코드이다.

하지만 해당 코드는 1초의 시간 제한 안에 돌아가기엔 무리가 있었다.

### 첫 번째 알고리즘

```python
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
```

## 크루스칼 알고리즘

DFS로 안된다는 것을 깨닫고 질문글을 훑어본 후 크루스칼 알고리즘을 선택하기로 했다.

우선 고려해야할 것은 크루스칼 알고리즘이 모든 노드를 연결시키기 위한 알고리즘이라는 것이다.

해당 문제는 root 노드에서부터 시작하는 모든 경로를 고려해야 하는데 크루스칼 알고리즘을
사용할 경우 가장 작은 가중치로 시작하는 경로만을 선택하고 나머지를 무시하게 된다.

- 이 경우 발생하는 반례가 다음과 같다.

```
3 3
1 2 2
1 3 3
2 3 9999
output: 10001
answer: 3
```

1. 크루스칼 알고리즘에 의해 1 -> 2의 간선을 선택하고 1 -> 3의 간선을 무시할 경우
  최종적으로는 1 -> 2 -> 3의 경로에 대한 가중치 10001을 결과로 얻게 된다.
2. 이에 대한 해결책으로 생각한 것이 EtherChannel의 Active/Passive 개념이다.
3. 앞서 시도한 DFS 기반 알고리즘에 크루스칼 알고리즘을 조합해서 모든 경로를 탐색하는데
  가중치가 가장 작은 경로로 이어지는 자식 노드를 Active로, 나머지를 Passive로 분류한다.
4. 만약 한 노드에 새로운 자식 노드가 추가되면 자식 노드들의 가중치를 비교해서 Active를 갱신하고
  해당 노드의 부모 노드를 타고 올라가며 동일한 작업을 반복한다.

해당 알고리즘은 root 노드에서부터 모든 자식 노드를 탐색해야 했던 DFS 기반 알고리즘과는 반대로
자식 노드에서부터 root 노드까지의 경로만을 탐색하기 때문에 시간 초과를 피할 수 있었다.

하지만 여러 조건들을 고려하다보니 작성자인 나조차도 알아보기 힘들정도로 코드가 많이 복잡해졌고
root 노드가 기준인데 굳이 아래서부터 위를 탐색하는 방식이 마음에 들지 않았다.
그리고 가장 큰 문제는 해당 알고리즘에도 반례가 있어서 정답이 될 수 없었다는 것이다.

### 두 번째 알고리즘

```python
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
```

## 프림 알고리즘

하루동안 고민한 끝에 크루스칼 알고리즘을 포기하고 이와 비슷하다는 프림 알고리즘을 선택하게 되었다.

이제까지 사용했던 Node 인스턴스 내에 모든 정보를 저장하는 접근방식을 버리고
프림 알고리즘의 기본에 집중했다.

부모 노드의 값을 자식 노드의 배열 값에 저장하는 Union-Find 알고리즘을 기반으로 그래프를 그리고
모든 노드에 대해 프림 알고리즘을 수행하여 최소 가중치를 구하는 방식을 구상했다.

하지만 이 경우에 두 가지 문제점이 있었다.

1. 프림 알고리즘도 결국 모든 노드를 연결하기 위한 알고리즘이기 때문에
  root에서 end-point까지 갔다 하더라도 거기서 멈추지 않고 다른 경로를 탐색하는 문제가 생긴다.

   - 해당 문제에 대한 해결책으로 Find 연산을 응용한 깊이 탐색 과정을 추가했다.
   - 매 반복마다 현재 노드에 대해 Find 연산을 수행하고 재귀한 횟수 반환하여 깊이로 지정한다.
   - 깊이가 지속적으로 증가하지 않을 경우 end-point까지 도달했다 판단하여 반복을 멈춘다.

2. 모든 경로의 깊이가 1일 경우 1번 조건을 무시하고 다른 경로를 탐색하는 문제가 있다.

   - root 노드에서 시작했는데 다시 root 노드로 돌아올 경우 해당 노드 자체를 무시한다.
   - 위 조건에 걸릴 경우 양의 무한대 값을 반환하여 가중치 판단 과정에서 제외시킬 수 있었다.
   - 이렇게 많은 시행착오를 거쳤지만 하나를 해결하면 다른 빈틈이 생겨버려 포기할 수밖에 없었다.
   - 심지어 백준에서는 heapdict 모듈을 지원하지 않아 해당 알고리즘을 활용할 수도 없었다.
   - 언젠가 이 문제를 완벽하게 해결하기 위해 디버그 값을 남긴다.

### 세 번째 알고리즘

```python
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

for _ in range(E):
    A, B, C = map(int, input().split())
    graph[A][B] = C
    graph[B][A] = C

weight_list = []
for node in graph.keys():
    heapq.heappush(weight_list, prim(graph, node))

print(heapq.heappop(weight_list))
```

```
3 3
1 2 2
1 3 3
2 3 9999
graph = {1: {2: 1, 3: 3}, 2: {1: 1, 3: 2}, 3: {2: 2, 1: 3}}
mst1 = [[1, 1, 0], [1, 2, 1], [2, 3, 2]], weight: 3
mst2 = [[2, 2, 0], [2, 1, 1], [2, 3, 2]], weight: 3
mst3 = [[3, 3, 0], [3, 2, 2], [2, 1, 1]], weight: 3
output: 3
answer: 3

6 8
1 3 -1
1 5 3
1 6 2
2 5 5
2 6 6
3 4 9
3 5 -1
5 6 -1
graph = {1: {3: -1, 5: 3, 6: 2}, 3: {1: -1, 4: 9, 5: -1}, 5: {1: 3, 2: 5, 3: -1, 6: -1}, 6: {1: 2, 2: 6, 5: -1}, 2: {5: 5, 6: 6}, 4: {3: 9}}
mst1 = [[1, 1, 0], [1, 3, -1], [3, 5, -1], [5, 6, -1], [5, 2, 5], [3, 4, 9]], w = 11
mst2 = [[3, 3, 0], [3, 5, -1], [5, 6, -1], [3, 1, -1], [5, 2, 5], [3, 4, 9]], w = 11
mst3 = [[5, 5, 0], [5, 6, -1], [5, 3, -1], [3, 1, -1], [5, 2, 5], [3, 4, 9]] 11
mst4 = [[6, 6, 0], [6, 5, -1], [5, 3, -1], [3, 1, -1], [5, 2, 5], [3, 4, 9]] 11
mst5 = [[2, 2, 0], [2, 5, 5], [5, 6, -1], [5, 3, -1], [3, 1, -1], [3, 4, 9]] 11
mst6 = [[4, 4, 0], [4, 3, 9], [3, 5, -1], [5, 6, -1], [3, 1, -1], [5, 2, 5]] 11
output: 11
answer: -3

3 3
1 2 2
1 3 3
2 3 9999
graph = {1: {2: 2, 3: 3}, 2: {1: 2, 3: 9999}, 3: {1: 3, 2: 9999}}
mst1 = [[1, 1, 0], [1, 2, 2], [1, 3, 3]], weight = 5
mst2 = [[2, 2, 0], [2, 1, 2], [1, 3, 3]], weight = 5
mst3 = [[3, 3, 0], [3, 1, 3], [1, 2, 2]], weight = 5
output: 5
answer: 3
```

## 결론

해당 문제에 대한 정답을 찾아본 결과 프림 알고리즘을 heapdict 없이 구현한 알고리즘을 보았는데
노드에 대한 방문 여부를 판단하여 경로를 구하는 방식이었다.

백준에서는 해당 문제가 통과되었지만 위 세 개의 데이터를 넣었을 때 예상과 다른 값이 나왔다.
아마 내가 문제를 제대로 이해하지 못했거나 채점 데이터 자체가 적어서 그랬을 것이다.
결과적으로 다른 사람이 작성한 정답을 보게 됐지만 완전히 납득하지는 못했다.

### 정답 알고리즘

```python
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
```
