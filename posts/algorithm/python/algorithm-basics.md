---
title: "파이썬 알고리즘 스터디 노트 - Set, Heap, DFS, BFS 정리"
date: "2022-03-20T13:37:54+09:00"
layout: "post"
description: >
  파이썬으로 자료구조(Set, Dictionary, Counter, Heap)와 알고리즘(Binary Search, DFS/BFS, Kruskal/Prim)을 학습한 스터디 노트입니다.
  백준 문제를 통해 시간 복잡도 개선 사례와 시행착오 과정을 코드와 함께 기록했습니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/4rjqwin7uhj6usnuuskmu/dfs-bfs.gif?rlkey=2t7382a8o6by70yqshafpi66f&st=1oa40lri&raw=1"
categories: ["Algorithm", "Python"]
tags: ["Python", "알고리즘", "자료구조", "백준", "Set", "Heap", "이진 탐색", "DFS", "BFS", "크루스칼 알고리즘", "프림 알고리즘", "Union-Find"]
---

## 자료구조

### Set

- [백준 1107번(리모컨) 문제](https://www.acmicpc.net/problem/1107)를 풀 때 사용
- 해당 문제는 특정 길이의 문자열에 대해 가능한 모든 조합을 탐색해야 하는데 시간복잡도를 줄이기 위해 중복이 없는 집합을 사용
- 빈집합은 set() 명령어로 간단하게 정의
- Set은 Dictionary와 동일한 Hash Table 기반이기 때문에 `x in s` 연산의 시간복잡도가
  **O(1)** 리스트의 `x in s` 연산 시간복잡도가 **O(n)** 인 것과는 큰 차이

#### Set을 활용한 코드 일부

```python
buttons = set([str(i) for i in range(10)])
channels = {N,}
diff = {abs(int_N-100)}
if M > 0:
    buttons -= set(list(input().split()))
    channels = set()
    for i in range(1, count+1):
        product = itertools.product(buttons, repeat=i)
        channels|= set(map(''.join, product))

    min_chan, max_chan = '0', '1'
    for _ in range(count-1):
        min_chan += max(buttons)
    for _ in range(count):
        max_chan += min(buttons)
    if set(max_chan) & buttons == set(max_chan):
        channels.add(max_chan)
    if set(min_chan) & buttons == set(min_chan):
        channels.add(min_chan)
```

### Dictionary

- [백준 1620번(나는야 포켓몬 마스터 이다솜) 문제](https://www.acmicpc.net/problem/1620)를 풀 때 사용
- 해당 문제는 문자열 또는 인덱스를 입력했을 때 대칭되는 값을 출력해야 하는데
  처음엔 시간복잡도가 **O(n)** 인 **List** 의 **index(x)** 를 사용하여 시간초과가 발생
- 문자열과 인덱스의 관계를 Dictionary로 구현해 탐색 시간복잡도를 **O(1)** 로 개선

### Coutner

- [백준 10816번(숫자카드 2) 문제](https://www.acmicpc.net/problem/10816)를 풀 때 사용
- 해당 문제는 숫자 카드의 값을 입력했을 때 해당 카드의 개수를 출력해야 하는데
  처음엔 시간복잡도가 **O(n)** 인 **List** 의 **count(x)** 를 사용하여 시간초과가 발생
- 전체 카드에 대한 Counter를 정의하여 탐색 시간복잡도를 **O(1)** 로 개선

### Heap

- [백준 7662번(이중 우선순위 큐) 문제](https://www.acmicpc.net/problem/7662)를 풀 때 사용
- 해당 문제는 최솟값과 최댓값 삭제 기능을 모두 가지고 있는 이중 우선순위 큐를 구현하는 것

1. 처음엔 **List** 의 **pop(x)**, **index(x)**, **max(x)/min(x)** 를 혼합하여 사용한 것 때문에
  **O(n^3)** 이상의 시간복잡도를 만들어서 시간초과가 발생
2. 두번째 시도에선 **List** 의 **pop(x)** 와 **heapq** 모듈의 **heappop(x)** 를 사용해 시간복잡도를 **O(1)** 로 개선
  하지만, Heap은 이진트리 기반으로 리스트와는 구조가 다르기 때문에 인덱스로 참조 시 에러가 발생
3. 세번째 시도에선 단일 큐를 Max Heap과 Min Heap으로 나누고 각각에서 **heappop(x), heappush(x)** 를 수행
  하지만, Max Heap 또는 Min Heap에서 삭제된 값이 반대쪽 Heap에서 남아있는 경우가 있어 에러가 발생
4. 해당 에러에 대한 해결책으로 Max Heap과 Min Heap을 동기화를 시키는 방법도 있지만,
  값이 유효한지 판단하는 **Dictionary** 를 구현해 값에 대한 참/거짓 여부를 참조하는 방법을 이용
  해당 Dictionary를 heappop(x) 사용 시 한 번, 최대/최솟값 출력 시 한 번씩 참조해 에러 해결

#### Heap을 활용한 코드 일부

```python
if cmd == 'I':
    n = int(n)
    heapq.heappush(min_Q, n)
    heapq.heappush(max_Q, -n)
    try:
        valid[n] += 1
    except KeyError:
        valid[n] = 1
    ins += 1
elif cmd == 'D':
    try:
        if n == '1':
            max_pop = -heapq.heappop(max_Q)
            while not valid[max_pop]:
                max_pop = -heapq.heappop(max_Q)
            valid[max_pop] -= 1
            ins -= 1
        elif n == '-1':
            min_pop = heapq.heappop(min_Q)
            while not valid[min_pop]:
                min_pop = heapq.heappop(min_Q)
            valid[min_pop] -= 1
            ins -= 1
    except IndexError:
        min_Q, max_Q = [], []
        continue
```

```python
max_pop, min_pop = 0, 0
while True:
    max_pop = -heapq.heappop(max_Q)
    if valid[max_pop]:
        break
while True:
    min_pop = heapq.heappop(min_Q)
    if valid[min_pop]:
        break
print(max_pop, min_pop)
```

## 조합/순열

### Combination

- [백준 1010번(다리 놓기) 문제](https://www.acmicpc.net/problem/1010)를 풀 때 사용
- 해당 문제는 강에 다리를 놓는 경우의 수를 출력해야 하는데 math 모듈의 comb 함수를 이용해 경우의 수를 계산

### Permutation

- [백준 1107번(리모컨) 문제](https://www.acmicpc.net/problem/1107)를 풀 때 사용
- 해당 문제에서 특정 길이의 문자열에 대해 가능한 모든 조합을 나열하는데,
  순서를 고려하고 중복을 허용하기 위해 중복 순열(Product)을 사용

#### Permutation을 활용한 코드 일부

```python
buttons = set([str(i) for i in range(10)])
...
for i in range(1, count+1):
        product = itertools.product(buttons, repeat=i)
        channels|= set(map(''.join, product))
```

## 탐색

### Binary Search

- [백준 1654번(랜선 자르기) 문제](https://www.acmicpc.net/problem/1654)를 풀 때 사용
- 해당 문제는 서로 다른 길이의 선들을 동일한 길이로 가장 길게 잘라야 되는데
  처음엔 가장 긴 선부터 가장 짧은 선까지의 범위 내에서 완전탐색을 진행하여 시간초과가 발생
- 완전탐색을 이분탐색으로 대체하여 시간복잡도 개선

#### Binary Search를 활용한 코드 일부

```python
while mn < mx:
    md = (mx + mn) // 2
    count = 0
    for i in range(K):
        count += k[i] // md
    if count < N:
        mx = md
    else:
        mn = md + 1
```

## 그래프

### DFS/BFS

- [백준 1260번(DFS와 BFS) 문제](https://www.acmicpc.net/problem/1260)를 풀 때 사용
- 해당 문제는 DFS와 BFS로 탐색했을 때의 결과를 출력하는 기본적인 문제
- DFS는 **깊이** 를 우선적으로 탐색, BFS는 **너비** 를 우선적으로 탐색
- DFS는 경로의 특징을 저장할 때 사용, BFS는 최단거리를 구할 때 사용
- DFS는 스택 또는 **재귀함수** 로 구현, BFS는 **큐(데크)** 를 이용해서 구현

#### DFS/BFS를 활용한 코드 일부

```python
def dfs(nodes, visited, node):
    visited[node] = True

    next_nodes = nodes[node]
    while next_nodes:
        next_node = heapq.heappop(next_nodes)
        if not visited[next_node]:
            print(next_node, end=' ')
            dfs(nodes, visited, next_node)
```

```python
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
```

### Union-Find Algorithm

- 두 노드가 같은 그래프에 속하는지 판별하는 알고리즘
- 노드를 합치는 Union 연산과 루트 노드를 찾는 Find 연산으로 이루어짐
- 배열에 나열된 모든 노드들은 기본적으로 자기 자신의 값을 가짐
- 노드를 합칠 때 자식 노드의 배열 값에 부모 노드의 배열 값을 넣음

#### 파이썬 구현 코드

```python
def find(graph: list, x: int) -> int:
    if graph[x] == x:
        return x
    graph[x] = find(graph, graph[x])

def union(graph: list, x: int, y: int) -> None:
    x = find(graph, x)
    y = find(graph, y)
    if x == y:
        return
    graph[y] = x
```

### Kruskal's Algorithm

- 가장 적은 비용으로 모든 노드를 연결하기 위해 사용하는 알고리즘 (최소 비용 신장 트리)
- 모든 간선 정보를 오름차순으로 정렬한 뒤 비용이 적은 간선부터 그래프에 포함
- 참고자료: [https://blog.naver.com/ndb796/221230994142](https://blog.naver.com/ndb796/221230994142)

#### 파이썬 구현 코드

```python
class Edge:
    def __init__(self, a: int, b: int, cost: int):
        self.parent = a
        self.child = b
        self.cost = cost

def get_parent(graph: list, x: int) -> int:
    if graph[x] == x:
        return x
    graph[x] = get_parent(graph, graph[x])

def union_parent(graph: list, a: int, b: int) -> None:
    a = get_parent(graph, a)
    b = get_parent(graph, b)
    if a < b:
        graph[b] = a
    else:
        graph[a] = b

def find(graph: list, a: int, b: int) -> int:
    a = get_parent(graph, a)
    b = get_parent(graph, b)
    if a == b:
        return True
    else:
        return False

def sort_edge(edge_list: list) -> list:
    return sorted(edge_list, key=lambda x: [x.cost, x.parent, x.child])

def union_edge(graph: list, edge_list: list) -> int:
    cost = 0
    for edge in edge_list:
        if not find(graph, edge.parent, edge.child):
            cost += edge.cost
            union_parent(graph, edge.parent, edge.child)
    return cost
```

### Prim's Algorithm

- 시작 정점을 선택한 후, 정점에 인접한 간선 중 최소 비용의 간선을 연결하여
  최소 신장 트리(MST)를 확장해가는 방식
- **Kruskal's Algorithm** 이 **비용이 가장 작은 간선부터** 다음 간선을 선택하는데 반해,
  **Prim's Algorithm** 은 **특정 정점에서부터** 다음 정점을 갱신해나가며 비용이 작은 간선을 선택
- Prim's Algorithm의 시간 복잡도는 최악의 경우 **O(E log E)**
  (while 구문에서 모든 간선에 대해 반복하고, 최소 힙 구조를 사용)
- 참고자료: [www.fun-coding.org/Chapter20-prim-live.html](http://www.fun-coding.org/Chapter20-prim-live.html)

#### 파이썬 구현 코드

```python
def prim(edge_list: list, start_node: int) -> list:
    mst = list()
    adjacent_edge_list = defaultdict(list)
    for weight, n1, n2 in edge_list:
        adjacent_edge_list[n1].append((weight, n1, n2))
        adjacent_edge_list[n1].append((weight, n2, n1))

    connected_nodes = {start_node}
    candidate_edge_list = adjacent_edge_list[start_node]
    heapq.heapify(candidate_edge_list)

    while candidate_edge_list:
        weight, n1, n2 = heapq.heappop(candidate_edge_list)
        if n2 not in connected_nodes:
            connected_nodes.add(n2)
            mst.append((weight, n1, n2))

            for edge in adjacent_edge_list[n2]:
                if edge[2] not in connected_nodes:
                    heapq.heappush(candidate_edge_list, edge)

    return mst
```

#### Prim's Algorithm 개선

- 간선이 아닌 **노드를 중심** 으로 우선순위 큐를 적용
- 노드마다 Key 값을 가지고 있고, Key 값을 우선순위 큐에 넣음
- Key 값이 0인 정점의 인접한 정점들에 대해 Key 값과 연결된 비용을 비교하여
  Key 값이 작으면 해당 정점의 Key 값을 갱신
- 개선된 Prim's Algorithm의 시간 복잡도는 **O(E log V)**
- 해당 알고리즘을 구현하기 위해 heapdict 라이브러리 사용
  (기존의 heap 내용을 업데이트하면 알아서 최소 힙의 구조로 업데이트됨)

#### 파이썬 구현 코드

```python
from heapdict import heapdict

def prim(graph: dict, start_node: int) -> (list, int):
    mst, keys, pi, total_weight = list(), heapdict(), dict(), 0

    for node in graph.keys():
        keys[node] = float('inf')
        pi[node] = None
    keys[start_node], pi[start_node] = 0, start_node

    while keys:
        current_node, current_key = keys.popitem()
        mst.append([pi[current_node], current_node, current_key])
        total_weight += current_key

        for adjacent, weight in graph[current_node].items():
            if adjacent in keys and weight < keys[adjacent]:
                keys[adjacent] = weight
                pi[adjacent] = current_node

    return mst, total_weight
```

## 연산자 오버로딩

- 연산자 오버로딩은 인스턴스 객체끼리 서로 연산을 할 수 있게 기존 연산자의 기능을 중복으로 정의하는 것
- 연산자 오버로딩의 예시

|**Method**|**Operator**|**Example**|
|---|---|---|
|\_\_add\_\_(self, other)|\+ (Binomial)|A + B, A += B|
|\_\_pos\_\_(self)|\+ (Unary)|+A|
|\_sub\_\_(self, other)|\- (Binomial)|A - B, A -= B|
|\_\_neg\_\_(self)|\- (Unary)|\-A|
|\_\_mul\_\_(self, other)|\*|A \* B, A \*= B|
|\_\_truediv\_\_(self, other)|/|A / B, A /= B|
|\_\_floordiv\_\_(self, other)|//|A // B, A //= B|
|\_\_mod\_\_(self, other)|%|A % B, A %= B|
|\_\_pow\_\_(self, other)|pow(), \*\*|pow(A, B), A \*\* B|
|\_\_eq\_\_(self, other)|\==|A == B|
|\_\_lt\_\_(self, other)|<|A < B|
|\_\_gt\_\_(self, other)|\>|A > B|
|\_\_lshift\_\_(self, other)|<<|A << B|
|\_\_rshift\_\_(self, other)|\>>|A >> B|
|\_\_and\_\_(self, other)|&|A & B, A &= B|
|\_\_xor\_\_(self, other)|^|A ^ B, A ^= B|
|\_\_or\_\_(self, other)|\||A \|B, A \|= B|
|\_\_invert\_\_(self)|~|~A|
|\_\_abs\_\_(self)|abs()|abs(A)|
