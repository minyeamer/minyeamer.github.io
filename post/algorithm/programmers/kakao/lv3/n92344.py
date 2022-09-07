# Lv.3 파괴되지 않은 건물
# https://programmers.co.kr/learn/courses/30/lessons/92344
# 누적합 활용

import numpy as np

def solution(board, skill):
    board = np.array(board)
    acc = np.zeros((len(board)+1,len(board[0])+1))
    type_dict = {1:-1, 2:1}
    for t, r1, c1, r2, c2, n in skill:
        acc[r1,c1] += n*type_dict[t]
        acc[r1,c2+1] += n*type_dict[t]*-1
        acc[r2+1,c1] += n*type_dict[t]*-1
        acc[r2+1,c2+1] += n*type_dict[t]

    acc = acc[:len(board),:len(board[0])].cumsum(axis=1).cumsum(axis=0)
    return np.count_nonzero(board+acc > 0)
