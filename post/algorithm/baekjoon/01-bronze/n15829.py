L = int(input())
print(sum([(ord(s)-96)*31**i for i,s in enumerate(input())])%1234567891)