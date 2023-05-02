from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

import connection_manager
from connection_manager import User, check_password_complexity, register_user, verify_user, get_user, get_current_user, \
    Token
from fastapi.middleware.cors import CORSMiddleware

from ingredients import add_custom_ingredient, get_all_ingredients, get_customs, CustomIngredient, Ingredient
from shopping import get_shopping, add_shopping_item

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
    return "Hello World"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/ingredients/getAll")
async def get_ingredients():
    return await get_all_ingredients()


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


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/register/")
async def register(user: User, response: Response):
    if not await check_password_complexity(user.password):
        response.status_code = 406
        return {"detail": "Password not complex enough"}
    response.headers.append("Access-Control-Allow-Origin", "https://www.justenough.server-welt.com")
    return await register_user(**user.dict())


@app.post("/api/ingredients/postCustomIngredient/")
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


@app.post("/api/shopping/postShoppingItem")
async def post_shopping_item(current_user: Annotated[User, Depends(get_current_user)], ingredient: Ingredient,response: Response):
    sql_state = await add_shopping_item(current_user, ingredient)
    if sql_state == 0:
        response.status_code = 201
    else:
        return sql_state


@app.get("/api/shopping/getShoppingItems")
async def get_shopping_items(current_user: Annotated[User, Depends(get_current_user)]):
    shopping_items = await get_shopping(current_user)
    return shopping_items
