from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import User, UserGroup
from app.schemas.user_group import UserGroupBase


async def create_user_group(
    db: AsyncSession, user: User, user_group: UserGroupBase
) -> UserGroup:
    db_user_group = UserGroup(
        name=user_group.name,
    )
    db_user_group.users.append(user)
    db.add(db_user_group)
    await db.commit()
    await db.refresh(db_user_group)
    return db_user_group


async def get_user_groups(db: AsyncSession) -> list[UserGroup]:
    result = await db.execute(select(UserGroup))
    return result.scalars().all()
