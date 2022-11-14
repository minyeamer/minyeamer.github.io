import sys
input = sys.stdin.readline

nodes = list()
for _ in range(int(input())):
    nodes.append(tuple(map(int,input().split())))
for x,y in sorted(nodes, key=lambda x: [x[1],x[0]]):
    print(x,y)