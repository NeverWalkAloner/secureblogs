from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserGroupBase(BaseModel):
    name: str


class UserGroupInDBBase(UserGroupBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
