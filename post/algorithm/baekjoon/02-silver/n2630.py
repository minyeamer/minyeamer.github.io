import sys
input = sys.stdin.readline

N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
answer = [0, 0]

def quad_comp(n, arr, r, c, answer):
    start = arr[r][c]
    for row in range(r,r+n):
        for col in range(c,c+n):
            if arr[row][col] != start:
                div = n//2
                for i in range(2):
                    for j in range(2):
                        quad_comp(div, arr, r+div*i, c+div*j, answer)
                return
    answer[start] += 1

quad_comp(N, arr, 0, 0, answer)

for num in answer:
    print(num)