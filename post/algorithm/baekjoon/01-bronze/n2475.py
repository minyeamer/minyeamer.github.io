n = list(map(int, input().split()))
v = 0
for i in n:
    v += i ** 2
print(v % 10)
