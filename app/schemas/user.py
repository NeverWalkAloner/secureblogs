from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import constr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: constr(strip_whitespace=True, min_length=8)


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
