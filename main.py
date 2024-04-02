
import json

import interface


def run_app():
    """
    runs the main app
    """
    print('=' * 50)
    print('FOOD MOOD')
    print('=' * 50)
    print('1. Run app')
    print('2. Add Recipe')
    temp_list = [1, 2]
    user_input = 1
    run = True
    while run:
        try:
            user_input = int(input('Enter a number (1/2): '))
            # Adjust the user input to match the list indexing (starting from 0)
            user_input = temp_list[user_input - 1]
            run = False
        except ValueError:
            print('=' * 50)
            print('FOOD MOOD')
            print('=' * 50)
            print('1. Run app')
            print('2. Add Recipe')
            print('Please enter a valid number (1/2): ')
        except IndexError:
            print('=' * 50)
            print('FOOD MOOD')
            print('=' * 50)
            print('1. Run app')
            print('2. Add Recipe')
            print('Please enter a valid number (1/2): ')
    if user_input == 1:
        interface.run_game()
    else:
        add_recipe('recipes.json')


def add_recipe_ui(filename):
    """
    User interface instance of add recipe
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    temp_dict = {'id': f'USERADDED{int(data[-1]['id'][-1]) + 1}',
                 'image': input('Enter a valid URL of the image of the recipe: '),
                 'name': input('Enter a valid name of the food: '),
                 'description': input('Enter a valid description of the food: '), 'author': '-',
                 'ratting': input('Enter a valid rating of recipe (1-5): '),
                 'ingredients': input('Enter the ingredients as a list: '),
                 'steps': input('Enter the steps as a list: '),
                 'nutrients': input('If any enter the nutrients as a dictionary, else enter {}: ')}
    url_input = input('Enter a valid URL of the recipe: ')
    temp_dict['url']: url_input
    prep_time = input('Enter the preperation time of the food (i.e. 10 mins, 1 hr and 10 mins): ')
    cook_time = input('Enter the cooking time of the food (i.e. 10 mins, 1 hr and 10 mins): ')
    temp_dict['times'] = {'Preperation': prep_time, 'Cooking': cook_time}
    temp_dict['serves'] = int(input('Enter serves: '))
    temp_dict['difficult'] = input('Enter difficulty (Easy or Challenging): ')
    temp_dict['vote_count'] = 0
    categories = ['Recipes with Animal Products',
                  'Vegan Recipes',
                  'Vegetarian Recipes',
                  'Meal-Specific Recipes',
                  'Miscellaneous']
    for i in range(len(categories)):
        print(f'{i + 1}. {categories[i]}')
    subcategory_input = int(input('Choose one subcategory above(1-5): '))
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


if __name__ == "__main__":
    run_app()
