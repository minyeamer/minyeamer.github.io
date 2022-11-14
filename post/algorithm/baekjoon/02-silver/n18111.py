import sys
from collections import Counter

input = sys.stdin.readline

N, M, B = map(int, input().split())
C = Counter()
for _ in range(N):
    C += Counter(map(int, input().split()))
T, H = sys.maxsize, 0
keys = list(C.keys())

for h in range(257):
    t = 0
    op1, op2 = 0, 0

    for k in keys:
        if k < h:
            op2 += C[k] * (h-k)
        elif k > h:
            op1 += C[k] * (k-h)

    if op2 > op1 + B:
        continue
    else:
        t = op1 * 2 + op2

    if t < T:
        T, H = t, h
    elif t == T and h > H:
        H = h

print(T, H)
