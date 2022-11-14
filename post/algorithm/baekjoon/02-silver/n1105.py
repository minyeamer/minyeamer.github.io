eight = 0
l, r = map(int, input().split())
l_str = str(l)
r_str = str(r)
if len(l_str) != len(r_str):
    print(0)
else:
    if l_str[0] != r_str[0]:
        print(0)
    else:
        for i in range(len(l_str)):
            if l_str[i] != r_str[i]:
                break
            else:
                if l_str[i] == '8':
                    eight += 1
        print(eight)
