def solution(clothes):
    answer = 1
    types = [type for cloth,type in clothes]
    counts = [types.count(type) for type in set(types)]
    for count in counts:
        answer *= count + 1
    return answer - 1