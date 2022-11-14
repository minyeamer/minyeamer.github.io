import sys
input = sys.stdin.readline

K, N = map(int, input().split())
k = [int(input()) for _ in range(K)]
mn, md, mx = 0, 0, max(k)+1

while mn < mx:
    md = (mx + mn) // 2
    count = 0
    for i in range(K):
        count += k[i] // md
    if count < N:
        mx = md
    else:
        mn = md + 1
print(mn - 1)
