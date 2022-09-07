n, m = map(int, input().split())
deut = set()
bo = set()
for i in range(n):
    deut.add(input())
for j in range(m):
    bo.add(input())

deutbojob = sorted(list(deut & bo))

print(len(deutbojob))

for word in deutbojob:
    print(word)
