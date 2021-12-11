# -*- coding: utf-8 -*-

from typing import List, Optional
from fastapi import FastAPI, Depends, Path, HTTPException
from mealplanner import adapters, services


app = FastAPI()


def get_use_case() -> services.ShowMealsUseCase:
    return services.ShowMealsUseCase(adapters.JsonStorage())


def get_meal_use_case() -> services.ShowMealDetailsUseCase:
    return services.ShowMealDetailsUseCase(adapters.JsonStorage())


def get_random_use_case() -> services.ShowRandomMealUseCase:
    return services.ShowRandomMealUseCase(adapters.JsonStorage())


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


@app.get("/random_meals", response_model=List[services.Meal])
def get_random_meals(num: Optional[int] = None,
                     use_case=Depends(get_random_use_case)):
    if num is None:
        num = 1

    return use_case.show_random_meals(num)
