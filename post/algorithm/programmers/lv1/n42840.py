def solution(answers):
    pts = [
        [1,2,3,4,5],
        [2,1,2,3,2,4,2,5],
        [3,3,1,1,2,2,4,4,5,5]
    ]
    scores = [0,0,0]
    for i in range(len(answers)):
        for j in range(3):
            if answers[i] == pts[j][i%len(pts[j])]:
                scores[j] += 1
    mx = max(scores)
    answers = [i for i,s in enumerate(scores, start=1) if s==mx]
    return answers