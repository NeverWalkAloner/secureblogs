from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator
from pydantic.types import constr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    """Return response data"""

    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """Convert UUID to pure hex string"""
        return value.hex


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: constr(strip_whitespace=True, min_length=8)


class Login(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8)


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    token: TokenBase | None = None
