# 합병 정렬
from typing import List


def merge_sort(unsorted_list: List) -> List:
    unsorted_list_length = len(unsorted_list)

    if unsorted_list_length <= 1:
        return unsorted_list

    mid = unsorted_list_length // 2
    left = merge_sort(unsorted_list[:mid])
    right = merge_sort(unsorted_list[mid:])
    merged_list = merge(left, right)
    return merged_list


def merge(left: List, right: List) -> List:
    merged_list = []

    while len(left) > 0 and len(right) > 0:
        if left[0] <= right[0]:
            merged_list.append(left.pop(0))
        else:
            merged_list.append(right.pop(0))

    if len(left) > 0:
        merged_list += left
    if len(right) > 0:
        merged_list += right

    return merged_list


print(merge_sort([123, 234, 567, 768, 432]))
