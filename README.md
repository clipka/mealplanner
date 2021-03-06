# Mealplanner

A just for fun project to learn FastAPI and mechanics of API and service development.

Initial structure of the project is based on: https://github.com/zueve/rentomatic which provides a lean view on the Clean Architecture approach.
The frontend is build with React based on the NetNinja Youtube tutorial (https://www.youtube.com/watch?v=j942wKiXFu8&list=PL4cUxeGkcC9gZD-Tvwfod2gaISzfRiP9d)

Mealplanner is a collection of food that the family enjoys eating. Goal is to create a list of recipes that can be chosen via an API. Out of this list of recipes, a shopping list can be generated to ease the weekly grocery shopping.


## Initiate

Create python virtual environment and install required packages

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Start

Start the service

```
.\venv\Scripts\activate
uvicorn mealplanner.app:app --reload --port 8080
```

Open browser and go to ```http://127.0.0.1:8080/meals```

## Ideas backlog

- [x] Generate API to get recipes
- [x] API for a random meal
- [x] add and show shopping lists
- [x] delete shopping lists
- [x] add items to shopping list by meal id
- [x] add specific item to shopping list
- [ ] add interface to add new recipes
- [ ] replace json file storage with data base if it gets bigger
- [ ] create meal plan for the next x days
- [ ] add certain filter operations to choose, e.g. only vegetarian, certain tags etc.
- [ ] add filter for least cooked food
- [ ] calculate amount of servings based on baselined ingredients
- [ ] connect Alexa to meal planner to tell what to cook today
- [ ] ...

## TODO

- [ ] Dependency Injection

Due to the way I use Depends() to integrate use cases, I initiate storage models before using them.
Therefore, I cannot create a shopping list and add items to it in the same invocation. That needs to be fixed.
