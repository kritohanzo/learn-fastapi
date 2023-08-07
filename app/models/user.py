from pydantic import BaseModel, EmailStr, PositiveInt, Field


class User(BaseModel):
    id: int
    name: str
    age: int

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False