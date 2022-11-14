def solution(brown, yellow):
    s = brown+yellow
    for h in range(3,s//2+1):
        w = s//h
        if w*h != s:
            continue
        y = (w-2)*(h-2)
        if y==yellow:
            return [w,h]