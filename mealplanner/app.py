# -*- coding: utf-8 -*-

from typing import List, Optional
from fastapi import FastAPI, Depends
from mealplanner import adapters, services


app = FastAPI()


def get_use_case() -> services.ShowMealsUseCase:
    return services.ShowMealsUseCase(adapters.JsonStorage())


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


@app.get("/random_meals", response_model=List[services.Meal])
def get_random_meals(num: Optional[int] = None,
                     use_case=Depends(get_random_use_case)):
    if num is None:
        num = 1

    return use_case.show_random_meals(num)
