# -*- coding: utf-8 -*-

from typing import List, Optional
from fastapi import FastAPI, Depends, Path, HTTPException, Body
from starlette.responses import Response
from mealplanner import services
from storage import adapters


app = FastAPI()

# use cases ##


def get_use_case() -> services.ShowMealsUseCase:
    return services.ShowMealsUseCase(adapters.JsonMealListStorage())


def get_meal_use_case() -> services.ShowMealDetailsUseCase:
    return services.ShowMealDetailsUseCase(adapters.JsonMealListStorage())


def get_random_use_case() -> services.ShowRandomMealUseCase:
    return services.ShowRandomMealUseCase(adapters.JsonMealListStorage())


def get_shopping_lists_use_case() -> services.ViewShoppingListsUseCase:
    return services.ViewShoppingListsUseCase(adapters.JsonShoppingListStorage())


def add_shopping_list_use_case() -> services.AddShoppingListUseCase:
    return services.AddShoppingListUseCase(adapters.JsonShoppingListStorage())


def get_shopping_list_use_case() -> services.ViewShoppingListUseCase:
    return services.ViewShoppingListUseCase(adapters.JsonShoppingListStorage())


def delete_shopping_list_use_case() -> services.DeleteShoppingListUseCase:
    return services.DeleteShoppingListUseCase(adapters.JsonShoppingListStorage())


def add_item_to_shopping_list_use_case() -> services.AddItemToShoppingListUseCase:
    return services.AddItemToShoppingListUseCase(adapters.JsonShoppingListStorage())


def add_meal_ingredients_to_shopping_list_use_case() -> services.AddMealIngredientsToShoppingListUseCase:
    return services.AddMealIngredientsToShoppingListUseCase(adapters.JsonShoppingListStorage(),
                                                            adapters.JsonMealListStorage())


def view_meal_plans_use_case() -> services.ViewMealPlansUseCase:
    return services.ViewMealPlansUseCase(adapters.JsonMealPlanStorage())


def get_meal_plan_use_case() -> services.ViewMealPlanUseCase:
    return services.ViewMealPlanUseCase(adapters.JsonMealPlanStorage())


def add_meal_plan_use_case() -> services.AddMealPlantUseCase:
    return services.AddMealPlantUseCase(adapters.JsonMealPlanStorage())


def delete_meal_plan_use_case() -> services.DeleteMealPlanUseCase:
    return services.DeleteMealPlanUseCase(adapters.JsonMealPlanStorage())

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


@app.post("/shopping_lists/{id}/add_item", status_code=200, response_class=Response)
def add_item_to_shopping_list(id: int = Path(..., ge=0),
                              item: services.Ingredient = Body(..., ne=None),
                              use_case=Depends(add_item_to_shopping_list_use_case)):
    ok = use_case.add_item(id, item)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")

    return


@app.post("/shopping_lists/{id}/add_meal", status_code=200, response_class=Response)
def add_meal_to_shopping_list(id: int = Path(..., ge=0),
                              meal_id: int = Body(..., ge=0),
                              use_case=Depends(add_meal_ingredients_to_shopping_list_use_case)):
    ok = use_case.add_meal_ingredients(id, meal_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")

    return


@app.get("/meal_plans", response_model=List[services.MealPlan])
def get_meal_plans(use_case=Depends(view_meal_plans_use_case)):
    return use_case.get_meal_plans()


@app.get("/meal_plans/{id}", response_model=services.MealPlan)
def get_meal_plan(id: int = Path(..., ge=0), use_case=Depends(get_meal_plan_use_case)):
    meal_plan = use_case.get_meal_plan(id)

    if meal_plan is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return use_case.get_meal_plan(id)


@app.post("/meal_plans", response_model=services.MealPlan)
def add_meal_plan(courses: List[services.Course] = Body(default=[]),
                  shoppingListId: int = Body(default=-1),
                  add_meal_plan_use_case=Depends(add_meal_plan_use_case),
                  add_shoppling_list_use_case=Depends(add_shopping_list_use_case),
                  get_shopping_list_use_case=Depends(get_shopping_list_use_case),
                  add_meal_integrients_use_case=Depends(add_meal_ingredients_to_shopping_list_use_case)):

    shopping_list = get_shopping_list_use_case.show_shopping_list(shoppingListId)
    if shopping_list is None:
        return HTTPException(status_code=404, detail=f"shopping list id {shoppingListId} not found.")

    meal_plan = add_meal_plan_use_case.add_meal_plan(courses, shoppingListId)

    # add courses meals to shopping list
    for course in meal_plan.courses:
        add_meal_integrients_use_case.add_meal_ingredients(shoppingListId, course.mealId, course.servings)

    return meal_plan


@app.delete("/meal_plans/{id}", status_code=204, response_class=Response)
def delete_meal_plan(id: int = Path(..., ge=0),
                     use_case=Depends(delete_meal_plan_use_case)):
    ok = use_case.delete_meal_plan(id)

    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")

    return
