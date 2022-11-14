# Lv.1 소수 만들기
# https://school.programmers.co.kr/learn/courses/30/lessons/12977

from itertools import combinations

def solution(nums):
    comb = map(sum, combinations(nums,3))
    is_prime = lambda x: all(x%i for i in range(2, int(x**0.5)+1))
    answer = sum(map(is_prime, comb))
    return answer