from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.config import settings
from app.db.base import Post, User
from app.schemas.post import PostBase


async def create_post(db: AsyncSession, post: PostBase, author: User) -> Post:
    db_post = Post(
        title=post.title,
        content=post.content,
        group_id=post.group_id,
        author=author,
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def get_posts_list(
    db: AsyncSession, page: int, user_group: Optional[int]
) -> list[Post]:
    max_per_page = settings.MAX_PER_PAGE
    offset = (page - 1) * max_per_page
    statement = (
        select(Post)
        .options(joinedload(Post.keys))
        .limit(max_per_page)
        .offset(offset)
        .order_by(Post.id.desc())
    )
    if user_group:
        statement = statement.where(Post.group_id == user_group)
    result = await db.execute(statement)
    return result.scalars().unique().all()


async def get_posts_count(
    db: AsyncSession, user_group: Optional[int]
) -> list[Post]:
    statement = select(func.count(Post.id))
    if user_group:
        statement = statement.where(Post.group_id == user_group)
    result = await db.execute(statement)
    return result.scalar()
