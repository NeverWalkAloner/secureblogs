from typing import Optional

from pydantic import BaseModel


# Shared properties
class PostBase(BaseModel):
    title: str
    content: str
    group_id: int


class PostInDBBase(PostBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
