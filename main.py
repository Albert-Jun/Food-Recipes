import json


def extract_recipes(data):
    """Extract the recipes"""
    with open(data, 'r') as f:
        file = json.load(f)
        difficulty_so_far = []
        for lines in file:
            if lines['times'] not in difficulty_so_far:
                difficulty_so_far.append(lines['times'])
        return difficulty_so_far
    # for lines in file:
    #     if lines['nutrients'] != {}:
    #         difficulty_so_far += 1
    # return difficulty_so_far
