import uuid as uuid
from pydantic import BaseModel

from db import *
from recipeClass import Custom_Recipe


# returns all recipes with id and the name
async def get_recipes():
    return mapped_select_query("recipe", ["id", "meal"], "True")


# returns a full recipe by id
async def get_full_recipe(recipe_id: str):
    if not recipe_id.__contains__("-"):
        return mapped_select_query("recipe", list(dict(Custom_Recipe()).keys()), f"id = {recipe_id}")
    elif recipe_id.__contains__("-"):
        return mapped_select_query("custom_recipes", list(dict(Custom_Recipe()).keys()), f"uuid = '{recipe_id}'")
    else:
        return None


# returns custom recipes by username
async def get_recipes_by_username(username):
    return mapped_select_query("custom_recipes", ["uuid", "meal"], f"belongs_user = '{username}'")


# posts a custom recipe into the database
async def post_recipe(username, recipe: Custom_Recipe):
    return insert_query("custom_recipes", ["uuid"] + list(dict(recipe).keys()) + ["belongs_user"], [uuid.uuid4()] + list(dict(recipe).values()) + [username])


# updates a custom recipe in the database
async def update_recipe(recipe_uuid, column, updated_value):
    return update_query("custom_recipes", column, f"uuid = '{recipe_uuid}'", updated_value)


# deletes a custom recipe in the database
async def delete_recipe(custom_recipe_uuid: str):
    return delete_query("custom_recipes", f"uuid = '{custom_recipe_uuid}'")
