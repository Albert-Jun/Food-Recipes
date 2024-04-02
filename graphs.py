"""
Graphs.py
For Graph Classes
"""
from __future__ import annotations
from typing import Any
import json


class _Vertex:
    """A vertex in a recipes graph, used to represent a subcategory, diffculty, serves, times and food.

    Each vertex represents any value

    Instance Attributes:
        - item: The data stored in this vertex, representing any value
        - kind: The type of this vertex: 'subcategory', 'difficult', 'serves', 'times', 'food'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'subcategory', 'difficult', 'serves', 'nutrients', 'times', 'food'}
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'subcategory', 'difficult', 'serves', 'times'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def match_choices(self, choices: list[str]) -> bool:
        """Return whether the food matches the choices. choices is a list of user inputs that describe the food.
        This function returns true if the food vertex matches the given choices.
        """
        if self.kind != 'food':
            return False

        for choice in choices:
            if not any(v2.item == choice for v2 in self.neighbours):
                return False
        return True


class _FoodVertex(_Vertex):
    """A vertex in a recipes graph of kind 'food'.

    Instance Attributes:
        - item: The name of the food, represented by a string
        - kind: The type of this vertex: 'food'
        - neighbours: The vertices that are adjacent to this vertex.
        - url: the url of the website the recipe is on, rerpesented by a string
        - image: the url of the image of the recipe, represented by a string
        - description: the food description, represented by a string
        - rating: the rating of the food given by the user, represented as an integer

    Representation Invariants:
        - self.kind == 'food'
        - 0 <= self.rating <= 5

    """
    url: str
    image: str
    description: str
    rating: int

    def __init__(self, item: Any, kind: str, url: str, image: str, description: str,
                 rating: int) -> None:
        """Initialize a new vertex with the given item, kind, url, image, description and rating.

        This vertex is initialized with no neighbours. (It uses the _Vertex class initializer for item, kind).

        Preconditions:
            - kind == 'food'
        """
        super().__init__(item, kind)
        self.url = url
        self.image = image
        self.description = description
        self.rating = rating


class Graph:
    """A graph used to represent recipes network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'subcategory', 'difficult', 'serves', 'nutrients', 'times'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_food_vertex(self, item: Any, kind: str, url: str, image: str, description: str, rating: int) -> None:
        """Add a food vertex with the given name, kind, url, image, description and rating to this graph."""

        if item not in self._vertices:
            self._vertices[item] = _FoodVertex(item, kind, url, image, description, rating)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_food_options(self, choices: list[str]) -> list[_Vertex]:
        """Return a list of food vertices from graph based on the given choices.
        The list is sorted based on rating (highest to lowest).
        If there are more than 10 only return the 10 highest rated
        """
        foods = [v for v in self._vertices.values() if v.match_choices(choices)]

        # Ssrt the food vertices based on their rating attribute in descending order
        foods.sort(key=lambda v: v.rating, reverse=True)

        # Return the top 10 food vertices with highest ratings
        return foods[:10]


def combine_times(times: dict) -> int:
    """
    Given a dictionary that maps Preparation and/or Cooking to their times,
    returns the combined times as an integer of minutes.

    Preconditions:
        - 'Preparation' in times or 'Cooking' in times
    """
    prep_time = times.get('Preparation', '0')
    cooking_time = times.get('Cooking', '0')

    return calc_time(prep_time) + calc_time(cooking_time)


def calc_time(time: str) -> int:
    """
    Given a string of time (ex. 4 hrs and 30 minutes), returns the number of minutes as an integer.
    If given a range such as 20 minutes - 40 minutes, it takes the longest option.
    """
    if 'No Time' in time:
        return 0

    if '-' in time:
        time = time.split(' - ')[-1]

    if 'and' in time:
        hrs, mins = time.split(' and ')[0], time.split(' and ')[1]
        total_mins = 60 * int(hrs.split()[0]) + int(mins.split()[0])
        return total_mins

    if 'hr' in time:
        return int(time.split()[0]) * 60

    return int(time.split()[0])


