# 피보나치 수열

zero = [1, 0, 1]
one = [0, 1, 1]


def fibonacci_count(num):
    length = len(zero)
    if num >= length:
        for i in range(length, num + 1):
            zero.append(zero[i - 1] + zero[i - 2])
            one.append(one[i - 1] + one[i - 2])
    print(zero[num], one[num])


for _ in range(int(input())):
    fibonacci_count(int(input()))
