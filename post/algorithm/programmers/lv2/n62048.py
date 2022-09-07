# Lv.2 멀쩡한 사각형
# https://school.programmers.co.kr/learn/courses/30/lessons/62048

def gcd(x,y):
    while(y):
        x,y = y, x%y
    return x

def solution(w,h):
    answer = w*h - (w+h-gcd(w,h))    
    return answer