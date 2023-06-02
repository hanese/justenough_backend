from db import *
import pandas as pd
import re


class custom_recipe_logic:
    recipeDF = pd.DataFrame()
    recipeDBColumns = ["uuid", "meal", "category", "area", "instructions", "meal_thumb", "tags",
                       "youtube", "ingredient1", "ingredient2", "ingredient3", "ingredient4", "ingredient5",
                       "ingredient6", "ingredient7", "ingredient8", "ingredient9", "ingredient10", "ingredient11",
                       "ingredient12", "ingredient13", "ingredient14", "ingredient15", "ingredient16", "ingredient17",
                       "ingredient18", "ingredient19", "ingredient20", "measure1", "measure2", "measure3", "measure4",
                       "measure5", "measure6", "measure7", "measure8", "measure9", "measure10", "measure11",
                       "measure12", "measure13", "measure14", "measure15", "measure16", "measure17", "measure18",
                       "measure19", "measure20", "source", "image_source", "creative_commons_confirmed",
                       "date_modified"]

    def __init__(self, username):

        output = mapped_select_query("custom_recipes", self.recipeDBColumns + ["belongs_user"],
                                     f"belongs_user = '{username}'")
        self.recipeDF = pd.DataFrame.from_dict(output)

    # use dataframes to return the recipes
    def getRecipes(self, ingredientList):
        d = {'uuid': [], 'matches': []}
        MatchesDF = pd.DataFrame(data=d)
        for recipe in self.recipeDF.iloc():
            count = 0
            id = recipe['uuid']
            recipeIngredientList = self.getIngredientsAsList(id)

            for recipeIngredient in recipeIngredientList:
                for ingredient in ingredientList:
                    if re.search(ingredient, recipeIngredient):
                        count += 1

            rowToAdd = [id, count]
            MatchesDF.loc[len(MatchesDF)] = rowToAdd

        MatchesDF = MatchesDF[MatchesDF['matches'] > 0]
        MatchesDF.sort_values(by=['matches'], ascending=False, inplace=True)

        resDF = pd.DataFrame(columns=self.recipeDBColumns)
        for recipe in MatchesDF.iloc:
            newRow = self.recipeDF.loc[self.recipeDF['uuid'] == recipe['uuid']]
            resDF = pd.concat([resDF, newRow], ignore_index=True)

        return resDF

    # returns the ingredients as a list
    def getIngredientsAsList(self, id: str):
        columnList = ["ingredient1", "ingredient2", "ingredient3", "ingredient4", "ingredient5", "ingredient6",
                      "ingredient7", "ingredient8", "ingredient9", "ingredient10", "ingredient11", "ingredient12",
                      "ingredient13", "ingredient14", "ingredient15", "ingredient16", "ingredient17", "ingredient18",
                      "ingredient19", "ingredient20"]
        row = self.recipeDF.loc[self.recipeDF["uuid"] == id]
        res = []
        for i in columnList:
            if row[i].iloc[0] != "None":
                res.append(row[i].iloc[0])
            else:
                break
        return res


"""
USAGE:
test = logic()
test2 = test.getRecipes(['butter'])
print(test2.iloc[0])
"""
