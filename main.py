import json

def extract_recipes(data):
    with open(data, 'r') as f:
        file = json.load(f)
    difficulty_so_far = set()
    max_so_far = 0
    for lines in file:
        if len(lines['name']) > max_so_far:
            difficulty_so_far.add(lines['name'])
            max_so_far = len(lines['name'])
            print(lines['name'])
    return difficulty_so_far

def get_food(data):
    with open(data, 'r') as f:
        file = json.load(f)
    temp_list = []
    for i in range(len(file)):
        temp_list.append(file[i])

    return temp_list


food_reccommended = get_food('recipes_small.json')
