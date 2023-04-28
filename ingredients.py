import db


async def get_all_ingredients():
    ingredient_list = db.select_query("ingredient", ["ingredient"], "true")
    return ingredient_list
