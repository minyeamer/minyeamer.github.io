n, m = map(int, input().split())
set, one = [], []
for i in range(m):
    a, b = map(int, input().split())
    set.append(a)
    one.append(b)
lowest_set = min(set)
lowest_one = min(one)
if lowest_one * 6 < lowest_set:
    price = n * lowest_one
else:
    price = n // 6 * lowest_set
    n = n % 6
    if n * lowest_one < lowest_set:
        price += n * lowest_one
    else:
        price += lowest_set
print(price)
