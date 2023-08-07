from pydantic import BaseModel


class Calculate(BaseModel):
    num1: int
    num2: int