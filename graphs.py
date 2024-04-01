"""
Graphs.py
For Graph Classes
"""
from __future__ import annotations
from typing import Any
import json, pprint


def extract_recipes(data):
    check = 'times'

    with open(data, 'r') as f:
        file = json.load(f)

    lst = []
    for lines in file:
        lst.append(combine_times(lines[check]))

    time_ranges = {'0 ~ 20': [], '20 ~ 40': [], '40 ~ 60': [], '60+': []}

    for i in range(len(lst)):
        if lst[i] <= 20:
            time_ranges['0 ~ 20'].append(lst[i])
        elif lst[i] <= 40:
            time_ranges['20 ~ 40'].append(lst[i])
        elif lst[i] <= 60:
            time_ranges['40 ~ 60'].append(lst[i])
        else:
            time_ranges['60+'].append(lst[i])

    for key in time_ranges:
        time_ranges[key] = len(time_ranges[key])

    # for lines in file:
    #   if lines[check] not in lst:
    #     lst.append(lines[check])

    # for i in range(len(lst)):
    #   count = 0
    #   for lines in file:
    #     if lines[check] != {}:
    #       if lines[check] == lst[i]:
    #           count += 1
    #   lst[i] = (lst[i], count)

    # acc = 0

    # for tuple in lst:
    #   acc += tuple[1]

    return time_ranges


class _Vertex:
    """A vertex in a recepies graph, used to represent a subcategory, diffculty, serves, nutrients, times and         food.

    Each vertex represents any value

    Instance Attributes:
        - item: The data stored in this vertex, representing any value
        - kind: The type of this vertex: 'subcategory', 'difficult', 'serves', 'nutrients', 'times', 'food'.
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
            - kind in {'subcategory', 'difficult', 'serves', 'nutrients', 'times', 'food'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class _Food_Vertex(_Vertex):
    url: str
    image: str
    description: str
    review: int

    def __init__(self, item: Any, kind: str, url: str, image: str, description: str,
                 review: int) -> None:
        super().__init__(item, kind)
        self.url = url
        self.image = image
        self.description = description
        self.review = review

    def match_choices(self, choices: list[str]) -> bool:
        for choice in choices:
            if not any(v2.item == choice for v2 in self.neighbours):
                return False

        return True


class Graph:
    """A graph used to represent recepies network
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

    def add_food_vertex(self, item: Any, kind: str, url: str, image: str, description: str, review: int) -> None:
        """Add a food vertex with the given name, kind, image and review to this graph."""

        if item not in self._vertices:
            self._vertices[item] = _Food_Vertex(item, kind, url, image, description, review)

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

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'subcategory', 'difficult', 'serves', 'nutrients', 'times', 'food'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())


def combine_times(times: dict) -> int:
    prep_time = times.get('Preparation', '0')
    cooking_time = times.get('Cooking', '0')

    return calc_time(prep_time) + calc_time(cooking_time)


def calc_time(time: str) -> int:
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
    categories = ['Recipes with Animal Products',
                  'Vegan Recipes',
                  'Vegetarian Recipes',
                  'Meal-Specific Recipes',
                  'Miscellaneous']

    for category in categories:
        graph.add_vertex(category, 'subcategory')


def add_difficulties(graph: Graph) -> None:
    graph.add_vertex('Easy', 'difficult')
    graph.add_vertex('Challenging', 'difficult')


def add_serves(graph: Graph) -> None:
    graph.add_vertex('1 ~ 2', 'serves')
    graph.add_vertex('3 ~ 4', 'serves')
    graph.add_vertex('5+', 'serves')


def add_times(graph: Graph) -> None:
    graph.add_vertex('Quick (0 ~ 20 mins)', 'times')
    graph.add_vertex('Moderate (20 ~ 40 mins)', 'times')
    graph.add_vertex('Lengthy (40 ~ 60 mins)', 'times')
    graph.add_vertex('More than 1 hr', 'times')


def add_edge_category(food: str, subcategory: str, graph: Graph) -> None:
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
    if difficulty == 'Easy':
        graph.add_edge(food, 'Easy')
    else:
        graph.add_edge(food, 'Challenging')


def add_edge_serves(food: str, serves: int, graph: Graph) -> None:
    if serves < 3:
        graph.add_edge(food, '1 ~ 2')
    elif serves < 5:
        graph.add_edge(food, '3 ~ 4')
    else:
        graph.add_edge(food, '5+')


def add_edge_times(food: str, times: dict, graph: Graph) -> None:
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
    """Build a graph from the recipes file.
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


def get_food_options(graph: Graph, choices: list[str]) -> list[_Vertex]:
    foods = [v for v in self._vertices.values() if v.match_choices(choices)]
    return foods[:5]

# pprint.pprint(extract_recipes('recipes.json'))

# print(calc_time('17 hrs and 30 mins'))

# [('A challenge', 8), ('Easy', 951), ('More effort', 63)]

# g = build_graph('recipes.json')

# v1 = g._vertices['Panuozzo sandwich']

# print(v1.item)
# print(v1.url)
# print(v1.image)
# print(v1.description)
# print(v1.review)

# for u in v1.neighbours:
#   print(u.item)

# ______________________________________________________________________
# st = extract_recipes('recipes.json')
# pprint.pprint(st)

# Recipes: 1022
# Serves: 1022
# Nutrients: 545
