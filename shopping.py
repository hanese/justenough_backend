from connection_manager import User
from db import mapped_select_query, insert_query, delete_query
import uuid


async def get_shopping(current_user: User):
    return mapped_select_query("shopping_list", ["uuid", "shopping_item"], f"belongs_user = '{current_user.username}'")


async def add_shopping_item(current_user, ingredient):
    return insert_query("shopping_list", ["uuid", "shopping_item", "belongs_user"],
                        [uuid.uuid4(), ingredient.ingredient, current_user.username])


async def delete_item(item_uuid):
    return delete_query("shopping_list", f"uuid = '{item_uuid}'")
