import uuid as uuid
from pydantic import BaseModel

from db import *
from recipeClass import Custom_Recipe


async def get_all_recipes():
    return mapped_select_query("recipe", ["id", "meal"], "True")


async def post_recipe(username, recipe: Custom_Recipe):
    return insert_query_no_columns("custom_recipes")


async def get_recipes(username):
    return mapped_select_query("custom_recipes", ["*"], f"belongs_user = '{username}")


async def update_recipe():
    return


async def delete_recipe():
    return
