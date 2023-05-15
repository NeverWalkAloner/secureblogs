from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.celery_tasks.workers import encrypt_post_content
from app.core.config import settings
from app.crud import crud_post
from app.models.users import User as UserModel
from app.schemas.post import (
    PaginatedPosts,
    PostBase,
    PostDetails,
    PostInDBBase,
)

router = APIRouter()


@router.post("/posts/", response_model=PostInDBBase, status_code=201)
async def create_post(
    post: PostBase,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    plain_content = post.content
    post.content = ""
    post = await crud_post.create_post(
        db=db,
        post=post,
        author=current_user,
    )
    encrypt_post_content.delay(post_id=post.id, content=plain_content)
    return post


@router.get("/posts/", response_model=PaginatedPosts)
async def get_posts(
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    user_group: Optional[int] = None,
):
    posts = await crud_post.get_posts_list(db, page, user_group)
    posts_count = await crud_post.get_posts_count(db, user_group)
    return PaginatedPosts(
        total_count=posts_count, per_page=settings.MAX_PER_PAGE, posts=posts
    )


@router.get("/posts/{post_id}/", response_model=PostDetails)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await crud_post.get_post(db, post_id, current_user)
    if not post:
        raise HTTPException(status_code=404)
    return post


@router.post("/posts/{post_id}/request_read/", status_code=204)
async def add_read_post_request(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    await crud_post.add_read_post_request(db, current_user, post_id)
