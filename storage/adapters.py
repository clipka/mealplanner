# -*- coding: utf-8 -*-
import os
import json
from typing import List
from mealplanner import services as s


class JsonStorage(s.MealPlanner):

    def __init__(self):
        with open(os.path.join("data", "recipes.json"), 'r', encoding='utf-8') as file:
            content = file.read()
        data = json.loads(content)
        self._storage = data['recipes']

    def get_meals(self, filters: s.MealFilter) -> List[s.Meal]:
        result = []
        for m in self._storage:
            meal = s.Meal.parse_raw(json.dumps(m))
            if filters.tag is None or filters.tag in meal.tags:
                result.append(meal)

        return result

    def get_meal(self, id) -> s.Meal:
        if id > len(self._storage):
            return None
        return self._storage[id]


class JsonShoppingListStorage(s.ShoppingLists):

    def __init__(self):
        with open(os.path.join("data", "shopping_lists.json"), 'r', encoding='utf-8') as file:
            content = file.read()
        if content:
            data = json.loads(content)
            self._storage = data['shoppingLists']
        else:
            self._storage = []

    def get_shopping_lists(self) -> List[s.ShoppingList]:
        return self._storage

    def add_shopping_list(self) -> s.ShoppingList:
        if len(self._storage) == 0:
            id = 0
        else:
            id = self._storage[len(self._storage)-1]['id'] + 1

        sl = s.ShoppingList(id=id, items=[])
        self._storage.append(sl.dict())

        with open(os.path.join("data", "shopping_lists.json"), 'w', encoding='utf-8') as file:
            data = {}
            data["$schema"] = "./shopping_lists_schema.json",
            data["shoppingLists"] = self._storage
            file.write(json.dumps(data, indent=4))
        return sl

    def delete_shopping_list(self, id: int) -> bool:
        for shopping_list in self._storage:
            if id == shopping_list['id']:
                self._storage.remove(shopping_list)
                with open(os.path.join("data", "shopping_lists.json"),
                          'w',
                          encoding='utf-8') as file:
                    data = {}
                    data["$schema"] = "./shopping_lists_schema.json",
                    data["shoppingLists"] = self._storage
                    file.write(json.dumps(data, indent=4))
                return True
        return False

    def get_shopping_list(self, id: int) -> s.ShoppingList:
        for shopping_list in self._storage:
            if id == shopping_list['id']:
                return s.ShoppingList(id=shopping_list['id'], items=shopping_list['items'])

        return None

    def update_shopping_list(self, shopping_list: s.ShoppingList) -> bool:
        for sl in self._storage:
            if sl['id'] == shopping_list.id:
                sl['items'] = []
                for item in shopping_list.items:
                    sl['items'].append(item.dict())

                with open(os.path.join("data", "shopping_lists.json"),
                          'w',
                          encoding='utf-8') as file:
                    data = {}
                    data["$schema"] = "./shopping_lists_schema.json",
                    data["shoppingLists"] = self._storage
                    file.write(json.dumps(data, indent=4))

                return True

        return False