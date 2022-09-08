A, B = input().split()
A = sum(map(int, list(A)))
B = sum(map(int, list(B)))
print(A * B)

# v1
# multi_sum = 0

# for a in A:
#     for b in B:
#         multi_sum += int(a) * int(b)

# print(multi_sum)
