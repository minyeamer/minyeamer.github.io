# 파이썬 알고리즘 풀이에 유용한 함수 모음

# 문자열 내 숫자의 합
from typing import List


def sum_of_num(args: str) -> int:
    result = 0
    for i in args:
        if i.isdigit():
            result += int(i)
    return result


# 소인수 분해
def prime_factorialization(args: int) -> List:
    result = [i for i in range(args+1)]
    num = 2
    while args != 1:
        if args % num == 0:
            result[num] += 1
            args //= num
        else:
            num += 1
    return result
