from collections import deque
import sys
input = sys.stdin.readline

queue = deque()
for _ in range(int(input())):
    cmd = input().split()
    try:
        if cmd[0] == 'push_front':
            queue.appendleft(int(cmd[1]))
        elif cmd[0] == 'push_back':
            queue.append(int(cmd[1]))
        elif cmd[0] == 'pop_front':
            print(queue.popleft())
        elif cmd[0] == 'pop_back':
            print(queue.pop())
        elif cmd[0] == 'size':
            print(len(queue))
        elif cmd[0] == 'empty':
            print(int(len(queue)==0))
        elif cmd[0] == 'front':
            print(queue[0])
        elif cmd[0] == 'back':
            print(queue[-1])
    except:
        print(-1)