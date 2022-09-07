# 조건1: len(A) < len(B)
# 조건2: sum(A) < sum(B)
# 조건3: sorted()
from typing import List


def sum_num(args: str) -> int:
    result = 0
    for i in args:
        if i.isdigit():
            result += int(i)
    return result


def serial_number() -> None:
    serial_list = []
    for _ in range(int(input())):
        serial_list.append(input())
    serial_list.sort(key=lambda x: (len(x), sum_num(x), x))
    for i in serial_list:
        print(i)


serial_number()
