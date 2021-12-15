# -*- coding: utf-8 -*-

from typing import List, Optional
from fastapi import FastAPI, Depends, Path, HTTPException
from starlette.responses import Response
from mealplanner import services
from storage import adapters


app = FastAPI()

# use cases ##


def get_use_case() -> services.ShowMealsUseCase:
    return services.ShowMealsUseCase(adapters.JsonStorage())


def get_meal_use_case() -> services.ShowMealDetailsUseCase:
    return services.ShowMealDetailsUseCase(adapters.JsonStorage())


def get_random_use_case() -> services.ShowRandomMealUseCase:
    return services.ShowRandomMealUseCase(adapters.JsonStorage())


def get_shopping_lists_use_case() -> services.ViewShoppingListsUseCase:
    return services.ViewShoppingListsUseCase(adapters.JsonShoppingListStorage())


def add_shopping_list_use_case() -> services.AddShoppingListUseCase:
    return services.AddShoppingListUseCase(adapters.JsonShoppingListStorage())


def get_shopping_list_use_case() -> services.ViewShoppingListUseCase:
    return services.ViewShoppingListUseCase(adapters.JsonShoppingListStorage())


def delete_shopping_list_use_case() -> services.DeleteShoppingListUseCase:
    return services.DeleteShoppingListUseCase(adapters.JsonShoppingListStorage())

# API ##


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


@app.get("/shopping_lists", response_model=List[services.ShoppingList])
def get_shopping_lists(use_case=Depends(get_shopping_lists_use_case)):
    return use_case.get_shopping_lists()


@app.post("/shopping_lists", response_model=services.ShoppingList)
def add_shopping_list(meals: List[int], use_case=Depends(add_shopping_list_use_case)):
    return use_case.add_shopping_list()


@app.get("/shopping_lists/{id}", response_model=services.ShoppingList)
def get_shopping_list(id: int = Path(..., ge=0), use_case=Depends(get_shopping_list_use_case)):
    shopping_list = use_case.show_shopping_list(id)

    if shopping_list is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return use_case.show_shopping_list(id)


@app.get("/shopping_lists/{id}/{detail}")
def get_shopping_lists_detail(id: int = Path(..., ge=0),
                              detail: str = Path(..., ne=None),
                              use_case=Depends(get_shopping_list_use_case)):
    shopping_list = use_case.show_shopping_list(id, detail)

    if shopping_list is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return use_case.show_shopping_list(id, detail)


@app.delete("/shopping_lists/{id}", status_code=204, response_class=Response)
def delete_shopping_list(id: int = Path(..., ge=0),
                         use_case=Depends(delete_shopping_list_use_case)):
    ok = use_case.delete_shopping_list(id)

    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")

    return
