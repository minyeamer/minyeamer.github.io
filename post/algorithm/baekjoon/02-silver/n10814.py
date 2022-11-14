import sys
input = sys.stdin.readline

members = list()
for _ in range(int(input())):
    age, name = input().split()
    members.append((int(age),name))
for age, name in sorted(members, key=lambda x: x[0]):
    print(age, name)