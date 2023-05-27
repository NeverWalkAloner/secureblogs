from typing import Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload

from app.core.config import settings
from app.db.base import Post, PostKeys, ReadPostRequest, User, UserKeys
from app.schemas.post import PostBase, PostKey


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


async def get_post_with_keys(
    db: AsyncSession, post_id: int, user: User
) -> Post:
    statement = (
        select(Post)
        .join(Post.keys)
        .join(PostKeys.public_key)
        .filter(UserKeys.user_id == user.id)
        .options(contains_eager(Post.keys).contains_eager(PostKeys.public_key))
        .execution_options(populate_existing=True)
        .where(Post.id == post_id)
    )
    result = await db.execute(statement)
    return result.scalars().first()


async def get_post(db: AsyncSession, post_id: int) -> Post:
    statement = select(Post).where(Post.id == post_id)
    result = await db.execute(statement)
    return result.scalars().first()


async def add_read_post_request(
    db: AsyncSession, user: User, post_id: int
) -> None:
    exists_statement = select(ReadPostRequest.id).where(
        (ReadPostRequest.user_id == user.id)
        & (ReadPostRequest.post_id == post_id)
    )
    result = await db.execute(exists_statement)
    if result.scalars().first():
        return None
    public_key_statement = select(UserKeys).where(
        (UserKeys.is_revoked == False) & (UserKeys.user_id == user.id)
    )
    result = await db.execute(public_key_statement)
    if not (public_key := result.scalars().first()):
        return None
    db_read_post_request = ReadPostRequest(
        user_id=user.id,
        post_id=post_id,
        public_key=public_key,
    )
    db.add(db_read_post_request)
    await db.commit()


async def delete_read_post_request(
    db: AsyncSession, post_id: int, request_id: int
) -> None:
    exists_statement = delete(ReadPostRequest).where(
        (ReadPostRequest.id == request_id)
        & (ReadPostRequest.post_id == post_id)
    )
    await db.execute(exists_statement)
    await db.commit()


async def create_post_key(
    db: AsyncSession, post_id: int, request_id: int, post_key: PostKey
) -> PostKeys | None:
    exists_statement = select(ReadPostRequest).where(
        (ReadPostRequest.id == request_id)
        & (ReadPostRequest.post_id == post_id)
    )
    result = await db.execute(exists_statement)
    if not (post_request := result.scalars().first()):
        return None
    db_post_key = PostKeys(
        post_id=post_id,
        public_key_id=post_request.public_key_id,
        encrypted_key=post_key.encrypted_key,
    )
    db.add(db_post_key)
    return await db.commit()
