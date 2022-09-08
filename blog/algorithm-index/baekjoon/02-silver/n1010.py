import math


# 조합
def set_bridge() -> None:
    for _ in range(int(input())):
        n, m = map(int, input().split())
        print(math.comb(m, n))
