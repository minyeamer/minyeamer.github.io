import sys
input = sys.stdin.readline

n, m = map(int, input().split())
pokemon_list, pokemon_dict = [], {}
for i in range(n):
    pokemon = input().rstrip()
    pokemon_list.append(pokemon)
    pokemon_dict[pokemon] = i + 1
for _ in range(m):
    query = input().rstrip()
    if query.isdigit():
        print(pokemon_list[int(query)-1])
    else:
        print(pokemon_dict[query])
