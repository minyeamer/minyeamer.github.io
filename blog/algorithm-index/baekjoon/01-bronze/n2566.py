table = []
for _ in range(9):
    table.append(list(map(int, input().split())))

nums = dict()
for i in range(9):
    for j in range(9):
        nums[table[i][j]] = (i+1,j+1)

max_num = max(nums)
print(max_num)
print(nums[max_num][0], nums[max_num][1])