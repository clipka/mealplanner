# Mealplanner

A just for fun project to learn FastAPI and mechanics of API and service development.

Initial structure of the project is based on: https://github.com/zueve/rentomatic which provides a lean view on the Clean Architecture approach.


Mealplanner is a collection of food that the family enjoys eating. Goal is to create a list of recipes that can be chosen via an API. Out of this list of recipes, a shopping list can be generated to ease the weekly grocery shopping.

## Start

.\venv\Scripts\activate
uvicorn mealplanner.app:app --reload --port 8080

## Ideas backlog

- [x] Generate API to get recipes
- [x] API for a random meal
- [ ] shopping lists etc
- [ ] add interface to add new recipes
- [ ] replace json file storage with data base if it gets bigger
- [ ] create meal plan for the next x days
- [ ] add certain filter operations to chose, e.g. only vegetarian, least cooked food, certain tags etc.
- [ ] calculate amount of servings based on baselined ingredients
- [ ] ...
