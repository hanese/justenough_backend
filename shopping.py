import db
from connection_manager import User
from db import mapped_select_query, insert_query, delete_query, update_query
import uuid


# returns the shopping list
async def get_shopping(current_user: User):
    return mapped_select_query("shopping_list", ["uuid", "shopping_item"], f"belongs_user = '{current_user.username}'")


# adds an ingredient to the shopping list
async def add_shopping(current_user, ingredient):
    return insert_query("shopping_list", ["uuid", "shopping_item", "belongs_user"],
                        [uuid.uuid4(), ingredient.ingredient, current_user.username])


# deletes a shopping item
async def delete_shopping(item_uuid):
    return delete_query("shopping_list", f"uuid = '{item_uuid}'")


# updates a shopping item
async def update_shopping(item_uuid: str, new_name):
    return update_query("shopping_list", "shopping_item", f"uuid = '{item_uuid}'", new_name)
