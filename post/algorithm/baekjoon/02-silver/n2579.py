import sys
input = sys.stdin.readline

N = int(input())
s = list()
dp = [0] * N
for _ in range(N):
    s.append(int(input()))

if N < 3:
    print(sum(s))
else:
    dp[0] = s[0]
    dp[1] = max(s[0]+s[1],s[1])
    dp[2] = max(s[0]+s[2],s[1]+s[2])
    for i in range(3,N):
        dp[i] = max(dp[i-2]+s[i],dp[i-3]+s[i]+s[i-1])
    print(dp[N-1])