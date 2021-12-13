# -*- coding: utf-8 -*-

from typing import List, Optional
from fastapi import FastAPI, Depends, Path, HTTPException
from fastapi.param_functions import Query
from mealplanner import adapters, services


app = FastAPI()


def get_use_case() -> services.ShowMealsUseCase:
    return services.ShowMealsUseCase(adapters.JsonStorage())


def get_meal_use_case() -> services.ShowMealDetailsUseCase:
    return services.ShowMealDetailsUseCase(adapters.JsonStorage())


def get_random_use_case() -> services.ShowRandomMealUseCase:
    return services.ShowRandomMealUseCase(adapters.JsonStorage())


def get_shopping_list_use_case() -> services.ShoppingListUseCase:
    return services.ShoppingListUseCase(adapters.JsonStorage())


@app.post("/meals", response_model=List[services.Meal])
def meals(filters: services.MealFilter, use_case=Depends(get_use_case)):
    return use_case.show_meals(filters)


@app.get("/meals", response_model=List[services.Meal])
def get_meals(tag: Optional[str] = None, use_case=Depends(get_use_case)):
    mf = services.MealFilter()

    if tag:
        mf.tag = tag

    return use_case.show_meals(mf)


@app.get("/meals/{id}", response_model=services.Meal)
def get_meal(id: int = Path(..., ge=0), use_case=Depends(get_meal_use_case)):
    meal = use_case.show_meal(id)

    if meal is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return use_case.show_meal(id)


@app.get("/meals/{id}/{detail}")
def get_meal_detail(id: int = Path(..., ge=0),
                    detail: str = Path(..., ne=None),
                    use_case=Depends(get_meal_use_case)):
    meal = use_case.show_meal(id, detail)

    if meal is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return use_case.show_meal(id, detail)


@app.get("/random_meals", response_model=List[services.Meal])
def get_random_meals(num: Optional[int] = None,
                     use_case=Depends(get_random_use_case)):
    if num is None:
        num = 1

    return use_case.show_random_meals(num)


@app.get("/shopping_list", response_model=services.ShoppingList)
def get_shopping_list(meals: List[int] = Query(None), use_case=Depends(get_shopping_list_use_case)):
    if not meals:
        raise HTTPException(status_code=400, detail="At least one meal id must be provided")
    for m in meals:
        if m < 0:
            raise HTTPException(status_code=404, detail="One or multiple ids < 0")

    sl = use_case.get_shopping_list(meals)

    if len(sl.items) == 0:
        raise HTTPException(status_code=404, detail="One or multiple ids not found")

    return sl
