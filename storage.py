import uuid

from db import *


# returns the custom storage
async def get_storage(username):
    return mapped_select_query("home_storage", ["uuid", "item"], f"belongs_user = '{username}'")


# puts a storage item into the database
async def post_storage(username, item):
    return insert_query("home_storage", ["uuid", "item", "belongs_user"], [uuid.uuid4(), item, username])


# updates a storage item
async def update_storage(storage_item_uuid, new_name):
    return update_query("home_storage", "item", f"uuid = '{storage_item_uuid}'", new_name)


# deletes a storage item
async def delete_storage(storage_item_uuid):
    return delete_query("home_storage", f"uuid = '{storage_item_uuid}'")
