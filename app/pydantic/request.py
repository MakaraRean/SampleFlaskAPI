import datetime
from typing import Union

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    qty: int
    price: float
    createdAt: datetime.datetime = datetime.datetime.now()
    category_id: int


class Category(BaseModel):
    name: str
    createAt: datetime.datetime


class User(BaseModel):
    username: str = "makara"
    password: str = "123"

class Token(BaseModel):
    access_token: str = ""
    token_type: str

class RefreshToken(BaseModel):
    refresh: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    password: str

