def solution(array, commands):
    answer = []
    for start,end,target in commands:
        start,end,target = start-1,end,target-1
        answer.append(sorted(array[start:end])[target])
    return answer