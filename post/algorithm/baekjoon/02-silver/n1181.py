import sys
input = sys.stdin.readline

words = set()

for _ in range(int(input())):
    words.add(input().rstrip())

for word in sorted(words, key=lambda x: [len(x), x]):
    print(word)
