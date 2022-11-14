def solution(citations):
    citations = sorted(citations)
    for i,citation in enumerate(citations):
        if citation >= len(citations)-i:
            return len(citations)-i
    return 0