import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline


def search_adjacent(arg, x, y):
    if arg[y][x]:
        arg[y][x] = 0
        if x > 0 and arg[y][x-1]:
            search_adjacent(arg, x-1, y)
        if x < len(arg[y])-1 and arg[y][x+1]:
            search_adjacent(arg, x+1, y)
        if y > 0 and arg[y-1][x]:
            search_adjacent(arg, x, y-1)
        if y < len(arg)-1 and arg[y+1][x]:
            search_adjacent(arg, x, y+1)
        return 1
    else:
        return 0


for T in range(int(input())):
    M, N, K = map(int, input().split())
    field = [[0 for _ in range(M)] for _ in range(N)]
    count = 0
    for _ in range(K):
        X, Y = map(int, input().split())
        field[Y][X] = 1
    for n in range(N):
        for m in range(M):
            count += search_adjacent(field, m, n)
    print(count)
