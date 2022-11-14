import sys
from collections import Counter
input = sys.stdin.readline

_ = int(input())
N = sorted(map(int, input().split()))
_ = int(input())
M = map(int, input().split())
C = Counter(N)
print(' '.join(f'{C[m]}' if m in C else '0' for m in M))
