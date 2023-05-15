import os
from datetime import datetime, timedelta
from typing import Annotated
import re
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import db
from db import connect
import psycopg2.errors

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv("hash_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def register_user(username: str, password: str):
    password = pwd_context.hash(password)
    with connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO users VALUES (%s, %s)",
                            (username, password))
            except psycopg2.errors.UniqueViolation:
                raise HTTPException(status_code=409, detail="username already exists")


async def verify_user(username: str, password: str):
    res = db.select_query("SELECT password FROM users WHERE username = %s", (username,))
    if not res:
        return False
    res = res[0]
    return pwd_context.verify(password, res[0])


async def check_password_complexity(password: str):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    password: str


app = FastAPI()


def get_expiry(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expiry = payload.get("exp")
    return datetime.utcfromtimestamp(expiry)


def get_user(username: str):
    user = db.select_query("SELECT username, password from users where username = %s", (username,))
    if user:
        return User(**dict(username=user[0][0], password=user[0][1]))
    return False


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
