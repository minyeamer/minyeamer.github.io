---
layout: post
title: Big-O List
date: 2022-03-20 18:12:00 +0900
categories: [Algorithm, References]
tags: [Algorithm, Problem Solving, Python, Big-O]
---

## List

| Operation | Example | Big-O |
|:----------|:--------|:------|
| Index | l[i] | O(1) |
| Store | l[i] = 0 | O(1) |
| Length | len(l) | O(1) |
| Append | l.append(x) | O(1) |
| Pop | l.pop() | O(1) |
| Slice | l[a:b] | O(b-a) |
| Construction | list(x) | O(len(x)) |
| Check | l1 == l2 | O(len(n)) |
| Insert | l[a:b] = x | O(n) |
| Containment | x in l | O(n) |
| Copy | l.copy() | O(n) |
| Remove | l.remove() | O(n) |
| Count | l.count(x) | O(n) |
| Index | l.index(x) | O(n) |
| Pop | l.pop(i) | O(n) |
| Extreme value | min(l)/max(l) | O(n) |
| Iteration | for v in l: | O(n) |
| Reverse | l.reverse() | O(n) |
| Sort | l.sort() | O(n Log n) |
| Multiply | k \* l | O(k n) |

## Set
| Operation | Example | Big-O |
|:----------|:--------|:------|
| Length | len(s) | O(1) |
| Add | s.add(x) | O(1) |
| Containment | x in s | O(1) |
| Remove | s.remove() | O(1) |
| Pop | s.pop() | O(1) |
| Construction | set(x) | O(len(x)) |
| Check | s1 == s2 | O(len(s)) |
| Union | s + t | O(len(s)+len(t)) |
| Intersection | s & t | O(len(s)+len(t)) |
| Difference | s - t | O(len(s)+len(t)) |
| Symmetric Diff | s ^ t | O(len(s)+len(t)) |
| Iteration | for v in s: | O(n) |
| Copy | s.copy() | O(n) |

## Dictionary
| Operation | Example | Big-O |
|:----------|:--------|:------|
| Index | d[k] | O(1) |
| Store | d[k] = v | O(1) |
| Length | len(d) | O(1) |
| Pop | d.pop() | O(1) |
| View | d.keys() | O(1) |
| Construction | dict(x) | O(len(x)) |
| Iteration | for k in d: | O(n) |

## Sort
| Method | Best | Average | Worst |
|:-------|:-----|:--------|:------|
| Insertion Sort | O(n) | O(n^2) | O(n^2) |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) |
| Bubble Sort | O(n^2) | O(n^2) | O(n^2) |
| Shell Sort | O(n) | O(n^1.5) | O(n^1.5) |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Radix Sort | O(dn) | O(dn) | O(dn) |

## Search
| Method | Search | Insert | Delete |
|:-------|:-------|:-------|:-------|
| Sequential | O(n) | O(1) | O(n) |
| Binary | O(log n) | O(log n + n) | O(log n + n) |
| Binary Search Tree (Balanced) | O(log n) | O(log n) | O(log n) |
| Binary Search Tree (Left-Associative) | O(n) | O(n) | O(n) |
| Hashing (Best) | O(1) | O(1) | O(1) |
| Hashing (Worst) | O(n) | O(n) | O(n) |


## Heap
| Operation | Example | Big-O |
|:----------|:--------|:------|
| Push | heapq.heappush(heap, x) | O(log n) |
| Pop | heapq.heappop(heap) | O(log n) |
| Construction | heapq.heapify(heap) | O(n) |

## DFS/BFS
N은 노드, E는 간선일 때
- 인접 리스트: O(N+E)
- 인접 행렬: O(N^2)
