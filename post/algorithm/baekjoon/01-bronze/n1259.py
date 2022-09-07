import sys
input = sys.stdin.readline

while True:
    word = input().rstrip()
    num = int(word)
    if not num:
        break
    if num == int(word[::-1]):
        print('yes')
    else:
        print('no')
