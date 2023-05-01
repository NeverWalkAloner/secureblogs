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


class PaginatedPosts(BaseModel):
    total_count: int
    per_page: int
    posts: list[PostInDBBase]


class PostKeyInDB(BaseModel):
    encrypted_key: str

    class Config:
        orm_mode = True


class PostDetails(PostInDBBase):
    keys: list[PostKeyInDB] | None
