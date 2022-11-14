from collections import Counter
import sys

input = sys.stdin.readline

N = int(input())
nums = [int(input()) for _ in range(N)]
nums.sort()

# 1
print(round(sum(nums) / N))

# 2
print(nums[N // 2])

# 3
C = Counter(nums).most_common(2)
most = C[0]
if most[1] < N and most[1] == C[1][1]:
    print(C[1][0])
else:
    print(most[0])

# 4
print(nums[-1] - nums[0])