def add_categories(graph: Graph) -> None:
    """Add all the subcategory vertices to the given graph."""
    categories = ['Recipes with Animal Products',
                  'Vegan Recipes',
                  'Vegetarian Recipes',
                  'Meal-Specific Recipes',
                  'Miscellaneous']

    for category in categories:
        graph.add_vertex(category, 'subcategory')


def add_difficulties(graph: Graph) -> None:
    """Add all the difficulty vertices to the given graph."""
    graph.add_vertex('Easy', 'difficult')
    graph.add_vertex('Challenging', 'difficult')


def add_serves(graph: Graph) -> None:
    """Add all the serves vertices to the given graph."""
    graph.add_vertex('1 ~ 2', 'serves')
    graph.add_vertex('3 ~ 4', 'serves')
    graph.add_vertex('5+', 'serves')


def add_times(graph: Graph) -> None:
    """Add all the times vertices to the given graph."""
    graph.add_vertex('Quick (0 ~ 20 mins)', 'times')
    graph.add_vertex('Moderate (20 ~ 40 mins)', 'times')
    graph.add_vertex('Lengthy (40 ~ 60 mins)', 'times')
    graph.add_vertex('More than 1 hr', 'times')


def add_edge_category(food: str, subcategory: str, graph: Graph) -> None:
    """Add an edge between the food vertex and the correct subcategory vertex in the given graph."""
    sub_to_main = {'Chicken': 'Recipes with Animal Products',
                   'Fish and seafood': 'Recipes with Animal Products',
                   'Meat': 'Recipes with Animal Products',
                   'Pasta': 'Recipes with Animal Products',
                   'Cheese recipes': 'Vegetarian Recipes',
                   'Vegetarian': 'Vegetarian Recipes',
                   'Vegan': 'Vegan Recipes',
                   'Breakfast recipes': 'Meal-Specific Recipes',
                   'Lunch recipes': 'Meal-Specific Recipes',
                   'Dinner recipes': 'Meal-Specific Recipes',
                   'Storecupboard': 'Miscellaneous',
                   'Desserts': 'Miscellaneous'}
    graph.add_edge(food, sub_to_main[subcategory])


def add_edge_difficulty(food: str, difficulty: str, graph: Graph) -> None:
    """Add an edge between the food vertex and the correct difficulty vertex in the given graph."""
    if difficulty == 'Easy':
        graph.add_edge(food, 'Easy')
    else:
        graph.add_edge(food, 'Challenging')


def add_edge_serves(food: str, serves: int, graph: Graph) -> None:
    """Add an edge between the food vertex and the correct serves vertex in the given graph."""
    if serves < 3:
        graph.add_edge(food, '1 ~ 2')
    elif serves < 5:
        graph.add_edge(food, '3 ~ 4')
    else:
        graph.add_edge(food, '5+')


def add_edge_times(food: str, times: dict, graph: Graph) -> None:
    """Add an edge between the food vertex and the correct times vertex in the given graph."""
    combined_times = combine_times(times)
    if combined_times <= 20:
        graph.add_edge(food, 'Quick (0 ~ 20 mins)')
    elif combined_times <= 40:
        graph.add_edge(food, 'Moderate (20 ~ 40 mins)')
    elif combined_times <= 60:
        graph.add_edge(food, 'Lengthy (40 ~ 60 mins)')
    else:
        graph.add_edge(food, 'More than 1 hr')


def build_graph(recipes_file: str) -> Graph:
    """Build a recipe graph using the given recipes file.
    """

    g = Graph()

    with open(recipes_file, 'r') as f:
        file = json.load(f)

        # add option vertices
        add_categories(g)
        add_difficulties(g)
        add_serves(g)
        add_times(g)

        for line in file:
            # add the food vertex
            g.add_food_vertex(line['name'], 'food', line['url'], line['image'], line['description'], line['rattings'])

            # create edge between food and option
            add_edge_category(line['name'], line['subcategory'], g)
            add_edge_difficulty(line['name'], line['difficult'], g)
            add_edge_serves(line['name'], line['serves'], g)
            add_edge_times(line['name'], line['times'], g)

    return g


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['json'],
        'allowed-io': ['build_graph'],
        'max-line-length': 120
    })
