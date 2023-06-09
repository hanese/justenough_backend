import uuid
from typing import Coroutine

from pydantic import BaseModel
from starlette.requests import Request

import db
from db import mapped_select_query, select_query, insert_query, delete_query, update_query
from connection_manager import User


class CustomIngredient(BaseModel):
    ingredient: str
    uuid: str


class Ingredient(BaseModel):
    ingredient: str


# performs sql and returns the result or the error code
async def get_ingredients():
    ingredient_list = mapped_select_query("ingredients", ["id", "ingredient", "description", "type"], "True")
    return ingredient_list


# performs sql and returns the result or the error code
async def add_custom_ingredient(current_user: User, ingredient: Ingredient):
    return insert_query("custom_ingredients", ["ingredient", "uuid", "belongs_user"],
                        [ingredient.ingredient, uuid.uuid4(), current_user.username])


# performs sql and returns the result or the error code
async def get_customs(current_user: User):
    customs = mapped_select_query("custom_ingredients", ["uuid", "ingredient", "belongs_user"],
                                  f"belongs_user = '{current_user.username}'")
    return customs


# performs sql and returns the result or the error code
async def delete_custom(uuid_custom: str):
    return delete_query("custom_ingredients", f"uuid = '{uuid_custom}'")


# performs sql and returns the result or the error code
async def update_custom(uuid_custom: str, new_name):
    return update_query("custom_ingredients", "ingredient", f"uuid = '{uuid_custom}'", new_name)
