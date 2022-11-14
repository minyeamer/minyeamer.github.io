import itertools

N = input()
int_N = int(N)
count, first = len(N), int(N[0])
M = int(input())
if M == 10:
    print(abs(int_N-100))
else:
    buttons = set([str(i) for i in range(10)])
    channels = {N,}
    diff = {abs(int_N-100)}
    if M > 0:
        buttons -= set(list(input().split()))
        channels = set()
        for i in range(1, count+1):
            product = itertools.product(buttons, repeat=i)
            channels |= set(map(''.join, product))

        min_chan, max_chan = '0', '1'
        for _ in range(count-1):
            min_chan += max(buttons)
        for _ in range(count):
            max_chan += min(buttons)
        if set(max_chan) & buttons == set(max_chan):
            channels.add(max_chan)
        if set(min_chan) & buttons == set(min_chan):
            channels.add(min_chan)

    if min(diff) <= count+1:
        print(min(diff))
    else:
        if N in channels:
            print(count)
        else:
            for channel in channels:
                if len(channel) > 1 and channel[0] == '0':
                    channel = str(int(channel))
                diff.add(abs(int_N-int(channel))+len(channel))
            print(min(diff))
