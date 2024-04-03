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
            print('INVALID INPUT!')
    return actual_input


def run_app():
    """
    runs the main 'FOOD MOOD' app
    """
    print('=' * 50)
    print('FOOD MOOD')
    print('=' * 50)
    print('1. Run app')
    print('2. Add Recipe')
    print('3. View Recipe')
    print('4. EXIT')
    temp_list = [1, 2, 3, 4]
    user_input = valid_int_input(temp_list, 'Enter a number (1 - 4): ')
    if user_input == 1:
        interface.run_game()
    elif user_input == 2:
        add_recipe('recipes_user_added.json')
    elif user_input == 3:
        view_recipe('recipes_user_added.json')
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
    adds a custom recipe to the recipes file
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

    print()
    run_app()


def view_recipe(filename):
    """View the current user added recipes"""
    with open(filename, 'r') as f:
        data = json.load(f)

    num = 1
    for line in data:
        print(f'{num}) {line['name']}')
        num += 1

    question = f'Choose the recipe number you would like to view (1-{num-1}):'
    user_input = valid_int_input([x for x in range(1, num)], question)

    print('=' * 50)
    print(data[user_input - 1]['name'])
    print('=' * 50)
    print(f"'{data[user_input - 1]['description']}")
    print(f'Ratings: {data[user_input - 1]["rattings"]}')
    print(f'Prep Time: {data[user_input - 1]["times"]["Preparation"]}')
    print(f'Cooking Time: {data[user_input - 1]["times"]["Cooking"]}')
    print(f'Difficulty: {data[user_input - 1]["difficult"]}')
    print(f'Subcategory: {data[user_input - 1]["subcategory"]}')
    print('-' * 50)
    print()
    run_app()


if __name__ == "__main__":
    run_app()
