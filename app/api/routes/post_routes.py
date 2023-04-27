from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.celery_tasks.workers import encrypt_post_content
from app.core.config import settings
from app.crud import crud_post
from app.models.users import User as UserModel
from app.schemas.post import PaginatedPosts, PostBase, PostInDBBase

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
