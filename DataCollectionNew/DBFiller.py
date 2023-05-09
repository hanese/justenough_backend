import db
import dataGrabber
import string

dg = dataGrabber.dataGrabber()


db.arbitrary_query("truncate recipe cascade;")
db.arbitrary_query("truncate ingredients cascade;")


def add_recipe(insertLetter):
    result = dg.convert(response=dg.getAPICall(f"search.php?f={insertLetter}"))["meals"]
    sql_list = []
    if result:
        for recipe in result:
            recipe = recipe.values()
            sql_list.append(recipe)

    for sql_recipe in sql_list:
        db.insert_query_no_columns("recipe", sql_recipe)
    return True


def add_ingredient():
    result = dg.convert(response=dg.getAPICall("list.php?i=list"))["meals"]
    sql_list = []
    if result:
        for ingredient in result:
            ingredient = ingredient.values()
            sql_list.append(ingredient)

    for sql_ingredient in sql_list:
        db.insert_query_no_columns("ingredients", sql_ingredient)
    return True


for letter in list(string.ascii_lowercase):
    add_recipe(letter)

add_ingredient()
