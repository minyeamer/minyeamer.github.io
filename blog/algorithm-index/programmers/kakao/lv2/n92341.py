# Lv.2 주차 요금 계산
# https://programmers.co.kr/learn/courses/30/lessons/92341

from math import ceil
from collections import defaultdict

def solution(fees, records):
    park_dict, time_dict = dict(), defaultdict(int)

    for record in records:
        time, car, stat = record.split()
        time = list(map(int,time.split(':')))
        if stat == 'IN':
            park_dict[car] = time
        else:
            delta = timedelta(park_dict[car],time)
            time_dict[car] += delta
            del park_dict[car]

    for car, time in park_dict.items():
        delta = timedelta(park_dict[car],[23,59])
        time_dict[car] += delta

    park = sorted(time_dict.items())
    return [fees[1]+int(ceil((fee-fees[0])/fees[2]))*fees[3]
            if fee-fees[0] > 0 else fees[1] for car,fee in park]

def timedelta(start, end):
    hourdelta, minutedelta = end[0]-start[0], end[1]-start[1]
    if minutedelta < 0:
        hourdelta, minutedelta = hourdelta-1, minutedelta+60
    return hourdelta*60 + minutedelta