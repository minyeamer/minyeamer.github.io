n = list(map(int, input().split()))
asc = sorted(n)
desc = sorted(n, reverse=True)
if n == asc:
    print('ascending')
elif n == desc:
    print('descending')
else:
    print('mixed')
