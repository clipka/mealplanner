# -*- coding: utf-8 -*-
import random
from enum import Enum
from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class Effort(BaseModel):
    preparationTime: int
    cookingTime: Optional[int]


class Ingredient(BaseModel):
    name: str
    amount: Optional[float]
    unit: Optional[str]


class Meal(BaseModel):
    source: Optional[str]
    id: int
    title: str
    description: Optional[str]
    tags: List[str]
    effort: Effort
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]


class MealFilter(BaseModel):
    tag: Optional[str] = None


class MealList:
    def get_meals(self, filters: MealFilter) -> List[Meal]: ...


class ShoppingList(BaseModel):
    id: int
    items: List[Ingredient]


class ShoppingLists:
    def get_shooping_lists() -> List[ShoppingList]: ...


class CourseType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"


class Course(BaseModel):
    day: date
    courseType: CourseType
    servings: int
    mealId: int

    class Config:
        use_enum_values = True


class MealPlan(BaseModel):
    id: int
    courses: List[Course]
    shoppingListId: int


class MealPlans:
    def get_meal_plans() -> List[MealPlan]: ...


# Use Cases


class ShowMealsUseCase:
    def __init__(self, repo: MealList):
        self.repo = repo

    def show_meals(self, filters: MealFilter) -> List[Meal]:
        meals = self.repo.get_meals(filters=filters)
        return meals


class ShowRandomMealUseCase:
    def __init__(self, repo: MealList):
        self.repo = repo

    def show_random_meals(self, num) -> List[Meal]:
        meals = self.repo.get_meals(MealFilter())
        rnd_meals = []
        rnd_list = random.sample(range(0, len(meals)), num)

        for rnd in rnd_list:
            rnd_meals.append(meals[rnd])

        return rnd_meals


class ShowMealDetailsUseCase:
    def __init__(self, repo: MealList):
        self.repo = repo

    def show_meal(self, id: int, detail: str = None) -> Meal:
        meal = self.repo.get_meal(id)
        if detail is None:
            return meal

        if detail in meal:
            return meal[detail]

        return None


class ShoppingListUseCase:
    def __init__(self, repo: MealList):
        self.repo = repo

    def get_shopping_list(self, ids: List[int]) -> ShoppingList:
        sl = ShoppingList(items=[])
        meals = self.repo.get_meals(MealFilter())

        for id in ids:
            if id > len(meals):
                return ShoppingList(items=[])

            meal = meals[id]
            for ingredient in meal.ingredients:
                _found = False
                # check if ingredient is in shoppinglist already
                # if in, just increase amount if available
                for item in sl.items:
                    if item.name == ingredient.name:
                        _found = True
                        if item.amount:
                            item.amount += ingredient.amount
                        break

                if not _found:
                    sl.items.append(ingredient)

        return sl


class ViewShoppingListsUseCase:
    def __init__(self, repo: ShoppingLists):
        self.repo = repo

    def get_shopping_lists(self) -> List[ShoppingList]:
        return self.repo.get_shopping_lists()


class ViewShoppingListUseCase:
    def __init__(self, repo: ShoppingLists):
        self.repo = repo

    def show_shopping_list(self, id: int, detail: str = None):
        shopping_lists = self.repo.get_shopping_lists()

        for shopping_list in shopping_lists:
            if id == shopping_list['id']:
                if detail is None:
                    return shopping_list
                if detail in shopping_list:
                    return shopping_list[detail]
                else:
                    return None
        return None


class AddShoppingListUseCase:
    def __init__(self, repo: ShoppingLists):
        self.repo = repo

    def add_shopping_list(self) -> ShoppingList:
        return self.repo.add_shopping_list()


class DeleteShoppingListUseCase:
    def __init__(self, repo: ShoppingLists):
        self.repo = repo

    def delete_shopping_list(self, id: int):
        return self.repo.delete_shopping_list(id)


class AddItemToShoppingListUseCase:
    def __init__(self, repo: ShoppingLists):
        self.repo = repo

    def add_item(self, id: int, item: Ingredient) -> bool:
        sl = self.repo.get_shopping_list(id)

        if sl is None:
            return False

        if len(sl.items) == 0:
            sl.items.append(item)
        else:
            _found = False
            # check if ingredient is in shoppinglist already
            # if in, just increase amount if available
            for i in sl.items:
                if i.name == item.name:
                    _found = True
                    if i.amount:
                        i.amount += i.amount

            if not _found:
                sl.items.append(item)

        self.repo.update_shopping_list(sl)

        return True


class AddMealIngredientsToShoppingListUseCase:
    def __init__(self, shopping_list_repo: ShoppingLists, meal_planner_repo: MealList):
        self.shopping_list_repo = shopping_list_repo
        self.meal_planner_repo = meal_planner_repo

    def add_meal_ingredients(self, shopping_list_id: int, meal_id: int, servings: int = -1) -> bool:
        sl = self.shopping_list_repo.get_shopping_list(shopping_list_id)
        if sl is None:
            return False

        show_meal_details_uc = ShowMealDetailsUseCase(self.meal_planner_repo)
        ingredients = show_meal_details_uc.show_meal(meal_id, "ingredients")
        if ingredients is None:
            return False

        add_item_uc = AddItemToShoppingListUseCase(self.shopping_list_repo)

        # calculate servings quotient
        servings_quotient = 1.0
        if servings != -1:
            meal_default_servings = show_meal_details_uc.show_meal(meal_id, "servings")
            servings_quotient = float(servings) / float(meal_default_servings)

        for i in ingredients:
            ingredient = Ingredient(name=i['name'])
            if 'amount' in i:
                ingredient.amount = i['amount'] * servings_quotient
            if 'unit' in i:
                ingredient.unit = i['unit']

            add_item_uc.add_item(shopping_list_id, ingredient)

        return True


class ViewMealPlansUseCase:
    def __init__(self, repo: MealPlans):
        self.repo = repo

    def get_meal_plans(self) -> List[MealPlan]:
        return self.repo.get_meal_plans()


class ViewMealPlanUseCase:
    def __init__(self, repo: MealPlans):
        self.repo = repo

    def get_meal_plan(self, id: int) -> MealPlan:
        return self.repo.get_meal_plan(id)


class AddMealPlantUseCase:
    def __init__(self, repo: MealPlans):
        self.repo = repo

    def add_meal_plan(self, courses: List[Course], shoppingListId: int) -> MealPlan:
        return self.repo.add_meal_plan(courses, shoppingListId)


class DeleteMealPlanUseCase:
    def __init__(self, repo: MealPlans):
        self.repo = repo

    def delete_meal_plan(self, id: int):
        return self.repo.delete_meal_plan(id)


class AddCourseToMealPlanUseCase:
    def __init__(self, repo: MealPlans):
        self.repo = repo

    def add_course(self, id: int, course: Course) -> bool:
        return self.repo.add_course(id, course)
