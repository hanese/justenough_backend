from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Query
from fastapi.security import OAuth2PasswordRequestForm

import connection_manager
from connection_manager import User, check_password_complexity, register_user, verify_user, get_user, get_current_user, \
    Token
from fastapi.middleware.cors import CORSMiddleware

from ingredients import *
from shopping import *
from storage import *
from recipes import *
from recipe_logic import *

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Welcome in the JustEnough-World"


@app.get("/api/ingredients/getAll")
async def get_all_ingredients():
    return await get_ingredients()


@app.get("/api/recipes/getAll")
async def get_all_recipes():
    return await get_recipes()


@app.get("/api/recipes/getRecipe/{recipe_id}")
async def get_recipe_by_id(recipe_id: str):
    return await get_full_recipe(recipe_id)


@app.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if not await verify_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=connection_manager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = connection_manager.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/register")
async def register(user: User, response: Response):
    if not await check_password_complexity(user.password):
        response.status_code = 406
        return {"detail": "Password not complex enough"}
    response.headers.append("Access-Control-Allow-Origin", "https://www.justenough.server-welt.com")
    return await register_user(**user.dict())


@app.post("/api/ingredients/postCustomIngredient")
async def post_custom_ingredient(current_user: Annotated[User, Depends(get_current_user)], custom: Ingredient,
                                 response: Response):
    sql_state = await add_custom_ingredient(current_user, custom)
    if sql_state == 0:
        response.status_code = 201
    else:
        return sql_state


@app.get("/api/ingredients/getCustomIngredients")
async def get_custom_ingredients(current_user: Annotated[User, Depends(get_current_user)]):
    custom_ingredients = await get_customs(current_user)
    return custom_ingredients


@app.delete("/api/ingredients/deleteCustomIngredient/{uuid}")
async def delete_custom_ingredient(current_user: Annotated[User, Depends(get_current_user)], uuid: str):
    sql_state = await delete_custom(uuid)
    return sql_state


@app.put("/api/ingredients/updateCustomIngredient/{CustomIngredientUuid}")
async def update_custom_ingredient(current_user: Annotated[User, Depends(get_current_user)], custom_ingredient_uuid: str, new_name: str):
    sql_state = await update_custom(custom_ingredient_uuid, new_name)
    return sql_state


@app.post("/api/shopping/postShoppingItem")
async def post_shopping_item(current_user: Annotated[User, Depends(get_current_user)], ingredient: Ingredient,response: Response):
    sql_state = await add_shopping(current_user, ingredient)
    if sql_state == 0:
        response.status_code = 201
    else:
        return sql_state


@app.get("/api/shopping/getShoppingItems")
async def get_shopping_items(current_user: Annotated[User, Depends(get_current_user)]):
    shopping_items = await get_shopping(current_user)
    return shopping_items


@app.delete("/api/shopping/deleteShoppingItem/{uuid}")
async def delete_shopping_item(current_user: Annotated[User, Depends(get_current_user)], uuid: str):
    sql_state = await delete_shopping(uuid)
    return sql_state


@app.put("/api/shopping/updateShoppingItem/{shoppingItemUuid}")
async def update_shopping_item(current_user: Annotated[User, Depends(get_current_user)], shopping_item_uuid: str, new_name: str):
    sql_state = await update_shopping(shopping_item_uuid, new_name)
    return sql_state


@app.post("/api/storage/postStorageItem")
async def post_storage_item(current_user: Annotated[User, Depends(get_current_user)], item: Ingredient):
    sql_state = await post_storage(current_user.username, item.ingredient)
    return sql_state


@app.get("/api/storage/getStorage")
async def get_home_storage(current_user: Annotated[User, Depends(get_current_user)]):
    sql_state = await get_storage(current_user.username)
    return sql_state


@app.put("/api/storage/updateItem/{storageItemUuid}")
async def update_storage_item(current_user: Annotated[User, Depends(get_current_user)], storage_item_uuid: str, new_name: str):
    sql_state = await update_storage(storage_item_uuid, new_name)
    return sql_state


@app.delete("/api/storage/deleteItem/{storageItemUuid}")
async def delete_storage_item(current_user: Annotated[User, Depends(get_current_user)], storage_item_uuid: str):
    sql_state = await delete_shopping(storage_item_uuid)
    return sql_state


@app.post("/api/recipes/postCustomRecipe")
async def post_custom_recipe(current_user: Annotated[User, Depends(get_current_user)], recipe: Custom_Recipe):
    sql_state = await post_recipe(current_user.username, recipe)
    return sql_state


@app.get("/api/recipes/getCustomRecipes")
async def get_custom_recipes(current_user: Annotated[User, Depends(get_current_user)]):
    custom_recipes = await get_recipes_by_username(current_user.username)
    return custom_recipes


@app.put("/api/recipes/updateRecipe/{recipeUuid}")
async def update_custom_recipe(current_user: Annotated[User, Depends(get_current_user)], recipe_uuid: str, column: str, updated_value: str):
    sql_state = await update_recipe(recipe_uuid, column, updated_value)
    return sql_state


@app.delete("/api/recipes/deleteRecipe/{recipeUuid}")
async def delete_custom_recipe(current_user: Annotated[User, Depends(get_current_user)], recipe_uuid: str):
    sql_state = await delete_recipe(recipe_uuid)
    return sql_state


@app.get("/api/recipes/getRecipesByIngredients/")
async def get_recipes_by_ingredients(ingredients: Annotated[list, Query()]):
    recipeList = []
    df = logic().getRecipes(ingredients)
    for i in range(len(df)):
        recipeList.append(df.iloc[i])
    return recipeList
