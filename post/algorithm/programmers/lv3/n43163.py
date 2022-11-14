from collections import deque

def check_words(query, key):
    diff = sum([q!=k for q,k in zip(query,key)])
    return diff == 1

def solution(begin, target, words):
    if target not in words:
        return 0

    q = deque()
    q.append([begin, 0])

    while q:
        word, depth = q.popleft()

        for change in words:
            if check_words(word, change):
                if change == target:
                    return depth+1
                else:
                    q.append([change, depth+1])