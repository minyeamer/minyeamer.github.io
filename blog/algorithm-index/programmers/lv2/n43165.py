def solution(numbers, target):
    answer = 0
    leaves = [0]
    for num in numbers:
        curr = []
        for parent in leaves:
            curr.append(parent + num)
            curr.append(parent - num)
        leaves = curr
    for leaf in leaves:
        if leaf == target:
            answer += 1
    return answer