N, K = map(int, input().split())
idx = 0

arr = list(range(1,N+1))
answer = list()
while arr:
    idx = (idx + K-1) % len(arr)
    answer.append(str(arr.pop(idx)))
print(f'<{", ".join(answer)}>')