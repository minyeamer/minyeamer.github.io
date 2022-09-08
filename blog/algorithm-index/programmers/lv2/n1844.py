from collections import deque

def solution(maps):
    n, m = len(maps), len(maps[0])
    visited = [[False] * m for _ in range(n)]
    dist = {(0,0): 0}
    q = deque()
    q.append((0,0))

    dx = [-1,0,1,0]
    dy = [0,1,0,-1]

    while q:
        y, x = q.popleft()
        for i in range(4):
            ny, nx = y+dy[i], x+dx[i]
            if 0<=ny<n and 0<=nx<m and not visited[ny][nx] and maps[ny][nx]:
                if ny==n-1 and nx==m-1:
                    return dist[(y, x)]+2
                q.append((ny,nx))
                dist[(ny,nx)] = dist[(y,x)]+1
                visited[ny][nx] = True

    return -1