from pydantic import BaseModel, EmailStr, PositiveInt, Field
from typing import Union

class User(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Union[PositiveInt, None] = Field(default=None, lt=130)
    is_subscribed: bool = False

class LoginData(BaseModel):
    username: str
    password: str