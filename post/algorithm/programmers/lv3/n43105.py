# Lv3. 정수 삼각형
# https://school.programmers.co.kr/learn/courses/30/lessons/43105

def solution(triangle):
    for i in range(1,len(triangle)):
        for j in range(len(triangle[i])):
            if j == 0:
                triangle[i][j] += triangle[i-1][j]
            elif j == len(triangle[i])-1:
                triangle[i][j] += triangle[i-1][j-1]
            else:
                triangle[i][j] += max(triangle[i-1][j-1],triangle[i-1][j])
    answer = max(triangle[-1])
    return answer