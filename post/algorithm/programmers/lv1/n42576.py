from collections import Counter
def solution(participant, completion):
    participant, completion = Counter(participant), Counter(completion)
    if participant.keys() == completion.keys():
        for p in participant.keys():
            if participant[p] != completion[p]:
                return p
    else:
        return (set(participant.keys()) - set(completion.keys())).pop()