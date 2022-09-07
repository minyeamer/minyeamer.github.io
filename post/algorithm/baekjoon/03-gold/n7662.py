import heapq
import sys
input = sys.stdin.readline

for T in range(int(input())):
    min_Q, max_Q = [], []
    valid, ins = {}, 0

    for k in range(int(input())):
        cmd, n = input().split()

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

    if ins > 0:
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
    else:
        print('EMPTY')
