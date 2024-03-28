import json

def extract_recipes(data):
    with open(data, 'r') as f:
        file = json.load(f)
    difficulty_so_far = set()
    for lines in file:
        if lines['rattings'] not in difficulty_so_far:
            difficulty_so_far.add(lines['rattings'])
    return difficulty_so_far
