# -*- coding: utf-8 -*-
import random
from typing import Optional, List
from pydantic import BaseModel


class Effort(BaseModel):
    preparationTime: int
    cookingTime: Optional[int]


class Ingredient(BaseModel):
    name: str
    amount: Optional[int]
    unit: Optional[str]


class Meal(BaseModel):
    source: Optional[str]
    title: str
    description: Optional[str]
    tags: List[str]
    effort: Effort
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]


class MealFilter(BaseModel):
    tag: Optional[str] = None


class MealPlanner:
    def get_meals(self, filters: MealFilter) -> List[Meal]: ...


class ShowMealsUseCase:
    def __init__(self, repo: MealPlanner):
        self.repo = repo

    def show_meals(self, filters: MealFilter) -> List[Meal]:
        meals = self.repo.get_meals(filters=filters)
        return meals


class ShowRandomMealUseCase:
    def __init__(self, repo: MealPlanner):
        self.repo = repo

    def show_random_meals(self, num) -> List[Meal]:
        meals = self.repo.get_meals(MealFilter())
        rnd_meals = []
        rnd_list = random.sample(range(0, len(meals)), num)

        for rnd in rnd_list:
            rnd_meals.append(meals[rnd])

        return rnd_meals
