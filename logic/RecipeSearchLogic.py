import db
import pandas as pd
import re
import numpy as np

class logic:
    recipeDF = pd.DataFrame()
    recipeDBColumns = ["id", "meal", "drink_alternate", "category", "area", "instructions", "meal_thumb", "tags", "youtube", "ingredient1", "ingredient2", "ingredient3", "ingredient4", "ingredient5", "ingredient6", "ingredient7", "ingredient8", "ingredient9", "ingredient10", "ingredient11", "ingredient12", "ingredient13", "ingredient14", "ingredient15", "ingredient16", "ingredient17", "ingredient18", "ingredient19", "ingredient20", "measure1", "measure2", "measure3", "measure4", "measure5", "measure6", "measure7", "measure8", "measure9", "measure10", "measure11", "measure12", "measure13", "measure14", "measure15", "measure16", "measure17", "measure18", "measure19", "measure20", "source", "image_source", "creative_commons_confirmed", "date_modified"]
    def __init__(self):
        connection = db.connect()

        output = db.select_query("recipe", self.recipeDBColumns, "true")
        self.recipeDF = pd.DataFrame.from_dict(output)
        connection.close()

        #print(self.recipeDF)

    def getRecipes(self, ingredientList):
        d = {'id': [], 'matches': []}
        MatchesDF = pd.DataFrame(data=d)
        for recipe in self.recipeDF.iloc():
            count = 0
            id = recipe['id']
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
        #resDF.reset_index(inplace=True)
        for recipe in MatchesDF.iloc:
            newRow = self.recipeDF.loc[self.recipeDF['id'] == recipe['id']]
            test = len(newRow.columns)
            test2 = len(self.recipeDBColumns)
            resDF.loc[len(resDF)] = newRow

        return resDF

    def getIngredientsAsList(self, id:str):
        columnList = ["ingredient1", "ingredient2", "ingredient3", "ingredient4", "ingredient5", "ingredient6", "ingredient7", "ingredient8", "ingredient9", "ingredient10", "ingredient11", "ingredient12", "ingredient13", "ingredient14", "ingredient15", "ingredient16", "ingredient17", "ingredient18", "ingredient19", "ingredient20"]
        row = self.recipeDF.loc[self.recipeDF["id"] == id]
        res = []
        for i in columnList:
            if row[i].iloc[0] != "None":
                res.append(row[i].iloc[0])
            else:
                break
        return res



test = logic()
test2 = print(test.getRecipes(['butter']))
#print(test2.sort_values(by=['matches'], ascending=False))

#print(test.recipeDF.loc[test.recipeDF['id'] == '52768'])