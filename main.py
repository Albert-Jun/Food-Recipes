"""
This Python module runs the "FOOD MOOD" application, which allows users to interact with a recipe reccomender system.
Users can run the app, add recipes, view recipes, and exit the application.

Copyright and Usage Information
===============================

This file is Copyright (c) Aref Malekanian, Albert Jun, Ahnaf Keenan Ardhito, Alfizza Kenaz
"""

import json
import interface


def valid_int_input(expected_int: list, input_quest: str):
    """
    Checks if the expected input is found
    """
    run = True
    actual_input = None
    while run:
        try:
            actual_input = int(input(f'{input_quest}'))
            if actual_input not in expected_int:
                raise ValueError
            run = False
        except ValueError:
            print(f'{input_quest}')
            print('INVALID INPUT!')
    return actual_input


def run_app():
    """
    runs the main 'FOOD MOOD' app
    """
    print('=' * 50)
    print('FOOD MOOD')
    print('=' * 50)
    print('1. Run App')
    print('2. Add Recipe')
    print('3. View Recipe')
    print('4. EXIT')
    temp_list = [1, 2, 3, 4]
    user_input = valid_int_input(temp_list, 'Enter a number (1 - 4): ')
    if user_input == 1:
        interface.run_game()
    elif user_input == 2:
        add_recipe('recipe_book')
    elif user_input == 3:
        view_recipe('recipe_book')
    else:
        return None


def add_recipe_ui(filename):
    """
    User interface instance of add recipe.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    temp_dict = {'id': f'USERADDED{int(data[-1]['id'][-1]) + 1}', 'name': input('Enter a valid name of the food: '),
                 'description': input('Enter a valid description of the food: '), 'author': '-',
                 'rattings': valid_int_input([1, 2, 3, 4, 5], 'Enter a valid rating of recipe (1-5): ')}
    prep_time = input('Enter the preparation time of the food (i.e. 10 mins, 1 hr and 10 mins): ')
    cook_time = input('Enter the cooking time of the food (i.e. 10 mins, 1 hr and 10 mins): ')
    temp_dict['times'] = {'Preparation': prep_time, 'Cooking': cook_time}
    serves = ['1 ~ 2 Serves', '2 ~ 4 Serves', '5+ Serves']
    for i in range(len(serves)):
        print(f'{i + 1}. {serves[i]}')
    temp_dict['serves'] = valid_int_input([1, 2, 3], 'Choose one that applies(1 - 3): ')
    difficulty = ['Easy', 'Challenging']
    for i in range(len(difficulty)):
        print(f'{i + 1}. {difficulty[i]}')
    difficulty_input = valid_int_input([1, 2], 'Choose difficulty(1/2): ')
    temp_dict['difficult'] = difficulty_input
    temp_dict['vote_count'] = 0
    categories = ['Recipes with Animal Products',
                  'Vegan Recipes',
                  'Vegetarian Recipes',
                  'Meal-Specific Recipes',
                  'Miscellaneous']
    for i in range(len(categories)):
        print(f'{i + 1}. {categories[i]}')
    subcategory_input = valid_int_input([1, 2, 3, 4, 5], 'Choose one subcategory above(1-5): ')
    temp_dict['subcategory'] = categories[subcategory_input - 1]
    temp_dict['dish_type'] = categories[subcategory_input - 1]
    temp_dict['maincategory'] = 'recipes'

    return temp_dict


def add_recipe(filename):
    """
    This function adds a custom recipe to the recipes file

    It asks the user to input the name, description, url of the website that has the recipe,
    rating, prep / cook time, number of serves, difficulty and category of the recipe and writes it
    into the recipe book txt file.
    """
    try:
        # Try to open the existing file and load its contents
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_data = []
    data = add_recipe_ui(filename)
    # Add the new data to the existing data
    existing_data.append(data)

    # Save the updated data back to the JSON file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)
    run_app()


def view_recipe(filename):
    """View the current user added recipes"""
    with open(filename, 'r') as f:
        data = json.load(f)
    for lines in data:
        print('=' * 50)
        print(lines['name'])
        print('=' * 50)
        print(f"'{lines['description']}")
        print(f'Ratings: {lines["rattings"]}')
        print(f'Prep Time: {lines["times"]["Preparation"]}')
        print(f'Cooking Time: {lines["times"]["Cooking"]}')
        print(f'Difficulty: {lines["difficult"]}')
        print(f'Subcategory: {lines["subcategory"]}')
        print('-' * 50)
    run_app()


if __name__ == "__main__":
    run_app()
