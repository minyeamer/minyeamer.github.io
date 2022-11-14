import sys
input = sys.stdin.readline

N = int(input())
P = sorted(map(int, input().split()))
mn = 0
for i in range(N):
    mn += sum(P[:i+1])
print(mn)
