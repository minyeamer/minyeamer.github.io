def solution(nums):
    num = len(nums)//2
    answer = min(num,len(set(nums)))
    return answer