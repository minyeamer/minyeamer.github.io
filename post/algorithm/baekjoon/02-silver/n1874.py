import sys
input = sys.stdin.readline

n = int(input())
s = []
op = []
count = 1
no = False
for i in range(n):
    num = int(input())
    while count <= num:
        s.append(count)
        op.append('+')
        count += 1
    if s[-1] == num:
        s.pop()
        op.append('-')
    else:
        no = True
if no:
    print('NO')
else:
    for i in op:
        print(i)
