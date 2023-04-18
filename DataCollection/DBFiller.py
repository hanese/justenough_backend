import db
import dataGrabber

recipeIdCounter = 0

ingredientIdCounter = 0

dg = dataGrabber.dataGrabber()

db.arbitrary_query("truncate recipe cascade;")
db.arbitrary_query("truncate recipe_ingredients cascade;")


def add_recipe(name: str):
    result = dg.convert(response=dg.getAPICall(name))[0]
    if result != "Could not find Recipe":
        global recipeIdCounter
        recipeIdCounter += 1
        db.connect()
        db.insert_query("recipe", ["id", "name", "instructions", "servings"],
                        [recipeIdCounter, result['title'].replace("'", "''"), result['instructions'].replace("'", "''"), result['servings']])
        add_recipe_ingredients(result['ingredients'], recipeIdCounter)
        result = "successfully added recipe"
    return result


def add_recipe_ingredients(ingredients: str, recipeId: int):
    global ingredientIdCounter
    ingredientList = ingredients.split('|')
    db.connect()
    for ingredient in ingredientList:
        ingredientIdCounter += 1
        db.insert_query("recipe_ingredients", ["recipe_id", "id", "text"], [recipeId, ingredientIdCounter, ingredient])


def process_list():
    recipeList = []
    with open("../recipeNames.txt", "r") as f:
        recipeList = f.readlines()

    f = open("../processOutput.txt", "w")

    if len(recipeList) > 0:
        for i in recipeList:
            result = add_recipe(i.strip())
            if result == "Could not find Recipe":
                f.write(f"Could not find recipe for: {i} \n")

    f.close()


process_list()
