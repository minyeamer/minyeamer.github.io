import heapq
import sys
from collections import deque

input = sys.stdin.readline

for _ in range(int(input())):
    N, M = map(int, input().split())
    priority = list(map(int, input().split()))
    current_Q = [(chr(65+i), (i+1, priority[i])) for i in range(N)]
    current_deque = deque(current_Q)
    priority = [-p for p in priority]
    heapq.heapify(priority)
    printer_Q = []
    for _ in range(N):
        max_priority = -heapq.heappop(priority)
        while current_deque[0][1][1] < max_priority:
            current_deque.append(current_deque.popleft())
        printer_Q.append(current_deque.popleft())
    print(printer_Q.index(current_Q[M])+1)
