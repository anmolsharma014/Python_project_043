import requests

class Recipe:
    def __init__(self, name, category, area, instructions, ingredients):
        self.name = name
        self.category = category
        self.area = area
        self.instructions = instructions
        self.ingredients = ingredients

    def display(self):
        print(f"\n🍽️ Recipe: {self.name}")
        print(f"Category: {self.category}")
        print(f"Area: {self.area}")
        print("\nInstructions:")
        print(self.instructions)
        print("\nIngredients:")
        for ing in self.ingredients:
            print(" -", ing)

def search_recipes_by_ingredient(ingredient):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    params = {"i": ingredient}

    response = requests.get(url, params=params)
    data = response.json()

    if data["meals"] is None:
        print("No recipes found for ingredient:", ingredient)
        return []

    return data["meals"]  

def get_recipe_details(meal_id):
    url = "https://www.themealdb.com/api/json/v1/1/lookup.php"
    params = {"i": meal_id}

    response = requests.get(url, params=params)
    data = response.json()["meals"][0]

    ingredients = []
    for i in range(1, 21):
        ingredient = data.get(f"strIngredient{i}")
        measure = data.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append(f"{ingredient} - {measure}")

    recipe = Recipe(
        name=data["strMeal"],
        category=data["strCategory"],
        area=data["strArea"],
        instructions=data["strInstructions"],
        ingredients=ingredients
    )
    return recipe

if __name__ == "__main__":
    ingredient = input("Enter ingredient to search recipes: ")

    meals = search_recipes_by_ingredient(ingredient)

    if not meals:
        exit()

    print("\nRecipes Found:")
    for index, meal in enumerate(meals, start=1):
        print(f"{index}. {meal['strMeal']}")

    choice = int(input("\nSelect a recipe number to view details: "))
    selected_meal = meals[choice - 1]

    recipe = get_recipe_details(selected_meal["idMeal"])
    recipe.display()
