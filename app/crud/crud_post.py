from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
