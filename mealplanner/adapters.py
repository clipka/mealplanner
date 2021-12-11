# -*- coding: utf-8 -*-
import os
import json
from typing import List
from mealplanner import services as s


class JsonStorage(s.MealPlanner):

    def __init__(self):
        print(f"cwd: {os.getcwd()}")
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
