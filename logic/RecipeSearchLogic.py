import db
import pandas as pd

class logic:
    recipeDF = pd.DataFrame()
    def __init__(self):
        connection = db.connect()
        output = db.select_query("recipe", ["id", "name", "instructions", "servings"], "true")
        print(type())
        connection.close()

    def getRecipes(ingredientList):
        for i in ingredientList:
            print("hi")


test = logic()
